<!-- LPR 用户管理 -->
<template>
  <div class="app-container">
    <!-- 搜索区域 -->
    <div class="search-container">
      <el-form ref="queryFormRef" :model="queryParams" :inline="true">
        <el-form-item label="关键字">
          <el-input
            v-model="queryParams.keyword"
            placeholder="手机号/昵称/邮箱"
            clearable
            @keyup.enter="handleQuery"
          />
        </el-form-item>

        <el-form-item label="用户类型">
          <el-select v-model="queryParams.user_type" placeholder="全部" clearable style="width: 150px">
            <el-option label="普通用户" value="free" />
            <el-option label="VIP" value="vip" />
            <el-option label="企业" value="enterprise" />
          </el-select>
        </el-form-item>

        <el-form-item label="状态">
          <el-select v-model="queryParams.status" placeholder="全部" clearable style="width: 150px">
            <el-option label="正常" value="active" />
            <el-option label="禁用" value="inactive" />
            <el-option label="封禁" value="banned" />
          </el-select>
        </el-form-item>

        <el-form-item label="注册时间">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="~"
            start-placeholder="开始时间"
            end-placeholder="截止时间"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
          <el-button icon="Refresh" @click="handleResetQuery">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 数据表格 -->
    <el-card>
      <div class="data-table__toolbar">
        <div>
          <el-button type="primary" icon="Plus" @click="handleAddUser">新增用户</el-button>
          <el-button type="success" icon="Upload" @click="handleImport">批量导入</el-button>
          <el-button type="danger" icon="Delete" :disabled="!hasSelection" @click="handleBatchDelete">
            批量删除
          </el-button>
          <el-button icon="Download" @click="handleExport">导出数据</el-button>
        </div>
      </div>

      <el-table
        v-loading="loading"
        :data="pageData"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="50" />
        <el-table-column label="ID" prop="id" width="80" />
        <el-table-column label="头像" width="80">
          <template #default="scope">
            <el-avatar :src="scope.row.avatar_url || '/default-avatar.png'" :size="40" />
          </template>
        </el-table-column>
        <el-table-column label="昵称" prop="nickname" min-width="120">
          <template #default="scope">
            <div class="nickname-cell" style="display: flex; align-items: center; gap: 8px;">
              <span>{{ scope.row.nickname }}</span>
              <el-tag v-if="scope.row.is_online" size="small" type="success" effect="light">在线</el-tag>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="手机号" prop="phone" width="130" />
        <el-table-column label="邮箱" prop="email" min-width="180" show-overflow-tooltip />
        <el-table-column label="用户类型" width="100">
          <template #default="scope">
            <el-tag :type="getUserTypeColor(scope.row.user_type)">
              {{ getUserTypeLabel(scope.row.user_type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="80">
          <template #default="scope">
            <el-tag :type="getStatusColor(scope.row.status)">
              {{ getStatusLabel(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="注册时间" prop="created_at" width="160" />
        <el-table-column label="最后登录" prop="last_login_at" width="160" />
        <el-table-column label="操作" fixed="right" width="300">
          <template #default="scope">
            <el-button type="primary" link size="small" @click="handleViewDetail(scope.row)">
              详情
            </el-button>
            <el-button type="warning" link size="small" @click="handleChangeType(scope.row)">
              改类型
            </el-button>
            <el-button
              v-if="scope.row.status !== 'banned'"
              type="danger"
              link
              size="small"
              @click="handleBan(scope.row)"
            >
              封禁
            </el-button>
            <el-button
              v-else
              type="success"
              link
              size="small"
              @click="handleUnban(scope.row.id)"
            >
              解封
            </el-button>
            <el-button type="info" link size="small" @click="handleResetPassword(scope.row)">
              重置密码
            </el-button>
            <el-button 
              v-if="scope.row.is_online" 
              type="danger" 
              link 
              size="small" 
              @click="handleForceLogout(scope.row)"
            >
              强制下线
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <pagination
        v-if="total > 0"
        v-model:total="total"
        v-model:page="queryParams.page"
        v-model:limit="queryParams.pageSize"
        @pagination="fetchUserList"
      />
    </el-card>

    <el-drawer v-model="detailDrawerVisible" title="用户详情" size="60%">
      <UserDetail v-if="detailDrawerVisible && currentUserId" :user-id="currentUserId" />
    </el-drawer>

    <!-- 封禁对话框 -->
    <el-dialog v-model="banDialogVisible" title="封禁用户" width="500px">
      <el-form :model="banForm" label-width="100px">
        <el-form-item label="封禁原因">
          <el-input v-model="banForm.reason" type="textarea" :rows="3" placeholder="请输入封禁原因" />
        </el-form-item>
        <el-form-item label="封禁时长">
          <el-radio-group v-model="banForm.duration">
            <el-radio label="temp">临时封禁</el-radio>
            <el-radio label="permanent">永久封禁</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item v-if="banForm.duration === 'temp'" label="解封时间">
          <el-date-picker
            v-model="banForm.banned_until"
            type="datetime"
            placeholder="选择解封时间"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="banDialogVisible = false">取消</el-button>
        <el-button type="danger" @click="handleConfirmBan">确定封禁</el-button>
      </template>
    </el-dialog>

    <!-- 修改类型对话框 -->
    <el-dialog v-model="typeDialogVisible" title="修改用户类型" width="400px">
      <el-form :model="typeForm" label-width="100px">
        <el-form-item label="新类型">
          <el-select v-model="typeForm.user_type">
            <el-option label="普通用户" value="free" />
            <el-option label="VIP" value="vip" />
            <el-option label="企业用户" value="enterprise" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="typeDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleConfirmChangeType">确定</el-button>
      </template>
    </el-dialog>

    <!-- 新增/编辑用户对话框 -->
    <el-dialog v-model="userFormVisible" :title="userForm.id ? '编辑用户' : '新增用户'" width="500px">
      <el-form :model="userForm" label-width="100px">
        <el-form-item label="昵称" required>
          <el-input v-model="userForm.nickname" placeholder="请输入昵称" />
        </el-form-item>
        <el-form-item label="手机号" required>
          <el-input v-model="userForm.phone" placeholder="请输入手机号" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="userForm.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="用户类型">
          <el-select v-model="userForm.user_type" style="width: 100%">
            <el-option label="普通用户" value="free" />
            <el-option label="VIP" value="vip" />
            <el-option label="企业用户" value="enterprise" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="!userForm.id" label="初始密码" required>
          <el-input v-model="userForm.password" type="password" show-password placeholder="请输入密码" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="userFormVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSaveUser">保存</el-button>
      </template>
    </el-dialog>

    <!-- 数据导入对话框 -->
    <el-dialog v-model="importVisible" title="批量导入用户" width="400px">
      <el-upload
        class="upload-demo"
        drag
        action="/api/v1/users/import"
        multiple
        :headers="uploadHeaders"
        :on-success="handleImportSuccess"
      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          将文件拖到此处，或<em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            请上传 .xlsx 或 .csv 文件，<el-link type="primary" :underline="false">下载模板</el-link>
          </div>
        </template>
      </el-upload>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import LprAPI from '@/api/lpr-api'
import type { User, UserListParams } from '@/types/lpr'
import UserDetail from './UserDetail.vue'

defineOptions({ name: 'UserManagement' })

// 查询参数
const queryParams = reactive<UserListParams>({
  page: 1,
  pageSize: 10
})

const dateRange = ref<string[]>([])
const pageData = ref<User[]>([])
const total = ref(0)
const loading = ref(false)

// 选中项
const selectedIds = ref<number[]>([])
const hasSelection = computed(() => selectedIds.value.length > 0)

// 抽屉/对话框状态
const detailDrawerVisible = ref(false)
const currentUserId = ref<number | null>(null)
const banDialogVisible = ref(false)
const typeDialogVisible = ref(false)

const banForm = reactive({
  user_id: 0,
  reason: '',
  duration: 'temp',
  banned_until: null as Date | null
})

const typeForm = reactive({
  user_id: 0,
  user_type: 'free'
})

const userFormVisible = ref(false)
const userForm = reactive({
  id: undefined as number | undefined,
  nickname: '',
  phone: '',
  email: '',
  user_type: 'free',
  password: ''
})

const importVisible = ref(false)
const uploadHeaders = { 'Authorization': 'Bearer ...' } // 实际应从 store 获取 token

// 获取用户列表
async function fetchUserList() {
  loading.value = true
  try {
    if (dateRange.value?.length === 2) {
      queryParams.start_date = dateRange.value[0]
      queryParams.end_date = dateRange.value[1]
    } else {
      queryParams.start_date = undefined
      queryParams.end_date = undefined
    }
    
    const data = await LprAPI.getUserList(queryParams)
    pageData.value = data.list
    total.value = data.total
  } catch (error) {
    ElMessage.error('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

function handleQuery() {
  queryParams.page = 1
  fetchUserList()
}

function handleResetQuery() {
  Object.assign(queryParams, { page: 1, pageSize: 10 })
  dateRange.value = []
  fetchUserList()
}

function handleSelectionChange(selection: User[]) {
  selectedIds.value = selection.map(item => item.id)
}

function handleViewDetail(row: User) {
  currentUserId.value = row.id
  detailDrawerVisible.value = true
}

function handleBan(row: User) {
  banForm.user_id = row.id
  banForm.reason = ''
  banForm.duration = 'temp'
  banForm.banned_until = null
  banDialogVisible.value = true
}

async function handleConfirmBan() {
  if (!banForm.reason) {
    ElMessage.warning('请输入封禁原因')
    return
  }
  
  try {
    await LprAPI.banUser({
      user_id: banForm.user_id,
      reason: banForm.reason,
      banned_until: banForm.duration === 'permanent' ? null : banForm.banned_until?.toISOString()
    })
    ElMessage.success('封禁成功')
    banDialogVisible.value = false
    fetchUserList()
  } catch (error) {
    ElMessage.error('封禁失败')
  }
}

async function handleUnban(userId: number) {
  try {
    await LprAPI.unbanUser(userId)
    ElMessage.success('解封成功')
    fetchUserList()
  } catch (error) {
    ElMessage.error('解封失败')
  }
}

function handleChangeType(row: User) {
  typeForm.user_id = row.id
  typeForm.user_type = row.user_type
  typeDialogVisible.value = true
}

async function handleConfirmChangeType() {
  try {
    await LprAPI.updateUserType(typeForm.user_id, typeForm.user_type as any)
    ElMessage.success('用户类型修改成功')
    typeDialogVisible.value = false
    fetchUserList()
  } catch (error) {
    ElMessage.error('修改失败')
  }
}

function handleAddUser() {
  Object.assign(userForm, { id: undefined, nickname: '', phone: '', email: '', user_type: 'free', password: '' })
  userFormVisible.value = true
}

async function handleSaveUser() {
  if (!userForm.nickname || !userForm.phone || (!userForm.id && !userForm.password)) {
    ElMessage.warning('请填写完整必填项')
    return
  }
  try {
    const data = { ...userForm }
    if (userForm.id) {
      await LprAPI.updateUser(userForm.id, data)
      ElMessage.success('修改成功')
    } else {
      await LprAPI.createUser(data)
      ElMessage.success('新增成功')
    }
    userFormVisible.value = false
    fetchUserList()
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

function handleImport() {
  importVisible.value = true
}

function handleImportSuccess() {
  ElMessage.success('导入成功')
  importVisible.value = false
  fetchUserList()
}

async function handleResetPassword(row: User) {
  ElMessageBox.confirm(`确认重置用户【${row.nickname}】的密码吗？`, '重置密码', {
    type: 'warning'
  }).then(async () => {
    try {
      const result = await LprAPI.resetUserPassword(row.id)
      ElMessageBox.alert(`新密码: ${result.new_password}`, '密码已重置', {
        confirmButtonText: '确定'
      })
    } catch (error) {
      ElMessage.error('重置密码失败')
    }
  }).catch(() => {})
}

async function handleForceLogout(row: User) {
  ElMessageBox.confirm(`确认强制用户【${row.nickname}】下线吗？其当前 Token 将失效。`, '强制下线', {
    type: 'warning'
  }).then(async () => {
    try {
      await LprAPI.forceLogout(row.id)
      ElMessage.success('已强制下线')
      fetchUserList()
    } catch (error) {
      ElMessage.error('强制下线失败')
    }
  }).catch(() => {})
}

async function handleBatchDelete() {
  ElMessageBox.confirm(`确认删除选中的 ${selectedIds.value.length} 个用户吗？`, '批量删除', {
    type: 'warning'
  }).then(async () => {
    try {
      await LprAPI.batchDeleteUsers(selectedIds.value)
      ElMessage.success('删除成功')
      fetchUserList()
    } catch (error) {
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

async function handleExport() {
  try {
    const res = await LprAPI.exportUsers(queryParams)
    // res is AxiosResponse if responseType is 'blob'
    const blob = res.data instanceof Blob ? res.data : new Blob([res.data], { type: 'text/csv' })
    
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `user_list_${new Date().getTime()}.csv`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } catch (error) {
    console.error('Export error:', error)
    ElMessage.error('导出失败')
  }
}

// 辅助函数
function getUserTypeLabel(type: string) {
  const map: Record<string, string> = {
    free: '普通',
    vip: 'VIP',
    enterprise: '企业'
  }
  return map[type] || type
}

function getUserTypeColor(type: string): "warning" | "success" | "info" | undefined {
  const map: Record<string, "warning" | "success" | "info" | undefined> = {
    free: undefined,
    vip: 'warning',
    enterprise: 'success'
  }
  return map[type]
}

function getStatusLabel(status: string) {
  const map: Record<string, string> = {
    active: '正常',
    inactive: '禁用',
    banned: '封禁'
  }
  return map[status] || status
}

function getStatusColor(status: string): "success" | "info" | "danger" | undefined {
  const map: Record<string, "success" | "info" | "danger" | undefined> = {
    active: 'success',
    inactive: 'info',
    banned: 'danger'
  }
  return map[status] || ''
}

onMounted(() => {
  fetchUserList()
})
</script>

<style scoped>
.nickname-cell {
  display: flex;
  align-items: center;
}
.ml-2 {
  margin-left: 8px;
}
</style>
