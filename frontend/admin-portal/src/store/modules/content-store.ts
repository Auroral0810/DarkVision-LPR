import { defineStore } from 'pinia'
import request from '@/utils/request'
import { ElMessage } from 'element-plus'

export const useContentStore = defineStore('content', {
  state: () => ({
    carousels: [] as any[],
    announcements: [] as any[],
    documents: [] as any[],
    faqs: [] as any[],
    faqCategories: [] as any[],
    loading: false
  }),
  actions: {
    // Carousels
    async fetchCarousels() {
      this.loading = true
      try {
        const res = await request.get('/api/admin/content/carousels')
        this.carousels = res as any
      } catch (error) {
        console.error(error)
      } finally {
        this.loading = false
      }
    },
    async createCarousel(data: any) {
      await request.post('/api/admin/content/carousels', data)
      await this.fetchCarousels()
    },
    async updateCarousel(id: number, data: any) {
      await request.put(`/api/admin/content/carousels/${id}`, data)
      await this.fetchCarousels()
    },
    async deleteCarousel(id: number) {
      await request.delete(`/api/admin/content/carousels/${id}`)
      await this.fetchCarousels()
    },

    // Announcements
    async fetchAnnouncements() {
      this.loading = true
      try {
        const res = await request.get('/api/admin/content/announcements')
        this.announcements = res as any
      } catch (error) {
        console.error(error)
      } finally {
        this.loading = false
      }
    },
    async createAnnouncement(data: any) {
      await request.post('/api/admin/content/announcements', data)
      await this.fetchAnnouncements()
    },
    async updateAnnouncement(id: number, data: any) {
      await request.put(`/api/admin/content/announcements/${id}`, data)
      await this.fetchAnnouncements()
    },
    async deleteAnnouncement(id: number) {
      await request.delete(`/api/admin/content/announcements/${id}`)
      await this.fetchAnnouncements()
    },

    // Documents
    async fetchDocuments() {
      this.loading = true
      try {
        const res = await request.get('/api/admin/content/documents')
        this.documents = res as any
      } catch (error) {
        console.error(error)
      } finally {
        this.loading = false
      }
    },
    async createDocument(data: any) {
      await request.post('/api/admin/content/documents', data)
      await this.fetchDocuments()
    },
    async updateDocument(id: number, data: any) {
      await request.put(`/api/admin/content/documents/${id}`, data)
      await this.fetchDocuments()
    },
    async deleteDocument(id: number) {
      await request.delete(`/api/admin/content/documents/${id}`)
      await this.fetchDocuments()
    },

    // FAQs
    async fetchFaqs() {
      this.loading = true
      try {
        const res = await request.get('/api/admin/content/faqs')
        this.faqs = res as any
      } catch (error) {
        console.error(error)
      } finally {
        this.loading = false
      }
    },
    async createFaq(data: any) {
      await request.post('/api/admin/content/faqs', data)
      await this.fetchFaqs()
    },
    async updateFaq(id: number, data: any) {
      await request.put(`/api/admin/content/faqs/${id}`, data)
      await this.fetchFaqs()
    },
    async deleteFaq(id: number) {
      await request.delete(`/api/admin/content/faqs/${id}`)
      await this.fetchFaqs()
    },

    // FAQ Categories
    async fetchFaqCategories() {
      try {
        const res = await request.get('/api/admin/content/faq-categories')
        this.faqCategories = res as any
      } catch (error) {
        console.error(error)
      }
    },
    async createFaqCategory(data: any) {
      await request.post('/api/admin/content/faq-categories', data)
      await this.fetchFaqCategories()
    },
    async updateFaqCategory(id: number, data: any) {
      await request.put(`/api/admin/content/faq-categories/${id}`, data)
      await this.fetchFaqCategories()
    },
    async deleteFaqCategory(id: number) {
      await request.delete(`/api/admin/content/faq-categories/${id}`)
      await this.fetchFaqCategories()
    }
  }
})
