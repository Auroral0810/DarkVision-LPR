<template>
  <div class="app-container">
    <el-tabs v-model="activeTab">
      <el-tab-pane label="轮播图管理" name="banner">
        <div class="filter-container">
          <el-button type="primary" icon="Plus" @click="handleBannerAdd">新增轮播图</el-button>
        </div>
        <el-table v-loading="loading" :data="bannerList" border style="width: 100%; margin-top: 20px;">
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
            <el-input :model-value="seoConfig.title" @update:model-value="handleSeoInput('title', $event)" placeholder="DarkVision - 低光照车牌识别系统" />
          </el-form-item>
          <el-form-item label="关键词">
            <el-input :model-value="seoConfig.keywords" @update:model-value="handleSeoInput('keywords', $event)" placeholder="LPR, 车牌识别, 低光照, AI" />
          </el-form-item>
          <el-form-item label="描述">
            <el-input :model-value="seoConfig.description" @update:model-value="handleSeoInput('description', $event)" type="textarea" :rows="4" placeholder="网站描述..." />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" :loading="submitLoading" @click="handleSaveSeo">保存配置</el-button>
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
          <el-button type="primary" :loading="submitLoading" @click="handleBannerSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useContentStore } from '@/store/modules/content-store'
import { useSystemConfigStore } from '@/store/modules/system-config-store'
import { storeToRefs } from 'pinia'
import { ElMessage, ElMessageBox } from 'element-plus'

const contentStore = useContentStore()
const systemConfigStore = useSystemConfigStore()

const { carousels: bannerList, loading } = storeToRefs(contentStore)
const { configs } = storeToRefs(systemConfigStore)

const activeTab = ref('banner')
const dialogVisible = ref(false)
const isEdit = ref(false)
const submitLoading = ref(false)

const seoConfig = computed(() => ({
  title: configs.value.base.seo_title || '',
  keywords: configs.value.base.seo_keywords || '',
  description: configs.value.base.seo_description || ''
}))

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
  Object.assign(bannerForm, { ...row })
  dialogVisible.value = true
}

function handleBannerDelete(row: any) {
  ElMessageBox.confirm('确认删除该轮播图吗？', '提示', { type: 'warning' }).then(async () => {
    await contentStore.deleteCarousel(row.id)
    ElMessage.success('删除成功')
  })
}

async function handleBannerSubmit() {
  if (!bannerForm.title || !bannerForm.image_url) {
    ElMessage.warning('请填写必填项')
    return
  }

  submitLoading.value = true
  try {
    if (isEdit.value) {
      await contentStore.updateCarousel(bannerForm.id!, { ...bannerForm })
      ElMessage.success('更新成功')
    } else {
      await contentStore.createCarousel({ ...bannerForm })
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
  } catch (error) {
    console.error(error)
  } finally {
    submitLoading.value = false
  }
}

async function handleSaveSeo() {
  submitLoading.value = true
  try {
    await systemConfigStore.updateConfigs({
      'base.seo_title': seoConfig.value.title,
      'base.seo_keywords': seoConfig.value.keywords,
      'base.seo_description': seoConfig.value.description
    })
    ElMessage.success('SEO 配置已保存')
  } catch (error) {
    console.error(error)
  } finally {
    submitLoading.value = false
  }
}

const handleSeoInput = (key: 'title' | 'keywords' | 'description', val: string) => {
  configs.value.base[`seo_${key}`] = val
}

onMounted(() => {
  contentStore.fetchCarousels()
  systemConfigStore.fetchConfigs()
})
</script>

<style scoped>
.app-container { padding: 20px; }
.filter-container { margin-bottom: 20px; }
</style>
