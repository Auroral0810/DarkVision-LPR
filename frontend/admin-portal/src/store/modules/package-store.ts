import { defineStore } from "pinia";
import request from "@/utils/request";

export const usePackageStore = defineStore("package", {
  state: () => ({
    packages: [] as any[],
    loading: false,
  }),
  actions: {
    async fetchPackages() {
      this.loading = true;
      try {
        const data = await request.get("/api/admin/packages/packages");
        this.packages = (data as any) || [];
      } catch (error) {
        console.error("Failed to fetch packages:", error);
      } finally {
        this.loading = false;
      }
    },
    clearCache() {
      this.packages = [];
    }
  },
});
