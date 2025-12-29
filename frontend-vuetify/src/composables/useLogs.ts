import { ref, onMounted, onBeforeUnmount } from 'vue'

export const logs = ref<string[]>([])
export function clearLogs() {
  logs.value = []
}

let websocket: WebSocket | null = null
let reconnectTimer: number | null = null
const maxLogs = 1000

function connectWebSocket() {
  const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
  const url = new URL(apiBaseUrl)
  const protocol = url.protocol === 'https:' ? 'wss:' : 'ws:'
  const wsUrl = `${protocol}//${url.host}/ws/logs`

  websocket = new WebSocket(wsUrl)

  websocket.addEventListener('open', () => {
    console.log('WebSocket连接已建立')
  })

  websocket.addEventListener('message', (event) => {
    const message = event.data
    logs.value.push(message)

    if (logs.value.length > maxLogs) {
      logs.value = logs.value.slice(-maxLogs)
    }
  })

  websocket.addEventListener('close', () => {
    console.log('WebSocket连接已关闭，尝试重连...')
    websocket = null
    reconnectTimer = window.setTimeout(connectWebSocket, 5000)
  })

  websocket.addEventListener('error', (error) => {
    console.error('WebSocket错误:', error)
  })
}

export function useLogs() {
  onMounted(() => {
    if (!websocket) {
      connectWebSocket()
    }
  })

  onBeforeUnmount(() => {
    if (websocket) {
      websocket.close()
    }
    if (reconnectTimer) {
      clearTimeout(reconnectTimer)
    }
  })
}
