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
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='权限表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permission`
--

LOCK TABLES `permission` WRITE;
/*!40000 ALTER TABLE `permission` DISABLE KEYS */;
INSERT INTO `permission` VALUES (1,'system','系统管理','系统管理目录',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',NULL,1),(2,'system:user','用户管理','用户管理菜单',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',1,1),(3,'user:list','查询用户','分页查询用户',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',2,2),(4,'user:create','创建用户','创建用户',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',2,2),(5,'user:update','修改用户','修改指定用户',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',2,2),(6,'user:delete','删除用户','删除用户',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',2,2),(7,'user:assign_role','分配角色','给用户分配角色',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',2,2),(8,'system:role','角色管理','角色管理菜单',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',1,1),(9,'role:list','查询角色','获取角色列表',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',8,2),(10,'role:create','创建角色','创建角色',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',8,2),(11,'role:update','更新角色','更新角色',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',8,2),(12,'role:delete','删除角色','删除角色',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',8,2),(13,'system:menu','菜单管理','菜单管理菜单',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',1,1),(14,'menu:list','查询菜单','获取菜单树/列表',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',13,2),(15,'menu:create','创建菜单','创建菜单',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',13,2),(16,'menu:update','更新菜单','更新菜单',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',13,2),(17,'menu:delete','删除菜单','删除菜单',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',13,2),(18,'lab','实验室管理','实验室管理目录',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',NULL,1),(19,'lab:list','实验室列表','实验室列表菜单',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',18,1),(20,'lab:detail','实验室详情','获取实验室详情',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',19,2),(21,'lab:create','创建实验室','创建实验室',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',19,2),(22,'lab:update','更新实验室','更新实验室',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',19,2),(23,'lab:delete','删除实验室','删除实验室',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',19,2),(24,'lab:image','更新实验室图片','更新实验室图片',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',19,2),(25,'lab:book','预约管理','预约管理菜单',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',18,1),(26,'lab_book:list','预约列表','获取实验室预约列表',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',25,2),(27,'lab_book:create','创建预约','创建实验室预约',1,'2026-10-16 23:25:00','2026-10-16 23:25:00',25,2);
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
INSERT INTO `role_permission` VALUES (1,1,'2026-11-14 16:14:41','2026-11-14 16:14:41'),(2,1,'2026-11-14 16:38:23','2026-11-14 16:38:23'),(3,18,'2026-10-16 23:25:01','2026-10-16 23:25:01'),(3,19,'2026-10-16 23:25:01','2026-10-16 23:25:01'),(3,20,'2026-10-16 23:25:01','2026-10-16 23:25:01'),(3,21,'2026-10-16 23:25:01','2026-10-16 23:25:01'),(3,22,'2026-10-16 23:25:01','2026-10-16 23:25:01'),(3,23,'2026-10-16 23:25:01','2026-10-16 23:25:01'),(3,24,'2026-10-16 23:25:01','2026-10-16 23:25:01'),(3,25,'2026-10-16 23:25:01','2026-10-16 23:25:01'),(3,26,'2026-10-16 23:25:01','2026-10-16 23:25:01'),(3,27,'2026-10-16 23:25:01','2026-10-16 23:25:01'),(4,18,'2026-10-16 23:25:01','2026-10-16 23:25:01'),(4,19,'2026-10-16 23:25:01','2026-10-16 23:25:01'),(4,20,'2026-10-16 23:25:01','2026-10-16 23:25:01'),(4,25,'2026-10-16 23:25:01','2026-10-16 23:25:01'),(4,26,'2026-10-16 23:25:01','2026-10-16 23:25:01'),(4,27,'2026-10-16 23:25:01','2026-10-16 23:25:01'),(5,1,'2026-11-14 16:16:30','2026-11-14 16:16:30');
/*!40000 ALTER TABLE `role_permission` ENABLE KEYS */;
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
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-14 18:30:56
