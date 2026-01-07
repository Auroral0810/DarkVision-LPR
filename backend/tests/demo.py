import bcrypt

# 1. 明文密码转换为字节串（BCrypt 要求输入为 bytes 类型）
password = b"123456"

# 2. 生成随机盐值，成本因子设为 10（行业常用值，越高越安全但计算越慢）
salt = bcrypt.gensalt(rounds=10)  # rounds 范围 4-31，推荐 10-12

# 3. 生成 BCrypt 哈希（自动融合盐值和密码）
hashed_password = bcrypt.hashpw(password, salt)

# 4. 输出结果
print("原始密码：", password.decode("utf-8"))
print("BCrypt 哈希：", hashed_password.decode("utf-8"))

# 5. 验证哈希是否匹配（验证环节，可选）
is_match = bcrypt.checkpw(password, hashed_password)
print("密码验证结果：", "匹配" if is_match else "不匹配")