# CCW Mirror - AI镜像服务聚合平台

## 项目简介

CCW Mirror是一个综合性AI服务聚合平台，旨在为用户提供一站式访问多种AI产品的服务。平台集成了主流AI服务（如OpenAI的ChatGPT和Anthropic的Claude），使用户能够在单一界面中与不同的AI模型进行交互，比较不同模型的回答，充分利用各AI产品的独特优势。

## 🌟 核心功能

- **多AI模型集成**: 支持OpenAI (ChatGPT) 和 Anthropic (Claude) 等主流AI模型
- **统一对话界面**: 在单一界面同时与多个AI模型对话
- **对话历史管理**: 保存、查询、分类历史对话记录
- **响应比较**: 方便对比不同AI模型对同一问题的回答差异
- **个性化设置**: 根据用户偏好自定义界面和AI行为
- **API密钥管理**: 安全管理用户的各类AI服务API密钥

## 🔧 技术栈

### 前端
- **框架**: Vue.js 3
- **构建工具**: Vite
- **UI组件库**: Element Plus/Ant Design Vue
- **状态管理**: Pinia
- **路由**: Vue Router
- **HTTP客户端**: Axios
- **语法支持**: TypeScript

### 后端
- **框架**: FastAPI (Python)
- **身份认证**: JWT
- **API文档**: Swagger/OpenAPI
- **异步处理**: Asyncio
- **缓存**: Redis
- **日志管理**: Loguru
- **API请求**: httpx

### 数据库
- **关系型数据库**: MySQL
- **ORM**: SQLAlchemy
- **迁移工具**: Alembic

### DevOps
- **容器化**: Docker
- **版本控制**: Git
- **CI/CD**: GitHub Actions
- **部署**: Nginx + Gunicorn

## 🏗️ 系统架构

```
+----------------+     +----------------+     +----------------+
|                |     |                |     |                |
|  前端应用层     | <=> |  后端服务层     | <=> |  数据持久层     |
|  (Vue.js 3)    |     |  (FastAPI)     |     |  (MySQL)       |
|                |     |                |     |                |
+----------------+     +----------------+     +----------------+
                              ↓
                       +----------------+
                       |                |
                       |  外部AI服务     |
                       |  (OpenAI等)    |
                       |                |
                       +----------------+
```

## 🚀 项目进度

- [x] 项目初始化
- [ ] 系统设计与架构
- [ ] 前端框架搭建
- [ ] 后端API设计
- [ ] 数据库表结构设计
- [ ] OpenAI接口集成
- [ ] Claude接口集成
- [ ] 用户认证系统
- [ ] 对话管理功能
- [ ] 数据分析功能
- [ ] 系统测试
- [ ] 部署上线

## 📋 如何运行

### 前端

```bash
# 进入前端目录
cd front-end/AiMirror

# 安装依赖
npm install

# 开发环境运行
npm run dev

# 构建生产环境
npm run build
```

### 后端

```bash
# 进入后端目录
cd back-end

# 创建并激活虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 运行开发服务器
uvicorn app.main:app --reload
```

### 数据库

```bash
# 数据库迁移
cd back-end
alembic upgrade head
```

## 🔐 环境变量配置

前端环境变量 (.env):
```
VITE_API_BASE_URL=http://localhost:8000/api
```

后端环境变量 (.env):
```
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/aimirror
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

## 👥 贡献指南

1. Fork 项目仓库
2. 创建您的功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开一个 Pull Request

## 📄 许可证

[MIT](LICENSE)

## 📞 联系方式

- 项目链接: [https://github.com/Sakura-zzz9527/CCW_mirror](https://github.com/Sakura-zzz9527/CCW_mirror)