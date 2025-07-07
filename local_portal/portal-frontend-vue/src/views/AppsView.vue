<template>
  <div class="apps-container">
    <h2>Available WebApps for {{ username }}</h2>
    <button @click="logout">Logout</button>
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
import { mapState, mapActions } from 'vuex';

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
    ...mapState(['token', 'username']) // Get token and username from Vuex state
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
      try {
        const response = await fetch('/apps/', {
          headers: {
            'Authorization': `Bearer ${this.token}`
          }
        });

        if (response.ok) {
          this.apps = await response.json();
        } else {
          const errorData = await response.json();
          this.errorMessage = `Failed to load apps: ${errorData.detail || response.statusText}`;
          if (response.status === 401 || response.status === 403) {
            // If unauthorized/forbidden, maybe token is stale or user lost permissions
            this.logout(); // Force logout
          }
        }
      } catch (error) {
        this.errorMessage = `Network error: ${error.message}`;
        console.error("Fetch apps error:", error);
      } finally {
        this.loading = false;
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
button {
  padding: 8px 12px;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 20px;
}
button:hover {
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
