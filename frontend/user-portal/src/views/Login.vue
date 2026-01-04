<template>
  <div class="login-page">
    <div class="login-card">
      <h2>DarkVision 登录</h2>
      <p>选择角色进入演示系统</p>
      
      <div class="role-buttons">
        <el-button type="info" class="role-btn" @click="handleLogin('FREE')">
          <div class="btn-content">
            <strong>普通用户</strong>
            <span>免费体验基础功能</span>
          </div>
        </el-button>
        
        <el-button type="warning" class="role-btn" @click="handleLogin('VIP')">
          <div class="btn-content">
            <strong>VIP 用户</strong>
            <span>批量处理与高级分析</span>
          </div>
        </el-button>
        
        <el-button type="primary" class="role-btn" @click="handleLogin('COMPANY')">
          <div class="btn-content">
            <strong>企业用户</strong>
            <span>无限用量与API支持</span>
          </div>
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useUserStore, UserRole } from '@/store/user'

const router = useRouter()
const userStore = useUserStore()

const handleLogin = (role: UserRole) => {
  userStore.login(role)
  router.push('/dashboard')
}
</script>

<style scoped lang="scss">
.login-page {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f1f5f9;
}

.login-card {
  background: white;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  text-align: center;
  
  h2 {
    margin: 0 0 8px;
    color: #0f172a;
  }
  
  p {
    color: #64748b;
    margin-bottom: 32px;
  }
}

.role-buttons {
  display: flex;
  flex-direction: column;
  gap: 16px;
  
  .role-btn {
    height: auto;
    padding: 16px;
    justify-content: flex-start;
    
    .btn-content {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      gap: 4px;
      
      strong {
        font-size: 16px;
      }
      
      span {
        font-size: 12px;
        opacity: 0.9;
        font-weight: normal;
      }
    }
  }
}
</style>
