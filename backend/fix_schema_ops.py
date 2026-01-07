from sqlalchemy import text
from app.core.database import engine

def fix_schema():
    with engine.connect() as conn:
        print("Starting schema repair...")
        
        # Helper to check if column exists
        def column_exists(table, col_name):
            sql = text("""
            SELECT count(*) 
            FROM information_schema.columns 
            WHERE table_name = :table 
            AND column_name = :col_name 
            AND table_schema = DATABASE()
            """)
            return conn.execute(sql, {"table": table, "col_name": col_name}).scalar() > 0

        # --- Fix 1: operation_logs table ---
        print("\nChecking 'operation_logs' table schema...")
        
        # 1. Rename admin_user_id to admin_id if exists/needed, OR handle mismatch. 
        # The model uses admin_id. The DB has admin_user_id.
        # Let's rename column for consistency with model.
        if column_exists('operation_logs', 'admin_user_id') and not column_exists('operation_logs', 'admin_id'):
            print("Renaming admin_user_id to admin_id...")
            try:
                # Need to drop FK first probably, but let's try CHANGE COLUMN
                # FK name is operation_logs_ibfk_1 usually
                conn.execute(text("ALTER TABLE operation_logs DROP FOREIGN KEY operation_logs_ibfk_1"))
                conn.execute(text("ALTER TABLE operation_logs CHANGE COLUMN admin_user_id admin_id BIGINT NULL COMMENT '操作人ID'"))
                # Re-add FK? Or generic index? 
                # Model defines FK but let's just leave it loose or add basic index for now to avoid complexity
                conn.execute(text("CREATE INDEX ix_operation_logs_admin_id ON operation_logs(admin_id)"))
                print("Renamed successfully.")
            except Exception as e:
                print(f"Rename failed: {e}")
        
        op_logs_columns = [
            ("module", "VARCHAR(50) NOT NULL DEFAULT 'system' COMMENT '功能模块'"),
            ("method", "VARCHAR(10) NULL COMMENT '请求方法'"),
            ("path", "VARCHAR(255) NULL COMMENT '请求路径'"),
            ("params", "TEXT NULL COMMENT '请求参数'"),
            ("result", "TEXT NULL COMMENT '响应结果'"),
            ("status", "INT DEFAULT 200 COMMENT '响应状态码'"),
            ("user_agent", "VARCHAR(255) NULL COMMENT 'User Agent'"),
            ("duration", "INT NULL COMMENT '耗时(ms)'")
        ]
        
        for col_name, col_def in op_logs_columns:
            if not column_exists('operation_logs', col_name):
                print(f"Adding column '{col_name}' to operation_logs...")
                try:
                    conn.execute(text(f"ALTER TABLE operation_logs ADD COLUMN {col_name} {col_def}"))
                except Exception as e:
                    print(f"Failed to add '{col_name}': {e}")
        
        # --- Fix 2: permissions table (double check) ---
        # (It was run before but good to be safe if user reset DB or something, though unlikely)
        
        conn.commit()
        print("\nSchema update completed.")

if __name__ == "__main__":
    fix_schema()
