# 数据库设计

> 统一命名空间: `zy_hr_` (全小写下划线)
> 数据库名: `zy_hr` (UTF8MB4)

---

## 一、ER 关系总览

```
zy_hr_employee_roster ──→ zy_hr_competency_analysis   (通过 name)
zy_hr_employee_roster ──→ zy_hr_employee_profile      (通过 name)
zy_hr_employee_roster ──→ zy_hr_teacher                (通过 name/teacher)
zy_hr_member ──────────→ zy_hr_score_record            (通过 member_id)
zy_hr_master_studio ───→ zy_hr_master_studio_member    (通过 studio_id)
zy_hr_group_project ───→ zy_hr_group_members           (通过 project_id)
zy_hr_group_project ───→ zy_hr_group_phases            (通过 project_id)
zy_hr_group_phases ────→ zy_hr_group_phase_content     (通过 phase_id)
zy_hr_group_project ───→ zy_hr_group_achievements      (通过 project_id)
zy_hr_group_project ───→ zy_hr_group_dashboards        (通过 project_id)
```

---

## 二、表清单

| # | 表名 | 中文名 | 行数 |
|---|------|--------|------|
| 1 | zy_hr_employee_roster | 员工花名册 | — |
| 2 | zy_hr_employee_profile | 员工档案(事件/证书/荣誉) | — |
| 3 | zy_hr_red_alert | 红色预警 | — |
| 4 | zy_hr_retirement_prediction | 退休人员预测 | — |
| 5 | zy_hr_personnel_statistics | 人员编制统计 | — |
| 6 | zy_hr_competency_analysis | 岗位胜任力分析 | — |
| 7 | zy_hr_talent_pool | 人才库 | — |
| 8 | zy_hr_teacher | 导师帮带关系 | — |
| 9 | zy_hr_score_record | 积分变更记录 | — |
| 10 | zy_hr_member | 积分成员表 | — |
| 11 | zy_hr_master_studio | 大师工作室信息 | — |
| 12 | zy_hr_master_studio_member | 大师工作室成员 | — |
| 13 | zy_hr_group_project | 课题项目 | — |
| 14 | zy_hr_group_members | 课题项目成员 | — |
| 15 | zy_hr_group_phases | 课题项目阶段 | — |
| 16 | zy_hr_group_phase_content | 课题项目阶段内容 | — |
| 17 | zy_hr_group_achievements | 课题项目成果 | — |
| 18 | zy_hr_group_dashboards | 课题项目统计看板 | — |

---

## 三、旧表名 → 新表名映射 (代码迁移用)

| 旧表名 | 新表名 |
|--------|--------|
| `employee_roster` | `zy_hr_employee_roster` |
| `employee_profile` | `zy_hr_employee_profile` |
| `red_alert` | `zy_hr_red_alert` |
| `Retirement_personnel_prediction` | `zy_hr_retirement_prediction` |
| `personnel_statistics` | `zy_hr_personnel_statistics` |
| `position_competency_analysis` | `zy_hr_competency_analysis` |
| `hs_rencai` | `zy_hr_talent_pool` |
| `tb_zjyc_teacher` | `zy_hr_teacher` |
| `tb_zjyc_score_record` | `zy_hr_score_record` |
| `tb_zjyc_member` | `zy_hr_member` |
| `tb_zjyc_masterstudio_info` | `zy_hr_master_studio` |
| `tb_zjyc_masterstudio_member` | `zy_hr_master_studio_member` |
| `tb_zjyc_group_project` | `zy_hr_group_project` |
| `tb_zjyc_group_members` | `zy_hr_group_members` |
| `tb_zjyc_group_phases` | `zy_hr_group_phases` |
| `tb_zjyc_group_phase_content` | `zy_hr_group_phase_content` |
| `tb_zjyc_group_achievements` | `zy_hr_group_achievements` |
| `tb_zjyc_group_dashboards` | `zy_hr_group_dashboards` |

---

## 四、表结构详情

### 4.1 zy_hr_employee_roster (员工花名册)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT PK | 主键ID |
| name | VARCHAR(50) | 员工姓名 |
| gender | VARCHAR(10) | 性别 |
| birth_date | DATE | 出生日期 |
| department | VARCHAR(100) | 部门 |
| current_position | VARCHAR(100) | 当前职位 |
| position_level | INT | 职位级别 |
| education_degree | VARCHAR(50) | 学历 |
| major | VARCHAR(100) | 专业 |
| current_position_years | INT | 当前职位工作时间(年) |
| political_status | VARCHAR(50) | 政治面貌 |
| professional_qualification | VARCHAR(100) | 专业技术资格 |
| vocational_skill_level | VARCHAR(100) | 职业技能等级 |
| work_start_date | DATE | 参加工作时间 |
| company | VARCHAR(100) | 所属公司 |
| created_at / updated_at | DATETIME | 时间戳 |

### 4.2 zy_hr_employee_profile (员工档案)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT PK | 主键ID |
| name | VARCHAR(50) | 员工姓名 |
| department | VARCHAR(100) | 部门 |
| current_position | VARCHAR(100) | 当前职位 |
| technical_certificates | TEXT | 技术证书 |
| skill_certificates | TEXT | 技能证书 |
| municipal_special_projects | TEXT | 市级专项工作 |
| provincial_special_projects | TEXT | 省级专项工作 |
| municipal_research_projects | TEXT | 市级课题 |
| provincial_research_projects | TEXT | 省级课题 |
| ... | TEXT | (竞赛/荣誉字段同上风格) |

### 4.3 zy_hr_red_alert (红色预警)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT PK | 主键ID |
| name | VARCHAR(50) | 姓名 |
| age | INT | 年龄 |
| department | VARCHAR(100) | 部门 |
| warning_type | VARCHAR(50) | 预警类型 |
| alert_level | INT | 预警等级 |
| description | VARCHAR(500) | 预警说明 |
| created_at | DATETIME | 创建时间 |

### 4.4 zy_hr_retirement_prediction (退休预测)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT PK | 主键ID |
| name | VARCHAR(50) | 姓名 |
| retiring_count | INT | 退休人数 |
| department | VARCHAR(100) | 部门 |
| prediction_year | INT | 预测年份 |

### 4.5 zy_hr_personnel_statistics (编制统计)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT PK | 主键ID |
| unit | VARCHAR(100) | 单位名称 |
| department | VARCHAR(100) | 部门名称 |
| authorized_total | INT | 编制总数 |
| authorized_unit_leader | INT | 编制_领导职数 |
| authorized_mid_level | INT | 编制_中层职数 |
| authorized_regular | INT | 编制_一般人员 |
| actual_total | INT | 实有总数 |
| ... | INT | (实有字段同上结构) |
| statistics_date | DATE | 统计日期 |

### 4.6 zy_hr_competency_analysis (胜任力分析)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT PK | 主键ID |
| name | VARCHAR(50) | 姓名 |
| score | DECIMAL(10,2) | 综合评分 |
| level | VARCHAR(50) | 评级 |
| analysis_date | DATE | 分析日期 |

### 4.7 zy_hr_talent_pool (人才库)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT PK | 主键ID |
| name | VARCHAR(50) | 姓名 |
| category | VARCHAR(50) | 人才类别 |
| education | VARCHAR(50) | 学历 |
| department | VARCHAR(100) | 部门 |
| current_position | VARCHAR(100) | 当前职位 |
| major | VARCHAR(100) | 专业 |
| wordcloud_tags | JSON | 词云标签 |
| del_flag | VARCHAR(10) | 删除标记 |

### 4.8 zy_hr_teacher (导师帮带)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT PK | 主键ID |
| name | VARCHAR(50) | 学员姓名 |
| teacher | VARCHAR(50) | 导师姓名 |
| type | VARCHAR(50) | 帮带类型 |
| status | INT | 状态 |

### 4.9 - 4.18 (课题项目组相关表)

课题项目组6张表通过 project_id 关联，形成1:N的树形结构：

```
zy_hr_group_project (1)
  ├─ zy_hr_group_members (N)     ── project_id
  ├─ zy_hr_group_phases (N)      ── project_id
  │   └─ zy_hr_group_phase_content (N) ── phase_id
  ├─ zy_hr_group_achievements (N) ── project_id
  └─ zy_hr_group_dashboards (1)  ── project_id
```

各表详细字段见 `scripts/schema.sql`。
