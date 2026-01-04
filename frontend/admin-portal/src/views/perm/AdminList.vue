<template>
  <div class="app-container">
    <el-tabs v-model="activeTab">
      <el-tab-pane label="管理员列表" name="list">
        <el-card shadow="never">
          <template #header>
            <el-button type="primary" icon="Plus">新增管理员</el-button>
          </template>
          <el-table :data="adminList" border>
            <el-table-column label="头像" width="80" align="center">
              <template #default="scope">
                <el-avatar :size="40" :src="scope.row.avatar" />
              </template>
            </el-table-column>
            <el-table-column label="账号名" prop="username" width="150" />
            <el-table-column label="所属角色" width="150">
              <template #default="scope">
                <el-tag v-for="role in scope.row.roles" :key="role" size="small" class="mr-1">{{ role }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="手机号" prop="phone" width="120" />
            <el-table-column label="上次登录时间" prop="lastLogin" width="180" />
            <el-table-column label="状态" width="100" align="center">
              <template #default="scope">
                <el-switch :model-value="scope.row.status === 1" />
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200" align="center">
              <template #default>
                <el-button type="primary" link icon="Edit">修改</el-button>
                <el-button type="danger" link icon="Delete">注销</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>

      <el-tab-pane label="敏感操作审计" name="audit">
        <el-card shadow="never">
          <el-table :data="auditLogs" border>
            <el-table-column label="操作人" prop="operator" width="120" />
            <el-table-column label="操作类型" prop="type" width="150" />
            <el-table-column label="操作内容" prop="content" />
            <el-table-column label="操作时间" prop="time" width="180" />
            <el-table-column label="操作IP" prop="ip" width="140" />
            <el-table-column label="状态" width="100" align="center">
              <template #default="scope">
                <el-tag :type="scope.row.success ? 'success' : 'danger'">{{ scope.row.success ? '成功' : '失败' }}</el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
const activeTab = ref('list')

const adminList = ref([
  { username: 'admin', avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=admin', roles: ['超级管理员'], phone: '138****0001', lastLogin: '2026-01-04 20:00:00', status: 1 },
  { username: 'operator01', avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=op1', roles: ['运营人员'], phone: '139****1122', lastLogin: '2026-01-04 18:30:00', status: 1 },
  { username: 'service02', avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=op2', roles: ['客服专员'], phone: '137****3344', lastLogin: '2026-01-04 10:15:00', status: 1 }
])

const auditLogs = ref([
  { operator: 'admin', type: '用户管理', content: '封禁用户 [ID: 10086], 原因: 恶意请求', time: '2026-01-04 21:00:00', ip: '127.0.0.1', success: true },
  { operator: 'operator01', type: '模型管理', content: '切换线上模型 [YOLOv12-X] -> [YOLOv12-PRO]', time: '2026-01-04 20:45:00', ip: '192.168.1.10', success: true },
  { operator: 'admin', type: '系统配置', content: '修改识别并发阈值: 20 -> 50', time: '2026-01-04 19:30:00', ip: '127.0.0.1', success: true }
])
</script>

<style scoped>
.mr-1 { margin-right: 4px; }
</style>
