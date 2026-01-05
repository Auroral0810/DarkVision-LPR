#!/bin/bash

# 认证系统测试脚本

BASE_URL="http://localhost:8000/api/v1/auth"

echo "======================================"
echo "DarkVision-LPR 认证系统测试"
echo "======================================"
echo ""

# 1. 测试注册
echo "1. 测试用户注册..."
REGISTER_RESPONSE=$(curl -s -X POST "$BASE_URL/register" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "13900139999",
    "nickname": "测试用户999",
    "password": "test123",
    "email": "test999@example.com"
  }')

echo "注册响应:"
echo "$REGISTER_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$REGISTER_RESPONSE"
echo ""

# 2. 测试密码登录
echo "2. 测试手机号+密码登录..."
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/login/phone" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "13800138000",
    "password": "password"
  }')

echo "登录响应:"
echo "$LOGIN_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$LOGIN_RESPONSE"

# 提取 token
TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['access_token'])" 2>/dev/null)

if [ -n "$TOKEN" ]; then
  echo "✅ 登录成功，Token: ${TOKEN:0:50}..."
else
  echo "❌ 登录失败"
  echo ""
  exit 1
fi
echo ""

# 3. 测试获取用户信息
echo "3. 测试获取当前用户信息..."
USER_INFO=$(curl -s -X GET "$BASE_URL/me" \
  -H "Authorization: Bearer $TOKEN")

echo "用户信息:"
echo "$USER_INFO" | python3 -m json.tool 2>/dev/null || echo "$USER_INFO"
echo ""

# 4. 测试发送验证码
echo "4. 测试发送短信验证码..."
SMS_RESPONSE=$(curl -s -X POST "$BASE_URL/sms/send" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "13800138000",
    "scene": "login"
  }')

echo "验证码响应:"
echo "$SMS_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$SMS_RESPONSE"

# 提取验证码
CODE=$(echo "$SMS_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['code'])" 2>/dev/null)

if [ -n "$CODE" ]; then
  echo "✅ 验证码已发送: $CODE"
else
  echo "❌ 验证码发送失败"
fi
echo ""

# 5. 测试验证码登录
if [ -n "$CODE" ]; then
  echo "5. 测试手机号+验证码登录..."
  SMS_LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/login/phone" \
    -H "Content-Type: application/json" \
    -d "{
      \"phone\": \"13800138000\",
      \"sms_code\": \"$CODE\"
    }")

  echo "验证码登录响应:"
  echo "$SMS_LOGIN_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$SMS_LOGIN_RESPONSE"
  echo ""
fi

# 6. 测试登出
echo "6. 测试登出..."
LOGOUT_RESPONSE=$(curl -s -X POST "$BASE_URL/logout" \
  -H "Authorization: Bearer $TOKEN")

echo "登出响应:"
echo "$LOGOUT_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$LOGOUT_RESPONSE"
echo ""

echo "======================================"
echo "测试完成！"
echo "======================================"

