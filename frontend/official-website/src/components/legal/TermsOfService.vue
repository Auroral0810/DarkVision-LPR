<template>
  <div class="legal-doc">
    <h4>1. 服务接受</h4>
    <p>访问或使用 DarkVision LPR 系统，即表示您同意遵守本服务条款。如果您不同意这些条款，请停止使用本服务。</p>
    
    <h4>2. 用户账户</h4>
    <p>您需要注册账户才能使用我们的核心功能。您有责任维护账户信息的保密性，并对账户下的所有活动负责。</p>

    <h4>3. 使用限制</h4>
    <p>您不得：</p>
    <ul>
      <li>对系统进行反向工程或尝试提取源代码</li>
      <li>使用服务进行非法活动</li>
      <li>超出API调用限制或滥用服务资源</li>
      <li>转售或分发我们的服务（除非获得授权）</li>
    </ul>

    <h4>4. 知识产权</h4>
    <p>DarkVision LPR 及其所有相关软件、算法、设计和内容均为我们的知识产权，受版权法保护。</p>

    <h4>5. 免责声明</h4>
    <p>服务按"原样"提供，不包含任何明示或暗示的保证。我们不对识别结果的绝对准确性负责。</p>

    <h4>6. 终止条款</h4>
    <p>如果用户违反本条款，我们保留随时终止或暂停服务的权利。</p>
  </div>
</template>

<script setup lang="ts">
// Terms of Service Content
</script>

<style scoped lang="scss">
.legal-doc {
  color: #374151;
  line-height: 1.6;

  h4 {
    font-size: 16px;
    font-weight: 600;
    color: #111827;
    margin: 24px 0 12px;
    
    &:first-child {
      margin-top: 0;
    }
  }

  p {
    margin-bottom: 16px;
    text-align: justify;
  }

  ul {
    padding-left: 20px;
    margin-bottom: 16px;
    
    li {
      margin-bottom: 8px;
      list-style-type: disc;
    }
  }
}
</style>
