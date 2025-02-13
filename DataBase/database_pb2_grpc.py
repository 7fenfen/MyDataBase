# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import database_pb2 as database__pb2

GRPC_GENERATED_VERSION = '1.68.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in database_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class DatabaseServiceStub(object):
    """======= 服务定义 =======
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.QueryDistance = channel.unary_unary(
                '/DatabaseService/QueryDistance',
                request_serializer=database__pb2.NearestQueryRequest.SerializeToString,
                response_deserializer=database__pb2.DisResponse.FromString,
                _registered_method=True)
        self.QueryNeedNum = channel.unary_unary(
                '/DatabaseService/QueryNeedNum',
                request_serializer=database__pb2.NumRequest.SerializeToString,
                response_deserializer=database__pb2.QueryResponse.FromString,
                _registered_method=True)
        self.AntiNearestQuery = channel.unary_unary(
                '/DatabaseService/AntiNearestQuery',
                request_serializer=database__pb2.AntiNearestQueryRequest.SerializeToString,
                response_deserializer=database__pb2.QueryResponse.FromString,
                _registered_method=True)
        self.EncryptedQueryDistance = channel.unary_unary(
                '/DatabaseService/EncryptedQueryDistance',
                request_serializer=database__pb2.EncryptedNearestQueryRequest.SerializeToString,
                response_deserializer=database__pb2.EncryptedDisResponse.FromString,
                _registered_method=True)
        self.EncryptedQueryNeedNum = channel.unary_unary(
                '/DatabaseService/EncryptedQueryNeedNum',
                request_serializer=database__pb2.NumRequest.SerializeToString,
                response_deserializer=database__pb2.EncryptedQueryResult.FromString,
                _registered_method=True)
        self.CompareQuery = channel.unary_unary(
                '/DatabaseService/CompareQuery',
                request_serializer=database__pb2.CompareOtherDatabase.SerializeToString,
                response_deserializer=database__pb2.CompareResponse.FromString,
                _registered_method=True)


class DatabaseServiceServicer(object):
    """======= 服务定义 =======
    """

    def QueryDistance(self, request, context):
        """======= federation向database发送的数据类型 =======
        最近邻查询的信道
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QueryNeedNum(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AntiNearestQuery(self, request, context):
        """反向最近邻查询的信道
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EncryptedQueryDistance(self, request, context):
        """加密最近邻查询的信道
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EncryptedQueryNeedNum(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CompareQuery(self, request, context):
        """======= database向database发送的数据类型 =======
        反向最近邻查询时用于跨数据库比较距离
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DatabaseServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'QueryDistance': grpc.unary_unary_rpc_method_handler(
                    servicer.QueryDistance,
                    request_deserializer=database__pb2.NearestQueryRequest.FromString,
                    response_serializer=database__pb2.DisResponse.SerializeToString,
            ),
            'QueryNeedNum': grpc.unary_unary_rpc_method_handler(
                    servicer.QueryNeedNum,
                    request_deserializer=database__pb2.NumRequest.FromString,
                    response_serializer=database__pb2.QueryResponse.SerializeToString,
            ),
            'AntiNearestQuery': grpc.unary_unary_rpc_method_handler(
                    servicer.AntiNearestQuery,
                    request_deserializer=database__pb2.AntiNearestQueryRequest.FromString,
                    response_serializer=database__pb2.QueryResponse.SerializeToString,
            ),
            'EncryptedQueryDistance': grpc.unary_unary_rpc_method_handler(
                    servicer.EncryptedQueryDistance,
                    request_deserializer=database__pb2.EncryptedNearestQueryRequest.FromString,
                    response_serializer=database__pb2.EncryptedDisResponse.SerializeToString,
            ),
            'EncryptedQueryNeedNum': grpc.unary_unary_rpc_method_handler(
                    servicer.EncryptedQueryNeedNum,
                    request_deserializer=database__pb2.NumRequest.FromString,
                    response_serializer=database__pb2.EncryptedQueryResult.SerializeToString,
            ),
            'CompareQuery': grpc.unary_unary_rpc_method_handler(
                    servicer.CompareQuery,
                    request_deserializer=database__pb2.CompareOtherDatabase.FromString,
                    response_serializer=database__pb2.CompareResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'DatabaseService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('DatabaseService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class DatabaseService(object):
    """======= 服务定义 =======
    """

    @staticmethod
    def QueryDistance(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/DatabaseService/QueryDistance',
            database__pb2.NearestQueryRequest.SerializeToString,
            database__pb2.DisResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def QueryNeedNum(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/DatabaseService/QueryNeedNum',
            database__pb2.NumRequest.SerializeToString,
            database__pb2.QueryResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def AntiNearestQuery(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/DatabaseService/AntiNearestQuery',
            database__pb2.AntiNearestQueryRequest.SerializeToString,
            database__pb2.QueryResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def EncryptedQueryDistance(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/DatabaseService/EncryptedQueryDistance',
            database__pb2.EncryptedNearestQueryRequest.SerializeToString,
            database__pb2.EncryptedDisResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def EncryptedQueryNeedNum(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/DatabaseService/EncryptedQueryNeedNum',
            database__pb2.NumRequest.SerializeToString,
            database__pb2.EncryptedQueryResult.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def CompareQuery(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/DatabaseService/CompareQuery',
            database__pb2.CompareOtherDatabase.SerializeToString,
            database__pb2.CompareResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
