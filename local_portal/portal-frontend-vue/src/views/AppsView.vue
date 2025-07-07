<template>
  <div class="apps-container">
    <div class="header">
      <h2>Available WebApps for {{ user ? user.username : 'User' }}</h2>
      <nav class="top-nav">
        <router-link v-if="isAdmin" to="/admin" class="admin-link">
          <span class="nav-icon">⚙️</span>
          Admin Dashboard
        </router-link>
        <button @click="logout" class="logout-btn">Logout</button>
      </nav>
    </div>
    
    <ul v-if="apps.length > 0" class="app-list">
      <li v-for="app in apps" :key="app.id">
        <span>{{ app.name }}</span>
        <a :href="app.url" target="_blank" rel="noopener noreferrer">Launch App</a>
        <p v-if="app.description">{{ app.description }}</p>
      </li>
    </ul>
    <p v-else-if="!loading && !errorMessage">No web applications available for you.</p>
    <p v-if="loading">Loading applications...</p>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script>
import { mapState, mapActions, mapGetters } from 'vuex';

export default {
  name: 'AppsView',
  data() {
    return {
      apps: [],
      loading: false,
      errorMessage: ''
    };
  },
  computed: {
    ...mapState(['token', 'user']),
    ...mapGetters(['isAdmin'])
  },
  watch: {
    token: {
      immediate: true, // Run handler immediately on component creation
      handler(newToken) {
        if (newToken) {
          this.fetchApps();
        } else {
          // If token becomes null (e.g., after logout), clear apps and redirect
          this.apps = [];
          this.$router.push('/login');
        }
      }
    }
  },
  methods: {
    ...mapActions(['logout']), // Map the logout action from Vuex
    async fetchApps() {
      this.loading = true;
      this.errorMessage = '';
      
      console.log("=== FETCH APPS DEBUG ==="); // DEBUG
      console.log("Current user:", this.user); // DEBUG
      console.log("User roles:", this.user ? this.user.roles : "No user"); // DEBUG
      console.log("Is Admin:", this.isAdmin); // DEBUG
      console.log("Token present:", !!this.token); // DEBUG
      
      try {
        console.log("Making request to /apps/ with token..."); // DEBUG
        const response = await fetch('/apps/', {
          headers: {
            'Authorization': `Bearer ${this.token}`
          }
        });

        console.log("Apps API response status:", response.status); // DEBUG
        
        if (response.ok) {
          const appsData = await response.json();
          console.log("Apps data received:", appsData); // DEBUG
          console.log("Number of apps:", appsData.length); // DEBUG
          this.apps = appsData;
        } else {
          const errorData = await response.json();
          console.error("Apps API error data:", errorData); // DEBUG
          this.errorMessage = `Failed to load apps: ${errorData.detail || response.statusText}`;
          if (response.status === 401 || response.status === 403) {
            // If unauthorized/forbidden, maybe token is stale or user lost permissions
            console.log("Unauthorized/Forbidden - forcing logout"); // DEBUG
            this.logout(); // Force logout
          }
        }
      } catch (error) {
        console.error("Fetch apps network error:", error); // DEBUG
        this.errorMessage = `Network error: ${error.message}`;
        console.error("Fetch apps error:", error);
      } finally {
        this.loading = false;
        console.log("=== FETCH APPS DEBUG END ==="); // DEBUG
      }
    }
  }
};
</script>

<style scoped>
.apps-container {
  max-width: 800px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  background-color: #fff;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 15px;
}

.header h2 {
  margin: 0;
  color: #2c3e50;
}

.top-nav {
  display: flex;
  gap: 15px;
  align-items: center;
}

.admin-link {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 15px;
  background-color: #17a2b8;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.admin-link:hover {
  background-color: #138496;
}

.nav-icon {
  font-size: 16px;
}

.logout-btn {
  padding: 8px 12px;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.logout-btn:hover {
  background-color: #c82333;
}

.app-list {
  list-style: none;
  padding: 0;
}
.app-list li {
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
  margin-bottom: 10px;
  padding: 15px;
  border-radius: 5px;
  display: flex;
  flex-wrap: wrap; /* Allow wrapping for description */
  justify-content: space-between;
  align-items: center;
}
.app-list li span {
  font-weight: bold;
  flex-basis: 60%; /* Take up more space */
}
.app-list li p {
  flex-basis: 100%; /* Description on new line */
  font-size: 0.9em;
  color: #666;
  margin-top: 5px;
  margin-bottom: 0;
}
.app-list li a {
  text-decoration: none;
  background-color: #28a745;
  color: white;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}
.app-list li a:hover {
  background-color: #218838;
}
.error {
  color: red;
  font-weight: bold;
}
</style>
