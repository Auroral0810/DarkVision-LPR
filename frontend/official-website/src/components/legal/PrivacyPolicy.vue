<template>
  <div class="legal-doc">
    <h4>1. 信息收集</h4>
    <p>我们收集的信息包括但不限于：用户注册信息（邮箱、手机号）、使用记录、API调用数据等。所有数据均用于提供和改进服务。</p>
    
    <h4>2. 信息使用</h4>
    <p>您的信息将用于：</p>
    <ul>
      <li>提供车牌识别服务</li>
      <li>发送服务通知和更新</li>
      <li>改进我们的算法和系统性能</li>
      <li>防止欺诈和滥用</li>
    </ul>

    <h4>3. 数据安全</h4>
    <p>我们采用行业标准的加密技术（如SSL/TLS）来保护您的数据传输和存储安全。所有敏感数据均经过加密处理。</p>

    <h4>4. Cookie 使用</h4>
    <p>我们使用 Cookie 来改善用户体验，记住您的偏好设置，并分析流量。您可以随时在浏览器设置中管理 Cookie。</p>

    <h4>5. 第三方服务</h4>
    <p>本服务可能包含指向第三方网站的链接。我们不对第三方网站的内容或隐私做法负责。</p>
    
    <h4>6. 政策更新</h4>
    <p>我们需要时会更新本隐私政策。更新后的政策将在网站上公布。</p>
  </div>
</template>

<script setup lang="ts">
// Privacy Policy Content
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
