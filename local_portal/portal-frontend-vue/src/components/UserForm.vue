<template>
  <form @submit.prevent="submitForm" class="user-form">
    <div class="form-group">
      <label for="username">Username:</label>
      <input type="text" id="username" v-model="localUser.username" required :disabled="isEditing" />
    </div>
    <div class="form-group">
      <label for="password">{{ isEditing ? 'New Password (optional):' : 'Password:' }}</label>
      <input type="password" id="password" v-model="localUser.password" :required="!isEditing" />
    </div>
    <div class="form-group">
      <label for="roles">Roles (comma-separated, e.g., admin,user):</label>
      <input type="text" id="roles" v-model="rolesInput" />
    </div>
    <button type="submit">{{ isEditing ? 'Update User' : 'Add User' }}</button>
    <button type="button" @click="$emit('cancel')" class="cancel-btn">Cancel</button>
  </form>
</template>

<script>
export default {
  name: 'UserForm',
  props: {
    user: {
      type: Object,
      default: () => ({ username: '', password: '', roles: [] })
    },
    isEditing: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      localUser: { ...this.user, password: '' }, // Clone user prop, clear password for security
      rolesInput: this.user.roles ? this.user.roles.join(',') : '' // Convert array to comma-separated string
    };
  },
  watch: {
    user: { // Watch for changes in the user prop (e.g., when editing a different user)
      handler(newUser) {
        this.localUser = { ...newUser, password: '' };
        this.rolesInput = newUser.roles ? newUser.roles.join(',') : '';
      },
      deep: true
    }
  },
  methods: {
    submitForm() {
      const userToSend = {
        username: this.localUser.username,
        password: this.localUser.password || undefined, // Send password only if provided
        roles: this.rolesInput.split(',').map(role => role.trim()).filter(Boolean) // Convert string to array
      };
      this.$emit('submit', userToSend);
    }
  }
};
</script>

<style scoped>
.user-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
  padding: 20px;
  border: 1px solid #eee;
  border-radius: 8px;
  background-color: #f9f9f9;
  margin-bottom: 20px;
}
.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  text-align: left;
}
.form-group input[type="text"],
.form-group input[type="password"] {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box; /* Include padding in width */
}
button {
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s ease;
}
button[type="submit"] {
  background-color: #28a745;
  color: white;
}
button[type="submit"]:hover {
  background-color: #218838;
}
.cancel-btn {
  background-color: #6c757d;
  color: white;
  margin-left: 10px;
}
.cancel-btn:hover {
  background-color: #5a6268;
}
</style>
