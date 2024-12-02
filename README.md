# FederatedDataBase

## 项目简介

科研课堂的大作业,是一个基于gRPC通信实现的具有一定加密功能的联邦数据库,
可以对指定数据进行最近邻查询

## 项目结构

### 后端

后端要求实现`server.py`,`database.py`两个程序

分别实现**联邦数据库的服务端**以及每个独立的**数据库本体**

客户端发送查询的数据请求,服务端使用`Flask`服务接收后发送查询操作给服务端管控下的数据库,

数据库在本地查询后,用同态加密算法与其它数据库进行比较,最后返回给服务端唯一的结果

由此防止因泄露数据过多导致的安全性降低

服务端再将结果返回给客户

### 前端
基于`Flutter`框架进行搭建,把注册用户分为**普通用户**和**管理员**

用户登陆后只能针对已有的联邦数据库(目前暂定只有一个)进行查询操作,并获得查询结果

管理员除了可以查询之外,还具有对数据库的**管理权限**,可以通过上传`json`文件添加一个数据库,
并且可以查看服务端运行过程中导出的日志

建议实现`/check`,`/add`两个路由来实现上述功能

## 项目依赖

建议安装`grpcio`,`tenseal`等软件包进行开发
```
pip install grpcio grpcio-tools tenseal
```

## 项目运行

先运行`database.py`
```shell
python DatabaseServer.py
```
再运行`server.py`
```shell
python FederatedQuery.py
```

## 目前想到的问题
1. gRPC(远程过程调用)是一个适用于服务器端进行通信的协议,
因此适用于`server`和`database`间进行相互通信,
至于`client`和`server`间的通信我想沿用`Flask`进行设计

2. 目前较为稳定的同态加密库没有官方的python软件包,具体如何配置有待学习

3. 数据库的存储问题,前端需要把已有数据库进行渲染,所以我们貌似要**用数据库存"数据库"**,

    要不是数据库间需要同态加密后进行通信,我都想用真的数据库(无语)

### 剩下的想到了再写吧