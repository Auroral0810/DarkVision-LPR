<template>
  <div class="app-container">
    <div class="filter-container">
      <el-button type="primary" icon="Plus" @click="handleAdd">新增文档</el-button>
    </div>

    <el-table :data="docList" border style="width: 100%; margin-top: 20px;">
      <el-table-column prop="id" label="ID" width="80" align="center" sortable />
      <el-table-column prop="title" label="文档标题" min-width="200" sortable />
      <el-table-column prop="doc_type" label="分类" width="120" align="center" sortable>
        <template #default="{ row }">
          <el-tag>{{ categoryMap[row.doc_type] || row.doc_type }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="version" label="版本" width="100" align="center" sortable />
      <el-table-column prop="updated_at" label="最后更新" width="160" align="center" sortable />
      <el-table-column label="操作" width="180" align="center" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
          <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog
      :title="isEdit ? '编辑文档' : '新增文档'"
      v-model="dialogVisible"
      width="800px"
    >
      <el-form ref="formRef" :model="form" label-width="100px">
        <el-form-item label="标题" prop="title" required>
          <el-input v-model="form.title" placeholder="请输入文档标题" />
        </el-form-item>
        <el-form-item label="分类" prop="doc_type" required>
          <el-select v-model="form.doc_type" placeholder="请选择分类">
            <el-option label="使用指南" value="guide" />
            <el-option label="API 文档" value="api" />
            <el-option label="常见问题" value="faq" />
            <el-option label="更新日志" value="changelog" />
          </el-select>
        </el-form-item>
        <el-form-item label="版本号" prop="version">
          <el-input v-model="form.version" placeholder="v1.0" />
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <el-input
            v-model="form.content"
            type="textarea"
            :rows="15"
            placeholder="请输入文档内容 (Markdown)"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useContentStore } from '@/store/modules/content-store'
import { storeToRefs } from 'pinia'
import { ElMessage, ElMessageBox } from 'element-plus'
import dayjs from 'dayjs'

const contentStore = useContentStore()
const { documents: docList, loading } = storeToRefs(contentStore)

const categoryMap: Record<string, string> = {
  guide: '使用指南',
  api: 'API 文档',
  faq: '常见问题',
  changelog: '更新日志'
}

const dialogVisible = ref(false)
const isEdit = ref(false)
const submitLoading = ref(false)
const form = reactive({
  id: undefined,
  title: '',
  doc_type: 'guide',
  version: '',
  content: '',
  is_current: true
})

function handleAdd() {
  isEdit.value = false
  Object.assign(form, { id: undefined, title: '', doc_type: 'guide', version: '', content: '', is_current: true })
  dialogVisible.value = true
}

function handleEdit(row: any) {
  isEdit.value = true
  Object.assign(form, { ...row })
  dialogVisible.value = true
}

function handleDelete(row: any) {
  ElMessageBox.confirm('确认删除该文档吗？', '提示', { type: 'warning' }).then(async () => {
    await contentStore.deleteDocument(row.id)
    ElMessage.success('删除成功')
  })
}

async function handleSubmit() {
  if (!form.title) {
    ElMessage.warning('请输入标题')
    return
  }
  
  submitLoading.value = true
  try {
    if (isEdit.value) {
      await contentStore.updateDocument(form.id!, { ...form })
      ElMessage.success('更新成功')
    } else {
      await contentStore.createDocument({ ...form })
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
  } catch (error) {
    console.error(error)
  } finally {
    submitLoading.value = false
  }
}

onMounted(() => {
  contentStore.fetchDocuments()
})
</script>

<style scoped>
.app-container { padding: 20px; }
.filter-container { margin-bottom: 20px; }
</style>
