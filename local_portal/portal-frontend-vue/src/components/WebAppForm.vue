<template>
  <form @submit.prevent="submitForm" class="webapp-form">
    <div class="form-group">
      <label for="appName">App Name:</label>
      <input type="text" id="appName" v-model="localApp.name" required />
    </div>
    <div class="form-group">
      <label for="appUrl">URL:</label>
      <input type="text" id="appUrl" v-model="localApp.url" required placeholder="e.g., http://localhost:5001" />
    </div>
    <div class="form-group">
      <label for="appRoles">Required Roles (comma-separated, e.g., user,admin):</label>
      <input type="text" id="appRoles" v-model="rolesInput" />
    </div>
    <div class="form-group">
      <label for="appDescription">Description (optional):</label>
      <textarea id="appDescription" v-model="localApp.description"></textarea>
    </div>
    <button type="submit">{{ isEditing ? 'Update WebApp' : 'Add WebApp' }}</button>
    <button type="button" @click="$emit('cancel')" class="cancel-btn">Cancel</button>
  </form>
</template>

<script>
export default {
  name: 'WebAppForm',
  props: {
    webapp: {
      type: Object,
      default: () => ({ name: '', url: '', required_roles: [], description: '' })
    },
    isEditing: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      localApp: { ...this.webapp }, // Clone prop to avoid direct mutation
      rolesInput: this.webapp.required_roles ? this.webapp.required_roles.join(',') : '' // Convert array to string
    };
  },
  watch: {
    webapp: { // Watch for changes in the webapp prop (e.g., when editing a different app)
      handler(newApp) {
        this.localApp = { ...newApp };
        this.rolesInput = newApp.required_roles ? newApp.required_roles.join(',') : '';
      },
      deep: true
    }
  },
  methods: {
    submitForm() {
      const appToSend = {
        name: this.localApp.name,
        url: this.localApp.url,
        description: this.localApp.description || undefined, // Send only if not empty
        required_roles: this.rolesInput.split(',').map(role => role.trim()).filter(Boolean) // Convert string to array
      };
      this.$emit('submit', appToSend);
    }
  }
};
</script>

<style scoped>
/* Reusing styles from UserForm for consistency. Adjust as needed. */
.webapp-form {
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
.form-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
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
