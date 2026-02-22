import Vue from "vue";
import Router from "vue-router";
import login from "../views/login";
import layout from '../views/layout.vue'
import onlyBooks from "@/views/onlyBooks.vue";  //写在顶部

Vue.use(Router);

export default new Router({
  mode: "history",
  routes: [
    {
      path: '/',
      name: 'login',
      component: login,
      meta: {
        title: "登录"
      },
    },
    {
      path: '/signIn',
      name: 'signIn',
      component: () => import('@/views/signIn.vue'),
      meta: {
        title: "注册"
      },
    },
    {
      path:"/visitor",
      component:()=>import ("@/views/onlyBooks.vue")
    },
    {
      path: '/home',
      name: 'home',
      component: layout, // 导入组件 Layout
      hidden: false,
      children: [
        {
          path: '/home',
          component: () => import('@/views/readers/home.vue')
        },
        {
          path: '/browBooks',
          component: () => import('@/views/readers/browBooks.vue')
        },
        {
          path: '/borrowNow',
          component: () => import('@/views/readers/borrowNow.vue')
        },
        {
          path: '/borrowHistory',
          component: () => import('@/views/readers/borrowHistory.vue')
        },
        {
          path: '/rechargeRecord',
          component: () => import('@/views/readers/rechargeRecord.vue')
        },
        {
          path: '/importantOperation',
          component: () => import('@/views/readers/importantOperation.vue')
        },
      ]
    },

  ]
});
