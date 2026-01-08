<template>
  <div class="app-container">
    <el-card class="filter-container" shadow="hover">
      <el-form :inline="true" :model="queryParams" ref="queryFormRef">
        <el-form-item label="车牌号" prop="license_plate">
          <el-input
            v-model="queryParams.license_plate"
            placeholder="请输入车牌号"
            clearable
            style="width: 200px"
            @keyup.enter="handleQuery"
          />
        </el-form-item>
        <el-form-item label="车牌类型" prop="plate_type">
          <el-select v-model="queryParams.plate_type" placeholder="请选择" clearable style="width: 150px">
            <el-option label="蓝牌" value="blue" />
            <el-option label="黄牌" value="yellow" />
            <el-option label="绿牌" value="green" />
            <el-option label="白牌" value="white" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="用户ID" prop="user_id">
          <el-input v-model="queryParams.user_id" placeholder="用户ID" clearable style="width: 150px" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
          <el-button icon="Refresh" @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-container" shadow="hover" style="margin-top: 20px">
      <el-table v-loading="loading" :data="recordList">
        <el-table-column prop="id" label="ID" width="80" align="center" sortable />
        <el-table-column label="图片" width="120" align="center">
          <template #default="scope">
            <el-image
              style="width: 80px; height: 60px"
              :src="scope.row.original_image_url"
              :preview-src-list="[scope.row.original_image_url]"
              fit="cover"
              preview-teleported
            />
          </template>
        </el-table-column>
        <el-table-column prop="license_plate" label="车牌号" width="120" align="center" sortable>
          <template #default="scope">
            <el-tag :type="getPlateTypeTag(scope.row.plate_type)">{{ scope.row.license_plate }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="confidence" label="置信度" width="100" align="center" sortable>
          <template #default="scope">
            {{ (scope.row.confidence * 100).toFixed(2) }}%
          </template>
        </el-table-column>
        <el-table-column prop="processing_time" label="耗时(ms)" width="100" align="center" sortable />
        <el-table-column prop="user_id" label="用户ID" width="100" align="center" sortable />
        <el-table-column prop="model_version" label="模型版本" width="120" align="center" sortable />
        <el-table-column prop="created_at" label="识别时间" width="180" align="center" sortable>
          <template #default="scope">
            {{ formatTime(scope.row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center" fixed="right">
          <template #default="scope">
            <el-button
              type="primary"
              link
              icon="View"
              @click="handleDetail(scope.row)"
            >详情</el-button>
            <el-button
              type="danger"
              link
              icon="Delete"
              @click="handleDelete(scope.row)"
            >删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination
          v-show="total > 0"
          :total="total"
          v-model:current-page="queryParams.page"
          v-model:page-size="queryParams.page_size"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="getList"
          @current-change="getList"
        />
      </div>
    </el-card>

    <!-- 详情弹窗 -->
    <el-dialog title="识别记录详情" v-model="detailVisible" width="600px" append-to-body>
      <el-descriptions :column="2" border>
        <el-descriptions-item label="ID">{{ detailData.id }}</el-descriptions-item>
        <el-descriptions-item label="用户ID">{{ detailData.user_id }}</el-descriptions-item>
        <el-descriptions-item label="车牌号">{{ detailData.license_plate }}</el-descriptions-item>
        <el-descriptions-item label="车牌类型">{{ detailData.plate_type }}</el-descriptions-item>
        <el-descriptions-item label="置信度">{{ (detailData.confidence * 100).toFixed(2) }}%</el-descriptions-item>
        <el-descriptions-item label="处理耗时">{{ detailData.processing_time }} ms</el-descriptions-item>
        <el-descriptions-item label="模型版本">{{ detailData.model_version }}</el-descriptions-item>
        <el-descriptions-item label="增强算法">{{ detailData.enhance_algorithm || '无' }}</el-descriptions-item>
        <el-descriptions-item label="识别时间" :span="2">{{ formatTime(detailData.created_at) }}</el-descriptions-item>
        <el-descriptions-item label="原始图片" :span="2">
          <el-image :src="detailData.original_image_url" fit="contain" preview-teleported />
        </el-descriptions-item>
        <el-descriptions-item v-if="detailData.enhanced_image_url" label="增强图片" :span="2">
          <el-image :src="detailData.enhanced_image_url" fit="contain" preview-teleported />
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getRecords, deleteRecord, type RecognitionRecord } from '@/api/recognition-api'
import dayjs from 'dayjs'

const loading = ref(false)
const total = ref(0)
const recordList = ref<RecognitionRecord[]>([])
const detailVisible = ref(false)
const detailData = ref<any>({})

const queryParams = reactive({
  page: 1,
  page_size: 20,
  license_plate: undefined,
  plate_type: undefined,
  user_id: undefined
})

const getList = async () => {
  loading.value = true
  try {
    const res: any = await getRecords(queryParams)
    recordList.value = res.list
    total.value = res.total
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const handleQuery = () => {
  queryParams.page = 1
  getList()
}

const resetQuery = () => {
  queryParams.license_plate = undefined
  queryParams.plate_type = undefined
  queryParams.user_id = undefined
  handleQuery()
}

const handleDetail = (row: RecognitionRecord) => {
  detailData.value = row
  detailVisible.value = true
}

const handleDelete = (row: RecognitionRecord) => {
  ElMessageBox.confirm('是否确认删除ID为\"' + row.id + '\"的识别记录？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    await deleteRecord(row.id)
    ElMessage.success('删除成功')
    getList()
  }).catch(() => {})
}

const getPlateTypeTag = (type?: string): any => {
  switch (type) {
    case 'blue': return 'primary'
    case 'yellow': return 'warning'
    case 'green': return 'success'
    case 'white': return 'info'
    default: return 'info'
  }
}

const formatTime = (timeStr: string) => {
  if (!timeStr) return ''
  return dayjs(timeStr).format('YYYY-MM-DD HH:mm:ss')
}

onMounted(() => {
  getList()
})
</script>

<style scoped>
.app-container {
  padding: 20px;
}
.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
