import axios from 'axios'
import { getToken } from './auth';

// 开发默认 127.0.0.1:8080，生产通过 .env.production 或构建时设置 VUE_APP_API_BASE_URL
const URL = process.env.VUE_APP_API_BASE_URL || "http://127.0.0.1:8080"
// create an axios instance
const service = axios.create({
    baseURL: URL, // url = base url + request url
    timeout: 10000,// request timeout
    withCredentials: true,
    crossDomain: true

})

// http request 拦截器
service.interceptors.request.use(
    config => {
        if (getToken()) {
            config.headers.Authorization =`Bearer ${getToken()}`;
        }
        return config
    },
    error => {
        return Promise.reject(error)
    }
)
service.interceptors.response.use(
    response => {
        if (response.status === 200) {
            return response.data
        }
        return Promise.reject(new Error(response.statusText || 'Error'));
    },
    error => {
        return Promise.reject(error)
    }
)

export default service
