<template>
  <div class="app-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>套餐与促销管理</span>
          <el-button type="primary" icon="Plus" @click="handleAddPackage">新增套餐</el-button>
        </div>
      </template>

      <el-tabs v-model="activeTab">
        <el-tab-pane label="套餐列表" name="packages">
          <el-table :data="packages" border stripe v-loading="loading">
            <el-table-column label="名称" prop="name" align="center" />
            <el-table-column label="代码" prop="code" align="center" />
            <el-table-column label="价格" prop="price" align="center">
              <template #default="{ row }">￥{{ row.price }}</template>
            </el-table-column>
            <el-table-column label="周期(月)" prop="duration_months" align="center">
              <template #default="{ row }">{{ row.duration_months || '永久' }}</template>
            </el-table-column>
            <el-table-column label="状态" width="100" align="center">
               <template #default="{ row }">
                 <el-tag :type="row.is_active ? 'success' : 'info'">{{ row.is_active ? '启用' : '禁用' }}</el-tag>
               </template>
            </el-table-column>
            <el-table-column label="操作" width="200" align="center">
              <template #default="{ row }">
                <el-button type="primary" link icon="Edit" @click="handleEditPackage(row)">编辑</el-button>
                <el-button type="warning" link icon="Ticket" @click="handlePromotion(row)">促销</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="当前促销" name="promotions">
           <el-table :data="promotions" border stripe v-loading="loading">
             <el-table-column label="活动名称" prop="name" align="center" />
             <el-table-column label="促销价格" prop="promotional_price" align="center" />
             <el-table-column label="开始时间" prop="start_time" align="center" />
             <el-table-column label="结束时间" prop="end_time" align="center" />
             <el-table-column label="状态" align="center">
                <template #default="{ row }">
                  <el-tag :type="row.is_active ? 'success' : 'danger'">{{ row.is_active ? '进行中' : '失效' }}</el-tag>
                </template>
             </el-table-column>
           </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <!-- 套餐编辑/新增对话框 -->
    <el-dialog v-model="pkgDialogVisible" :title="isEdit ? '编辑套餐' : '新增套餐'" width="600px">
      <el-form :model="pkgForm" label-width="100px">
        <el-form-item label="套餐名称">
          <el-input v-model="pkgForm.name" />
        </el-form-item>
        <el-form-item label="唯一代码">
          <el-input v-model="pkgForm.code" :disabled="isEdit" />
        </el-form-item>
        <el-form-item label="价格">
          <el-input-number v-model="pkgForm.price" :precision="2" />
        </el-form-item>
        <el-form-item label="周期(月)">
          <el-input-number v-model="pkgForm.duration_months" :min="0" placeholder="0为永久" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input type="textarea" v-model="pkgForm.description" />
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="pkgForm.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="pkgDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitPackage">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const activeTab = ref('packages')
const packages = ref([])
const promotions = ref([])
const loading = ref(false)
const pkgDialogVisible = ref(false)
const isEdit = ref(false)

const pkgForm = ref({
  id: null,
  name: '',
  code: '',
  price: 0,
  duration_months: 1,
  description: '',
  is_active: true,
  features: []
})

async function fetchPackages() {
  loading.value = true
  try {
    const res = await axios.get('/api/v1/admin/packages/packages')
    packages.value = res.data.data
  } catch (err) {
    ElMessage.error('获取套餐失败')
  } finally {
    loading.value = false
  }
}

async function fetchPromotions() {
  try {
    const res = await axios.get('/api/v1/admin/packages/promotions')
    promotions.value = res.data.data
  } catch (err) {}
}

function handleAddPackage() {
  isEdit.value = false
  pkgForm.value = { id: null, name: '', code: '', price: 0, duration_months: 1, description: '', is_active: true, features: [] }
  pkgDialogVisible.value = true
}

function handleEditPackage(row: any) {
  isEdit.value = true
  pkgForm.value = { ...row }
  pkgDialogVisible.value = true
}

async function submitPackage() {
  try {
    if (isEdit.value) {
      await axios.put(`/api/v1/admin/packages/packages/${pkgForm.value.id}`, pkgForm.value)
    } else {
      await axios.post('/api/v1/admin/packages/packages', pkgForm.value)
    }
    ElMessage.success('操作成功')
    pkgDialogVisible.value = false
    fetchPackages()
  } catch (err) {
    ElMessage.error('提交失败')
  }
}

function handlePromotion(row: any) {
  ElMessage.info(`为 ${row.name} 创建促销活动功能开发中`)
}

onMounted(() => {
  fetchPackages()
  fetchPromotions()
})
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>
