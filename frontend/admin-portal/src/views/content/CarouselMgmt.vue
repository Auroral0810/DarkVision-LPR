<template>
  <div class="app-container">
    <el-card shadow="hover">
      <div class="header-actions" style="margin-bottom: 20px;">
        <el-button type="primary" icon="Plus" @click="handleAdd">新增轮播图</el-button>
        <el-button icon="Refresh" @click="fetchData">刷新</el-button>
      </div>

      <el-table v-loading="loading" :data="carousels" border>
        <el-table-column prop="id" label="ID" width="80" align="center" />
        <el-table-column prop="title" label="标题" min-width="150" />
        <el-table-column prop="image_url" label="图片" width="180">
          <template #default="{ row }">
            <el-image 
              :src="row.image_url" 
              :preview-src-list="[row.image_url]"
              fit="cover"
              style="width: 150px; height: 80px; border-radius: 4px;"
            />
          </template>
        </el-table-column>
        <el-table-column prop="link_url" label="跳转链接" min-width="150" />
        <el-table-column prop="sort_order" label="排序" width="80" align="center" />
        <el-table-column prop="is_enabled" label="状态" width="100" align="center">
           <template #default="{ row }">
            <el-tag :type="row.is_enabled ? 'success' : 'info'">
              {{ row.is_enabled ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" align="center" />
        <el-table-column label="操作" width="150" align="center" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- Dialog -->
    <el-dialog
      :title="isEdit ? '编辑轮播图' : '新增轮播图'"
      v-model="dialogVisible"
      width="500px"
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入标题" />
        </el-form-item>
        <el-form-item label="图片链接" prop="image_url">
          <el-input v-model="form.image_url" placeholder="请输入图片URL" />
        </el-form-item>
        <el-form-item label="跳转链接" prop="link_url">
          <el-input v-model="form.link_url" placeholder="请输入跳转URL (可选)" />
        </el-form-item>
        <el-form-item label="排序" prop="sort_order">
          <el-input-number v-model="form.sort_order" :min="0" />
        </el-form-item>
        <el-form-item label="是否启用" prop="is_enabled">
           <el-switch v-model="form.is_enabled" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit" :loading="submitLoading">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { useContentStore } from '@/store/modules/content-store'
import { storeToRefs } from 'pinia'
import { ElMessage, ElMessageBox } from 'element-plus'

const store = useContentStore()
const { carousels, loading } = storeToRefs(store)

const dialogVisible = ref(false)
const submitLoading = ref(false)
const isEdit = ref(false)
const formRef = ref()

const form = reactive({
  id: undefined,
  title: '',
  image_url: '',
  link_url: '',
  sort_order: 0,
  is_enabled: true
})

const rules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  image_url: [{ required: true, message: '请输入图片URL', trigger: 'blur' }]
}

function fetchData() {
  store.fetchCarousels()
}

onMounted(() => {
  fetchData()
})

function handleAdd() {
  isEdit.value = false
  form.id = undefined
  form.title = ''
  form.image_url = ''
  form.link_url = ''
  form.sort_order = 0
  form.is_enabled = true
  dialogVisible.value = true
}

function handleEdit(row: any) {
  isEdit.value = true
  form.id = row.id
  form.title = row.title
  form.image_url = row.image_url
  form.link_url = row.link_url
  form.sort_order = row.sort_order
  form.is_enabled = row.is_enabled
  dialogVisible.value = true
}

async function handleDelete(row: any) {
    try {
        await ElMessageBox.confirm('确认删除该轮播图吗？', '确认', { type: 'warning' })
        await store.deleteCarousel(row.id)
        ElMessage.success('删除成功')
    } catch (e) {}
}

async function handleSubmit() {
  if (!formRef.value) return
  await formRef.value.validate(async (valid: boolean) => {
    if (valid) {
      submitLoading.value = true
      try {
        if (isEdit.value) {
            await store.updateCarousel(form.id!, { ...form })
            ElMessage.success('更新成功')
        } else {
            await store.createCarousel({ ...form })
            ElMessage.success('创建成功')
        }
        dialogVisible.value = false
      } catch (e) {
      } finally {
        submitLoading.value = false
      }
    }
  })
}
</script>

<style scoped>
.app-container {
  padding: 20px;
}
</style>
