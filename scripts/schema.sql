-- ============================================================
-- ZY-HR 镇江烟草人才培养数智平台 - 数据库Schema
-- 统一命名空间: zy_hr_ (全小写下划线)
-- 字符集: utf8mb4
-- ============================================================

CREATE DATABASE IF NOT EXISTS `zy_hr` DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `zy_hr`;

-- ============================================================
-- 1. 员工花名册
-- ============================================================
DROP TABLE IF EXISTS `zy_hr_employee_roster`;
CREATE TABLE `zy_hr_employee_roster` (
  `id`            INT           NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name`          VARCHAR(50)   NOT NULL                COMMENT '员工姓名',
  `gender`        VARCHAR(10)   DEFAULT NULL            COMMENT '性别',
  `birth_date`    DATE          DEFAULT NULL            COMMENT '出生日期',
  `department`    VARCHAR(100)  DEFAULT NULL            COMMENT '部门',
  `current_position` VARCHAR(100) DEFAULT NULL          COMMENT '当前职位',
  `position_level` INT          DEFAULT 0              COMMENT '职位级别',
  `education_degree` VARCHAR(50) DEFAULT NULL           COMMENT '学历',
  `major`         VARCHAR(100)  DEFAULT NULL            COMMENT '专业',
  `current_position_years` INT  DEFAULT 0              COMMENT '当前职位工作时间(年)',
  `political_status` VARCHAR(50) DEFAULT NULL           COMMENT '政治面貌/是否党员',
  `professional_qualification` VARCHAR(100) DEFAULT NULL COMMENT '专业技术资格',
  `vocational_skill_level` VARCHAR(100) DEFAULT NULL    COMMENT '职业技能等级',
  `work_start_date` DATE        DEFAULT NULL            COMMENT '参加工作时间',
  `company`       VARCHAR(100)  DEFAULT NULL            COMMENT '所属公司',
  `created_at`    DATETIME     DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at`    DATETIME     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_department` (`department`),
  KEY `idx_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='员工花名册';

-- ============================================================
-- 2. 员工档案（含各类事件字段）
-- ============================================================
DROP TABLE IF EXISTS `zy_hr_employee_profile`;
CREATE TABLE `zy_hr_employee_profile` (
  `id`            INT           NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name`          VARCHAR(50)   NOT NULL                COMMENT '员工姓名',
  `department`    VARCHAR(100)  DEFAULT NULL            COMMENT '部门',
  `current_position` VARCHAR(100) DEFAULT NULL          COMMENT '当前职位',
  `technical_certificates`   TEXT  DEFAULT NULL         COMMENT '技术证书(格式: (2020年)市级:证书名;)',
  `skill_certificates`       TEXT  DEFAULT NULL         COMMENT '技能证书',
  `municipal_special_projects`  TEXT DEFAULT NULL       COMMENT '市级专项工作',
  `provincial_special_projects` TEXT DEFAULT NULL       COMMENT '省级专项工作',
  `municipal_research_projects` TEXT DEFAULT NULL       COMMENT '市级课题',
  `provincial_research_projects` TEXT DEFAULT NULL       COMMENT '省级课题',
  `municipal_competitions`   TEXT  DEFAULT NULL         COMMENT '市级竞赛',
  `provincial_competitions`  TEXT  DEFAULT NULL         COMMENT '省级竞赛',
  `municipal_honors`         TEXT  DEFAULT NULL         COMMENT '市级荣誉',
  `provincial_honors`        TEXT  DEFAULT NULL         COMMENT '省级荣誉',
  `created_at`    DATETIME     DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at`    DATETIME     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='员工档案(事件/证书/荣誉)';

-- ============================================================
-- 3. 红色预警
-- ============================================================
DROP TABLE IF EXISTS `zy_hr_red_alert`;
CREATE TABLE `zy_hr_red_alert` (
  `id`            INT           NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name`          VARCHAR(50)   DEFAULT NULL            COMMENT '姓名',
  `age`           INT           DEFAULT 0              COMMENT '年龄',
  `department`    VARCHAR(100)  DEFAULT NULL            COMMENT '部门',
  `warning_type`  VARCHAR(50)   DEFAULT NULL            COMMENT '预警类型(retirement等)',
  `alert_level`   INT           DEFAULT 0              COMMENT '预警等级',
  `description`   VARCHAR(500)  DEFAULT NULL            COMMENT '预警说明',
  `created_at`    DATETIME      DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_department` (`department`),
  KEY `idx_warning_type` (`warning_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='红色预警';

-- ============================================================
-- 4. 退休人员预测
-- ============================================================
DROP TABLE IF EXISTS `zy_hr_retirement_prediction`;
CREATE TABLE `zy_hr_retirement_prediction` (
  `id`            INT           NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name`          VARCHAR(50)   DEFAULT NULL            COMMENT '姓名',
  `retiring_count` INT          DEFAULT 0              COMMENT '退休人数',
  `department`    VARCHAR(100)  DEFAULT NULL            COMMENT '部门',
  `prediction_year` INT         DEFAULT NULL            COMMENT '预测年份',
  `created_at`    DATETIME      DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_year` (`prediction_year`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='退休人员预测';

-- ============================================================
-- 5. 人员编制统计
-- ============================================================
DROP TABLE IF EXISTS `zy_hr_personnel_statistics`;
CREATE TABLE `zy_hr_personnel_statistics` (
  `id`                        INT           NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `unit`                      VARCHAR(100)  DEFAULT NULL            COMMENT '单位名称',
  `department`                VARCHAR(100)  DEFAULT NULL            COMMENT '部门名称',
  `authorized_total`          INT           DEFAULT 0              COMMENT '人员编制数_总数',
  `authorized_unit_leader`    INT           DEFAULT 0              COMMENT '人员编制数_单位(非)领导职数',
  `authorized_mid_level`      INT           DEFAULT 0              COMMENT '人员编制数_中层职数',
  `authorized_regular`        INT           DEFAULT 0              COMMENT '人员编制数_一般人员',
  `actual_total`              INT           DEFAULT 0              COMMENT '实有人数_总数',
  `actual_unit_leader`        INT           DEFAULT 0              COMMENT '实有人数_单位(非)领导职数',
  `actual_mid_level`          INT           DEFAULT 0              COMMENT '实有人数_中层职数',
  `actual_regular`            INT           DEFAULT 0              COMMENT '实有人数_一般人员',
  `remark`                    VARCHAR(500)  DEFAULT NULL            COMMENT '备注',
  `statistics_date`           DATE          DEFAULT NULL            COMMENT '统计日期',
  `created_at`                DATETIME      DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_department` (`department`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='人员编制统计';

-- ============================================================
-- 6. 岗位胜任力分析
-- ============================================================
DROP TABLE IF EXISTS `zy_hr_competency_analysis`;
CREATE TABLE `zy_hr_competency_analysis` (
  `id`            INT           NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name`          VARCHAR(50)   NOT NULL                COMMENT '姓名',
  `score`         DECIMAL(10,2) DEFAULT 0.00           COMMENT '综合评分',
  `level`         VARCHAR(50)   DEFAULT NULL            COMMENT '评级(优秀/良好/合格等)',
  `analysis_date` DATE          DEFAULT NULL            COMMENT '分析日期',
  `created_at`    DATETIME      DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at`    DATETIME      DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='岗位胜任力分析';

-- ============================================================
-- 7. 人才库
-- ============================================================
DROP TABLE IF EXISTS `zy_hr_talent_pool`;
CREATE TABLE `zy_hr_talent_pool` (
  `id`              INT           NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name`            VARCHAR(50)   NOT NULL                COMMENT '姓名',
  `category`        VARCHAR(50)   DEFAULT NULL            COMMENT '人才类别(admin/innovation/teacher/technical)',
  `education`       VARCHAR(50)   DEFAULT NULL            COMMENT '学历',
  `standard_education` VARCHAR(50) DEFAULT NULL           COMMENT '标准学历',
  `department`      VARCHAR(100)  DEFAULT NULL            COMMENT '部门',
  `current_position` VARCHAR(100) DEFAULT NULL            COMMENT '当前职位',
  `major`           VARCHAR(100)  DEFAULT NULL            COMMENT '专业',
  `wordcloud_tags`  JSON          DEFAULT NULL            COMMENT '词云标签JSON',
  `del_flag`        VARCHAR(10)   DEFAULT '0'             COMMENT '删除标记(0正常/1删除)',
  `created_at`      DATETIME      DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at`      DATETIME      DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_category` (`category`),
  KEY `idx_name` (`name`),
  KEY `idx_del_flag` (`del_flag`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='人才库';

-- ============================================================
-- 8. 导师帮带关系
-- ============================================================
DROP TABLE IF EXISTS `zy_hr_teacher`;
CREATE TABLE `zy_hr_teacher` (
  `id`            INT           NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name`          VARCHAR(50)   NOT NULL                COMMENT '学员姓名',
  `teacher`       VARCHAR(50)   DEFAULT NULL            COMMENT '导师姓名',
  `type`          VARCHAR(50)   DEFAULT NULL            COMMENT '帮带类型(员工/导师)',
  `relationship`  VARCHAR(100)  DEFAULT NULL            COMMENT '师徒关系',
  `start_date`    DATE          DEFAULT NULL            COMMENT '开始日期',
  `end_date`      DATE          DEFAULT NULL            COMMENT '结束日期',
  `status`        INT           DEFAULT 1              COMMENT '状态(1启用/0停用)',
  `created_at`    DATETIME      DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at`    DATETIME      DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_name` (`name`),
  KEY `idx_teacher` (`teacher`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='导师帮带关系';

-- ============================================================
-- 9. 积分变更记录
-- ============================================================
DROP TABLE IF EXISTS `zy_hr_score_record`;
CREATE TABLE `zy_hr_score_record` (
  `id`              INT           NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `member_id`       INT           DEFAULT NULL            COMMENT '成员ID(关联zy_hr_member)',
  `achievement_id`  INT           DEFAULT NULL            COMMENT '关联成果ID',
  `before_score`    INT           DEFAULT 0              COMMENT '变更前积分',
  `after_score`     INT           DEFAULT 0              COMMENT '变更后积分',
  `score_change`    INT           DEFAULT 0              COMMENT '积分变更值',
  `achievement_type` VARCHAR(100) DEFAULT NULL            COMMENT '关联成果类型(论文/专利等)',
  `change_reason`   VARCHAR(500)  DEFAULT NULL            COMMENT '积分变更原因',
  `operation_time`  DATETIME      DEFAULT NULL            COMMENT '积分操作时间',
  `create_time`     DATETIME      DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_member_id` (`member_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='积分变更记录';

-- ============================================================
-- 10. 成员表
-- ============================================================
DROP TABLE IF EXISTS `zy_hr_member`;
CREATE TABLE `zy_hr_member` (
  `id`            INT           NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `member_name`   VARCHAR(50)   NOT NULL                COMMENT '成员姓名',
  `department`    VARCHAR(100)  DEFAULT NULL            COMMENT '部门',
  `member_type`   INT           DEFAULT 0              COMMENT '成员类型',
  `score`         INT           DEFAULT 0              COMMENT '当前积分',
  `created_at`    DATETIME      DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at`    DATETIME      DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_member_name` (`member_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='积分成员表';

-- ============================================================
-- 11. 大师工作室信息
-- ============================================================
DROP TABLE IF EXISTS `zy_hr_master_studio`;
CREATE TABLE `zy_hr_master_studio` (
  `id`            INT           NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name`          VARCHAR(100)  NOT NULL                COMMENT '工作室名称',
  `description`   TEXT          DEFAULT NULL            COMMENT '工作室描述',
  `status`        INT           DEFAULT 1              COMMENT '状态(1启用/0停用)',
  `create_time`   DATETIME      DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at`    DATETIME      DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='大师工作室信息';

-- ============================================================
-- 12. 大师工作室成员
-- ============================================================
DROP TABLE IF EXISTS `zy_hr_master_studio_member`;
CREATE TABLE `zy_hr_master_studio_member` (
  `id`            INT           NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `studio_id`     INT           NOT NULL                COMMENT '工作室ID',
  `member_id`     INT           DEFAULT NULL            COMMENT '成员ID',
  `member_name`   VARCHAR(50)   DEFAULT NULL            COMMENT '成员姓名',
  `role`          VARCHAR(50)   DEFAULT NULL            COMMENT '角色(负责人/成员)',
  `created_at`    DATETIME      DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_studio_id` (`studio_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='大师工作室成员';

-- ============================================================
-- 13. 课题项目
-- ============================================================
DROP TABLE IF EXISTS `zy_hr_group_project`;
CREATE TABLE `zy_hr_group_project` (
  `project_id`        INT           NOT NULL AUTO_INCREMENT COMMENT '项目ID',
  `project_name`      VARCHAR(200)  NOT NULL                COMMENT '项目名称',
  `project_title`     VARCHAR(200)  DEFAULT NULL            COMMENT '项目标题',
  `project_description` TEXT        DEFAULT NULL            COMMENT '项目描述',
  `leader`            VARCHAR(50)   DEFAULT NULL            COMMENT '项目负责人',
  `status`            INT           DEFAULT 1              COMMENT '状态(1进行中/0已结束/-1隐藏)',
  `sort_order`        INT           DEFAULT 0              COMMENT '排序',
  `start_date`        DATE          DEFAULT NULL            COMMENT '开始日期',
  `end_date`          DATE          DEFAULT NULL            COMMENT '结束日期',
  `visibility`        INT           DEFAULT 1              COMMENT '显示(1显示/0隐藏)',
  `created_at`        DATETIME      DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at`        DATETIME      DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`project_id`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='课题项目';

-- ============================================================
-- 14. 课题项目成员
-- ============================================================
DROP TABLE IF EXISTS `zy_hr_group_members`;
CREATE TABLE `zy_hr_group_members` (
  `member_id`     INT           NOT NULL AUTO_INCREMENT COMMENT '成员ID',
  `project_id`    INT           NOT NULL                COMMENT '项目ID',
  `member_name`   VARCHAR(50)   NOT NULL                COMMENT '成员姓名',
  `member_title`  VARCHAR(100)  DEFAULT NULL            COMMENT '成员头衔',
  `member_type`   INT           DEFAULT 0              COMMENT '成员类型',
  `member_image`  VARCHAR(500)  DEFAULT NULL            COMMENT '成员头像URL',
  `sort_order`    INT           DEFAULT 0              COMMENT '排序',
  `created_at`    DATETIME      DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`member_id`),
  KEY `idx_project_id` (`project_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='课题项目成员';

-- ============================================================
-- 15. 课题项目阶段
-- ============================================================
DROP TABLE IF EXISTS `zy_hr_group_phases`;
CREATE TABLE `zy_hr_group_phases` (
  `phase_id`          INT           NOT NULL AUTO_INCREMENT COMMENT '阶段ID',
  `project_id`        INT           NOT NULL                COMMENT '项目ID',
  `phase_name`        VARCHAR(200)  DEFAULT NULL            COMMENT '阶段名称',
  `phase_description` TEXT          DEFAULT NULL            COMMENT '阶段描述',
  `phase_order`       INT           DEFAULT 0              COMMENT '排序',
  `start_date`        DATE          DEFAULT NULL            COMMENT '开始日期',
  `end_date`          DATE          DEFAULT NULL            COMMENT '结束日期',
  `created_at`        DATETIME      DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`phase_id`),
  KEY `idx_project_id` (`project_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='课题项目阶段';

-- ============================================================
-- 16. 课题项目阶段内容
-- ============================================================
DROP TABLE IF EXISTS `zy_hr_group_phase_content`;
CREATE TABLE `zy_hr_group_phase_content` (
  `content_id`       INT           NOT NULL AUTO_INCREMENT COMMENT '内容ID',
  `phase_id`         INT           NOT NULL                COMMENT '阶段ID',
  `project_id`       INT           DEFAULT NULL            COMMENT '项目ID',
  `content_title`    VARCHAR(200)  DEFAULT NULL            COMMENT '内容标题',
  `content_text`     TEXT          DEFAULT NULL            COMMENT '内容文本',
  `sort_order`       INT           DEFAULT 0              COMMENT '排序',
  `created_at`       DATETIME      DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`content_id`),
  KEY `idx_phase_id` (`phase_id`),
  KEY `idx_project_id` (`project_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='课题项目阶段内容';

-- ============================================================
-- 17. 课题项目成果
-- ============================================================
DROP TABLE IF EXISTS `zy_hr_group_achievements`;
CREATE TABLE `zy_hr_group_achievements` (
  `achievement_id`    INT           NOT NULL AUTO_INCREMENT COMMENT '成果ID',
  `project_id`        INT           NOT NULL                COMMENT '项目ID',
  `title`             VARCHAR(200)  NOT NULL                COMMENT '成果标题',
  `type`              VARCHAR(100)  DEFAULT NULL            COMMENT '成果类型(论文/专利/软件著作权等)',
  `description`       TEXT          DEFAULT NULL            COMMENT '成果描述',
  `achievement_date`  DATE          DEFAULT NULL            COMMENT '成果日期',
  `icon`              VARCHAR(500)  DEFAULT NULL            COMMENT '成果图标URL',
  `status`            INT           DEFAULT 1              COMMENT '状态',
  `sort_order`        INT           DEFAULT 0              COMMENT '排序',
  `created_at`        DATETIME      DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at`        DATETIME      DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`achievement_id`),
  KEY `idx_project_id` (`project_id`),
  KEY `idx_type` (`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='课题项目成果';

-- ============================================================
-- 18. 课题项目统计看板
-- ============================================================
DROP TABLE IF EXISTS `zy_hr_group_dashboards`;
CREATE TABLE `zy_hr_group_dashboards` (
  `dashboard_id`    INT           NOT NULL AUTO_INCREMENT COMMENT '看板ID',
  `project_id`      INT           NOT NULL                COMMENT '项目ID',
  `dashboard_name`  VARCHAR(200)  DEFAULT NULL            COMMENT '看板名称',
  `dashboard_status` INT          DEFAULT 1              COMMENT '状态',
  `member_count`    INT           DEFAULT 0              COMMENT '成员数',
  `phase_count`     INT           DEFAULT 0              COMMENT '阶段数',
  `achievement_count` INT         DEFAULT 0              COMMENT '成果数',
  `view_count`      INT           DEFAULT 0              COMMENT '浏览数',
  `created_at`      DATETIME      DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at`      DATETIME      DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`dashboard_id`),
  KEY `idx_project_id` (`project_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='课题项目统计看板';

-- ============================================================
-- 索引汇总
-- ============================================================
-- 所有表均建立外键关联索引以优化 JOIN 查询性能
-- 主表: zy_hr_group_project          → 关联: members/phases/achievements/dashboards
-- 主表: zy_hr_employee_roster        → 关联: competency_analysis/employee_profile/teacher
-- 主表: zy_hr_employee_profile       → 通过 name 关联 employee_roster
-- 主表: zy_hr_talent_pool            → 独立人才库
-- 主表: zy_hr_master_studio          → 关联: master_studio_member
-- 主表: zy_hr_member                 → 关联: score_record
