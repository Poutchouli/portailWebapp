import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '../views/LoginView.vue';
import AppsView from '../views/AppsView.vue';
import AdminDashboardView from '../views/AdminDashboardView.vue';
import UserManagementView from '../views/UserManagementView.vue';
import WebAppManagementView from '../views/WebAppManagementView.vue';
import RoleManagementView from '../views/RoleManagementView.vue'; // NEW IMPORT
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
    path: '/admin',
    name: 'AdminDashboard',
    component: AdminDashboardView,
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      {
        path: 'users',
        name: 'ManageUsers',
        component: UserManagementView
      },
      {
        path: 'apps',
        name: 'ManageWebApps',
        component: WebAppManagementView
      },
      { // NEW CHILD ROUTE
        path: 'roles',
        name: 'ManageRoles',
        component: RoleManagementView
      }
    ]
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
      // Check if route requires admin access
      if (to.matched.some(record => record.meta.requiresAdmin)) {
        // Ensure user info is loaded
        if (!store.state.user) {
          // Try to fetch user info first
          store.dispatch('fetchUserInfo').then(() => {
            if (store.getters.isAdmin) {
              next(); // User is admin, allow access
            } else {
              next({ name: 'Apps' }); // Not admin, redirect to apps
            }
          });
        } else {
          if (store.getters.isAdmin) {
            next(); // User is admin, allow access
          } else {
            next({ name: 'Apps' }); // Not admin, redirect to apps
          }
        }
      } else {
        next(); // Route doesn't require admin, allow access
      }
    }
  } else {
    next(); // Does not require auth, allow access
  }
});

export default router;
