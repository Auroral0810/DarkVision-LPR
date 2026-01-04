<template>
  <div class="app-container">
    <el-row :gutter="20" class="mb-4">
      <el-col :span="8">
        <el-card shadow="hover">
          <el-statistic title="识别成功率" :value="98.5">
            <template #suffix>%</template>
          </el-statistic>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <el-statistic title="平均耗时" :value="156">
            <template #suffix>ms</template>
          </el-statistic>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <el-statistic title="今日并发峰值" :value="42">
            <template #suffix>qps</template>
          </el-statistic>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="mb-4">
      <template #header><span>性能趋势</span></template>
      <div style="height: 350px; display: flex; align-items: center; justify-content: center; color: #999;">
        [ ECharts: 识别耗时与成功率双轴图 ]
      </div>
    </el-card>

    <el-row :gutter="20">
      <el-col :span="12">
        <el-card>
          <template #header><span>异常原因分类</span></template>
          <div style="height: 300px; display: flex; align-items: center; justify-content: center; color: #999;">
            [ ECharts: 错误代码分布饼图 ]
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header><span>不同场景下表现</span></template>
          <div style="height: 300px; display: flex; align-items: center; justify-content: center; color: #999;">
            [ ECharts: 夜间 vs 白天准确率对比 ]
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
// Logic for fetching stats would go here
</script>

<style scoped>
.mb-4 {
  margin-bottom: 20px;
}
</style>
