<template>
  <div class="app-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>订单管理</span>
          <div class="header-ops">
            <el-button type="primary" icon="Plus" @click="handleManualOrder">手动创建订单</el-button>
            <el-button icon="Download" @click="handleExport">导出 CSV</el-button>
          </div>
        </div>
      </template>

      <div class="filter-container mb-4">
        <el-select v-model="listQuery.status" placeholder="订单状态" clearable style="width: 150px">
          <el-option label="待支付" value="pending" />
          <el-option label="已支付" value="paid" />
          <el-option label="已取消" value="cancelled" />
          <el-option label="已退款" value="refunded" />
        </el-select>
        <el-button class="ml-2" type="primary" icon="Search" @click="fetchData">查询</el-button>
      </div>

      <el-table v-loading="loading" :data="list" border stripe>
        <el-table-column label="订单号" prop="order_no" width="200" align="center" />
        <el-table-column label="用户" prop="nickname" align="center" />
        <el-table-column label="产品套餐" prop="package_name" align="center" />
        <el-table-column label="金额" prop="amount" width="120" align="center">
          <template #default="{ row }">￥{{ row.amount }}</template>
        </el-table-column>
        <el-table-column label="支付方式" prop="payment_method" width="120" align="center" />
        <el-table-column label="状态" prop="status" width="120" align="center">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ getStatusLabel(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="创建时间" prop="created_at" width="180" align="center" />
        <el-table-column label="操作" width="150" align="center">
          <template #default="{ row }">
            <el-button v-if="row.status === 'paid'" type="danger" link @click="handleRefund(row)">退款</el-button>
            <el-button type="primary" link icon="View">详情</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container mt-4">
        <el-pagination
          v-model:current-page="listQuery.page"
          v-model:page-size="listQuery.limit"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @current-change="fetchData"
          @size-change="fetchData"
        />
      </div>
    </el-card>

    <!-- 手动创建订单对话框 -->
    <el-dialog v-model="dialogVisible" title="手动创建订单">
       <el-form :model="orderForm" label-width="100px">
         <el-form-item label="用户 ID">
           <el-input v-model="orderForm.user_id" placeholder="请输入用户ID" />
         </el-form-item>
         <el-form-item label="套餐 ID">
           <el-input v-model="orderForm.package_id" placeholder="请输入套餐ID" />
         </el-form-item>
         <el-form-item label="金额">
           <el-input-number v-model="orderForm.amount" :precision="2" :step="0.1" />
         </el-form-item>
         <el-form-item label="支付状态">
           <el-radio-group v-model="orderForm.status">
             <el-radio label="pending">待支付</el-radio>
             <el-radio label="paid">已支付</el-radio>
           </el-radio-group>
         </el-form-item>
       </el-form>
       <template #footer>
         <el-button @click="dialogVisible = false">取消</el-button>
         <el-button type="primary" @click="submitManualOrder">确定</el-button>
       </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/utils/request'

const list = ref([])
const total = ref(0)
const loading = ref(false)
const dialogVisible = ref(false)

const listQuery = ref({
  page: 1,
  limit: 20,
  status: ''
})

const orderForm = ref({
  user_id: '',
  package_id: '',
  amount: 0,
  status: 'paid'
})

async function fetchData() {
  loading.value = true
  try {
    const skip = (listQuery.value.page - 1) * listQuery.value.limit
    const data = await request.get('/api/admin/orders/', {
      params: { 
        skip, 
        limit: listQuery.value.limit,
        status: listQuery.value.status || undefined
      }
    })
    list.value = data || []
  } catch (err) {
  } finally {
    loading.value = false
  }
}

function getStatusType(s: string) {
  const map: any = { paid: 'success', pending: 'warning', cancelled: 'info', refunded: 'danger' }
  return map[s] || 'info'
}

function getStatusLabel(s: string) {
  const map: any = { paid: '已支付', pending: '待支付', cancelled: '已取消', refunded: '已退款' }
  return map[s] || s
}

function handleManualOrder() {
  dialogVisible.value = true
}

async function submitManualOrder() {
  try {
    await request.post('/api/admin/orders/manual', orderForm.value)
    ElMessage.success('订单创建成功')
    dialogVisible.value = false
    fetchData()
  } catch (err) {
  }
}

async function handleRefund(row: any) {
  try {
    await ElMessageBox.confirm('确定要为该订单办理退款吗？', '提示', { type: 'warning' })
    await request.post(`/api/admin/orders/${row.id}/refund`)
    ElMessage.success('退款申请已提交')
    fetchData()
  } catch (err) {
  }
}

function handleExport() {
  ElMessage.info('功能开发中...')
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
.mb-4 { margin-bottom: 20px; }
.ml-2 { margin-left: 8px; }
.mt-4 { margin-top: 20px; }
</style>
