<script setup lang="ts">
import { useUserStore } from '@/store/user'
import { useUserWebSocket } from '@/composables/useUserWebSocket'

const userStore = useUserStore()
// 启用 WebSocket 监听用户状态（强制下线等）
useUserWebSocket()
</script>

<template>
  <el-config-provider :locale="userStore.locale">
    <router-view />
  </el-config-provider>
</template>

<style>
body {
  margin: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
