import request from '@/utils/request'

// --- Interfaces ---

export interface Carousel {
  id: number
  title: string
  image_url: string
  link_url?: string
  sort_order: number
  is_enabled: boolean
  created_at: string
}

export interface Announcement {
  id: number
  title: string
  content: string
  display_position: string
  start_time?: string
  end_time?: string
  is_enabled: boolean
  created_at: string
  created_by: number
}

export interface Document {
  id: number
  title: string
  doc_type: string
  content: string
  version: string
  is_current: boolean
  created_at: string
  created_by: number
}

export interface FaqCategory {
  id: number
  name: string
  sort_order: number
}

export interface Faq {
  id: number
  question: string
  answer: string
  category_id?: number
  sort_order: number
  is_hot: boolean
  view_count: number
  created_at: string
  category?: FaqCategory
}

// --- API Methods ---

const BASE_URL = '/api/admin/content'

export default {
  // Carousels
  getCarousels(params?: any) {
    return request({
      url: `${BASE_URL}/carousels`,
      method: 'get',
      params
    })
  },
  createCarousel(data: any) {
    return request({
      url: `${BASE_URL}/carousels`,
      method: 'post',
      data
    })
  },
  updateCarousel(id: number, data: any) {
    return request({
      url: `${BASE_URL}/carousels/${id}`,
      method: 'put',
      data
    })
  },
  deleteCarousel(id: number) {
    return request({
      url: `${BASE_URL}/carousels/${id}`,
      method: 'delete'
    })
  },

  // Announcements
  getAnnouncements(params?: any) {
    return request({
      url: `${BASE_URL}/announcements`,
      method: 'get',
      params
    })
  },
  createAnnouncement(data: any) {
    return request({
      url: `${BASE_URL}/announcements`,
      method: 'post',
      data
    })
  },
  updateAnnouncement(id: number, data: any) {
    return request({
      url: `${BASE_URL}/announcements/${id}`,
      method: 'put',
      data
    })
  },
  deleteAnnouncement(id: number) {
    return request({
      url: `${BASE_URL}/announcements/${id}`,
      method: 'delete'
    })
  },

  // Documents
  getDocuments(params?: any) {
    return request({
      url: `${BASE_URL}/documents`,
      method: 'get',
      params
    })
  },
  createDocument(data: any) {
    return request({
      url: `${BASE_URL}/documents`,
      method: 'post',
      data
    })
  },
  updateDocument(id: number, data: any) {
    return request({
      url: `${BASE_URL}/documents/${id}`,
      method: 'put',
      data
    })
  },
  deleteDocument(id: number) {
    return request({
      url: `${BASE_URL}/documents/${id}`,
      method: 'delete'
    })
  },

  // FAQs
  getFaqCategories() {
    return request({
      url: `${BASE_URL}/faqs/categories`,
      method: 'get'
    })
  },
  createFaqCategory(data: any) {
    return request({
      url: `${BASE_URL}/faqs/categories`,
      method: 'post',
      data
    })
  },
  updateFaqCategory(id: number, data: any) {
    return request({
      url: `${BASE_URL}/faqs/categories/${id}`,
      method: 'put',
      data
    })
  },
  deleteFaqCategory(id: number) {
    return request({
      url: `${BASE_URL}/faqs/categories/${id}`,
      method: 'delete'
    })
  },
  getFaqs(params?: any) {
    return request({
      url: `${BASE_URL}/faqs`,
      method: 'get',
      params
    })
  },
  createFaq(data: any) {
    return request({
      url: `${BASE_URL}/faqs`,
      method: 'post',
      data
    })
  },
  updateFaq(id: number, data: any) {
    return request({
      url: `${BASE_URL}/faqs/${id}`,
      method: 'put',
      data
    })
  },
  deleteFaq(id: number) {
    return request({
      url: `${BASE_URL}/faqs/${id}`,
      method: 'delete'
    })
  }
}
