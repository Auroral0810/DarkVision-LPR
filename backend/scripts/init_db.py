import sys
from pathlib import Path

# 将 backend 目录添加到 Python 路径
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from app.core.database import Base, engine
from app.models.user import User, UserProfile, UserMembership

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("数据库表创建完成！")