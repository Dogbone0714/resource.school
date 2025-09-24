# Zeabur 部署指南

本指南将帮助您在 Zeabur 平台上自动部署 Resource School 应用程序。

## 部署前准备

### 1. 确保代码已推送到 Git 仓库
```bash
git add .
git commit -m "准备 Zeabur 部署"
git push origin main
```

### 2. 数据库已配置
- ✅ MySQL 服务已在 Zeabur 上运行
- ✅ 数据库连接信息已更新

## 部署步骤

### 方法一：使用 Zeabur Dashboard（推荐）

1. **登录 Zeabur**
   - 访问 [https://zeabur.com](https://zeabur.com)
   - 使用 GitHub 账号登录

2. **创建新项目**
   - 点击 "New Project"
   - 输入项目名称：`resource-school`

3. **部署后端服务**
   - 点击 "Add Service"
   - 选择 "GitHub Repository"
   - 选择您的仓库
   - 选择 "Dockerfile" 作为部署方式
   - 设置 Dockerfile 路径：`backend/Dockerfile`
   - 设置构建上下文：`.`
   - 添加环境变量：
     ```
     DATABASE_URL=mysql+pymysql://root:0h96Laxmn4Q57N2XBj8oepU1ysO3ErCT@cgk1.clusters.zeabur.com:32188/zeabur
     SECRET_KEY=your-production-secret-key-change-this
     ```
   - 点击 "Deploy"

4. **部署前端服务**
   - 再次点击 "Add Service"
   - 选择相同的 GitHub 仓库
   - 选择 "Dockerfile" 作为部署方式
   - 设置 Dockerfile 路径：`frontend/Dockerfile`
   - 设置构建上下文：`.`
   - 添加环境变量：
     ```
     VITE_API_URL=https://resouceschool.zeabur.app
     ```
   - 点击 "Deploy"

5. **配置域名**
   - 在项目设置中，为前端服务配置自定义域名
   - 设置域名：`resouceschool.zeabur.app`

### 方法二：使用 Zeabur CLI

1. **安装 Zeabur CLI**
   ```bash
   npm install -g @zeabur/cli
   ```

2. **登录**
   ```bash
   zeabur login
   ```

3. **部署项目**
   ```bash
   zeabur deploy
   ```

## 环境变量配置

### 后端环境变量
```
DATABASE_URL=mysql+pymysql://root:0h96Laxmn4Q57N2XBj8oepU1ysO3ErCT@cgk1.clusters.zeabur.com:32188/zeabur
SECRET_KEY=your-production-secret-key-change-this
```

### 前端环境变量
```
VITE_API_URL=https://resouceschool.zeabur.app
```

## 自动部署设置

### 1. 启用自动部署
- 在 Zeabur Dashboard 中，进入项目设置
- 启用 "Auto Deploy" 选项
- 选择要自动部署的分支（通常是 `main` 或 `master`）

### 2. 设置 Webhook（可选）
- 在 GitHub 仓库设置中添加 Webhook
- Webhook URL：`https://api.zeabur.com/webhook/your-project-id`
- 触发事件：Push events

## 监控和日志

### 查看服务状态
- 在 Zeabur Dashboard 中查看服务状态
- 绿色表示运行正常，红色表示有问题

### 查看日志
- 点击服务名称进入详情页
- 在 "Logs" 标签页查看实时日志
- 可以下载日志文件进行详细分析

### 性能监控
- 在 "Metrics" 标签页查看 CPU、内存使用情况
- 监控请求响应时间和错误率

## 故障排除

### 常见问题

1. **构建失败**
   - 检查 Dockerfile 语法
   - 确认所有依赖文件都存在
   - 查看构建日志中的错误信息

2. **服务无法启动**
   - 检查环境变量是否正确设置
   - 确认数据库连接是否正常
   - 查看服务启动日志

3. **数据库连接失败**
   - 确认 MySQL 服务正在运行
   - 检查数据库连接字符串格式
   - 验证用户名和密码

### 调试步骤

1. **本地测试**
   ```bash
   # 测试后端
   cd backend
   python init_database.py
   uvicorn src.main:app --host 0.0.0.0 --port 8000
   
   # 测试前端
   cd frontend
   npm run build
   npm run preview
   ```

2. **检查网络连接**
   - 确认 Zeabur 服务可以访问外部数据库
   - 检查防火墙设置

## 更新部署

### 代码更新后重新部署
1. 推送新代码到 Git 仓库
2. 如果启用了自动部署，系统会自动重新构建和部署
3. 如果没有启用自动部署，手动触发重新部署

### 环境变量更新
1. 在 Zeabur Dashboard 中更新环境变量
2. 重启服务使新环境变量生效

## 安全建议

1. **更改默认密钥**
   - 在生产环境中使用强密钥
   - 定期轮换密钥

2. **数据库安全**
   - 使用强密码
   - 限制数据库访问权限
   - 定期备份数据

3. **HTTPS 配置**
   - 确保所有服务都使用 HTTPS
   - 配置适当的 CORS 策略

## 成本优化

1. **资源使用监控**
   - 定期检查 CPU 和内存使用情况
   - 根据实际需求调整资源配置

2. **自动扩缩容**
   - 配置自动扩缩容规则
   - 在低流量时减少资源使用

## 联系支持

如果遇到问题，可以：
- 查看 Zeabur 官方文档
- 在 Zeabur Discord 社区寻求帮助
- 提交 GitHub Issue
