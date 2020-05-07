import Vue from 'vue';
import VueRouter from 'vue-router';
// import Home from '../views/Home.vue';
import Ping from '../components/ping.vue';
import AdminSystem from '../components/AdminSystem.vue';
import Application from '../components/Application.vue';


Vue.use(VueRouter);

const routes = [
  {
    path: '/ping',
    name: 'Ping',
    component: Ping,
  },
  {
    path: '/adminsystem',
    name: 'AdminSystem',
    component: AdminSystem,
  },
  {
    path: '/admin/application',
    name: 'Application',
    component: Application,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
