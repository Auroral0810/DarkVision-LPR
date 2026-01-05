<template>
  <div id="app">
    <Header v-if="showHeader" />
    <main class="main-content">
      <router-view />
    </main>
    <Footer v-if="showFooter" />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import Header from '@/components/layout/Header.vue'
import Footer from '@/components/layout/Footer.vue'
import { useWebsiteStore } from '@/store/website'

const route = useRoute()
const websiteStore = useWebsiteStore()

// 应用加载时获取一次官网内容
onMounted(() => {
  websiteStore.fetchContent()
})

const showHeader = computed(() => {
  return !['/login', '/register'].includes(route.path)
})

const showFooter = computed(() => {
  return !['/login', '/register'].includes(route.path)
})
</script>

<style>
#app {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  width: 100%;
}
</style>