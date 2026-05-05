import { reactive } from 'vue'

export const toast = reactive({
  show: false,
  message: '',
  type: 'success', // 'success', 'error', 'info'
  duration: 3000,
  
  success(msg) {
    this.showNotify(msg, 'success')
  },
  
  error(msg) {
    this.showNotify(msg, 'error')
  },
  
  info(msg) {
    this.showNotify(msg, 'info')
  },
  
  showNotify(message, type) {
    this.message = message
    this.type = type
    this.show = true
  }
})
