import { watch, onUnmounted } from 'vue'
import { useUserStore } from '@/store/user'
import { ElMessageBox } from 'element-plus'

export function useUserWebSocket() {
  const userStore = useUserStore()
  let ws: WebSocket | null = null
  let reconnectTimer: any = null
  let isForcedLogout = false

  const connect = () => {
    if (!userStore.token || !userStore.userInfo.id || isForcedLogout) return

    // 获取 API Base URL，并将 http 替换为 ws
    const apiBase = (import.meta as any)?.env?.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'
    const wsProtocol = apiBase.startsWith('https') ? 'wss' : 'ws'
    const wsBase = apiBase.replace(/^http(s)?/, wsProtocol)
    
    // 构建 WebSocket URL
    const wsUrl = `${wsBase}/ws/user/${userStore.userInfo.id}?token=${userStore.token}`

    ws = new WebSocket(wsUrl)

    ws.onopen = () => {
      console.log('[WebSocket] User connection established')
    }

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        // 处理强制下线
        if (data.type === 'force_logout') {
          handleForceLogout(data.message)
        }
        // 处理封禁 (如果需要单独处理)
        else if (data.type === 'user_banned') {
            handleForceLogout(data.message || '您的账号已被封禁')
        }
      } catch (e) {
        console.error('[WebSocket] Message parse error', e)
      }
    }

    ws.onclose = (e) => {
      console.log('[WebSocket] Disconnected', e.code)
      // 如果不是因为强制下线而关闭，且用户仍处于登录状态，则尝试重连
      if (!isForcedLogout && userStore.isLoggedIn) {
        if (reconnectTimer) clearTimeout(reconnectTimer)
        reconnectTimer = setTimeout(connect, 5000)
      }
    }
    
    ws.onerror = (e) => {
        console.error('[WebSocket] Error', e)
        ws?.close()
    }
  }

  const close = () => {
     if (ws) {
         ws.close()
         ws = null
     }
     if (reconnectTimer) {
         clearTimeout(reconnectTimer)
         reconnectTimer = null
     }
  }

  const handleForceLogout = (msg: string) => {
      isForcedLogout = true
      close() // 停止重连
      
      ElMessageBox.alert(msg || '您已被管理员强制下线，请重新登录', '下线通知', {
          confirmButtonText: '确定',
          type: 'warning',
          showClose: false,
          closeOnClickModal: false,
          closeOnPressEscape: false,
          callback: async () => {
              try {
                  // 清理状态
                  await userStore.logout()
              } catch (e) {
                  // ignore
              } finally {
                  window.location.href = '/login'
              }
          }
      })
  }

  // 监听登录状态变化
  watch(() => userStore.isLoggedIn, (val) => {
      if (val) {
          isForcedLogout = false
          connect()
      } else {
          close()
      }
  }, { immediate: true })

  onUnmounted(() => {
      close()
  })
}
