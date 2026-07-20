-- ============================================================
-- ZY-HR Schema 补齐 + 数据迁移
-- 从 yancao (旧表名) → zy_hr (新表名 zy_hr_ 前缀)
-- ============================================================

USE zy_hr;

-- ============================================================
-- 1. zy_hr_employee_roster (补齐字段)
-- ============================================================
ALTER TABLE zy_hr_employee_roster
  ADD COLUMN `age` int DEFAULT NULL AFTER `name`,
  ADD COLUMN `ethnicity` text DEFAULT NULL AFTER `gender`,
  ADD COLUMN `native_place` text DEFAULT NULL AFTER `ethnicity`,
  ADD COLUMN `party_join_date` text DEFAULT NULL AFTER `birth_date`,
  ADD COLUMN `secondary_department` text DEFAULT NULL AFTER `department`,
  ADD COLUMN `current_position_start_date` text DEFAULT NULL AFTER `current_position`,
  ADD COLUMN `current_position_years` int DEFAULT 0 AFTER `current_position_start_date`,
  ADD COLUMN `current_level_start_date` text DEFAULT NULL AFTER `current_position_years`,
  ADD COLUMN `current_level_years` text DEFAULT NULL AFTER `current_level_start_date`,
  ADD COLUMN `major_category` text DEFAULT NULL AFTER `major`,
  ADD COLUMN `is_urgent_major` text DEFAULT NULL AFTER `major_category`,
  ADD COLUMN `position_nature` varchar(255) DEFAULT NULL AFTER `position_level`,
  ADD COLUMN `original_retirement_age` int DEFAULT NULL AFTER `position_nature`,
  ADD COLUMN `retirement_age` varchar(255) DEFAULT NULL AFTER `original_retirement_age`,
  ADD COLUMN `retirement_date` datetime DEFAULT NULL AFTER `retirement_age`,
  ADD COLUMN `tobacco_company_entry_date` date DEFAULT NULL AFTER `work_start_date`,
  ADD COLUMN `img` text DEFAULT NULL AFTER `company`,
  ADD COLUMN `remarks` text DEFAULT NULL AFTER `img`;

-- ============================================================
-- 2. zy_hr_employee_profile (补齐字段)
-- ============================================================
ALTER TABLE zy_hr_employee_profile
  ADD COLUMN `birth_date` varchar(50) DEFAULT NULL AFTER `name`,
  ADD COLUMN `company` varchar(255) DEFAULT NULL AFTER `birth_date`,
  ADD COLUMN `major` varchar(100) DEFAULT NULL AFTER `current_position`,
  ADD COLUMN `position` varchar(100) DEFAULT NULL AFTER `major`;

-- ============================================================
-- 3. zy_hr_red_alert (旧表结构完全不同，直接重建)
-- ============================================================
DROP TABLE IF EXISTS zy_hr_red_alert;
CREATE TABLE zy_hr_red_alert (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `department` varchar(255) DEFAULT NULL,
  `position` varchar(255) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `retiring_count` int DEFAULT NULL,
  `total_count` text DEFAULT NULL,
  `retirement_ratio` varchar(255) DEFAULT NULL,
  `is_red_alert` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- 4. zy_hr_retirement_prediction (补齐字段)
-- ============================================================
ALTER TABLE zy_hr_retirement_prediction
  ADD COLUMN `position` varchar(255) DEFAULT NULL AFTER `name`,
  ADD COLUMN `is_red_alert` tinyint(1) DEFAULT NULL AFTER `retiring_count`,
  ADD COLUMN `retirement_ratio` decimal(5,2) DEFAULT NULL AFTER `is_red_alert`,
  ADD COLUMN `total_count` int DEFAULT NULL AFTER `retirement_ratio`;

-- ============================================================
-- 5. zy_hr_personnel_statistics (补齐字段)
-- ============================================================
ALTER TABLE zy_hr_personnel_statistics
  ADD COLUMN `authorized_department_leader` int DEFAULT 0 AFTER `authorized_total`,
  ADD COLUMN `authorized_secondary_dept_head` int DEFAULT 0 AFTER `authorized_department_leader`,
  ADD COLUMN `authorized_section_level_non_leader` int DEFAULT 0 AFTER `authorized_secondary_dept_head`,
  ADD COLUMN `authorized_clerk_level12` int DEFAULT 0 AFTER `authorized_section_level_non_leader`,
  ADD COLUMN `authorized_comprehensive_affairs` int DEFAULT 0 AFTER `authorized_clerk_level12`,
  ADD COLUMN `authorized_business_operation` int DEFAULT 0 AFTER `authorized_comprehensive_affairs`,
  ADD COLUMN `actual_department_leader` int DEFAULT 0 AFTER `actual_total`,
  ADD COLUMN `actual_secondary_dept_head` int DEFAULT 0 AFTER `actual_department_leader`,
  ADD COLUMN `actual_section_level_non_leader` int DEFAULT 0 AFTER `actual_secondary_dept_head`,
  ADD COLUMN `actual_clerk_level12` int DEFAULT 0 AFTER `actual_section_level_non_leader`,
  ADD COLUMN `actual_comprehensive_affairs` int DEFAULT 0 AFTER `actual_clerk_level12`,
  ADD COLUMN `actual_business_operation` int DEFAULT 0 AFTER `actual_comprehensive_affairs`,
  ADD COLUMN `created_time` datetime DEFAULT CURRENT_TIMESTAMP,
  ADD COLUMN `updated_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

-- ============================================================
-- 6. zy_hr_competency_analysis (补齐字段)
-- ============================================================
DROP TABLE IF EXISTS zy_hr_competency_analysis;
CREATE TABLE zy_hr_competency_analysis (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `company` varchar(255) DEFAULT NULL,
  `department` varchar(255) DEFAULT NULL,
  `current_position` varchar(255) DEFAULT NULL,
  `target_position` varchar(255) DEFAULT NULL,
  `basic_element_score` varchar(255) DEFAULT NULL,
  `skill_element_score` varchar(255) DEFAULT NULL,
  `bonus_element_score` varchar(255) DEFAULT NULL,
  `comprehensive_score` varchar(255) DEFAULT NULL,
  `score` decimal(10,2) DEFAULT NULL,
  `level` varchar(50) DEFAULT NULL,
  `current_position_competency` varchar(255) DEFAULT NULL,
  `basic_factor_analysis` text DEFAULT NULL,
  `skill_factor_analysis` text DEFAULT NULL,
  `bonus_factor_analysis` text DEFAULT NULL,
  `strength_analysis` varchar(255) DEFAULT NULL,
  `weakness_analysis` varchar(255) DEFAULT NULL,
  `recommendation` varchar(255) DEFAULT NULL,
  `analysis_date` date DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- 7. zy_hr_talent_pool (补齐字段)
-- ============================================================
ALTER TABLE zy_hr_talent_pool
  ADD COLUMN `create_by` bigint DEFAULT NULL AFTER `del_flag`,
  ADD COLUMN `create_dept` bigint DEFAULT NULL AFTER `create_by`,
  ADD COLUMN `create_time` datetime DEFAULT NULL AFTER `create_dept`,
  ADD COLUMN `update_by` bigint DEFAULT NULL AFTER `create_time`,
  ADD COLUMN `update_time` datetime DEFAULT NULL AFTER `update_by`,
  ADD COLUMN `description` varchar(500) DEFAULT '0' AFTER `update_time`,
  ADD COLUMN `order_num` int DEFAULT 0 AFTER `description`,
  ADD COLUMN `photo` varchar(500) DEFAULT NULL AFTER `order_num`,
  ADD COLUMN `tags` varchar(255) DEFAULT NULL AFTER `photo`;

-- ============================================================
-- 8. zy_hr_group_project (补齐字段)
-- ============================================================
ALTER TABLE zy_hr_group_project
  ADD COLUMN `background_image` varchar(500) DEFAULT NULL AFTER `project_description`,
  ADD COLUMN `project_intro1` text DEFAULT NULL AFTER `background_image`,
  ADD COLUMN `project_intro2` text DEFAULT NULL AFTER `project_intro1`,
  ADD COLUMN `project_slogan` varchar(200) DEFAULT NULL AFTER `project_intro2`;

-- ============================================================
-- 9-18. 其他表 (新表完全覆盖旧表字段，无需ALTER)
-- zy_hr_teacher ✅
-- zy_hr_score_record ✅
-- zy_hr_member ✅
-- zy_hr_master_studio ✅
-- zy_hr_master_studio_member ✅
-- zy_hr_group_members ✅
-- zy_hr_group_phases ✅
-- zy_hr_group_phase_content ✅
-- zy_hr_group_achievements ✅
-- zy_hr_group_dashboards ✅
-- ============================================================
