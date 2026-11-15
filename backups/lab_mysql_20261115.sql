-- MySQL dump 10.13  Distrib 8.0.46, for Linux (x86_64)
--
-- Host: localhost    Database: my_lab
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `my_lab`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `my_lab` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `my_lab`;

--
-- Table structure for table `ai_title`
--

DROP TABLE IF EXISTS `ai_title`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ai_title` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime NOT NULL COMMENT '创建时间',
  `updated_at` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `ix_ai_title_user_id` (`user_id`),
  CONSTRAINT `ai_title_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='AI 标题表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ai_title`
--

LOCK TABLES `ai_title` WRITE;
/*!40000 ALTER TABLE `ai_title` DISABLE KEYS */;
INSERT INTO `ai_title` VALUES (1,4,'简单的问候','2026-10-25 21:22:15','2026-10-25 21:22:15'),(2,4,'简单的问候','2026-10-25 21:23:48','2026-10-25 21:23:48'),(3,4,'色情低俗内容','2026-10-25 21:24:02','2026-10-25 21:24:02'),(4,4,'e','2026-10-25 21:33:26','2026-10-25 21:33:26'),(5,4,'打招呼','2026-10-25 21:33:47','2026-10-25 21:33:47'),(6,4,'字母e标题','2026-10-25 21:35:32','2026-10-25 21:35:32'),(7,4,'用户问候','2026-10-25 21:38:45','2026-10-25 21:38:45'),(8,4,'用户说e','2026-10-25 21:38:47','2026-10-25 21:38:47'),(9,4,'标题：e','2026-10-25 21:42:28','2026-10-25 21:42:28'),(10,4,'标题：w','2026-10-25 21:42:36','2026-10-25 21:42:36'),(11,4,'2','2026-10-25 21:42:49','2026-10-25 21:42:49'),(12,4,'hello','2026-10-25 21:43:00','2026-10-25 21:43:00'),(13,4,'重复的数字串','2026-10-25 21:43:11','2026-10-25 21:43:11'),(14,4,'用户说e','2026-10-25 21:52:29','2026-10-25 21:52:29'),(15,4,'eee','2026-10-25 22:11:41','2026-10-25 22:11:41');
/*!40000 ALTER TABLE `ai_title` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('3e02e66408a2');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lab`
--

DROP TABLE IF EXISTS `lab`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lab` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '实验室名',
  `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '描述',
  `image` varchar(70) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '图片',
  `capacity` int NOT NULL COMMENT '容量',
  `open_time` time DEFAULT NULL COMMENT '开放时间',
  `close_time` time DEFAULT NULL COMMENT '结束时间',
  `status` int NOT NULL COMMENT '状态',
  `created_at` datetime NOT NULL COMMENT '创建时间',
  `updated_at` datetime NOT NULL COMMENT '更新时间',
  `manager_id` int NOT NULL COMMENT '管理员id',
  `building` int NOT NULL COMMENT '所属楼层号',
  `floor` int NOT NULL COMMENT '所属楼层',
  `area` int NOT NULL COMMENT '占地面积(m2)',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='实验室表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lab`
--

LOCK TABLES `lab` WRITE;
/*!40000 ALTER TABLE `lab` DISABLE KEYS */;
INSERT INTO `lab` VALUES (1,'人工智能实验室','面向机器学习与深度学习研究,配备 GPU 服务器','/uploads/20261017153419203181_da1fac23.png',30,'08:00:00','22:00:00',1,'2026-10-16 23:25:01','2026-10-17 15:34:20',1,1,3,120),(2,'大数据实验室','数据挖掘与可视化教学使用','/uploads/20261017182429798919_37d719e1.png',40,'08:30:00','21:00:00',1,'2026-10-16 23:25:01','2026-10-17 18:24:31',1,1,4,150),(3,'网络安全实验室','攻防演练与渗透测试实训环境',NULL,20,'09:00:00','20:00:00',1,'2026-10-16 23:25:01','2026-10-16 23:25:01',2,2,2,90),(4,'物联网实验室','传感器与嵌入式开发平台','uploads/lab/iot.jpg',25,'08:00:00','18:00:00',1,'2026-10-16 23:25:01','2026-10-16 23:25:01',2,2,3,100),(5,'云计算实验室','虚拟化与容器编排实验,支持远程接入',NULL,35,'00:00:00','23:59:00',1,'2026-10-16 23:25:01','2026-10-16 23:25:01',3,3,1,200),(6,'软件工程实验室','敏捷开发与项目管理实训,暂未开放',NULL,45,'08:00:00','18:00:00',0,'2026-10-16 23:25:01','2026-10-16 23:25:01',3,3,5,160),(8,'阿文','',NULL,0,'09:00:00','20:00:00',1,'2026-10-17 18:19:29','2026-10-17 18:19:39',1,0,0,0);
/*!40000 ALTER TABLE `lab` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lab_book`
--

DROP TABLE IF EXISTS `lab_book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lab_book` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` int NOT NULL COMMENT '用户id',
  `lab_id` int NOT NULL COMMENT '实验室id',
  `start_time` time NOT NULL COMMENT '预约开始时间',
  `end_time` time NOT NULL COMMENT '预约结束时间',
  `people_count` int NOT NULL COMMENT '预约人数',
  `status` int NOT NULL COMMENT '预约状态: 0-待审核,1-审核通过,2-,3-已取消',
  `reviewer_id` int NOT NULL COMMENT '审核人id',
  `reviewer_remark` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '审核人备注',
  `created_at` datetime NOT NULL COMMENT '创建时间',
  `updated_at` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `ix_lab_book_reviewer_id` (`reviewer_id`),
  KEY `ix_lab_book_user_id` (`user_id`),
  CONSTRAINT `lab_book_ibfk_1` FOREIGN KEY (`reviewer_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `lab_book_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='实验室预约表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lab_book`
--

LOCK TABLES `lab_book` WRITE;
/*!40000 ALTER TABLE `lab_book` DISABLE KEYS */;
INSERT INTO `lab_book` VALUES (1,2,1,'09:00:00','11:00:00',10,1,1,'','2026-10-16 23:25:01','2026-11-14 15:40:31'),(2,3,1,'14:00:00','16:00:00',20,1,1,'','2026-10-16 23:25:01','2026-10-17 17:16:43'),(3,2,2,'10:00:00','12:00:00',30,2,1,'','2026-10-16 23:25:01','2026-10-17 17:16:45'),(4,3,3,'15:00:00','17:00:00',15,1,2,'通过','2026-10-16 23:25:01','2026-10-16 23:25:01'),(5,1,3,'08:30:00','10:30:00',12,0,2,NULL,'2026-10-16 23:25:01','2026-10-16 23:25:01'),(6,2,4,'13:00:00','15:00:00',8,3,2,'申请人主动取消','2026-10-16 23:25:01','2026-10-16 23:25:01'),(7,3,5,'19:00:00','21:00:00',25,1,3,'晚间时段可用','2026-10-16 23:25:01','2026-10-16 23:25:01'),(8,1,5,'13:00:00','15:00:00',18,0,3,NULL,'2026-10-16 23:25:01','2026-10-16 23:25:01'),(9,2,6,'09:00:00','11:00:00',6,3,3,'实验室未开放','2026-10-16 23:25:01','2026-10-16 23:25:01'),(10,3,6,'11:00:00','13:00:00',40,0,3,NULL,'2026-10-16 23:25:01','2026-10-16 23:25:01');
/*!40000 ALTER TABLE `lab_book` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permission`
--

DROP TABLE IF EXISTS `permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `permission` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键',
  `code` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '权限标识: 如 lab:create,user:list',
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '权限名',
  `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '描述',
  `status` int NOT NULL COMMENT '状态: 0-禁用,1-启用',
  `created_at` datetime NOT NULL COMMENT '创建时间',
  `updated_at` datetime NOT NULL COMMENT '更新时间',
  `pid` int DEFAULT NULL COMMENT '父级权限id',
  `type` int NOT NULL COMMENT '权限类型: 1-菜单,2-按钮',
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='权限表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permission`
--

LOCK TABLES `permission` WRITE;
/*!40000 ALTER TABLE `permission` DISABLE KEYS */;
INSERT INTO `permission` VALUES (1,'system','系统管理','系统管理目录',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',NULL,1),(3,'user:list','用户管理','用户管理页面',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',1,1),(4,'user:create','创建用户','创建用户',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',3,2),(5,'user:update','修改用户','修改指定用户',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',3,2),(6,'user:delete','删除用户','删除用户',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',3,2),(7,'user:assign-role','分配角色','给用户分配角色',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',3,2),(9,'role:list','角色管理','角色管理页面',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',1,1),(10,'role:create','创建角色','创建角色',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',9,2),(11,'role:update','更新角色','更新角色',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',9,2),(12,'role:delete','删除角色','删除角色',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',9,2),(14,'menu:list','菜单管理','菜单管理页面',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',1,1),(15,'menu:create','创建菜单','创建菜单',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',14,2),(16,'menu:update','更新菜单','更新菜单',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',14,2),(17,'menu:delete','删除菜单','删除菜单',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',14,2),(18,'lab','实验室管理','实验室管理目录',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',NULL,1),(19,'lab:list','实验室列表','实验室列表菜单',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',18,1),(20,'lab:detail','实验室详情','获取实验室详情',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',19,2),(21,'lab:create','创建实验室','创建实验室',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',19,2),(22,'lab:update','更新实验室','更新实验室',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',19,2),(23,'lab:delete','删除实验室','删除实验室',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',19,2),(24,'lab:image','更新实验室图片','更新实验室图片',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',19,2),(25,'labbook:list','实验室预约管理','预约管理菜单',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',18,1),(26,'labbook:query','查询预约','获取实验室预约列表',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',25,2),(27,'labbook:create','创建预约','创建实验室预约',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',25,2),(28,'ai:chat','AI 小助手','AI 对话页面',1,'2026-11-14 18:31:18','2026-11-14 18:31:18',NULL,1),(29,'labdevice:list','设备管理','实验室设备管理页面',1,'2026-11-14 18:31:18','2026-11-14 18:31:18',18,1),(30,'user:status','启用/禁用用户','用户启用禁用按钮',1,'2026-11-14 18:31:18','2026-11-14 18:31:18',3,2),(31,'role:status','启用/禁用角色','角色启用禁用按钮',1,'2026-11-14 18:31:18','2026-11-14 18:31:18',9,2),(32,'role:assign-permission','分配权限','给角色分配权限按钮',1,'2026-11-14 18:31:18','2026-11-14 18:31:18',9,2),(33,'labbook:accept','审批预约','同意/拒绝预约按钮',1,'2026-11-14 18:31:18','2026-11-14 18:31:18',25,2);
/*!40000 ALTER TABLE `permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '角色名,可扩展: 学生/管理员/校长等',
  `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '描述',
  `status` int NOT NULL COMMENT '状态: 0-禁用,1-启用',
  `created_at` datetime NOT NULL COMMENT '创建时间',
  `updated_at` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `uq_role_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (1,'超级管理员','系统最高权限,不受权限表约束',1,'2026-10-16 23:25:00','2026-10-16 23:26:11'),(2,'管理员','实验室日常管理',1,'2026-10-16 23:25:00','2026-10-16 23:25:00'),(3,'教师','指导教师,可查看与管理自己名下的实验室',1,'2026-10-16 23:25:00','2026-10-16 23:25:00'),(4,'学生','普通学生,只读',1,'2026-10-16 23:25:00','2026-10-16 23:25:00'),(5,'访客','临时访客,只读',1,'2026-10-16 23:25:00','2026-10-16 23:26:11');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role_permission`
--

DROP TABLE IF EXISTS `role_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role_permission` (
  `role_id` int NOT NULL COMMENT '角色ID',
  `permission_id` int NOT NULL COMMENT '权限ID',
  `created_at` datetime NOT NULL COMMENT '创建时间',
  `updated_at` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`role_id`,`permission_id`),
  KEY `ix_role_permission_permission_id` (`permission_id`),
  CONSTRAINT `role_permission_ibfk_1` FOREIGN KEY (`permission_id`) REFERENCES `permission` (`id`) ON DELETE CASCADE,
  CONSTRAINT `role_permission_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色权限关联表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role_permission`
--

LOCK TABLES `role_permission` WRITE;
/*!40000 ALTER TABLE `role_permission` DISABLE KEYS */;
INSERT INTO `role_permission` VALUES (1,1,'2026-11-14 18:51:51','2026-11-14 18:51:51'),(1,3,'2026-11-14 18:51:51','2026-11-14 18:51:51'),(1,4,'2026-11-14 18:51:51','2026-11-14 18:51:51'),(1,5,'2026-11-14 18:51:51','2026-11-14 18:51:51'),(1,6,'2026-11-14 18:51:51','2026-11-14 18:51:51'),(1,7,'2026-11-14 18:51:51','2026-11-14 18:51:51'),(1,9,'2026-11-14 18:51:51','2026-11-14 18:51:51'),(1,10,'2026-11-14 18:51:51','2026-11-14 18:51:51'),(1,11,'2026-11-14 18:51:51','2026-11-14 18:51:51'),(1,12,'2026-11-14 18:51:51','2026-11-14 18:51:51'),(1,14,'2026-11-14 18:51:51','2026-11-14 18:51:51'),(1,15,'2026-11-14 18:51:51','2026-11-14 18:51:51'),(1,16,'2026-11-14 18:51:51','2026-11-14 18:51:51'),(1,17,'2026-11-14 18:51:51','2026-11-14 18:51:51'),(1,18,'2026-11-14 18:51:51','2026-11-14 18:51:51'),(1,19,'2026-11-14 18:51:51','2026-11-14 18:51:51'),(1,24,'2026-11-14 18:51:51','2026-11-14 18:51:51'),(1,25,'2026-11-14 18:51:51','2026-11-14 18:51:51'),(1,26,'2026-11-14 18:51:51','2026-11-14 18:51:51'),(1,27,'2026-11-14 18:51:51','2026-11-14 18:51:51'),(1,28,'2026-11-14 18:51:51','2026-11-14 18:51:51'),(1,29,'2026-11-14 18:51:51','2026-11-14 18:51:51'),(1,30,'2026-11-14 18:51:51','2026-11-14 18:51:51'),(1,31,'2026-11-14 18:51:51','2026-11-14 18:51:51'),(1,32,'2026-11-14 18:51:51','2026-11-14 18:51:51'),(1,33,'2026-11-14 18:51:51','2026-11-14 18:51:51'),(2,1,'2026-11-14 18:32:33','2026-11-14 18:32:33'),(2,3,'2026-11-14 18:32:33','2026-11-14 18:32:33'),(2,4,'2026-11-14 18:32:33','2026-11-14 18:32:33'),(2,5,'2026-11-14 18:32:33','2026-11-14 18:32:33'),(2,6,'2026-11-14 18:32:33','2026-11-14 18:32:33'),(2,7,'2026-11-14 18:32:33','2026-11-14 18:32:33'),(2,9,'2026-11-14 18:32:33','2026-11-14 18:32:33'),(2,10,'2026-11-14 18:32:33','2026-11-14 18:32:33'),(2,11,'2026-11-14 18:32:33','2026-11-14 18:32:33'),(2,12,'2026-11-14 18:32:33','2026-11-14 18:32:33'),(2,14,'2026-11-14 18:32:33','2026-11-14 18:32:33'),(2,15,'2026-11-14 18:32:33','2026-11-14 18:32:33'),(2,16,'2026-11-14 18:32:33','2026-11-14 18:32:33'),(2,17,'2026-11-14 18:32:33','2026-11-14 18:32:33'),(2,18,'2026-11-14 18:32:33','2026-11-14 18:32:33'),(2,19,'2026-11-14 18:32:33','2026-11-14 18:32:33'),(2,20,'2026-11-14 18:32:33','2026-11-14 18:32:33'),(2,21,'2026-11-14 18:32:33','2026-11-14 18:32:33'),(2,22,'2026-11-14 18:32:33','2026-11-14 18:32:33'),(2,23,'2026-11-14 18:32:33','2026-11-14 18:32:33'),(2,24,'2026-11-14 18:32:33','2026-11-14 18:32:33'),(2,25,'2026-11-14 18:32:33','2026-11-14 18:32:33'),(2,26,'2026-11-14 18:32:33','2026-11-14 18:32:33'),(2,27,'2026-11-14 18:32:33','2026-11-14 18:32:33'),(2,28,'2026-11-14 18:32:33','2026-11-14 18:32:33'),(2,29,'2026-11-14 18:32:33','2026-11-14 18:32:33'),(2,30,'2026-11-14 18:32:33','2026-11-14 18:32:33'),(2,31,'2026-11-14 18:32:33','2026-11-14 18:32:33'),(2,32,'2026-11-14 18:32:33','2026-11-14 18:32:33'),(2,33,'2026-11-14 18:32:33','2026-11-14 18:32:33'),(3,18,'2026-10-16 23:25:01','2026-10-16 23:25:01'),(3,19,'2026-10-16 23:25:01','2026-10-16 23:25:01'),(3,20,'2026-10-16 23:25:01','2026-10-16 23:25:01'),(3,21,'2026-10-16 23:25:01','2026-10-16 23:25:01'),(3,22,'2026-10-16 23:25:01','2026-10-16 23:25:01'),(3,23,'2026-10-16 23:25:01','2026-10-16 23:25:01'),(3,24,'2026-10-16 23:25:01','2026-10-16 23:25:01'),(3,25,'2026-10-16 23:25:01','2026-10-16 23:25:01'),(3,26,'2026-10-16 23:25:01','2026-10-16 23:25:01'),(3,27,'2026-10-16 23:25:01','2026-10-16 23:25:01'),(4,18,'2026-10-16 23:25:01','2026-10-16 23:25:01'),(4,19,'2026-10-16 23:25:01','2026-10-16 23:25:01'),(4,20,'2026-10-16 23:25:01','2026-10-16 23:25:01'),(4,25,'2026-10-16 23:25:01','2026-10-16 23:25:01'),(4,26,'2026-10-16 23:25:01','2026-10-16 23:25:01'),(4,27,'2026-10-16 23:25:01','2026-10-16 23:25:01'),(5,1,'2026-11-14 16:16:30','2026-11-14 16:16:30');
/*!40000 ALTER TABLE `role_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键',
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户名',
  `password` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '密码',
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '姓名',
  `email` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '邮箱',
  `phone` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '手机号',
  `avatar` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '头像',
  `status` int NOT NULL COMMENT '状态: 0-禁用,1-启用',
  `created_at` datetime NOT NULL COMMENT '创建时间',
  `updated_at` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'root','$2b$12$Xz6ufqTD79/EWPmAYx8hBeaRV3DZ6Q5fxbhdUr9xnSkcr7FzZLPsO','超级管理员','root@lab.local','13800000000',NULL,1,'2026-10-16 23:25:00','2026-10-16 23:25:00'),(2,'zhangsan','$2b$12$e/SL67kwH/CQPlasPXCc9OHSBjt1H6hAUYBXANn7OBSF1gAnIYgEC','张三','zhangsan@lab.local','13800000001',NULL,1,'2026-10-16 23:25:01','2026-10-16 23:25:01'),(3,'lisi','$2b$12$mQAFik4EBNd85RJRZB198eWaIKhBlUkZeMrGdgTeFeFC8QdaTI2s6','李四','lisi@lab.local','13800000002',NULL,1,'2026-10-16 23:25:01','2026-10-16 23:25:01'),(4,'elf','$2b$12$UWgK26MzYT/XbsARmlqJru4TjElM7AHlLco3Sta3ucTB6E7aoPTXq','l;r','1915284259@qq.com','17712327930','/uploads/20261025212336055624_7bb4c20f.png',1,'2026-10-17 17:41:04','2026-10-25 21:23:37');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_role`
--

DROP TABLE IF EXISTS `user_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_role` (
  `user_id` int NOT NULL COMMENT '用户ID',
  `role_id` int NOT NULL COMMENT '角色ID',
  `created_at` datetime NOT NULL COMMENT '创建时间',
  `updated_at` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`user_id`,`role_id`),
  KEY `ix_user_role_role_id` (`role_id`),
  CONSTRAINT `user_role_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE CASCADE,
  CONSTRAINT `user_role_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户角色关联表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_role`
--

LOCK TABLES `user_role` WRITE;
/*!40000 ALTER TABLE `user_role` DISABLE KEYS */;
INSERT INTO `user_role` VALUES (1,1,'2026-10-16 23:25:01','2026-10-16 23:25:01'),(2,4,'2026-10-16 23:25:01','2026-10-16 23:25:01'),(3,3,'2026-10-16 23:25:01','2026-10-16 23:25:01');
/*!40000 ALTER TABLE `user_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'my_lab'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-15 16:16:58
