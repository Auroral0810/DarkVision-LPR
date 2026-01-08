<template>
  <div class="app-container">
    <el-tabs v-model="activeTab">
      <el-tab-pane label="轮播图管理" name="banner">
        <div class="filter-container">
          <el-button type="primary" icon="Plus" @click="handleBannerAdd">新增轮播图</el-button>
        </div>
        <el-table :data="bannerList" border style="width: 100%; margin-top: 20px;">
          <el-table-column prop="id" label="ID" width="80" align="center" sortable />
          <el-table-column prop="title" label="标题" min-width="150" sortable />
          <el-table-column label="图片" width="180">
            <template #default="{ row }">
              <el-image 
                :src="row.image_url" 
                :preview-src-list="[row.image_url]"
                fit="cover"
                style="width: 150px; height: 80px; border-radius: 4px;"
              />
            </template>
          </el-table-column>
          <el-table-column prop="link_url" label="跳转链接" min-width="150" sortable />
          <el-table-column prop="sort_order" label="排序" width="80" align="center" sortable />
          <el-table-column prop="is_enabled" label="状态" width="100" align="center" sortable>
             <template #default="{ row }">
              <el-tag :type="row.is_enabled ? 'success' : 'info'">
                {{ row.is_enabled ? '启用' : '禁用' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150" align="center" fixed="right">
            <template #default="{ row }">
              <el-button type="primary" link @click="handleBannerEdit(row)">编辑</el-button>
              <el-button type="danger" link @click="handleBannerDelete(row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <el-tab-pane label="SEO 配置" name="seo">
        <el-form label-width="120px" style="max-width: 600px; margin-top: 20px;">
          <el-form-item label="网站标题">
            <el-input v-model="seoConfig.title" placeholder="DarkVision - 低光照车牌识别系统" />
          </el-form-item>
          <el-form-item label="关键词">
            <el-input v-model="seoConfig.keywords" placeholder="LPR, 车牌识别, 低光照, AI" />
          </el-form-item>
          <el-form-item label="描述">
            <el-input v-model="seoConfig.description" type="textarea" :rows="4" placeholder="网站描述..." />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSaveSeo">保存配置</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
    </el-tabs>

    <!-- Banner Dialog -->
    <el-dialog
      :title="isEdit ? '编辑轮播图' : '新增轮播图'"
      v-model="dialogVisible"
      width="500px"
    >
      <el-form ref="bannerFormRef" :model="bannerForm" label-width="100px">
        <el-form-item label="标题" prop="title" required>
          <el-input v-model="bannerForm.title" placeholder="请输入标题" />
        </el-form-item>
        <el-form-item label="图片链接" prop="image_url" required>
          <el-input v-model="bannerForm.image_url" placeholder="请输入图片URL" />
        </el-form-item>
        <el-form-item label="跳转链接" prop="link_url">
          <el-input v-model="bannerForm.link_url" placeholder="请输入跳转URL (可选)" />
        </el-form-item>
        <el-form-item label="排序" prop="sort_order">
          <el-input-number v-model="bannerForm.sort_order" :min="0" />
        </el-form-item>
        <el-form-item label="是否启用" prop="is_enabled">
           <el-switch v-model="bannerForm.is_enabled" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleBannerSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const activeTab = ref('banner')
const dialogVisible = ref(false)
const isEdit = ref(false)

// Mock Data
const bannerList = ref([
  { id: 1, title: '首页Banner 1', image_url: 'https://placehold.co/800x400', link_url: '/product', sort_order: 1, is_enabled: true },
  { id: 2, title: '活动推广', image_url: 'https://placehold.co/800x400', link_url: '/activity', sort_order: 2, is_enabled: false }
])

const seoConfig = reactive({
  title: 'DarkVision - 低光照车牌识别系统',
  keywords: 'LPR, 车牌识别, 低光照, AI, 深度学习',
  description: 'DarkVision LPR 是一款专为低光照环境设计的车牌识别系统，采用最新的 YOLOv12 模型，提供高精度的识别服务。'
})

const bannerForm = reactive({
  id: undefined,
  title: '',
  image_url: '',
  link_url: '',
  sort_order: 0,
  is_enabled: true
})

function handleBannerAdd() {
  isEdit.value = false
  Object.assign(bannerForm, { id: undefined, title: '', image_url: '', link_url: '', sort_order: 0, is_enabled: true })
  dialogVisible.value = true
}

function handleBannerEdit(row: any) {
  isEdit.value = true
  Object.assign(bannerForm, row)
  dialogVisible.value = true
}

function handleBannerDelete(row: any) {
  ElMessageBox.confirm('确认删除该轮播图吗？', '提示', { type: 'warning' }).then(() => {
    bannerList.value = bannerList.value.filter(item => item.id !== row.id)
    ElMessage.success('删除成功')
  })
}

function handleBannerSubmit() {
  if (isEdit.value) {
    const index = bannerList.value.findIndex((item: any) => item.id === bannerForm.id)
    if (index !== -1) {
      bannerList.value[index] = { ...bannerForm } as any
    }
    ElMessage.success('更新成功')
  } else {
    bannerList.value.push({ ...bannerForm, id: Date.now() } as any)
    ElMessage.success('创建成功')
  }
  dialogVisible.value = false
}

function handleSaveSeo() {
  ElMessage.success('SEO 配置已保存')
}
</script>

<style scoped>
.app-container { padding: 20px; }
.filter-container { margin-bottom: 20px; }
</style>
