import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.js'
import axios from 'axios'
import 'vue3-toastify/dist/index.css'
import router from "./router/index.js";
import App from "@/App.vue";
import {createApp} from "vue";

axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
axios.defaults.xsrfCookieName = 'csrftoken'

axios.defaults.baseURL = 'http://127.0.0.1:8000/'

axios.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token')
        if (!token) {
            router.push('/auth')
        } else if (token) {
            config.headers['Authorization'] = `Bearer ${token}`
        }

        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

const app = createApp(App)
app.use(router)
app.mount('#app')
