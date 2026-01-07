<template>
  <div class="verification-container">
    <div class="filter-header">
      <el-form :inline="true" :model="queryParams">
        <el-form-item label="关键字">
          <el-input v-model="queryParams.keyword" placeholder="昵称 / 手机 / 邮箱" clearable @keyup.enter="handleQuery" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="queryParams.status" placeholder="认证状态" clearable style="width: 140px">
            <el-option label="待审核" value="pending" />
            <el-option label="已通过" value="approved" />
            <el-option label="已驳回" value="rejected" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleQuery">查询</el-button>
          <el-button @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <el-card shadow="never">
      <el-table v-loading="loading" :data="dataList" border style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" align="center" />
        
        <el-table-column label="申请人" min-width="180">
          <template #default="{ row }">
            <div class="user-cell">
               <el-avatar :size="32" :src="row.user.avatar_url">
                  {{ row.user.nickname.charAt(0) }}
               </el-avatar>
               <div class="user-info">
                 <div class="name">{{ row.user.nickname }}</div>
                 <div class="sub">{{ row.user.phone || row.user.email || '无联系方式' }}</div>
               </div>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="real_name" label="真实姓名" width="120" />
        <el-table-column prop="id_card_number" label="身份证号" width="180" />
        
        <el-table-column label="提交时间" width="170" align="center">
          <template #default="{ row }">
            {{ formatTime(row.created_at) }}
          </template>
        </el-table-column>
        
        <el-table-column label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ getStatusText(row.status) }}</el-tag>
          </template>
        </el-table-column>

        <el-table-column label="操作" width="120" align="center" fixed="right">
          <template #default="{ row }">
            <el-button 
                text 
                type="primary" 
                size="small" 
                @click="openAudit(row)"
            >
                {{ row.status === 'pending' ? '审核' : '查看详情' }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-footer">
        <el-pagination
          v-model:current-page="queryParams.page"
          v-model:page-size="queryParams.pageSize"
          :total="total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleQuery"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>

    <audit-dialog 
        v-model="auditVisible" 
        :verification-id="currentRow?.id || null"
        :detail-from-list="currentRow"
        @success="handleQuery"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import VerificationAPI, { type VerificationItem, type VerificationListParams } from '@/api/verification-api'
import dayjs from 'dayjs'
import AuditDialog from './components/AuditDialog.vue'

const loading = ref(false)
const dataList = ref<VerificationItem[]>([])
const total = ref(0)
const auditVisible = ref(false)
const currentRow = ref<VerificationItem | null>(null)

const queryParams = reactive<VerificationListParams>({
  page: 1,
  pageSize: 10,
  keyword: '',
  status: 'pending' // Default to pending tasks
})

const getStatusType = (status: string) => {
  const map: any = { pending: 'warning', approved: 'success', rejected: 'danger' }
  return map[status] || 'info'
}

const getStatusText = (status: string) => {
  const map: any = { pending: '待审核', approved: '已通过', rejected: '已驳回' }
  return map[status] || status
}

const formatTime = (time: string) => {
  return dayjs(time).format('YYYY-MM-DD HH:mm')
}

const fetchList = async () => {
    loading.value = true
    try {
        const res = await VerificationAPI.getVerifications(queryParams)
        dataList.value = res.list
        total.value = res.total
    } finally {
        loading.value = false
    }
}

const handleQuery = () => {
    queryParams.page = 1
    fetchList()
}

const resetQuery = () => {
    queryParams.keyword = ''
    queryParams.status = ''
    handleQuery()
}

const handlePageChange = (page: number) => {
    queryParams.page = page
    fetchList()
}

const openAudit = (row: VerificationItem) => {
    currentRow.value = row
    auditVisible.value = true
}

onMounted(() => {
    fetchList()
})
</script>

<style scoped lang="scss">
.verification-container {
  padding: 20px;
  
  .filter-header {
      background-color: #fff;
      padding: 18px 20px 0;
      margin-bottom: 20px;
      border-radius: 4px;
      box-shadow: 0 1px 4px rgba(0,21,41,.08);
  }
}

.user-cell {
    display: flex;
    align-items: center;
    gap: 10px;
    
    .user-info {
        display: flex;
        flex-direction: column;
        line-height: 1.3;
        
        .name {
            font-weight: 500;
        }
        .sub {
            font-size: 12px;
            color: #909399;
        }
    }
}

.pagination-footer {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
}
</style>
