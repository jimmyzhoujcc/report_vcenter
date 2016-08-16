-- MySQL dump 10.13  Distrib 5.7.13, for osx10.11 (x86_64)
--
-- Host: localhost    Database: mysite
-- ------------------------------------------------------
-- Server version	5.7.13

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (2,'group_add_hosts');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (1,2,19),(2,2,20),(3,2,21);
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
  UNIQUE KEY `auth_permission_content_type_id_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permissi_content_type_id_2f476e4b_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add host',7,'add_host'),(20,'Can change host',7,'change_host'),(21,'Can delete host',7,'delete_host'),(22,'Can add category',8,'add_category'),(23,'Can change category',8,'change_category'),(24,'Can delete category',8,'delete_category'),(25,'Can add host_ user',9,'add_host_user'),(26,'Can change host_ user',9,'change_host_user'),(27,'Can delete host_ user',9,'delete_host_user');
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
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$24000$Nr1H4cX6fVKA$8rwv/i1ne9YM3oLt4vd5qs98gsvi+V3x6VBXz7I2IFg=','2016-08-02 17:28:37.970297',1,'jimmy','jimmy','zhou','jimmyzhou@cpic.com',1,1,'2016-07-31 11:38:39.000000'),(2,'pbkdf2_sha256$24000$30hwCaiMdAcl$rN7I4iCXtwY6G1PqJ6G34gEAs6cZ0AQ/Vdvd8HNYqlA=','2016-08-11 11:00:13.212732',1,'zhanghua','hua','zhang','zhanghua@cpic.com',1,1,'2016-07-31 11:42:29.000000'),(3,'pbkdf2_sha256$24000$hEij5LjexWOs$ZSrwFpZkivyKHHG3ojViqAN2u92lhnn3+a9NEtV1DaY=',NULL,0,'lixin','xin','li','lixin@cpic.com',0,1,'2016-07-31 14:46:37.000000'),(4,'pbkdf2_sha256$24000$YzMQkDmK3oag$oiJHh6TcjOiybNGFBudFyYQUC+j3JU9uzYLXYO+0VDw=','2016-08-11 10:59:49.688597',0,'zhaolong','long','zhao','zhaolong@cpic.com',1,1,'2016-07-31 14:47:43.000000'),(5,'pbkdf2_sha256$24000$mtRmkOaOYUWz$j2Z/TGYtrJ6owapUqyc7OYcsC2khleTBfP/Sy3FK25U=','2016-08-02 05:39:22.710233',0,'wujiang','jing','wu','wujing@cpic.com',0,1,'2016-07-31 14:48:35.000000'),(6,'pbkdf2_sha256$24000$sORQoN0tFRv3$C8GxRxVqBJgqCP0pRbU5jHg7fMacbWIKFVrG45vHgs8=','2016-08-11 10:59:32.890245',0,'xujing','jing','xu','xujing@cpic.com',0,1,'2016-07-31 14:49:13.000000'),(7,'pbkdf2_sha256$24000$KwvpMU69BTfW$MzVCDbByGnPrE/bdbUYDsM4RZ8dnG88HaMTgliNvRY8=','2016-08-11 11:01:29.769705',1,'lihai','hai','li','lihai@cpic.com',1,1,'2016-07-31 14:49:49.000000');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
INSERT INTO `auth_user_groups` VALUES (2,2,2),(1,4,2);
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
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
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2016-07-31 11:42:29.620395','2','zhanghua',1,'Added.',4,1),(2,'2016-07-31 11:47:54.118185','2','zhanghua',2,'Changed first_name, last_name and email.',4,1),(3,'2016-07-31 11:48:11.339806','2','zhanghua',2,'Changed is_staff.',4,1),(4,'2016-07-31 12:10:24.640770','2','zhanghua',2,'Changed is_superuser.',4,1),(5,'2016-07-31 12:47:38.710434','1','superuser',1,'Added.',8,1),(6,'2016-07-31 12:47:51.392226','2','admin',1,'Added.',8,1),(7,'2016-07-31 12:47:57.774664','3','user',1,'Added.',8,1),(8,'2016-07-31 13:53:52.548438','17','jimmy',1,'Added.',9,1),(9,'2016-07-31 13:55:12.250303','17','jimmy',2,'Changed manager, department and comment.',9,1),(10,'2016-07-31 14:23:09.640299','19','zhanghua',1,'Added.',9,1),(11,'2016-07-31 14:27:13.749164','1','10.193.100.1',1,'Added.',7,1),(12,'2016-07-31 14:28:11.123164','2','10.193.100.2',1,'Added.',7,1),(13,'2016-07-31 14:29:00.792724','3','10.193.100.3',1,'Added.',7,1),(14,'2016-07-31 14:30:15.337589','4','10.193.100.4',1,'Added.',7,1),(15,'2016-07-31 14:31:25.883311','5','10.193.100.5',1,'Added.',7,1),(16,'2016-07-31 14:32:11.109250','6','10.193.100.6',1,'Added.',7,1),(17,'2016-07-31 14:33:06.630372','7','10.193.100.7',1,'Added.',7,1),(18,'2016-07-31 14:46:37.797172','3','lixin',1,'Added.',4,1),(19,'2016-07-31 14:47:10.614027','20','lixin',1,'Added.',9,1),(20,'2016-07-31 14:47:43.834612','4','zhaolong',1,'Added.',4,1),(21,'2016-07-31 14:48:04.221794','21','zhaolong',1,'Added.',9,1),(22,'2016-07-31 14:48:35.988452','5','wujiang',1,'Added.',4,1),(23,'2016-07-31 14:48:53.612789','22','wujiang',1,'Added.',9,1),(24,'2016-07-31 14:49:13.347478','6','xujing',1,'Added.',4,1),(25,'2016-07-31 14:49:32.846080','23','xujing',1,'Added.',9,1),(26,'2016-07-31 14:49:49.357818','7','lihai',1,'Added.',4,1),(27,'2016-07-31 14:50:07.441305','24','lihai',1,'Added.',9,1),(28,'2016-07-31 15:05:00.412905','4','zhaolong',2,'Changed first_name, last_name and email.',4,1),(29,'2016-07-31 15:05:19.381204','6','xujing',2,'Changed first_name, last_name and email.',4,1),(30,'2016-07-31 15:05:36.766518','5','wujiang',2,'Changed first_name, last_name and email.',4,1),(31,'2016-07-31 15:05:58.939823','3','lixin',2,'Changed first_name, last_name and email.',4,1),(32,'2016-07-31 15:06:17.813149','7','lihai',2,'Changed first_name, last_name and email.',4,1),(33,'2016-07-31 15:06:47.842197','1','jimmy',2,'Changed first_name, last_name and email.',4,1),(34,'2016-07-31 15:10:04.785371','1','10.193.100.1',2,'Changed version.',7,2),(35,'2016-07-31 15:10:25.577653','7','10.193.100.7',2,'Changed visible.',7,2),(36,'2016-07-31 15:10:32.981566','6','10.193.100.6',2,'Changed visible.',7,2),(37,'2016-07-31 15:10:39.800242','5','10.193.100.5',2,'Changed visible.',7,2),(38,'2016-07-31 15:10:47.961295','4','10.193.100.4',2,'Changed visible.',7,2),(39,'2016-07-31 15:11:02.677437','3','10.193.100.3',2,'Changed visible.',7,2),(40,'2016-07-31 15:11:28.652901','1','10.193.100.1',2,'Changed supervisor.',7,2),(41,'2016-07-31 15:11:36.689118','3','10.193.100.3',2,'Changed supervisor.',7,2),(42,'2016-07-31 15:11:46.821242','4','10.193.100.4',2,'Changed supervisor.',7,2),(43,'2016-07-31 15:11:53.960020','5','10.193.100.5',2,'Changed supervisor.',7,2),(44,'2016-07-31 15:12:00.674764','6','10.193.100.6',2,'Changed supervisor.',7,2),(45,'2016-08-02 05:40:24.413879','7','lihai',2,'Changed is_staff.',4,2),(46,'2016-08-02 05:41:20.810398','7','lihai',2,'Changed is_superuser.',4,1),(47,'2016-08-02 15:26:10.513362','4','zhaolong',2,'Changed is_staff.',4,1),(48,'2016-08-02 15:28:28.512910','1','zhaolong',1,'Added.',3,1),(49,'2016-08-02 15:28:57.387459','1','zhaolong',3,'',3,1),(50,'2016-08-02 15:30:50.919564','2','group_add_hosts',1,'Added.',3,1),(51,'2016-08-02 15:31:22.808602','2','group_add_hosts',2,'Changed permissions.',3,1),(52,'2016-08-02 15:31:34.878106','2','group_add_hosts',2,'No fields changed.',3,1),(53,'2016-08-02 15:31:54.191592','4','zhaolong',2,'Changed groups.',4,1),(54,'2016-08-02 16:52:27.709405','2','zhanghua',2,'Changed groups.',4,1);
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
  UNIQUE KEY `django_content_type_app_label_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(6,'sessions','session'),(8,'web','category'),(7,'web','host'),(9,'web','host_user');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2016-07-31 11:19:00.754968'),(2,'auth','0001_initial','2016-07-31 11:19:01.122133'),(3,'admin','0001_initial','2016-07-31 11:19:01.197072'),(4,'admin','0002_logentry_remove_auto_add','2016-07-31 11:19:01.235867'),(5,'contenttypes','0002_remove_content_type_name','2016-07-31 11:19:01.321574'),(6,'auth','0002_alter_permission_name_max_length','2016-07-31 11:19:01.349891'),(7,'auth','0003_alter_user_email_max_length','2016-07-31 11:19:01.387579'),(8,'auth','0004_alter_user_username_opts','2016-07-31 11:19:01.405804'),(9,'auth','0005_alter_user_last_login_null','2016-07-31 11:19:01.440027'),(10,'auth','0006_require_contenttypes_0002','2016-07-31 11:19:01.442656'),(11,'auth','0007_alter_validators_add_error_messages','2016-07-31 11:19:01.460713'),(12,'sessions','0001_initial','2016-07-31 11:19:01.495695'),(13,'web','0001_initial','2016-07-31 11:19:01.700999'),(14,'web','0002_remove_host_user_status','2016-07-31 13:30:47.563531'),(15,'web','0003_auto_20160731_1332','2016-07-31 13:32:42.126892'),(16,'web','0004_auto_20160731_1353','2016-07-31 13:53:11.480835'),(17,'web','0005_auto_20160731_1356','2016-07-31 13:57:05.169470'),(18,'web','0006_auto_20160731_1422','2016-07-31 14:22:20.461997'),(19,'web','0007_host_user_status','2016-07-31 14:36:20.262560'),(20,'web','0008_auto_20160731_1501','2016-07-31 15:01:28.645853');
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
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('6twjn4azy0fz720sccpvt01ajuttpsdy','MTc4NzI3OThjMDFlOTczOTI0NzA5MjE1YjIzMmZkNDZlY2RkY2JhYTp7Il9hdXRoX3VzZXJfaGFzaCI6IjU0M2QwMWY5MThkM2JlMTY3ZmFmNzAwYTRkNTBhMDAyOWE3YWY1MzkiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiI3In0=','2016-08-25 11:01:29.774758');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `web_category`
--

DROP TABLE IF EXISTS `web_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `web_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `web_category`
--

LOCK TABLES `web_category` WRITE;
/*!40000 ALTER TABLE `web_category` DISABLE KEYS */;
INSERT INTO `web_category` VALUES (1,'superuser'),(2,'admin'),(3,'user');
/*!40000 ALTER TABLE `web_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `web_host`
--

DROP TABLE IF EXISTS `web_host`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `web_host` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(15) NOT NULL,
  `name` varchar(15) NOT NULL,
  `location` varchar(15) DEFAULT NULL,
  `version` varchar(10) DEFAULT NULL,
  `comment` varchar(50) DEFAULT NULL,
  `path` varchar(100) NOT NULL,
  `visible` tinyint(1) NOT NULL,
  `create_at` datetime(6) NOT NULL,
  `update_at` datetime(6) NOT NULL,
  `category_id` int(11) NOT NULL,
  `supervisor_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `web_host_category_id_26a9a6d2_fk_web_category_id` (`category_id`),
  KEY `web_host_09a1e5fd` (`supervisor_id`),
  CONSTRAINT `web_host_category_id_26a9a6d2_fk_web_category_id` FOREIGN KEY (`category_id`) REFERENCES `web_category` (`id`),
  CONSTRAINT `web_host_supervisor_id_55824953_fk_web_host_user_id` FOREIGN KEY (`supervisor_id`) REFERENCES `web_host_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `web_host`
--

LOCK TABLES `web_host` WRITE;
/*!40000 ALTER TABLE `web_host` DISABLE KEYS */;
INSERT INTO `web_host` VALUES (1,'10.193.100.1','HMC_1','shanghai','3.4.1.14','','/Users/jcc/PycharmProjects/mysite/web',1,'2016-07-31 14:27:10.000000','2016-07-31 14:27:12.000000',1,20),(2,'10.193.100.2','HMC_2','shanghai','3.4.1.16','','/Users/jcc/PycharmProjects/mysite/web',0,'2016-07-31 14:28:07.000000','2016-07-31 14:28:09.000000',3,19),(3,'10.193.100.3','HMC_3','shanghai','3.4.1.16','','/Users/jcc/PycharmProjects/mysite/web',1,'2016-07-31 14:28:57.000000','2016-07-31 14:28:59.000000',2,21),(4,'10.193.100.4','HMC_4','beijing','3.4.1.16','','/Users/jcc/PycharmProjects/mysite/web',1,'2016-07-31 14:30:10.000000','2016-07-31 14:30:13.000000',2,22),(5,'10.193.100.5','HMC_5','beijing','3.4.1.15','','/Users/jcc/PycharmProjects/mysite/web',1,'2016-07-31 14:31:22.000000','2016-07-31 14:31:24.000000',2,23),(6,'10.193.100.6','HMC_6','beijing','3.4.1.17','','/Users/jcc/PycharmProjects/mysite/web',1,'2016-07-31 14:32:06.000000','2016-07-31 14:32:09.000000',1,24),(7,'10.193.100.7','HMC_7','guangzhou','3.4.1.17','','/Users/jcc/PycharmProjects/mysite/web',1,'2016-07-31 14:33:02.000000','2016-07-31 14:33:04.000000',1,19);
/*!40000 ALTER TABLE `web_host` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `web_host_user`
--

DROP TABLE IF EXISTS `web_host_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `web_host_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(10) DEFAULT NULL,
  `manager` varchar(10) DEFAULT NULL,
  `department` varchar(10) DEFAULT NULL,
  `comment` varchar(50) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `status` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `web_host_user_e8701ad4` (`user_id`),
  CONSTRAINT `web_host_user_user_id_e7471fbb_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `web_host_user`
--

LOCK TABLES `web_host_user` WRITE;
/*!40000 ALTER TABLE `web_host_user` DISABLE KEYS */;
INSERT INTO `web_host_user` VALUES (19,'zhanghua','zjg','dev1','development',2,1),(20,'lixin','lixin','dev-2','development',3,1),(21,'zhaolong','zhaolong','dev-3','development',4,0),(22,'wujiang','wujiang','dev-4','development',5,1),(23,'xujing','xujing','dev-3','development',6,0),(24,'lihai','lihai','dev-2','development',7,1);
/*!40000 ALTER TABLE `web_host_user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-08-16 22:59:09
