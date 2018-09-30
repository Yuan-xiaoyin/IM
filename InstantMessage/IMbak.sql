-- MySQL dump 10.13  Distrib 5.7.22, for macos10.13 (x86_64)
--
-- Host: localhost    Database: IM
-- ------------------------------------------------------
-- Server version	5.7.22

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
-- Table structure for table `chat_history`
--

DROP TABLE IF EXISTS `chat_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chat_history` (
  `UID` int(11) DEFAULT NULL,
  `FID` int(11) DEFAULT NULL,
  `msg` varchar(1024) DEFAULT NULL,
  `send_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_history`
--

LOCK TABLES `chat_history` WRITE;
/*!40000 ALTER TABLE `chat_history` DISABLE KEYS */;
INSERT INTO `chat_history` VALUES (10012,10013,'好的','2018-08-27 12:42:28'),(10013,10012,'哈喽','2018-08-27 13:15:14'),(10012,10013,'可以的','2018-08-27 13:15:28'),(10013,10012,'dd','2018-08-28 20:01:24'),(10012,10013,'nihaoa','2018-08-28 21:21:21'),(10013,10012,'说句话','2018-08-28 21:25:35'),(10012,10013,'HELLO','2018-08-28 22:05:59'),(10013,10012,'呵呵','2018-08-28 22:06:52'),(10013,10012,'在吗','2018-08-28 22:17:08'),(10012,10013,'在的啊','2018-08-28 22:17:17'),(10013,10012,'我来了','2018-08-28 22:22:10'),(10012,10013,'你来了？','2018-08-28 22:22:24'),(10013,10012,'我又来了','2018-08-28 22:25:29'),(10012,10013,'年来干哈','2018-08-28 22:25:40'),(10012,10013,'come on','2018-08-28 22:30:09'),(10012,10013,'\nlalaal','2018-08-28 22:30:17'),(10013,10012,'lululu','2018-08-28 22:30:24'),(10013,10012,'\nlolo','2018-08-28 22:30:33'),(10013,9999,'嘚啵嘚啵','2018-08-28 22:56:20'),(10012,9999,'？？','2018-08-28 22:56:42'),(10012,9999,'laile','2018-08-28 23:06:40'),(10013,9999,'heh','2018-08-28 23:06:46'),(10012,9999,'hei','2018-08-28 23:19:10'),(10013,9999,'wolele','2018-08-28 23:20:44'),(10013,9999,'haha','2018-08-28 23:47:54'),(10013,9999,'ok','2018-08-28 23:49:28'),(10012,9999,'o什么k','2018-08-28 23:49:41'),(10013,9999,'\n你是不是傻','2018-08-28 23:49:49'),(10013,9999,'嘚啵嘚啵嘚啵','2018-08-28 23:54:28'),(10013,9999,'\n啦啦','2018-08-28 23:55:02'),(10013,9999,'\n哦哦','2018-08-28 23:55:05'),(10013,9999,'\n啊啊','2018-08-28 23:55:07');
/*!40000 ALTER TABLE `chat_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `friends`
--

DROP TABLE IF EXISTS `friends`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `friends` (
  `UID` int(11) NOT NULL,
  `FID` int(11) DEFAULT NULL,
  `add_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `friends`
--

LOCK TABLES `friends` WRITE;
/*!40000 ALTER TABLE `friends` DISABLE KEYS */;
INSERT INTO `friends` VALUES (10001,10002,'2018-08-19 00:19:15'),(10001,10003,'2018-08-19 00:32:41'),(10001,10004,'2018-08-19 00:33:02'),(10001,10009,'2018-08-19 00:48:19'),(10001,10010,'2018-08-19 00:49:35'),(10001,10005,'2018-08-19 01:56:31'),(10002,10003,'2018-08-19 02:52:34'),(10002,10004,'2018-08-19 02:55:52'),(10002,10005,'2018-08-19 02:59:00'),(10001,10006,'2018-08-19 03:04:08'),(10001,10007,'2018-08-19 03:13:06'),(10001,10008,'2018-08-19 03:18:07'),(10001,10011,'2018-08-19 03:25:40'),(10002,10006,'2018-08-19 03:31:06'),(10002,10007,'2018-08-19 12:20:34'),(10002,10008,'2018-08-19 12:21:42'),(10002,10009,'2018-08-19 12:33:05'),(10002,10010,'2018-08-19 14:10:04'),(10002,10011,'2018-08-19 14:15:31'),(10003,10004,'2018-08-19 14:25:43'),(10003,10006,'2018-08-19 14:25:56'),(10003,10007,'2018-08-19 14:27:37'),(10003,10008,'2018-08-19 14:31:32'),(10003,10009,'2018-08-19 14:44:51'),(10003,10010,'2018-08-19 14:47:34'),(10003,10011,'2018-08-19 14:59:31'),(10003,10005,'2018-08-19 15:00:54'),(10012,10001,'2018-08-19 15:47:09'),(10013,10001,'2018-08-19 16:45:55'),(10012,10013,'2018-08-19 22:00:38'),(10012,10011,'2018-08-19 22:00:55'),(10012,10008,'2018-08-19 22:01:16');
/*!40000 ALTER TABLE `friends` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_info`
--

DROP TABLE IF EXISTS `user_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_info` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `name` char(16) DEFAULT NULL,
  `passwd` char(20) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL DEFAULT '12345678',
  `register_time` datetime DEFAULT NULL,
  `last_time` datetime DEFAULT NULL,
  `nick_name` varchar(24) DEFAULT NULL,
  `logo` varchar(128) NOT NULL DEFAULT './image/user_logo.jpg',
  `status` tinyint(3) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=10014 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_info`
--

LOCK TABLES `user_info` WRITE;
/*!40000 ALTER TABLE `user_info` DISABLE KEYS */;
INSERT INTO `user_info` VALUES (10001,'HLB123','HHzzWW00','2018-08-11 11:18:04','2018-08-26 10:56:24','胡萝卜','./image/user_logo.jpg',0),(10002,'hlb001','12345678胡先生001','2018-08-12 01:55:20','2018-08-19 02:58:46','','./image/user_logo.jpg',0),(10003,'hlb002','HXS00200胡先生002','2018-08-12 02:12:11',NULL,'','./image/user_logo.jpg',0),(10004,'hlb003','hxs00300胡先生003','2018-08-12 02:13:51',NULL,'','./image/user_logo.jpg',0),(10005,'wmyqxmj','wmyqxmjMMMmmm','2018-08-12 02:15:49',NULL,'','./image/user_logo.jpg',0),(10006,'yonghuming','woshimima','2018-08-12 02:18:47','2018-08-12 02:19:08','我是昵称','./image/user_logo.jpg',0),(10007,'hlb1234','hhhhhhhh','2018-08-12 15:52:42',NULL,'hhh','./image/user_logo.jpg',0),(10008,'hlb12345','hhhhhhhh','2018-08-12 15:52:52',NULL,'hhh','./image/user_logo.jpg',0),(10009,'ddddddd','bbbbbbbb','2018-08-14 00:10:30',NULL,'ddse','./image/user_logo.jpg',0),(10010,'dddddd','bbbbbbbb','2018-08-14 00:11:48',NULL,'dddd','./image/user_logo.jpg',0),(10011,'bbbbbb','dddddddd','2018-08-14 12:48:03',NULL,'ddd','./image/user_logo.jpg',0),(10012,'hlb100','11111111','2018-08-19 15:28:05','2018-08-29 00:43:51','Hey Man','./image/user_logo.jpg',0),(10013,'hlb101','11111111','2018-08-19 16:45:32','2018-08-28 23:54:06','集合进攻暗影主宰','./image/user_logo.jpg',0);
/*!40000 ALTER TABLE `user_info` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-08-29  9:07:28
