import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import clickOutside from './directives/clickOutside'
import FButton from './components/common/FButton.vue'

const app = createApp(App)

app.component('FButton', FButton)
app.use(createPinia())
app.use(router)
app.use(vuetify)
app.directive('click-outside', clickOutside)

app.mount('#app')