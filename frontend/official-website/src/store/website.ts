import { defineStore } from 'pinia'
import { ref } from 'vue'
import request from '@/utils/request'
import type { 
  Carousel, Announcement, ClientDownload, Faq, Document, SystemConfig 
} from '@/types/website'

export const useWebsiteStore = defineStore('website', () => {
  const carousels = ref<Carousel[]>([])
  const announcements = ref<Announcement[]>([])
  const downloads = ref<ClientDownload[]>([])
  const faqs = ref<Faq[]>([])
  const documents = ref<Document[]>([])
  const configs = ref<SystemConfig[]>([])
  
  const loading = ref(false)
  const loaded = ref(false) // 标记数据是否已加载

  const fetchContent = async (force = false) => {
    // 如果已经加载过且不强制刷新，则直接返回
    if (loaded.value && !force) return

    loading.value = true
    try {
      const { data } = await request.get('/website/content')
      if (data) {
        carousels.value = data.carousels || []
        announcements.value = data.announcements || []
        downloads.value = data.downloads || []
        faqs.value = data.faqs || []
        documents.value = data.documents || []
        configs.value = data.configs || []
        loaded.value = true
      }
    } catch (error) {
      console.error('Failed to fetch website content:', error)
    } finally {
      loading.value = false
    }
  }

  return {
    carousels,
    announcements,
    downloads,
    faqs,
    documents,
    configs,
    loading,
    loaded,
    fetchContent
  }
})

