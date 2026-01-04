<template>
  <div class="dashboard-layout">
    <el-container class="layout-container">
      <el-aside width="240px" class="aside">
        <div class="logo">
          <h2>DarkVision</h2>
          <span class="role-badge" :class="userStore.userInfo.role.toLowerCase()">
            {{ userStore.userInfo.role }}
          </span>
        </div>
        
        <el-menu
          :default-active="activeMenu"
          class="el-menu-vertical"
          router
          :collapse="isCollapse"
        >
          <el-menu-item index="/dashboard/overview">
            <el-icon><Odometer /></el-icon>
            <span>概览</span>
          </el-menu-item>
          
          <el-menu-item index="/dashboard/recognition">
            <el-icon><Camera /></el-icon>
            <span>开始识别</span>
          </el-menu-item>
          
          <el-menu-item index="/dashboard/history">
            <el-icon><List /></el-icon>
            <span>历史记录</span>
          </el-menu-item>
          
          <el-menu-item v-if="userStore.isVIP" index="/dashboard/analysis">
            <el-icon><TrendCharts /></el-icon>
            <span>数据分析</span>
            <el-tag size="small" type="warning" effect="dark" class="menu-tag">VIP</el-tag>
          </el-menu-item>
          
          <el-menu-item index="/dashboard/settings">
            <el-icon><Setting /></el-icon>
            <span>账户设置</span>
          </el-menu-item>
        </el-menu>

        <div class="user-profile">
          <div class="user-info">
            <el-avatar :size="32" :src="userStore.userInfo.avatar" />
            <span class="username">{{ userStore.userInfo.nickname }}</span>
          </div>
          <el-button type="text" @click="handleLogout">退出</el-button>
        </div>
      </el-aside>
      
      <el-container>
        <el-header class="header">
          <div class="header-left">
            <h3>{{ currentRouteTitle }}</h3>
          </div>
          <div class="header-right">
            <el-button v-if="!userStore.isVIP" type="primary" size="small" round>
              升级 VIP
            </el-button>
            <el-dropdown @command="handleCommand">
              <span class="el-dropdown-link">
                切换角色演示<el-icon class="el-icon--right"><arrow-down /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="FREE">普通用户</el-dropdown-item>
                  <el-dropdown-item command="VIP">VIP用户</el-dropdown-item>
                  <el-dropdown-item command="COMPANY">企业用户</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
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
import { Odometer, Camera, List, TrendCharts, Setting, ArrowDown } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const isCollapse = ref(false)

const activeMenu = computed(() => route.path)
const currentRouteTitle = computed(() => route.meta.title || 'Dashboard')

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}

const handleCommand = (command: string) => {
  // @ts-ignore
  userStore.switchRole(command)
}
</script>

<style scoped lang="scss">
.dashboard-layout {
  height: 100vh;
  width: 100vw;
  background-color: #f8fafc;
}

.layout-container {
  height: 100%;
}

.aside {
  background-color: white;
  border-right: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  
  .logo {
    height: 64px;
    display: flex;
    align-items: center;
    padding: 0 20px;
    border-bottom: 1px solid #eff6ff;
    
    h2 {
      margin: 0;
      font-size: 18px;
      color: #0f172a;
      flex: 1;
    }
    
    .role-badge {
      font-size: 10px;
      padding: 2px 6px;
      border-radius: 4px;
      font-weight: 600;
      
      &.free {
        background: #f1f5f9;
        color: #64748b;
      }
      &.vip {
        background: #fff7ed;
        color: #ea580c;
      }
      &.company {
        background: #eff6ff;
        color: #2563eb;
      }
    }
  }
}

.el-menu-vertical {
  border-right: none;
  flex: 1;
  padding: 16px 0;
  
  :deep(.el-menu-item) {
    height: 48px;
    margin: 4px 12px;
    border-radius: 8px;
    
    &.is-active {
      background-color: #eff6ff;
      color: #2563eb;
      font-weight: 500;
    }
    
    .menu-tag {
      margin-left: auto;
      transform: scale(0.8);
    }
  }
}

.user-profile {
  padding: 16px;
  border-top: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  
  .user-info {
    display: flex;
    align-items: center;
    gap: 8px;
    
    .username {
      font-size: 14px;
      font-weight: 500;
      color: #334155;
    }
  }
}

.header {
  background: white;
  height: 64px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  
  h3 {
    margin: 0;
    font-size: 18px;
    font-weight: 600;
    color: #1e293b;
  }
}

.main {
  padding: 32px;
  overflow-y: auto;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
