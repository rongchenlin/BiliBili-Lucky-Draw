-- MySQL dump 10.13  Distrib 5.7.19, for Win64 (x86_64)
--
-- Host: 123.56.224.232    Database: bilibili
-- ------------------------------------------------------
-- Server version	5.7.40-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `t_fans`
--

-- CREATE DATABASE bilibili;
use bilibili;

DROP TABLE IF EXISTS `t_fans`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_fans` (
  `fans_id` varchar(50) NOT NULL,
  `flag` int(11) DEFAULT NULL,
  `insert_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`fans_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `t_log`
--

DROP TABLE IF EXISTS `t_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_log` (
  `ip` varchar(50) DEFAULT NULL,
  `function_name` varchar(50) DEFAULT NULL,
  `note` varchar(50) DEFAULT NULL,
  `content` varchar(2550) DEFAULT NULL,
  `insert_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `retry_dyn_id` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `t_share`
--

DROP TABLE IF EXISTS `t_share`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_share` (
  `user_id` varchar(50) DEFAULT NULL,
  `fans_id` varchar(50) DEFAULT NULL,
  `dyn_id` varchar(30) DEFAULT NULL,
  `flag` int(11) DEFAULT NULL,
  `insert_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `t_users_cnt`
--

DROP TABLE IF EXISTS `t_users_cnt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_users_cnt` (
  `user_id` varchar(50) DEFAULT NULL,
  `draw_cnt` int(11) DEFAULT NULL,
  `last_time` varchar(50) DEFAULT NULL,
  `last_draw_time` varchar(50) DEFAULT NULL,
  `insert_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-04-08 11:06:09

INSERT INTO bilibili.t_users_cnt (user_id, draw_cnt, last_time, last_draw_time, insert_time, update_time) VALUES ('8248488', 11, '2022-11-19', '2022-11-19', '2023-02-08 14:17:21', null)


-- 预设一些数据
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8478055', 13, '2023-04-11 07:33:28', '2023-03-03 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8364020', 13, '2023-03-15 07:30:36', '2023-02-22 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8284376', 13, '2023-02-25 09:36:17', '2023-05-19 14:37:37');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8269393', 13, '2023-02-21 01:46:52', '2023-01-24 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8254607', 13, '2023-02-13 13:15:27', '2023-06-23 05:20:09');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8499477', 12, '2023-04-16 07:30:41', '2023-02-24 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8498340', 12, '2023-04-16 07:30:30', '2023-04-01 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8498108', 12, '2023-04-16 07:30:29', '2023-03-14 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8497820', 12, '2023-04-16 07:30:24', '2023-05-01 16:08:54');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8497257', 12, '2023-04-16 07:30:20', '2023-03-08 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8495605', 12, '2023-04-16 07:30:02', '2023-03-14 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8494315', 12, '2023-04-15 07:40:42', '2023-03-26 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8493796', 12, '2023-04-15 07:40:38', '2023-01-09 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8493767', 12, '2023-04-15 07:40:37', '2023-03-02 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8493456', 12, '2023-04-15 07:40:34', '2023-03-20 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8491793', 12, '2023-04-15 07:40:13', '2023-02-22 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8491518', 12, '2023-04-15 07:40:09', '2023-01-12 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8491434', 12, '2023-04-14 07:30:41', '2023-04-27 09:36:02');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8491323', 12, '2023-04-14 07:30:40', '2023-02-03 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8491250', 12, '2023-04-14 07:30:38', '2023-04-01 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8490148', 12, '2023-04-14 07:30:26', '2023-01-09 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8489420', 12, '2023-04-14 07:30:19', '2023-01-14 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8489048', 12, '2023-04-14 07:30:14', '2023-01-27 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8489026', 12, '2023-04-14 07:30:13', '2023-01-22 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8488598', 12, '2023-04-14 07:30:07', '2023-01-16 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8488468', 12, '2023-04-14 07:30:06', '2023-02-21 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8487566', 12, '2023-04-13 07:30:52', '2023-04-18 03:47:31');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8487472', 12, '2023-04-13 07:30:50', '2023-02-27 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8487379', 12, '2023-04-13 07:30:47', '2023-01-16 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8486715', 12, '2023-04-13 07:30:40', '2023-05-01 13:17:16');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8486556', 12, '2023-04-13 07:30:37', '2023-01-06 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8486405', 12, '2023-04-13 07:30:35', '2023-01-20 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8485761', 12, '2023-04-13 07:30:32', '2023-03-03 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8485406', 12, '2023-04-13 07:30:28', '2023-03-31 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8484806', 12, '2023-04-13 07:30:20', '2023-03-29 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8484479', 12, '2023-04-13 07:30:14', '2023-01-26 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8484390', 12, '2023-04-13 07:30:13', '2023-01-29 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8484316', 12, '2023-04-13 07:30:10', '2023-01-24 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8482866', 12, '2023-04-12 07:30:39', '2023-03-31 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8482794', 12, '2023-04-12 07:30:38', '2023-03-16 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8481739', 12, '2023-04-12 07:30:28', '2023-01-24 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8481645', 12, '2023-04-12 07:30:26', '2023-01-25 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8481116', 12, '2023-04-12 07:30:22', '2023-02-04 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8479989', 12, '2023-04-12 07:30:08', '2023-04-28 06:50:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8480034', 12, '2023-04-12 07:30:08', '2023-04-26 06:09:05');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8479775', 12, '2023-04-12 07:30:06', '2023-02-24 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8477357', 12, '2023-04-11 07:33:21', '2023-01-22 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8476862', 12, '2023-04-11 07:33:13', '2023-03-15 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8475590', 12, '2023-04-11 07:33:04', '2023-02-17 00:00:00');
INSERT INTO bilibili.t_fans (fans_id, flag, insert_time, update_time) VALUES ('8475594', 12, '2023-04-11 07:33:04', '2023-02-24 00:00:00');
