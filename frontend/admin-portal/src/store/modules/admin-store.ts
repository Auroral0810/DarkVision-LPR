import { defineStore } from 'pinia'
import request from '@/utils/request'
import { ElMessage } from 'element-plus'

export const useAdminStore = defineStore('admin', {
  state: () => ({
    adminUsers: [],
    roles: [], 
    permissions: [],
    loading: false
  }),
  actions: {
    // Admin Users
    async fetchAdminUsers() {
      this.loading = true
      try {
        const res = await request.get('/api/admin/admin-users')
        this.adminUsers = res.data
      } catch (error) {
        console.error(error)
      } finally {
        this.loading = false
      }
    },
    async createAdminUser(data: any) {
      await request.post('/api/admin/admin-users', data)
      await this.fetchAdminUsers()
    },
    async updateAdminUser(id: number, data: any) {
      await request.put(`/api/admin/admin-users/${id}`, data)
      await this.fetchAdminUsers()
    },
    // Roles (Alternative to RoleAPI if using store)
    async fetchRoles() {
       // Note: RoleAPI returns paged result, but here we assume we might want full list for dropdowns
       // We can call /components/options or similar, or just use the paged API and get all?
       // My updated backend `admin_service` returns all, but `role.py` pages it.
       // For dropdowns, we usually need ALL roles.
       // Let's assume we can increase pageSize or add `/all` endpoint.
       // Existing `role.py` has `@router.get("/all")`!
       try {
         const res = await request.get('/api/admin/roles/all')
         this.roles = res.data
       } catch (e) {}
    }
  }
})
