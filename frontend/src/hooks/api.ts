import Cookies from 'universal-cookie';
import axios from 'axios'

const cookies = new Cookies();

const axiosInstance = axios.create({
  baseURL: '/api/',
  headers: {Accept: 'application/json',
  'Content-Type': 'application/json',
  'X-Requested-With': 'XMLHttpRequest',
  'Cache-Control': 'no-cache',
  'X-CSRFToken': cookies.get('csrftoken'),},
  withCredentials: true,

})


axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    const code = error && error.response ? error.response.status : 0
    if (code === 500) {
      alert('A server error occurred, Please try again later!')
    }
    return Promise.reject(error)
  },
)

export const post = async (url:string, data: object) => {
  try {
    const response = await axiosInstance.post(url, data)
    return response
  } catch (error:any) {
    if(error.response.status === 400){
      let message = error.response.data.message
      message = Array.isArray(message) ? message[0] : message
      message && alert(message)
    }
    return error?.response as any
  }
}

export const get = async (url: string, params = {}) => {
  try {
    const response = await axiosInstance.get(url, { params })
    return response
  } catch (error:any) {
    if(error.response.status === 400){
      let message = error.response.data.message
      message = Array.isArray(message) ? message[0] : message
      message && alert(message)
    }
    return error?.response as any
  }
}

export const put = async (url:string, data?: object) => {
  try {
    const response = await axiosInstance.put(url, data)
    return response
  } catch (error:any) {
    if(error.response.status === 400){
      let message = error.response.data.message
      message = Array.isArray(message) ? message[0] : message
      message && alert(message)
    }
    return error?.response as any
  }
}

const api = {
    get, post, put
}

export default api