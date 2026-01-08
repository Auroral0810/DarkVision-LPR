<template>
  <div class="app-container">
    <div class="filter-container">
      <el-button type="primary" icon="Plus" @click="handleAdd">新增公告</el-button>
    </div>

    <el-table
      v-loading="loading"
      :data="announcements"
      border
      style="width: 100%; margin-top: 20px;"
    >
      <el-table-column prop="id" label="ID" width="80" align="center" />
      <el-table-column prop="title" label="标题" min-width="200" />
      <el-table-column prop="display_position" label="显示位置" width="120" align="center">
        <template #default="{ row }">
          <el-tag>{{ positionMap[row.display_position] || row.display_position }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="is_enabled" label="状态" width="100" align="center">
        <template #default="{ row }">
          <el-tag :type="row.is_enabled ? 'success' : 'info'">
            {{ row.is_enabled ? '启用' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="start_time" label="开始时间" width="160" align="center" />
      <el-table-column prop="end_time" label="结束时间" width="160" align="center" />
      <el-table-column prop="created_at" label="创建时间" width="160" align="center" />
      <el-table-column label="操作" width="180" align="center" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
          <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- Dialog -->
    <el-dialog
      :title="isEdit ? '编辑公告' : '新增公告'"
      v-model="dialogVisible"
      width="600px"
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入公告标题" />
        </el-form-item>
        <el-form-item label="显示位置" prop="display_position">
          <el-select v-model="form.display_position" placeholder="请选择">
            <el-option label="弹窗 (Popup)" value="popup" />
            <el-option label="横幅 (Banner)" value="banner" />
            <el-option label="消息中心" value="message_center" />
          </el-select>
        </el-form-item>
        <el-form-item label="有效期" prop="timeRange">
          <el-date-picker
            v-model="timeRange"
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
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit" :loading="submitLoading">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useContentStore } from '@/store/modules/content-store'
import { storeToRefs } from 'pinia'
import { ElMessage, ElMessageBox } from 'element-plus'

const store = useContentStore()
const { announcements, loading } = storeToRefs(store)

const positionMap: Record<string, string> = {
  popup: '弹窗',
  banner: '横幅',
  message_center: '消息中心'
}

const dialogVisible = ref(false)
const submitLoading = ref(false)
const isEdit = ref(false)
const formRef = ref()

const form = ref({
  id: undefined,
  title: '',
  content: '',
  display_position: 'popup',
  is_enabled: true
})

const timeRange = ref([])

onMounted(() => {
  store.fetchAnnouncements()
})

const rules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入内容', trigger: 'blur' }],
  display_position: [{ required: true, message: '请选择位置', trigger: 'change' }]
}

function handleAdd() {
  isEdit.value = false
  form.value = {
    id: undefined,
    title: '',
    content: '',
    display_position: 'popup',
    is_enabled: true
  }
  timeRange.value = []
  dialogVisible.value = true
}

function handleEdit(row: any) {
  isEdit.value = true
  form.value = { ...row }
  timeRange.value = row.start_time && row.end_time ? [row.start_time, row.end_time] : []
  dialogVisible.value = true
}

function handleDelete(row: any) {
  ElMessageBox.confirm('确认删除该公告吗？', '提示', { type: 'warning' }).then(async () => {
    await store.deleteAnnouncement(row.id)
    ElMessage.success('删除成功')
  })
}

async function handleSubmit() {
  if (!formRef.value) return
  await formRef.value.validate(async (valid: boolean) => {
    if (valid) {
      submitLoading.value = true
      try {
        const payload = { ...form.value }
        if (timeRange.value && timeRange.value.length === 2) {
            payload.start_time = timeRange.value[0]
            payload.end_time = timeRange.value[1]
        } else {
            payload.start_time = null
            payload.end_time = null
        }

        if (isEdit.value) {
          await store.updateAnnouncement(form.value.id, payload)
          ElMessage.success('更新成功')
        } else {
          await store.createAnnouncement(payload)
          ElMessage.success('创建成功')
        }
        dialogVisible.value = false
      } catch (e) {
        // error handled in store or interceptor
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
