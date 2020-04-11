import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home' 
import PersonalInfo from '@/components/PersonalInfo'
import MyShop from '@/components/MyShop'
import ShopSystem from '@/components/ShopSystem'
import DishesManagement from '@/components/DishesManagement'
import OrderManagement from '@/components/OrderManagement'
import Information from '@/components/Information'
// import Sidebar from '@/components/Sidebar'
// import Content from '@/components/Content'
// import Header from '@/components/Header'

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/',
            name: 'Home',
            component: Home
        },
        // {
        //     path: '/sidebar',
        //     name: 'Sidebar',
        //     component: Sidebar
        // },
        // {
        //     path: '/header',
        //     name: 'Header',
        //     component: Header
        // },
        // {
        //     path: '/content',
        //     name: 'Content',
        //     component: Content
        // },
        {
            path: '/personalinfo',
            name: 'PersonalInfo',
            component: PersonalInfo
        },
        {
            path: '/myshop',
            name: 'MyShop',
            component: MyShop
        },
        {
            path: '/shopsystem',
            name: 'ShopSystem',
            component: ShopSystem
        },
        {
            path: '/dishesmanagement',
            name: 'DishesManagement',
            component: DishesManagement
        },
        {
            path: '/ordermanagement',
            name: 'OrderManagement',
            component: OrderManagement
        },
        {
            path: '/information',
            name: 'Information',
            component: Information
        }
        
    ]
})