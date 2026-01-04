<template>
  <div id="app">
    <Header v-if="showHeader" />
    <main class="main-content">
      <router-view />
    </main>
    <Footer v-if="showFooter" />
    
    <LoginModal 
      v-model:visible="appStore.loginModalVisible"
      @switch-to-register="appStore.showRegisterModal" 
    />
    <RegisterModal 
      v-model:visible="appStore.registerModalVisible"
      @switch-to-login="appStore.showLoginModal" 
    />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/store/user'
import { useAppStore } from '@/store/app'
import Header from '@/components/layout/Header.vue'
import Footer from '@/components/layout/Footer.vue'
import LoginModal from '@/components/LoginModal.vue'
import RegisterModal from '@/components/RegisterModal.vue'

const route = useRoute()
const userStore = useUserStore()
const appStore = useAppStore()

const showHeader = computed(() => {
  return !['/login', '/register'].includes(route.path)
})

const showFooter = computed(() => {
  return !['/login', '/register'].includes(route.path)
})

onMounted(() => {
  userStore.initUserInfo()
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