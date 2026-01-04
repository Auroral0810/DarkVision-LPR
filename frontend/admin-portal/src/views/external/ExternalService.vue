<template>
  <div class="app-container">
    <el-tabs type="border-card">
      <el-tab-pane label="对象存储 (OSS)">
        <el-form label-width="140px">
          <el-form-item label="存储类型">
            <el-radio-group v-model="oss.type">
              <el-radio label="aliyun">阿里云 OSS</el-radio>
              <el-radio label="minio">MinIO (内置)</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="Endpoint">
            <el-input v-model="oss.endpoint" />
          </el-form-item>
          <el-form-item label="AccessKey ID">
            <el-input v-model="oss.ak" type="password" show-password />
          </el-form-item>
          <el-form-item label="AccessKey Secret">
            <el-input v-model="oss.sk" type="password" show-password />
          </el-form-item>
          <el-form-item label="Bucket 名称">
            <el-input v-model="oss.bucket" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary">连接测试</el-button>
            <el-button type="success">保存配置</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <el-tab-pane label="支付网关">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-card header="微信支付">
              <el-form label-width="80px">
                <el-form-item label="AppID"><el-input v-model="pay.wx.appId" /></el-form-item>
                <el-form-item label="MchID"><el-input v-model="pay.wx.mchId" /></el-form-item>
                <el-form-item label="已启用"><el-switch v-model="pay.wx.enabled" /></el-form-item>
              </el-form>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card header="支付宝">
              <el-form label-width="80px">
                <el-form-item label="AppID"><el-input v-model="pay.ali.appId" /></el-form-item>
                <el-form-item label="已启用"><el-switch v-model="pay.ali.enabled" /></el-form-item>
              </el-form>
            </el-card>
          </el-col>
        </el-row>
      </el-tab-pane>

      <el-tab-pane label="第三方登录">
        <el-table :data="oauth" border>
          <el-table-column label="平台" prop="platform" width="120" />
          <el-table-column label="ClientID" prop="clientId" />
          <el-table-column label="状态" width="100">
            <template #default="scope"><el-switch v-model="scope.row.enabled" /></template>
          </el-table-column>
          <el-table-column label="操作" width="100">
            <template #default><el-button type="primary" link>编辑</el-button></template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
const oss = reactive({ type: 'aliyun', endpoint: 'oss-cn-beijing.aliyuncs.com', ak: '************', sk: '************', bucket: 'darkvision-lpr' })
const pay = reactive({
  wx: { appId: 'wx1234567890', mchId: '12345678', enabled: true },
  ali: { appId: '20210000000', enabled: true }
})
const oauth = ref([
  { platform: '微信', clientId: 'wx_oauth_123', enabled: true },
  { platform: 'QQ', clientId: 'qq_oauth_456', enabled: false },
  { platform: 'GitHub', clientId: 'gh_oauth_789', enabled: true }
])
</script>
