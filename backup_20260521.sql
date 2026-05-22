-- MariaDB dump 10.19  Distrib 10.4.32-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: BMarketSite_db
-- ------------------------------------------------------
-- Server version	10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin_tbl`
--

DROP TABLE IF EXISTS `admin_tbl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin_tbl` (
  `admin_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `full_name` varchar(64) NOT NULL,
  `address` varchar(254) NOT NULL,
  `contact_number` varchar(16) NOT NULL,
  `email` varchar(128) NOT NULL,
  `username` varchar(64) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`admin_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_tbl`
--

LOCK TABLES `admin_tbl` WRITE;
/*!40000 ALTER TABLE `admin_tbl` DISABLE KEYS */;
INSERT INTO `admin_tbl` VALUES (1,'iaje','filamer','09123456789','iajevaliente@gmail.com','iaje','pbkdf2_sha256$600000$4BrTsFz1zUWJsnBQXzdnaK$ZHRLYIL+kR+qQWW2VCfn7Z20LsjV7SOObXz04i2HjXA=','0000-00-00 00:00:00.000000','2026-05-21 04:56:52.576487');
/*!40000 ALTER TABLE `admin_tbl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add admin',1,'add_admin'),(2,'Can change admin',1,'change_admin'),(3,'Can delete admin',1,'delete_admin'),(4,'Can view admin',1,'view_admin'),(5,'Can add genders',2,'add_genders'),(6,'Can change genders',2,'change_genders'),(7,'Can delete genders',2,'delete_genders'),(8,'Can view genders',2,'view_genders'),(9,'Can add payment',3,'add_payment'),(10,'Can change payment',3,'change_payment'),(11,'Can delete payment',3,'delete_payment'),(12,'Can view payment',3,'view_payment'),(13,'Can add product_ gender',4,'add_product_gender'),(14,'Can change product_ gender',4,'change_product_gender'),(15,'Can delete product_ gender',4,'delete_product_gender'),(16,'Can view product_ gender',4,'view_product_gender'),(17,'Can add product_ size',5,'add_product_size'),(18,'Can change product_ size',5,'change_product_size'),(19,'Can delete product_ size',5,'delete_product_size'),(20,'Can view product_ size',5,'view_product_size'),(21,'Can add users',6,'add_users'),(22,'Can change users',6,'change_users'),(23,'Can delete users',6,'delete_users'),(24,'Can view users',6,'view_users'),(25,'Can add products',7,'add_products'),(26,'Can change products',7,'change_products'),(27,'Can delete products',7,'delete_products'),(28,'Can view products',7,'view_products'),(29,'Can add history',8,'add_history'),(30,'Can change history',8,'change_history'),(31,'Can delete history',8,'delete_history'),(32,'Can view history',8,'view_history'),(33,'Can add cart',9,'add_cart'),(34,'Can change cart',9,'change_cart'),(35,'Can delete cart',9,'delete_cart'),(36,'Can view cart',9,'view_cart'),(37,'Can add log entry',10,'add_logentry'),(38,'Can change log entry',10,'change_logentry'),(39,'Can delete log entry',10,'delete_logentry'),(40,'Can view log entry',10,'view_logentry'),(41,'Can add permission',11,'add_permission'),(42,'Can change permission',11,'change_permission'),(43,'Can delete permission',11,'delete_permission'),(44,'Can view permission',11,'view_permission'),(45,'Can add group',12,'add_group'),(46,'Can change group',12,'change_group'),(47,'Can delete group',12,'delete_group'),(48,'Can view group',12,'view_group'),(49,'Can add user',13,'add_user'),(50,'Can change user',13,'change_user'),(51,'Can delete user',13,'delete_user'),(52,'Can view user',13,'view_user'),(53,'Can add content type',14,'add_contenttype'),(54,'Can change content type',14,'change_contenttype'),(55,'Can delete content type',14,'delete_contenttype'),(56,'Can view content type',14,'view_contenttype'),(57,'Can add session',15,'add_session'),(58,'Can change session',15,'change_session'),(59,'Can delete session',15,'delete_session'),(60,'Can view session',15,'view_session');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cart_tbl`
--

DROP TABLE IF EXISTS `cart_tbl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cart_tbl` (
  `cart_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) DEFAULT NULL,
  `product_name_id` bigint(20) NOT NULL,
  `product_size_id` bigint(20) NOT NULL,
  `product_price` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`cart_id`),
  KEY `cart_tbl_user_id_a6a04e4f_fk_users_tbl_user_id` (`user_id`),
  KEY `cart_tbl_product_name_id_b5da2d95_fk_product_tbl_product_id` (`product_name_id`),
  KEY `fk_cart_product_size` (`product_size_id`),
  CONSTRAINT `cart_tbl_product_name_id_b5da2d95_fk_product_tbl_product_id` FOREIGN KEY (`product_name_id`) REFERENCES `product_tbl` (`product_id`),
  CONSTRAINT `cart_tbl_user_id_a6a04e4f_fk_users_tbl_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_tbl` (`user_id`),
  CONSTRAINT `fk_cart_product_size` FOREIGN KEY (`product_size_id`) REFERENCES `product_size_tbl` (`product_size_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart_tbl`
--

LOCK TABLES `cart_tbl` WRITE;
/*!40000 ALTER TABLE `cart_tbl` DISABLE KEYS */;
/*!40000 ALTER TABLE `cart_tbl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (10,'admin','logentry'),(12,'auth','group'),(11,'auth','permission'),(13,'auth','user'),(14,'contenttypes','contenttype'),(1,'crud','admin'),(9,'crud','cart'),(2,'crud','genders'),(8,'crud','history'),(3,'crud','payment'),(7,'crud','products'),(4,'crud','product_gender'),(5,'crud','product_size'),(6,'crud','users'),(15,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-05-21 04:53:54.383716'),(2,'auth','0001_initial','2026-05-21 04:53:54.772682'),(3,'admin','0001_initial','2026-05-21 04:53:54.858971'),(4,'admin','0002_logentry_remove_auto_add','2026-05-21 04:53:54.864212'),(5,'admin','0003_logentry_add_action_flag_choices','2026-05-21 04:53:54.869589'),(6,'contenttypes','0002_remove_content_type_name','2026-05-21 04:53:54.908589'),(7,'auth','0002_alter_permission_name_max_length','2026-05-21 04:53:54.952023'),(8,'auth','0003_alter_user_email_max_length','2026-05-21 04:53:54.963874'),(9,'auth','0004_alter_user_username_opts','2026-05-21 04:53:54.968660'),(10,'auth','0005_alter_user_last_login_null','2026-05-21 04:53:55.000166'),(11,'auth','0006_require_contenttypes_0002','2026-05-21 04:53:55.002617'),(12,'auth','0007_alter_validators_add_error_messages','2026-05-21 04:53:55.007755'),(13,'auth','0008_alter_user_username_max_length','2026-05-21 04:53:55.018620'),(14,'auth','0009_alter_user_last_name_max_length','2026-05-21 04:53:55.028917'),(15,'auth','0010_alter_group_name_max_length','2026-05-21 04:53:55.039735'),(16,'auth','0011_update_proxy_permissions','2026-05-21 04:53:55.045360'),(17,'auth','0012_alter_user_first_name_max_length','2026-05-21 04:53:55.055495'),(18,'crud','0001_initial','2026-05-21 04:53:55.436426'),(19,'crud','0002_auto_20260520_0951','2026-05-21 04:53:55.483657'),(20,'crud','0003_auto_20260520_1031','2026-05-21 04:53:55.492606'),(21,'sessions','0001_initial','2026-05-21 04:53:55.514970');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `genders_tbl`
--

DROP TABLE IF EXISTS `genders_tbl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `genders_tbl` (
  `gender_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `gender` varchar(55) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`gender_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `genders_tbl`
--

LOCK TABLES `genders_tbl` WRITE;
/*!40000 ALTER TABLE `genders_tbl` DISABLE KEYS */;
INSERT INTO `genders_tbl` VALUES (1,'Male','0000-00-00 00:00:00.000000','0000-00-00 00:00:00.000000'),(2,'Female','0000-00-00 00:00:00.000000','0000-00-00 00:00:00.000000'),(3,'Rather not say','0000-00-00 00:00:00.000000','0000-00-00 00:00:00.000000');
/*!40000 ALTER TABLE `genders_tbl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `history_tbl`
--

DROP TABLE IF EXISTS `history_tbl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `history_tbl` (
  `history_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `order_ref` varchar(128) NOT NULL,
  `buyer_id` bigint(20) NOT NULL,
  `payment_method_id` bigint(20) NOT NULL,
  `product_name_id` bigint(20) NOT NULL,
  `quantity` int(11) NOT NULL,
  `product_price` int(11) NOT NULL,
  `product_total` int(20) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`history_id`),
  KEY `history_tbl_buyer_id_088206f9_fk_users_tbl_user_id` (`buyer_id`),
  KEY `history_tbl_payment_method_id_45e62afc_fk_payment_tbl_payment_id` (`payment_method_id`),
  KEY `history_tbl_product_name_id_024cb4b1_fk_product_tbl_product_id` (`product_name_id`),
  CONSTRAINT `history_tbl_buyer_id_088206f9_fk_users_tbl_user_id` FOREIGN KEY (`buyer_id`) REFERENCES `users_tbl` (`user_id`),
  CONSTRAINT `history_tbl_payment_method_id_45e62afc_fk_payment_tbl_payment_id` FOREIGN KEY (`payment_method_id`) REFERENCES `payment_tbl` (`payment_id`),
  CONSTRAINT `history_tbl_product_name_id_024cb4b1_fk_product_tbl_product_id` FOREIGN KEY (`product_name_id`) REFERENCES `product_tbl` (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `history_tbl`
--

LOCK TABLES `history_tbl` WRITE;
/*!40000 ALTER TABLE `history_tbl` DISABLE KEYS */;
INSERT INTO `history_tbl` VALUES (1,'98E74EF3',2,1,2,2,8095,16190,'2026-05-21 05:34:48.440100','2026-05-21 05:34:48.440112'),(2,'46979A6A',2,2,8,5,6295,31475,'2026-05-21 05:35:48.882101','2026-05-21 05:35:48.882133'),(3,'EC920D6D',4,1,12,1,6795,6795,'2026-05-21 06:34:35.799700','2026-05-21 06:34:35.799764'),(5,'0B45C0EB',4,1,3,1,7595,7595,'2026-05-21 07:17:31.458555','2026-05-21 07:17:31.458591'),(6,'A944C8F5',14,1,2,1,8095,23285,'2026-05-21 07:36:17.892588','2026-05-21 07:36:17.892708'),(7,'A944C8F5',14,1,3,2,7595,23285,'2026-05-21 07:36:17.919704','2026-05-21 07:36:17.919800');
/*!40000 ALTER TABLE `history_tbl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment_tbl`
--

DROP TABLE IF EXISTS `payment_tbl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `payment_tbl` (
  `payment_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `payment_method` varchar(128) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`payment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_tbl`
--

LOCK TABLES `payment_tbl` WRITE;
/*!40000 ALTER TABLE `payment_tbl` DISABLE KEYS */;
INSERT INTO `payment_tbl` VALUES (1,'Cash on Delivery','0000-00-00 00:00:00.000000','0000-00-00 00:00:00.000000'),(2,'Gcash','0000-00-00 00:00:00.000000','0000-00-00 00:00:00.000000');
/*!40000 ALTER TABLE `payment_tbl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_gender_tbl`
--

DROP TABLE IF EXISTS `product_gender_tbl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_gender_tbl` (
  `product_gender_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `product_gender` varchar(128) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`product_gender_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_gender_tbl`
--

LOCK TABLES `product_gender_tbl` WRITE;
/*!40000 ALTER TABLE `product_gender_tbl` DISABLE KEYS */;
INSERT INTO `product_gender_tbl` VALUES (1,'Men','0000-00-00 00:00:00.000000','0000-00-00 00:00:00.000000'),(2,'Women','0000-00-00 00:00:00.000000','0000-00-00 00:00:00.000000');
/*!40000 ALTER TABLE `product_gender_tbl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_size_tbl`
--

DROP TABLE IF EXISTS `product_size_tbl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_size_tbl` (
  `product_size_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `product_size` varchar(128) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`product_size_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_size_tbl`
--

LOCK TABLES `product_size_tbl` WRITE;
/*!40000 ALTER TABLE `product_size_tbl` DISABLE KEYS */;
INSERT INTO `product_size_tbl` VALUES (1,'9','0000-00-00 00:00:00.000000','0000-00-00 00:00:00.000000'),(2,'10','0000-00-00 00:00:00.000000','0000-00-00 00:00:00.000000'),(3,'11','0000-00-00 00:00:00.000000','0000-00-00 00:00:00.000000'),(4,'12','0000-00-00 00:00:00.000000','0000-00-00 00:00:00.000000'),(5,'13','0000-00-00 00:00:00.000000','0000-00-00 00:00:00.000000');
/*!40000 ALTER TABLE `product_size_tbl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_tbl`
--

DROP TABLE IF EXISTS `product_tbl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_tbl` (
  `product_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `product_name` varchar(128) NOT NULL,
  `product_brand` varchar(128) NOT NULL,
  `product_image` varchar(100) NOT NULL,
  `product_gender_id` bigint(20) NOT NULL,
  `product_size_id` bigint(20) NOT NULL,
  `product_price` int(11) NOT NULL,
  `product_quantity` int(11) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`product_id`),
  KEY `product_tbl_product_gender_id_9b9f54f8_fk_product_g` (`product_gender_id`),
  KEY `product_tbl_product_size_id_af2bc4e5_fk_product_s` (`product_size_id`),
  CONSTRAINT `product_tbl_product_gender_id_9b9f54f8_fk_product_g` FOREIGN KEY (`product_gender_id`) REFERENCES `product_gender_tbl` (`product_gender_id`),
  CONSTRAINT `product_tbl_product_size_id_af2bc4e5_fk_product_s` FOREIGN KEY (`product_size_id`) REFERENCES `product_size_tbl` (`product_size_id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_tbl`
--

LOCK TABLES `product_tbl` WRITE;
/*!40000 ALTER TABLE `product_tbl` DISABLE KEYS */;
INSERT INTO `product_tbl` VALUES (2,'Nike Air Max \'Laser 90\'','Nike','product_img/image_2026-05-21_130925946.png',1,3,8095,10,'2026-05-21 05:10:07.529135','2026-05-21 07:41:55.456572'),(3,'Ja 3 \'Kool-Aid\' EP','Nike','product_img/image_2026-05-21_131024424.png',1,4,7595,7,'2026-05-21 05:10:47.598035','2026-05-21 07:36:17.928101'),(4,'Nike Air Max 90 \'Tiempo\'','Nike','product_img/image_2026-05-21_131059510.png',1,4,8095,14,'2026-05-21 05:11:15.059059','2026-05-21 05:11:15.059076'),(5,'Nike Air Max 90 \'Hypervenom\'','Nike','product_img/image_2026-05-21_131126490.png',1,4,8095,11,'2026-05-21 05:11:38.472114','2026-05-21 05:11:38.472127'),(6,'Nike G.T. Cut 4 \'Victor Wembanyama\' EP','Nike','product_img/image_2026-05-21_131151716.png',1,5,11495,9,'2026-05-21 05:12:08.885393','2026-05-21 05:12:08.885419'),(7,'Jordan Pointe','Nike','product_img/image_2026-05-21_131321761.png',2,2,6995,3,'2026-05-21 05:13:35.349016','2026-05-21 05:13:35.349051'),(8,'Nike Air Superfly','Nike','product_img/image_2026-05-21_131350783.png',2,2,6295,13,'2026-05-21 05:14:10.631001','2026-05-21 05:35:48.889433'),(9,'Air Jordan 1 Low','Nike','product_img/image_2026-05-21_131426480.png',2,3,6395,7,'2026-05-21 05:14:38.749650','2026-05-21 05:14:38.749662'),(10,'Nike Air Max 95 Big Bubble','Nike','product_img/image_2026-05-21_131452919.png',2,2,9695,10,'2026-05-21 05:15:04.947896','2026-05-21 07:21:03.687826'),(11,'Nike Air Rift','Nike','product_img/image_2026-05-21_131518885.png',2,2,6295,8,'2026-05-21 05:15:32.400955','2026-05-21 05:15:32.400977'),(12,'204l unisex sneakers - grey','NEW BALANCE','product_img/image_2026-05-21_131630354_P45seY1.png',1,2,6795,23,'2026-05-21 05:17:21.659567','2026-05-21 06:34:35.808997'),(13,'204l unisex sneakers - white','NEW BALANCE','product_img/image_2026-05-21_131808022_mqbkgwT.png',1,2,6795,42,'2026-05-21 05:18:29.461857','2026-05-21 05:18:29.461872'),(14,'1906 men\'s sneakers shoes - grey','NEW BALANCE','product_img/image_2026-05-21_131844255.png',1,2,4897,23,'2026-05-21 05:18:59.898140','2026-05-21 05:18:59.898154'),(15,'327 v1 women\'s sneaker shoes - beige','NEW BALANCE','product_img/image_2026-05-21_131909645.png',2,4,5516,21,'2026-05-21 05:19:35.792920','2026-05-21 05:19:35.792940'),(17,'New balance 327 women\'s sneakers shoes','NEW BALANCE','product_img/image_2026-05-21_132041809.png',1,3,4826,21,'2026-05-21 05:21:01.472013','2026-05-21 05:21:01.472033');
/*!40000 ALTER TABLE `product_tbl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_tbl`
--

DROP TABLE IF EXISTS `users_tbl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_tbl` (
  `user_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `full_name` varchar(64) NOT NULL,
  `gender_id` bigint(20) NOT NULL,
  `birthdate` date NOT NULL,
  `address` varchar(254) NOT NULL,
  `contact_number` varchar(16) NOT NULL,
  `email` varchar(128) NOT NULL,
  `username` varchar(64) NOT NULL,
  `password` varchar(255) NOT NULL,
  `profile_pic` varchar(100) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  KEY `users_tbl_gender_id_76c8e31a_fk_genders_tbl_gender_id` (`gender_id`),
  CONSTRAINT `users_tbl_gender_id_76c8e31a_fk_genders_tbl_gender_id` FOREIGN KEY (`gender_id`) REFERENCES `genders_tbl` (`gender_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_tbl`
--

LOCK TABLES `users_tbl` WRITE;
/*!40000 ALTER TABLE `users_tbl` DISABLE KEYS */;
INSERT INTO `users_tbl` VALUES (2,'Jan Michael Unarce',1,'2001-01-09','Panay ','09591242512','UnarceDe@gmail.com','jan','pbkdf2_sha256$600000$IdInZFnoHfQUC0gGB66ZQh$RVY3Hjx/ePaCsvrGDe/l52I9JPzHOTmKqGduPZ8Vvbs=','profile_pics/bilay2.jpg','2026-05-21 05:22:03.365177','2026-05-21 12:42:41.276654'),(4,'Shindo Amacan',3,'2222-02-22','New','091123412512','iaje.valiente@yahoo.com','shindow','pbkdf2_sha256$600000$zQXCrP2q6h5DR0ccmBFhtD$vvdb9Cv1Z89DIHRBCNl9hw9uQQ/nb1kMaRdUQFhQmOU=','profile_pics/pngtree-humanoid-robot-holding-a-luminous-earth-globe-in-its-hand-png-imag_2eGKclF.webp','2026-05-21 05:39:50.087864','2026-05-21 05:39:50.087882'),(14,'Joven',1,'2001-09-11','Roxas city ','09192312512','joven@gmail.com','joven1','pbkdf2_sha256$600000$YpX7ZFddDSrIv9wHGaA5jW$04lVEQ5jJ3uASUBk6kYFAKAoudN430/HZlBZxV9u6jI=','profile_pics/44792536-2afc-4d7e-a09b-84248758bf93_removalai_preview.png','2026-05-21 07:23:30.696900','2026-05-21 07:23:30.696954');
/*!40000 ALTER TABLE `users_tbl` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-21 20:51:53
