<template>
  <div class="app-container">
    <el-card shadow="hover">
      <div class="header-actions" style="margin-bottom: 20px;">
        <el-button type="primary" icon="Plus" @click="handleAdd">新增管理员</el-button>
        <el-button icon="Refresh" @click="fetchData">刷新</el-button>
      </div>

      <el-table v-loading="loading" :data="adminUsers" border>
        <el-table-column prop="id" label="ID" width="80" align="center" />
        <el-table-column prop="nickname" label="昵称" width="150" />
        <el-table-column prop="phone" label="手机号" width="150" />
        <el-table-column label="角色" min-width="200">
          <template #default="{ row }">
            <el-tag v-for="role in row.roles" :key="role.id" style="margin-right: 5px;">
              {{ role.name }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
           <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'danger'">
              {{ row.status === 'active' ? '正常' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" align="center" />
        <el-table-column label="操作" width="200" align="center" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
            <el-button type="warning" link @click="handleResetPwd(row)">重置密码</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- Dialog -->
    <el-dialog
      :title="isEdit ? '编辑管理员' : '新增管理员'"
      v-model="dialogVisible"
      width="600px"
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="昵称" prop="nickname">
          <el-input v-model="form.nickname" placeholder="请输入昵称" />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入手机号" />
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="!isEdit">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>
        <el-form-item label="角色" prop="role_ids">
          <el-select v-model="form.role_ids" multiple placeholder="请选择角色" style="width: 100%">
            <el-option
              v-for="role in roles"
              :key="role.id"
              :label="role.name"
              :value="role.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="is_active" v-if="isEdit">
           <el-switch v-model="form.is_active" active-text="正常" inactive-text="禁用" />
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
import { ref, onMounted, reactive } from 'vue'
import { useAdminStore } from '@/store/modules/admin-store'
import { storeToRefs } from 'pinia'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/utils/request'

const store = useAdminStore()
const { adminUsers, roles, loading } = storeToRefs(store)

const dialogVisible = ref(false)
const submitLoading = ref(false)
const isEdit = ref(false)
const formRef = ref()

const form = reactive({
  id: undefined,
  nickname: '',
  phone: '',
  password: '',
  role_ids: [] as number[],
  is_active: true
})

const rules = {
  nickname: [{ required: true, message: '请输入昵称', trigger: 'blur' }],
  phone: [{ required: true, message: '请输入手机号', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  role_ids: [{ required: true, message: '请选择角色', trigger: 'change' }]
}

function fetchData() {
  store.fetchAdminUsers()
  store.fetchRoles() // Ensure we have roles for dropdown
}

onMounted(() => {
  fetchData()
})

function handleAdd() {
  isEdit.value = false
  form.id = undefined
  form.nickname = ''
  form.phone = ''
  form.password = ''
  form.role_ids = []
  form.is_active = true
  dialogVisible.value = true
}

function handleEdit(row: any) {
  isEdit.value = true
  form.id = row.id
  form.nickname = row.nickname
  form.phone = row.phone
  form.role_ids = row.roles.map((r: any) => r.id)
  form.is_active = row.status === 'active'
  dialogVisible.value = true
}

function handleResetPwd(row: any) {
    ElMessageBox.prompt('请输入新密码', '重置密码', {
        inputType: 'password',
        inputPattern: /.{6,}/,
        inputErrorMessage: '密码长度至少6位'
    }).then(async ({ value }) => {
        await request.put(`/api/admin/admin-users/${row.id}`, { password: value })
        ElMessage.success('密码已重置')
    }).catch(() => {})
}

async function handleSubmit() {
  if (!formRef.value) return
  await formRef.value.validate(async (valid: boolean) => {
    if (valid) {
      submitLoading.value = true
      try {
        if (isEdit.value) {
            await store.updateAdminUser(form.id!, {
                nickname: form.nickname,
                phone: form.phone,
                role_ids: form.role_ids,
                is_active: form.is_active
            })
            ElMessage.success('更新成功')
        } else {
            await store.createAdminUser({
                nickname: form.nickname,
                phone: form.phone,
                password: form.password,
                role_ids: form.role_ids
            })
            ElMessage.success('创建成功')
        }
        dialogVisible.value = false
      } catch (e) {
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
