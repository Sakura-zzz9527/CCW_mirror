import os
import sys
from dotenv import load_dotenv
import pymysql

# 加载环境变量
load_dotenv()

def test_database_connection():
    """测试数据库连接"""
    print("正在测试数据库连接...")
    
    # 从.env文件获取数据库配置
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = int(os.getenv("DB_PORT", "3306"))
    db_name = os.getenv("DB_NAME")
    
    print(f"数据库配置: {db_host}:{db_port}/{db_name}")
    
    try:
        # 尝试连接数据库
        connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            port=db_port,
            database=db_name
        )
        
        print("✅ 数据库连接成功！")
        
        # 获取数据库版本信息
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"数据库版本: {version[0]}")
            
            # 检查数据库中的表
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            if tables:
                print("\n数据库中的表:")
                for i, table in enumerate(tables, 1):
                    print(f"{i}. {table[0]}")
                    
                    # 检查表结构
                    cursor.execute(f"DESCRIBE {table[0]}")
                    columns = cursor.fetchall()
                    print(f"  表结构 ({len(columns)}列):")
                    for col in columns:
                        print(f"  - {col[0]} ({col[1]})")
                    print()
            else:
                print("数据库中没有表")
        
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ 数据库连接失败: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_database_connection()
    if not success:
        sys.exit(1)  # 连接失败则返回非零退出码