<template>
  <!-- 悬浮按钮 -->
  <div class="ai-assistant">
    <!-- AI 助手图标按钮 -->
    <el-button
      v-if="!dialogVisible"
      class="ai-fab-button"
      type="primary"
      circle
      size="large"
      @click="handleOpen"
    >
      <div class="i-svg:ai ai-icon" />
    </el-button>

    <!-- AI 对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="AI 智能助手"
      width="600px"
      :close-on-click-modal="false"
      draggable
      class="ai-assistant-dialog"
    >
      <template #header>
        <div class="dialog-header">
          <div class="i-svg:ai header-icon" />
          <span class="title">AI 智能助手</span>
        </div>
      </template>

      <!-- 命令输入 -->
      <div class="command-input">
        <el-input
          v-model="command"
          type="textarea"
          :rows="3"
          placeholder="试试说：修改test用户的姓名为测试人员&#10;或者：跳转到用户管理&#10;按 Ctrl+Enter 快速发送"
          :disabled="loading"
          @keydown.ctrl.enter="handleExecute"
        />
      </div>

      <!-- 快捷命令示例 -->
      <div class="quick-commands">
        <div class="section-title">💡 试试这些命令：</div>
        <el-tag
          v-for="example in examples"
          :key="example"
          class="command-tag"
          @click="command = example"
        >
          {{ example }}
        </el-tag>
      </div>

      <!-- AI 响应结果 -->
      <div v-if="response" class="ai-response">
        <el-alert :title="response.explanation" type="success" :closable="false" show-icon />

        <!-- 将要执行的操作 -->
        <div v-if="response.action" class="action-preview">
          <div class="action-title">🎯 将要执行：</div>
          <div class="action-content">
            <div v-if="response.action.type === 'navigate'">
              <el-icon><Position /></el-icon>
              跳转到：
              <strong>{{ response.action.pageName }}</strong>
              <span v-if="response.action.query" class="query-info">
                并搜索：
                <el-tag type="warning" size="small">{{ response.action.query }}</el-tag>
              </span>
            </div>
            <div v-if="response.action.type === 'navigate-and-execute'">
              <el-icon><Position /></el-icon>
              跳转至：
              <strong>{{ response.action.pageName }}</strong>
              <span v-if="response.action.query" class="query-info">
                并搜索：
                <el-tag type="warning" size="small">{{ response.action.query }}</el-tag>
              </span>
              <el-divider direction="vertical" />
              <el-icon><Tools /></el-icon>
              执行：
              <strong>{{ response.action.functionCall.name }}</strong>
            </div>
            <div v-if="response.action.type === 'execute'">
              <el-icon><Tools /></el-icon>
              执行：
              <strong>{{ response.action.functionName }}</strong>
            </div>
          </div>
        </div>
      </div>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="handleClose">取消</el-button>
          <el-button type="primary" :loading="loading" @click="handleExecute">
            <el-icon><MagicStick /></el-icon>
            执行命令
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onBeforeUnmount } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { Position, Tools, MagicStick } from "@element-plus/icons-vue";
import AiCommandApi from "@/api/ai";

const router = useRouter();

type ToolFunctionCall = {
  name: string;
  arguments: Record<string, any>;
};

// 统一的动作描述（区分“跳转”、“跳转+执行”、“仅执行”三种场景）
type AiAction =
  | {
      type: "navigate";
      path: string;
      pageName: string;
      query?: string;
    }
  | {
      type: "navigate-and-execute";
      path: string;
      pageName: string;
      query?: string;
      functionCall: ToolFunctionCall;
      parseLogId?: string; // Add parseLogId
    }
  | {
      type: "execute";
      functionName: string;
      functionCall: ToolFunctionCall;
      parseLogId?: string; // Add parseLogId
    };

type AiResponse = {
  explanation: string;
  action: AiAction | null;
};

// 状态管理
const dialogVisible = ref(false);
const command = ref("");
const loading = ref(false);
const response = ref<AiResponse | null>(null);

// 快捷命令示例
const examples = [
  "修改test用户的姓名为测试人员",
  "获取姓名为张三的用户信息",
  "跳转到用户管理",
  "打开角色管理页面",
];

// 打开对话框
const handleOpen = () => {
  dialogVisible.value = true;
  command.value = "";
  response.value = null;
};

// 关闭对话框
const handleClose = () => {
  dialogVisible.value = false;
  command.value = "";
  response.value = null;
};

// 执行命令
const handleExecute = async () => {
  const rawCommand = command.value.trim();
  if (!rawCommand) {
    ElMessage.warning("请输入命令");
    return;
  }

  // 优先检测无需调用 AI 的纯跳转命令
  const directNavigation = tryDirectNavigate(rawCommand);
  if (directNavigation && directNavigation.action) {
    response.value = directNavigation;
    await executeAction(directNavigation.action);
    return;
  }

  loading.value = true;

  try {
    // 调用 AI API 解析命令
    const result = await AiCommandApi.parseCommand({
      command: rawCommand,
      currentRoute: router.currentRoute.value.path,
      currentComponent: router.currentRoute.value.name as string,
      context: {
        userRoles: [],
      },
    });

    if (!result.success) {
      ElMessage.error(result.error || "命令解析失败");
      return;
    }

    // 解析 AI 返回的操作类型
    const action = parseAction(result, rawCommand);
    response.value = {
      explanation: result.explanation ?? "命令解析成功，准备执行操作",
      action,
    };

    // 等待用户确认后执行
    if (action) {
      await executeAction(action);
    }
  } catch (error: any) {
    console.error("AI 命令执行失败:", error);
    ElMessage.error(error.message || "命令执行失败");
  } finally {
    loading.value = false;
  }
};

// 路由配置映射表（自动从 lprRoutes 提取）
const routeConfig = [
  { keywords: ["dashboard", "首页", "控制台", "overview"], path: "/dashboard/overview", name: "控制台首页" },
  // 用户管理
  { keywords: ["用户", "user", "user list", "人员"], path: "/user/list", name: "用户列表" },
  { keywords: ["实名", "verification", "auth", "certification"], path: "/user/verification", name: "实名认证审核" },
  { keywords: ["标签", "tag", "用户标签"], path: "/user/tags", name: "用户标签管理" },
  // 权限与管理员
  { keywords: ["角色", "role"], path: "/permission/role", name: "角色管理" },
  { keywords: ["权限", "permission"], path: "/permission/management", name: "权限管理" },
  { keywords: ["管理员", "admin", "admin account"], path: "/permission/admin", name: "管理员账户" },
  // 识别服务
  { keywords: ["识别任务", "task", "监控", "识别监控", "task monitor"], path: "/recognition/tasks", name: "任务监控" },
  { keywords: ["识别记录", "record", "history"], path: "/recognition/records", name: "识别记录" },
  { keywords: ["识别模型", "model", "算法", "algorithm"], path: "/recognition/models", name: "模型管理" },
  // 内容运营
  { keywords: ["官网内容", "content", "site"], path: "/content/site", name: "官网内容" },
  { keywords: ["文档", "doc", "document"], path: "/content/docs", name: "文档管理" },
  { keywords: ["公告", "announcement", "notice"], path: "/content/announcement", name: "公告管理" },
  { keywords: ["FAQ", "question", "help", "常见问题"], path: "/content/faq", name: "FAQ 管理" },
  // 订单与财务
  { keywords: ["订单", "order", "payment"], path: "/finance/orders", name: "订单管理" },
  { keywords: ["套餐", "package", "plan"], path: "/finance/packages", name: "套餐管理" },
  { keywords: ["财务", "finance", "report", "报表"], path: "/finance/reports", name: "财务报表" },
  // 统计分析
  { keywords: ["用户统计", "user stats", "user analysis", "分析", "analysis"], path: "/statistics/user", name: "用户统计" },
  { keywords: ["识别统计", "recognition stats", "识别分析", "analysis"], path: "/statistics/recognition", name: "识别统计" },
  { keywords: ["看板", "dashboard", "board", "business"], path: "/statistics/board", name: "业务看板" },
  // 日志与安全
  { keywords: ["操作日志", "operation log", "oplog"], path: "/log/operation", name: "操作日志" },
  { keywords: ["系统日志", "system log", "syslog"], path: "/log/system", name: "系统日志" },
  { keywords: ["安全", "security"], path: "/log/security", name: "安全配置" },
  // 系统配置
  { keywords: ["配置", "setting", "config", "基础配置"], path: "/setting/base", name: "基础配置" },
  { keywords: ["参数", "param", "识别参数"], path: "/setting/params", name: "识别参数" },
  { keywords: ["限额", "quota", "limit"], path: "/setting/quotas", name: "限额配置" },
  { keywords: ["邮件", "短信", "sms", "email", "消息", "通知"], path: "/setting/email-sms", name: "邮件 & 短信" },
  // 第三方服务
  { keywords: ["存储", "storage", "oss"], path: "/external/storage", name: "存储配置" },
  { keywords: ["支付", "payment", "pay"], path: "/external/payment", name: "支付配置" },
  { keywords: ["第三方登录", "login", "oauth"], path: "/external/login", name: "第三方登录" },
  // 系统维护
  { keywords: ["缓存", "cache"], path: "/maintenance/cache", name: "缓存管理" },
  { keywords: ["任务调度", "任务", "调度", "定时任务"], path: "/maintenance/tasks", name: "任务调度" },
  { keywords: ["版本", "更新", "version", "upgrade"], path: "/maintenance/version", name: "版本更新" },
  // 备份与恢复
  { keywords: ["备份", "backup", "数据备份"], path: "/backup/data", name: "数据备份" },
  { keywords: ["恢复", "recover", "数据恢复"], path: "/backup/recover", name: "数据恢复" },
];

// 根据函数名推断路由（如 getUserInfo -> /system/user）
const normalizeText = (text: string) => text.replace(/\s+/g, " ").trim().toLowerCase();

const inferRouteFromFunction = (functionName: string) => {
  const fnLower = normalizeText(functionName);
  for (const config of routeConfig) {
    // 检查函数名是否包含关键词（如 getUserInfo 包含 user）
    if (config.keywords.some((kw) => fnLower.includes(kw.toLowerCase()))) {
      return { path: config.path, name: config.name };
    }
  }
  return null;
};

// 根据命令文本匹配路由
const matchRouteFromCommand = (cmd: string) => {
  const normalized = normalizeText(cmd);
  for (const config of routeConfig) {
    if (config.keywords.some((kw) => normalized.includes(kw.toLowerCase()))) {
      return { path: config.path, name: config.name };
    }
  }
  return null;
};

const extractKeywordFromCommand = (cmd: string): string => {
  const normalized = normalizeText(cmd);
  // 从 routeConfig 动态获取所有数据类型关键词
  const allKeywords = routeConfig.flatMap((config) =>
    config.keywords.map((kw) => kw.toLowerCase())
  );
  const keywordsPattern = allKeywords.join("|");

  const patterns = [
    new RegExp(`(?:查询|获取|搜索|查找|找).*?([^\\s，,。]+?)(?:的)?(?:${keywordsPattern})`, "i"),
    new RegExp(`(?:${keywordsPattern}).*?([^\\s，,。]+?)(?:的|信息|详情)?`, "i"),
    new RegExp(
      `(?:姓名为|名字叫|叫做|名称为|名是|为)([^\\s，,。]+?)(?:的)?(?:${keywordsPattern})?`,
      "i"
    ),
    new RegExp(`([^\\s，,。]+?)(?:的)?(?:${keywordsPattern})(?:信息|详情)?`, "i"),
  ];

  for (const pattern of patterns) {
    const match = normalized.match(pattern);
    if (match && match[1]) {
      let extracted = match[1].trim();
      extracted = extracted.replace(/姓名为|名字叫|叫做|名称为|名是|为|的|信息|详情/g, "");
      if (
        extracted &&
        !allKeywords.some((type) => extracted.toLowerCase().includes(type.toLowerCase()))
      ) {
        return extracted;
      }
    }
  }
  return "";
};

const tryDirectNavigate = (rawCommand: string): AiResponse | null => {
  const navigationIntents = ["跳转", "打开", "进入", "前往", "去", "浏览", "查看"];
  const operationIntents = [
    "修改",
    "更新",
    "变更",
    "删除",
    "添加",
    "创建",
    "设置",
    "获取",
    "查询",
    "搜索",
  ];

  const hasNavigationIntent = navigationIntents.some((keyword) => rawCommand.includes(keyword));
  const hasOperationIntent = operationIntents.some((keyword) => rawCommand.includes(keyword));

  if (!hasNavigationIntent || hasOperationIntent) {
    return null;
  }

  const routeInfo = matchRouteFromCommand(rawCommand);
  if (!routeInfo) {
    return null;
  }

  const keyword = extractKeywordFromCommand(rawCommand);
  const action: AiAction = {
    type: "navigate",
    path: routeInfo.path,
    pageName: routeInfo.name,
    query: keyword || undefined,
  };

  return {
    explanation: `检测到跳转命令，正在前往 ${routeInfo.name}`,
    action,
  };
};

// 解析 AI 返回的操作类型
const parseAction = (result: any, rawCommand: string): AiAction | null => {
  const cmd = normalizeText(rawCommand);
  const primaryCall = result.functionCalls?.[0];
  const functionName = primaryCall?.name;
  const parseLogId = result.parseLogId; // Extract log ID

  // 优先从函数名推断路由，其次从命令文本匹配
  let routeInfo = functionName ? inferRouteFromFunction(functionName) : null;
  if (!routeInfo) {
    routeInfo = matchRouteFromCommand(cmd);
  }

  const routePath = routeInfo?.path || "";
  const pageName = routeInfo?.name || "";
  const keyword = extractKeywordFromCommand(cmd);

  if (primaryCall && functionName) {
    const fnNameLower = functionName.toLowerCase();

    // 1) 查询类函数 -> 跳转并执行筛选
    const isQueryFunction =
      fnNameLower.includes("query") ||
      fnNameLower.includes("search") ||
      fnNameLower.includes("list") ||
      fnNameLower.includes("get");

    if (isQueryFunction) {
       if (routePath) {
        return {
          type: "navigate-and-execute",
          path: routePath,
          pageName,
          functionCall: primaryCall,
          query: keyword || undefined, // Assume keyword extraction logic is same
          parseLogId
        };
       }
    }

    // 2) 其他操作类函数 -> 跳转并执行
    // ... (keep match logic)
    // 3) 其他匹配
    if (routePath) {
      return {
        type: "navigate-and-execute",
        path: routePath,
        pageName,
        functionCall: primaryCall,
        parseLogId
      };
    }

    return {
      type: "execute",
      functionName,
      functionCall: primaryCall,
      parseLogId
    };
  }

  // 4) 无函数调用，仅跳转
  if (routePath) {
    return {
      type: "navigate",
      path: routePath,
      pageName,
      query: keyword || undefined,
    };
  }

  return null;
};

// 定时器引用（用于清理）
let navigationTimer: ReturnType<typeof setTimeout> | null = null;
let executeTimer: ReturnType<typeof setTimeout> | null = null;

// 执行操作
const executeAction = async (action: AiAction) => {
  // 🎯 新增：跳转并执行操作
  if (action.type === "navigate-and-execute") {
    
    // 如果是修改类操作 (非查询)，先调用后端执行，再跳转
    const isModify = action.parseLogId && !action.query; 
    
    if (isModify) {
        ElMessage.warning(`正在执行操作: ${action.functionCall.name}...`);
        try {
            await AiCommandApi.executeCommand({
                parseLogId: action.parseLogId,
                functionCall: action.functionCall,
                currentRoute: router.currentRoute.value.path
            });
            ElMessage.success("操作执行成功，正在前往页面查看...");
        } catch (e: any) {
            console.error(e);
            ElMessage.error("操作执行失败，请重试");
            return; // 失败则中止
        }
    } else {
        ElMessage.success(`正在跳转到 ${action.pageName} ...`);
    }

    // 清理之前的定时器
    if (navigationTimer) {
      clearTimeout(navigationTimer);
    }

    // 跳转
    navigationTimer = setTimeout(() => {
      navigationTimer = null;
      const queryParams: any = {};
      
      // 如果不是为了执行(已经执行过了)，就不传 aiAction 参数避免重复
      // 但为了让页面知道刚刚发生了操作（可能触发刷新），还是可以传个标记
      if (isModify) {
          queryParams.actionResult = "success";
          queryParams._t = Date.now();
      } else {
           // 如果是查询类或者未执行的，传递 aiAction 让页面处理 (如果有的话)
           // 目前页面可能还没实现处理 aiAction，但保留机制
           queryParams.aiAction = encodeURIComponent(
              JSON.stringify({
                functionName: action.functionCall.name,
                arguments: action.functionCall.arguments,
                timestamp: Date.now(),
              })
            );
      }

      // 如果有查询关键字，也一并传递 (查询类)
      if (action.query) {
        queryParams.keywords = action.query;
        queryParams.autoSearch = "true";
      }

      router.push({
        path: action.path,
        query: queryParams,
      });

      // 关闭对话框
      handleClose();
    }, 800);
    return;
  }
  
  if (action.type === "navigate") {
    // 检查是否已经在目标页面
    const currentPath = router.currentRoute.value.path;

    if (currentPath === action.path) {
      // 如果已经在目标页面
      if (action.query) {
        // ...
        router.replace({
          path: action.path,
          query: {
            keywords: action.query,
            autoSearch: "true",
            _t: Date.now().toString(), // 添加时间戳强制刷新
          },
        });
      } else {
        ElMessage.warning(`您已经在 ${action.pageName} 页面了`);
      }
      handleClose();
      return;
    }

    // 不在目标页面，正常跳转
    ElMessage.success(`正在跳转到 ${action.pageName}...`);
     if (navigationTimer) clearTimeout(navigationTimer);
    
    navigationTimer = setTimeout(() => {
      navigationTimer = null;
      router.push({
        path: action.path,
        query: action.query
          ? {
              keywords: action.query, // 传递关键字参数
              autoSearch: "true", // 标记自动搜索
            }
          : undefined,
      });
      handleClose();
    }, 800);
    return;
  }

  if (action.type === "execute") {
    // 执行函数调用 - 现在真正执行
    if (action.parseLogId) {
        ElMessage.info(`正在执行: ${action.functionName || '操作'}...`);
        try {
            const res = await AiCommandApi.executeCommand({
                parseLogId: action.parseLogId,
                functionCall: action.functionCall,
                currentRoute: router.currentRoute.value.path
            });
            ElMessage.success(res.message || "执行成功");
            handleClose();
        } catch (e: any) {
            ElMessage.error(e.message || "执行失败");
        }
    } else {
        ElMessage.warning("无法执行：缺少必要信息");
    }
  }
};

// 组件卸载时清理定时器
onBeforeUnmount(() => {
  if (navigationTimer) {
    clearTimeout(navigationTimer);
    navigationTimer = null;
  }
  if (executeTimer) {
    clearTimeout(executeTimer);
    executeTimer = null;
  }
});
</script>

<style scoped lang="scss">
.ai-assistant {
  .ai-fab-button {
    position: fixed;
    right: 30px;
    bottom: 80px;
    z-index: 9999;
    width: 60px;
    height: 60px;
    box-shadow: 0 4px 12px rgba(2, 119, 252, 0.4);
    transition: all 0.3s ease;

    &:hover {
      box-shadow: 0 6px 20px rgba(2, 119, 252, 0.6);
      transform: scale(1.1);
    }

    .ai-icon {
      width: 32px;
      height: 32px;
    }
  }
}

.ai-assistant-dialog {
  .dialog-header {
    display: flex;
    gap: 12px;
    align-items: center;

    .header-icon {
      width: 28px;
      height: 28px;
    }

    .title {
      font-size: 18px;
      font-weight: 600;
      color: var(--el-text-color-primary);
    }
  }

  .command-input {
    margin-bottom: 16px;
  }

  .quick-commands {
    margin-bottom: 20px;

    .section-title {
      margin-bottom: 8px;
      font-size: 14px;
      color: var(--el-text-color-secondary);
    }

    .command-tag {
      margin-right: 8px;
      margin-bottom: 8px;
      cursor: pointer;
      transition: all 0.3s;

      &:hover {
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
      }
    }
  }

  .ai-response {
    margin-top: 16px;

    .action-preview {
      padding: 12px;
      margin-top: 12px;
      background-color: var(--el-fill-color-light);
      border-radius: 8px;

      .action-title {
        margin-bottom: 8px;
        font-size: 14px;
        font-weight: 600;
        color: var(--el-text-color-primary);
      }

      .action-content {
        display: flex;
        gap: 8px;
        align-items: center;
        color: var(--el-text-color-regular);

        .el-icon {
          color: var(--el-color-primary);
        }

        .query-info {
          margin-left: 8px;
        }
      }
    }
  }

  .dialog-footer {
    display: flex;
    gap: 12px;
    justify-content: flex-end;
  }
}
</style>
