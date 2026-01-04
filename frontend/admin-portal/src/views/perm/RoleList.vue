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
        <el-table-column label="角色名称" prop="name" />
        <el-table-column label="角色标识" prop="code" width="150" />
        <el-table-column label="当前用户数" prop="userCount" width="120" align="center" />
        <el-table-column label="状态" width="100" align="center">
          <template #default="scope">
            <el-tag :type="scope.row.status === 1 ? 'success' : 'info'">{{ scope.row.status === 1 ? '启用' : '禁用' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="创建时间" prop="createTime" width="180" />
        <el-table-column label="操作" width="250" align="center">
          <template #default="scope">
            <el-button type="primary" size="small" link icon="Edit" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button type="primary" size="small" link icon="Lock" @click="handleAssign(scope.row)">权限分配</el-button>
            <el-button type="danger" size="small" link icon="Delete" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 权限分配对话框 -->
    <el-dialog v-model="dialog.visible" :title="dialog.title" width="500px">
      <el-scrollbar max-height="400px">
        <el-tree
          ref="permissionTreeRef"
          :data="permissionTree"
          show-checkbox
          node-key="id"
          :props="{ label: 'name', children: 'children' }"
        />
      </el-scrollbar>
      <template #footer>
        <el-button @click="dialog.visible = false">取消</el-button>
        <el-button type="primary" @click="submitPermission">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
const loading = ref(false)
const queryParams = reactive({
  keywords: ''
})

const roleList = ref([
  { id: 1, name: '超级管理员', code: 'SUPER_ADMIN', userCount: 2, status: 1, createTime: '2025-01-01 12:00:00' },
  { id: 2, name: '运营人员', code: 'OPERATOR', userCount: 5, status: 1, createTime: '2025-01-05 15:30:00' },
  { id: 3, name: '客服专员', code: 'CUSTOMER_SERVICE', userCount: 3, status: 1, createTime: '2025-01-10 09:00:00' },
  { id: 4, name: '财务审核', code: 'FINANCE_AUDIT', userCount: 1, status: 1, createTime: '2025-01-12 14:20:00' }
])

const dialog = reactive({
  visible: false,
  title: ''
})

const permissionTree = ref([
  {
    id: 1,
    name: 'DV-LPR管理',
    children: [
      { id: 11, name: '数据分析', children: [ { id: 111, name: '全局概览' }, { id: 112, name: '用户统计' } ] },
      { id: 12, name: '用户管理', children: [ { id: 121, name: '用户列表' }, { id: 122, name: '封禁权限' } ] },
      { id: 13, name: '识别服务', children: [ { id: 131, name: '实时监控' }, { id: 132, name: '记录管理' }, { id: 133, name: '模型切换' } ] },
      { id: 14, name: '财务订单', children: [ { id: 141, name: '订单查看' }, { id: 142, name: '退款审核' } ] }
    ]
  }
])

function handleQuery() {}
function resetQuery() {}
function handleAdd() {}
function handleEdit(row: any) {}
function handleAssign(row: any) {
  dialog.title = `为 [${row.name}] 分配权限`
  dialog.visible = true
}
function handleDelete(row: any) {}
function submitPermission() {
  ElMessage.success('权限分配成功')
  dialog.visible = false
}
</script>
