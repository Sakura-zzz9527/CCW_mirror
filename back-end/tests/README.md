# CCW Mirror API 测试文档

## 测试目录结构

```
tests/
  ├── conftest.py              # pytest配置和共享夹具
  ├── test_api.py              # 原始API测试脚本
  ├── test_api_pytest.py       # 使用pytest框架的API测试
  ├── test_db_connection.py    # 数据库连接测试
  ├── test_results.json        # 测试结果记录
  ├── test_api_issues_summary.md  # 测试问题总结文档
  └── .env                     # 测试环境配置
```

## 运行测试

### 使用批处理文件运行

在项目根目录下，使用以下命令:

```bash
# 运行所有测试
run_tests.bat all

# 仅运行数据库连接测试
run_tests.bat db

# 仅运行API测试
run_tests.bat api

# 运行pytest框架的测试
run_tests.bat pytest
```

### 使用pytest运行

如果要使用pytest框架运行测试，请使用以下命令:

```bash
# 使用pytest运行全部测试
pytest -xvs tests/

# 运行特定测试文件
pytest -xvs tests/test_api_pytest.py

# 生成测试覆盖率报告
pytest --cov=app tests/
```

## 测试结果

测试结果将保存在 `tests/test_results.json` 文件中，包含成功和失败的测试详情。你也可以在控制台查看实时测试结果。

## 测试环境配置

测试使用 `tests/.env` 文件中的环境变量，可以添加以下测试特定的配置：

```
# 测试配置示例
TEST_BASE_URL=http://localhost:8000
```

## 添加新测试

1. 对于标准测试，可以直接在 `test_api.py` 中添加新的测试函数
2. 对于使用pytest框架的测试，在 `test_api_pytest.py` 中添加新的测试函数
3. 所有测试应该使用 `conftest.py` 中定义的夹具和工具函数

## 常见问题和故障排除

请参考 `test_api_issues_summary.md` 文件，其中包含了测试过程中发现的问题和解决方案。

## 常见错误及解决方法

1. **连接错误**
   - 确保 API 服务器正在运行
   - 检查 `.env` 文件中的 URL 配置是否正确

2. **认证错误**
   - 确保测试用户凭据正确
   - 检查 API 认证端点是否正常工作

3. **测试数据依赖**
   - 某些测试可能依赖于特定的数据库状态
   - 如果测试数据不一致，可能需要重置测试数据库

## 持续集成

测试已配置为可以在 CI 环境中运行。CI 脚本会自动:

1. 设置测试环境
2. 运行所有测试
3. 生成报告