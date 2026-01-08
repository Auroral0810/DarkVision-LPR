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
            <el-table-column label="操作" width="250" align="center">
              <template #default="{ row }">
                <el-button type="primary" link icon="Edit" @click="handleEditPackage(row)">编辑</el-button>
                <el-button type="success" link icon="List" @click="handleViewFeatures(row)">权益</el-button>
                <el-button type="warning" link icon="Ticket" @click="handlePromotion(row)">促销</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="当前促销" name="promotions">
           <el-table :data="promotions" border stripe v-loading="loading">
             <el-table-column label="活动名称" prop="name" align="center" />
             <el-table-column label="折扣率" prop="discount_rate" align="center" />
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

    <!-- 权益明细编辑抽屉 -->
    <el-drawer v-model="featureDrawerVisible" :title="`权益明细 - ${currentPackage?.name}`" size="500px">
      <el-form label-position="top">
        <el-table :data="featureList" border stripe size="small">
          <el-table-column label="功能点" width="180">
            <template #default="{ row }">
              <div class="feature-key-col">
                <div class="display-name">{{ row.feature_display_name || row.feature_key }}</div>
                <code class="key-code">{{ row.feature_key }}</code>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="配置值">
            <template #default="{ row }">
              <div style="display: flex; align-items: center; gap: 8px;">
                <el-switch v-if="isBooleanFeature(row)" v-model="row.feature_value" active-value="true" inactive-value="false" />
                <el-input-number v-else-if="isNumberFeature(row)" v-model="row.feature_value" :min="0" style="flex: 1" />
                <el-input v-else v-model="row.feature_value" placeholder="请输入值" style="flex: 1" />
                <el-tooltip v-if="row.feature_description" :content="row.feature_description" placement="top">
                  <el-icon><InfoFilled /></el-icon>
                </el-tooltip>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </el-form>
      <template #footer>
        <el-button @click="featureDrawerVisible = false">取消</el-button>
        <el-button type="primary" @click="submitFeatures" :loading="featureLoading">保存更改</el-button>
      </template>
    </el-drawer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { InfoFilled } from '@element-plus/icons-vue'
import request from '@/utils/request'
import { usePackageStore } from '@/store'

const packageStore = usePackageStore()
const activeTab = ref('packages')
const packages = computed(() => packageStore.packages)
const promotions = ref([])
const loading = computed(() => packageStore.loading)
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
} as any)

const featureDrawerVisible = ref(false)
const featureLoading = ref(false)
const currentPackage = ref<any>(null)
const featureList = ref<any[]>([])

async function fetchPackages() {
  await packageStore.fetchPackages()
}

async function fetchPromotions() {
  try {
    const data = await request.get('/api/admin/packages/promotions')
    promotions.value = (data as any) || []
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
    const submitData = {
      ...pkgForm.value,
      features: pkgForm.value.features?.map((f: any) => ({
        ...f,
        feature_value: String(f.feature_value)
      }))
    }
    if (isEdit.value) {
      await request.put(`/api/admin/packages/packages/${pkgForm.value.id}`, submitData)
    } else {
      await request.post('/api/admin/packages/packages', submitData)
    }
    ElMessage.success('操作成功')
    pkgDialogVisible.value = false
    fetchPackages()
  } catch (err) {
  }
}

async function handleViewFeatures(row: any) {
  currentPackage.value = row
  featureDrawerVisible.value = true
  try {
    const data = await request.get(`/api/admin/packages/packages/${row.id}/features`)
    featureList.value = (data as any) || []
  } catch (err) {
    ElMessage.error('获取权益失败')
  }
}

async function submitFeatures() {
  if (!currentPackage.value) return
  featureLoading.value = true
  try {
    // 关键修复：确保所有 feature_value 都是字符串
    const formattedFeatures = featureList.value.map(f => ({
      ...f,
      feature_value: String(f.feature_value)
    }))
    await request.put(`/api/admin/packages/packages/${currentPackage.value.id}/features`, {
      features: formattedFeatures
    })
    ElMessage.success('权益更新成功')
    featureDrawerVisible.value = false
    fetchPackages()
  } catch (err) {
  } finally {
    featureLoading.value = false
  }
}

function isBooleanFeature(row: any) {
  return row.feature_value === 'true' || row.feature_value === 'false' || row.feature_key.endsWith('_enabled') || row.feature_key.startsWith('ad_') || row.feature_key.includes('sync')
}

function isNumberFeature(row: any) {
  const k = row.feature_key
  return k.includes('limit') || k.includes('count') || k.includes('size') || k.includes('days') || k.includes('records') || k.includes('discount')
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
.feature-key-col { display: flex; flex-direction: column; }
.display-name { font-weight: bold; font-size: 13px; }
.key-code { font-size: 11px; color: #909399; margin-top: 2px; }
</style>
