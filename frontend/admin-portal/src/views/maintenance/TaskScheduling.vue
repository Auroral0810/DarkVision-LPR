<template>
  <div class="task-scheduling-container">
    <el-card v-loading="loading">
      <template #header>
        <div class="card-header">
          <span><el-icon><Calendar /></el-icon> 定时任务管理</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon> 添加任务
          </el-button>
        </div>
      </template>

      <el-table :data="tasks" style="width: 100%">
        <el-table-column prop="name" label="任务名称" min-width="150" />
        <el-table-column prop="task_code" label="任务代码" width="180" />
        <el-table-column prop="cron_expression" label="Cron 表达式" width="140" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'info'">
              {{ row.status === 1 ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="last_run_at" label="最后运行时间" width="170">
          <template #default="{ row }">
            {{ row.last_run_at ? formatDate(row.last_run_at) : '从未运行' }}
          </template>
        </el-table-column>
        <el-table-column prop="next_run_at" label="下次运行时间" width="170">
          <template #default="{ row }">
            {{ row.status === 1 ? formatDate(row.next_run_at) : '-' }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleRun(row)">立即执行</el-button>
            <el-button :type="row.status === 1 ? 'warning' : 'success'" link @click="handleToggle(row)">
              {{ row.status === 1 ? '暂时禁用' : '继续启用' }}
            </el-button>
            <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 任务编辑弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑任务' : '添加任务'"
      width="500px"
    >
      <el-form :model="form" label-width="100px" ref="formRef" :rules="rules">
        <el-form-item label="任务名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入任务名称" />
        </el-form-item>
        <el-form-item label="任务代码" prop="task_code">
          <el-input v-model="form.task_code" placeholder="请输入任务代码 (需要后端代码支持)" :disabled="isEdit" />
        </el-form-item>
        <el-form-item label="Cron 表达式" prop="cron_expression">
          <el-input v-model="form.cron_expression" placeholder="e.g. 0 1 * * *" />
          <div class="form-tip">分 小时 日 月 周 (5位 cron 表达式)</div>
        </el-form-item>
        <el-form-item label="任务备注" prop="remark">
          <el-input v-model="form.remark" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { maintenanceApi } from '@/api/maintenance'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Calendar, Plus } from '@element-plus/icons-vue'
import dayjs from 'dayjs'

const loading = ref(false)
const submitLoading = ref(false)
const tasks = ref<any[]>([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const currentId = ref<number | null>(null)

const form = ref({
  name: '',
  task_code: '',
  cron_expression: '',
  remark: ''
})

const rules = {
  name: [{ required: true, message: '请输入任务名称', trigger: 'blur' }],
  task_code: [{ required: true, message: '请输入任务代码', trigger: 'blur' }],
  cron_expression: [{ required: true, message: '请输入 Cron 表达式', trigger: 'blur' }]
}

const fetchTasks = async () => {
  loading.value = true
  try {
    const res = await maintenanceApi.getTasks()
    tasks.value = res
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
    name: '',
    task_code: '',
    cron_expression: '',
    remark: ''
  }
  dialogVisible.value = true
}

const handleEdit = (row: any) => {
  isEdit.value = true
  currentId.value = row.id
  form.value = {
    name: row.name,
    task_code: row.task_code,
    cron_expression: row.cron_expression,
    remark: row.remark || ''
  }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  submitLoading.value = true
  try {
    if (isEdit.value && currentId.value) {
      await maintenanceApi.updateTask(currentId.value, form.value)
      ElMessage.success('更新成功')
    } else {
      await maintenanceApi.createTask(form.value)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchTasks()
  } catch (error) {
    console.error(error)
  } finally {
    submitLoading.value = false
  }
}

const handleRun = async (row: any) => {
  try {
    await ElMessageBox.confirm(`确定立即执行任务: ${row.name} 吗？`, '提示')
    await maintenanceApi.runTask(row.id)
    ElMessage.success('指令下发成功')
    setTimeout(fetchTasks, 1000)
  } catch (error) { e => {} }
}

const handleToggle = async (row: any) => {
  try {
    await maintenanceApi.toggleTask(row.id)
    ElMessage.success(`${row.status === 1 ? '已禁用' : '已启用'}`)
    fetchTasks()
  } catch (error) {}
}

const handleDelete = async (row: any) => {
  try {
    await ElMessageBox.confirm('确定删除该任务吗？APScheduler 中也会同步移除。', '警告', { type: 'error' })
    await maintenanceApi.deleteTask(row.id)
    ElMessage.success('删除成功')
    fetchTasks()
  } catch (error) {}
}

const formatDate = (date: any) => {
  return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
}

onMounted(() => {
  fetchTasks()
})
</script>

<style scoped>
.task-scheduling-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}
</style>
