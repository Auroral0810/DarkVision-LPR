<template>
  <div class="app-container">
    <div class="search-container">
      <el-button type="primary" icon="Plus" @click="handleAdd">发布公告</el-button>
    </div>

    <el-card shadow="never" class="mt-20">
      <el-table v-loading="loading" :data="list" border highlight-current-row>
        <el-table-column label="ID" prop="id" width="80" align="center" />
        <el-table-column label="标题" prop="title" />
        <el-table-column label="位置" prop="display_position" width="100" align="center" />
        <el-table-column label="有效时间" width="300" align="center">
          <template #default="{ row }">
            <div v-if="row.start_time || row.end_time">
               {{ row.start_time ? formatDate(row.start_time) : '不限' }} 
               至 
               {{ row.end_time ? formatDate(row.end_time) : '不限' }}
            </div>
            <div v-else>永久有效</div>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="row.is_enabled ? 'success' : 'info'">
              {{ row.is_enabled ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="创建时间" prop="created_at" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" align="center">
          <template #default="scope">
            <el-button type="primary" size="small" link icon="Edit" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button type="danger" size="small" link icon="Delete" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog 
      v-model="dialog.visible" 
      :title="dialog.title" 
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入标题" />
        </el-form-item>
        <el-form-item label="显示位置" prop="display_position">
           <el-select v-model="form.display_position">
              <el-option label="顶部通告栏" value="top" />
              <el-option label="首页弹窗" value="modal" />
              <el-option label="滚动消息" value="scroll" />
           </el-select>
        </el-form-item>
        <el-form-item label="有效时间">
           <el-date-picker
              v-model="dateRange"
              type="datetimerange"
              range-separator="至"
              start-placeholder="开始时间"
              end-placeholder="结束时间"
              value-format="YYYY-MM-DD HH:mm:ss"
           />
        </el-form-item>
        <el-form-item label="状态" prop="is_enabled">
          <el-switch v-model="form.is_enabled" active-text="启用" inactive-text="禁用" />
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <el-input 
            v-model="form.content" 
            type="textarea" 
            :rows="6" 
            placeholder="请输入公告内容" 
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialog.visible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import ContentAPI, { type Announcement } from '@/api/content-api'
import dayjs from 'dayjs'

const loading = ref(false)
const list = ref<Announcement[]>([])
const dateRange = ref([])

const dialog = reactive({
  visible: false,
  title: '',
  isEdit: false
})

const formRef = ref()
const form = reactive({
  id: undefined as number | undefined,
  title: '',
  content: '',
  display_position: 'top',
  start_time: '',
  end_time: '',
  is_enabled: true
})

const rules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入内容', trigger: 'blur' }],
  display_position: [{ required: true, message: '请选择位置', trigger: 'change' }]
}

function formatDate(date: string) {
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}

async function fetchList() {
  loading.value = true
  try {
    const res = await ContentAPI.getAnnouncements()
    list.value = res as any
  } finally {
    loading.value = false
  }
}

function resetForm() {
  form.id = undefined
  form.title = ''
  form.content = ''
  form.display_position = 'top'
  form.start_time = ''
  form.end_time = ''
  form.is_enabled = true
  dateRange.value = []
}

function handleAdd() {
  resetForm()
  dialog.title = '发布公告'
  dialog.isEdit = false
  dialog.visible = true
}

function handleEdit(row: Announcement) {
  resetForm()
  Object.assign(form, row)
  if (row.start_time && row.end_time) {
      dateRange.value = [row.start_time, row.end_time] as any
  }
  dialog.title = '编辑公告'
  dialog.isEdit = true
  dialog.visible = true
}

async function handleDelete(row: Announcement) {
  await ElMessageBox.confirm(`确认删除公告 "${row.title}" 吗?`, '警告', {
    type: 'warning'
  })
  try {
    await ContentAPI.deleteAnnouncement(row.id)
    ElMessage.success('删除成功')
    fetchList()
  } catch (error) {
    // handled
  }
}

async function handleSubmit() {
  if (!formRef.value) return
  await formRef.value.validate()
  
  if (dateRange.value && dateRange.value.length === 2) {
      form.start_time = dateRange.value[0]
      form.end_time = dateRange.value[1]
  } else {
      form.start_time = ''
      form.end_time = ''
  }

  try {
    if (dialog.isEdit && form.id) {
      await ContentAPI.updateAnnouncement(form.id, form)
      ElMessage.success('更新成功')
    } else {
      await ContentAPI.createAnnouncement(form)
      ElMessage.success('发布成功')
    }
    dialog.visible = false
    fetchList()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

onMounted(() => {
  fetchList()
})
</script>

<style scoped>
.mt-20 {
  margin-top: 20px;
}
</style>
