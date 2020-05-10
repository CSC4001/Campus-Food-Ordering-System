import Vue from 'vue'
import Router from 'vue-router'
//auth
import Login from '@/components/UserInterface/Login'
import Register from '@/components/UserInterface/Register'
//user 
import Home from '@/components/UserInterface/Home' 
import PersonalInfo from '@/components/UserInterface/PersonalInfo'
import MyShop from '@/components/UserInterface/MyShop'
//shop
import ShopSystem from '@/components/Shop/ShopSystem'
import DishesManagement from '@/components/Shop/DishesManagement'
import ShopOrderManagement from '@/components/Shop/OrderManagement'
import Information from '@/components/Shop/Information'
//admin
import AdminSystem from '@/components/Admin/AdminSystem'
import CloseApplication from '@/components/Admin/CloseApplication'
import OpenApplication from '@/components/Admin/OpenApplication'
import UnblockApplication from '@/components/Admin/UnblockApplication'
import UserManagement from '@/components/Admin/UserManagement'
import ShopManagement from '@/components/Admin/ShopManagement'
import AdminOrderManagement from '@/components/Admin/OrderManagement'
// order
import Shop from '@/components/Order/Shop'
import Search from '@/components/Order/Search'
import MyOrder from '@/components/UserInterface/MyOrder'
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
        {
            path: '/login',
            name: 'Login',
            component: Login
        },
        {
            path: '/register',
            name: 'Register',
            component: Register
        },
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
            path: '/shops/:shopid',
            name: 'Shops',
            component: Shop
        },
        {
            path: '/search/:searchType/:searchKey',
            name: 'Search',
            component: Search
        },
        {
            path: '/myorder',
            name: 'MyOrder',
            component: MyOrder
        },
        {
            path: '/shopsystem/',
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
            path: '/admin/closeapplication',
            name: 'CloseApplication',
            component: CloseApplication
        },
        {
            path: '/admin/openapplication',
            name: 'OpenApplication',
            component: OpenApplication
        },
        {
            path: '/admin/unblockapplication',
            name: 'UnblockApplication',
            component: UnblockApplication
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