<template>
  <div class="data-recovery-container">
    <el-alert
      title="数据恢复风险提示"
      type="error"
      description="数据恢复将覆盖当前数据库的所有数据，此操作不可逆！请确保您已经备份了当前数据，或者清楚您正在做什么。建议在业务停止期间进行。"
      show-icon
      :closable="false"
      class="mb-4"
    />

    <el-card class="box-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <div class="title-area">
            <span class="title">数据恢复 / 还原</span>
            <el-tag type="danger" class="ml-2">Data Restoration</el-tag>
          </div>
          <div class="header-actions">
            <el-button @click="fetchData" :icon="Refresh">刷新列表</el-button>
          </div>
        </div>
      </template>

      <el-table
        v-loading="loading"
        :data="list"
        style="width: 100%"
        border
        stripe
      >
        <el-table-column prop="id" label="ID" width="80" align="center" />
        <el-table-column prop="filename" label="备份源文件" min-width="200">
           <template #default="{ row }">
            <el-icon class="mr-1"><Files /></el-icon>
            {{ row.filename }}
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="备份时间" width="180" align="center" />
        <el-table-column prop="file_size" label="大小" width="120" align="center">
          <template #default="{ row }">
            {{ formatSize(row.file_size) }}
          </template>
        </el-table-column>
        <el-table-column prop="description" label="备注" min-width="150" show-overflow-tooltip />
        <el-table-column label="操作" width="150" align="center" fixed="right">
          <template #default="{ row }">
            <el-button
              type="danger"
              :icon="RefreshLeft"
              @click="handleRestoreClick(row)"
              :disabled="row.status !== 'success'"
            >
              还原此备份
            </el-button>
          </template>
        </el-table-column>
      </el-table>

       <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="queryParams.page"
          v-model:page-size="queryParams.size"
          :page-sizes="[10, 20]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="fetchData"
          @current-change="fetchData"
        />
      </div>
    </el-card>

    <!-- 还原确认对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="⚠️ 高风险操作确认"
      width="500px"
      append-to-body
      center
    >
      <div class="confirm-content">
        <el-result
          icon="warning"
          title="确定要还原数据库吗？"
          sub-title="当前数据库将被完全覆盖，且无法撤销！"
        />
        <div class="backup-info" v-if="selectedBackup">
          <p><strong>目标备份文件：</strong> {{ selectedBackup.filename }}</p>
          <p><strong>备份时间：</strong> {{ selectedBackup.created_at }}</p>
        </div>
        <div class="verify-input">
          <p>请输入 <strong>confirm</strong> 以确认操作：</p>
          <el-input v-model="confirmInput" placeholder="confirm" />
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button
            type="danger"
            :loading="restoring"
            :disabled="confirmInput !== 'confirm'"
            @click="executeRestore"
          >
            我已知晓风险，立即还原
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { ElMessage, ElNotification } from 'element-plus';
import { Refresh, RefreshLeft, Files } from '@element-plus/icons-vue';
import BackupApi, { BackupRecord, BackupQuery } from '@/api/backup';

const loading = ref(false);
const restoring = ref(false);
const list = ref<BackupRecord[]>([]);
const total = ref(0);
const dateRange = ref(null);

const dialogVisible = ref(false);
const selectedBackup = ref<BackupRecord | null>(null);
const confirmInput = ref('');

const queryParams = reactive<BackupQuery>({
  page: 1,
  size: 10,
});

const fetchData = async () => {
  loading.value = true;
  try {
    const res: any = await BackupApi.getBackupList(queryParams);
    list.value = res.list;
    total.value = res.total;
  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
};

const handleRestoreClick = (row: BackupRecord) => {
  selectedBackup.value = row;
  confirmInput.value = '';
  dialogVisible.value = true;
};

const executeRestore = async () => {
  if (!selectedBackup.value) return;
  restoring.value = true;
  try {
    await BackupApi.restoreBackup(selectedBackup.value.id);
    ElNotification({
      title: '还原成功',
      message: '数据库已成功还原到指定版本。',
      type: 'success',
      duration: 5000
    });
    dialogVisible.value = false;
  } catch (error) {
    console.error(error);
  } finally {
    restoring.value = false;
  }
};

const formatSize = (bytes: number) => {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

onMounted(() => {
  fetchData();
});
</script>

<style scoped lang="scss">
.data-recovery-container {
  padding: 20px;

  .mb-4 {
    margin-bottom: 20px;
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    .title-area {
        display: flex;
        align-items: center;
        .title {
            font-size: 18px;
            font-weight: 600;
        }
    }
  }

  .pagination-container {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }

  .confirm-content {
    .backup-info {
      background: #fdf6ec;
      padding: 10px;
      border-radius: 4px;
      margin: 10px 0;
      color: #e6a23c;
      font-size: 13px;
    }
    .verify-input {
      margin-top: 15px;
      p {
        margin-bottom: 5px;
        font-size: 14px;
      }
    }
  }
}
</style>
