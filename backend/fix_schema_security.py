import pymysql
import sys
import os

# 把上一层目录加入 path 以便导入 app.config
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.config import settings

def fix_schema():
    connection = pymysql.connect(
        host=settings.MYSQL_HOST,
        port=settings.MYSQL_PORT,
        user=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD,
        database=settings.MYSQL_DATABASE,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    try:
        with connection.cursor() as cursor:
            print("Creating system_ip_rules table...")
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS `system_ip_rules` (
              `id` bigint NOT NULL AUTO_INCREMENT,
              `ip_address` varchar(45) NOT NULL,
              `type` enum('allow','deny') NOT NULL DEFAULT 'deny',
              `remark` varchar(255) DEFAULT NULL,
              `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
              `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
              PRIMARY KEY (`id`),
              UNIQUE KEY `uniq_ip` (`ip_address`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='系统IP规则表(黑白名单)';
            """
            cursor.execute(create_table_sql)
            
            # 同时也检查 operation_logs 是否有 module 字段（之前脚本改过，这里双重确认）
            cursor.execute("DESCRIBE operation_logs")
            columns = [row['Field'] for row in cursor.fetchall()]
            if 'module' not in columns:
                print("Adding missing 'module' column to operation_logs...")
                cursor.execute("ALTER TABLE operation_logs ADD COLUMN module varchar(50) NOT NULL AFTER admin_id")
            
        connection.commit()
        print("Schema fix completed successfully.")
    finally:
        connection.close()

if __name__ == "__main__":
    fix_schema()
