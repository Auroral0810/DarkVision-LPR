<template>
  <div class="cache-mgmt-container">
    <el-card class="stats-card" v-loading="loading">
      <template #header>
        <div class="card-header">
          <span><el-icon><Monitor /></el-icon> Redis 状态统计</span>
          <el-button type="primary" link @click="fetchStats">刷新</el-button>
        </div>
      </template>
      
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="stat-item">
            <div class="label">Redis 版本</div>
            <div class="value">{{ stats.redis_version || '-' }}</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-item">
            <div class="label">运行时间</div>
            <div class="value">{{ formatUptime(stats.uptime_in_seconds) }}</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-item">
            <div class="label">已使用内存</div>
            <div class="value">{{ stats.used_memory_human || '-' }}</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-item">
            <div class="label">当前 Key 总数</div>
            <div class="value">{{ stats.keys_count || 0 }}</div>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <el-card class="key-mgmt-card" v-loading="keyLoading">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <span><el-icon><Key /></el-icon> 键名管理</span>
            <el-input
              v-model="searchPattern"
              placeholder="搜索 Key (支持 * 通配符)"
              class="search-input"
              @keyup.enter="searchKeys"
            >
              <template #append>
                <el-button @click="searchKeys"><el-icon><Search /></el-icon></el-button>
              </template>
            </el-input>
          </div>
          <div class="header-right">
            <el-button type="danger" plain @click="handleClearByPrefix">按前缀清理</el-button>
            <el-button type="danger" @click="handleClearAll">清空所有缓存</el-button>
          </div>
        </div>
      </template>

      <el-table :data="keys" style="width: 100%">
        <el-table-column prop="key" label="键名" />
        <el-table-column prop="type" label="类型" width="100">
          <template #default="{ row }">
            <el-tag size="small" :type="getTypeTag(row.type)">{{ row.type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="ttl" label="过期时间(s)" width="120">
          <template #default="{ row }">
            <span :class="{ 'permanent': row.ttl === -1 }">
              {{ row.ttl === -1 ? '永久' : row.ttl }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="size" label="长度/大小" width="120" />
        <el-table-column label="操作" width="100" fixed="right">
          <template #default="{ row }">
            <el-button type="danger" link @click="deleteKey(row.key)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { maintenanceApi } from '@/api/maintenance'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Monitor, Key, Search } from '@element-plus/icons-vue'

const loading = ref(false)
const keyLoading = ref(false)
const stats = ref<any>({})
const keys = ref<any[]>([])
const searchPattern = ref('*')

const fetchStats = async () => {
  loading.value = true
  try {
    const res = await maintenanceApi.getCacheStats()
    stats.value = res
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const searchKeys = async () => {
  keyLoading.value = true
  try {
    const res = await maintenanceApi.searchCacheKeys({ pattern: searchPattern.value })
    keys.value = res
  } catch (error) {
    console.error(error)
  } finally {
    keyLoading.value = false
  }
}

const deleteKey = async (key: string) => {
  try {
    await ElMessageBox.confirm(`确定删除 Key: ${key} 吗？`, '提示', { type: 'warning' })
    await maintenanceApi.clearCache({ keys: [key] })
    ElMessage.success('删除成功')
    searchKeys()
    fetchStats()
  } catch (error) {
    if (error !== 'cancel') console.error(error)
  }
}

const handleClearByPrefix = async () => {
  try {
    const { value: prefix } = await ElMessageBox.prompt('请输入要清理的 Key 前缀', '按前缀清理', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      inputPlaceholder: '例如: recognition_cache_'
    })
    
    if (!prefix) return
    
    await maintenanceApi.clearCache({ prefix })
    ElMessage.success('清理成功')
    searchKeys()
    fetchStats()
  } catch (error) {
    if (error !== 'cancel') console.error(error)
  }
}

const handleClearAll = async () => {
  try {
    await ElMessageBox.confirm('确定清空所有 Redis 缓存吗？此操作可能会对系统性能产生短暂影响。', '警告', {
      type: 'error',
      confirmButtonClass: 'el-button--danger'
    })
    
    await maintenanceApi.clearCache({})
    ElMessage.success('已清空所有缓存')
    searchKeys()
    fetchStats()
  } catch (error) {
    if (error !== 'cancel') console.error(error)
  }
}

const formatUptime = (seconds: number) => {
  if (!seconds) return '-'
  const d = Math.floor(seconds / (3600 * 24))
  const h = Math.floor((seconds % (3600 * 24)) / 3600)
  const m = Math.floor((seconds % 3600) / 60)
  return `${d}天 ${h}时 ${m}分`
}

const getTypeTag = (type: string) => {
  const map: any = {
    string: '',
    hash: 'success',
    list: 'warning',
    set: 'info',
    zset: 'danger'
  }
  return map[type] || ''
}

onMounted(() => {
  fetchStats()
  searchKeys()
})
</script>

<style scoped>
.cache-mgmt-container {
  padding: 20px;
}

.stats-card {
  margin-bottom: 20px;
}

.stat-item {
  text-align: center;
  padding: 10px;
}

.stat-item .label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.stat-item .value {
  font-size: 20px;
  font-weight: bold;
  color: #303133;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.search-input {
  width: 300px;
}

.permanent {
  color: #909399;
  font-style: italic;
}
</style>
