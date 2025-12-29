// /**
//  * router/index.ts
//  *
//  * Automatic routes for `./src/pages/*.vue`
//  */

// // Composables
// import { createRouter, createWebHistory } from 'vue-router'
// import { routes } from 'vue-router/auto-routes'

// const router = createRouter({
//   history: createWebHistory(import.meta.env.BASE_URL),
//   routes,
// })

// // Workaround for https://github.com/vitejs/vite/issues/11804
// router.onError((err, to) => {
//   if (err?.message?.includes?.('Failed to fetch dynamically imported module')) {
//     if (localStorage.getItem('vuetify:dynamic-reload')) {
//       console.error('Dynamic import error, reloading page did not fix it', err)
//     } else {
//       console.log('Reloading page to fix dynamic import error')
//       localStorage.setItem('vuetify:dynamic-reload', 'true')
//       location.assign(to.fullPath)
//     }
//   } else {
//     console.error(err)
//   }
// })

// router.isReady().then(() => {
//   localStorage.removeItem('vuetify:dynamic-reload')
// })

// export default router

import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/pages/index.vue'),
      meta: { title: '首页', icon: 'mdi-home' },
    },
    {
      path: '/docs',
      name: 'docs',
      component: () => import('@/pages/docs.vue'),
      meta: { title: '文档', icon: 'mdi-file-document' },
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('@/pages/settings.vue'),
      meta: { title: '设置', icon: 'mdi-cog' },
    },
    {
      path: '/monitor',
      name: 'monitor',
      component: () => import('@/pages/monitor.vue'),
      meta: { title: '监控', icon: 'mdi-monitor' },
    },
    {
      path: '/friend-links',
      name: 'friend-links',
      component: () => import('@/pages/friend-links.vue'),
      meta: { title: '友情链接', icon: 'mdi-link' },
    },
    {
      path: '/yituliu',
      name: 'yituliu',
      component: () => import('@/pages/yituliu.vue'),
      meta: { title: '终末地一图流', icon: 'mdi-map' },
    },
    {
      path: '/logs',
      name: 'logs',
      component: () => import('@/pages/logs.vue'),
      meta: { title: '日志', icon: 'mdi-file-document-outline' },
    },
  ],
})

router.afterEach((to) => {
  if (to.meta.title) {
    document.title = `${to.meta.title} - 终末地基质妙妙小工具`
  } else {
    document.title = '终末地基质妙妙小工具'
  }
})

export default router
