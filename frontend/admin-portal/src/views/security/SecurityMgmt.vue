<template>
  <div class="app-container">
    <el-tabs type="border-card">
      <el-tab-pane label="访问控制">
        <el-form label-width="120px">
          <el-form-item label="IP 黑名单">
            <el-input type="textarea" :rows="5" v-model="security.blacklist" placeholder="每行一个 IP 地址" />
            <div class="help-text">被列入黑名单的 IP 将无法访问 API 接口</div>
          </el-form-item>
          <el-form-item label="登录上限">
            <el-input-number v-model="security.loginLimit" />
            <span class="ml-2">次失败后锁定账户 (30分钟)</span>
          </el-form-item>
          <el-form-item>
            <el-button type="primary">应用策略</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <el-tab-pane label="安全审计">
        <el-table :data="securityLogs" border>
          <el-table-column label="事件" prop="event" width="150" />
          <el-table-column label="详情" prop="details" />
          <el-table-column label="IP" prop="ip" width="140" />
          <el-table-column label="时间" prop="time" width="180" />
          <el-table-column label="级别" width="100" align="center">
            <template #default="scope">
              <el-tag :type="scope.row.level === 'High' ? 'danger' : 'warning'">{{ scope.row.level }}</el-tag>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
const security = reactive({
  blacklist: '1.2.3.4\n11.22.33.44',
  loginLimit: 5
})
const securityLogs = ref([
  { event: '敏感操作告警', details: '管理员 admin 修改了系统核心识置信度', ip: '127.0.0.1', time: '2026-01-04 21:00:00', level: 'High' },
  { event: '异地登录', details: '用户 user_123 从上海登录 (常用地: 北京)', ip: '202.10.22.33', time: '2026-01-04 18:00:00', level: 'Medium' }
])
</script>

<style scoped>
.help-text { font-size: 12px; color: #999; margin-top: 4px; }
.ml-2 { margin-left: 8px; }
</style>
