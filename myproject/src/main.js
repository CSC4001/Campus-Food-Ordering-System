// import Vue from 'vue'
// import App from './App.vue'

// Vue.config.productionTip = false

// new Vue({
//   render: h => h(App),
// }).$mount('#app')

import Vue from 'vue';
import App from './App';
import router from './router'
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/antd.css';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import Avue from '@smallwei/avue';
import '@smallwei/avue/lib/index.css';


Vue.config.productionTip = false;

Vue.use(Antd);
Vue.use(ElementUI);
Vue.use(Avue)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  render: h => h(App),
  
  
});