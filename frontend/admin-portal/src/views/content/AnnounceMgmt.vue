<template>
  <div class="app-container">
    <div class="filter-container">
      <el-button type="primary" icon="Plus" @click="handleAdd">新增公告</el-button>
    </div>

    <el-table :data="announceList" border style="width: 100%; margin-top: 20px;">
      <el-table-column prop="id" label="ID" width="80" align="center" sortable />
      <el-table-column prop="title" label="标题" min-width="200" sortable />
      <el-table-column prop="type" label="类型" width="100" align="center" sortable>
        <template #default="{ row }">
          <el-tag :type="getTypeTag(row.type)">{{ typeMap[row.type] || row.type }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="100" align="center" sortable>
        <template #default="{ row }">
          <el-tag :type="row.status === 'published' ? 'success' : 'info'">
            {{ row.status === 'published' ? '已发布' : '草稿' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="160" align="center" sortable />
      <el-table-column label="操作" width="200" align="center" fixed="right">
        <template #default="{ row }">
          <el-button v-if="row.status === 'draft'" type="success" link @click="handlePublish(row)">发布</el-button>
          <el-button v-else type="warning" link @click="handleRevoke(row)">撤回</el-button>
          <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
          <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog
      :title="isEdit ? '编辑公告' : '新增公告'"
      v-model="dialogVisible"
      width="600px"
    >
      <el-form ref="formRef" :model="form" label-width="80px">
        <el-form-item label="标题" prop="title" required>
          <el-input v-model="form.title" placeholder="请输入公告标题" />
        </el-form-item>
        <el-form-item label="类型" prop="type" required>
          <el-select v-model="form.type" placeholder="请选择类型">
            <el-option label="系统通知" value="system" />
            <el-option label="活动通知" value="activity" />
            <el-option label="维护通知" value="maintenance" />
          </el-select>
        </el-form-item>
        <el-form-item label="内容" prop="content" required>
          <el-input
            v-model="form.content"
            type="textarea"
            :rows="5"
            placeholder="请输入公告内容"
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
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import dayjs from 'dayjs'

const typeMap: Record<string, string> = {
  system: '系统通知',
  activity: '活动通知',
  maintenance: '维护通知'
}

const announceList = ref([
  { id: 1, title: '系统升级通知 v1.2', type: 'system', status: 'published', content: '系统将于今晚进行升级...', created_at: '2025-01-08' },
  { id: 2, title: '春节放假安排', type: 'activity', status: 'draft', content: '春节期间服务安排...', created_at: '2025-01-09' }
])

const dialogVisible = ref(false)
const isEdit = ref(false)
const form = reactive({
  id: undefined,
  title: '',
  type: 'system',
  content: '',
  status: 'draft'
})

function getTypeTag(type: string) {
  const map: any = { system: 'primary', activity: 'warning', maintenance: 'danger' }
  return map[type] || 'info'
}

function handleAdd() {
  isEdit.value = false
  Object.assign(form, { id: undefined, title: '', type: 'system', content: '', status: 'draft' })
  dialogVisible.value = true
}

function handleEdit(row: any) {
  isEdit.value = true
  Object.assign(form, row)
  dialogVisible.value = true
}

function handleDelete(row: any) {
  ElMessageBox.confirm('确认删除该公告吗？', '提示', { type: 'warning' }).then(() => {
    announceList.value = announceList.value.filter(item => item.id !== row.id)
    ElMessage.success('删除成功')
  })
}

function handlePublish(row: any) {
  row.status = 'published'
  ElMessage.success('发布成功')
}

function handleRevoke(row: any) {
  row.status = 'draft'
  ElMessage.warning('已撤回')
}

function handleSubmit() {
  if (!form.title || !form.content) {
    ElMessage.warning('请填写完整信息')
    return
  }
  
  if (isEdit.value) {
    const index = announceList.value.findIndex((item: any) => item.id === form.id)
    if (index !== -1) {
      announceList.value[index] = { ...form, created_at: announceList.value[index].created_at } as any
    }
    ElMessage.success('更新成功')
  } else {
    announceList.value.push({ ...form, id: Date.now(), created_at: dayjs().format('YYYY-MM-DD') } as any)
    ElMessage.success('创建成功')
  }
  dialogVisible.value = false
}
</script>

<style scoped>
.app-container { padding: 20px; }
.filter-container { margin-bottom: 20px; }
</style>
