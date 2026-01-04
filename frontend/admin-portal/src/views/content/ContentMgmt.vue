<template>
  <div class="app-container">
    <el-tabs v-model="activeTab">
      <el-tab-pane label="轮播图管理" name="banner">
        <el-card shadow="never">
          <template #header><el-button type="primary" icon="Plus">上传新 Banner</el-button></template>
          <el-table :data="banners" border>
            <el-table-column label="预览" width="200">
              <template #default="scope">
                <el-image :src="scope.row.url" :preview-src-list="[scope.row.url]" />
              </template>
            </el-table-column>
            <el-table-column label="标题" prop="title" />
            <el-table-column label="链接" prop="link" />
            <el-table-column label="排序" prop="sort" width="80" align="center" />
            <el-table-column label="状态" width="100" align="center">
              <template #default="scope">
                <el-switch :model-value="scope.row.active" />
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150" align="center">
              <template #default>
                <el-button type="primary" link icon="Edit">编辑</el-button>
                <el-button type="danger" link icon="Delete">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>

      <el-tab-pane label="公告通知" name="notice">
        <el-card shadow="never">
          <template #header><el-button type="primary" icon="Plus">发布公告</el-button></template>
          <el-table :data="notices" border>
            <el-table-column label="标题" prop="title" />
            <el-table-column label="类型" prop="type" width="100" />
            <el-table-column label="发布时间" prop="time" width="180" />
            <el-table-column label="状态" width="100" align="center">
              <template #default="scope">
                <el-tag :type="scope.row.active ? 'success' : 'info'">{{ scope.row.active ? '展示中' : '已下线' }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150" align="center">
              <template #default>
                <el-button type="primary" link icon="View">预览</el-button>
                <el-button type="danger" link icon="Close">下线</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>

      <el-tab-pane label="FAQ 知识库" name="faq">
        <el-card shadow="never">
          <template #header><el-button type="primary" icon="Plus">新增常见问题</el-button></template>
          <el-collapse accordion>
            <el-collapse-item v-for="item in faqs" :key="item.id" :title="item.q">
              <div>{{ item.a }}</div>
              <div class="mt-2">
                <el-button size="small" type="primary" plain>编辑</el-button>
                <el-button size="small" type="danger" plain>删除</el-button>
              </div>
            </el-collapse-item>
          </el-collapse>
        </el-card>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
const activeTab = ref('banner')
const banners = ref([
  { url: 'https://picsum.photos/seed/lpr1/800/400', title: '低照度识别技术革新', link: '/tech', sort: 1, active: true },
  { url: 'https://picsum.photos/seed/lpr2/800/400', title: 'VIP 精英套餐限时优惠', link: '/pricing', sort: 2, active: true }
])
const notices = ref([
  { title: '关于系统维护的公告', type: '维护', time: '2026-01-04 10:00:00', active: true },
  { title: '新增对 YOLOv12-PRO 模型支持', type: '更新', time: '2026-01-01 12:00:00', active: true }
])
const faqs = ref([
  { id: 1, q: '如何提高识别准确率？', a: '建议上传分辨率在 720p 以上的图片，并确保车牌在画面中清晰可见。' },
  { id: 2, q: '免费用户有哪些限制？', a: '免费用户每日可进行 20 次识别尝试，单个文件大小限制为 5MB。' }
])
</script>

<style scoped>
.mt-2 { margin-top: 8px; }
</style>
