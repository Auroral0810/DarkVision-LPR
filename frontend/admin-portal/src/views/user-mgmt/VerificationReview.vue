<template>
  <div class="app-container">
    <el-card>
      <el-tabs v-model="activeTab" @tab-change="handleQuery">
        <el-tab-pane label="待审核" name="pending" />
        <el-tab-pane label="已通过" name="approved" />
        <el-tab-pane label="已拒绝" name="rejected" />
      </el-tabs>

      <el-table v-loading="loading" :data="pageData">
        <el-table-column label="用户ID" prop="user_id" width="80" />
        <el-table-column label="申请时间" prop="created_at" width="160" />
        <el-table-column label="身份证照片" width="300">
          <template #default="scope">
            <div style="display: flex; gap: 10px">
              <el-image :src="scope.row.id_card_front" style="width: 120px" fit="contain" :preview-src-list="[scope.row.id_card_front]" />
              <el-image :src="scope.row.id_card_back" style="width: 120px" fit="contain" :preview-src-list="[scope.row.id_card_back]" />
            </div>
          </template>
        </el-table-column>
        <el-table-column label="人脸照片" width="150">
          <template #default="scope">
            <el-image v-if="scope.row.face_photo" :src="scope.row.face_photo" style="width: 100px" fit="contain" />
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.status === 'approved' ? 'success' : scope.row.status === 'rejected' ? 'danger' : ''">
              {{ scope.row.status === 'pending' ? '待审核' : scope.row.status === 'approved' ? '已通过' : '已拒绝' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="拒绝原因" prop="reject_reason" show-overflow-tooltip />
        <el-table-column label="操作" width="200" v-if="activeTab === 'pending'">
          <template #default="scope">
            <el-button type="success" link @click="handleReview(scope.row.id, 'approved')">通过</el-button>
            <el-button type="danger" link @click="handleReject(scope.row)">拒绝</el-button>
          </template>
        </el-table-column>
      </el-table>

      <pagination v-if="total > 0" v-model:total="total" v-model:page="queryParams.page" v-model:limit="queryParams.pageSize" @pagination="fetchList" />
    </el-card>

    <el-dialog v-model="rejectDialogVisible" title="拒绝认证" width="500px">
      <el-input v-model="rejectReason" type="textarea" rows="4" placeholder="请输入拒绝原因" />
      <template #footer>
        <el-button @click="rejectDialogVisible = false">取消</el-button>
        <el-button type="danger" @click="handleConfirmReject">确定拒绝</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import LprAPI from '@/api/lpr-api'

const activeTab = ref('pending')
const pageData = ref([])
const total = ref(0)
const loading = ref(false)
const queryParams = reactive({ status: 'pending', page: 1, pageSize: 10 })
const rejectDialogVisible = ref(false)
const rejectReason = ref('')
const currentReviewId = ref(0)

async function fetchList() {
  loading.value = true
  try {
    queryParams.status = activeTab.value
    const data = await LprAPI.getVerificationList(queryParams)
    pageData.value = data.list
    total.value = data.total
  } finally {
    loading.value = false
  }
}

function handleQuery() {
  queryParams.page = 1
  fetchList()
}

async function handleReview(id: number, status: 'approved' | 'rejected', reason?: string) {
  try {
    await LprAPI.reviewVerification({ verification_id: id, status, reject_reason: reason })
    ElMessage.success(status === 'approved' ? '审核通过' : '已拒绝')
    fetchList()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

function handleReject(row: any) {
  currentReviewId.value = row.id
  rejectReason.value = ''
  rejectDialogVisible.value = true
}

function handleConfirmReject() {
  if (!rejectReason.value) {
    ElMessage.warning('请输入拒绝原因')
    return
  }
  handleReview(currentReviewId.value, 'rejected', rejectReason.value)
  rejectDialogVisible.value = false
}

onMounted(() => {
  fetchList()
})
</script>
