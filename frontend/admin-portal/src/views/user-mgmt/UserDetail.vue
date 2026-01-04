<template>
  <div class="user-detail">
    <el-skeleton :loading="loading" animated>
      <template #default>
        <el-descriptions title="基本信息" :column="2" border>
          <el-descriptions-item label="用户ID">{{ userInfo?.id }}</el-descriptions-item>
          <el-descriptions-item label="昵称">{{ userInfo?.nickname }}</el-descriptions-item>
          <el-descriptions-item label="手机号">{{ userInfo?.phone }}</el-descriptions-item>
          <el-descriptions-item label="邮箱">{{ userInfo?.email }}</el-descriptions-item>
          <el-descriptions-item label="用户类型">
            <el-tag :type="getUserTypeColor(userInfo?.user_type)">
              {{ getUserTypeLabel(userInfo?.user_type) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusColor(userInfo?.status)">
              {{ getStatusLabel(userInfo?.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="注册时间">{{ userInfo?.created_at }}</el-descriptions-item>
          <el-descriptions-item label="最后登录">{{ userInfo?.last_login_at }}</el-descriptions-item>
        </el-descriptions>

        <el-divider />

        <h3>登录历史</h3>
        <el-table :data="[]" border>
          <el-table-column label="登录时间" prop="login_time" />
          <el-table-column label="IP地址" prop="ip_address" />
          <el-table-column label="设备" prop="device" />
        </el-table>

        <el-divider />

        <div class="actions">
          <el-button type="primary">强制下线</el-button>
          <el-button type="danger">删除用户</el-button>
        </div>
      </template>
    </el-skeleton>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import LprAPI from '@/api/lpr-api'
import type { User } from '@/types/lpr'

const props = defineProps<{ userId: number }>()
const userInfo = ref<User | null>(null)
const loading = ref(false)

async function fetchUserDetail() {
  loading.value = true
  try {
    userInfo.value = await LprAPI.getUserDetail(props.userId)
  } finally {
    loading.value = false
  }
}

function getUserTypeLabel(type?: string) {
  const map: Record<string, string> = { free: '普通', vip: 'VIP', enterprise: '企业' }
  return map[type || ''] || type
}

function getUserTypeColor(type?: string): 'success' | 'warning' | 'danger' | 'info' {
  const map: Record<string, 'success' | 'warning' | 'danger' | 'info'> = { free: 'info', vip: 'warning', enterprise: 'success' }
  return (map[type || ''] || 'info') as 'success' | 'warning' | 'danger' | 'info'
}

function getStatusLabel(status?: string) {
  const map: Record<string, string> = { active: '正常', inactive: '禁用', banned: '封禁' }
  return map[status || ''] || status
}

function getStatusColor(status?: string): 'success' | 'warning' | 'danger' | 'info' {
  const map: Record<string, 'success' | 'warning' | 'danger' | 'info'> = { active: 'success', inactive: 'info', banned: 'danger' }
  return (map[status || ''] || 'info') as 'success' | 'warning' | 'danger' | 'info'
}

onMounted(() => {
  fetchUserDetail()
})
</script>
