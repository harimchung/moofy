import Vue from 'vue'
import App from './App.vue'
import store from './store'
import router from './router'
import axios from 'axios'
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'

// font-awesome 이용하기
import { library } from "@fortawesome/fontawesome-svg-core";
import {  faChevronLeft, faChevronRight, faStar, faMagnifyingGlass } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
library.add( faChevronLeft, faChevronRight,  faStar, faMagnifyingGlass )
Vue.component('font-awesome-icon', FontAwesomeIcon)


// vue-apex-charts 이용하기
import VueApexCharts from 'vue-apexcharts'
Vue.use(VueApexCharts)
Vue.component('apexchart', VueApexCharts)



Vue.config.productionTip = false

new Vue({
  store,
  router,
  render: h => h(App),

  created: function () {
    axios({
      method:'get',
      url:'http://127.0.0.1:8000/movies/'
    }).then(res=>{
      this.$store.commit('LOAD_MOVIE', res.data)
      this.$store.dispatch('calculateAge')
      this.$store.dispatch('calculateLogout')
    }).catch(err=>{
      console.log(err)
    })
    
  }
}).$mount('#app')

