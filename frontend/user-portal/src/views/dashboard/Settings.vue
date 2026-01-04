<template>
  <div class="settings-view">
    <div class="settings-card">
      <h3>基本信息</h3>
      <el-form label-position="top">
        <el-form-item label="昵称">
          <el-input v-model="userStore.userInfo.nickname" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="userStore.userInfo.email" disabled />
        </el-form-item>
        <el-form-item>
          <el-button type="primary">保存修改</el-button>
        </el-form-item>
      </el-form>
    </div>
    
    <div class="settings-card">
      <h3>安全设置</h3>
      <div class="setting-item">
        <div class="setting-info">
          <h4>登录密码</h4>
          <p>建议定期修改密码以保护账户安全</p>
        </div>
        <el-button link type="primary">修改</el-button>
      </div>
      
      <div class="setting-item">
        <div class="setting-info">
          <h4>实名认证</h4>
          <p class="verified" v-if="userStore.isVIP">已认证</p>
          <p v-else>未认证</p>
        </div>
        <el-button link type="primary" v-if="!userStore.isVIP">去认证</el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useUserStore } from '@/store/user'

const userStore = useUserStore()
</script>

<style scoped lang="scss">
.settings-view {
  max-width: 800px;
}

.settings-card {
  background: white;
  padding: 32px;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  margin-bottom: 24px;
  
  h3 {
    margin: 0 0 24px;
    font-size: 18px;
    color: #0f172a;
    border-bottom: 1px solid #f1f5f9;
    padding-bottom: 16px;
  }
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 0;
  border-bottom: 1px solid #f8fafc;
  
  &:last-child {
    border-bottom: none;
  }
  
  .setting-info {
    h4 {
      margin: 0 0 4px;
      font-size: 14px;
      color: #334155;
    }
    
    p {
      margin: 0;
      font-size: 13px;
      color: #94a3b8;
      
      &.verified {
        color: #10b981;
      }
    }
  }
}
</style>
