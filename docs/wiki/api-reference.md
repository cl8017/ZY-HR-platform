# API 接口参考

> 项目全部 REST API 文档。Base URL 取决于部署环境。

---

## 一、接口概览

| 模块 | 前缀 | 接口数量 |
|------|------|---------|
| 数据看板 | `/` (无前缀) | 6 |
| 员工/人事 | `/` (无前缀) | 4 |
| 人才库 | `/api/zjyc/*` + `/api/board/*` | 4 |
| 导师帮带 | `/` + `/api/zjyc/teacher` | 3 |
| 大师工作室 | `/api/zjyc/*` | 1 |
| 课题项目组 | `/api/group/*` | 11 |
| **合计** | | **29** |

---

## 二、响应格式

### 旧风格（部分接口）
```json
// 直接返回数组
[
  {"department": "部门A", "retiring_count": 5}
]
```

### 新风格（课题项目组模块）
```json
{
  "code": 200,
  "msg": "查询成功",
  "data": { ... }
}
```

> 重构后统一为 `{code, msg, data}` 格式。

---

## 三、数据看板

### 3.1 红色预警数据

```
GET /red_alert
```
**响应**: 直接返回 `red_alert` 表全部数据（数组）

### 3.2 退休人员预测

```
GET /retirement_personnel_prediction
```
**查询条件**: `retiring_count > 0`
**响应**: 退休预测人员列表

### 3.3 人员编制统计

```
GET /compilation
```
**响应**: 含所有编制/实有字段的完整统计（字段名含中文别名）

### 3.4 部门预警分析

```
GET /red_alert_department?male_age=63&female_age=58
```
**参数**:
| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `male_age` | int | 63 | 男性退休年龄阈值 |
| `female_age` | int | 58 | 女性退休年龄阈值 |
**响应**: 按部门统计退休人数、占比、是否红色预警

### 3.5 员工花名册

```
GET /employee_roster_markdown?pagesize=1&offset=1
```
**参数**:
| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `pagesize` | int | 1 | 每页条数 |
| `offset` | int | 1 | 偏移量 |
**条件**: `position_level > 10` 且未在 `position_competency_analysis` 表中
**响应**: 员工列表（含中文别名字段）

### 3.6 岗位胜任力分析

```
GET /position_competency_analysis?id=1
```
**参数**:
| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `id` | int | 1 | 员工ID |

---

## 四、人才库

### 4.1 人才评分统计

```
GET /api/zjyc/score
```
**响应**: 人才评分数据

### 4.2 人才分类统计

```
GET /api/zjyc/count_by_category
```
**响应**: 各分类人才数量

### 4.3 人才数据看板

```
GET /api/board/talent/category?category=xxx
```
**参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| `category` | string | 人才分类筛选 |
**响应**: 含专业分类、公司分布、性别分布等多维统计

---

## 五、导师帮带

### 5.1 导师查询

```
GET /api/zjyc/teacher
```
**响应**: 导师关系数据

### 5.2 员工事件查询

```
GET /employee/events?name=员工姓名
```
**参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| `name` | string | 员工姓名 |
**响应**: 该员工的所有事件记录

### 5.3 个人词云

```
GET /person/wordcloud?name=员工姓名
```
**参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| `name` | string | 员工姓名 |
**响应**: 词云数据（词+权重）

---

## 六、大师工作室

### 6.1 创建工作室

```
POST /api/zjyc/create_master_studio
```
**请求体**: 工作室信息 JSON
**响应**: 创建结果

---

## 七、课题项目组

### 7.1 项目列表

```
GET /api/group/projects
```
**响应**: 项目列表（含负责人姓名）

### 7.2 项目详情

```
GET /api/group/<int:project_id>
```
**响应**: 项目完整信息

### 7.3 项目成员

```
GET /api/group/<int:project_id>/members
```

### 7.4 项目阶段

```
GET /api/group/<int:project_id>/phases
```
**响应**: 阶段列表（含阶段内容）

### 7.5 项目成果

```
GET /api/group/<int:project_id>/achievements
```

### 7.6 项目看板

```
GET /api/group/<int:project_id>/dashboard
```
**响应**: 项目进展统计

### 7.7 创建项目

```
POST /api/group/create-project
```
**请求体**:
```json
{
  "project_name": "项目名称",
  "project_title": "项目标题",
  "project_description": "简介",
  "project_intro1": "介绍1",
  "project_intro2": "介绍2",
  "project_slogan": "标语",
  "background_image": "背景图URL",
  "start_date": "2025-01-01",
  "end_date": "2025-12-31",
  "status": 1,
  "leader_name": "负责人姓名"
}
```

### 7.8 添加成员

```
POST /api/group/<int:project_id>/add-member
```
**请求体**: `{member_name, member_title, member_type, ...}`

### 7.9 添加成果

```
POST /api/group/<int:project_id>/add-achievement
```
**请求体**: `{achievement_name, achievement_type, ...}`

### 7.10 项目统计

```
GET /api/group/statistics
```
**响应**: 项目总数、成员总数、成果总数、各类型分布

### 7.11 切换可见性

```
PUT /api/group/<int:project_id>/toggle-visibility
```
**请求体**: `{"is_visible": true/false}`
**说明**: 修改 `status` 字段（1=显示，0=隐藏）

---

## 八、健康检查（重构后新增）

```
GET /api/health
```
**响应**: `{"code": 200, "msg": "ok", "data": {"status": "running", "db": "ok"}}`
