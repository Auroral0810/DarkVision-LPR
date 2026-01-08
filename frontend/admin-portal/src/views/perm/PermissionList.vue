<template>
  <div class="app-container">
    <div class="filter-container">
      <el-button type="primary" icon="Plus" @click="handleAdd">新增权限</el-button>
      <el-button icon="Refresh" @click="initData">刷新</el-button>
    </div>

    <el-table
      :data="permissionList"
      border
      style="width: 100%; margin-top: 20px;"
      row-key="id"
      default-expand-all
      :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
    >
      <el-table-column prop="name" label="权限名称" min-width="180" sortable />
      <el-table-column prop="code" label="权限标识" width="180" />
      <el-table-column prop="type" label="类型" width="100" align="center">
        <template #default="{ row }">
          <el-tag :type="getTypeTag(row.type)">{{ typeMap[row.type] }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="path" label="路由/API路径" min-width="200" />
      <el-table-column label="操作" width="200" align="center" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link icon="Plus" size="small" @click="handleAddSub(row)" v-if="row.type !== 'button'">新增子项</el-button>
          <el-button type="primary" link icon="Edit" size="small" @click="handleEdit(row)">编辑</el-button>
          <el-button type="danger" link icon="Delete" size="small" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog
      :title="isEdit ? '编辑权限' : '新增权限'"
      v-model="dialogVisible"
      width="600px"
    >
      <el-form ref="formRef" :model="form" label-width="100px">
        <el-form-item label="上级权限">
          <el-cascader
            v-model="form.parent_id"
            :options="permissionList"
            :props="{ checkStrictly: true, value: 'id', label: 'name', emitPath: false }"
            clearable
            placeholder="选择上级 (留空为顶级)"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="权限名称" prop="name" required>
          <el-input v-model="form.name" placeholder="菜单或按钮名称" />
        </el-form-item>
        <el-form-item label="权限类型" prop="type" required>
          <el-radio-group v-model="form.type">
            <el-radio label="menu">菜单</el-radio>
            <el-radio label="button">按钮</el-radio>
            <el-radio label="api">API</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="权限标识" prop="code" required>
          <el-input v-model="form.code" placeholder="user:list, user:add" />
        </el-form-item>
        <el-form-item label="路由/路径" prop="path" v-if="form.type !== 'button'">
          <el-input v-model="form.path" placeholder="/user/list" />
        </el-form-item>
        <el-form-item label="排序" prop="sort_order">
          <el-input-number v-model="form.sort_order" :min="0" />
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

const typeMap: Record<string, string> = {
  menu: '菜单',
  button: '按钮',
  api: 'API'
}

const permissionList = ref<any[]>([])

const dialogVisible = ref(false)
const isEdit = ref(false)
const form = reactive({
  id: undefined,
  parent_id: null as number | null,
  name: '',
  code: '',
  type: 'menu',
  path: '',
  sort_order: 0
})

function initData() {
  // Mock Data
  permissionList.value = [
    {
      id: 1,
      name: '用户管理',
      code: 'user:mgmt',
      type: 'menu',
      path: '/user',
      children: [
        { id: 11, name: '用户列表', code: 'user:list', type: 'menu', path: '/user/list', children: [
            { id: 111, name: '新增用户', code: 'user:add', type: 'button' },
            { id: 112, name: '删除用户', code: 'user:delete', type: 'button' }
        ]},
        { id: 12, name: '实名认证', code: 'user:verify', type: 'menu', path: '/user/verification' }
      ]
    },
    {
      id: 2,
      name: '系统设置',
      code: 'sys:config',
      type: 'menu',
      path: '/setting',
      children: [
        { id: 21, name: '基础配置', code: 'sys:base', type: 'menu', path: '/setting/base' }
      ]
    }
  ]
}

initData()

function getTypeTag(type: string) {
  const map: any = { menu: '', button: 'info', api: 'warning' }
  return map[type]
}

function handleAdd() {
  isEdit.value = false
  Object.assign(form, { id: undefined, parent_id: null, name: '', code: '', type: 'menu', path: '', sort_order: 0 })
  dialogVisible.value = true
}

function handleAddSub(row: any) {
  isEdit.value = false
  Object.assign(form, { id: undefined, parent_id: row.id, name: '', code: '', type: 'button', path: '', sort_order: 0 })
  dialogVisible.value = true
}

function handleEdit(row: any) {
  isEdit.value = true
  Object.assign(form, row)
  dialogVisible.value = true
}

function handleDelete(row: any) {
  ElMessageBox.confirm('确认删除该权限项吗？', '提示', { type: 'warning' }).then(() => {
    ElMessage.success('删除成功 (Mock)')
    initData()
  })
}

function handleSubmit() {
  if (!form.name || !form.code) {
    ElMessage.warning('请填写必填项')
    return
  }
  ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
  dialogVisible.value = false
  // 实际项目中需调用API并刷新列表
}
</script>

<style scoped>
.app-container { padding: 20px; }
.filter-container { margin-bottom: 20px; }
</style>
