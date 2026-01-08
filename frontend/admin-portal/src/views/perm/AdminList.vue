<template>
  <div class="app-container">
    <div class="filter-container">
      <el-button type="primary" icon="Plus" @click="handleAdd">新增管理员</el-button>
    </div>

    <el-table :data="adminList" border style="width: 100%; margin-top: 20px;">
      <el-table-column prop="id" label="ID" width="80" align="center" sortable />
      <el-table-column prop="username" label="用户名" width="150" sortable />
      <el-table-column prop="nickname" label="昵称" width="150" sortable />
      <el-table-column label="角色" min-width="200">
        <template #default="{ row }">
          <el-tag v-for="role in row.roles" :key="role" style="margin-right: 5px;">{{ role }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="100" align="center" sortable>
        <template #default="{ row }">
          <el-tag :type="row.status === 'active' ? 'success' : 'danger'">
            {{ row.status === 'active' ? '正常' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="last_login" label="最后登录" width="180" align="center" sortable />
      <el-table-column label="操作" width="200" align="center" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
          <el-button type="warning" link @click="handleResetPwd(row)">重置密码</el-button>
          <el-button type="danger" link @click="handleDelete(row)" :disabled="row.username === 'admin'">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog
      :title="isEdit ? '编辑管理员' : '新增管理员'"
      v-model="dialogVisible"
      width="500px"
    >
      <el-form ref="formRef" :model="form" label-width="100px">
        <el-form-item label="用户名" prop="username" required>
          <el-input v-model="form.username" :disabled="isEdit" placeholder="登录账号" />
        </el-form-item>
        <el-form-item label="昵称" prop="nickname" required>
          <el-input v-model="form.nickname" placeholder="显示名称" />
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="!isEdit" required>
          <el-input v-model="form.password" type="password" show-password placeholder="初始密码" />
        </el-form-item>
        <el-form-item label="角色" prop="roles">
          <el-select v-model="form.roles" multiple placeholder="请选择角色" style="width: 100%">
            <el-option label="超级管理员" value="super_admin" />
            <el-option label="用户管理员" value="user_manager" />
            <el-option label="运营专员" value="ops_manager" />
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
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const adminList = ref([
  { id: 1, username: 'admin', nickname: '系统管理员', roles: ['super_admin'], status: 'active', last_login: '2025-01-08 12:00:00' },
  { id: 2, username: 'ops_user', nickname: '运营小王', roles: ['ops_manager'], status: 'active', last_login: '2025-01-07 09:30:00' }
])

const dialogVisible = ref(false)
const isEdit = ref(false)
const form = reactive({
  id: undefined,
  username: '',
  nickname: '',
  password: '',
  roles: [],
  status: 'active'
})

function handleAdd() {
  isEdit.value = false
  Object.assign(form, { id: undefined, username: '', nickname: '', password: '', roles: [], status: 'active' })
  dialogVisible.value = true
}

function handleEdit(row: any) {
  isEdit.value = true
  Object.assign(form, { ...row, password: '' }) // Don't fill password
  dialogVisible.value = true
}

function handleDelete(row: any) {
  ElMessageBox.confirm('确认删除该管理员吗？', '提示', { type: 'warning' }).then(() => {
    adminList.value = adminList.value.filter(item => item.id !== row.id)
    ElMessage.success('删除成功')
  })
}

function handleResetPwd(row: any) {
  ElMessageBox.prompt('请输入新密码', '重置密码', {
    inputType: 'password',
    inputPattern: /.{6,}/,
    inputErrorMessage: '密码长度至少6位'
  }).then(({ value }) => {
    ElMessage.success('密码重置成功')
  }).catch(() => {})
}

function handleSubmit() {
  if (!form.username || !form.nickname) {
    ElMessage.warning('请填写必填项')
    return
  }
  
  if (isEdit.value) {
    const index = adminList.value.findIndex((item: any) => item.id === form.id)
    if (index !== -1) {
      adminList.value[index] = { ...adminList.value[index], ...form } as any
    }
    ElMessage.success('更新成功')
  } else {
    adminList.value.push({ ...form, id: Date.now(), last_login: '-' } as any)
    ElMessage.success('创建成功')
  }
  dialogVisible.value = false
}
</script>

<style scoped>
.app-container { padding: 20px; }
.filter-container { margin-bottom: 20px; }
</style>
