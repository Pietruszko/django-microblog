import axios from 'axios'

const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/',
    headers: {
        'Content-Type': 'application/json'
    }
})

api.interceptors.response.use(
    response => response,
    error => {
        if (error.response?.status === 401) {
            // Token is invalid - clear it
            localStorage.removeItem('token')
            window.location.href = '/login' // Full reload to reset state
        }
        return Promise.reject(error)
    }
)

const SKIP_AUTH_URLS = ['register', 'login']

api.interceptors.request.use(config => {
    if (SKIP_AUTH_URLS.some(url => config.url.includes(url))) {
        return config
    }

    const token = localStorage.getItem('token')
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
})

export default api