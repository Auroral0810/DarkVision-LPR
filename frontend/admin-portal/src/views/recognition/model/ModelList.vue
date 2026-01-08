<template>
  <div class="app-container">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>模型版本管理</span>
          <el-button type="primary" icon="Plus" @click="handleAdd">新增模型</el-button>
        </div>
      </template>

      <el-table v-loading="loading" :data="modelList" border stripe>
        <el-table-column prop="version" label="版本号" width="120" align="center" sortable />
        <el-table-column prop="name" label="模型名称" width="200" align="center" sortable />
        <el-table-column prop="accuracy" label="准确率" width="120" align="center" sortable>
          <template #default="scope">
            <span v-if="scope.row.accuracy">{{ scope.row.accuracy }}%</span>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column prop="is_active" label="当前线上" width="100" align="center" sortable>
          <template #default="scope">
            <el-tag :type="scope.row.is_active ? 'success' : 'info'">
              {{ scope.row.is_active ? '是' : '否' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
        <el-table-column prop="created_at" label="创建时间" width="180" align="center" sortable>
          <template #default="scope">
            {{ formatTime(scope.row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" align="center" fixed="right">
          <template #default="scope">
            <el-button
              type="primary"
              link
              icon="Edit"
              @click="handleEdit(scope.row)"
            >编辑</el-button>
            <el-button
              v-if="!scope.row.is_active"
              type="success"
              link
              icon="Check"
              @click="handleActivate(scope.row)"
            >启用</el-button>
            <el-button
              type="danger"
              link
              icon="Delete"
              @click="handleDelete(scope.row)"
            >删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 表单弹窗 -->
    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="500px" append-to-body>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="版本号" prop="version">
          <el-input v-model="form.version" placeholder="如: v1.2.0" :disabled="!!form.id" />
        </el-form-item>
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" placeholder="模型名称" />
        </el-form-item>
        <el-form-item label="准确率(%)" prop="accuracy">
          <el-input-number v-model="form.accuracy" :precision="2" :step="0.01" :min="0" :max="100" />
        </el-form-item>
        <el-form-item label="线上模型" prop="is_active">
          <el-switch v-model="form.is_active" />
        </el-form-item>
        <el-form-item label="权重路径" prop="file_path">
          <el-input v-model="form.file_path" placeholder="/models/lpr_v1.pth" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="form.description" type="textarea" placeholder="版本变更说明..." />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">确定</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getModels, createModel, updateModel, deleteModel, type RecognitionModel } from '@/api/recognition-api'
import dayjs from 'dayjs'

const loading = ref(false)
const modelList = ref<RecognitionModel[]>([])
const dialogVisible = ref(false)
const dialogTitle = ref('')
const formRef = ref()

const form = ref<any>({
  id: undefined,
  version: '',
  name: '',
  accuracy: undefined,
  is_active: false,
  file_path: '',
  description: ''
})

const rules = {
  version: [{ required: true, message: '请输入版本号', trigger: 'blur' }],
  name: [{ required: true, message: '请输入模型名称', trigger: 'blur' }]
}

const getList = async () => {
  loading.value = true
  try {
    const res: any = await getModels()
    modelList.value = res
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  form.value = {
    id: undefined,
    version: '',
    name: '',
    accuracy: undefined,
    is_active: false,
    file_path: '',
    description: ''
  }
  dialogTitle.value = '新增模型版本'
  dialogVisible.value = true
}

const handleEdit = (row: RecognitionModel) => {
  form.value = { ...row }
  dialogTitle.value = '编辑模型版本'
  dialogVisible.value = true
}

const submitForm = async () => {
  formRef.value.validate(async (valid: boolean) => {
    if (valid) {
      if (form.value.id) {
        await updateModel(form.value.id, form.value)
        ElMessage.success('更新成功')
      } else {
        await createModel(form.value)
        ElMessage.success('新增成功')
      }
      dialogVisible.value = false
      getList()
    }
  })
}

const handleActivate = (row: RecognitionModel) => {
  ElMessageBox.confirm('是否将版本 \"' + row.version + '\" 切换为当前线上运行版？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'info'
  }).then(async () => {
    await updateModel(row.id, { is_active: true })
    ElMessage.success('已切换线上版本')
    getList()
  }).catch(() => {})
}

const handleDelete = (row: RecognitionModel) => {
  if (row.is_active) {
    ElMessage.warning('线上运行中的模型不能删除')
    return
  }
  ElMessageBox.confirm('确定删除模型版本 \"' + row.version + '\" 吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    await deleteModel(row.id)
    ElMessage.success('删除成功')
    getList()
  }).catch(() => {})
}

const formatTime = (timeStr: string) => {
  if (!timeStr) return ''
  return dayjs(timeStr).format('YYYY-MM-DD HH:mm:ss')
}

onMounted(() => {
  getList()
})
</script>

<style scoped>
.app-container {
  padding: 20px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
