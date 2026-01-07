<template>
  <div class="app-container">
    <div class="search-container">
       <el-select v-model="currDocType" placeholder="文档类型" @change="handleTypeChange" style="width: 200px; margin-right: 10px;">
          <el-option label="全部" value="" />
          <el-option label="技术文档" value="tech" />
          <el-option label="服务协议" value="service_agreement" />
          <el-option label="隐私政策" value="privacy_policy" />
       </el-select>
       <el-button type="primary" icon="Plus" @click="handleAdd">新增文档</el-button>
    </div>

    <el-card shadow="never" class="mt-20">
      <el-table v-loading="loading" :data="list" border highlight-current-row>
        <el-table-column label="ID" prop="id" width="80" align="center" />
        <el-table-column label="标题" prop="title" />
        <el-table-column label="类型" width="120" align="center">
           <template #default="{ row }">
              <el-tag>{{ formatType(row.doc_type) }}</el-tag>
           </template>
        </el-table-column>
        <el-table-column label="版本" prop="version" width="100" align="center" />
        <el-table-column label="当前版本" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="row.is_current ? 'success' : 'info'">
              {{ row.is_current ? '是' : '否' }}
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
      width="800px"
      :close-on-click-modal="false"
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入标题" />
        </el-form-item>
        <el-form-item label="类型" prop="doc_type">
           <el-select v-model="form.doc_type">
              <el-option label="技术文档" value="tech" />
              <el-option label="服务协议" value="service_agreement" />
              <el-option label="隐私政策" value="privacy_policy" />
           </el-select>
        </el-form-item>
        <el-form-item label="版本号" prop="version">
          <el-input v-model="form.version" placeholder="v1.0" />
        </el-form-item>
         <el-form-item label="当前版本" prop="is_current">
          <el-switch v-model="form.is_current" active-text="设为当前生效版本" />
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <el-input 
            v-model="form.content" 
            type="textarea" 
            :rows="15" 
            placeholder="支持 Markdown 格式" 
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
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import ContentAPI, { type Document } from '@/api/content-api'
import dayjs from 'dayjs'

const loading = ref(false)
const list = ref<Document[]>([])
const currDocType = ref('')

const dialog = reactive({
  visible: false,
  title: '',
  isEdit: false
})

const formRef = ref()
const form = reactive({
  id: undefined as number | undefined,
  title: '',
  doc_type: 'tech',
  content: '',
  version: '',
  is_current: false
})

const rules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  doc_type: [{ required: true, message: '请选择类型', trigger: 'change' }],
  version: [{ required: true, message: '请输入版本', trigger: 'blur' }],
  content: [{ required: true, message: '请输入内容', trigger: 'blur' }]
}

function formatDate(date: string) {
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}

function formatType(type: string) {
  const map: any = {
    'tech': '技术文档',
    'service_agreement': '服务协议',
    'privacy_policy': '隐私政策'
  }
  return map[type] || type
}

async function fetchList() {
  loading.value = true
  try {
    const params = currDocType.value ? { doc_type: currDocType.value } : {}
    const res = await ContentAPI.getDocuments(params)
    list.value = res as any
  } finally {
    loading.value = false
  }
}

function handleTypeChange() {
  fetchList()
}

function resetForm() {
  form.id = undefined
  form.title = ''
  form.doc_type = 'tech'
  form.content = ''
  form.version = ''
  form.is_current = false
}

function handleAdd() {
  resetForm()
  dialog.title = '新增文档'
  dialog.isEdit = false
  dialog.visible = true
}

function handleEdit(row: Document) {
  resetForm()
  Object.assign(form, row)
  dialog.title = '编辑文档'
  dialog.isEdit = true
  dialog.visible = true
}

async function handleDelete(row: Document) {
  await ElMessageBox.confirm(`确认删除文档 "${row.title}" 吗?`, '警告', {
    type: 'warning'
  })
  try {
    await ContentAPI.deleteDocument(row.id)
    ElMessage.success('删除成功')
    fetchList()
  } catch (error) {
    // handled
  }
}

async function handleSubmit() {
  if (!formRef.value) return
  await formRef.value.validate()
  
  try {
    if (dialog.isEdit && form.id) {
      await ContentAPI.updateDocument(form.id, form)
      ElMessage.success('更新成功')
    } else {
      await ContentAPI.createDocument(form)
      ElMessage.success('创建成功')
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
