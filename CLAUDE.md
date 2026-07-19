# ZY-HR 镇江烟草人才培养数智平台

## 项目结构

```
ZY-HR/
├── backend/           # Flask 后端（模块化重构中）
│   ├── app.py         # Flask 入口
│   ├── config.py      # 配置管理
│   ├── models/        # 数据模型
│   ├── routes/        # 路由模块（Blueprint）
│   └── services/      # 业务逻辑层
├── static/            # 静态资源（CSS/JS）
├── pages/             # 前端页面
├── scripts/           # 运维脚本
├── docs/wiki/         # 项目文档（必须同步更新）
└── zjyc_api.py        # 原始后端 API（重构目标，1812行）
```

## 开发规范（必须遵守）

### SOP 11 步
所有代码变更必须走完 11 步 SOP：
1. 读 wiki 了解项目结构
2. 敏感词检查（「造假」→「异常」）
3. 聚焦改动，不顺手 refactor 无关代码
4. DB 变更→SQL + wiki + CHANGELOG
5. 三表对齐（API → 表列 → 前端列）
6. 跑测试 + 浏览器实物验证
7. CHANGELOG 同步
8. Wiki 同步（与代码同 PR）
9. Git push（主动推送）
10. 输出真实执行报告

### 前置条件
- 修改前先 `git pull origin main`
- 前端修改后用浏览器实物截图验证
- 每次代码变更后主动 git commit + push

### 注意事项
- 当前部署在 Windows 生产服务器上（不是本机 WSL）
- 本地开发不需要连接真实 DB，测试路由用 mock
- 前端页面在静态 HTML 里，用 Tailwind CDN
- 原始 zjyc_api.py 保持不动，新代码走 backend/
