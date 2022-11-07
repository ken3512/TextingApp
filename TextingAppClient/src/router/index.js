import { nextTick } from 'vue';
import { createRouter, createWebHistory } from 'vue-router'
import Signup from '../views/Signup.vue'
import Login from '../views/Login.vue'
import Home from '../views/Home.vue'
import Activate from '../views/Activate.vue'
import Chat from '../views/Chat.vue'
import store from '../store/index.js'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/signup',
      name: 'Signup',
      component: Signup,
    },
    {
      path: '/activate',
      name: 'Activate',
      component: Activate,
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
    },
    {
      path: '/',
      name: 'Home',
      component: Home,
    },
    {
      path: '/chat',
      name: 'Chat',
      component: Chat,
    }
  ]
})

router.beforeEach((to, from, next) => {
  let authRequired = ['/', '/chat']
  let unauthRequired = ['/login', '/signup']
  if (authRequired.includes(to.path) && !store.state.isAuthenticated) {
    next('/login')
  } else if (unauthRequired.includes(to.path) && store.state.isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router