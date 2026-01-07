from sqlalchemy import text
from app.core.database import engine

def fix_schema():
    with engine.connect() as conn:
        print("Checking 'permissions' table schema...")
        
        # Helper to check if column exists
        def column_exists(col_name):
            sql = text("""
            SELECT count(*) 
            FROM information_schema.columns 
            WHERE table_name = 'permissions' 
            AND column_name = :col_name 
            AND table_schema = DATABASE()
            """)
            return conn.execute(sql, {"col_name": col_name}).scalar() > 0

        columns_to_add = [
            ("description", "VARCHAR(255) NULL COMMENT '描述'"),
            ("type", "VARCHAR(20) DEFAULT 'menu' COMMENT '类型: menu/button/api'"),
            ("parent_id", "BIGINT NULL COMMENT '父权限ID'"),
            ("path", "VARCHAR(255) NULL COMMENT '前端路由路径'"),
            ("component", "VARCHAR(255) NULL COMMENT '前端组件路径'"),
            ("icon", "VARCHAR(50) NULL COMMENT '图标'"),
            ("sort_order", "INT DEFAULT 0 COMMENT '排序'"),
            ("updated_at", "DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
        ]

        for col_name, col_def in columns_to_add:
            if not column_exists(col_name):
                print(f"Adding column '{col_name}'...")
                try:
                    conn.execute(text(f"ALTER TABLE permissions ADD COLUMN {col_name} {col_def}"))
                    print(f"Column '{col_name}' added.")
                except Exception as e:
                    print(f"Failed to add column '{col_name}': {e}")
            else:
                print(f"Column '{col_name}' already exists.")
        
        # Check for FK on parent_id
        # Ideally should add foreign key constraint if it doesn't exist, but skipping for simplicity now unless necessary.
        # Adding simple FK if possible
        try:
             # This might fail if data prevents it, or if it exists. 
             # We can check constraints first but let's try safely.
             # Actually, let's just commit the columns first.
             pass
        except:
            pass

        conn.commit()
        print("Schema update completed.")

if __name__ == "__main__":
    fix_schema()
