-- MySQL dump 10.13  Distrib 8.0.36, for macos14 (arm64)
--
-- Host: 127.0.0.1    Database: darkvision_lpr
-- ------------------------------------------------------
-- Server version	8.0.36

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
-- Table structure for table `admin_roles`
--

DROP TABLE IF EXISTS `admin_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin_roles` (
  `admin_user_id` bigint NOT NULL,
  `role_id` bigint NOT NULL,
  PRIMARY KEY (`admin_user_id`,`role_id`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `admin_roles_ibfk_1` FOREIGN KEY (`admin_user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `admin_roles_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='管理员-角色关联';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_roles`
--

LOCK TABLES `admin_roles` WRITE;
/*!40000 ALTER TABLE `admin_roles` DISABLE KEYS */;
INSERT INTO `admin_roles` VALUES (5,1);
/*!40000 ALTER TABLE `admin_roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `announcements`
--

DROP TABLE IF EXISTS `announcements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `announcements` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `content` text NOT NULL,
  `display_position` enum('popup','banner','message_center') NOT NULL,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `is_enabled` tinyint(1) DEFAULT '1',
  `created_by` bigint NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `announcements_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='系统公告';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `announcements`
--

LOCK TABLES `announcements` WRITE;
/*!40000 ALTER TABLE `announcements` DISABLE KEYS */;
INSERT INTO `announcements` VALUES (1,'春节期间服务调整通知','春节期间（2026.02.10-02.17）技术支持时间调整为9:00-18:00，感谢您的理解！','banner','2026-01-20 00:00:00','2026-02-18 23:59:59',1,5,'2026-01-05 23:51:43'),(2,'VIP用户新增功能通知','VIP用户现已支持视频流实时识别功能，快去体验吧！','popup','2026-01-01 00:00:00','2026-01-31 23:59:59',1,5,'2026-01-05 23:51:43'),(3,'系统维护通知','DarkVision LPR 将于本周六凌晨 2:00 进行系统升级，预计耗时 2 小时。','banner','2026-01-06 04:36:01','2026-01-13 04:36:01',1,1,'2026-01-06 04:36:01');
/*!40000 ALTER TABLE `announcements` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `batch_recognition_items`
--

DROP TABLE IF EXISTS `batch_recognition_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `batch_recognition_items` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `task_id` bigint NOT NULL,
  `result_id` bigint DEFAULT NULL,
  `item_index` int NOT NULL COMMENT '批量上传顺序',
  `status` enum('pending','success','failed') NOT NULL DEFAULT 'pending',
  PRIMARY KEY (`id`),
  KEY `task_id` (`task_id`),
  KEY `result_id` (`result_id`),
  CONSTRAINT `batch_recognition_items_ibfk_1` FOREIGN KEY (`task_id`) REFERENCES `recognition_tasks` (`id`) ON DELETE CASCADE,
  CONSTRAINT `batch_recognition_items_ibfk_2` FOREIGN KEY (`result_id`) REFERENCES `recognition_results` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='批量识别子项';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `batch_recognition_items`
--

LOCK TABLES `batch_recognition_items` WRITE;
/*!40000 ALTER TABLE `batch_recognition_items` DISABLE KEYS */;
INSERT INTO `batch_recognition_items` VALUES (1,2,2,1,'success'),(2,2,3,2,'success'),(3,2,NULL,3,'failed');
/*!40000 ALTER TABLE `batch_recognition_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `carousels`
--

DROP TABLE IF EXISTS `carousels`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `carousels` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `image_url` varchar(255) NOT NULL,
  `link_url` varchar(255) DEFAULT NULL,
  `sort_order` int DEFAULT '0',
  `is_enabled` tinyint(1) DEFAULT '1',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='首页轮播图';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carousels`
--

LOCK TABLES `carousels` WRITE;
/*!40000 ALTER TABLE `carousels` DISABLE KEYS */;
INSERT INTO `carousels` VALUES (1,'DarkVision-LPR v2.1 全新发布','https://oss.example.com/carousel/1.jpg','/news/v2.1-release',1,1,'2026-01-05 23:51:43'),(2,'企业版限时优惠','https://oss.example.com/carousel/2.jpg','/packages/enterprise',2,1,'2026-01-05 23:51:43'),(3,'API接口文档更新','https://oss.example.com/carousel/3.jpg','/docs/api',3,1,'2026-01-05 23:51:43'),(4,'智能感知，精准识别','https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80',NULL,1,1,'2026-01-06 04:36:01'),(5,'夜间识别，清晰如昼','https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80',NULL,2,1,'2026-01-06 04:36:01');
/*!40000 ALTER TABLE `carousels` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `client_downloads`
--

DROP TABLE IF EXISTS `client_downloads`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `client_downloads` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `os` enum('windows','macos','linux') NOT NULL,
  `version` varchar(20) NOT NULL,
  `download_url` varchar(255) NOT NULL,
  `changelog` text,
  `release_date` date NOT NULL,
  `is_latest` tinyint(1) DEFAULT '0',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_os_latest` (`os`,`is_latest`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='客户端下载';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `client_downloads`
--

LOCK TABLES `client_downloads` WRITE;
/*!40000 ALTER TABLE `client_downloads` DISABLE KEYS */;
INSERT INTO `client_downloads` VALUES (7,'windows','v1.0.0','https://github.com/Auroral0810/EasyRename/releases/download/v1.0.0/EasyRename_1.0.0_x64_zh%2DCN.msi','Initial Release','2026-01-01',1,'2026-01-06 04:37:15'),(8,'macos','v1.0.0','https://github.com/Auroral0810/EasyRename/releases/download/v1.0.0/EasyRename_1.0.0_aarch64.dmg','Initial Release','2026-01-01',1,'2026-01-06 04:37:15'),(9,'linux','v1.0.0','https://github.com/Auroral0810/EasyRename/releases/download/v1.0.0/easy%2Drename_1.0.0_amd64.deb','Initial Release','2026-01-01',1,'2026-01-06 04:37:15');
/*!40000 ALTER TABLE `client_downloads` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contact_messages`
--

DROP TABLE IF EXISTS `contact_messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contact_messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL COMMENT '姓名',
  `email` varchar(100) NOT NULL COMMENT '邮箱',
  `message` text NOT NULL COMMENT '咨询内容',
  `status` enum('pending','processed','ignored') NOT NULL DEFAULT 'pending' COMMENT '处理状态',
  `ip_address` varchar(45) DEFAULT NULL COMMENT 'IP地址',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `processed_at` datetime DEFAULT NULL COMMENT '处理时间',
  `processed_by` int DEFAULT NULL COMMENT '处理人ID',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='联系/咨询消息表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contact_messages`
--

LOCK TABLES `contact_messages` WRITE;
/*!40000 ALTER TABLE `contact_messages` DISABLE KEYS */;
INSERT INTO `contact_messages` VALUES (1,'俞云烽','15968588744@163.com','test.....','pending','127.0.0.1','2026-01-06 03:56:33',NULL,NULL),(2,'俞云烽','15968588744@163.com','test.....','pending','127.0.0.1','2026-01-06 03:58:34',NULL,NULL),(3,'俞云烽','15968588744@163.com','test2','pending','127.0.0.1','2026-01-06 04:00:25',NULL,NULL),(4,'俞云烽','15968588744@163.com','你好','pending','127.0.0.1','2026-01-06 17:01:49',NULL,NULL);
/*!40000 ALTER TABLE `contact_messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `coupons`
--

DROP TABLE IF EXISTS `coupons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `coupons` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(50) NOT NULL,
  `discount_type` enum('percent','fixed') NOT NULL,
  `discount_value` decimal(10,2) NOT NULL,
  `expire_date` datetime DEFAULT NULL,
  `max_usage` int DEFAULT NULL,
  `used_count` int DEFAULT '0',
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='优惠券';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coupons`
--

LOCK TABLES `coupons` WRITE;
/*!40000 ALTER TABLE `coupons` DISABLE KEYS */;
INSERT INTO `coupons` VALUES (1,'VIP2026','percent',10.00,'2026-12-31 23:59:59',1000,56,1,'2026-01-05 23:51:43'),(2,'NEWUSER5','fixed',5.00,'2026-06-30 23:59:59',5000,1289,1,'2026-01-05 23:51:43'),(3,'ENTERPRISE1000','fixed',1000.00,'2026-03-31 23:59:59',100,23,1,'2026-01-05 23:51:43');
/*!40000 ALTER TABLE `coupons` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `documents`
--

DROP TABLE IF EXISTS `documents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `documents` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `doc_type` enum('tech','service_agreement','privacy_policy') NOT NULL,
  `content` longtext NOT NULL,
  `version` varchar(20) NOT NULL,
  `is_current` tinyint(1) DEFAULT '0',
  `created_by` bigint NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `documents_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='文档（技术文档、服务协议等）';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `documents`
--

LOCK TABLES `documents` WRITE;
/*!40000 ALTER TABLE `documents` DISABLE KEYS */;
INSERT INTO `documents` VALUES (1,'API接口文档','tech','# DarkVision-LPR API接口文档\n## 基础信息\n接口地址：https://api.darkvision.com/v1/lpr\n请求方式：POST\nContent-Type：application/json\n...','v2.1',1,5,'2026-01-05 23:51:43'),(2,'用户服务协议','service_agreement','### 服务协议\n1. 服务范围\n本服务提供车牌识别相关技术服务，包括图片识别、视频识别等...','v1.2',1,5,'2026-01-05 23:51:43'),(3,'隐私政策','privacy_policy','### 隐私政策\n1. 信息收集\n我们仅收集必要的用户信息，包括手机号、身份证信息（实名认证）等...','v1.1',1,5,'2026-01-05 23:51:43'),(4,'技术文档','tech','## 架构概览\n\nDarkVision LPR 采用微服务架构...\n\n## 部署指南\n\n1. Docker Compose...\n','1.0.0',1,1,'2026-01-06 04:37:15'),(5,'服务协议','service_agreement','## 1. 服务内容\n\n本协议是您与 DarkVision 之间关于使用本服务的法律协议...','1.0.0',1,1,'2026-01-06 04:37:15'),(6,'隐私政策','privacy_policy','## 1. 信息收集\n\n我们收集您的以下信息以提供更好的服务...','1.0.0',1,1,'2026-01-06 04:37:15');
/*!40000 ALTER TABLE `documents` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `faq_categories`
--

DROP TABLE IF EXISTS `faq_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `faq_categories` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `sort_order` int DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='FAQ分类';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faq_categories`
--

LOCK TABLES `faq_categories` WRITE;
/*!40000 ALTER TABLE `faq_categories` DISABLE KEYS */;
INSERT INTO `faq_categories` VALUES (1,'新手入门',1),(2,'会员服务',2),(3,'技术支持',3);
/*!40000 ALTER TABLE `faq_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `faqs`
--

DROP TABLE IF EXISTS `faqs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `faqs` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `category_id` bigint DEFAULT NULL,
  `question` varchar(255) NOT NULL,
  `answer` text NOT NULL,
  `sort_order` int DEFAULT '0',
  `view_count` int DEFAULT '0',
  `is_hot` tinyint(1) DEFAULT '0',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `faqs_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `faq_categories` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='常见问题';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faqs`
--

LOCK TABLES `faqs` WRITE;
/*!40000 ALTER TABLE `faqs` DISABLE KEYS */;
INSERT INTO `faqs` VALUES (1,NULL,'如何修改绑定的手机号？','登录后进入【个人中心】-【账号安全】，点击手机号右侧的【修改】按钮，按照提示完成短信验证即可修改。',1,1258,1,'2026-01-05 23:51:43'),(2,NULL,'识别结果不准确怎么办？','您可以尝试使用图片增强功能（如CLAHE、锐化等），或者上传更高清晰度的图片。如果问题依然存在，请联系客服提供图片进行技术排查。',1,2890,1,'2026-01-05 23:51:43'),(3,NULL,'VIP会员有哪些特权？','VIP会员享有更高的每日识别限额、更多的图片增强算法、批量识别无数量限制、导出识别结果等特权，具体请查看会员套餐详情页。',1,1567,1,'2026-01-05 23:51:43'),(4,NULL,'如何获取API接口密钥？','企业版用户登录后进入【开发者中心】-【API管理】，点击【生成密钥】按钮即可获取API Key和Secret。',1,890,0,'2026-01-05 23:51:43'),(5,1,'如何开始使用系统？','注册账号后即可开始使用，普通用户每日有20次免费识别机会。您可以在控制台查看详细的使用指南。',1,100,1,'2026-01-06 04:36:41'),(6,1,'支持哪些图片格式？','支持 JPG、PNG、BMP 等常见图片格式。单张图片建议在 5MB 以内，VIP 用户支持最大 10MB 的高清图片。',2,90,0,'2026-01-06 04:36:41'),(7,2,'如何升级到 VIP？','在价格页面选择 VIP 方案，点击购买并完成支付后，您的账号将立即升级，享受更多权益。',3,80,1,'2026-01-06 04:36:41'),(8,2,'是否提供 API 接口？','是的，VIP 用户和企业用户可以使用 RESTful API 接口。我们提供完善的 API 文档和多语言 SDK。',4,70,0,'2026-01-06 04:36:41');
/*!40000 ALTER TABLE `faqs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login_logs`
--

DROP TABLE IF EXISTS `login_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `login_logs` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `user_agent` text,
  `success` tinyint(1) NOT NULL DEFAULT '0',
  `failure_reason` varchar(255) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_time` (`user_id`,`created_at`),
  CONSTRAINT `login_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='登录日志';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login_logs`
--

LOCK TABLES `login_logs` WRITE;
/*!40000 ALTER TABLE `login_logs` DISABLE KEYS */;
INSERT INTO `login_logs` VALUES (1,1,'192.168.1.100','Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0',1,NULL,'2026-01-05 23:50:11'),(2,2,'192.168.1.101','Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) Safari/605.1.15',1,NULL,'2026-01-05 23:50:11'),(3,5,'192.168.1.200','Mozilla/5.0 (Linux; Android 14) Chrome/120.0.0.0',1,NULL,'2026-01-05 23:50:11'),(4,1,'192.168.1.100','Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0',0,'密码错误','2026-01-05 23:50:11'),(5,7,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',1,NULL,'2026-01-06 17:26:23'),(6,7,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',0,'','2026-01-06 18:25:20'),(7,7,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',0,'','2026-01-06 18:25:37'),(8,7,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',1,NULL,'2026-01-06 18:25:55'),(9,7,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',1,NULL,'2026-01-06 19:19:41'),(10,7,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',1,NULL,'2026-01-06 21:10:02'),(11,7,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',1,NULL,'2026-01-06 21:15:42'),(12,7,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',0,'','2026-01-07 02:54:34'),(13,7,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',1,NULL,'2026-01-07 02:54:36'),(14,7,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',1,NULL,'2026-01-07 03:16:33'),(15,7,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',1,NULL,'2026-01-07 03:17:30'),(16,5,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',0,'System Error: ','2026-01-07 18:32:43'),(17,5,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',0,'System Error: ','2026-01-07 18:35:47'),(18,5,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',0,'System Error: ','2026-01-07 18:38:02'),(19,5,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',0,'System Error: ','2026-01-07 18:38:20'),(20,5,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',1,NULL,'2026-01-07 18:41:09'),(21,5,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',1,NULL,'2026-01-07 18:54:56'),(22,5,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',1,NULL,'2026-01-07 19:01:19'),(23,5,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',1,NULL,'2026-01-07 19:05:06'),(24,5,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',1,NULL,'2026-01-07 19:22:30'),(25,5,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',1,NULL,'2026-01-07 19:25:46'),(26,5,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',1,NULL,'2026-01-07 19:26:22'),(27,5,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',1,NULL,'2026-01-07 19:28:02'),(28,5,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',1,NULL,'2026-01-07 19:29:53'),(29,5,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',1,NULL,'2026-01-07 19:48:10'),(30,5,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',1,NULL,'2026-01-07 19:52:13'),(31,5,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',1,NULL,'2026-01-07 19:53:36'),(32,5,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',1,NULL,'2026-01-07 20:11:14'),(33,5,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',1,NULL,'2026-01-07 20:14:38'),(34,5,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',1,NULL,'2026-01-07 20:19:17'),(35,7,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',1,NULL,'2026-01-07 21:19:23'),(36,7,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',1,NULL,'2026-01-07 21:35:01'),(37,7,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',1,NULL,'2026-01-07 21:35:48'),(38,7,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',1,NULL,'2026-01-07 21:37:19'),(39,7,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',1,NULL,'2026-01-07 21:38:03'),(40,7,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',1,NULL,'2026-01-07 21:41:18'),(41,7,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',1,NULL,'2026-01-07 21:42:10'),(42,7,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',1,NULL,'2026-01-07 21:49:00'),(43,5,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',1,NULL,'2026-01-07 21:52:04'),(44,7,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',1,NULL,'2026-01-07 21:55:23'),(45,7,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',1,NULL,'2026-01-07 21:58:23'),(46,5,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',1,NULL,'2026-01-07 21:59:20'),(47,7,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',1,NULL,'2026-01-07 21:59:40'),(56,8,'127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:140.0) Gecko/20100101 Firefox/140.0',1,NULL,'2026-01-07 22:01:55');
/*!40000 ALTER TABLE `login_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `message_templates`
--

DROP TABLE IF EXISTS `message_templates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `message_templates` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `template_key` varchar(100) NOT NULL,
  `title` varchar(200) NOT NULL,
  `content` text NOT NULL,
  `type` enum('email','sms','station') NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `template_key` (`template_key`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='消息模板（邮件、短信）';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `message_templates`
--

LOCK TABLES `message_templates` WRITE;
/*!40000 ALTER TABLE `message_templates` DISABLE KEYS */;
INSERT INTO `message_templates` VALUES (1,'register_sms','【DarkVision】注册验证码','您的注册验证码是：{code}，5分钟内有效。','sms','2026-01-05 23:51:43'),(2,'reset_password_email','DarkVision密码重置','尊敬的用户，您请求重置密码，请点击链接：{url}（有效期1小时）','email','2026-01-05 23:51:43'),(3,'order_paid','订单支付成功通知','您的订单{order_no}已支付成功，感谢您的购买！','station','2026-01-05 23:51:43');
/*!40000 ALTER TABLE `message_templates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `operation_logs`
--

DROP TABLE IF EXISTS `operation_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `operation_logs` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `admin_id` bigint DEFAULT NULL COMMENT '操作人ID',
  `action` varchar(100) NOT NULL,
  `target_type` varchar(50) DEFAULT NULL,
  `target_id` bigint DEFAULT NULL,
  `description` text,
  `ip_address` varchar(45) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `module` varchar(50) NOT NULL DEFAULT 'system' COMMENT '功能模块',
  `method` varchar(10) DEFAULT NULL COMMENT '请求方法',
  `path` varchar(255) DEFAULT NULL COMMENT '请求路径',
  `params` text COMMENT '请求参数',
  `result` text COMMENT '响应结果',
  `status` int DEFAULT '200' COMMENT '响应状态码',
  `user_agent` varchar(255) DEFAULT NULL COMMENT 'User Agent',
  `duration` int DEFAULT NULL COMMENT '耗时(ms)',
  PRIMARY KEY (`id`),
  KEY `idx_admin_action` (`admin_id`,`action`),
  KEY `ix_operation_logs_admin_id` (`admin_id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='管理员操作日志';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `operation_logs`
--

LOCK TABLES `operation_logs` WRITE;
/*!40000 ALTER TABLE `operation_logs` DISABLE KEYS */;
INSERT INTO `operation_logs` VALUES (1,5,'user:ban','user',10,'禁用用户ID10（违规使用）','192.168.1.200','2026-01-05 23:51:43','system',NULL,NULL,NULL,NULL,200,NULL,NULL),(2,5,'order:refund','order',5,'为订单ID5办理退款（用户申请）','192.168.1.200','2026-01-05 23:51:43','system',NULL,NULL,NULL,NULL,200,NULL,NULL),(3,5,'system:config','system_config',1,'修改每日免费识别限额为10次','192.168.1.200','2026-01-05 23:51:43','system',NULL,NULL,NULL,NULL,200,NULL,NULL),(4,5,'update',NULL,NULL,'Updated role user_manager',NULL,'2026-01-08 04:31:47','role','PUT',NULL,NULL,NULL,200,NULL,NULL),(5,5,'update',NULL,NULL,'Updated role user_manager',NULL,'2026-01-08 04:32:10','role','PUT',NULL,NULL,NULL,200,NULL,NULL),(6,5,'create',NULL,NULL,'Created permission sss',NULL,'2026-01-08 04:33:15','permission','POST',NULL,NULL,NULL,200,NULL,NULL),(7,5,'delete',NULL,NULL,'Deleted permission 18',NULL,'2026-01-08 04:33:33','permission','DELETE',NULL,NULL,NULL,200,NULL,NULL),(8,5,'update',NULL,NULL,'Updated permission 查看用户',NULL,'2026-01-08 04:33:41','permission','PUT',NULL,NULL,NULL,200,NULL,NULL),(9,5,'update',NULL,NULL,'Updated permission 查看用户',NULL,'2026-01-08 04:33:52','permission','PUT',NULL,NULL,NULL,200,NULL,NULL),(10,5,'update',NULL,NULL,'Updated permission 管理识别记录',NULL,'2026-01-08 04:33:59','permission','PUT',NULL,NULL,NULL,200,NULL,NULL),(11,5,'update',NULL,NULL,'Updated permission 管理识别记录',NULL,'2026-01-08 04:34:09','permission','PUT',NULL,NULL,NULL,200,NULL,NULL),(12,5,'update',NULL,NULL,'Updated role user_manager',NULL,'2026-01-08 04:36:07','role','PUT',NULL,NULL,NULL,200,NULL,NULL),(13,5,'update',NULL,NULL,'Updated role user_manager',NULL,'2026-01-08 04:36:21','role','PUT',NULL,NULL,NULL,200,NULL,NULL),(14,5,'update',NULL,NULL,'Updated role user_manager',NULL,'2026-01-08 04:39:48','role','PUT',NULL,NULL,NULL,200,NULL,NULL);
/*!40000 ALTER TABLE `operation_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `order_no` varchar(64) NOT NULL,
  `user_id` bigint NOT NULL,
  `package_id` bigint NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `status` enum('pending','paid','cancelled','refunded') NOT NULL DEFAULT 'pending',
  `payment_method` enum('wechat','alipay','bank') DEFAULT NULL,
  `paid_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_no` (`order_no`),
  KEY `user_id` (`user_id`),
  KEY `package_id` (`package_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`package_id`) REFERENCES `packages` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='订单';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `package_features`
--

DROP TABLE IF EXISTS `package_features`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `package_features` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `package_id` bigint NOT NULL,
  `feature_key` varchar(100) NOT NULL COMMENT '如 daily_limit',
  `feature_value` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `package_id` (`package_id`),
  CONSTRAINT `package_features_ibfk_1` FOREIGN KEY (`package_id`) REFERENCES `packages` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='套餐功能明细（用于对比表）';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `package_features`
--

LOCK TABLES `package_features` WRITE;
/*!40000 ALTER TABLE `package_features` DISABLE KEYS */;
INSERT INTO `package_features` VALUES (20,1,'daily_limit','20'),(21,1,'max_image_size','5MB'),(22,1,'history_retention','7 days'),(23,2,'daily_limit','500'),(24,2,'api_limit','5000'),(25,2,'batch_size','50'),(26,2,'video_limit','10'),(27,3,'daily_limit','Unlimited'),(28,3,'custom_model','Yes'),(29,3,'private_deployment','Optional');
/*!40000 ALTER TABLE `package_features` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `packages`
--

DROP TABLE IF EXISTS `packages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `packages` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `code` enum('free','vip_monthly','vip_yearly','enterprise_custom') NOT NULL COMMENT '套餐编码（free/vip_monthly/vip_yearly/enterprise_custom）',
  `price` decimal(10,2) NOT NULL,
  `duration_months` int DEFAULT NULL COMMENT '月数，永久为NULL',
  `description` text,
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='套餐定义';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `packages`
--

LOCK TABLES `packages` WRITE;
/*!40000 ALTER TABLE `packages` DISABLE KEYS */;
INSERT INTO `packages` VALUES (1,'免费版','free',0.00,NULL,'个人学习与体验',1,'2026-01-06 04:41:43'),(2,'VIP 会员','vip_monthly',99.00,1,'专业开发者与小型团队',1,'2026-01-06 04:41:43'),(3,'企业版','enterprise_custom',0.00,NULL,'大型企业与定制化需求',1,'2026-01-06 04:41:43');
/*!40000 ALTER TABLE `packages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `page_view_logs`
--

DROP TABLE IF EXISTS `page_view_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `page_view_logs` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint DEFAULT NULL COMMENT '登录用户ID，未登录为NULL',
  `page_path` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '页面路径',
  `page_type` varchar(7) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '页面类型',
  `ip_address` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'IP地址',
  `user_agent` text COLLATE utf8mb4_unicode_ci COMMENT 'User-Agent',
  `referer` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '来源页面',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `ix_page_view_logs_created_at` (`created_at`),
  KEY `ix_page_view_logs_id` (`id`),
  KEY `ix_page_view_logs_user_id` (`user_id`),
  CONSTRAINT `page_view_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=373 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `page_view_logs`
--

LOCK TABLES `page_view_logs` WRITE;
/*!40000 ALTER TABLE `page_view_logs` DISABLE KEYS */;
INSERT INTO `page_view_logs` VALUES (1,NULL,'/','landing','114.242.123.45','Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0','https://www.google.com/search?q=车牌识别','2026-01-05 09:15:30'),(2,NULL,'/','landing','58.221.89.156','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15','https://www.baidu.com/s?wd=车牌识别系统','2026-01-05 10:22:15'),(3,NULL,'/','landing','183.12.67.89','Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) Safari/605.1.15',NULL,'2026-01-05 14:38:42'),(4,1,'/','landing','192.168.1.100','Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0',NULL,'2026-01-05 09:00:05'),(5,2,'/','landing','192.168.1.101','Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) Safari/605.1.15',NULL,'2026-01-05 10:15:20'),(6,7,'/','landing','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/143.0.0.0',NULL,'2026-01-06 17:26:23'),(7,NULL,'/pricing','pricing','114.242.123.45','Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0','https://darkvision.com/','2026-01-05 09:18:45'),(8,NULL,'/pricing','pricing','221.10.45.78','Mozilla/5.0 (Windows NT 10.0; Win64; x64) Edge/120.0.0.0','https://darkvision.com/','2026-01-05 11:25:33'),(9,1,'/pricing','pricing','192.168.1.100','Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0','https://darkvision.com/','2026-01-05 09:05:12'),(10,2,'/pricing','pricing','192.168.1.101','Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) Safari/605.1.15','https://darkvision.com/features','2026-01-05 10:20:45'),(11,7,'/pricing','pricing','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/143.0.0.0','https://darkvision.com/','2026-01-06 18:30:15'),(12,NULL,'/features','feature','114.242.123.45','Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0','https://darkvision.com/','2026-01-05 09:16:20'),(13,NULL,'/features','feature','58.221.89.156','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15','https://darkvision.com/pricing','2026-01-05 10:25:10'),(14,2,'/features','feature','192.168.1.101','Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) Safari/605.1.15','https://darkvision.com/','2026-01-05 10:18:30'),(15,NULL,'/docs','docs','183.12.67.89','Mozilla/5.0 (Linux; Android 13) Chrome/120.0.0.0','https://www.google.com/search?q=车牌识别API文档','2026-01-05 15:42:18'),(16,3,'/docs','docs','192.168.1.102','Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0','https://darkvision.com/features','2026-01-05 11:30:25'),(17,7,'/docs','docs','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/143.0.0.0','https://darkvision.com/','2026-01-06 19:45:33'),(18,NULL,'/about','about','221.10.45.78','Mozilla/5.0 (Windows NT 10.0; Win64; x64) Edge/120.0.0.0','https://darkvision.com/','2026-01-05 11:28:50'),(19,1,'/about','about','192.168.1.100','Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0','https://darkvision.com/','2026-01-05 09:10:40'),(20,NULL,'/contact','contact','114.242.123.45','Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0','https://darkvision.com/about','2026-01-05 09:20:15'),(21,NULL,'/contact','contact','58.221.89.156','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15','https://darkvision.com/pricing','2026-01-05 10:30:22'),(22,7,'/contact','contact','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/143.0.0.0','https://darkvision.com/about','2026-01-06 17:01:35'),(23,NULL,'/download','other','183.12.67.89','Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0','https://darkvision.com/','2026-01-05 16:12:45'),(24,2,'/download','other','192.168.1.101','Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) Safari/605.1.15','https://darkvision.com/docs','2026-01-05 10:45:30'),(25,NULL,'/','landing','221.56.78.90','Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0','https://www.google.com','2026-01-06 08:30:20'),(26,NULL,'/','landing','114.89.45.123','Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) Safari/605.1.15',NULL,'2026-01-06 09:15:45'),(27,NULL,'/pricing','pricing','221.56.78.90','Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0','https://darkvision.com/','2026-01-06 08:35:10'),(28,7,'/','landing','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/143.0.0.0',NULL,'2026-01-06 17:26:23'),(29,7,'/features','feature','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/143.0.0.0','https://darkvision.com/','2026-01-06 17:30:50'),(30,7,'/pricing','pricing','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/143.0.0.0','https://darkvision.com/features','2026-01-06 17:35:20'),(31,5,'/','landing','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/143.0.0.0',NULL,'2026-01-06 18:41:09'),(32,NULL,'/features','feature','114.89.45.123','Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) Safari/605.1.15','https://darkvision.com/','2026-01-06 09:20:30'),(33,NULL,'/','landing','183.67.89.12','Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0','https://www.baidu.com','2026-01-07 10:20:15'),(34,NULL,'/','landing','221.34.56.78','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15',NULL,'2026-01-07 11:45:30'),(35,NULL,'/pricing','pricing','183.67.89.12','Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0','https://darkvision.com/','2026-01-07 10:25:40'),(36,7,'/','landing','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/143.0.0.0',NULL,'2026-01-07 02:54:36'),(37,7,'/docs','docs','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/143.0.0.0','https://darkvision.com/','2026-01-07 03:00:15'),(38,5,'/','landing','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/143.0.0.0',NULL,'2026-01-07 18:41:09'),(39,5,'/pricing','pricing','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/143.0.0.0','https://darkvision.com/','2026-01-07 18:45:22'),(40,NULL,'/contact','contact','221.34.56.78','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15','https://darkvision.com/about','2026-01-07 12:10:50'),(41,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-07 21:20:10'),(42,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-07 21:20:54'),(43,7,'/dashboard/recognition','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-07 21:20:59'),(44,7,'/dashboard/history','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-07 21:21:00'),(45,7,'/dashboard/analysis','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-07 21:32:49'),(46,NULL,'/login','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-07 21:32:55'),(47,NULL,'/login','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-07 21:33:30'),(48,NULL,'/login','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15','http://localhost:3001/','2026-01-07 21:33:50'),(49,NULL,'/login','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:140.0) Gecko/20100101 Firefox/140.0','http://localhost:3001/','2026-01-07 21:34:20'),(50,NULL,'/login','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:140.0) Gecko/20100101 Firefox/140.0','http://localhost:3001/','2026-01-07 21:34:29'),(51,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-07 21:35:01'),(52,7,'/dashboard/analysis','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-07 21:35:29'),(53,NULL,'/login','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-07 21:35:36'),(54,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-07 21:35:48'),(55,NULL,'/login','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-07 21:37:13'),(56,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-07 21:37:19'),(57,NULL,'/login','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-07 21:38:00'),(58,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-07 21:38:04'),(59,NULL,'/login','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-07 21:41:15'),(60,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-07 21:41:19'),(61,NULL,'/login','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-07 21:42:06'),(62,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-07 21:42:11'),(63,7,'/dashboard/settings','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-07 21:42:17'),(64,NULL,'/login','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-07 21:48:55'),(65,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-07 21:49:01'),(66,NULL,'/login','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-07 21:55:22'),(67,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-07 21:55:23'),(68,NULL,'/login','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:140.0) Gecko/20100101 Firefox/140.0','http://localhost:3001/','2026-01-07 21:57:46'),(69,NULL,'/login','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:140.0) Gecko/20100101 Firefox/140.0','http://localhost:3001/','2026-01-07 21:57:46'),(70,NULL,'/login','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-07 21:58:18'),(71,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-07 21:58:23'),(72,NULL,'/login','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-07 21:59:14'),(73,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-07 21:59:40'),(74,NULL,'/register','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:140.0) Gecko/20100101 Firefox/140.0','http://localhost:3001/','2026-01-07 22:01:36'),(75,NULL,'/login','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:140.0) Gecko/20100101 Firefox/140.0','http://localhost:3001/','2026-01-07 22:01:44'),(76,8,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:140.0) Gecko/20100101 Firefox/140.0','http://localhost:3001/','2026-01-07 22:01:55'),(77,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-07 22:03:10'),(78,5,'/dashboard/overview','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-07 22:16:41'),(79,NULL,'/','website','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3000/','2026-01-07 22:18:11'),(80,5,'/dashboard/overview','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-07 22:18:25'),(81,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-07 22:18:28'),(82,NULL,'/pricing','website','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3000/','2026-01-07 22:18:32'),(83,NULL,'/documentation','website','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3000/','2026-01-07 22:18:35'),(84,NULL,'/download','website','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3000/','2026-01-07 22:19:03'),(85,NULL,'/features','website','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3000/','2026-01-07 22:19:04'),(86,NULL,'/download','website','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3000/','2026-01-07 22:19:05'),(87,NULL,'/','website','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3000/','2026-01-07 22:19:32'),(88,5,'/dashboard/overview','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-07 22:25:17'),(89,NULL,'/','website','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3000/','2026-01-07 22:25:21'),(90,NULL,'/','website','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3000/','2026-01-07 22:30:56'),(91,5,'/dashboard/overview','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-07 22:31:13'),(92,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-07 22:31:16'),(93,5,'/dashboard/overview','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-07 22:31:22'),(94,NULL,'/download','website','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3000/','2026-01-07 22:31:28'),(95,NULL,'/features','website','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3000/','2026-01-07 22:31:29'),(96,NULL,'/capabilities','website','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3000/','2026-01-07 22:31:29'),(97,NULL,'/pricing','website','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3000/','2026-01-07 22:31:30'),(98,NULL,'/documentation','website','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3000/','2026-01-07 22:31:31'),(99,5,'/dashboard/overview','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-07 22:31:36'),(100,7,'/dashboard/history','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-07 22:31:45'),(101,7,'/dashboard/history','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-07 22:31:46'),(102,7,'/dashboard/analysis','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-07 22:31:47'),(103,7,'/dashboard/settings','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-07 22:31:49'),(104,5,'/dashboard/overview','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-07 22:31:53'),(105,NULL,'/','website','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3000/','2026-01-07 22:33:14'),(106,NULL,'/capabilities','website','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3000/','2026-01-07 22:33:21'),(107,NULL,'/pricing','website','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3000/','2026-01-07 22:33:26'),(108,NULL,'/','website','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3000/','2026-01-07 22:40:35'),(109,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-07 22:40:42'),(110,NULL,'/','website','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3000/','2026-01-07 22:41:06'),(111,NULL,'/','website','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:140.0) Gecko/20100101 Firefox/140.0','http://localhost:3000/','2026-01-07 22:41:21'),(112,8,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:140.0) Gecko/20100101 Firefox/140.0','http://localhost:3001/','2026-01-07 22:41:31'),(113,NULL,'/login','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:146.0) Gecko/20100101 Firefox/146.0','http://localhost:3001/','2026-01-07 22:42:02'),(114,8,'/api/v1/auth/login','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:146.0) Gecko/20100101 Firefox/146.0',NULL,'2026-01-07 22:42:35'),(115,8,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:146.0) Gecko/20100101 Firefox/146.0','http://localhost:3001/','2026-01-07 22:42:35'),(116,5,'/dashboard/overview','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-07 22:43:09'),(117,5,'/dashboard/overview','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-07 22:44:05'),(118,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-07 22:47:16'),(119,NULL,'/login','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:146.0) Gecko/20100101 Firefox/146.0','http://localhost:3001/','2026-01-07 22:47:25'),(120,NULL,'/register','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:146.0) Gecko/20100101 Firefox/146.0','http://localhost:3001/','2026-01-07 22:47:29'),(121,NULL,'/login','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:146.0) Gecko/20100101 Firefox/146.0','http://localhost:3001/','2026-01-07 22:48:04'),(122,9,'/api/v1/auth/login','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:146.0) Gecko/20100101 Firefox/146.0',NULL,'2026-01-07 22:48:15'),(123,9,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:146.0) Gecko/20100101 Firefox/146.0','http://localhost:3001/','2026-01-07 22:48:15'),(124,5,'/dashboard/overview','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-07 22:48:34'),(125,5,'/dashboard/overview','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-07 23:06:53'),(126,5,'/dashboard/overview','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-07 23:07:30'),(127,5,'/dashboard/overview','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-07 23:07:41'),(128,NULL,'/login?redirect=/dashboard/overview','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-07 23:08:52'),(129,5,'/api/admin/login','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',NULL,'2026-01-07 23:09:04'),(130,5,'/dashboard/overview','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-07 23:09:05'),(131,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-07 23:17:36'),(132,5,'/user/verification','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-07 23:17:37'),(133,5,'/user/tags','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-07 23:17:38'),(134,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-07 23:17:39'),(135,5,'/dashboard/overview','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-07 23:20:25'),(136,NULL,'/','website','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3000/','2026-01-07 23:22:04'),(137,5,'/content/faq','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-07 23:25:07'),(138,5,'/content/announcement','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-07 23:25:08'),(139,5,'/dashboard/overview','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-07 23:34:47'),(140,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-07 23:43:07'),(141,5,'/user/tags','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-07 23:46:01'),(142,5,'/user/verification','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-07 23:46:03'),(143,5,'/permission/role','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-07 23:46:08'),(144,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-07 23:46:14'),(145,5,'/user/verification','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-07 23:55:29'),(146,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-07 23:55:29'),(147,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-07 23:55:29'),(148,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-07 23:57:21'),(149,5,'/permission/role','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-07 23:58:10'),(150,5,'/permission/management','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-07 23:58:13'),(151,5,'/permission/role','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-07 23:58:14'),(152,5,'/permission/management','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-07 23:58:18'),(153,5,'/permission/admin','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-07 23:58:19'),(154,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-07 23:58:25'),(155,5,'/user/verification','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 00:04:41'),(156,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 00:04:42'),(157,5,'/recognition/records','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 00:10:10'),(158,5,'/recognition/tasks','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 00:10:14'),(159,5,'/statistics/user','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 00:10:19'),(160,5,'/finance/orders','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 00:10:24'),(161,5,'/finance/packages','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 00:10:38'),(162,5,'/finance/reports','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 00:10:39'),(163,5,'/statistics/user','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 00:10:39'),(164,5,'/statistics/recognition','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 00:10:40'),(165,5,'/statistics/board','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 00:10:41'),(166,5,'/permission/management','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 00:10:51'),(167,5,'/permission/role','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 00:10:52'),(168,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 00:10:53'),(169,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 00:10:57'),(170,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 00:38:23'),(171,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 00:51:45'),(172,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 00:55:35'),(173,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 00:55:51'),(174,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 00:56:00'),(175,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 00:56:32'),(176,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 00:56:32'),(177,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 00:57:33'),(178,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 00:57:39'),(179,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 00:57:46'),(180,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 00:58:23'),(181,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 01:00:28'),(182,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:00:28'),(183,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:00:35'),(184,7,'/dashboard/recognition','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:00:40'),(185,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:00:40'),(186,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:00:56'),(187,NULL,'/login','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:01:51'),(188,7,'/api/v1/auth/login','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',NULL,'2026-01-08 01:01:56'),(189,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:01:57'),(190,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 01:02:07'),(191,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 01:03:19'),(192,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 01:03:41'),(193,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 01:04:08'),(194,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 01:04:48'),(195,7,'/dashboard/analysis','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:08:17'),(196,7,'/dashboard/analysis','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:08:22'),(197,7,'/dashboard/analysis','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:11:25'),(198,7,'/dashboard/analysis','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:12:37'),(199,NULL,'/','website','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3000/','2026-01-08 01:12:55'),(200,NULL,'/login','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:13:15'),(201,7,'/api/v1/auth/login','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',NULL,'2026-01-08 01:13:19'),(202,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:13:19'),(203,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 01:13:23'),(204,7,'/dashboard/history','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:13:37'),(205,NULL,'/login','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:21:34'),(206,7,'/api/v1/auth/login','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',NULL,'2026-01-08 01:23:05'),(207,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:23:06'),(208,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 01:23:12'),(209,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:25:02'),(210,NULL,'/login','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:25:05'),(211,7,'/api/v1/auth/login','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',NULL,'2026-01-08 01:25:18'),(212,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:25:18'),(213,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 01:25:21'),(214,NULL,'/login','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:25:30'),(215,7,'/api/v1/auth/login','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',NULL,'2026-01-08 01:25:35'),(216,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:25:36'),(217,7,'/dashboard/recognition','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:25:38'),(218,7,'/dashboard/history','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:25:39'),(219,7,'/dashboard/recognition','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:25:41'),(220,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:29:26'),(221,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:29:29'),(222,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:30:12'),(223,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:30:44'),(224,7,'/dashboard/history','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:30:52'),(225,7,'/dashboard/history','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:30:53'),(226,7,'/dashboard/analysis','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:30:54'),(227,7,'/dashboard/recognition','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:30:57'),(228,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:31:08'),(229,7,'/dashboard/recognition','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:31:10'),(230,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:31:10'),(231,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:31:12'),(232,7,'/dashboard/history','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:31:13'),(233,7,'/dashboard/analysis','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:31:15'),(234,7,'/dashboard/analysis','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:34:37'),(235,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:34:40'),(236,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:34:42'),(237,7,'/dashboard/recognition','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:34:43'),(238,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:34:54'),(239,7,'/dashboard/analysis','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:34:57'),(240,7,'/dashboard/analysis','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:44:06'),(241,7,'/dashboard/recognition','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:44:10'),(242,7,'/dashboard/history','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:44:10'),(243,7,'/dashboard/recognition','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:44:11'),(244,7,'/dashboard/history','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:45:26'),(245,7,'/dashboard/analysis','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:45:28'),(246,7,'/dashboard/history','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:48:28'),(247,7,'/dashboard/recognition','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 01:48:30'),(248,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 02:29:06'),(249,5,'/permission/role','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 02:30:19'),(250,5,'/permission/admin','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 02:30:21'),(251,5,'/permission/management','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 02:30:23'),(252,5,'/permission/role','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 02:30:24'),(253,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 02:30:25'),(254,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 02:34:53'),(255,5,'/user/verification','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 02:37:53'),(256,5,'/user/verification','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 02:42:41'),(257,5,'/user/verification','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 02:43:09'),(258,5,'/user/verification','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 02:45:20'),(259,5,'/user/tags','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 02:45:47'),(260,5,'/user/verification','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 02:45:49'),(261,5,'/user/tags','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 02:45:49'),(262,5,'/user/tags','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 02:45:51'),(263,5,'/user/verification','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 02:45:52'),(264,5,'/user/verification','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 02:55:47'),(265,5,'/user/verification','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 02:56:10'),(266,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 02:56:18'),(267,5,'/user/verification','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 02:56:20'),(268,5,'/user/verification','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 02:59:05'),(269,5,'/user/verification','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 03:01:08'),(270,5,'/user/verification','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 03:01:31'),(271,5,'/user/verification','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 03:01:56'),(272,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 03:03:10'),(273,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 03:06:14'),(274,5,'/user/verification','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 03:07:34'),(275,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 03:07:44'),(276,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 03:09:41'),(277,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 03:10:29'),(278,5,'/user/verification','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 03:11:33'),(279,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 03:16:38'),(280,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 03:31:22'),(281,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 03:32:06'),(282,5,'/user/verification','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 03:32:33'),(283,5,'/user/verification','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 03:32:40'),(284,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 03:32:41'),(285,7,'/dashboard/history','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 03:33:56'),(286,7,'/dashboard/analysis','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 03:33:58'),(287,7,'/dashboard/overview','user','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3001/','2026-01-08 03:34:00'),(288,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 03:35:56'),(289,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 03:40:21'),(290,5,'/user/verification','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 03:42:06'),(291,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 03:45:06'),(292,5,'/user/verification','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 03:45:20'),(293,5,'/permission/role','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 03:45:25'),(294,5,'/permission/management','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 03:45:27'),(295,5,'/permission/admin','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 03:45:28'),(296,5,'/permission/role','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 03:45:29'),(297,5,'/permission/management','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 03:45:30'),(298,5,'/permission/admin','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 03:45:30'),(299,5,'/permission/management','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 03:50:15'),(300,5,'/permission/role','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 03:50:16'),(301,5,'/permission/admin','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 03:50:17'),(302,5,'/permission/role','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 03:50:18'),(303,5,'/permission/management','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 03:50:18'),(304,5,'/permission/role','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 03:50:39'),(305,5,'/permission/admin','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 03:50:41'),(306,5,'/permission/management','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 03:51:48'),(307,5,'/permission/role','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 03:59:46'),(308,5,'/permission/admin','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 03:59:47'),(309,5,'/permission/role','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 03:59:48'),(310,5,'/permission/role','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:03:21'),(311,5,'/permission/role','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:03:28'),(312,5,'/user/list','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:03:59'),(313,5,'/user/tags','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:04:12'),(314,5,'/user/verification','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:04:12'),(315,5,'/permission/role','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:04:16'),(316,5,'/permission/admin','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:04:18'),(317,5,'/permission/management','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:04:22'),(318,5,'/permission/role','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:04:23'),(319,5,'/permission/management','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:04:24'),(320,5,'/permission/role','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:04:25'),(321,5,'/permission/role','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:04:45'),(322,5,'/permission/admin','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:04:47'),(323,5,'/permission/role','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:04:47'),(324,5,'/permission/role','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:05:27'),(325,5,'/permission/role','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:05:30'),(326,5,'/permission/management','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:05:35'),(327,5,'/permission/admin','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:05:36'),(328,5,'/permission/management','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:05:43'),(329,5,'/permission/admin','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:05:44'),(330,5,'/permission/role','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:05:45'),(331,5,'/permission/role','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:06:09'),(332,5,'/permission/admin','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:06:14'),(333,5,'/permission/admin','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:06:23'),(334,5,'/permission/management','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:06:25'),(335,5,'/permission/role','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:06:29'),(336,5,'/permission/management','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:06:42'),(337,5,'/permission/admin','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:06:42'),(338,5,'/permission/role','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:06:43'),(339,5,'/permission/management','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:08:10'),(340,5,'/permission/management','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:08:11'),(341,5,'/permission/admin','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:08:11'),(342,5,'/permission/role','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:08:12'),(343,5,'/permission/admin','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:13:04'),(344,5,'/permission/role','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:13:06'),(345,5,'/permission/management','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:13:07'),(346,5,'/permission/role','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:17:12'),(347,5,'/permission/management','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:17:12'),(348,5,'/permission/role','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:23:12'),(349,5,'/permission/management','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:23:18'),(350,5,'/permission/role','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:23:33'),(351,5,'/permission/management','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:31:38'),(352,5,'/permission/admin','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:31:40'),(353,5,'/permission/role','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:31:41'),(354,5,'/permission/role','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:32:02'),(355,5,'/permission/management','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:32:59'),(356,5,'/permission/management','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:32:59'),(357,5,'/permission/admin','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:34:13'),(358,5,'/permission/role','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:34:31'),(359,5,'/recognition/tasks','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:34:38'),(360,5,'/recognition/records','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:34:39'),(361,5,'/recognition/models','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:34:40'),(362,5,'/content/docs','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:34:44'),(363,5,'/content/announcement','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:34:44'),(364,5,'/content/site','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:34:44'),(365,5,'/content/faq','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:34:45'),(366,5,'/content/site','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:34:46'),(367,5,'/statistics/user','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:35:00'),(368,5,'/statistics/recognition','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:35:02'),(369,5,'/statistics/board','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:35:05'),(370,5,'/log/operation','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:35:11'),(371,5,'/permission/role','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:36:01'),(372,5,'/permission/management','admin','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','http://localhost:3002/','2026-01-08 04:39:53');
/*!40000 ALTER TABLE `page_view_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `password_reset_tokens`
--

DROP TABLE IF EXISTS `password_reset_tokens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `password_reset_tokens` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `token` varchar(255) NOT NULL,
  `expires_at` datetime NOT NULL,
  `used` tinyint(1) NOT NULL DEFAULT '0',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token` (`token`),
  KEY `user_id` (`user_id`),
  KEY `idx_token` (`token`),
  CONSTRAINT `password_reset_tokens_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='密码重置令牌';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `password_reset_tokens`
--

LOCK TABLES `password_reset_tokens` WRITE;
/*!40000 ALTER TABLE `password_reset_tokens` DISABLE KEYS */;
INSERT INTO `password_reset_tokens` VALUES (1,1,'reset_token_1736064000_001','2026-01-06 09:00:00',0,'2026-01-05 23:51:43'),(2,2,'reset_token_1736064000_002','2026-01-06 10:00:00',1,'2026-01-05 23:51:43');
/*!40000 ALTER TABLE `password_reset_tokens` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments`
--

DROP TABLE IF EXISTS `payments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `order_id` bigint NOT NULL,
  `transaction_id` varchar(128) DEFAULT NULL COMMENT '第三方交易号',
  `amount` decimal(10,2) NOT NULL,
  `status` enum('success','failed','pending') NOT NULL,
  `payload` json DEFAULT NULL COMMENT '回调原始数据',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `order_id` (`order_id`),
  CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='支付记录';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments`
--

LOCK TABLES `payments` WRITE;
/*!40000 ALTER TABLE `payments` DISABLE KEYS */;
/*!40000 ALTER TABLE `payments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permissions`
--

DROP TABLE IF EXISTS `permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(100) NOT NULL COMMENT '权限标识，如 user:ban',
  `name` varchar(100) NOT NULL,
  `category` varchar(50) DEFAULT NULL COMMENT '分类分组',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `description` varchar(255) DEFAULT NULL COMMENT '描述',
  `type` varchar(20) DEFAULT 'menu' COMMENT '类型: menu/button/api',
  `parent_id` bigint DEFAULT NULL COMMENT '父权限ID',
  `path` varchar(255) DEFAULT NULL COMMENT '前端路由路径',
  `component` varchar(255) DEFAULT NULL COMMENT '前端组件路径',
  `icon` varchar(50) DEFAULT NULL COMMENT '图标',
  `sort_order` int DEFAULT '0' COMMENT '排序',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='权限项';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permissions`
--

LOCK TABLES `permissions` WRITE;
/*!40000 ALTER TABLE `permissions` DISABLE KEYS */;
INSERT INTO `permissions` VALUES (1,'*','全部权限','system','2026-01-05 23:50:11',NULL,'menu',NULL,NULL,NULL,NULL,0,'2026-01-08 04:21:54'),(2,'user:view','查看用户','user','2026-01-05 23:50:11','','menu',NULL,NULL,NULL,NULL,0,'2026-01-08 04:33:52'),(3,'user:ban','禁用用户','user','2026-01-05 23:50:11',NULL,'menu',NULL,NULL,NULL,NULL,0,'2026-01-08 04:21:54'),(4,'order:view','查看订单','finance','2026-01-05 23:50:11',NULL,'menu',NULL,NULL,NULL,NULL,0,'2026-01-08 04:21:54'),(5,'order:refund','订单退款','finance','2026-01-05 23:50:11',NULL,'menu',NULL,NULL,NULL,NULL,0,'2026-01-08 04:21:54'),(6,'content:manage','管理官网内容','ops','2026-01-05 23:50:11',NULL,'menu',NULL,NULL,NULL,NULL,0,'2026-01-08 04:21:54'),(7,'notice:manage','管理公告/FAQ','ops','2026-01-05 23:50:11',NULL,'menu',NULL,NULL,NULL,NULL,0,'2026-01-08 04:21:54'),(8,'activity:manage','管理促销活动','ops','2026-01-05 23:50:11',NULL,'menu',NULL,NULL,NULL,NULL,0,'2026-01-08 04:21:54'),(9,'user:stat:view','查看用户统计','ops','2026-01-05 23:50:11',NULL,'menu',NULL,NULL,NULL,NULL,0,'2026-01-08 04:21:54'),(10,'ai:task:monitor','监控识别任务','ai','2026-01-05 23:50:11',NULL,'menu',NULL,NULL,NULL,NULL,0,'2026-01-08 04:21:54'),(11,'ai:record:manage','管理识别记录','ai','2026-01-05 23:50:11',NULL,'menu',NULL,NULL,NULL,NULL,0,'2026-01-08 04:34:09'),(12,'ai:model:manage','管理识别模型','ai','2026-01-05 23:50:11',NULL,'menu',NULL,NULL,NULL,NULL,0,'2026-01-08 04:21:54'),(13,'ai:stat:view','查看识别统计','ai','2026-01-05 23:50:11',NULL,'menu',NULL,NULL,NULL,NULL,0,'2026-01-08 04:21:54'),(14,'system:log:view','查看系统日志','security','2026-01-05 23:50:11',NULL,'menu',NULL,NULL,NULL,NULL,0,'2026-01-08 04:21:54'),(15,'system:ip:manage','管理IP黑白名单','security','2026-01-05 23:50:11',NULL,'menu',NULL,NULL,NULL,NULL,0,'2026-01-08 04:21:54'),(16,'system:backup:manage','管理数据备份恢复','security','2026-01-05 23:50:11',NULL,'menu',NULL,NULL,NULL,NULL,0,'2026-01-08 04:21:54'),(17,'system:monitor:view','查看系统性能监控','security','2026-01-05 23:50:11',NULL,'menu',NULL,NULL,NULL,NULL,0,'2026-01-08 04:21:54');
/*!40000 ALTER TABLE `permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `real_name_verifications`
--

DROP TABLE IF EXISTS `real_name_verifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `real_name_verifications` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `id_card_front` varchar(255) NOT NULL COMMENT '身份证正面OSS路径',
  `id_card_back` varchar(255) NOT NULL COMMENT '身份证反面OSS路径',
  `face_photo` varchar(255) DEFAULT NULL COMMENT '人脸活体照片',
  `status` enum('pending','approved','rejected') NOT NULL DEFAULT 'pending',
  `reject_reason` text,
  `reviewed_by` bigint DEFAULT NULL COMMENT '审核管理员ID',
  `reviewed_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `reviewed_by` (`reviewed_by`),
  CONSTRAINT `real_name_verifications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `real_name_verifications_ibfk_2` FOREIGN KEY (`reviewed_by`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='实名认证信息';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `real_name_verifications`
--

LOCK TABLES `real_name_verifications` WRITE;
/*!40000 ALTER TABLE `real_name_verifications` DISABLE KEYS */;
INSERT INTO `real_name_verifications` VALUES (1,1,'https://oss.example.com/idcard/front/1.jpg','https://oss.example.com/idcard/back/1.jpg','https://oss.example.com/face/1.jpg','approved',NULL,5,'2026-01-02 10:00:00','2026-01-05 23:50:11'),(2,2,'https://oss.example.com/idcard/front/2.jpg','https://oss.example.com/idcard/back/2.jpg','https://oss.example.com/face/2.jpg','approved',NULL,5,'2026-01-02 10:30:00','2026-01-05 23:50:11'),(4,7,'http://lucky-yyf.oss-cn-beijing.aliyuncs.com/lpr%2Fupload%2Fb4671f2c-31ba-4adc-a77c-bf3ddbf95e48.png?OSSAccessKeyId=LTAI5tCJAKHv96E4hYuhUEG4&Expires=1767810602&Signature=wL0G52zRIQl7ChXsj5ljXAD1JCg%3D','http://lucky-yyf.oss-cn-beijing.aliyuncs.com/lpr%2Fupload%2F7054ae6d-0d19-4997-b8e4-33c5ccb1270d.png?OSSAccessKeyId=LTAI5tCJAKHv96E4hYuhUEG4&Expires=1767810602&Signature=NCHhSYua6DS8mqkkIuHf6ywV3Qk%3D',NULL,'pending',NULL,NULL,NULL,'2026-01-07 02:33:59');
/*!40000 ALTER TABLE `real_name_verifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recognition_models`
--

DROP TABLE IF EXISTS `recognition_models`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recognition_models` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `version` varchar(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '0' COMMENT '当前线上模型',
  `accuracy` decimal(5,2) DEFAULT NULL,
  `description` text,
  `file_path` varchar(255) DEFAULT NULL COMMENT '模型权重路径',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `version` (`version`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='模型版本';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recognition_models`
--

LOCK TABLES `recognition_models` WRITE;
/*!40000 ALTER TABLE `recognition_models` DISABLE KEYS */;
INSERT INTO `recognition_models` VALUES (1,'v2.0.0','基础版车牌识别模型',0,98.50,'基础版模型，支持蓝黄白绿牌','/models/lpr_v2.0.0.pth','2026-01-05 23:50:11'),(2,'v2.1.0','增强版车牌识别模型',1,99.20,'增强版模型，支持更多车牌类型和低质量图片','/models/lpr_v2.1.0.pth','2026-01-05 23:50:11'),(3,'v2.2.0-beta','测试版模型',0,99.50,'测试版，优化了新能源车牌识别','/models/lpr_v2.2.0-beta.pth','2026-01-05 23:50:11');
/*!40000 ALTER TABLE `recognition_models` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recognition_presets`
--

DROP TABLE IF EXISTS `recognition_presets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recognition_presets` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `name` varchar(100) NOT NULL,
  `algorithm` varchar(50) NOT NULL,
  `parameters` json NOT NULL,
  `is_default` tinyint(1) DEFAULT '0',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `recognition_presets_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='增强预设';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recognition_presets`
--

LOCK TABLES `recognition_presets` WRITE;
/*!40000 ALTER TABLE `recognition_presets` DISABLE KEYS */;
INSERT INTO `recognition_presets` VALUES (1,2,'我的默认增强','clahe','{\"grid_size\": [8, 8], \"clip_limit\": 2.0}',1,'2026-01-05 23:50:11'),(2,3,'企业专用增强','unsharp','{\"amount\": 1.5, \"radius\": 1.0, \"threshold\": 0}',1,'2026-01-05 23:50:11');
/*!40000 ALTER TABLE `recognition_presets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recognition_results`
--

DROP TABLE IF EXISTS `recognition_results`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recognition_results` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `task_id` bigint DEFAULT NULL COMMENT '关联任务ID（批量/视频）',
  `user_id` bigint NOT NULL,
  `original_image_url` varchar(255) NOT NULL,
  `enhanced_image_url` varchar(255) DEFAULT NULL,
  `license_plate` varchar(20) NOT NULL,
  `plate_type` enum('blue','yellow','green','white','other') DEFAULT NULL,
  `confidence` decimal(5,4) NOT NULL,
  `bbox` json DEFAULT NULL COMMENT '车牌坐标 [x,y,w,h]',
  `enhance_algorithm` varchar(50) DEFAULT NULL,
  `model_version` varchar(20) DEFAULT NULL,
  `processed_at` datetime NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `is_deleted` tinyint(1) DEFAULT '0',
  `processing_time` float DEFAULT NULL COMMENT '处理时长(ms)',
  PRIMARY KEY (`id`),
  KEY `task_id` (`task_id`),
  KEY `idx_user_plate` (`user_id`,`license_plate`),
  KEY `idx_processed_at` (`processed_at`),
  CONSTRAINT `recognition_results_ibfk_1` FOREIGN KEY (`task_id`) REFERENCES `recognition_tasks` (`id`) ON DELETE SET NULL,
  CONSTRAINT `recognition_results_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='识别结果';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recognition_results`
--

LOCK TABLES `recognition_results` WRITE;
/*!40000 ALTER TABLE `recognition_results` DISABLE KEYS */;
INSERT INTO `recognition_results` VALUES (1,1,1,'https://oss.example.com/images/1.jpg','https://oss.example.com/enhanced/1.jpg','京A12345','blue',0.9985,'[100, 80, 180, 60]','clahe','v2.1.0','2026-01-05 09:00:05','2026-01-05 23:50:11',0,NULL),(2,2,2,'https://oss.example.com/images/2_1.jpg','https://oss.example.com/enhanced/2_1.jpg','沪B67890','yellow',0.9978,'[120, 90, 190, 70]','unsharp','v2.1.0','2026-01-05 10:00:05','2026-01-05 23:50:11',0,NULL),(3,2,2,'https://oss.example.com/images/2_2.jpg','https://oss.example.com/enhanced/2_2.jpg','粤C11223','green',0.9965,'[110, 85, 185, 65]','clahe','v2.1.0','2026-01-05 10:00:10','2026-01-05 23:50:11',0,NULL),(4,NULL,2,'https://oss.example.com/images/3.jpg',NULL,'苏D44556','white',0.9990,'[95, 75, 175, 55]','none','v2.1.0','2026-01-05 13:00:00','2026-01-05 23:50:11',0,NULL),(5,7,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/4b052018-649d-4b79-a014-3d2583823268.png',NULL,'京A99999','blue',0.8488,'[99, 475, 223, 532]',NULL,NULL,'2026-01-06 20:20:49','2026-01-06 20:20:49',0,NULL),(6,8,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/3ae4acec-4eb9-4e01-b57c-d4e18fdc260d.png',NULL,'皖AAF77','blue',0.4590,'[10, 38, 508, 197]',NULL,NULL,'2026-01-06 20:26:55','2026-01-06 20:26:54',1,NULL),(8,10,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/c7e274ce-bcd4-47e3-b4c8-58599a19b8a1.png',NULL,'皖A6K50','blue',0.7672,'[6, 0, 809, 222]',NULL,NULL,'2026-01-06 21:00:12','2026-01-06 21:00:11',0,NULL),(10,12,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/96e553c2-4af4-4519-bb0c-0cbed3d4b393.png',NULL,'皖AAF77','blue',0.4590,'[10, 38, 508, 197]',NULL,NULL,'2026-01-06 21:01:04','2026-01-06 21:01:04',0,NULL),(11,13,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/b21961f9-135b-4c97-a707-caa10a9a4037.jpg',NULL,'皖AD18989','blue',0.7432,'[197, 413, 477, 506]',NULL,NULL,'2026-01-06 21:01:56','2026-01-06 21:01:55',0,NULL),(13,15,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/0ff4d505-99da-485b-9653-b6a27770c569.jpg',NULL,'皖AYR388','blue',0.8498,'[150, 513, 421, 595]',NULL,NULL,'2026-01-07 03:29:07','2026-01-07 03:29:07',1,NULL),(14,16,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/2eeaaed7-3907-4e68-a2f3-cec0c6edd991.jpg',NULL,'皖AY8T35','blue',0.8653,'[298, 479, 457, 550]',NULL,NULL,'2026-01-07 03:43:19','2026-01-07 03:43:18',0,NULL),(15,16,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/6549a302-cc36-4174-91fc-06cb2919aa0c.jpg',NULL,'皖APS627','blue',0.8709,'[244, 526, 463, 597]',NULL,NULL,'2026-01-07 03:43:19','2026-01-07 03:43:19',0,NULL),(16,16,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/45f542b3-f235-42a9-aa7d-3e2baf5249c9.jpg',NULL,'豫ADB4566','blue',0.7658,'[232, 523, 406, 571]',NULL,NULL,'2026-01-07 03:43:20','2026-01-07 03:43:19',0,NULL),(17,16,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/057f742f-71ec-4463-b47f-f9b3e1f47d30.jpg',NULL,'皖AET769','blue',0.8859,'[224, 436, 413, 506]',NULL,NULL,'2026-01-07 03:43:20','2026-01-07 03:43:20',0,NULL),(18,16,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/c5bdf8dc-c8f8-4457-a33e-bc4d2cf8c742.jpg',NULL,'皖A48679','blue',0.8773,'[293, 552, 498, 612]',NULL,NULL,'2026-01-07 03:43:21','2026-01-07 03:43:20',0,NULL),(19,17,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/abcdabe5-ae0c-4a5d-9edb-8fb7780e925a.jpg',NULL,'皖A24498','blue',0.8875,'[268, 446, 498, 526]',NULL,NULL,'2026-01-07 03:54:26','2026-01-07 03:54:26',0,NULL),(20,17,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/115478f6-e270-4860-8c4f-2c95e7f89dfb.jpg',NULL,'皖AB320A','blue',0.8767,'[185, 407, 423, 484]',NULL,NULL,'2026-01-07 03:54:27','2026-01-07 03:54:26',0,NULL),(21,17,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/c3af4adb-73af-41dc-a022-476695ba7f03.jpg',NULL,'皖A09L62','blue',0.8677,'[281, 484, 516, 548]',NULL,NULL,'2026-01-07 03:54:27','2026-01-07 03:54:27',0,NULL),(22,17,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/bd9b5e66-596c-43ef-9b14-9a2ee1d2dabe.jpg',NULL,'皖AWL890','blue',0.8718,'[141, 549, 381, 614]',NULL,NULL,'2026-01-07 03:54:28','2026-01-07 03:54:27',0,NULL),(23,18,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/226734ba-bf8a-46c9-a1af-c62689c827c9.jpg',NULL,'皖AY8T35','blue',0.8653,'[298, 479, 457, 550]',NULL,NULL,'2026-01-07 03:55:00','2026-01-07 03:54:59',0,NULL),(24,19,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/c5e06638-8592-4db7-8c37-7d7fdf8ac141.jpg',NULL,'皖AQ8611','blue',0.8706,'[346, 489, 532, 547]',NULL,NULL,'2026-01-07 03:57:02','2026-01-07 03:57:02',0,NULL),(25,20,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/788de9b4-92a7-4eda-a1be-62a56209238c.jpg',NULL,'皖AM387Y','blue',0.8877,'[298, 415, 485, 478]',NULL,NULL,'2026-01-07 04:00:03','2026-01-07 04:00:02',0,NULL),(26,20,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/2fd029ba-2f76-4c5f-b1bd-4dd613ad36ea.jpg',NULL,'皖AAN920','blue',0.8507,'[288, 531, 470, 595]',NULL,NULL,'2026-01-07 04:00:04','2026-01-07 04:00:03',0,NULL),(27,20,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/91750d0e-c82b-4344-a272-74fc13c65088.jpg',NULL,'皖A5M877','blue',0.8667,'[255, 490, 440, 550]',NULL,NULL,'2026-01-07 04:00:04','2026-01-07 04:00:04',0,NULL),(28,21,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/eb14823e-e8d5-4c8a-a351-ef322b54dd5d.jpg',NULL,'皖APS627','blue',0.8709,'[244, 526, 463, 597]',NULL,NULL,'2026-01-07 04:01:19','2026-01-07 04:01:19',0,NULL),(29,21,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/5528006f-33a1-4ec6-91b8-1f90dae97428.jpg',NULL,'皖A5M877','blue',0.8667,'[255, 490, 440, 550]',NULL,NULL,'2026-01-07 04:01:20','2026-01-07 04:01:19',0,NULL),(30,22,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/21323b3a-561e-4112-a50a-29be1c56c324.jpg',NULL,'皖AM387Y','blue',0.8877,'[298, 415, 485, 478]',NULL,NULL,'2026-01-07 04:02:05','2026-01-07 04:02:04',0,NULL),(31,22,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/43a69053-4299-46aa-9ab3-6a04e0764302.jpg',NULL,'皖AAN920','blue',0.8507,'[288, 531, 470, 595]',NULL,NULL,'2026-01-07 04:02:05','2026-01-07 04:02:05',0,NULL),(32,22,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/58f5d01e-8ee2-409f-a1a1-d509f4cd774b.jpg',NULL,'皖A5M877','blue',0.8667,'[255, 490, 440, 550]',NULL,NULL,'2026-01-07 04:02:06','2026-01-07 04:02:05',0,NULL),(33,22,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/d074fee3-5139-4907-aca3-d7aeb35c621f.jpg',NULL,'皖APS627','blue',0.8709,'[244, 526, 463, 597]',NULL,NULL,'2026-01-07 04:02:06','2026-01-07 04:02:06',0,NULL),(34,23,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/d0276fd1-bc32-4dcf-a920-09f2ec3bf488.jpg',NULL,'皖AD41988','blue',0.7784,'[170, 531, 509, 608]',NULL,NULL,'2026-01-07 04:07:02','2026-01-07 04:07:01',0,NULL),(35,23,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/27817699-1a08-469b-9d40-8f569a82b807.jpg',NULL,'皖AD18989','blue',0.7432,'[197, 413, 477, 506]',NULL,NULL,'2026-01-07 04:07:02','2026-01-07 04:07:02',0,NULL),(36,24,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/13a07841-fd9c-43ae-bbbb-178c3674764c.jpg',NULL,'皖A15926','blue',0.8570,'[272, 357, 473, 415]',NULL,NULL,'2026-01-08 01:26:04','2026-01-08 01:26:03',0,NULL),(37,25,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/eead894a-ebc3-40ae-b1d3-a785af2810e1.jpg',NULL,'皖AS8730','blue',0.8865,'[139, 599, 328, 660]',NULL,NULL,'2026-01-08 01:28:36','2026-01-08 01:28:36',0,NULL),(38,26,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/cc7cdb46-1986-4e64-8e72-57b845f261c5.jpg',NULL,'皖AC979U','blue',0.8544,'[185, 470, 406, 534]',NULL,NULL,'2026-01-08 01:28:50','2026-01-08 01:28:49',0,NULL),(39,26,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/45156b7b-820a-4dae-99e1-5a99483a3dd9.jpg',NULL,'皖AFY002','blue',0.8483,'[261, 454, 474, 550]',NULL,NULL,'2026-01-08 01:28:51','2026-01-08 01:28:50',0,NULL),(40,26,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/4d473ad9-c7c5-4e17-8064-7e0e79481424.jpg',NULL,'皖A921Z6','blue',0.7470,'[359, 363, 568, 437]',NULL,NULL,'2026-01-08 01:28:51','2026-01-08 01:28:51',0,NULL),(41,27,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/10e78bff-f1c6-4bdf-acfa-285ac6518c5c.jpg',NULL,'皖A80U968','blue',0.8356,'[195, 555, 387, 610]',NULL,NULL,'2026-01-08 01:29:18','2026-01-08 01:29:18',0,NULL),(42,27,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/e8526696-3231-4220-b107-92ce7a9c6f32.jpg',NULL,'皖AS8730','blue',0.8865,'[139, 599, 328, 660]',NULL,NULL,'2026-01-08 01:29:19','2026-01-08 01:29:18',0,NULL),(43,27,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/ecd8a7d8-4984-4353-b0e6-dd6d55291401.jpg',NULL,'皖AC979U','blue',0.8544,'[185, 470, 406, 534]',NULL,NULL,'2026-01-08 01:29:19','2026-01-08 01:29:19',0,NULL),(44,28,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/134b1dd4-ad0c-41ab-856d-24b44a6c2165.jpg',NULL,'鲁H06200','blue',0.8107,'[253, 472, 438, 545]',NULL,NULL,'2026-01-08 01:31:07','2026-01-08 01:31:07',0,NULL),(45,29,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/76349f70-e040-4309-9eb6-b670546f0552.jpg',NULL,'皖A80U968','blue',0.8356,'[195, 555, 387, 610]',NULL,NULL,'2026-01-08 01:34:52','2026-01-08 01:34:51',0,NULL),(46,30,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/b5a2834e-cdd2-4d85-99c5-c6709aa6a323.jpg',NULL,'皖AC979U','blue',0.8544,'[185, 470, 406, 534]',NULL,NULL,'2026-01-08 01:44:20','2026-01-08 01:44:19',0,1762.12),(47,31,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/221a009f-3e46-4b59-a8b8-60bc8fb60fa1.jpg',NULL,'皖AFY002','blue',0.8483,'[261, 454, 474, 550]',NULL,NULL,'2026-01-08 01:48:43','2026-01-08 01:48:42',0,3736.43),(48,32,7,'https://lucky-yyf-foever-1736511628526081.oss-cn-beijing.oss-accesspoint.aliyuncs.com/lpr/upload/2b7885fb-b21d-4835-846f-92b59d14e727.jpg',NULL,'皖A921Z6','blue',0.7470,'[359, 363, 568, 437]',NULL,NULL,'2026-01-08 01:50:39','2026-01-08 01:50:39',0,3082.65);
/*!40000 ALTER TABLE `recognition_results` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recognition_statistics`
--

DROP TABLE IF EXISTS `recognition_statistics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recognition_statistics` (
  `user_id` bigint NOT NULL,
  `sub_user_id` bigint DEFAULT NULL COMMENT '子账户独立统计',
  `stat_date` date NOT NULL,
  `daily_count` int DEFAULT '0',
  `monthly_count` int DEFAULT '0',
  `video_count` int DEFAULT '0',
  `api_count` int DEFAULT '0',
  PRIMARY KEY (`user_id`,`stat_date`),
  KEY `sub_user_id` (`sub_user_id`),
  CONSTRAINT `recognition_statistics_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `recognition_statistics_ibfk_2` FOREIGN KEY (`sub_user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='识别统计（限额）';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recognition_statistics`
--

LOCK TABLES `recognition_statistics` WRITE;
/*!40000 ALTER TABLE `recognition_statistics` DISABLE KEYS */;
INSERT INTO `recognition_statistics` VALUES (1,NULL,'2026-01-05',5,15,0,0),(2,NULL,'2026-01-05',20,65,2,5),(3,NULL,'2026-01-05',100,350,5,20),(4,3,'2026-01-05',45,120,1,8),(7,NULL,'2026-01-06',9,9,0,0),(7,NULL,'2026-01-07',4,4,0,0),(7,NULL,'2026-01-08',7,7,0,0);
/*!40000 ALTER TABLE `recognition_statistics` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recognition_tasks`
--

DROP TABLE IF EXISTS `recognition_tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recognition_tasks` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `task_uuid` varchar(64) NOT NULL COMMENT '业务任务UUID（前端展示）',
  `user_id` bigint NOT NULL,
  `task_type` enum('single','batch','video','realtime') NOT NULL,
  `status` enum('pending','processing','completed','failed') NOT NULL DEFAULT 'pending',
  `progress` decimal(5,2) DEFAULT '0.00',
  `total_items` int DEFAULT NULL,
  `success_count` int DEFAULT '0',
  `failed_count` int DEFAULT '0',
  `started_at` datetime DEFAULT NULL,
  `finished_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `is_deleted` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `task_uuid` (`task_uuid`),
  KEY `idx_user_status` (`user_id`,`status`),
  KEY `idx_task_uuid` (`task_uuid`),
  CONSTRAINT `recognition_tasks_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='识别任务主表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recognition_tasks`
--

LOCK TABLES `recognition_tasks` WRITE;
/*!40000 ALTER TABLE `recognition_tasks` DISABLE KEYS */;
INSERT INTO `recognition_tasks` VALUES (1,'task_1736064000_001',1,'single','completed',100.00,1,1,0,'2026-01-05 09:00:00','2026-01-05 09:00:05','2026-01-05 23:50:11',0),(2,'task_1736064000_002',2,'batch','completed',100.00,10,9,1,'2026-01-05 10:00:00','2026-01-05 10:00:30','2026-01-05 23:50:11',0),(3,'task_1736064000_003',3,'video','processing',75.00,NULL,NULL,NULL,'2026-01-05 11:00:00',NULL,'2026-01-05 23:50:11',0),(4,'task_1736064000_004',4,'single','failed',0.00,1,0,1,'2026-01-05 12:00:00','2026-01-05 12:00:03','2026-01-05 23:50:11',0),(5,'e8a31cd9-0c2c-4b97-9b99-fe5fe8e8914a',7,'single','failed',0.00,1,0,1,'2026-01-06 20:13:46','2026-01-06 20:13:46','2026-01-06 20:13:46',0),(6,'0b31435a-2d81-4678-8bc5-f9f97285caf3',7,'single','failed',0.00,1,0,1,'2026-01-06 20:18:01','2026-01-06 20:18:02','2026-01-06 20:18:00',0),(7,'aa379589-a7d5-458a-b653-3b3869a1bcd4',7,'single','completed',100.00,1,1,0,'2026-01-06 20:20:48','2026-01-06 20:20:49','2026-01-06 20:20:47',0),(8,'c96823ff-2f36-45ea-bbe8-454eacc24aa1',7,'single','completed',100.00,1,1,0,'2026-01-06 20:26:54','2026-01-06 20:26:55','2026-01-06 20:26:53',0),(10,'4b684d24-4c64-4b55-a41f-c55a42487e80',7,'single','completed',100.00,1,1,0,'2026-01-06 21:00:10','2026-01-06 21:00:12','2026-01-06 21:00:09',0),(12,'1d5fdd03-cb05-4ba2-a596-5b9f3f051454',7,'single','completed',100.00,1,1,0,'2026-01-06 21:01:04','2026-01-06 21:01:04','2026-01-06 21:01:02',0),(13,'b719275d-c568-4b28-b3ff-e9204d1b3b71',7,'single','completed',100.00,1,1,0,'2026-01-06 21:01:55','2026-01-06 21:01:56','2026-01-06 21:01:53',0),(15,'ebd7ff47-014b-4eb9-958e-e8adbf3c94a3',7,'single','completed',100.00,1,1,0,'2026-01-07 03:29:06','2026-01-07 03:29:07','2026-01-07 03:29:04',0),(16,'192bef97-1706-4419-b8a3-eef965e9926c',7,'batch','completed',100.00,5,5,0,'2026-01-07 03:43:16','2026-01-07 03:43:21','2026-01-07 03:43:16',0),(17,'9cd1b334-ef28-4987-8a6e-cf5a8ee543d4',7,'batch','completed',100.00,4,4,0,'2026-01-07 03:54:24','2026-01-07 03:54:28','2026-01-07 03:54:23',0),(18,'906862d0-a47a-4b19-aa79-f6fcdbbf81c4',7,'single','completed',100.00,1,1,0,'2026-01-07 03:54:59','2026-01-07 03:55:00','2026-01-07 03:54:57',0),(19,'a809ce1a-831a-4d8a-9c56-1899061c5fb7',7,'single','completed',100.00,1,1,0,'2026-01-07 03:57:01','2026-01-07 03:57:02','2026-01-07 03:57:00',0),(20,'94a7d8dd-b56e-4dd7-a551-f6b0debdf7fd',7,'batch','completed',100.00,3,3,0,'2026-01-07 04:00:02','2026-01-07 04:00:04','2026-01-07 04:00:01',0),(21,'991b3a40-cd65-4def-836f-d61df9295159',7,'batch','completed',100.00,2,2,0,'2026-01-07 04:01:19','2026-01-07 04:01:20','2026-01-07 04:01:18',0),(22,'4693f62d-9d53-4731-b634-2f34a6c8d822',7,'batch','completed',100.00,4,4,0,'2026-01-07 04:02:04','2026-01-07 04:02:06','2026-01-07 04:02:04',0),(23,'886b0d05-dcf5-4d30-8cf9-e50cae83842b',7,'batch','completed',100.00,3,2,1,'2026-01-07 04:07:00','2026-01-07 04:07:02','2026-01-07 04:07:00',0),(24,'f5296398-08ca-4806-92e8-3dc5ad2247ff',7,'single','completed',100.00,1,1,0,'2026-01-08 01:26:02','2026-01-08 01:26:04','2026-01-08 01:26:01',0),(25,'84abfb4f-75a3-4ece-ad81-d7f9e91d12f3',7,'single','completed',100.00,1,1,0,'2026-01-08 01:28:35','2026-01-08 01:28:36','2026-01-08 01:28:34',0),(26,'f08c9196-b576-4ca7-a4d3-a06b88660236',7,'batch','completed',100.00,3,3,0,'2026-01-08 01:28:49','2026-01-08 01:28:51','2026-01-08 01:28:48',0),(27,'8cc30ca0-24a1-43bb-9a04-d07ac5c64573',7,'batch','completed',100.00,3,3,0,'2026-01-08 01:29:17','2026-01-08 01:29:19','2026-01-08 01:29:17',0),(28,'1277fdb6-b5c9-42ad-af73-fc83ae3c264d',7,'single','completed',100.00,1,1,0,'2026-01-08 01:31:06','2026-01-08 01:31:07','2026-01-08 01:31:05',0),(29,'312f7286-1d62-4932-a388-b091503c15b0',7,'single','completed',100.00,1,1,0,'2026-01-08 01:34:50','2026-01-08 01:34:52','2026-01-08 01:34:49',0),(30,'0b8b2ddc-f19b-43e8-92fc-cb806ee256d1',7,'single','completed',100.00,1,1,0,'2026-01-08 01:44:18','2026-01-08 01:44:20','2026-01-08 01:44:16',0),(31,'626637f1-bc5b-435d-a68c-7597f1d2f5d9',7,'single','completed',100.00,1,1,0,'2026-01-08 01:48:39','2026-01-08 01:48:43','2026-01-08 01:48:38',0),(32,'660ceced-f3f2-48db-b884-92b767c11db2',7,'single','completed',100.00,1,1,0,'2026-01-08 01:50:36','2026-01-08 01:50:39','2026-01-08 01:50:34',0);
/*!40000 ALTER TABLE `recognition_tasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role_permissions`
--

DROP TABLE IF EXISTS `role_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role_permissions` (
  `role_id` bigint NOT NULL,
  `permission_id` bigint NOT NULL,
  PRIMARY KEY (`role_id`,`permission_id`),
  KEY `permission_id` (`permission_id`),
  CONSTRAINT `role_permissions_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE CASCADE,
  CONSTRAINT `role_permissions_ibfk_2` FOREIGN KEY (`permission_id`) REFERENCES `permissions` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='角色-权限关联';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role_permissions`
--

LOCK TABLES `role_permissions` WRITE;
/*!40000 ALTER TABLE `role_permissions` DISABLE KEYS */;
INSERT INTO `role_permissions` VALUES (2,2),(2,3),(3,4),(3,5),(4,6),(4,7),(4,8),(4,9),(5,10),(5,11),(5,12),(5,13),(6,14),(6,15),(6,16),(6,17);
/*!40000 ALTER TABLE `role_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` text,
  `is_system` tinyint(1) NOT NULL DEFAULT '0' COMMENT '系统内置角色不可删除',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='管理员角色';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'super_admin','超级管理员，拥有所有权限',1,'2026-01-05 23:50:11'),(2,'user_manager','用户管理管理员，负责用户与认证相关操作',1,'2026-01-05 23:50:11'),(3,'finance_manager','财务管理员，负责订单与收入相关操作',1,'2026-01-05 23:50:11'),(4,'ops_manager','运营管理员，负责官网内容、活动、公告管理',1,'2026-01-05 23:50:11'),(5,'ai_manager','算法/识别管理员，负责模型与识别服务管理',1,'2026-01-05 23:50:11'),(6,'security_admin','安全/运维管理员，负责系统安全与运维管理',1,'2026-01-05 23:50:11');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `security_logs`
--

DROP TABLE IF EXISTS `security_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `security_logs` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `event_type` varchar(100) NOT NULL,
  `user_id` bigint DEFAULT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `description` text,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `security_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='安全事件日志';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `security_logs`
--

LOCK TABLES `security_logs` WRITE;
/*!40000 ALTER TABLE `security_logs` DISABLE KEYS */;
INSERT INTO `security_logs` VALUES (1,'login_attempt_failed',1,'192.168.1.100','密码错误，连续3次失败','2026-01-05 23:51:43'),(2,'password_changed',2,'192.168.1.101','用户主动修改密码','2026-01-05 23:51:43'),(3,'api_key_created',3,'192.168.1.102','生成新的API密钥，旧密钥已失效','2026-01-05 23:51:43'),(4,'suspicious_activity',NULL,'10.0.0.5','批量尝试访问未授权接口','2026-01-05 23:51:43');
/*!40000 ALTER TABLE `security_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sub_accounts`
--

DROP TABLE IF EXISTS `sub_accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sub_accounts` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `enterprise_user_id` bigint NOT NULL COMMENT '企业主账户ID',
  `sub_user_id` bigint NOT NULL COMMENT '子账户用户ID',
  `role` enum('admin','operator','viewer') NOT NULL DEFAULT 'operator' COMMENT '子账户权限级别',
  `quota_daily` int DEFAULT NULL COMMENT '子账户独立每日识别限额（可覆盖全局）',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_sub` (`enterprise_user_id`,`sub_user_id`),
  KEY `sub_user_id` (`sub_user_id`),
  CONSTRAINT `sub_accounts_ibfk_1` FOREIGN KEY (`enterprise_user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `sub_accounts_ibfk_2` FOREIGN KEY (`sub_user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='企业子账户';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sub_accounts`
--

LOCK TABLES `sub_accounts` WRITE;
/*!40000 ALTER TABLE `sub_accounts` DISABLE KEYS */;
INSERT INTO `sub_accounts` VALUES (1,3,4,'operator',500,'2026-01-05 23:50:11');
/*!40000 ALTER TABLE `sub_accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_configs`
--

DROP TABLE IF EXISTS `system_configs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_configs` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `config_key` varchar(100) NOT NULL,
  `config_value` text NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `is_public` tinyint(1) DEFAULT '0' COMMENT '是否前端可读',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `config_key` (`config_key`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='系统全局配置（限额、SEO、SMTP等）';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_configs`
--

LOCK TABLES `system_configs` WRITE;
/*!40000 ALTER TABLE `system_configs` DISABLE KEYS */;
INSERT INTO `system_configs` VALUES (1,'free_daily_limit','10','免费用户每日识别限额',1,'2026-01-05 23:51:43'),(2,'vip_monthly_limit','50','月卡VIP每日识别限额',1,'2026-01-05 23:51:43'),(3,'vip_yearly_limit','100','年卡VIP每日识别限额',1,'2026-01-05 23:51:43'),(4,'smtp_host','smtp.example.com','SMTP服务器地址',0,'2026-01-05 23:51:43'),(5,'smtp_port','587','SMTP端口',0,'2026-01-05 23:51:43'),(6,'oss_domain','https://oss.example.com','OSS域名',1,'2026-01-05 23:51:43'),(7,'seo_title','DarkVision-LPR - 高精度车牌识别系统','网站SEO标题',1,'2026-01-05 23:51:43'),(8,'total_recognition_count','125680','累计识别车牌数量',1,'2026-01-06 04:38:16'),(9,'service_availability','99.9%','服务可用性',1,'2026-01-06 04:38:16'),(10,'enterprise_clients','500+','企业客户数量',1,'2026-01-06 04:38:16');
/*!40000 ALTER TABLE `system_configs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_logs`
--

DROP TABLE IF EXISTS `system_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_logs` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `level` enum('info','warning','error','critical') NOT NULL,
  `message` text NOT NULL,
  `context` json DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='系统日志';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_logs`
--

LOCK TABLES `system_logs` WRITE;
/*!40000 ALTER TABLE `system_logs` DISABLE KEYS */;
INSERT INTO `system_logs` VALUES (1,'info','系统启动成功','{\"time\": \"2026-01-05 08:00:00\", \"service\": \"lpr-api\", \"version\": \"v2.1.0\"}','2026-01-05 23:51:43'),(2,'warning','模型加载耗时过长','{\"model\": \"v2.1.0\", \"duration\": \"15.2s\", \"threshold\": \"10s\"}','2026-01-05 23:51:43'),(3,'error','OSS存储连接失败','{\"error\": \"connection timeout\", \"endpoint\": \"oss.example.com\"}','2026-01-05 23:51:43'),(4,'critical','数据库连接池耗尽','{\"used\": 50, \"waiters\": 12, \"pool_size\": 50}','2026-01-05 23:51:43');
/*!40000 ALTER TABLE `system_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `third_party_logins`
--

DROP TABLE IF EXISTS `third_party_logins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `third_party_logins` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `provider` enum('wechat','qq','github') NOT NULL,
  `open_id` varchar(255) NOT NULL,
  `union_id` varchar(255) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_provider_openid` (`provider`,`open_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `third_party_logins_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='第三方登录绑定';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `third_party_logins`
--

LOCK TABLES `third_party_logins` WRITE;
/*!40000 ALTER TABLE `third_party_logins` DISABLE KEYS */;
INSERT INTO `third_party_logins` VALUES (1,1,'wechat','wx_openid_123456789','wx_unionid_987654321','2026-01-05 23:51:43'),(2,2,'github','github_123456789',NULL,'2026-01-05 23:51:43');
/*!40000 ALTER TABLE `third_party_logins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_activity_logs`
--

DROP TABLE IF EXISTS `user_activity_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_activity_logs` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `action` enum('login','upload_image','recognition','batch_recognition','export','api_call') NOT NULL,
  `detail` json DEFAULT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_activity_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户行为日志';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_activity_logs`
--

LOCK TABLES `user_activity_logs` WRITE;
/*!40000 ALTER TABLE `user_activity_logs` DISABLE KEYS */;
INSERT INTO `user_activity_logs` VALUES (1,1,'login','{\"device\": \"windows\", \"browser\": \"chrome\"}','192.168.1.100','2026-01-05 23:51:43'),(2,1,'upload_image','{\"file_size\": \"1.2MB\", \"file_type\": \"jpg\"}','192.168.1.100','2026-01-05 23:51:43'),(3,1,'recognition','{\"plate\": \"京A12345\", \"confidence\": 0.9985}','192.168.1.100','2026-01-05 23:51:43'),(4,2,'batch_recognition','{\"failed\": 1, \"success\": 9, \"total_items\": 10}','192.168.1.101','2026-01-05 23:51:43'),(5,3,'api_call','{\"endpoint\": \"/lpr/recognize\", \"api_version\": \"v1\", \"response_time\": \"0.8s\"}','192.168.1.102','2026-01-05 23:51:43');
/*!40000 ALTER TABLE `user_activity_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_memberships`
--

DROP TABLE IF EXISTS `user_memberships`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_memberships` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `membership_type` enum('free','vip_monthly','vip_yearly','enterprise_custom') NOT NULL,
  `start_date` datetime NOT NULL,
  `expire_date` datetime DEFAULT NULL COMMENT '永久会员为NULL',
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_user_active` (`user_id`,`is_active`),
  CONSTRAINT `user_memberships_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='会员状态';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_memberships`
--

LOCK TABLES `user_memberships` WRITE;
/*!40000 ALTER TABLE `user_memberships` DISABLE KEYS */;
INSERT INTO `user_memberships` VALUES (1,1,'free','2026-01-01 00:00:00',NULL,1,'2026-01-05 23:50:11','2026-01-05 23:50:11'),(2,2,'vip_monthly','2026-01-01 00:00:00','2026-02-01 00:00:00',1,'2026-01-05 23:50:11','2026-01-05 23:50:11'),(3,3,'enterprise_custom','2026-01-01 00:00:00','2027-01-01 00:00:00',1,'2026-01-05 23:50:11','2026-01-05 23:50:11'),(5,7,'free','2026-01-06 01:44:38',NULL,1,'2026-01-06 01:44:38','2026-01-06 01:44:37'),(6,8,'free','2026-01-06 02:50:59',NULL,1,'2026-01-06 02:50:59','2026-01-06 02:50:58'),(7,9,'free','2026-01-07 22:48:05',NULL,1,'2026-01-07 22:48:05','2026-01-07 22:48:04');
/*!40000 ALTER TABLE `user_memberships` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_profiles`
--

DROP TABLE IF EXISTS `user_profiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_profiles` (
  `user_id` bigint NOT NULL,
  `real_name` varchar(50) DEFAULT NULL COMMENT '实名姓名（加密存储）',
  `id_card_number` varchar(18) DEFAULT NULL COMMENT '身份证号（加密存储）',
  `gender` enum('male','female','unknown') DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `address` text,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  CONSTRAINT `user_profiles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户扩展信息';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_profiles`
--

LOCK TABLES `user_profiles` WRITE;
/*!40000 ALTER TABLE `user_profiles` DISABLE KEYS */;
INSERT INTO `user_profiles` VALUES (1,'张三','110101199001011234','male','1990-01-01','北京市朝阳区某某街道1号','2026-01-05 23:50:11','2026-01-05 23:50:11'),(2,'李四','110101199002021234','female','1990-02-02','上海市浦东新区某某街道2号','2026-01-05 23:50:11','2026-01-05 23:50:11'),(3,'王五','110101199003031234','male','1990-03-03','广州市天河区某某街道3号','2026-01-05 23:50:11','2026-01-05 23:50:11'),(7,'俞云烽','330683200408101611','unknown','2004-08-10','江苏省/南京市/浦口区/浦口区雨山西路86号南京审计大学','2026-01-06 01:44:38','2026-01-07 04:03:55'),(8,NULL,NULL,NULL,NULL,NULL,'2026-01-06 02:50:59','2026-01-06 02:50:58'),(9,NULL,NULL,NULL,NULL,NULL,'2026-01-07 22:48:05','2026-01-07 22:48:04');
/*!40000 ALTER TABLE `user_profiles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `phone` varchar(11) DEFAULT NULL,
  `nickname` varchar(50) NOT NULL COMMENT '昵称（全局唯一）',
  `email` varchar(100) DEFAULT NULL COMMENT '邮箱（可选）',
  `password_hash` varchar(255) NOT NULL COMMENT '密码哈希（bcrypt）',
  `avatar_url` varchar(255) DEFAULT NULL COMMENT '头像OSS路径',
  `user_type` enum('free','vip','enterprise','admin') NOT NULL DEFAULT 'free' COMMENT '用户类型',
  `parent_id` bigint DEFAULT NULL COMMENT '企业子账户所属主账户ID（仅子账户填写）',
  `status` enum('active','inactive','banned') NOT NULL DEFAULT 'active',
  `banned_reason` text,
  `banned_until` datetime DEFAULT NULL,
  `last_login_at` datetime DEFAULT NULL,
  `last_login_ip` varchar(45) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` datetime DEFAULT NULL COMMENT '软删除',
  PRIMARY KEY (`id`),
  UNIQUE KEY `nickname` (`nickname`),
  UNIQUE KEY `phone` (`phone`),
  UNIQUE KEY `email` (`email`),
  KEY `idx_phone` (`phone`),
  KEY `idx_nickname` (`nickname`),
  KEY `idx_parent` (`parent_id`),
  KEY `idx_status` (`status`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='主用户表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'13800138000','普通用户001','user001@example.com','$2a$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi','https://oss.example.com/avatars/user001.jpg','free',NULL,'active',NULL,NULL,NULL,NULL,'2026-01-05 23:50:11','2026-01-05 23:50:11',NULL),(2,'13800138001','VIP用户001','vip001@example.com','$2a$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi','https://oss.example.com/avatars/vip001.jpg','vip',NULL,'active',NULL,NULL,NULL,NULL,'2026-01-05 23:50:11','2026-01-05 23:50:11',NULL),(3,'13800138002','企业用户001','enterprise001@example.com','$2a$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi','https://oss.example.com/avatars/enterprise001.jpg','enterprise',NULL,'active',NULL,NULL,NULL,NULL,'2026-01-05 23:50:11','2026-01-05 23:50:11',NULL),(4,'13800138003','企业子账户001','sub001@example.com','$2a$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi','https://oss.example.com/avatars/sub001.jpg','enterprise',3,'active',NULL,NULL,NULL,NULL,'2026-01-05 23:50:11','2026-01-05 23:50:11',NULL),(5,'13800138999','系统管理员','admin@darkvision.com','$2b$10$wsE1MI3mJ8NTBlUiMIQm8u6HC0kpP7fDKsMmMmVHtVTTFK0dwjvUm','https://oss.example.com/avatars/admin.jpg','admin',NULL,'active',NULL,NULL,'2026-01-07 23:09:05','127.0.0.1','2026-01-05 23:50:11','2026-01-07 23:09:04',NULL),(7,NULL,'auroral','15968588744@163.com','$2b$12$T52eShAA6muF.wY6QY8uDeKLxa6Qus90SVN10pztx0kbMhj0zREWq','http://lucky-yyf.oss-cn-beijing.aliyuncs.com/lpr%2Fupload%2F7599d650-e60a-46e9-b657-1b7b54906378.jpg?OSSAccessKeyId=LTAI5tCJAKHv96E4hYuhUEG4&Expires=1767815992&Signature=wEeQhjCq781XsrjLZRva2lutCc8%3D','vip',NULL,'active',NULL,NULL,'2026-01-08 01:25:35','127.0.0.1','2026-01-06 01:44:38','2026-01-08 01:25:34',NULL),(8,NULL,'aaa','1957689514@qq.com','$2b$12$PrqqEEJuCFAVf/3XFF8lF.jxpYo5Hjd8fQqc55MAXSSb6C7TUcqea',NULL,'vip',NULL,'active',NULL,NULL,'2026-01-07 22:42:35','127.0.0.1','2026-01-06 02:50:59','2026-01-07 22:42:35',NULL),(9,'15968588744','aaaaa',NULL,'$2b$12$32uulGkcc1unkZGU2ctkAe6ot7AnPUUK5iq91lW5UcRRBDKc7LyLu',NULL,'vip',NULL,'active',NULL,NULL,'2026-01-07 22:48:15','127.0.0.1','2026-01-07 22:48:05','2026-01-08 00:43:32',NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `video_recognition_frames`
--

DROP TABLE IF EXISTS `video_recognition_frames`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `video_recognition_frames` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `task_id` bigint NOT NULL,
  `result_id` bigint DEFAULT NULL,
  `frame_timestamp` decimal(10,3) NOT NULL COMMENT '视频时间戳（秒）',
  `frame_index` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `task_id` (`task_id`),
  KEY `result_id` (`result_id`),
  CONSTRAINT `video_recognition_frames_ibfk_1` FOREIGN KEY (`task_id`) REFERENCES `recognition_tasks` (`id`) ON DELETE CASCADE,
  CONSTRAINT `video_recognition_frames_ibfk_2` FOREIGN KEY (`result_id`) REFERENCES `recognition_results` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='视频识别帧';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `video_recognition_frames`
--

LOCK TABLES `video_recognition_frames` WRITE;
/*!40000 ALTER TABLE `video_recognition_frames` DISABLE KEYS */;
INSERT INTO `video_recognition_frames` VALUES (1,3,NULL,10.500,315),(2,3,NULL,20.750,622),(3,3,NULL,30.200,906);
/*!40000 ALTER TABLE `video_recognition_frames` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `visit_statistics`
--

DROP TABLE IF EXISTS `visit_statistics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `visit_statistics` (
  `stat_date` date NOT NULL COMMENT '统计日期',
  `page_type` varchar(7) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '页面类型',
  `pv` int DEFAULT NULL COMMENT '页面浏览量',
  `uv` int DEFAULT NULL COMMENT '独立访客数（基于IP）',
  `login_uv` int DEFAULT NULL COMMENT '登录用户数（基于user_id）',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`stat_date`,`page_type`),
  KEY `ix_visit_statistics_stat_date` (`stat_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `visit_statistics`
--

LOCK TABLES `visit_statistics` WRITE;
/*!40000 ALTER TABLE `visit_statistics` DISABLE KEYS */;
INSERT INTO `visit_statistics` VALUES ('2026-01-05','about',2,2,1,'2026-01-06 00:05:00','2026-01-06 00:05:00'),('2026-01-05','contact',3,2,1,'2026-01-06 00:05:00','2026-01-06 00:05:00'),('2026-01-05','docs',3,2,2,'2026-01-06 00:05:00','2026-01-06 00:05:00'),('2026-01-05','feature',3,3,1,'2026-01-06 00:05:00','2026-01-06 00:05:00'),('2026-01-05','landing',6,5,3,'2026-01-06 00:05:00','2026-01-06 00:05:00'),('2026-01-05','other',2,2,1,'2026-01-06 00:05:00','2026-01-06 00:05:00'),('2026-01-05','pricing',5,4,3,'2026-01-06 00:05:00','2026-01-06 00:05:00'),('2026-01-06','about',0,0,0,'2026-01-07 00:05:00','2026-01-07 00:05:00'),('2026-01-06','contact',0,0,0,'2026-01-07 00:05:00','2026-01-07 00:05:00'),('2026-01-06','docs',0,0,0,'2026-01-07 00:05:00','2026-01-07 00:05:00'),('2026-01-06','feature',2,2,1,'2026-01-07 00:05:00','2026-01-07 00:05:00'),('2026-01-06','landing',5,4,2,'2026-01-07 00:05:00','2026-01-07 00:05:00'),('2026-01-06','other',0,0,0,'2026-01-07 00:05:00','2026-01-07 00:05:00'),('2026-01-06','pricing',2,2,1,'2026-01-07 00:05:00','2026-01-07 00:05:00'),('2026-01-07','about',0,0,0,'2026-01-08 00:05:00','2026-01-08 00:05:00'),('2026-01-07','admin',39,1,1,'2026-01-07 22:25:17','2026-01-08 01:00:00'),('2026-01-07','contact',1,1,0,'2026-01-08 00:05:00','2026-01-08 00:05:00'),('2026-01-07','docs',1,1,1,'2026-01-08 00:05:00','2026-01-08 00:05:00'),('2026-01-07','feature',0,0,0,'2026-01-08 00:05:00','2026-01-08 00:05:00'),('2026-01-07','landing',4,4,2,'2026-01-08 00:05:00','2026-01-08 00:05:00'),('2026-01-07','other',0,0,0,'2026-01-08 00:05:00','2026-01-08 00:05:00'),('2026-01-07','pricing',2,2,1,'2026-01-08 00:05:00','2026-01-08 00:05:00'),('2026-01-07','user',54,1,3,'2026-01-07 22:31:16','2026-01-08 01:00:00'),('2026-01-07','website',21,1,0,'2026-01-07 22:25:21','2026-01-08 01:00:00'),('2026-01-08','admin',149,1,1,'2026-01-08 00:04:41','2026-01-08 04:39:53'),('2026-01-08','user',64,1,1,'2026-01-08 00:55:51','2026-01-08 03:34:00'),('2026-01-08','website',1,1,0,'2026-01-08 01:12:55','2026-01-08 01:12:55');
/*!40000 ALTER TABLE `visit_statistics` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-01-08  4:41:54
