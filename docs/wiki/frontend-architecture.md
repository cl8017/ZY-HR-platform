# 前端架构

> 前端页面清单、技术栈依赖、设计体系说明。

---

## 一、页面清单

### 1.1 根目录页面

| 页面 | 用途 | 行数 | 图表库 | 状态 |
|------|------|------|--------|------|
| `login.html` | 登录页（调用若依 SSO） | 339 | 无 | ✅ 在用 |
| `index.html` | 数据看板（红色预警+退休预测） | 286 | ECharts | ✅ 在用 |
| `board.html` | 人力资源数据驾驶舱 | 295 | ECharts | ✅ 在用 |
| `model.html` | 招聘规划分析模型 | 1460 | Chart.js | ✅ 在用 |
| `model3.html` | 招聘分析模型 3.0 | 1480 | Chart.js | ⚠️ 待确认 |
| `ddc.html` | 文档智能查重 | 1166 | 无 | ✅ 在用 |
| `ddc_v2.html` | 文档查重 v2 | 1195 | 无 | ✅ 在用 |
| `position_competency_analysis.html` | 岗位胜任力分析 | 315 | Chart.js | ✅ 在用 |
| `Recruitment_forecast.html` | 招聘预测 | 454 | ECharts | ✅ 在用 |
| `kakou.html` | 卡口分析 | 528 | - | ⚠️ 待确认 |
| `roc.html` | ROC 分析 | 897 | ECharts | ⚠️ 待确认 |
| `doubao_agent_with_plaza.html` | 豆包智能体 | 590 | - | ⚠️ 待确认 |
| `mammoth_test.html` | Word 解析测试 | 396 | 无 | 🧪 测试页 |
| `login.vue` | 若依 Vue 登录组件 | 310 | Element UI | 🔗 集成参考 |

> 带 时间戳 或 `v1`/`v2` 后缀的文件已在 [重构方案](./refactoring-plan#%E6%96%87%E4%BB%B6%E6%B8%85%E7%90%86%E6%B8%85%E5%8D%95) 中标记为废弃。

### 1.2 子模块页面

| 页面 | 用途 | 行数 | 状态 |
|------|------|------|------|
| `人才库/talent_bank.html` | 人才库主页面 | 1185 | ✅ 在用 |
| `人才库/talent_brand.html` | 品牌人才 | ~500 | ✅ 在用 |
| `人才库/talent-detail.html` | 人才详情 | ~400 | ✅ 在用 |
| `人才库/talent_analysis_dashboard.html` | 人才数据分析 | - | ✅ 在用 |
| `大师工作室/master_class.html` | 大师工作室列表 | 544 | ✅ 在用 |
| `大师工作室/studio-detail.html` | 工作室详情 | ~300 | ✅ 在用 |
| `导师帮带看板/teacher.html` | 导师帮带看板 | 689 | ✅ 在用 |
| `课题项目组/admin-projects.html` | 项目管理后台 | ~700 | ✅ 在用 |
| `课题项目组/project-group.html` | 项目组详情展示 | ~500 | ✅ 在用 |
| `课题项目组/project-group-edit.html` | 项目编辑 | ~400 | ✅ 在用 |
| `课题项目组/group_list.html` | 项目组列表 | ~400 | ✅ 在用 |

---

## 二、CDN 依赖

| 库 | 用途 | 当前版本 | 来源 |
|------|------|---------|------|
| Tailwind CSS | CSS 框架 | latest (CDN) | `cdn.tailwindcss.com` |
| Font Awesome | 图标库 | 4.7.0 / 7.1.0 (混用) | `cdn.jsdelivr.net/npm/font-awesome` |
| ECharts | 数据可视化 | 5.4.3 | `cdn.jsdelivr.net/npm/echarts` |
| Chart.js | 图表库 | 4.4.8 | `cdn.jsdelivr.net/npm/chart.js` |
| ECharts-GL | 3D 可视化 | 2.0.8 | 本地 `assets/js/` |
| AOS | 滚动动画 | 2.3.4 | `cdn.jsdelivr.net/npm/aos` |
| Mammoth.js | Word 解析 | 1.6.0 | `cdn.jsdelivr.net/npm/mammoth` |
| pdf.js | PDF 解析 | 3.4.120 | `cdn.jsdelivr.net/npm/pdfjs-dist` |
| marked.js | Markdown 渲染 | 3.0.8 | `cdn.jsdelivr.net/npm/marked` |
| ECharts WordCloud | 词云 | 2.1.0 | `cdn.jsdelivr.net/npm/echarts-wordcloud` |

---

## 三、设计体系

### 3.1 当前风格差异

每个大模块采用了不同的设计语言：

| 模块 | 主色调 | 设计风格 | 页面 |
|------|--------|---------|------|
| 登录 | 烟草绿 `#1E5A32` | 科技商务风 | login.html |
| 看板 | 深蓝 `#0F172A` | 暗色系数据大屏 | index.html, board.html |
| 人才库 | 亮蓝 `#0EA5E9` | 深色科技风 | talent_bank.html |
| 导师帮带 | 深蓝 `#092047` | 暗色信息看板 | teacher.html |
| 大师工作室 | 蓝 `#0056b3` | 商务卡片风 | master_class.html |
| 文档查重 | 蓝 `#165DFF` | 简洁工具风 | ddc.html |
| 课题项目 | 蓝绿渐变 | 展示型 | admin-projects.html |

### 3.2 统一设计方案

重构后采用一套主题变量贯穿所有页面：

```css
/* 主色板 */
--color-primary: #1E5A32;      /* 烟草绿 — 品牌主色 */
--color-secondary: #0A84FF;    /* 科技蓝 — 辅助色 */
--color-accent: #D4AF37;       /* 金色 — 强调色 */

/* 背景系统 */
--color-bg: #F5F7FA;           /* 页面背景 */
--color-surface: #FFFFFF;      /* 卡片/面板背景 */
--color-dark-bg: #0F172A;      /* 暗色卡片背景（大屏模式） */

/* 文字系统 */
--color-text: #1D2129;
--color-text-secondary: #667085;
--color-text-light: #FFFFFF;

/* 语义色 */
--color-success: #52C41A;
--color-warning: #FAAD14;
--color-danger: #FF4D4F;
--color-info: #165DFF;
```

### 3.3 统一布局结构

```
┌────────────────────────────────────────────────┐
│  Header (固定高度 64px)                         │
│  ├─ Logo / 项目名称                             │
│  ├─ 导航菜单                                    │
│  └─ 用户信息/退出                                │
├────────────┬───────────────────────────────────┤
│  Sidebar   │  Content (主内容区)                │
│  (240px)   │                                   │
│            │   ┌─── Breadcrumb ───┐             │
│  导航项    │   │                   │             │
│  1. 看板   │   │   页面主体内容    │             │
│  2. 人才库 │   │                   │             │
│  3. 导师   │   └───────────────────┘             │
│  4. 工作室 │                                     │
│  5. 项目组 │                                     │
│  6. 查重   │                                     │
└────────────┴───────────────────────────────────┘
```

## 四、重构重点

1. **统一 Tailwind 配置** — 所有页面使用同一份 `tailwind.config`（可通过 `static/js/tailwind-config.js` 共享）
2. **公共布局组件** — header + sidebar 布局统一抽取
3. **API 请求封装** — 统一错误处理、Token 携带
4. **CDN 版本统一** — FontAwesome 统一到 6.x，ECharts 版本锁定
5. **主题色统一** — 烟草绿作为品牌主色贯穿全局
