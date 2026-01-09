<template>
  <div class="app-container">
    <div class="filter-container">
      <el-button type="primary" icon="Plus" @click="handleAdd">新增角色</el-button>
    </div>

    <el-table v-loading="loading" :data="roleList" border style="width: 100%; margin-top: 20px;">
      <el-table-column prop="id" label="ID" width="80" align="center" sortable />
      <el-table-column prop="name" label="角色名称" width="180" sortable />
      <el-table-column prop="description" label="描述" min-width="200" />
      <el-table-column prop="is_system" label="类型" width="100" align="center">
        <template #default="{ row }">
          <el-tag :type="row.is_system ? 'warning' : 'info'">
            {{ row.is_system ? '系统' : '自定义' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template #default="{ row }">
          {{ new Date(row.created_at).toLocaleString() }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="250" align="center" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
          <el-button type="success" link @click="handlePermission(row)">权限设置</el-button>
          <el-button type="danger" link @click="handleDelete(row)" :disabled="row.is_system">删除</el-button>
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
        <el-form-item label="描述" prop="description">
          <el-input v-model="form.description" type="textarea" placeholder="角色描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">保存</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- Permission Setting Dialog -->
    <el-drawer
      v-model="permDrawerVisible"
      title="权限设置"
      size="450px"
    >
      <div style="margin-bottom: 20px;">
        <h3>正在为角色：{{ currentRole?.name }} 设置权限</h3>
      </div>
      <el-tree
        ref="treeRef"
        :data="permTreeData"
        show-checkbox
        node-key="id"
        :props="{ label: 'name' }"
        default-expand-all
      />
      <template #footer>
        <div style="flex: auto">
          <el-button @click="permDrawerVisible = false">取消</el-button>
          <el-button type="primary" :loading="saveLoading" @click="handleSavePerm">保存权限并应用</el-button>
        </div>
      </template>
    </el-drawer>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import LprAPI from '@/api/lpr-api'

const roleList = ref<any[]>([])
const loading = ref(false)

const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref<any>(null)
const form = reactive({
  id: undefined as number | undefined,
  name: '',
  description: '',
  is_system: false
})

const permDrawerVisible = ref(false)
const currentRole = ref<any>(null)
const treeRef = ref<any>(null)
const permTreeData = ref<any[]>([])
const saveLoading = ref(false)

async function fetchData() {
  loading.value = true
  try {
    const res = await LprAPI.getRoleList()
    roleList.value = res.list
  } catch (error) {
    console.error('获取角色列表失败', error)
  } finally {
    loading.value = false
  }
}

async function fetchPermTree() {
  try {
    const res = await LprAPI.getPermissionTree()
    permTreeData.value = res
  } catch (error) {
    console.error('获取权限树失败', error)
  }
}

function handleAdd() {
  isEdit.value = false
  Object.assign(form, { id: undefined, name: '', description: '', is_system: false })
  dialogVisible.value = true
}

function handleEdit(row: any) {
  isEdit.value = true
  Object.assign(form, {
    id: row.id,
    name: row.name,
    description: row.description,
    is_system: row.is_system
  })
  dialogVisible.value = true
}

async function handleDelete(row: any) {
  try {
    await ElMessageBox.confirm(`确认删除角色 "${row.name}" 吗？`, '提示', { type: 'warning' })
    await LprAPI.deleteRole(row.id)
    ElMessage.success('删除成功')
    fetchData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除角色失败', error)
    }
  }
}

async function handleSubmit() {
  if (!form.name) {
    ElMessage.warning('请填写角色名称')
    return
  }
  
  try {
    if (isEdit.value && form.id) {
      await LprAPI.updateRole(form.id, {
        name: form.name,
        description: form.description
      })
      ElMessage.success('更新成功')
    } else {
      await LprAPI.createRole({
        name: form.name,
        description: form.description,
        permission_ids: []
      })
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchData()
  } catch (error) {
    console.error('保存角色失败', error)
  }
}

async function handlePermission(row: any) {
  currentRole.value = row
  permDrawerVisible.value = true
  
  // Fetch tree if empty
  if (permTreeData.value.length === 0) {
    await fetchPermTree()
  }
  
  // Set checked nodes
  nextTick(() => {
    if (treeRef.value) {
      treeRef.value.setCheckedKeys(row.permission_ids || [])
    }
  })
}

async function handleSavePerm() {
  if (!currentRole.value) return
  
  saveLoading.value = true
  try {
    const keys = treeRef.value.getCheckedKeys()
    const halfKeys = treeRef.value.getHalfCheckedKeys()
    const allKeys = [...keys, ...halfKeys]
    
    await LprAPI.updateRole(currentRole.value.id, {
      permission_ids: allKeys
    })
    
    ElMessage.success('权限更新成功')
    permDrawerVisible.value = false
    fetchData()
  } catch (error) {
    console.error('保存权限失败', error)
  } finally {
    saveLoading.value = false
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.app-container { padding: 20px; }
.filter-container { margin-bottom: 20px; }
</style>
