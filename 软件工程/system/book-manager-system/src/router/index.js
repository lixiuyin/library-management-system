import Vue from "vue";
import Router from "vue-router";
import login from "../views/login";
import layout from '../views/layout.vue'

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
      path: '/bookManage',
      name: 'bookManage',
      component: layout, // 导入组件 Layout
      hidden: false,
      children: [
        {
          path: '/bookManage',
          component: () => import('@/views/manager/book/bookManage.vue')
        },
        {
          path: '/userManage',
          component: () => import('@/views/manager/user/userManage.vue')
        },
        {
          path: '/borrowManage',
          component: () => import('@/views/manager/borrow/borrowManage.vue')
        },
        {
          path: '/borrowNow',
          component: () => import('@/views/manager/borrow/borrowNow.vue')
        },
        {
          path: '/borrowHistory',
          component: () => import('@/views/manager/borrow/borrowHistory.vue')
        },
        {
          path: '/borrowRank',
          component: () => import('@/views/manager/borrow/borrowRank.vue')
        },
        {
          path: '/importantRecordManage',
          component: () => import('@/views/manager/record/importantRecordManage.vue')
        },
        {
          path: '/systemManage',
          component: () => import('@/views/manager/system/systemManage.vue')
        },
      ]
    },

  ]
});
