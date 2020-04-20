import Vue from 'vue'
import Router from 'vue-router'
//user 
import Home from '@/components/UserInterface/Home' 
import PersonalInfo from '@/components/UserInterface/PersonalInfo'
//shop
import MyShop from '@/components/MyShop'
import ShopSystem from '@/components/Shop/ShopSystem'
import DishesManagement from '@/components/Shop/DishesManagement'
import ShopOrderManagement from '@/components/Shop/OrderManagement'
import Information from '@/components/Shop/Information'
//admin
import AdminSystem from '@/components/Admin/AdminSystem'
import Application from '@/components/Admin/Application'
import UserManagement from '@/components/Admin/UserManagement'
import ShopManagement from '@/components/Admin/ShopManagement'
import AdminOrderManagement from '@/components/Admin/OrderManagement'
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
            path: '/shop/dishesmanagement',
            name: 'DishesManagement',
            component: DishesManagement
        },
        {
            path: '/shop/ordermanagement',
            name: 'ShopOrderManagement',
            component: ShopOrderManagement
        },
        {
            path: '/shop/information',
            name: 'Information',
            component: Information
        },
        {
            path: '/adminsystem',
            name: 'AdminSystem',
            component: AdminSystem
        },
        {
            path: '/admin/application',
            name: 'Application',
            component: Application
        },
        {
            path: '/admin/usermanagement',
            name: 'UserManagement',
            component: UserManagement
        },
        {
            path: '/admin/shopmanagement',
            name: 'ShopManagement',
            component: ShopManagement
        },
        {
            path: '/admin/ordermanagement',
            name: 'AdminOrderManagement',
            component: AdminOrderManagement
        },
        
    ]
})