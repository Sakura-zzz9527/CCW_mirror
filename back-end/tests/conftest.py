"""
CCW Mirror测试配置文件
包含共享的测试夹具和实用函数
"""
# pylint: disable=import-error
# type: ignore

import sys
sys.path.append("../env/Lib/site-packages")
import os
import json
import pytest  # type: ignore
import datetime
from dotenv import load_dotenv

# 加载环境配置
load_dotenv()

# 测试配置
BASE_URL = os.getenv("TEST_BASE_URL", "http://localhost:8000")
API_PATH = os.getenv("API_PATH", "")  # 默认为空，直接访问根路径
TEST_USER = os.getenv("TEST_USER", "testuser")
TEST_PASSWORD = os.getenv("TEST_PASSWORD", "password123")
TEST_EMAIL = os.getenv("TEST_EMAIL", "test@example.com")

# 日志文件
RESULTS_FILE = os.path.join(os.path.dirname(__file__), "test_results.json")


@pytest.fixture(scope="session")
def api_client():
    """
    创建一个API客户端夹具，可用于各个测试
    """
    class APIClient:
        def __init__(self):
            self.base_url = BASE_URL
            self.api_path = API_PATH
            self.token = None
            self.results = {"success": [], "fail": []}
        
        def get_url(self, endpoint):
            """获取完整的API URL"""
            return f"{self.base_url}{self.api_path}{endpoint}"
        
        def set_token(self, token):
            """设置认证令牌"""
            self.token = token
        
        def get_headers(self):
            """获取请求头"""
            headers = {"Content-Type": "application/json"}
            if self.token:
                headers["Authorization"] = f"Bearer {self.token}"
            return headers
        
        def log_result(self, name, success, response=None, error=None, note=None):
            """记录测试结果"""
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            result = {
                "name": name,
                "time": now
            }
            
            if response:
                result["status_code"] = response.status_code
                try:
                    result["response"] = response.json()
                except:
                    result["response"] = response.text
            
            if error:
                result["error"] = str(error)
            
            if note:
                result["note"] = note
            
            if success:
                self.results["success"].append(result)
            else:
                self.results["fail"].append(result)
            
            return success
        
        def save_results(self):
            """保存测试结果到文件"""
            with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2)
    
    return APIClient()


def pytest_sessionfinish(session, exitstatus):
    """测试会话结束时保存测试结果"""
    # 这里可以添加更多的测试结果处理逻辑
    pass