from sqlalchemy import text
from app.core.database import engine

def fix_schema():
    with engine.connect() as conn:
        print("Checking 'announcements' table...")
        
        # Check if table exists
        check_sql = text("SHOW TABLES LIKE 'announcements'")
        result = conn.execute(check_sql).scalar()
        
        if not result:
            print("Table 'announcements' missing. Creating...")
            create_sql = text("""
            CREATE TABLE `announcements` (
              `id` int NOT NULL AUTO_INCREMENT,
              `title` varchar(200) NOT NULL,
              `content` text NOT NULL,
              `display_position` varchar(50) NOT NULL,
              `start_time` datetime DEFAULT NULL,
              `end_time` datetime DEFAULT NULL,
              `is_enabled` tinyint(1) DEFAULT '1',
              `created_by` bigint NOT NULL,
              `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
              PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='系统公告';
            """)
            conn.execute(create_sql)
            print("Table created successfully.")
        else:
            print("Table 'announcements' already exists.")

if __name__ == "__main__":
    fix_schema()
