<template>
  <div class="version-update-container">
    <el-card v-loading="loading">
      <template #header>
        <div class="card-header">
          <span><el-icon><InfoFilled /></el-icon> 版本发布记录</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Promotion /></el-icon> 发布新版本
          </el-button>
        </div>
      </template>

      <el-timeline v-if="versions.length > 0">
        <el-timeline-item
          v-for="ver in versions"
          :key="ver.id"
          :timestamp="formatDate(ver.created_at)"
          placement="top"
          :type="ver.is_force ? 'danger' : 'primary'"
        >
          <el-card class="version-card">
            <template #header>
              <div class="version-header">
                <span class="version-num">{{ ver.version_number }}</span>
                <span class="version-title">{{ ver.title }}</span>
                <div class="version-tags">
                  <el-tag size="small">{{ getTypeText(ver.type) }}</el-tag>
                  <el-tag v-if="ver.is_force" size="small" type="danger">强制更新</el-tag>
                </div>
                <div class="version-actions">
                  <el-button type="primary" link @click="handleEdit(ver)">编辑</el-button>
                  <el-button type="danger" link @click="handleDelete(ver)">删除</el-button>
                </div>
              </div>
            </template>
            <div class="version-content">
              <pre>{{ ver.content }}</pre>
            </div>
            <div v-if="ver.download_url" class="version-footer">
              <el-link type="primary" :href="ver.download_url" target="_blank">
                <el-icon><Download /></el-icon> 下载地址
              </el-link>
            </div>
          </el-card>
        </el-timeline-item>
      </el-timeline>
      <el-empty v-else description="暂无版本记录" />

      <div class="pagination-container">
        <el-pagination
          v-model:current-page="page"
          v-model:page-size="pageSize"
          :total="total"
          layout="total, prev, pager, next"
          @current-change="fetchVersions"
        />
      </div>
    </el-card>

    <!-- 版本发布弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑版本信息' : '发布新版本'"
      width="600px"
    >
      <el-form :model="form" label-width="100px" ref="formRef" :rules="rules">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="版本号" prop="version_number">
              <el-input v-model="form.version_number" placeholder="e.g. v1.2.0" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="版本类型" prop="type">
              <el-select v-model="form.type" style="width: 100%">
                <el-option label="系统版本" value="system" />
                <el-option label="App端" value="app" />
                <el-option label="API 接口" value="api" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="版本标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入更新标题" />
        </el-form-item>
        
        <el-form-item label="更新内容" prop="content">
          <el-input v-model="form.content" type="textarea" :rows="6" placeholder="请输入更新日志..." />
        </el-form-item>

        <el-form-item label="下载链接" prop="download_url">
          <el-input v-model="form.download_url" placeholder="可选，安装包或补丁下载地址" />
        </el-form-item>

        <el-form-item label="强制更新" prop="is_force">
          <el-radio-group v-model="form.is_force">
            <el-radio :label="0">否</el-radio>
            <el-radio :label="1">是</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="handleSubmit">发布</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { maintenanceApi } from '@/api/maintenance'
import { ElMessage, ElMessageBox } from 'element-plus'
import { InfoFilled, Promotion, Download } from '@element-plus/icons-vue'
import dayjs from 'dayjs'

const loading = ref(false)
const submitLoading = ref(false)
const versions = ref<any[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)
const dialogVisible = ref(false)
const isEdit = ref(false)
const currentId = ref<number | null>(null)

const form = ref({
  version_number: '',
  title: '',
  content: '',
  type: 'system',
  is_force: 0,
  download_url: ''
})

const rules = {
  version_number: [{ required: true, message: '请输入版本号', trigger: 'blur' }],
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入更新内容', trigger: 'blur' }]
}

const fetchVersions = async () => {
  loading.value = true
  try {
    const res = await maintenanceApi.getVersions({
      page: page.value,
      page_size: pageSize.value
    })
    versions.value = res.list
    total.value = res.total
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  isEdit.value = false
  currentId.value = null
  form.value = {
    version_number: '',
    title: '',
    content: '',
    type: 'system',
    is_force: 0,
    download_url: ''
  }
  dialogVisible.value = true
}

const handleEdit = (ver: any) => {
  isEdit.value = true
  currentId.value = ver.id
  form.value = {
    version_number: ver.version_number,
    title: ver.title,
    content: ver.content,
    type: ver.type,
    is_force: ver.is_force,
    download_url: ver.download_url || ''
  }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  submitLoading.value = true
  try {
    if (isEdit.value && currentId.value) {
      await maintenanceApi.updateVersion(currentId.value, form.value)
      ElMessage.success('更新成功')
    } else {
      await maintenanceApi.createVersion(form.value)
      ElMessage.success('发布成功')
    }
    dialogVisible.value = false
    fetchVersions()
  } catch (error) {
    console.error(error)
  } finally {
    submitLoading.value = false
  }
}

const handleDelete = async (ver: any) => {
  try {
    await ElMessageBox.confirm(`确定删除版本 ${ver.version_number} 记录吗？`, '警告', { type: 'error' })
    await maintenanceApi.deleteVersion(ver.id)
    ElMessage.success('删除成功')
    fetchVersions()
  } catch (error) {}
}

const getTypeText = (type: string) => {
  const map: any = {
    system: '系统版本',
    app: 'App端',
    api: 'API接口'
  }
  return map[type] || type
}

const formatDate = (date: any) => {
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}

onMounted(() => {
  fetchVersions()
})
</script>

<style scoped>
.version-update-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.version-card {
  margin-bottom: 5px;
}

.version-header {
  display: flex;
  align-items: center;
  gap: 15px;
}

.version-num {
  font-size: 18px;
  font-weight: bold;
  color: #409eff;
}

.version-title {
  font-weight: bold;
}

.version-tags {
  display: flex;
  gap: 8px;
}

.version-actions {
  margin-left: auto;
}

.version-content pre {
  margin: 0;
  white-space: pre-wrap;
  font-family: inherit;
  color: #606266;
  line-height: 1.6;
}

.version-footer {
  margin-top: 15px;
  border-top: 1px dashed #ebeef5;
  padding-top: 10px;
}

.pagination-container {
  margin-top: 30px;
  display: flex;
  justify-content: center;
}
</style>
