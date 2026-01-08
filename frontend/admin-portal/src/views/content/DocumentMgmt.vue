<template>
  <div class="app-container">
    <div class="filter-container">
      <el-button type="primary" icon="Plus" @click="handleAdd">新增文档</el-button>
    </div>

    <el-table
      v-loading="loading"
      :data="documents"
      border
      style="width: 100%; margin-top: 20px;"
    >
      <el-table-column prop="id" label="ID" width="80" align="center" sortable />
      <el-table-column prop="title" label="标题" min-width="200" sortable />
      <el-table-column prop="doc_type" label="类型" width="150" align="center" sortable>
        <template #default="{ row }">
            <el-tag>{{ typeMap[row.doc_type] || row.doc_type }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="version" label="版本" width="100" align="center" sortable />
      <el-table-column prop="is_current" label="当前版本" width="100" align="center" sortable>
        <template #default="{ row }">
          <el-tag :type="row.is_current ? 'success' : 'info'">
            {{ row.is_current ? '是' : '否' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="160" align="center" sortable />
      <el-table-column label="操作" width="180" align="center" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
          <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- Dialog -->
    <el-dialog
      :title="isEdit ? '编辑文档' : '新增文档'"
      v-model="dialogVisible"
      width="800px"
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入文档标题" />
        </el-form-item>
        <el-form-item label="类型" prop="doc_type">
          <el-select v-model="form.doc_type" placeholder="请选择类型">
            <el-option label="技术文档" value="tech" />
            <el-option label="服务协议" value="service_agreement" />
            <el-option label="隐私政策" value="privacy_policy" />
          </el-select>
        </el-form-item>
        <el-form-item label="版本号" prop="version">
          <el-input v-model="form.version" placeholder="e.g. v1.0" />
        </el-form-item>
        <el-form-item label="设为当前" prop="is_current">
          <el-switch v-model="form.is_current" active-text="是" inactive-text="否" />
          <span style="margin-left: 10px; color: #999; font-size: 12px;">(同类型旧版本将自动设为非当前)</span>
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <el-input
            v-model="form.content"
            type="textarea"
            :rows="15"
            placeholder="请输入文档内容 (Markdown or HTML)"
          />
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
import { ref, onMounted } from 'vue'
import { useContentStore } from '@/store/modules/content-store'
import { storeToRefs } from 'pinia'
import { ElMessage, ElMessageBox } from 'element-plus'

const store = useContentStore()
const { documents, loading } = storeToRefs(store)

const typeMap: Record<string, string> = {
    tech: '技术文档',
    service_agreement: '服务协议',
    privacy_policy: '隐私政策'
}

const dialogVisible = ref(false)
const submitLoading = ref(false)
const isEdit = ref(false)
const formRef = ref()

const form = ref({
  id: undefined,
  title: '',
  doc_type: 'tech',
  content: '',
  version: '',
  is_current: false
})

onMounted(() => {
  store.fetchDocuments()
})

const rules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  doc_type: [{ required: true, message: '请选择类型', trigger: 'change' }],
  version: [{ required: true, message: '请输入版本号', trigger: 'blur' }],
  content: [{ required: true, message: '请输入内容', trigger: 'blur' }]
}

function handleAdd() {
  isEdit.value = false
  form.value = {
    id: undefined,
    title: '',
    doc_type: 'tech',
    content: '',
    version: 'v1.0',
    is_current: true
  }
  dialogVisible.value = true
}

function handleEdit(row: any) {
  isEdit.value = true
  form.value = { ...row }
  dialogVisible.value = true
}

function handleDelete(row: any) {
  ElMessageBox.confirm('确认删除该文档吗？', '提示', { type: 'warning' }).then(async () => {
    await store.deleteDocument(row.id)
    ElMessage.success('删除成功')
  })
}

async function handleSubmit() {
  if (!formRef.value) return
  await formRef.value.validate(async (valid: boolean) => {
    if (valid) {
      submitLoading.value = true
      try {
        if (isEdit.value) {
          await store.updateDocument(form.value.id, form.value)
          ElMessage.success('更新成功')
        } else {
          await store.createDocument(form.value)
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
