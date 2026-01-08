<template>
  <div class="app-container">
    <div class="filter-container">
      <el-button type="primary" icon="Plus" @click="handleAdd">新增角色</el-button>
    </div>

    <el-table :data="roleList" border style="width: 100%; margin-top: 20px;">
      <el-table-column prop="id" label="ID" width="80" align="center" sortable />
      <el-table-column prop="name" label="角色名称" width="150" sortable />
      <el-table-column prop="code" label="角色标识" width="150" sortable />
      <el-table-column prop="description" label="描述" min-width="200" />
      <el-table-column prop="status" label="状态" width="100" align="center" sortable>
        <template #default="{ row }">
          <el-tag :type="row.status === 'active' ? 'success' : 'danger'">
            {{ row.status === 'active' ? '启用' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="250" align="center" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
          <el-button type="success" link @click="handlePermission(row)">权限设置</el-button>
          <el-button type="danger" link @click="handleDelete(row)" :disabled="row.code === 'super_admin'">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- Role Edit Dialog -->
    <el-dialog
      :title="isEdit ? '编辑角色' : '新增角色'"
      v-model="dialogVisible"
      width="500px"
    >
      <el-form ref="formRef" :model="form" label-width="80px">
        <el-form-item label="角色名称" prop="name" required>
          <el-input v-model="form.name" placeholder="请输入角色名称" />
        </el-form-item>
        <el-form-item label="角色标识" prop="code" required>
          <el-input v-model="form.code" placeholder="请输入角色标识 (e.g. admin)" :disabled="isEdit && form.code === 'super_admin'" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="form.description" type="textarea" placeholder="角色描述" />
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

    <!-- Permission Setting Dialog (Mock) -->
    <el-drawer
      v-model="permDrawerVisible"
      title="权限设置"
      size="400px"
    >
      <div style="margin-bottom: 20px;">
        <h3>正在为角色：{{ currentRole?.name }} 设置权限</h3>
      </div>
      <el-tree
        :data="permTreeData"
        show-checkbox
        node-key="id"
        :default-expanded-keys="[1, 2]"
        :default-checked-keys="[1, 2]"
      />
      <template #footer>
        <div style="flex: auto">
          <el-button @click="permDrawerVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSavePerm">保存权限</el-button>
        </div>
      </template>
    </el-drawer>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const roleList = ref([
  { id: 1, name: '超级管理员', code: 'super_admin', description: '拥有所有权限', status: 'active' },
  { id: 2, name: '用户管理员', code: 'user_manager', description: '管理用户和认证', status: 'active' },
  { id: 3, name: '运营专员', code: 'ops_manager', description: '负责内容和活动', status: 'active' }
])

const dialogVisible = ref(false)
const isEdit = ref(false)
const form = reactive({
  id: undefined,
  name: '',
  code: '',
  description: '',
  status: 'active'
})

const permDrawerVisible = ref(false)
const currentRole = ref<any>(null)
const permTreeData = [
  {
    id: 1,
    label: 'Dashboard',
    children: [{ id: 11, label: '概览' }]
  },
  {
    id: 2,
    label: '用户管理',
    children: [
      { id: 21, label: '用户列表' },
      { id: 22, label: '实名认证' }
    ]
  },
  {
    id: 3,
    label: '内容管理',
    children: [
      { id: 31, label: '文章管理' },
      { id: 32, label: '公告管理' }
    ]
  }
]

function handleAdd() {
  isEdit.value = false
  Object.assign(form, { id: undefined, name: '', code: '', description: '', status: 'active' })
  dialogVisible.value = true
}

function handleEdit(row: any) {
  isEdit.value = true
  Object.assign(form, row)
  dialogVisible.value = true
}

function handleDelete(row: any) {
  ElMessageBox.confirm('确认删除该角色吗？', '提示', { type: 'warning' }).then(() => {
    roleList.value = roleList.value.filter(item => item.id !== row.id)
    ElMessage.success('删除成功')
  })
}

function handleSubmit() {
  if (!form.name || !form.code) {
    ElMessage.warning('请填写必填项')
    return
  }
  
  if (isEdit.value) {
    const index = roleList.value.findIndex((item: any) => item.id === form.id)
    if (index !== -1) {
      roleList.value[index] = { ...form } as any
    }
    ElMessage.success('更新成功')
  } else {
    roleList.value.push({ ...form, id: Date.now() } as any)
    ElMessage.success('创建成功')
  }
  dialogVisible.value = false
}

function handlePermission(row: any) {
  currentRole.value = row
  permDrawerVisible.value = true
}

function handleSavePerm() {
  ElMessage.success('权限设置已保存')
  permDrawerVisible.value = false
}
</script>

<style scoped>
.app-container { padding: 20px; }
.filter-container { margin-bottom: 20px; }
</style>
