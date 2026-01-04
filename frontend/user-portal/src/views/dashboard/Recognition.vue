<template>
  <div class="recognition-view">
    <el-tabs v-model="activeTab" class="recognition-tabs">
      <el-tab-pane label="单张识别" name="single">
        <SingleUploader />
      </el-tab-pane>
      
      <el-tab-pane label="批量识别" name="batch">
        <template #label>
          <span>批量识别</span>
          <el-tag v-if="!userStore.isVIP" size="small" type="warning" class="tab-tag">VIP</el-tag>
        </template>
        
        <div v-if="userStore.isVIP">
          <BatchUploader />
        </div>
        <div v-else class="vip-lock">
          <el-empty description="批量识别是 VIP 专属功能">
            <template #extra>
              <el-button type="warning" @click="showUpgrade">升级到 VIP</el-button>
            </template>
          </el-empty>
        </div>
      </el-tab-pane>
      
      <el-tab-pane label="视频识别" name="video">
        <template #label>
          <span>视频识别</span>
          <el-tag v-if="!userStore.isVIP" size="small" type="warning" class="tab-tag">VIP</el-tag>
        </template>
        
        <div class="vip-lock">
          <el-empty description="视频识别功能开发中...">
            <template #extra>
              <el-button type="primary" disabled>敬请期待</el-button>
            </template>
          </el-empty>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useUserStore } from '@/store/user'
import SingleUploader from '@/components/recognition/SingleUploader.vue'
import BatchUploader from '@/components/recognition/BatchUploader.vue'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()
const activeTab = ref('single')

const showUpgrade = () => {
  ElMessage.warning('请联系管理员升级账户')
}
</script>

<style scoped lang="scss">
.recognition-view {
  background: white;
  padding: 24px;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  min-height: 600px;
}

.recognition-tabs {
  :deep(.el-tabs__header) {
    margin-bottom: 32px;
  }
}

.tab-tag {
  margin-left: 8px;
  transform: scale(0.8);
}

.vip-lock {
  padding: 40px 0;
  display: flex;
  justify-content: center;
}
</style>
