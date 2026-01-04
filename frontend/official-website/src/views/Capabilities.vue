<template>
  <div class="page">
    <h1>{{ title }}</h1>
    <p>页面开发中...</p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const title = ref('PAGE_TITLE')
</script>

<style scoped>
.page {
  padding: 2rem;
}
</style>
