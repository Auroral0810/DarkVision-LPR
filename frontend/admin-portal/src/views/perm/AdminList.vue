<template>
  <div class="app-container">
    <div class="filter-container">
      <el-button type="primary" icon="Plus" @click="handleAdd">新增管理员</el-button>
    </div>

    <el-table v-loading="loading" :data="adminList" border style="width: 100%; margin-top: 20px;">
      <el-table-column prop="id" label="ID" width="80" align="center" sortable />
      <el-table-column prop="phone" label="手机号/账号" width="150" sortable />
      <el-table-column prop="nickname" label="昵称" width="150" sortable />
      <el-table-column label="角色" min-width="200">
        <template #default="{ row }">
          <el-tag v-for="role in row.roles" :key="role.id" style="margin-right: 5px;">{{ role.name }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="100" align="center" sortable>
        <template #default="{ row }">
          <el-tag :type="row.status === 'active' ? 'success' : 'danger'">
            {{ row.status === 'active' ? '正常' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="last_login_at" label="最后登录" width="180" align="center" sortable>
        <template #default="{ row }">
          {{ row.last_login_at ? new Date(row.last_login_at).toLocaleString() : '-' }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" align="center" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
          <el-button type="warning" link @click="handleResetPwd(row)">重置密码</el-button>
          <el-button type="danger" link @click="handleDelete(row)" :disabled="row.id === 1">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog
      :title="isEdit ? '编辑管理员' : '新增管理员'"
      v-model="dialogVisible"
      width="500px"
    >
      <el-form ref="formRef" :model="form" label-width="100px">
        <el-form-item label="手机号" prop="phone" required>
          <el-input v-model="form.phone" placeholder="作为登录账号" />
        </el-form-item>
        <el-form-item label="昵称" prop="nickname" required>
          <el-input v-model="form.nickname" placeholder="显示名称" />
        </el-form-item>
        <el-form-item label="真实姓名" prop="real_name">
          <el-input v-model="form.real_name" placeholder="选填" />
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="!isEdit" required>
          <el-input v-model="form.password" type="password" show-password placeholder="初始密码" />
        </el-form-item>
        <el-form-item label="角色" prop="role_ids">
          <el-select v-model="form.role_ids" multiple placeholder="请选择角色" style="width: 100%">
            <el-option 
              v-for="item in roleOptions" 
              :key="item.id" 
              :label="item.name" 
              :value="item.id" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-switch v-model="form.status" active-value="active" inactive-value="inactive" />
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
import { ElMessage, ElMessageBox } from 'element-plus'
import LprAPI from '@/api/lpr-api'

const adminList = ref<any[]>([])
const loading = ref(false)
const roleOptions = ref<any[]>([])

const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref<any>(null)
const form = reactive({
  id: undefined as number | undefined,
  phone: '',
  nickname: '',
  password: '',
  role_ids: [] as number[],
  status: 'active',
  real_name: ''
})

async function fetchRoles() {
  try {
    const res = await LprAPI.getRoleList()
    roleOptions.value = res.list
  } catch (error) {
    console.error('获取角色列表失败', error)
  }
}

async function fetchData() {
  loading.value = true
  try {
    const res = await LprAPI.getAdminUserList()
    adminList.value = res
  } catch (error) {
    console.error('获取管理员列表失败', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
  fetchRoles()
})

function handleAdd() {
  isEdit.value = false
  Object.assign(form, { id: undefined, phone: '', nickname: '', password: '', role_ids: [], status: 'active', real_name: '' })
  dialogVisible.value = true
}

function handleEdit(row: any) {
  isEdit.value = true
  Object.assign(form, {
    id: row.id,
    phone: row.phone,
    nickname: row.nickname,
    password: '', 
    role_ids: row.roles.map((r: any) => r.id),
    status: row.status,
    real_name: row.profile?.real_name || ''
  })
  dialogVisible.value = true
}

async function handleDelete(row: any) {
  try {
    await ElMessageBox.confirm(`确认删除管理员 "${row.nickname}" 吗？`, '提示', { type: 'warning' })
    // Use regular delete user API or specific admin delete if exists
    // admin_service.py doesn't have a specific delete_admin_user yet, uses user_type check?
    // Let's check AdminUser API again.
    // ... Actually, I can use banUser or deleteUser.
    await LprAPI.batchDeleteUsers([row.id])
    ElMessage.success('删除成功')
    fetchData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除管理员失败', error)
    }
  }
}

async function handleResetPwd(row: any) {
  try {
    const { value } = await ElMessageBox.prompt('请输入新密码', '重置密码', {
      inputType: 'password',
      inputPattern: /.{6,}/,
      inputErrorMessage: '密码长度至少6位'
    })
    
    await LprAPI.updateAdminUser(row.id, { password: value })
    ElMessage.success('密码重置成功')
  } catch (error) {
    if (error !== 'cancel') {
       console.error('重置密码失败', error)
    }
  }
}

async function handleSubmit() {
  if (!form.nickname || !form.phone || (!isEdit.value && !form.password)) {
    ElMessage.warning('请填写必填项')
    return
  }
  
  try {
    if (isEdit.value && form.id) {
      await LprAPI.updateAdminUser(form.id, {
        nickname: form.nickname,
        phone: form.phone,
        role_ids: form.role_ids,
        is_active: form.status === 'active'
      })
      ElMessage.success('更新成功')
    } else {
      await LprAPI.createAdminUser({
        nickname: form.nickname,
        phone: form.phone,
        password: form.password,
        role_ids: form.role_ids,
        real_name: form.real_name
      })
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchData()
  } catch (error) {
    console.error('保存管理员失败', error)
  }
}
</script>

<style scoped>
.app-container { padding: 20px; }
.filter-container { margin-bottom: 20px; }
</style>
