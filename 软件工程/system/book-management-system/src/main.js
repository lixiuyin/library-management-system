import Vue from 'vue'
import App from './App.vue'
import router from './router' //引入vue-router
import store from  './store'
import ElementUI from 'element-ui'; //全局引入element
import 'element-ui/lib/theme-chalk/index.css';
import axios from "axios";

Vue.config.productionTip = false
Vue.use(ElementUI);     //全局注入element
new Vue({
  render: h => h(App),
  router,
  store
}).$mount('#app')

