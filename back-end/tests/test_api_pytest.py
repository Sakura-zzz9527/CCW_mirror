"""
CCW Mirror API测试 - Pytest版本
使用pytest框架测试API端点
"""
# pylint: disable=import-error
import sys
sys.path.append("../env/Lib/site-packages")
import pytest  # type: ignore
import requests  # type: ignore
import json
import os

# 测试根路由
def test_root(api_client):
    """测试API根路由是否可访问"""
    response = requests.get(api_client.get_url("/"))
    assert response.status_code == 200
    api_client.log_result("根路由", response.status_code == 200, response)

# 测试健康检查
def test_health(api_client):
    """测试健康检查端点"""
    response = requests.get(api_client.get_url("/api/health"))  # 更新为正确的端点路径
    assert response.status_code == 200
    health_data = response.json()
    assert "status" in health_data
    assert health_data["status"] == "healthy"
    api_client.log_result("健康检查", response.status_code == 200, response)

# 测试用户登录
def test_login(api_client):
    """测试用户登录功能"""
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "username": os.getenv("TEST_USER", "testuser"),
        "password": os.getenv("TEST_PASSWORD", "password123")
    }
    
    response = requests.post(
        api_client.get_url("/api/users/login"), 
        data=data,
        headers=headers
    )
    
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    
    # 保存令牌用于后续测试
    api_client.set_token(token_data["access_token"])
    
    api_client.log_result("用户登录", response.status_code == 200, response)

# 测试获取当前用户信息
def test_get_current_user(api_client):
    """测试获取当前用户信息"""
    # 确保已登录
    if not api_client.token:
        test_login(api_client)
    
    headers = api_client.get_headers()
    response = requests.get(api_client.get_url("/api/users/me"), headers=headers)
    
    assert response.status_code == 200
    user_data = response.json()
    assert "username" in user_data
    
    api_client.log_result("获取当前用户信息", response.status_code == 200, response)

# 完成后保存测试结果
@pytest.fixture(scope="session", autouse=True)
def save_test_results(api_client):
    """测试完成后保存结果"""
    yield
    api_client.save_results()

if __name__ == "__main__":
    print("请使用pytest运行此测试文件")
    print("示例: pytest -xvs test_api_pytest.py")