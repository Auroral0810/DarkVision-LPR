<template>
  <div class="app-container">
    <el-card>
      <el-table :data="modelList" v-loading="loading">
        <el-table-column label="模型ID" prop="id" width="80" />
        <el-table-column label="模型名称" prop="name" min-width="200" />
        <el-table-column label="版本" prop="version" width="150" />
        <el-table-column label="准确率" width="120">
          <template #default="scope">
            <span style="font-weight: 600">{{ scope.row.accuracy }}%</span>
          </template>
        </el-table-column>
        <el-table-column label="推理速度" width="120">
          <template #default="scope">{{ scope.row.inference_time_ms }}ms</template>
        </el-table-column>
        <el-table-column label="GPU占用" width="120">
          <template #default="scope">{{ scope.row.gpu_memory_mb }}MB</template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="scope">
            <el-tag v-if="scope.row.is_active" type="success">使用中</el-tag>
            <el-tag v-else type="info">待机</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="创建时间" prop="created_at" width="160" />
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button
              v-if="!scope.row.is_active"
              type="primary"
              link
              @click="handleActivate(scope.row.id)"
            >
              切换使用
            </el-button>
            <el-button type="info" link>查看详情</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-card title="模型性能对比" class="mt-4">
      <div style="height: 400px; display: flex; align-items: center; justify-content: center; color: #999;">
        图表占位 - 模型性能对比雷达图/柱状图
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import LprAPI from '@/api/lpr-api'

const modelList = ref([])
const loading = ref(false)

async function fetchModelList() {
  loading.value = true
  try {
    modelList.value = await LprAPI.getModelList()
  } finally {
    loading.value = false
  }
}

async function handleActivate(id: number) {
  ElMessageBox.confirm('切换模型会导致服务短暂中断，是否继续？', '确认切换', {
    type: 'warning'
  })
    .then(async () => {
      try {
        await LprAPI.switchModel(id)
        ElMessage.success('模型切换成功')
        fetchModelList()
      } catch (error) {
        ElMessage.error('切换失败')
      }
    })
    .catch(() => {})
}

onMounted(() => {
  fetchModelList()
})
</script>

<style scoped>
.mt-4 {
  margin-top: 20px;
}
</style>
