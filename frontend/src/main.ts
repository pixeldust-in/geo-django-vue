import { createApp } from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import  VueGoogleMaps from '@fawmi/vue-google-maps'
import './assets/base.css'

createApp(App).use(store).use(router)
.use(VueGoogleMaps, {
  load: {
    key: "AIzaSyCcX-UvqSA_VwA1SNm9VfAcVj38RmG9QlI",
    libraries: "places"
  }
}).mount('#app')
