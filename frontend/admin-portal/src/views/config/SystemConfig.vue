<template>
  <div class="app-container">
    <el-tabs type="border-card">
      <el-tab-pane label="基础配置">
        <el-form label-width="140px" style="max-width: 600px">
          <el-form-item label="系统名称">
            <el-input v-model="config.base.name" />
          </el-form-item>
          <el-form-item label="SEO 标题">
            <el-input v-model="config.base.title" />
          </el-form-item>
          <el-form-item label="备案号">
            <el-input v-model="config.base.icp" />
          </el-form-item>
          <el-form-item label="维护状态">
            <el-switch v-model="config.base.maintenance" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary">保存基础设置</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <el-tab-pane label="识别参数">
        <el-form label-width="140px" style="max-width: 600px">
          <el-form-item label="置信度阈值">
            <el-slider v-model="config.lpr.confidence" :min="0" :max="1" :step="0.01" />
          </el-form-item>
          <el-form-item label="并发线程数">
            <el-input-number v-model="config.lpr.threads" :min="1" :max="100" />
          </el-form-item>
          <el-form-item label="图像增强级别">
            <el-radio-group v-model="config.lpr.enhance">
              <el-radio label="auto">自动</el-radio>
              <el-radio label="low">低</el-radio>
              <el-radio label="high">极高</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item>
            <el-button type="primary">保存算法参数</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <el-tab-pane label="用户限额">
        <el-table :data="config.quotas" border>
          <el-table-column label="用户类型" prop="type" width="120" />
          <el-table-column label="单日识别限制">
            <template #default="scope">
              <el-input-number v-model="scope.row.dailyLimit" />
            </template>
          </el-table-column>
          <el-table-column label="文件大小限制 (MB)">
            <template #default="scope">
              <el-input-number v-model="scope.row.sizeLimit" />
            </template>
          </el-table-column>
        </el-table>
        <div class="mt-4 text-center">
          <el-button type="primary">保存限额配置</el-button>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
const config = reactive({
  base: { name: 'DarkVision LPR', title: '智能低照度车牌识别系统', icp: '京ICP备12345678号', maintenance: false },
  lpr: { confidence: 0.85, threads: 16, enhance: 'auto' },
  quotas: [
    { type: 'FREE', dailyLimit: 20, sizeLimit: 5 },
    { type: 'VIP', dailyLimit: 500, sizeLimit: 15 },
    { type: 'ENTERPRISE', dailyLimit: 10000, sizeLimit: 100 }
  ]
})
</script>

<style scoped>
.mt-4 { margin-top: 20px; }
.text-center { text-align: center; }
</style>
