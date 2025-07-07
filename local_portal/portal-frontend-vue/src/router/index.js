import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '../views/LoginView.vue';
import AppsView from '../views/AppsView.vue';
import store from '../store'; // Import your Vuex store

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: LoginView
  },
  {
    path: '/apps',
    name: 'Apps',
    component: AppsView,
    meta: { requiresAuth: true } // Meta field to protect this route
  },
  {
    path: '/',
    redirect: '/apps' // Redirect root to /apps (which will redirect to login if not authenticated)
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Navigation guard for authentication
router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // This route requires auth, check if logged in
    if (!store.state.token) {
      next({ name: 'Login' }); // Not logged in, redirect to login page
    } else {
      next(); // Go to the route
    }
  } else {
    next(); // Does not require auth, allow access
  }
});

export default router;
