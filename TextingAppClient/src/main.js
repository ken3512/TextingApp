import { createApp } from 'vue'

import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import naive from 'naive-ui'

axios.defaults.baseURL = 'http://127.0.0.1:8000'


const app = createApp(App)

app.use(naive)
app.use(store)
app.use(router, axios)
app.mount('#app')
