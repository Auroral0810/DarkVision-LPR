<template>
  <div class="app-container">
    <el-row :gutter="20">
      <el-col :span="6" v-for="kpi in financeKpis" :key="kpi.label">
        <el-card shadow="hover">
          <div class="kpi-label">{{ kpi.label }}</div>
          <div class="kpi-value">￥{{ kpi.value }}</div>
          <div class="kpi-trend" :class="kpi.trend > 0 ? 'up' : 'down'">
            {{ kpi.trend > 0 ? '+' : '' }}{{ kpi.trend }}% 较昨日
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-tabs v-model="activeTab" class="mt-4">
      <el-tab-pane label="订单列表" name="orders">
        <el-table :data="orders" border>
          <el-table-column label="订单号" prop="orderId" width="180" />
          <el-table-column label="用户" prop="user" />
          <el-table-column label="产品" prop="product" />
          <el-table-column label="金额" prop="amount" width="100" />
          <el-table-column label="时间" prop="time" width="180" />
          <el-table-column label="状态" width="100">
            <template #default="scope">
              <el-tag :type="getStatusType(scope.row.status)">{{ scope.row.status }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="120" align="center">
            <template #default>
              <el-button type="primary" link icon="Document">详情</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <el-tab-pane label="套餐定价" name="packages">
        <el-row :gutter="20">
          <el-col :span="8" v-for="pkg in packages" :key="pkg.name">
            <el-card header="{{ pkg.name }}">
              <div class="pkg-price">￥{{ pkg.price }} / {{ pkg.unit }}</div>
              <ul class="pkg-features">
                <li v-for="f in pkg.features" :key="f">{{ f }}</li>
              </ul>
              <div class="text-right"><el-button type="primary" size="small">修改配置</el-button></div>
            </el-card>
          </el-col>
        </el-row>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
const activeTab = ref('orders')
const financeKpis = ref([
  { label: '今日收入', value: '4,520.00', trend: 12.5 },
  { label: '本月总额', value: '128,400.00', trend: 8.2 },
  { label: '待支付订单', value: 12, trend: -5.1 },
  { label: '退款审核中', value: 3, trend: 0 }
])
const orders = ref([
  { orderId: 'ORD20260104001', user: '张三 (13800138000)', product: 'VIP 个人月度套餐', amount: '￥99.00', time: '2026-01-04 15:00:00', status: '已支付' },
  { orderId: 'ORD20260104002', user: '李四 (13900139001)', product: '企业识别点数包 (10万次)', amount: '￥1,999.00', time: '2026-01-04 14:30:00', status: '已支付' }
])
const packages = ref([
  { name: 'FREE 体验版', price: 0, unit: '永久', features: ['20次/日 识别限额', '基础技术支持', '保留1周记录'] },
  { name: 'VIP 个人版', price: 99, unit: '月', features: ['500次/日 识别限额', '优先排队通道', '保留1年记录', '高级图像增强'] },
  { name: 'ENTERPRISE 企业版', price: 999, unit: '月起', features: ['不限量识别', '定制化 API 接入', '数据私有化部署', '24/7 技术支持'] }
])

function getStatusType(s: string) {
  if (s === '已支付') return 'success'
  if (s === '待支付') return 'warning'
  return 'info'
}
</script>

<style scoped>
.kpi-label { font-size: 14px; color: #666; }
.kpi-value { font-size: 24px; font-weight: bold; margin: 8px 0; }
.kpi-trend { font-size: 12px; }
.up { color: #f56c6c; }
.down { color: #67c23a; }
.mt-4 { margin-top: 20px; }
.pkg-price { font-size: 20px; font-weight: bold; color: var(--el-color-primary); margin-bottom: 12px; }
.pkg-features { list-style: none; padding: 0; font-size: 13px; color: #666; margin-bottom: 12px; }
.pkg-features li { margin-bottom: 6px; }
.text-right { text-align: right; }
</style>
