<template>
  <div class="app-container">
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card header="缓存管理 (Redis)">
          <div class="mb-4">
            <el-statistic title="缓存 Key 总数" :value="12450" />
          </div>
          <el-button type="warning" icon="Delete">清除系统配置缓存</el-button>
          <el-button type="danger" icon="Delete">清除所有用户 Session</el-button>
          <div class="mt-4"><el-link type="info">查看慢查询 Key 记录</el-link></div>
        </el-card>

        <el-card header="版本管理" class="mt-4">
          <el-descriptions :column="1" border>
            <el-descriptions-item label="当前版本">v1.2.4 (stable)</el-descriptions-item>
            <el-descriptions-item label="最新版本"><el-tag type="info">v1.2.5 (available)</el-tag></el-descriptions-item>
          </el-descriptions>
          <div class="mt-4">
            <el-button type="primary">检查更新</el-button>
            <el-button type="success" plain>推送更新公告</el-button>
          </div>
        </el-card>
      </el-col>

      <el-col :span="12">
        <el-card header="数据备份 & 恢复">
          <template #header>
            <div class="card-header">
              <span>数据库备份列表</span>
              <el-button type="primary" size="small" icon="Plus">立即备份</el-button>
            </div>
          </template>
          <el-table :data="backups" border size="small">
            <el-table-column label="备份名称" prop="name" />
            <el-table-column label="大小" prop="size" width="100" />
            <el-table-column label="时间" prop="time" width="150" />
            <el-table-column label="操作" width="120">
              <template #default>
                <el-button type="primary" link>恢复</el-button>
                <el-button type="danger" link>删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          <div class="mt-2 text-right">
            <el-switch v-model="autoBackup" active-text="开启每日自动备份" />
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
const autoBackup = ref(true)
const backups = ref([
  { name: 'db_full_20260104.sql.gz', size: '245MB', time: '2026-01-04 03:00' },
  { name: 'db_full_20260103.sql.gz', size: '242MB', time: '2026-01-03 03:00' },
  { name: 'db_full_20260102.sql.gz', size: '238MB', time: '2026-01-02 03:00' }
])
</script>

<style scoped>
.mb-4 { margin-bottom: 20px; }
.mt-4 { margin-top: 20px; }
.mt-2 { margin-top: 8px; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
.text-right { text-align: right; }
</style>
