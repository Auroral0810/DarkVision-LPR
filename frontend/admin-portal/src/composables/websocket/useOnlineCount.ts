import { ref, onMounted, onUnmounted, getCurrentInstance, readonly } from "vue";
import StatsAPI from "@/api/stats-api";

/**
 * 全局单例实例
 */
let globalInstance: ReturnType<typeof createOnlineCountComposable> | null = null;

/**
 * 创建在线用户计数组合式函数（内部工厂函数）
 */
function createOnlineCountComposable() {
  // ==================== 状态管理 ====================
  const onlineUserCount = ref(0);
  const lastUpdateTime = ref(0);
  const isConnected = ref(false); // 模拟连接状态
  let pollingTimer: NodeJS.Timeout | null = null;

  /**
   * 获取在线用户数量
   */
  const fetchOnlineCount = async () => {
    try {
      const res = await StatsAPI.getOnlineUserCount();
      if (res && res.count !== undefined) {
        onlineUserCount.value = res.count;
        lastUpdateTime.value = Date.now();
        isConnected.value = true;
      }
    } catch (error) {
      console.error("[useOnlineCount] 获取在线用户数失败:", error);
      isConnected.value = false;
    }
  };

  /**
   * 初始化轮询
   */
  const initialize = () => {
    if (pollingTimer) return;

    console.log("[useOnlineCount] 初始化在线用户计数服务 (轮询模式)...");
    
    // 立即执行一次
    fetchOnlineCount();

    // 启动轮询 (每 30 秒)
    pollingTimer = setInterval(fetchOnlineCount, 30000);
    isConnected.value = true;
  };

  /**
   * 清理资源
   */
  const cleanup = () => {
    console.log("[useOnlineCount] 清理在线用户计数服务...");
    if (pollingTimer) {
      clearInterval(pollingTimer);
      pollingTimer = null;
    }
    isConnected.value = false;
    onlineUserCount.value = 0;
  };

  return {
    // 状态
    onlineUserCount: readonly(onlineUserCount),
    lastUpdateTime: readonly(lastUpdateTime),
    isConnected: readonly(isConnected),
    connectionState: ref("CONNECTED"), // 模拟 WebSocket 状态字符串

    // 方法
    initialize,
    cleanup,

    // 别名方法（向后兼容）
    initWebSocket: initialize,
    closeWebSocket: cleanup,
  };
}

/**
 * 在线用户计数组合式函数（单例模式）
 *
 * 用于实时显示系统在线用户数量
 *
 * @param options 配置选项
 * @param options.autoInit 是否在组件挂载时自动初始化（默认 true）
 */
export function useOnlineCount(options: { autoInit?: boolean } = {}) {
  const { autoInit = true } = options;

  // 获取或创建单例实例
  if (!globalInstance) {
    globalInstance = createOnlineCountComposable();
  }

  // 只在组件上下文中且 autoInit 为 true 时使用生命周期钩子
  const instance = getCurrentInstance();
  if (autoInit && instance) {
    onMounted(() => {
      // 只有在未连接时才尝试初始化
      if (!globalInstance!.isConnected.value) {
        globalInstance!.initialize();
      }
    });

    onUnmounted(() => {
      // 保持全局轮询，不自动停止，除非显式调用 cleanup
    });
  }

  return globalInstance;
}
