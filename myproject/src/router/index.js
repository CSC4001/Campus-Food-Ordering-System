import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
// import Header from '@/components/Header'
import Sidebar from '@/components/Sidebar'
// import Content from '@/components/Content'

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/',
            name: 'Home',
            component: Home
        },
        {
            path: '/test',
            name: 'Sidebar',
            component: Sidebar
        }
    ]
})