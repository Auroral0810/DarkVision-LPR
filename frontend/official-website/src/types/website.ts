export interface Carousel {
  id: number
  title: string
  image_url: string
  link_url: string | null
  sort_order: number
  is_enabled: boolean
}

export interface Announcement {
  id: number
  title: string
  content: string
  display_position: 'popup' | 'banner' | 'message_center'
  start_time: string | null
  end_time: string | null
  is_enabled: boolean
}

export interface FaqCategory {
  id: number
  name: string
  sort_order: number
}

export interface Faq {
  id: number
  category_id: number | null
  question: string
  answer: string
  sort_order: number
  view_count: number
  is_hot: boolean
}

export interface Document {
  id: number
  title: string
  doc_type: 'tech' | 'service_agreement' | 'privacy_policy'
  content: string
  version: string
  is_current: boolean
}

export interface ClientDownload {
  id: number
  os: 'windows' | 'macos' | 'linux'
  version: string
  download_url: string
  changelog: string | null
  release_date: string
  is_latest: boolean
}

export interface SystemConfig {
  id: number
  config_key: string
  config_value: string
  description: string | null
  is_public: boolean
}

// ContactMessage type is already handled in the contact form logic

