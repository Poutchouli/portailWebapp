<template>
  <div id="app">
    <nav v-if="isAuthenticated" class="navbar">
      <div class="nav-container">
        <h1 class="nav-title">Portal</h1>
        <div class="nav-links">
          <router-link to="/apps" class="nav-link">📱 My Apps</router-link>
          <router-link v-if="isAdmin" to="/admin" class="nav-link admin-link">⚙️ Admin Dashboard</router-link>
        </div>
        <div class="nav-user">
          <span v-if="user">Welcome, {{ user.username }}!</span>
          <button @click="logout" class="logout-btn">Logout</button>
        </div>
      </div>
    </nav>
    
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'App',
  setup() {
    const store = useStore()
    const router = useRouter()
    
    const isAuthenticated = computed(() => store.getters.isAuthenticated)
    const user = computed(() => store.getters.user)
    const isAdmin = computed(() => store.getters.isAdmin)
    
    // Check if user is already logged in
    if (store.state.token) {
      store.dispatch('fetchUserInfo')
    }
    
    const logout = () => {
      store.dispatch('logout')
      router.push('/login')
    }
    
    return {
      isAuthenticated,
      user,
      isAdmin,
      logout
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.navbar {
  background-color: #2c3e50;
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-title {
  font-size: 1.5rem;
  font-weight: bold;
}

.nav-links {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.nav-link {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.2s;
  font-weight: 500;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.nav-link.router-link-active {
  background-color: #3498db;
}

.admin-link {
  background-color: #e67e22;
}

.admin-link:hover {
  background-color: #d35400;
}

.nav-user {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logout-btn {
  background-color: #e74c3c;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.logout-btn:hover {
  background-color: #c0392b;
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

/* Responsive design */
@media (max-width: 768px) {
  .nav-container {
    padding: 0 1rem;
    flex-direction: column;
    gap: 1rem;
  }

  .nav-links {
    order: -1;
  }
  
  .main-content {
    padding: 1rem;
  }
}
</style>
