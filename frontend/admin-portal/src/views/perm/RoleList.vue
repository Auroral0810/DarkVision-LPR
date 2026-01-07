<template>
  <div class="app-container">
    <div class="search-container">
      <el-form :inline="true">
        <el-form-item label="角色名称">
          <el-input v-model="queryParams.keywords" placeholder="搜索角色名称" clearable @keyup.enter="handleQuery" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="Search" @click="handleQuery">查询</el-button>
          <el-button icon="Refresh" @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <el-card shadow="never">
      <template #header>
        <el-button type="success" icon="Plus" @click="handleAdd">新增角色</el-button>
      </template>

      <el-table v-loading="loading" :data="roleList" border highlight-current-row>
        <el-table-column label="ID" prop="id" width="80" align="center" />
        <el-table-column label="角色名称" prop="name" />
        <el-table-column label="描述" prop="description" />
        <el-table-column label="创建时间" prop="created_at" width="180">
           <template #default="{ row }">
             {{ formatDate(row.created_at) }}
           </template>
        </el-table-column>
        <el-table-column label="操作" width="250" align="center">
          <template #default="scope">
            <el-button type="primary" size="small" link icon="Edit" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button 
              type="danger" 
              size="small" 
              link 
              icon="Delete" 
              @click="handleDelete(scope.row)" 
              :disabled="scope.row.name === 'ROOT' || scope.row.id === 1"
            >删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 角色表单对话框 -->
    <el-dialog 
      v-model="dialog.visible" 
      :title="dialog.title" 
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="角色名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入角色名称" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="form.description" type="textarea" placeholder="请输入描述" />
        </el-form-item>
        <el-form-item label="权限分配">
          <div class="permission-tree-container">
             <el-input
               v-model="filterText"
               placeholder="输入关键字进行过滤"
               size="small"
               style="margin-bottom: 10px;"
             />
             <el-scrollbar max-height="300px">
                <el-tree
                  ref="permissionTreeRef"
                  :data="permissionTree"
                  show-checkbox
                  node-key="id"
                  :props="{ label: 'name', children: 'children' }"
                  :filte
                  r-node-method="filterNode"
                  default-expand-all
                />
             </el-scrollbar>
          </div>
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
import { ref, reactive, onMounted, nextTick, watch } from 'vue'
import { ElMessage, ElMessageBox, ElTree } from 'element-plus'
import PermAPI, { type Role, type Permission } from '@/api/perm-api'
import dayjs from 'dayjs'

const loading = ref(false)
const queryParams = reactive({
  keywords: ''
})

const roleList = ref<Role[]>([])
const permissionTree = ref<Permission[]>([])
const filterText = ref('')
const permissionTreeRef = ref<InstanceType<typeof ElTree>>()
const formRef = ref()

const dialog = reactive({
  visible: false,
  title: '',
  isEdit: false
})

const form = reactive({
  id: undefined as number | undefined,
  name: '',
  description: '',
  permission_ids: [] as number[]
})

const rules = {
  name: [{ required: true, message: '请输入角色名称', trigger: 'blur' }]
}

// 监听过滤输入
watch(filterText, (val) => {
  permissionTreeRef.value!.filter(val)
})

const filterNode = (value: string, data: any) => {
  if (!value) return true
  return data.name.includes(value)
}

function formatDate(date: string) {
  return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
}

// 将扁平列表转换为树形结构
function buildTree(items: Permission[], parentId: number | null = null): Permission[] {
  const tree: Permission[] = []
  for (const item of items) {
    if (item.parent_id === parentId) {
      const children = buildTree(items, item.id)
      if (children.length) {
        item.children = children
      }
      tree.push(item)
    }
  }
  return tree
}

async function fetchPermissions() {
  try {
    const res = await PermAPI.getPermissions()
    // 假设后端返回的是包含所有权限的扁平列表，如果已经是树形则不需要 buildTree
    // 根据之前的 API 实现，后端返回的是扁平列表
    // 但后端 API 注释里写了 get_permission_tree，但实现可能只是简单列表。
    // 如果是扁平列表，我们需要自己在前端构建树，或者依赖后端返回树。
    // 这里我们假设后端返回扁平列表，我们在前端构建树，这样更稳健。
    // 为了保险，先检查 res 是否有 children 属性，如果没有则构建
    if (res.length > 0 && !res[0].children && res.some(p => p.parent_id !== null)) {
         permissionTree.value = buildTree(res)
    } else {
         permissionTree.value = res
    }
  } catch (error) {
    console.error(error)
  }
}

async function fetchList() {
  loading.value = true
  try {
    const res = await PermAPI.getRoles()
    roleList.value = res.list
    if (queryParams.keywords) {
        roleList.value = roleList.value.filter(r => r.name.includes(queryParams.keywords))
    }
  } finally {
    loading.value = false
  }
}

function handleQuery() {
  fetchList()
}

function resetQuery() {
  queryParams.keywords = ''
  fetchList()
}

function resetForm() {
  form.id = undefined
  form.name = ''
  form.description = ''
  form.permission_ids = []
  nextTick(() => {
     if (permissionTreeRef.value) {
         permissionTreeRef.value.setCheckedKeys([], false)
     }
  })
}

async function handleAdd() {
  resetForm()
  if (permissionTree.value.length === 0) {
      await fetchPermissions()
  }
  dialog.title = '新增角色'
  dialog.isEdit = false
  dialog.visible = true
}

async function handleEdit(row: Role) {
  resetForm()
  if (permissionTree.value.length === 0) {
      await fetchPermissions()
  }
  dialog.title = '编辑角色'
  dialog.isEdit = true
  
  // 获取最新详情以确保权限是最新的
  try {
      const res = await PermAPI.getRoles() // 为了简单直接拿列表里的（假设列表包含 permission_ids，根据之前后端实现是包含了）
      // 或者调用详情接口
      // const detail = await PermAPI.getRoleDetail(row.id)
      
      // 这里的 row 可能不包含 integrity 的 permission_ids，如果列表接口返回了，则直接用
      // 以前面的后端代码看，列表接口返回了 permission_ids
      const fullRow = res.list.find(r => r.id === row.id) || row
      
      // Map permissions object array to IDs if permission_ids is empty but permissions is present
      let permIds = fullRow.permission_ids || []
      if (permIds.length === 0 && fullRow.permissions && fullRow.permissions.length > 0) {
          permIds = fullRow.permissions.map((p: any) => p.id)
      }

      Object.assign(form, {
          id: fullRow.id,
          name: fullRow.name,
          description: fullRow.description,
          permission_ids: permIds
      })
      
      dialog.visible = true
      nextTick(() => {
          if (permissionTreeRef.value && form.permission_ids) {
              permissionTreeRef.value.setCheckedKeys(form.permission_ids, false)
          }
      })
  } catch(e) {
      ElMessage.error('获取详情失败')
  }
}

async function handleDelete(row: Role) {
  await ElMessageBox.confirm(`确认删除角色 "${row.name}" 吗?`, '警告', {
    type: 'warning'
  })
  try {
    await PermAPI.deleteRole(row.id)
    ElMessage.success('删除成功')
    fetchList()
  } catch (error) {
    // handled
  }
}

async function handleSubmit() {
  if (!formRef.value) return
  await formRef.value.validate()
  
  // 获取选中的权限ID
  const checkedKeys = permissionTreeRef.value!.getCheckedKeys()
  const halfCheckedKeys = permissionTreeRef.value!.getHalfCheckedKeys()
  const allPermissionIds = [...checkedKeys, ...halfCheckedKeys] as number[]
  
  const data = {
      name: form.name,
      description: form.description,
      permission_ids: allPermissionIds
  }
  
  try {
    if (dialog.isEdit && form.id) {
      await PermAPI.updateRole(form.id, data)
      ElMessage.success('更新成功')
    } else {
      await PermAPI.createRole(data)
      ElMessage.success('创建成功')
    }
    dialog.visible = false
    fetchList()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

onMounted(() => {
  fetchList()
  fetchPermissions()
})
</script>

<style scoped>
.permission-tree-container {
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    padding: 10px;
}
</style>
