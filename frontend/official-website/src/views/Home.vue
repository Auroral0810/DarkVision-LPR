<template>
    <div class="home">
      <h1>欢迎使用暗视车牌识别系统</h1>
      <el-button type="primary" @click="handleClick">
        <el-icon><Search /></el-icon>
        开始使用
      </el-button>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ElMessage } from 'element-plus'
  
  const handleClick = () => {
    ElMessage.success('欢迎使用！')
  }
  </script>
  
  <style scoped>
  .home {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
  }
  
  h1 {
    margin-bottom: 2rem;
  }
  </style>