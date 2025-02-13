import concurrent.futures
import grpc
from concurrent import futures
from functools import cmp_to_key
import database_pb2
import database_pb2_grpc
import federation_pb2
import federation_pb2_grpc
from threading import Thread
import mysql.connector
from mysql.connector import Error
import tenseal as ts
from DataBaseConfig import configs
from EncryptedMaxHeap import EncryptedMaxHeap, encrypt_compare


class DatabaseServiceServicer(database_pb2_grpc.DatabaseServiceServicer):
    def __init__(self, database_id, other_database_address, config, options):
        self.database_id = database_id
        # 建立与其他数据库的信道
        self.other_database = self.stub_init(other_database_address, options)
        # 建立与联邦端的信道
        self.federation_stub = federation_pb2_grpc.FederationServiceStub(
            grpc.insecure_channel("localhost:50051", options))
        # 创建自己的加密环境
        self.context = self.create_context()
        # 获取数据
        self.data = self.get_data(config)
        # 储存容器(用于跨方法调用)
        self.distances = []  # 用来存储到查询点的距离
        self.enc_distances = []  # 用来存储到查询点的加密距离
        # 联邦传入的加密环境
        self.database_party_context = None

    @staticmethod
    def stub_init(addresses, options):
        stubs = []
        for address in addresses:
            channel = grpc.insecure_channel(address, options)
            stubs.append(database_pb2_grpc.DatabaseServiceStub(channel))

        return stubs

    @staticmethod
    def create_context():
        context = ts.context(
            ts.SCHEME_TYPE.CKKS,
            poly_modulus_degree=8192,
            coeff_mod_bit_sizes=[40, 21, 21, 40]
        )
        context.generate_galois_keys()
        context.global_scale = 2 ** 21
        return context

    def get_data(self, config):
        try:
            # 初始化连接和游标
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()
            # 定义参数化查询
            query = "SELECT position_x, position_y, min_dis FROM data"
            # 执行查询
            cursor.execute(query)
            # 获取查询结果
            records = cursor.fetchall()
            print(f'Database{self.database_id} Load Data Successfully')
            # 返回结果
            return records

        except Error as e:
            print("Error while connecting to MySQL", e)

    @staticmethod
    def calculate_distance(x1, y1, x2, y2):
        return (x2 - x1) ** 2 + (y2 - y1) ** 2

    # 定义一个处理单个数据的函数
    def process_data(self, data_entry, enc_query_x, enc_query_y, context):
        x, y, _ = data_entry
        # 加密x, y
        enc_x = ts.ckks_vector(context, [x])
        enc_y = ts.ckks_vector(context, [y])
        # 计算距离(加密后)
        distance = self.calculate_distance(enc_query_x, enc_query_y, enc_x, enc_y)
        return (distance, x, y)

    def QueryDistance(self, request, context):
        query_x = request.position_x
        query_y = request.position_y
        query_num = request.query_num

        self.distances = []  # 清空距离数据
        for x, y, _ in self.data:
            distance = self.calculate_distance(query_x, query_y, x, y)
            self.distances.append((distance, x, y))

        # 按照距离升序排序
        self.distances.sort(key=lambda x: x[0])

        # 返回前query_num个距离
        nearest_distances = [database_pb2.DisResult(
            distance=distance)
            for distance, _, _ in self.distances[:query_num]]

        return database_pb2.DisResponse(results=nearest_distances)

    def QueryNeedNum(self, request, context):
        num_points = request.need_num

        # 直接根据已排序的距离列表返回最接近的num_points个点
        nearest_points = self.distances[:num_points]

        results = [
            database_pb2.QueryResult(
                position_x=x,
                position_y=y,
                database_id=self.database_id
            )
            for _, x, y in nearest_points
        ]

        # 清空 distances，以便下一次查询时可以重新计算
        self.distances = []
        return database_pb2.QueryResponse(results=results)

    def AntiNearestQuery(self, request, context):
        temp_result = []
        final_result = []
        query_x = request.position_x
        query_y = request.position_y

        # 看有没有以查询点为最小最近邻的点
        for x, y, min_dis in self.data:
            dis = self.calculate_distance(query_x, query_y, x, y)
            if dis < min_dis:
                temp_result.append((x, y, dis))
        # 序列化加密环境
        serialized_context = self.context.serialize()
        # 与其它数据库比较
        for item in temp_result:
            # 加密数据
            enc_position_x = ts.ckks_vector(self.context, [item[0]]).serialize()
            enc_position_y = ts.ckks_vector(self.context, [item[1]]).serialize()
            enc_min_dis = ts.ckks_vector(self.context, [item[2]]).serialize()
            # 创建结果列表
            results = []
            for stub in self.other_database:
                response = stub.CompareQuery(
                    database_pb2.CompareOtherDatabase(
                        context=serialized_context,
                        position_x=enc_position_x,
                        position_y=enc_position_y,
                        min_dis=enc_min_dis
                    )
                )
                results.extend(ts.ckks_vector_from(self.context, response.results).decrypt())
            # 排除与其它数据库中点最近的点
            flag = False
            for result in results:
                if round(result) < 0:
                    flag = True
            if not flag:
                final_result.append(database_pb2.QueryResult(
                    position_x=item[0],
                    position_y=item[1],
                    database_id=self.database_id))

        return database_pb2.QueryResponse(results=final_result)

    def EncryptedQueryDistance(self, request, context):
        # 接收数据
        query_num = request.query_num
        # 还原加密环境
        self.database_party_context = ts.context_from(request.context)
        # 把数据加载到新的加密环境
        enc_query_x = ts.ckks_vector_from(self.database_party_context, request.position_x)
        enc_query_y = ts.ckks_vector_from(self.database_party_context, request.position_y)

        self.enc_distances = []  # 清空距离数据
        temp_distances = []

        # 使用 ThreadPoolExecutor 来并行计算
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = []
            for data_entry in self.data:
                results.append(
                    executor.submit(self.process_data, data_entry,
                                    enc_query_x, enc_query_y, self.database_party_context))
            # 获取结果
            for future in concurrent.futures.as_completed(results):
                temp_distances.append(future.result())

        # 用大顶堆找出前query_num个元素
        max_heap = EncryptedMaxHeap(query_num)
        for item in temp_distances:
            max_heap.push(item)
        self.enc_distances = max_heap.get_elements()

        # 堆的顺序不是按照大小的，所以还需要简单排序一下
        self.enc_distances.sort(key=cmp_to_key(encrypt_compare))

        # 返回前query_num个距离
        nearest_distances = [database_pb2.EncryptedDisResult(
            distance=distance.serialize())
            for distance, _, _ in self.enc_distances]

        return database_pb2.EncryptedDisResponse(results=nearest_distances)

    def EncryptedQueryNeedNum(self, request, context):
        # 接收数据
        num_points = request.need_num
        # 直接根据已排序的距离列表返回最接近的num_points个点
        nearest_points = self.enc_distances[:num_points]
        x = [row[1] for row in nearest_points]
        y = [row[2] for row in nearest_points]
        enc_x = ts.ckks_vector(self.database_party_context, x)
        enc_y = ts.ckks_vector(self.database_party_context, y)

        # 清空 distances，以便下一次查询时可以重新计算
        self.enc_distances = []

        # 构建返回数据
        return database_pb2.EncryptedQueryResult(
            position_x=enc_x.serialize(),
            position_y=enc_y.serialize(),
            database_id=self.database_id
        )

    def CompareQuery(self, request, context):
        # 还原加密环境
        database_party_context = ts.context_from(request.context)
        # 把数据加载到新的加密环境
        enc_query_x = ts.ckks_vector_from(database_party_context, request.position_x)
        enc_query_y = ts.ckks_vector_from(database_party_context, request.position_y)
        enc_min_dis = ts.ckks_vector_from(database_party_context, request.min_dis)
        # x,y单独的列表
        x = [row[0] for row in self.data]
        y = [row[1] for row in self.data]
        # 加密x,y
        enc_x = ts.ckks_vector(database_party_context, x)
        enc_y = ts.ckks_vector(database_party_context, y)
        # 计算距离(加密后)
        distance = self.calculate_distance(enc_query_x, enc_query_y, enc_x, enc_y)
        dis_diff = distance - enc_min_dis
        # 返回结果
        return database_pb2.CompareResponse(results=dis_diff.serialize())


def serve(database_id, other_database_address, port, config, options):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options=options)
    # 添加查询服务
    database_pb2_grpc.add_DatabaseServiceServicer_to_server(
        DatabaseServiceServicer(database_id, other_database_address, config, options), server)
    # 监听端口
    server.add_insecure_port(f'[::]:{port}')
    print(f"Database Server {database_id} started on ports {port} \n")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    # 数据库地址
    databases = ["localhost:60051", "localhost:60052", "localhost:60053"]

    # 设置消息大小为 100MB
    max_msg_size = 100 * 1024 * 1024
    msg_options = [
        ('grpc.max_send_message_length', max_msg_size),
        ('grpc.max_receive_message_length', max_msg_size),
    ]

    # 建立与联邦端的信道
    federation_stub = federation_pb2_grpc.FederationServiceStub(
        grpc.insecure_channel("localhost:50051", msg_options))

    # 启动多个服务端
    thread1 = Thread(target=serve, args=(1, [databases[1], databases[2]], 60051, configs[0], msg_options))
    thread2 = Thread(target=serve, args=(2, [databases[0], databases[2]], 60052, configs[1], msg_options))
    thread3 = Thread(target=serve, args=(3, [databases[0], databases[1]], 60053, configs[2], msg_options))

    thread1.start()
    thread2.start()
    thread3.start()

    # 等待线程结束
    thread1.join()
    thread2.join()
    thread3.join()
