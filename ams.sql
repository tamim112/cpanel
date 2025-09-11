/*
SQLyog Ultimate
MySQL - 8.0.31-google : Database - access_management
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
/*Table structure for table `business_units` */

CREATE TABLE `business_units` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sbu_prefix` varchar(20) DEFAULT NULL,
  `sbu_name` varchar(20) DEFAULT NULL,
  `sbu_full_name` varchar(100) DEFAULT NULL,
  `sbu_location` varchar(50) DEFAULT NULL,
  `status` int DEFAULT NULL,
  `field1` varchar(100) DEFAULT NULL,
  `field2` int DEFAULT NULL,
  `note` varchar(255) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `created_by` varchar(512) DEFAULT NULL,
  `updated_on` datetime DEFAULT NULL,
  `updated_by` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;

/*Data for the table `business_units` */

insert  into `business_units`(`id`,`sbu_prefix`,`sbu_name`,`sbu_full_name`,`sbu_location`,`status`,`field1`,`field2`,`note`,`created_on`,`created_by`,`updated_on`,`updated_by`) values 
(1,'10','TCL','Transcom Limited','Gulshan 2, Dhaka',1,'',0,'','2025-09-11 17:03:40',NULL,'2025-09-11 17:03:40',NULL),
(2,'11','SKF','Eskayef Pharma','Banani, Dhaka',1,'',0,'','2025-09-11 12:26:44',NULL,'2025-09-11 12:26:44',NULL);

/*Table structure for table `projects` */

CREATE TABLE `projects` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cid` varchar(20) DEFAULT NULL,
  `project_id` varchar(20) DEFAULT NULL,
  `project_name` varchar(100) DEFAULT NULL,
  `project_description` varchar(200) DEFAULT NULL,
  `status` int DEFAULT NULL,
  `field1` varchar(100) DEFAULT NULL,
  `field2` int DEFAULT NULL,
  `note` varchar(255) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `created_by` varchar(512) DEFAULT NULL,
  `updated_on` datetime DEFAULT NULL,
  `updated_by` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;

/*Data for the table `projects` */

insert  into `projects`(`id`,`cid`,`project_id`,`project_name`,`project_description`,`status`,`field1`,`field2`,`note`,`created_on`,`created_by`,`updated_on`,`updated_by`) values 
(1,'TCL','ams','ams','Access Management System',1,'',0,'','2025-09-11 17:04:15',NULL,'2025-09-11 17:04:15',NULL),
(2,'SKF','expense','expense','Asset Tracking System',1,'',0,'','2025-09-11 12:27:12',NULL,'2025-09-11 12:27:12',NULL);

/*Table structure for table `u_role_has_tasks` */

CREATE TABLE `u_role_has_tasks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cid` varchar(20) DEFAULT NULL,
  `pid` varchar(20) DEFAULT NULL,
  `role_id` varchar(20) DEFAULT NULL,
  `role_name` varchar(100) DEFAULT NULL,
  `task_id` varchar(20) DEFAULT NULL,
  `task_name` varchar(200) DEFAULT NULL,
  `group_id` varchar(20) DEFAULT NULL,
  `group_name` varchar(100) DEFAULT NULL,
  `status` int DEFAULT NULL,
  `field1` varchar(100) DEFAULT NULL,
  `field2` int DEFAULT NULL,
  `note` varchar(255) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `created_by` varchar(512) DEFAULT NULL,
  `updated_on` datetime DEFAULT NULL,
  `updated_by` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb3;

/*Data for the table `u_role_has_tasks` */

insert  into `u_role_has_tasks`(`id`,`cid`,`pid`,`role_id`,`role_name`,`task_id`,`task_name`,`group_id`,`group_name`,`status`,`field1`,`field2`,`note`,`created_on`,`created_by`,`updated_on`,`updated_by`) values 
(11,'TCL',NULL,'1','system_admin','1','company_management',NULL,NULL,1,'',0,'','2025-09-11 17:43:55',NULL,'2025-09-11 17:43:55',NULL),
(12,'TCL',NULL,'1','system_admin','2','project_management',NULL,NULL,1,'',0,'','2025-09-11 17:43:55',NULL,'2025-09-11 17:43:55',NULL),
(13,'TCL',NULL,'1','system_admin','5','role_manage',NULL,NULL,1,'',0,'','2025-09-11 17:43:55',NULL,'2025-09-11 17:43:55',NULL),
(14,'TCL',NULL,'1','system_admin','3','task_group_manage',NULL,NULL,1,'',0,'','2025-09-11 17:43:55',NULL,'2025-09-11 17:43:55',NULL),
(15,'TCL',NULL,'1','system_admin','4','task_manage',NULL,NULL,1,'',0,'','2025-09-11 17:43:55',NULL,'2025-09-11 17:43:55',NULL),
(16,'TCL',NULL,'1','system_admin','6','user_create',NULL,NULL,1,'',0,'','2025-09-11 17:43:55',NULL,'2025-09-11 17:43:55',NULL),
(17,'TCL',NULL,'1','system_admin','8','user_delete',NULL,NULL,1,'',0,'','2025-09-11 17:43:55',NULL,'2025-09-11 17:43:55',NULL),
(18,'TCL',NULL,'1','system_admin','7','user_view',NULL,NULL,1,'',0,'','2025-09-11 17:43:55',NULL,'2025-09-11 17:43:55',NULL),
(25,'TCL',NULL,'2','admin','5','role_manage',NULL,NULL,1,'',0,'','2025-09-11 18:09:48',NULL,'2025-09-11 18:09:48',NULL),
(26,'TCL',NULL,'2','admin','3','task_group_manage',NULL,NULL,1,'',0,'','2025-09-11 18:09:48',NULL,'2025-09-11 18:09:48',NULL),
(27,'TCL',NULL,'2','admin','4','task_manage',NULL,NULL,1,'',0,'','2025-09-11 18:09:48',NULL,'2025-09-11 18:09:48',NULL),
(28,'TCL',NULL,'2','admin','6','user_create',NULL,NULL,1,'',0,'','2025-09-11 18:09:48',NULL,'2025-09-11 18:09:48',NULL),
(29,'TCL',NULL,'2','admin','8','user_delete',NULL,NULL,1,'',0,'','2025-09-11 18:09:48',NULL,'2025-09-11 18:09:48',NULL),
(30,'TCL',NULL,'2','admin','7','user_view',NULL,NULL,1,'',0,'','2025-09-11 18:09:48',NULL,'2025-09-11 18:09:48',NULL),
(32,'SKF',NULL,'3','sysadmin','9','vendor_create',NULL,NULL,1,'',0,'','2025-09-11 12:54:31',NULL,'2025-09-11 12:54:31',NULL);

/*Table structure for table `u_roles` */

CREATE TABLE `u_roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cid` varchar(20) DEFAULT NULL,
  `pid` varchar(20) DEFAULT NULL,
  `role_name` varchar(200) DEFAULT NULL,
  `role_description` varchar(200) DEFAULT NULL,
  `status` int DEFAULT NULL,
  `field1` varchar(100) DEFAULT NULL,
  `field2` int DEFAULT NULL,
  `note` varchar(255) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `created_by` varchar(512) DEFAULT NULL,
  `updated_on` datetime DEFAULT NULL,
  `updated_by` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;

/*Data for the table `u_roles` */

insert  into `u_roles`(`id`,`cid`,`pid`,`role_name`,`role_description`,`status`,`field1`,`field2`,`note`,`created_on`,`created_by`,`updated_on`,`updated_by`) values 
(1,'TCL','ams','system_admin','System Admin',1,'',0,'','2025-09-11 17:14:12',NULL,'2025-09-11 17:14:12',NULL),
(2,'TCL','ams','admin','Admin',1,'',0,'','2025-09-11 17:14:20',NULL,'2025-09-11 17:14:20',NULL),
(3,'SKF','expense','sysadmin','main role',1,'',0,'','2025-09-11 12:28:48',NULL,'2025-09-11 12:28:48',NULL);

/*Table structure for table `u_task_group` */

CREATE TABLE `u_task_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cid` varchar(20) DEFAULT NULL,
  `pid` varchar(20) DEFAULT NULL,
  `group_name` varchar(200) DEFAULT NULL,
  `group_description` varchar(200) DEFAULT NULL,
  `status` int DEFAULT NULL,
  `field1` varchar(100) DEFAULT NULL,
  `field2` int DEFAULT NULL,
  `note` varchar(255) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `created_by` varchar(512) DEFAULT NULL,
  `updated_on` datetime DEFAULT NULL,
  `updated_by` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;

/*Data for the table `u_task_group` */

insert  into `u_task_group`(`id`,`cid`,`pid`,`group_name`,`group_description`,`status`,`field1`,`field2`,`note`,`created_on`,`created_by`,`updated_on`,`updated_by`) values 
(1,'TCL','ams','company','Company',1,'',0,'','2025-09-11 17:04:48',NULL,'2025-09-11 17:04:48',NULL),
(2,'TCL','ams','project','Project',1,'',0,'','2025-09-11 17:05:03',NULL,'2025-09-11 17:05:03',NULL),
(3,'TCL','ams','task_management','Task Management',1,'',0,'','2025-09-11 17:05:31',NULL,'2025-09-11 17:05:31',NULL),
(4,'TCL','ams','role_management','Role Management',1,'',0,'','2025-09-11 17:05:51',NULL,'2025-09-11 17:05:51',NULL),
(5,'TCL','ams','user_management','User Management',1,'',0,'','2025-09-11 17:06:11',NULL,'2025-09-11 17:06:11',NULL),
(6,'SKF','expense','master_setup','Setup Master ',1,'',0,'','2025-09-11 12:27:51',NULL,'2025-09-11 12:27:51',NULL);

/*Table structure for table `u_tasks` */

CREATE TABLE `u_tasks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cid` varchar(20) DEFAULT NULL,
  `pid` varchar(20) DEFAULT NULL,
  `task_name` varchar(200) DEFAULT NULL,
  `task_description` varchar(200) DEFAULT NULL,
  `group_id` varchar(20) DEFAULT NULL,
  `group_name` varchar(100) DEFAULT NULL,
  `status` int DEFAULT NULL,
  `field1` varchar(100) DEFAULT NULL,
  `field2` int DEFAULT NULL,
  `note` varchar(255) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `created_by` varchar(512) DEFAULT NULL,
  `updated_on` datetime DEFAULT NULL,
  `updated_by` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb3;

/*Data for the table `u_tasks` */

insert  into `u_tasks`(`id`,`cid`,`pid`,`task_name`,`task_description`,`group_id`,`group_name`,`status`,`field1`,`field2`,`note`,`created_on`,`created_by`,`updated_on`,`updated_by`) values 
(1,'TCL','ams','company_management','Company management Create, Edit, Delete','1','company',1,'',0,'','2025-09-11 17:06:59',NULL,'2025-09-11 17:06:59',NULL),
(2,'TCL','ams','project_management','Project management','2','project',1,'',0,'','2025-09-11 17:10:22',NULL,'2025-09-11 17:10:22',NULL),
(3,'TCL','ams','task_group_manage','Task group manage','3','task_management',1,'',0,'','2025-09-11 17:11:59',NULL,'2025-09-11 17:11:59',NULL),
(4,'TCL','ams','task_manage','Task manage','3','task_management',1,'',0,'','2025-09-11 17:12:19',NULL,'2025-09-11 17:12:19',NULL),
(5,'TCL','ams','role_manage','Role manage','4','role_management',1,'',0,'','2025-09-11 17:12:36',NULL,'2025-09-11 17:12:36',NULL),
(6,'TCL','ams','user_create','user create','5','user_management',1,'',0,'','2025-09-11 17:12:59',NULL,'2025-09-11 17:12:59',NULL),
(7,'TCL','ams','user_view','user view','5','user_management',1,'',0,'','2025-09-11 17:30:26',NULL,'2025-09-11 17:30:26',NULL),
(8,'TCL','ams','user_delete','User Delete','5','user_management',1,'',0,'','2025-09-11 17:30:36',NULL,'2025-09-11 17:30:36',NULL),
(9,'SKF','expense','vendor_create','Access for Vendor Create','6','master_setup',1,'',0,'','2025-09-11 12:28:15',NULL,'2025-09-11 12:28:15',NULL);

/*Table structure for table `users` */

CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cid` varchar(20) DEFAULT NULL,
  `pid` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `user_id` varchar(20) DEFAULT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `full_name` varchar(200) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `username` varchar(100) NOT NULL DEFAULT '',
  `mobile` varchar(20) DEFAULT NULL,
  `password` varchar(256) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  `user_type` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT 'general',
  `image_path` varchar(200) DEFAULT NULL,
  `role_id` varchar(10) DEFAULT NULL,
  `user_role` varchar(100) DEFAULT NULL,
  `status` int DEFAULT NULL,
  `device_id` varchar(100) DEFAULT NULL,
  `sync_code` int DEFAULT NULL,
  `app_version` varchar(50) DEFAULT NULL,
  `otp_token` int DEFAULT NULL,
  `token_expire_time` datetime DEFAULT NULL,
  `otp_status` int DEFAULT NULL,
  `field1` varchar(100) DEFAULT NULL,
  `field2` int DEFAULT NULL,
  `note` varchar(255) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `created_by` varchar(512) DEFAULT NULL,
  `updated_on` datetime DEFAULT NULL,
  `updated_by` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;

/*Data for the table `users` */

insert  into `users`(`id`,`cid`,`pid`,`user_id`,`first_name`,`last_name`,`full_name`,`email`,`username`,`mobile`,`password`,`gender`,`location`,`user_type`,`image_path`,`role_id`,`user_role`,`status`,`device_id`,`sync_code`,`app_version`,`otp_token`,`token_expire_time`,`otp_status`,`field1`,`field2`,`note`,`created_on`,`created_by`,`updated_on`,`updated_by`) values 
(1,'TCL','ams','1001','System',' Admin','System  Admin','sysadmin@gmail.com','sysadmin','+8801710000001','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','None','Gulshan 2','sysadmin','default_profile.png','1','system_admin',1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2025-09-11 17:22:54',NULL),
(7,'TCL','ams','1002','Admin','','Admin ','admin@gmail.com','admin','012589655166','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','None','Gulshan 2','admin','default_profile.png','2','admin',1,'-',0,NULL,0,NULL,0,'',0,'','2025-09-11 17:24:05',NULL,'2025-09-11 17:24:05',NULL),
(8,'SKF','expense','1003','Expense ','Admin','Expense  Admin','root@gmail.com','stnmy','011111111111','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','None','DHK','sysadmin','default_profile.png','3','sysadmin',1,'-',0,NULL,0,NULL,0,'',0,'','2025-09-11 12:30:19',NULL,'2025-09-11 12:30:19',NULL);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
