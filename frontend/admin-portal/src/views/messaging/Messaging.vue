<template>
  <div class="app-container">
    <el-tabs v-model="activeTab">
      <el-tab-pane label="消息推送" name="push">
        <el-card shadow="never" style="max-width: 800px">
          <el-form label-width="100px">
            <el-form-item label="推送对象">
              <el-radio-group v-model="msg.target">
                <el-radio label="all">全部用户</el-radio>
                <el-radio label="vip">VIP 用户</el-radio>
                <el-radio label="specific">特定 ID</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="消息内容">
              <el-input type="textarea" :rows="4" v-model="msg.content" placeholder="输入推送内容..." />
            </el-form-item>
            <el-form-item label="推送渠道">
              <el-checkbox-group v-model="msg.channels">
                <el-checkbox label="web">站内信</el-checkbox>
                <el-checkbox label="sms">短信</el-checkbox>
                <el-checkbox label="email">邮件</el-checkbox>
              </el-checkbox-group>
            </el-form-item>
            <el-form-item>
              <el-button type="primary">立即推送</el-button>
              <el-button>定时发送</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>

      <el-tab-pane label="消息记录" name="history">
        <el-table :data="history" border>
          <el-table-column label="推送内容" prop="content" show-overflow-tooltip />
          <el-table-column label="目标" prop="target" width="120" />
          <el-table-column label="渠道" prop="channel" width="100" />
          <el-table-column label="发送时间" prop="time" width="180" />
          <el-table-column label="成功率" width="120">
            <template #default="scope">
              <el-progress :percentage="scope.row.rate" />
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
const activeTab = ref('push')
const msg = reactive({
  target: 'all',
  content: '',
  channels: ['web']
})
const history = ref([
  { content: '系统维护通知：本周日凌晨进行数据库优化', target: '全员', channel: '站内信', time: '2026-01-04 09:00:00', rate: 100 },
  { content: '您的 VIP 账户即将到期，请及时续费', target: '部分', channel: '短信', time: '2026-01-02 18:30:00', rate: 98 }
])
</script>
