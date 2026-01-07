<template>
  <div class="app-container">
    <el-tabs v-model="activeTab" @tab-change="handleTabChange">
      <el-tab-pane label="管理员列表" name="list">
        <el-card shadow="never">
          <template #header>
            <div class="flex justify-between items-center">
               <span>管理员列表</span>
               <el-button type="primary" icon="Plus" @click="handleAdd">新增管理员</el-button>
            </div>
          </template>
          
          <el-table v-loading="loading" :data="adminList" border>
            <el-table-column label="ID" prop="id" width="80" align="center" />
            <el-table-column label="头像" width="80" align="center">
              <template #default="scope">
                <el-avatar :size="40" :src="scope.row.avatar_url || ''" >{{ scope.row.nickname?.charAt(0) }}</el-avatar>
              </template>
            </el-table-column>
            <el-table-column label="昵称" prop="nickname" width="150" />
            <el-table-column label="手机号" prop="phone" width="120" />
            <el-table-column label="所属角色" min-width="200">
              <template #default="scope">
                <el-tag 
                  v-for="role in scope.row.roles" 
                  :key="role.id" 
                  size="small" 
                  class="mr-1"
                  type="info"
                  effect="plain"
                >
                  {{ role.name }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="上次登录时间" prop="last_login_at" width="180">
               <template #default="{ row }">
                 {{ row.last_login_at ? formatDate(row.last_login_at) : '-' }}
               </template>
            </el-table-column>
            <el-table-column label="状态" width="100" align="center">
              <template #default="scope">
                <el-tag :type="scope.row.status === 'active' ? 'success' : 'danger'">
                  {{ scope.row.status === 'active' ? '正常' : '封禁' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200" align="center">
              <template #default="scope">
                <el-button type="primary" link icon="Edit" @click="handleEdit(scope.row)">修改</el-button>
                <el-button 
                   type="danger" 
                   link 
                   icon="Delete" 
                   @click="handleDelete(scope.row)"
                   :disabled="scope.row.id === 1" 
                >删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          
          <div class="pagination-container">
            <el-pagination
              v-model:current-page="adminParams.page"
              v-model:page-size="adminParams.pageSize"
              :total="adminTotal"
              :page-sizes="[10, 20, 50]"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="fetchAdmins"
              @current-change="fetchAdmins"
            />
          </div>
        </el-card>
      </el-tab-pane>

      <el-tab-pane label="敏感操作审计" name="audit">
        <el-card shadow="never">
          <div class="search-container mb-4">
             <el-form :inline="true">
                <el-form-item label="模块">
                   <el-input v-model="logParams.module" placeholder="功能模块" clearable @change="fetchLogs" />
                </el-form-item>
                <el-form-item>
                   <el-button type="primary" @click="fetchLogs">查询</el-button>
                </el-form-item>
             </el-form>
          </div>
          
          <el-table v-loading="logLoading" :data="logList" border>
            <el-table-column label="ID" prop="id" width="80" align="center" />
            <el-table-column label="操作人" prop="admin_username" width="120" />
            <el-table-column label="模块" prop="module" width="120" />
            <el-table-column label="类型" prop="action" width="100" />
            <el-table-column label="描述" prop="description" show-overflow-tooltip/>
            <el-table-column label="IP" prop="ip_address" width="140" />
            <el-table-column label="状态" width="80" align="center">
               <template #default="{ row }">
                  <el-tag :type="row.status === 200 ? 'success' : 'danger'">{{ row.status }}</el-tag>
               </template>
            </el-table-column>
            <el-table-column label="时间" prop="created_at" width="180">
              <template #default="{ row }">
                 {{ formatDate(row.created_at) }}
              </template>
            </el-table-column>
          </el-table>
          
          <div class="pagination-container">
            <el-pagination
              v-model:current-page="logParams.page"
              v-model:page-size="logParams.pageSize"
              :total="logTotal"
              :page-sizes="[10, 20, 50]"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="fetchLogs"
              @current-change="fetchLogs"
            />
          </div>
        </el-card>
      </el-tab-pane>
    </el-tabs>
    
    <!-- 管理员表单 -->
    <el-dialog 
      v-model="dialog.visible" 
      :title="dialog.title" 
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="昵称" prop="nickname">
          <el-input v-model="form.nickname" placeholder="管理员昵称" />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="form.phone" placeholder="手机号" maxlength="11" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="邮箱" />
        </el-form-item>
        <el-form-item v-if="!dialog.isEdit" label="密码" prop="password">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>
        <el-form-item label="角色" prop="role_ids">
          <el-select v-model="form.role_ids" multiple placeholder="请选择角色" style="width: 100%">
             <el-option 
               v-for="role in allRoles" 
               :key="role.id" 
               :label="role.name" 
               :value="role.id" 
             />
          </el-select>
        </el-form-item>
        <el-form-item v-if="dialog.isEdit" label="状态" prop="status">
           <el-radio-group v-model="form.status">
              <el-radio label="active">正常</el-radio>
              <el-radio label="banned">封禁</el-radio>
           </el-radio-group>
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
import type { User } from '@/types/lpr'
import UserAPI from '@/api/user-api'
import PermAPI, { type Role } from '@/api/perm-api'
import SystemAPI, { type OperationLog } from '@/api/system-api'
import dayjs from 'dayjs'

const activeTab = ref('list')
const loading = ref(false)
const logLoading = ref(false)

// Admin List Data
const adminList = ref<User[]>([])
const adminTotal = ref(0)
const adminParams = reactive({
  page: 1,
  pageSize: 10,
  user_type: 'admin' as any // 强制查询 admin
})

// Log Data
const logList = ref<OperationLog[]>([])
const logTotal = ref(0)
const logParams = reactive({
  page: 1,
  pageSize: 10,
  module: '',
  admin_id: undefined
})

// Roles
const allRoles = ref<Role[]>([])

// Dialog
const dialog = reactive({
  visible: false,
  title: '',
  isEdit: false
})
const formRef = ref()
const form = reactive({
  id: undefined as number | undefined,
  nickname: '',
  phone: '',
  email: '',
  password: '',
  role_ids: [] as number[],
  status: 'active'
})

const rules = {
  nickname: [{ required: true, message: '请输入昵称', trigger: 'blur' }],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '手机号格式不正确', trigger: 'blur' }
  ],
  password: [{ required: true, message: '请输入密码', trigger: 'blur', min: 6 }]
}

function formatDate(date: string) {
  return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
}

async function fetchAdmins() {
  loading.value = true
  try {
    const res = await UserAPI.getUserList(adminParams)
    adminList.value = res.list
    adminTotal.value = res.total
  } finally {
    loading.value = false
  }
}

async function fetchLogs() {
  logLoading.value = true
  try {
    const res = await SystemAPI.getLogs({
        page: logParams.page,
        page_size: logParams.pageSize,
        module: logParams.module
    })
    logList.value = res.list
    logTotal.value = res.total
  } finally {
    logLoading.value = false
  }
}

async function fetchRoles() {
    try {
        const res = await PermAPI.getAllRoles()
        allRoles.value = res
    } catch(e) {
        // quiet
    }
}

function handleTabChange(name: string) {
    if (name === 'list' && adminList.value.length === 0) {
        fetchAdmins()
    } else if (name === 'audit' && logList.value.length === 0) {
        fetchLogs()
    }
}

function resetForm() {
    form.id = undefined
    form.nickname = ''
    form.phone = ''
    form.email = ''
    form.password = ''
    form.role_ids = []
    form.status = 'active'
}

async function handleAdd() {
    resetForm()
    if (allRoles.value.length === 0) await fetchRoles()
    dialog.title = '新增管理员'
    dialog.isEdit = false
    dialog.visible = true
}

async function handleEdit(row: User) {
    resetForm()
    if (allRoles.value.length === 0) await fetchRoles()
    
    dialog.title = '编辑管理员'
    dialog.isEdit = true
    
    Object.assign(form, {
        id: row.id,
        nickname: row.nickname,
        phone: row.phone,
        email: row.email,
        status: row.status,
        role_ids: row.roles ? row.roles.map((r: any) => r.id) : []
    })
    dialog.visible = true
}

async function handleDelete(row: User) {
    await ElMessageBox.confirm(`确认删除管理员 "${row.nickname}" 吗?`, '警告', {
        type: 'warning'
    })
    try {
        await UserAPI.deleteUser(row.id)
        ElMessage.success('删除成功')
        fetchAdmins()
    } catch(e) {
        // handled
    }
}

async function handleSubmit() {
    if (!formRef.value) return
    // 如果是编辑模式，密码非必填，可以移除校验规则或暂时忽略
    // 这里简单处理：编辑时如果有值才校验，或者在 template 中 v-if 控制
    
    await formRef.value.validate()
    
    const data: any = {
        nickname: form.nickname,
        phone: form.phone,
        email: form.email,
        user_type: 'admin',
        role_ids: form.role_ids
    }
    
    try {
        if (dialog.isEdit && form.id) {
            data.status = form.status
            await UserAPI.updateUser(form.id, data)
            ElMessage.success('更新成功')
        } else {
            data.password = form.password
            await UserAPI.createUser(data)
            ElMessage.success('创建成功')
        }
        dialog.visible = false
        fetchAdmins()
    } catch(e) {
        ElMessage.error('操作失败')
    }
}

onMounted(() => {
    fetchAdmins()
})
</script>

<style scoped>
.mr-1 { margin-right: 4px; }
.pagination-container {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
}
.flex { display: flex; }
.justify-between { justify-content: space-between; }
.items-center { align-items: center; }
.mb-4 { margin-bottom: 1rem; }
</style>
