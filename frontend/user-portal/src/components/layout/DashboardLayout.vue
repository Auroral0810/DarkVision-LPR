<template>
  <div class="dashboard-layout">
    <el-container class="layout-container">
      <el-aside width="240px" class="aside">
        <div class="logo">
          <div class="logo-icon">DV</div>
          <h2>DarkVision</h2>
          <span class="role-badge" :class="userStore.userInfo.role.toLowerCase()">
            {{ roleText }}
          </span>
        </div>
        
        <el-menu
          :default-active="activeMenu"
          class="el-menu-vertical"
          router
          :collapse="isCollapse"
          background-color="#0f172a"
          text-color="#94a3b8"
          active-text-color="#ffffff"
        >
          <div class="menu-group-title">控制台</div>
          <el-menu-item index="/dashboard/overview">
            <el-icon><Odometer /></el-icon>
            <span>概览</span>
          </el-menu-item>
          
          <div class="menu-group-title">识别服务</div>
          <el-menu-item index="/dashboard/recognition">
            <el-icon><Camera /></el-icon>
            <span>开始识别</span>
          </el-menu-item>
          
          <el-menu-item index="/dashboard/history">
            <el-icon><List /></el-icon>
            <span>历史记录</span>
          </el-menu-item>
          
          <el-menu-item index="/dashboard/analysis">
            <el-icon><TrendCharts /></el-icon>
            <span>数据分析</span>
            <el-tag v-if="!userStore.isVIP" size="small" type="danger" effect="dark" class="menu-tag">VIP</el-tag>
          </el-menu-item>
          
          <div class="menu-group-title">账户</div>
          <el-menu-item index="/dashboard/settings">
            <el-icon><Setting /></el-icon>
            <span>账户设置</span>
          </el-menu-item>
        </el-menu>

        <div class="user-profile">
          <div class="user-info">
            <el-avatar :size="36" :src="userStore.userInfo.avatar" />
            <div class="user-details">
              <span class="username">{{ userStore.userInfo.nickname }}</span>
              <span class="email">{{ userStore.userInfo.email }}</span>
            </div>
          </div>
          <el-dropdown trigger="click" @command="handleProfileCommand">
            <el-button link class="logout-btn">
              <el-icon><MoreFilled /></el-icon>
            </el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="logout" class="danger-item">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-aside>
      
      <el-container class="main-container">
        <el-header class="header">
          <div class="header-left">
            <h3>{{ currentRouteTitle }}</h3>
          </div>
          <div class="header-right">
            <el-button v-if="!userStore.isVIP" type="primary" size="default" round class="upgrade-btn" @click="handleUpgrade">
              <el-icon><Trophy /></el-icon>
              升级 VIP
            </el-button>
            <div class="role-switcher">
              <span class="label">当前演示角色:</span>
              <el-dropdown @command="handleRoleSwitch">
                <span class="el-dropdown-link">
                  {{ userStore.userInfo.role }}<el-icon class="el-icon--right"><ArrowDown /></el-icon>
                </span>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="FREE">FREE (普通用户)</el-dropdown-item>
                    <el-dropdown-item command="VIP">VIP (高级用户)</el-dropdown-item>
                    <el-dropdown-item command="COMPANY">COMPANY (企业用户)</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </div>
        </el-header>
        
        <el-main class="main">
          <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { Odometer, Camera, List, TrendCharts, Setting, ArrowDown, MoreFilled, Trophy } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const isCollapse = ref(false)

const activeMenu = computed(() => route.path)
const currentRouteTitle = computed(() => route.meta.title || 'Dashboard')

const roleText = computed(() => {
  switch (userStore.userInfo.role) {
    case 'FREE': return '免费版'
    case 'VIP': return '专业版'
    case 'COMPANY': return '企业版'
    default: return ''
  }
})

const handleProfileCommand = (command: string) => {
  if (command === 'logout') {
    userStore.logout()
    router.push('/login')
    ElMessage.success('已退出登录')
  }
}

const handleRoleSwitch = (command: string) => {
  // @ts-ignore
  userStore.switchRole(command)
  ElMessage.success(`已切换至 ${command} 角色`)
}

const handleUpgrade = () => {
  // TODO: 跳转到升级页面
  ElMessage.info('跳转至升级页面')
}
</script>

<style scoped lang="scss">
.dashboard-layout {
  height: 100vh;
  width: 100vw;
  background-color: #f1f5f9;
}

.layout-container {
  height: 100%;
}

.aside {
  background-color: #0f172a;
  color: white;
  display: flex;
  flex-direction: column;
  transition: width 0.3s;
  
  .logo {
    height: 80px;
    display: flex;
    align-items: center;
    padding: 0 24px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    
    .logo-icon {
      width: 32px;
      height: 32px;
      background: #2563eb;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      margin-right: 12px;
    }
    
    h2 {
      margin: 0;
      font-size: 18px;
      font-weight: 600;
      color: white;
      flex: 1;
    }
    
    .role-badge {
      font-size: 10px;
      padding: 2px 6px;
      border-radius: 4px;
      background: rgba(255, 255, 255, 0.1);
      color: #94a3b8;
      
      &.vip { color: #f59e0b; background: rgba(245, 158, 11, 0.1); }
      &.company { color: #3b82f6; background: rgba(59, 130, 246, 0.1); }
    }
  }
}

.el-menu-vertical {
  border-right: none;
  flex: 1;
  padding: 24px 16px;
  
  .menu-group-title {
    padding: 0 12px;
    margin-bottom: 8px;
    margin-top: 24px;
    font-size: 12px;
    color: #64748b;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    
    &:first-child {
      margin-top: 0;
    }
  }
  
  :deep(.el-menu-item) {
    height: 44px;
    margin-bottom: 4px;
    border-radius: 8px;
    color: #94a3b8;
    
    &:hover {
      background-color: rgba(255, 255, 255, 0.05);
      color: white;
    }
    
    &.is-active {
      background-color: #2563eb;
      color: white;
      font-weight: 500;
      
      &:hover {
        background-color: #1d4ed8;
      }
    }
    
    .el-icon {
      font-size: 18px;
    }
    
    .menu-tag {
      margin-left: auto;
      transform: scale(0.8);
    }
  }
}

.user-profile {
  padding: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
  
  .user-info {
    display: flex;
    align-items: center;
    gap: 12px;
    overflow: hidden;
    
    .user-details {
      display: flex;
      flex-direction: column;
      overflow: hidden;
      
      .username {
        font-size: 14px;
        font-weight: 600;
        color: white;
      }
      
      .email {
        font-size: 12px;
        color: #64748b;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }
    }
  }
  
  .logout-btn {
    color: #64748b;
    &:hover { color: white; }
  }
}

.main-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

.header {
  background: white;
  height: 72px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  
  h3 {
    margin: 0;
    font-size: 20px;
    font-weight: 700;
    color: #1e293b;
  }
  
  .header-right {
    display: flex;
    align-items: center;
    gap: 24px;
    
    .upgrade-btn {
      font-weight: 600;
      background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
      border: none;
      
      &:hover {
        opacity: 0.9;
      }
    }
    
    .role-switcher {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 14px;
      
      .label {
        color: #64748b;
      }
      
      .el-dropdown-link {
        cursor: pointer;
        color: #1e293b;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 4px;
      }
    }
  }
}

.main {
  padding: 32px;
  overflow-y: auto;
  flex: 1;
  background-color: #f1f5f9;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.danger-item {
  color: #ef4444;
  &:hover {
    color: #dc2626;
    background-color: #fef2f2;
  }
}
</style>