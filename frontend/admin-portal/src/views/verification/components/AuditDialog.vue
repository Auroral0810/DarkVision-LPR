<template>
  <el-dialog
    v-model="visible"
    title="实名认证审核"
    width="900px"
    destroy-on-close
    :close-on-click-modal="false"
  >
    <div v-if="detail" class="audit-container">
      <div class="user-info-section">
        <h3>申请人信息</h3>
        <el-descriptions :column="1" border>
          <el-descriptions-item label="用户昵称">{{ detail.user.nickname }}</el-descriptions-item>
          <el-descriptions-item label="手机号码">{{ detail.user.phone || '未绑定' }}</el-descriptions-item>
          <el-descriptions-item label="提交姓名">{{ detail.real_name || '-' }}</el-descriptions-item>
          <el-descriptions-item label="身份证号">{{ detail.id_card_number || '-' }}</el-descriptions-item>
          <el-descriptions-item label="申请时间">{{ formatDate(detail.created_at) }}</el-descriptions-item>
        </el-descriptions>
        
        <div class="status-badge">
             <el-tag :type="getStatusType(detail.status)" size="large">{{ getStatusText(detail.status) }}</el-tag>
        </div>
      </div>

      <div class="id-images-section">
        <h3>证件照片</h3>
        <div class="image-grid">
          <div class="image-item">
            <span class="label">人脸照片</span>
            <el-image 
              :src="detail.face_photo || ''" 
              :preview-src-list="detail.face_photo ? [detail.face_photo] : []"
              fit="cover"
              class="id-img"
            >
              <template #error>
                <div class="image-slot">
                  <el-icon><icon-picture /></el-icon>
                </div>
              </template>
            </el-image>
          </div>
          <div class="image-item">
            <span class="label">身份证人像面</span>
            <el-image 
              :src="detail.id_card_front || ''" 
              :preview-src-list="detail.id_card_front ? [detail.id_card_front] : []"
              fit="cover"
              class="id-img"
            >
              <template #error>
                <div class="image-slot">
                  <el-icon><icon-picture /></el-icon>
                  <span class="error-text">加载失败</span>
                </div>
              </template>
            </el-image>
          </div>
          <div class="image-item">
            <span class="label">身份证国徽面</span>
            <el-image 
              :src="detail.id_card_back || ''" 
              :preview-src-list="detail.id_card_back ? [detail.id_card_back] : []"
              fit="cover"
              class="id-img"
            >
              <template #error>
                <div class="image-slot">
                  <el-icon><icon-picture /></el-icon>
                  <span class="error-text">加载失败</span>
                </div>
              </template>
            </el-image>
          </div>
        </div>
      </div>
    </div>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="visible = false">关闭</el-button>
        <template v-if="detail?.status === 'pending'">
            <el-button type="danger" @click="handleReject">驳回</el-button>
            <el-button type="success" @click="handleApprove">通过认证</el-button>
        </template>
      </div>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { VerificationItem } from '@/api/verification-api'
import VerificationAPI from '@/api/verification-api'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Picture as IconPicture } from '@element-plus/icons-vue'
import dayjs from 'dayjs'

const props = defineProps<{
  modelValue: boolean
  verificationId: number | null
  detailFromList?: VerificationItem | null
}>()

const emit = defineEmits(['update:modelValue', 'success'])

const visible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const detail = computed(() => props.detailFromList)

const formatDate = (date: string) => {
  return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
}

const getStatusType = (status: string) => {
  const map: any = { pending: 'warning', approved: 'success', rejected: 'danger' }
  return map[status] || 'info'
}

const getStatusText = (status: string) => {
  const map: any = { pending: '待审核', approved: '已通过', rejected: '已驳回' }
  return map[status] || status
}

const handleApprove = async () => {
    if (!detail.value) return
    try {
        await ElMessageBox.confirm('确定要通过该用户的实名认证请求吗？', '通过确认', {
            confirmButtonText: '通过',
            cancelButtonText: '取消',
            type: 'warning'
        })
        
        await VerificationAPI.auditVerification(detail.value.id, { action: 'approve' })
        ElMessage.success('操作成功')
        visible.value = false
        emit('success')
    } catch (e) {
        // cancel or error
    }
}

const handleReject = async () => {
    if (!detail.value) return
    try {
        const { value } = await ElMessageBox.prompt('请输入驳回原因', '驳回确认', {
            confirmButtonText: '驳回',
            cancelButtonText: '取消',
            inputPattern: /\S+/,
            inputErrorMessage: '驳回原因不能为空'
        })
        
        await VerificationAPI.auditVerification(detail.value.id, { action: 'reject', reject_reason: value })
        ElMessage.success('操作成功')
        visible.value = false
        emit('success')
    } catch (e) {
        // cancel
    }
}
</script>

<style scoped lang="scss">
.audit-container {
  display: flex;
  gap: 20px;
}

.user-info-section {
  width: 300px;
  flex-shrink: 0;
  
  h3 {
      margin-top: 0;
      margin-bottom: 15px;
      font-size: 16px;
      border-left: 4px solid #409eff;
      padding-left: 10px;
  }
}

.status-badge {
    margin-top: 20px;
    text-align: center;
}

.id-images-section {
  flex: 1;
  
  h3 {
      margin-top: 0;
      margin-bottom: 15px;
      font-size: 16px;
      border-left: 4px solid #409eff;
      padding-left: 10px;
  }
}

.image-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
    
    .image-item {
        display: flex;
        flex-direction: column;
        
        .label {
            margin-bottom: 8px;
            font-size: 13px;
            color: #606266;
            font-weight: bold;
        }
        
        .id-img {
            width: 100%;
            height: 180px;
            border-radius: 4px;
            border: 1px solid #dcdfe6;
            background-color: #f5f7fa;
            
            :deep(.image-slot) {
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                width: 100%;
                height: 100%;
                color: #909399;
                font-size: 24px;
                gap: 8px;
                
                .error-text {
                    font-size: 12px;
                    color: #909399;
                }
            }
        }
    }
}
</style>
