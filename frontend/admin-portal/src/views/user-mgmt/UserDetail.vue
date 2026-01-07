<template>
  <div class="user-detail-container">
    <el-skeleton :loading="loading" animated>
      <template #default>
        <!-- 头部摘要信息卡片 -->
        <div class="header-summary">
          <div class="summary-card status-card">
            <div class="card-icon" :class="userInfo?.status">
              <el-icon><UserIcon /></el-icon>
            </div>
            <div class="card-content">
              <span class="label">账户状态</span>
              <span class="value">{{ getStatusLabel(userInfo?.status) }}</span>
            </div>
          </div>
          <div class="summary-card type-card">
            <div class="card-icon" :class="userInfo?.user_type">
              <el-icon><Management /></el-icon>
            </div>
            <div class="card-content">
              <span class="label">用户类型</span>
              <span class="value">{{ getUserTypeLabel(userInfo?.user_type) }}</span>
            </div>
          </div>
          <div class="summary-card quota-card">
            <div class="card-icon">
              <el-icon><PieChart /></el-icon>
            </div>
            <div class="card-content">
              <span class="label">今日限额使用</span>
              <span class="value">{{ getQuotaPercentage() }}%</span>
            </div>
          </div>
        </div>

        <el-tabs v-model="activeTab" class="detail-tabs">
          <!-- 核心概览 -->
          <el-tab-pane label="核心概览" name="overview">
            <div class="tab-content">
               <el-descriptions :column="2" border>
                <el-descriptions-item label="用户ID">
                   <el-tag size="small" effect="plain">{{ userInfo?.id }}</el-tag>
                </el-descriptions-item>
                <el-descriptions-item label="昵称">{{ userInfo?.nickname }}</el-descriptions-item>
                <el-descriptions-item label="手机号">{{ userInfo?.phone || '未绑定' }}</el-descriptions-item>
                <el-descriptions-item label="邮箱">{{ userInfo?.email || '未设置' }}</el-descriptions-item>
                <el-descriptions-item label="注册时间">{{ formatDate(userInfo?.created_at) }}</el-descriptions-item>
                <el-descriptions-item label="最后登录">{{ formatDate(userInfo?.last_login_at) }}</el-descriptions-item>
                <el-descriptions-item label="最后登录IP">{{ userInfo?.last_login_ip || '未知' }}</el-descriptions-item>
                <el-descriptions-item label="封禁说明" v-if="userInfo?.status === 'banned'">
                   <div class="ban-highlight">
                     <el-alert :title="'原因: ' + (userInfo?.banned_reason || '未定义')" type="error" :closable="false" />
                     <div v-if="userInfo?.banned_until" class="ban-until">截至: {{ formatDate(userInfo.banned_until) }}</div>
                   </div>
                </el-descriptions-item>
              </el-descriptions>
              
              <div class="overview-stats">
                <div class="stat-item">
                  <div class="stat-label">今日识别</div>
                  <div class="stat-value primary">{{ userInfo?.used_quota_today }} / {{ userInfo?.daily_quota }}</div>
                  <el-progress :percentage="getQuotaPercentage()" :status="getQuotaPercentage() > 90 ? 'exception' : ''" :stroke-width="10" />
                </div>
                <div class="stat-item">
                  <div class="stat-label">累计识别</div>
                  <div class="stat-value">{{ userInfo?.total_recognition_count }}</div>
                </div>
              </div>
            </div>
          </el-tab-pane>

          <!-- 账户与资料 -->
          <el-tab-pane label="账户与资料" name="profile">
            <div class="tab-content">
              <el-descriptions title="身份信息" :column="2" border>
                <el-descriptions-item label="真实姓名">{{ userInfo?.real_name || '未填写' }}</el-descriptions-item>
                <el-descriptions-item label="性别">{{ getGenderLabel(userInfo?.gender) }}</el-descriptions-item>
                <el-descriptions-item label="生日">{{ userInfo?.birthday || '未设置' }}</el-descriptions-item>
                <el-descriptions-item label="居住地址" :span="2">{{ userInfo?.address || '未填写' }}</el-descriptions-item>
              </el-descriptions>

              <el-divider />

              <el-descriptions title="会员详情" :column="2" border>
                <el-descriptions-item label="会员等级">
                  <el-tag :type="userInfo?.is_membership_active ? 'warning' : 'info'" effect="dark">
                    {{ userInfo?.membership_type || '普通用户' }}
                  </el-tag>
                </el-descriptions-item>
                <el-descriptions-item label="有效期至" v-if="userInfo?.is_membership_active">
                  {{ formatDate(userInfo?.membership_expire_date) }}
                </el-descriptions-item>
                <el-descriptions-item label="会员状态">
                  {{ userInfo?.is_membership_active ? '生效中' : '已过期/未开通' }}
                </el-descriptions-item>
              </el-descriptions>
            </div>
          </el-tab-pane>

          <!-- 业务数据 -->
          <el-tab-pane label="业务与统计" name="usage">
            <div class="tab-content">
              <div class="usage-grid">
                <el-card shadow="never" class="usage-card">
                  <template #header>服务使用统计</template>
                  <div class="usage-info">
                    <div class="info-row">
                      <span>总识别任务:</span>
                      <strong>{{ userInfo?.total_recognition_count }} 次</strong>
                    </div>
                    <div class="info-row">
                      <span>最后识别活动:</span>
                      <strong>{{ formatDate(userInfo?.last_recognition_at) || '暂无活动' }}</strong>
                    </div>
                  </div>
                </el-card>
                
                <el-card shadow="never" class="usage-card">
                  <template #header>财务统计</template>
                  <div class="usage-info">
                    <div class="info-row">
                      <span>累计消费金额:</span>
                      <strong class="money">￥{{ userInfo?.total_order_amount?.toFixed(2) }}</strong>
                    </div>
                    <div class="info-row">
                      <span>成功订单数:</span>
                      <strong>{{ userInfo?.order_count }} 笔</strong>
                    </div>
                  </div>
                </el-card>
              </div>

              <div class="quota-detail">
                <h4>今日配额详情</h4>
                <div class="quota-bars">
                  <div class="bar-label">
                    <span>接口识别 ({{ userInfo?.used_quota_today }}/{{ userInfo?.daily_quota }})</span>
                    <span>{{ getQuotaPercentage() }}%</span>
                  </div>
                  <el-progress :percentage="getQuotaPercentage()" primary />
                </div>
              </div>
            </div>
          </el-tab-pane>

          <!-- 认证与安全 -->
          <el-tab-pane label="认证与安全" name="security">
            <div class="tab-content">
              <div class="verification-section">
                <div class="verify-status">
                   <span>实名认证状态: </span>
                   <el-tag :type="getVerifyStatusColor(userInfo?.verification_status)">
                    {{ getVerifyStatusLabel(userInfo?.verification_status) }}
                  </el-tag>
                  <div v-if="userInfo?.verification_status === 'rejected'" class="reject-reason">
                    驳回原因: {{ userInfo?.reject_reason }}
                  </div>
                </div>

                <div class="verify-images" v-if="userInfo?.id_card_front || userInfo?.id_card_back">
                   <div class="image-box" v-if="userInfo?.id_card_front">
                      <el-image 
                        :src="userInfo.id_card_front" 
                        :preview-src-list="[userInfo.id_card_front]" 
                        fit="cover" 
                      />
                      <div class="img-label">身份证正面</div>
                   </div>
                   <div class="image-box" v-if="userInfo?.id_card_back">
                      <el-image 
                        :src="userInfo.id_card_back" 
                        :preview-src-list="[userInfo.id_card_back]" 
                        fit="cover" 
                      />
                      <div class="img-label">身份证反面</div>
                   </div>
                </div>
              </div>

              <el-divider />

              <el-descriptions title="层级与权限" :column="2" border>
                <el-descriptions-item label="归属类别">
                   {{ userInfo?.is_enterprise_main ? '企业主账户' : (userInfo?.parent_id ? '企业子账户' : '独立账户') }}
                </el-descriptions-item>
                <el-descriptions-item label="所属主账户" v-if="userInfo?.parent_id">
                  {{ userInfo?.parent_nickname }}
                </el-descriptions-item>
                <el-descriptions-item label="管理角色" :span="2" v-if="userInfo?.is_admin">
                  <el-tag v-for="role in userInfo?.roles" :key="role" size="small" class="role-tag">{{ role }}</el-tag>
                </el-descriptions-item>
              </el-descriptions>
            </div>
          </el-tab-pane>
        </el-tabs>

        <div class="action-footer">
          <el-button type="primary" plain icon="Remove" @click="handleForceLogout">强制下线</el-button>
          <el-button type="danger" plain icon="Delete" @click="handleDeleteUser">删除账户</el-button>
        </div>
      </template>
    </el-skeleton>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import LprAPI from '@/api/lpr-api'
import type { User } from '@/types/lpr'
import { ElMessage, ElMessageBox } from 'element-plus'
import { User as UserIcon, Management, PieChart } from '@element-plus/icons-vue'

const props = defineProps<{ userId: number }>()
const userInfo = ref<User | null>(null)
const loading = ref(false)
const activeTab = ref('overview')

async function fetchUserDetail() {
  loading.value = true
  try {
    userInfo.value = await LprAPI.getUserDetail(props.userId)
  } catch (err) {
    ElMessage.error('获取用户详情失败')
  } finally {
    loading.value = false
  }
}

// 格式化展示
function formatDate(dateStr?: string | null) {
  if (!dateStr) return '-'
  return dateStr.replace('T', ' ').split('.')[0]
}

function getUserTypeLabel(type?: string) {
  const map: Record<string, string> = { free: '普通用户', vip: 'VIP', enterprise: '企业用户', admin: '系统管理员' }
  return map[type || ''] || type
}

function getUserTypeColor(type?: string): 'success' | 'warning' | 'danger' | 'info' {
  const map: Record<string, 'success' | 'warning' | 'danger' | 'info'> = {
    free: 'info',
    vip: 'warning',
    enterprise: 'success',
    admin: 'danger'
  }
  return (map[type || ''] || 'info') as any
}

function getStatusLabel(status?: string) {
  const map: Record<string, string> = { active: '账号正常', inactive: '已禁用', banned: '已封禁' }
  return map[status || ''] || status
}

function getStatusColor(status?: string): 'success' | 'warning' | 'danger' | 'info' {
  const map: Record<string, 'success' | 'warning' | 'danger' | 'info'> = {
    active: 'success',
    inactive: 'info',
    banned: 'danger'
  }
  return (map[status || ''] || 'info') as any
}

function getGenderLabel(gender?: string | null) {
  const map: Record<string, string> = { male: '男', female: '女', unknown: '未知' }
  return map[gender || ''] || '未知'
}

function getVerifyStatusLabel(status?: string | null) {
  const map: Record<string, string> = { 
    pending: '审核中', 
    approved: '认证通过', 
    rejected: '被驳回' 
  }
  return map[status || ''] || '未发起认证'
}

function getVerifyStatusColor(status?: string | null): 'primary' | 'success' | 'danger' | 'info' {
  const map: Record<string, 'primary' | 'success' | 'danger' | 'info'> = {
    pending: 'primary',
    approved: 'success',
    rejected: 'danger'
  }
  return (map[status || ''] || 'info') as any
}

function getQuotaPercentage() {
  if (!userInfo.value || !userInfo.value.daily_quota) return 0
  return Math.min(100, Math.round((userInfo.value.used_quota_today || 0) / userInfo.value.daily_quota * 100))
}

const handleForceLogout = () => {
  ElMessage.info('功能开发中...')
}

const handleDeleteUser = () => {
  ElMessageBox.confirm('确定要删除该用户吗？此操作不可逆！', '危险操作', {
    type: 'error',
    confirmButtonClass: 'el-button--danger'
  }).then(() => {
    ElMessage.info('功能开发中...')
  }).catch(() => {})
}

onMounted(() => {
  fetchUserDetail()
})
</script>

<style scoped lang="scss">
.user-detail-container {
  padding: 0 5px 20px;
  background: #fcfcfd;

  .header-summary {
    display: flex;
    gap: 15px;
    margin-bottom: 25px;

    .summary-card {
      flex: 1;
      background: #fff;
      border-radius: 12px;
      padding: 15px;
      display: flex;
      align-items: center;
      gap: 15px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.03);
      border: 1px solid #f0f0f0;

      .card-icon {
        width: 48px;
        height: 48px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        background: #f5f7fa;
        color: #909399;

        &.active, &.vip { background: #f0f9eb; color: #67c23a; }
        &.banned, &.admin { background: #fef0f0; color: #f56c6c; }
        &.enterprise { background: #ecf5ff; color: #409eff; }
      }

      .card-content {
        .label { font-size: 13px; color: #909399; display: block; margin-bottom: 4px; }
        .value { font-size: 16px; font-weight: 600; color: #303133; }
      }
    }
  }

  .detail-tabs {
    background: #fff;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    border: 1px solid #f0f0f0;
    overflow: hidden;

    :deep(.el-tabs__header) {
      margin: 0;
      padding: 5px 15px 0;
      background: #fafafa;
      border-bottom: 1px solid #f0f0f0;
    }

    .tab-content {
      padding: 20px;
    }
  }

  .ban-highlight {
    margin-top: 5px;
    .ban-until { margin-top: 8px; font-size: 12px; color: #909399; text-align: right; }
  }

  .overview-stats {
    display: flex;
    gap: 30px;
    margin-top: 25px;
    .stat-item {
      flex: 1;
      .stat-label { font-size: 14px; color: #606266; margin-bottom: 10px; }
      .stat-value { font-size: 24px; font-weight: 700; margin-bottom: 8px;
        &.primary { color: var(--el-color-primary); }
      }
    }
  }

  .usage-grid {
    display: flex;
    gap: 20px;
    margin-bottom: 25px;
    .usage-card {
      flex: 1;
      .usage-info {
        .info-row {
          display: flex;
          justify-content: space-between;
          margin-bottom: 12px;
          font-size: 14px;
          span { color: #909399; }
          strong { color: #303133; &.money { color: var(--el-color-warning); font-size: 16px;} }
        }
      }
    }
  }

  .verification-section {
    .verify-status {
      margin-bottom: 20px;
      font-size: 15px;
      .reject-reason { margin-top: 10px; color: var(--el-color-danger); font-size: 13px; }
    }
    .verify-images {
       display: flex;
       gap: 20px;
       .image-box {
         flex: 1;
         .el-image {
           width: 100%;
           height: 160px;
           border-radius: 8px;
           border: 1px solid #f0f0f0;
           cursor: pointer;
           transition: transform 0.3s;
           &:hover { transform: scale(1.02); }
         }
         .img-label { text-align: center; margin-top: 8px; font-size: 13px; color: #909399; }
       }
    }
  }

  .role-tag { margin-right: 8px; }

  .action-footer {
    margin-top: 30px;
    display: flex;
    justify-content: center;
    gap: 20px;
    .el-button { padding: 12px 30px; }
  }
}
</style>
