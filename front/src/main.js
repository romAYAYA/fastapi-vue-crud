import {createApp} from 'vue'
import './style.css'
import PrimeVue from 'primevue/config'
import App from './App.vue'
import Button from 'primevue/button'
import Toast from 'primevue/toast'
import ToastService from 'primevue/toastservice'
import Lara from './presets/lara/index.js'
import Dialog from 'primevue/dialog';

const app = createApp(App)
app.use(PrimeVue, {ripple: true, unstyled: true, pt: Lara})
app.use(ToastService)


app.component('Button', Button)
app.component('Toast', Toast)
app.component('Dialog', Dialog)

app.mount('#app')