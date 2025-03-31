import requests
import json
from datetime import datetime
import traceback  # 添加导入

# API基本URL
BASE_URL = "http://localhost:8000"
API_V1 = "/api"

# 测试结果记录
results = {
    "success": [],
    "fail": []
}

def log_test(name, success, response=None, error=None):
    """记录测试结果"""
    status = "success" if success else "fail"
    result = {
        "name": name,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    
    if success:
        if response:
            result["status_code"] = response.status_code
            try:
                result["response"] = response.json()
            except:
                result["response"] = response.text
        results["success"].append(result)
        print(f"✅ 测试通过: {name}")
    else:
        if error:
            error_str = str(error)
            result["error"] = error_str
            print(f"错误详情: {error_str}")
            # 添加堆栈跟踪
            if isinstance(error, Exception):
                traceback_str = traceback.format_exc()
                print(f"异常堆栈: {traceback_str}")
                result["traceback"] = traceback_str
        
        if response:
            result["status_code"] = response.status_code
            try:
                resp_json = response.json()
                result["response"] = resp_json
                print(f"响应状态码: {response.status_code}")
                print(f"响应内容: {resp_json}")
            except Exception as e:
                result["response"] = response.text
                print(f"响应状态码: {response.status_code}")
                print(f"响应内容: {response.text}")
        
        results["fail"].append(result)
        error_msg = error if error else '未知错误'
        print(f"❌ 测试失败: {name} - {error_msg}")

def test_health_check():
    """测试健康检查接口"""
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        log_test("健康检查", response.status_code == 200, response)
        return response
    except Exception as e:
        log_test("健康检查", False, error=e)
        return None

def test_root():
    """测试根路由"""
    try:
        response = requests.get(f"{BASE_URL}/")
        log_test("根路由", response.status_code == 200, response)
        return response
    except Exception as e:
        log_test("根路由", False, error=e)
        return None

def test_create_user():
    """测试创建用户"""
    try:
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
        print(f"POST请求到: {BASE_URL}{API_V1}/users/register")
        response = requests.post(f"{BASE_URL}{API_V1}/users/register", json=data)
        log_test("创建用户", response.status_code in [200, 201], response)
        return response
    except Exception as e:
        log_test("创建用户", False, error=e)
        return None

def test_login():
    """测试用户登录"""
    try:
        # OAuth2 要求使用form-data格式
        data = {
            "username": "testuser",
            "password": "password123"
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        print(f"POST请求到: {BASE_URL}{API_V1}/users/login")
        response = requests.post(
            f"{BASE_URL}{API_V1}/users/login", 
            data=data,  # 使用data而不是json
            headers=headers
        )
        log_test("用户登录", response.status_code == 200, response)
        
        # 如果登录成功，返回token以供后续测试使用
        if response.status_code == 200:
            return response.json().get("access_token")
        return None
    except Exception as e:
        log_test("用户登录", False, error=e)
        return None

def test_get_users(token=None):
    """测试获取用户列表（仅管理员可用）"""
    try:
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        print(f"GET请求到: {BASE_URL}{API_V1}/users/")
        response = requests.get(f"{BASE_URL}{API_V1}/users/", headers=headers)
        log_test("获取用户列表", response.status_code == 200, response)
        return response
    except Exception as e:
        log_test("获取用户列表", False, error=e)
        return None

def test_get_current_user(token=None):
    """测试获取当前用户信息"""
    try:
        if not token:
            log_test("获取当前用户信息", False, error="未提供令牌")
            return None
            
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        print(f"GET请求到: {BASE_URL}{API_V1}/users/me")
        response = requests.get(f"{BASE_URL}{API_V1}/users/me", headers=headers)
        log_test("获取当前用户信息", response.status_code == 200, response)
        return response
    except Exception as e:
        log_test("获取当前用户信息", False, error=e)
        return None

def check_server_connection():
    """检查API服务是否可用"""
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("API服务连接正常")
            return True
        else:
            print(f"API服务返回异常状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"无法连接到API服务: {e}")
        return False

def run_tests():
    """运行所有测试"""
    print("开始API测试...\n")
    
    # 检查服务器连接
    if not check_server_connection():
        print("无法连接到API服务，测试终止")
        return
    
    # 基础测试
    test_root()
    test_health_check()
    
    # 用户相关测试
    try:
        user_response = test_create_user()
        print(f"创建用户请求结果: {user_response}")
        
        token = test_login()
        print(f"登录获取的令牌: {token}")
        
        # 有权限的测试
        if token:
            current_user_response = test_get_current_user(token)
            print(f"获取当前用户信息结果: {current_user_response}")
            
        # 无权限的测试（普通用户无法访问用户列表）
        users_response = test_get_users(token)
        print(f"获取用户列表结果（应当403）: {users_response}")
    except Exception as e:
        print(f"测试过程中发生未捕获的异常: {e}")
        print(traceback.format_exc())
    
    # 打印测试摘要
    print("\n测试摘要:")
    print(f"通过: {len(results['success'])}")
    print(f"失败: {len(results['fail'])}")
    
    if results['fail']:
        print("\n失败的测试:")
        for test in results['fail']:
            print(f"- {test['name']}: {test.get('error', '未知错误')}")
    
    # 保存测试结果
    with open("test_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("\n测试结果已保存到 test_results.json")

if __name__ == "__main__":
    run_tests()