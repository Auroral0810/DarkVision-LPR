import { defineStore } from 'pinia'
import request from '@/utils/request'
import { ElMessage } from 'element-plus'

export const useSystemConfigStore = defineStore('system-config', {
  state: () => ({
    configs: {
      base: {} as any,
      recognition: {} as any,
      quota: {} as any,
      notice: {} as any,
      security: {} as any,
      other: {} as any
    },
    loading: false
  }),
  actions: {
    async fetchConfigs() {
      this.loading = true
      try {
        const res = await request.get('/api/admin/system/configs')
        this.configs = res as any
      } catch (error) {
        console.error('Failed to fetch system configs:', error)
      } finally {
        this.loading = false
      }
    },
    async updateConfigs(configs: Record<string, any>) {
      this.loading = true
      try {
        await request.put('/api/admin/system/configs', { configs })
        ElMessage.success('配置更新成功')
        await this.fetchConfigs()
      } catch (error) {
        console.error('Failed to update system configs:', error)
      } finally {
        this.loading = false
      }
    }
  }
})
