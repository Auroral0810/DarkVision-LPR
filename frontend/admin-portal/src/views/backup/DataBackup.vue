<template>
  <div class="data-backup-container">
    <el-card class="box-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <div class="title-area">
            <span class="title">数据备份管理</span>
            <el-tag type="info" class="ml-2">System Backup</el-tag>
          </div>
          <div class="header-actions">
            <el-button type="primary" :icon="Plus" @click="handleCreate" :loading="creating">
              新建备份
            </el-button>
          </div>
        </div>
      </template>

      <!-- 搜索筛选 -->
      <div class="filter-container">
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          value-format="YYYY-MM-DD"
          @change="fetchData"
          style="width: 300px"
        />
        <el-button class="ml-2" :icon="Refresh" circle @click="fetchData" />
      </div>

      <!-- 表格 -->
      <el-table
        v-loading="loading"
        :data="list"
        style="width: 100%"
        border
        stripe
        highlight-current-row
      >
        <el-table-column prop="id" label="ID" width="80" align="center" />
        <el-table-column prop="filename" label="备份文件名" min-width="200">
          <template #default="{ row }">
            <el-icon class="mr-1"><Document /></el-icon>
            {{ row.filename }}
          </template>
        </el-table-column>
        <el-table-column prop="file_size" label="大小" width="120" align="center">
          <template #default="{ row }">
            {{ formatSize(row.file_size) }}
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" align="center" />
        <el-table-column prop="creator_name" label="操作人" width="120" align="center" />
        <el-table-column prop="description" label="备注" min-width="150" show-overflow-tooltip />
        <el-table-column label="操作" width="200" align="center" fixed="right">
          <template #default="{ row }">
            <el-button
              type="primary"
              link
              :icon="Download"
              @click="handleDownload(row)"
            >
              下载
            </el-button>
            <el-popconfirm
              title="确定要删除该备份吗？此操作不可逆。"
              confirm-button-text="删除"
              cancel-button-text="取消"
              confirm-button-type="danger"
              @confirm="handleDelete(row)"
            >
              <template #reference>
                <el-button type="danger" link :icon="Delete">
                  删除
                </el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="queryParams.page"
          v-model:page-size="queryParams.size"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="fetchData"
          @current-change="fetchData"
        />
      </div>
    </el-card>

    <!-- 创建备份对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="新建备份"
      width="500px"
      append-to-body
    >
      <el-form label-position="top">
        <el-form-item label="备注说明">
          <el-input
            v-model="createForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入备份备注（可选）"
          />
        </el-form-item>
        <el-alert
          title="注意：备份过程可能会占用系统资源，建议在业务低峰期进行。"
          type="warning"
          :closable="false"
          show-icon
        />
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" :loading="creating" @click="confirmCreate">
            开始备份
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import { Plus, Delete, Download, Refresh, Document } from '@element-plus/icons-vue';
import BackupApi, { BackupRecord, BackupQuery } from '@/api/backup';

const loading = ref(false);
const creating = ref(false);
const list = ref<BackupRecord[]>([]);
const total = ref(0);
const dialogVisible = ref(false);
const dateRange = ref<[string, string] | null>(null);

const queryParams = reactive<BackupQuery>({
  page: 1,
  size: 10,
});

const createForm = reactive({
  description: '',
});

const fetchData = async () => {
  loading.value = true;
  try {
    const params = { ...queryParams };
    if (dateRange.value) {
      params.start_time = dateRange.value[0];
      params.end_time = dateRange.value[1];
    }
    const res: any = await BackupApi.getBackupList(params);
    list.value = res.list;
    total.value = res.total;
  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
};

const handleCreate = () => {
  createForm.description = '';
  dialogVisible.value = true;
};

const confirmCreate = async () => {
  creating.value = true;
  try {
    await BackupApi.createBackup({ description: createForm.description });
    ElMessage.success('备份创建成功');
    dialogVisible.value = false;
    fetchData();
  } catch (error) {
    console.error(error);
  } finally {
    creating.value = false;
  }
};

const handleDelete = async (row: BackupRecord) => {
  try {
    await BackupApi.deleteBackup(row.id);
    ElMessage.success('删除成功');
    fetchData();
  } catch (error) {
    console.error(error);
  }
};

const handleDownload = (row: BackupRecord) => {
  const url = BackupApi.getDownloadUrl(row.id);
  window.open(url, '_blank');
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
.data-backup-container {
  padding: 20px;

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
        color: #303133;
      }
    }
  }

  .filter-container {
    margin-bottom: 20px;
    display: flex;
    align-items: center;
  }

  .pagination-container {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }
}
</style>
