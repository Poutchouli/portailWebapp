<template>
  <form @submit.prevent="submitForm" class="role-form">
    <div class="form-group">
      <label for="roleName">Role Name:</label>
      <input type="text" id="roleName" v-model="localRole.name" required />
    </div>
    <div class="form-group">
      <label for="roleDescription">Description (optional):</label>
      <textarea id="roleDescription" v-model="localRole.description"></textarea>
    </div>
    <button type="submit">{{ isEditing ? 'Update Role' : 'Add Role' }}</button>
    <button type="button" @click="$emit('cancel')" class="cancel-btn">Cancel</button>
  </form>
</template>

<script>
export default {
  name: 'RoleForm',
  props: {
    role: {
      type: Object,
      default: () => ({ name: '', description: '' })
    },
    isEditing: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      localRole: { ...this.role } // Clone prop to avoid direct mutation
    };
  },
  watch: {
    role: { // Watch for changes in the role prop (e.g., when editing a different role)
      handler(newRole) {
        this.localRole = { ...newRole };
      },
      deep: true
    }
  },
  methods: {
    submitForm() {
      const roleToSend = {
        name: this.localRole.name,
        description: this.localRole.description || undefined // Send only if not empty
      };
      this.$emit('submit', roleToSend);
    }
  }
};
</script>

<style scoped>
/* Reusing styles from UserForm for consistency. Adjust as needed. */
.role-form {
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
