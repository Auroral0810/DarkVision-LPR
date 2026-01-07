<template>
  <div class="app-container">
    <el-card shadow="never">
      <template #header>
        <div class="flex justify-between items-center">
          <span>权限管理</span>
          <div class="flex gap-2">
             <el-button type="default" icon="Refresh" @click="fetchPermissions">刷新</el-button>
             <el-button type="primary" icon="Plus" @click="handleAdd('menu', null)">新增顶级权限</el-button>
          </div>
        </div>
      </template>

      <el-table
        v-loading="loading"
        :data="permissionList"
        row-key="id"
        border
        default-expand-all
        :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
      >
        <el-table-column prop="name" label="名称" width="200" />
        <el-table-column prop="code" label="标识 (Code)" width="200" />
        <el-table-column prop="type" label="类型" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="getParamType(row.type).type">{{ getParamType(row.type).label }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="path" label="路径 (Path)" show-overflow-tooltip />
        <el-table-column prop="component" label="组件 (Component)" show-overflow-tooltip />
        <el-table-column prop="icon" label="图标" width="80" align="center">
          <template #default="{ row }">
            <el-icon v-if="row.icon"><component :is="row.icon" /></el-icon>
          </template>
        </el-table-column>
        <el-table-column prop="sort_order" label="排序" width="80" align="center" />
        <el-table-column label="操作" width="250" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="handleAdd(row.type === 'menu' ? 'button' : 'sub_api', row.id)" v-if="row.type !== 'api'">新增下级</el-button>
            <el-button link type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button link type="danger" size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 权限表单 Dialog -->
    <el-dialog
      v-model="dialog.visible"
      :title="dialog.isEdit ? '编辑权限' : '新增权限'"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="上级权限" prop="parent_id">
           <el-tree-select
              v-model="form.parent_id"
              :data="treeSelectData"
              :props="{ label: 'name', value: 'id', children: 'children' }"
              value-key="id" 
              placeholder="选择上级权限 (不选则为顶级)"
              check-strictly
              clearable
              style="width: 100%"
           />
        </el-form-item>
        <el-form-item label="权限类型" prop="type">
          <el-radio-group v-model="form.type">
            <el-radio label="menu">菜单</el-radio>
            <el-radio label="button">按钮</el-radio>
            <el-radio label="api">接口</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" placeholder="如: 用户管理" />
        </el-form-item>
        <el-form-item label="标识 Code" prop="code">
          <el-input v-model="form.code" placeholder="如: user:list" />
        </el-form-item>
        <el-form-item label="路由 Path" prop="path" v-if="form.type !== 'button'">
          <el-input v-model="form.path" placeholder="如: /user/list" />
        </el-form-item>
        <el-form-item label="组件 Path" prop="component" v-if="form.type === 'menu'">
          <el-input v-model="form.component" placeholder="如: views/user/UserList.vue" />
        </el-form-item>
        <el-form-item label="图标" prop="icon" v-if="form.type === 'menu'">
          <el-input v-model="form.icon" placeholder="如: el-icon-User" />
        </el-form-item>
        <el-form-item label="排序" prop="sort_order">
          <el-input-number v-model="form.sort_order" :min="0" :max="999" />
        </el-form-item>
         <el-form-item label="描述" prop="description">
          <el-input v-model="form.description" type="textarea" placeholder="" />
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
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import PermAPI, { type Permission } from '@/api/perm-api'

const loading = ref(false)
const permissionList = ref<Permission[]>([])

const dialog = reactive({
    visible: false,
    isEdit: false
})
const formRef = ref()
const form = reactive({
    id: undefined as number | undefined,
    parent_id: undefined as number | undefined | null, // null is important for root
    name: '',
    code: '',
    type: 'menu',
    path: '',
    component: '',
    icon: '',
    sort_order: 0,
    description: ''
})

const rules = {
    name: [{ required: true, message: '请输入名称', trigger: 'blur' }],
    code: [{ required: true, message: '请输入标识 Code', trigger: 'blur' }],
    type: [{ required: true, message: '请选择类型', trigger: 'change' }]
}

// Transform permission list for tree select (add root option if needed, but here we rely on clearable to select root)
const treeSelectData = computed(() => {
    // We can filter out current edit node's children to prevent circular reference if desired
    return permissionList.value
})

function getParamType(type: string) {
    const map: any = {
        'menu': { label: '菜单', type: 'primary' },
        'button': { label: '按钮', type: 'success' },
        'api': { label: '接口', type: 'info' }
    }
    return map[type] || { label: type, type: 'info' }
}

async function fetchPermissions() {
    loading.value = true
    try {
        const res = await PermAPI.getPermissions()
        permissionList.value = res
    } finally {
        loading.value = false
    }
}

function resetForm() {
    form.id = undefined
    form.parent_id = undefined
    form.name = ''
    form.code = ''
    form.type = 'menu'
    form.path = ''
    form.component = ''
    form.icon = ''
    form.sort_order = 0
    form.description = ''
}

function handleAdd(type: string, parentId: number | null) {
    resetForm()
    dialog.isEdit = false
    // If adding sub-level, default to button or menu logic? 
    if (type === 'sub_api') {
        form.type = 'api'
    } else {
        form.type = type
    }
    
    if (parentId) {
        form.parent_id = parentId
    }
    
    dialog.visible = true
}

function handleEdit(row: Permission) {
    resetForm()
    dialog.isEdit = true
    Object.assign(form, row)
    // ensure parent_id is handled correctly (sometimes 0 or null)
    if (form.parent_id === 0) form.parent_id = undefined
    
    dialog.visible = true
}

async function handleDelete(row: Permission) {
     await ElMessageBox.confirm(`确认删除权限 "${row.name}" 吗? 如果存在子权限将一并删除。`, '警告', {
        type: 'warning'
    })
    try {
        await PermAPI.deletePermission(row.id)
        ElMessage.success('删除成功')
        fetchPermissions()
    } catch(e) {
        // handled
    }
}

async function handleSubmit() {
    if (!formRef.value) return
    await formRef.value.validate()
    
    const data = { ...form }
    if (!data.parent_id) data.parent_id = null // Ensure null for root
    
    try {
        if (dialog.isEdit && form.id) {
            await PermAPI.updatePermission(form.id, data)
            ElMessage.success('更新成功')
        } else {
            await PermAPI.createPermission(data)
            ElMessage.success('创建成功')
        }
        dialog.visible = false
        fetchPermissions()
    } catch(e) {
        ElMessage.error('操作失败')
    }
}

onMounted(() => {
    fetchPermissions()
})
</script>

<style scoped>
.flex { display: flex; }
.justify-between { justify-content: space-between; }
.items-center { align-items: center; }
.gap-2 { gap: 0.5rem; }
</style>
