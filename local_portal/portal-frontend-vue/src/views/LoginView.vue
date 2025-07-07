<template>
  <div class="login-container">
    <h2>Login to Portal</h2>
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit">Login</button>
    </form>
    <p v-if="message" :class="{'success': isSuccess, 'error': !isSuccess}">{{ message }}</p>
  </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  name: 'LoginView',
  data() {
    return {
      username: '',
      password: '',
      message: '',
      isSuccess: false
    };
  },
  methods: {
    ...mapActions(['login']), // Map the login action from Vuex
    async handleLogin() {
      try {
        this.message = ''; // Clear previous messages
        await this.login({ username: this.username, password: this.password });
        this.message = 'Login successful!';
        this.isSuccess = true;
        this.$router.push('/apps'); // Redirect to /apps on success
      } catch (error) {
        this.message = error.message || 'An unexpected error occurred.';
        this.isSuccess = false;
        console.error("Login error:", error);
      }
    }
  }
};
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  background-color: #fff;
}
.form-group {
  margin-bottom: 15px;
}
label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}
input[type="text"], input[type="password"] {
  width: calc(100% - 22px);
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
button {
  padding: 10px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:hover {
  background-color: #0056b3;
}
.success {
  color: green;
  font-weight: bold;
}
.error {
  color: red;
  font-weight: bold;
}
</style>
