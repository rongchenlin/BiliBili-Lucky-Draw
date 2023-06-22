# B站抽奖转发——薅羊毛脚本

## 简介

常刷B站的伙伴们，是不是每次看到Up主的抽奖活动都行动不已，毕竟`抽奖总得试试吗，万一中奖了呢`，然后一波关注+转发之后，迎来的每每都是`从不缺席，从不中奖`。

So，如果有个小脚本能够帮助你去看看**今天有哪些Up有抽奖活动，然后还能帮助你自动进行抽奖（转发动态+关注）**，那么你是不是可以花更多时间去看看二次元动漫呀。本着有羊毛一起薅的想法，我做了一个B站自动抽奖活动转发的小脚本，帮助伙伴们自动参与Up主的活动转发，提高伙伴们的中奖率，同时还能解放大家的双手，开开心心薅羊毛。

本薅羊毛脚本，虽然目前只是一个V0的脚本，但是已经正常运转几个月了，我也薅到了一点儿羊毛啦，下面就来看看它是怎么玩的吧。

**声明**: <u>**此脚本仅用于学习和测试，作者本人并不对其负责，请于运行测试完成后自行删除，请勿滥用！**</u>

## 效果

本程序内置一个扫描脚本，该脚本去挖掘那些经常转发抽奖动态的伙伴，然后每天定时去扫描他们今天的动态信息，随后再利用一个抽奖动态识别与转发脚本来进行活动参与，转发后的效果是这样的：

<img src="img/Readme.assets/image-20230518202338234.png" alt="image-20230518202338234" style="zoom:67%;" />

## docker部署

### 1.准备工作【以后更新版本不需要这个步骤】

#### 1.1 创建数据库

在MySQL5.7版本以上数据库执行下面的脚本：`bilibili-dump.sql`

#### 1.2 创建selenium环境

```dockerfile
docker run -d -p 5555:4444 -p 7900:7900 --shm-size="1g" -e SE_NODE_MAX_SESSIONS=5 -e SE_NODE_MAX_INSTANCES=5 selenium/standalone-chrome:latest
```

可以访问 [your_ip:5555]()，如果出现下面的界面，说明selenium环境创建成功

![image-20230622125900829](img/Readme.assets/image-20230622125900829.png)

#### 1.3 修改个人配置

在`globals.py`文件中，修改数据库，服务器IP信息

![image-20230622155928146](img/Readme.assets/image-20230622155928146.png)

### 2.启动程序

#### 2.1 启动生成Cookie的脚本

##### 2.1.1 构建镜像

```dockerfile
docker build -t bilibili_gen_cookie -f Dockerfile.GenCookie .
```

##### 2.1.2 启动容器

```dockerfile
docker run bilibili_gen_cookie
```

##### 2.1.3 扫码登录

访问 [your_ip:5555]()，扫码登录,自动生成Cookie

![funtion](img/Readme.assets/funtion-16874096887972.gif)

##### 2.1.4 检查Cookie

到项目所在文件夹，查看是否生成Cookie

<img src="img/Readme.assets/image-20230622124901169.png" alt="image-20230622124901169" style="zoom:150%;" />

<img src="img/Readme.assets/image-20230622124931448.png" alt="image-20230622124931448" style="zoom:200%;" />

#### 2.2 启动转发动态脚本

##### 2.2.1 构建镜像

```java
docker build -t bilibili_dynamic_share .
```

##### 2.2.2 运行镜像

```java
docker run bilibili_dynamic_share
```

## TODO

- [x] 项目采用Docker部署
- [x] 扫描B站二维码登录B站，自动生成Cookie并保存到本地项目文件夹cookie中
- [x] 登录过期，使用Cookie续期
- [ ] 每日任务执行情况推送（之前用的方糖酱，后续将重新加入）
- [ ] 将数据库搭建的工作使用Docker部署
- [ ] 过期动态的删除
- [ ] 接入B站UP主每日总结的抽奖动态列表，自动完成对其转发
