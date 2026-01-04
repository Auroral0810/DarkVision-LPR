<template>
  <div class="placeholder-container">
    <el-empty :description="description">
      <template #extra>
        <el-tag type="info">开发中 / Under Development</el-tag>
      </template>
    </el-empty>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const description = computed(() => {
  return (route.meta.title as string) || '该功能正在积极开发中...'
})
</script>

<style scoped>
.placeholder-container {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #fff;
  border-radius: 8px;
  margin: 20px;
}
</style>
