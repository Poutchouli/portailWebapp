<template>
  <div class="role-management-container">
    <h3>Role Management</h3>

    <div class="role-list-section">
      <h4>All Defined Roles</h4>
      <button @click="showAddRoleForm = true" class="add-btn">Add New Role</button>

      <p v-if="loading" class="loading-message">Loading roles...</p>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

      <table v-if="roles.length > 0 && !loading" class="roles-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Description</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="role in roles" :key="role.id">
            <td>{{ role.id }}</td>
            <td>{{ role.name }}</td>
            <td>{{ role.description || '-' }}</td>
            <td>
              <button @click="editRole(role)" class="action-btn edit-btn">Edit</button>
              <button @click="confirmDelete(role.id)" class="action-btn delete-btn">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else-if="!loading && !errorMessage">No roles found.</p>
    </div>

    <div v-if="showAddRoleForm || showEditRoleForm" class="form-section">
      <h4>{{ showEditRoleForm ? 'Edit Role' : 'Add New Role' }}</h4>
      <RoleForm
        :role="selectedRole"
        :isEditing="showEditRoleForm"
        @submit="handleRoleFormSubmit"
        @cancel="cancelRoleForm"
      />
      <p v-if="formMessage" :class="{'success': isFormSuccess, 'error': !isFormSuccess}">{{ formMessage }}</p>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';
import RoleForm from '@/components/RoleForm.vue';

export default {
  name: 'RoleManagementView',
  components: {
    RoleForm
  },
  data() {
    return {
      roles: [],
      loading: false,
      errorMessage: '',
      showAddRoleForm: false,
      showEditRoleForm: false,
      selectedRole: null, // Role object for editing
      formMessage: '',
      isFormSuccess: false,
    };
  },
  computed: {
    ...mapState(['token'])
  },
  mounted() {
    this.fetchRoles();
  },
  methods: {
    async fetchRoles() {
      this.loading = true;
      this.errorMessage = '';
      try {
        const response = await fetch('/roles/', { // Call the new /roles/ endpoint
          headers: {
            'Authorization': `Bearer ${this.token}`
          }
        });

        if (response.ok) {
          this.roles = await response.json();
        } else {
          const errorData = await response.json();
          this.errorMessage = `Failed to load roles: ${errorData.detail || response.statusText}`;
        }
      } catch (error) {
        this.errorMessage = `Network error: ${error.message}`;
        console.error("Fetch roles error:", error);
      } finally {
        this.loading = false;
      }
    },
    editRole(role) {
      this.selectedRole = { ...role }; // Clone to avoid direct mutation
      this.showEditRoleForm = true;
      this.showAddRoleForm = false; // Ensure add form is hidden
      this.formMessage = '';
    },
    async handleRoleFormSubmit(roleData) {
      this.formMessage = '';
      this.isFormSuccess = false;

      try {
        let response;
        if (this.showEditRoleForm) {
          // Update existing role
          response = await fetch(`/roles/${this.selectedRole.id}`, {
            method: 'PATCH',
            headers: {
              'Authorization': `Bearer ${this.token}`,
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(roleData)
          });
          this.formMessage = 'Role updated successfully!';
        } else {
          // Add new role
          response = await fetch('/roles/', {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${this.token}`,
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(roleData)
          });
          this.formMessage = 'Role added successfully!';
        }

        if (response.ok) {
          this.isFormSuccess = true;
          this.fetchRoles(); // Refresh the list
          this.cancelRoleForm(); // Hide form
        } else {
          const errorData = await response.json();
          this.formMessage = `Operation failed: ${errorData.detail || response.statusText}`;
          this.isFormSuccess = false;
        }
      } catch (error) {
        this.formMessage = `Network error: ${error.message}`;
        this.isFormSuccess = false;
        console.error("Role form submit error:", error);
      }
    },
    async confirmDelete(roleId) {
      if (confirm('Are you sure you want to delete this role? This action cannot be undone and may affect users/apps if not unassigned.')) {
        try {
          const response = await fetch(`/roles/${roleId}`, {
            method: 'DELETE',
            headers: {
              'Authorization': `Bearer ${this.token}`
            }
          });

          if (response.ok) {
            this.formMessage = 'Role deleted successfully!';
            this.isFormSuccess = true;
            this.fetchRoles(); // Refresh the list
          } else {
            const errorData = await response.json();
            this.formMessage = `Deletion failed: ${errorData.detail || response.statusText}`;
            this.isFormSuccess = false;
          }
        } catch (error) {
          this.formMessage = `Network error: ${error.message}`;
          this.isFormSuccess = false;
          console.error("Delete role error:", error);
        }
      }
    },
    cancelRoleForm() {
      this.showAddRoleForm = false;
      this.showEditRoleForm = false;
      this.selectedRole = null;
      this.formMessage = ''; // Clear form message on cancel
    }
  }
};
</script>

<style scoped>
/* Reusing styles from UserManagementView for consistency. Adjust as needed. */
.role-management-container {
  max-width: 1000px;
  margin: 30px auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  text-align: left;
}
h3 {
  color: #34495e;
  text-align: center;
  margin-bottom: 25px;
}
.add-btn {
  background-color: #007bff;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 20px;
  font-weight: bold;
}
.add-btn:hover {
  background-color: #0056b3;
}
.loading-message, .error-message, .success-message {
  padding: 10px;
  border-radius: 4px;
  margin-top: 15px;
  font-weight: bold;
}
.loading-message {
  background-color: #e0f7fa;
  color: #007bb6;
}
.error-message, .error {
  background-color: #ffebee;
  color: #c62828;
}
.success-message, .success {
    background-color: #e8f5e9;
    color: #2e7d32;
}
.roles-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}
.roles-table th, .roles-table td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
}
.roles-table th {
  background-color: #f2f2f2;
  font-weight: bold;
}
.roles-table tr:nth-child(even) {
  background-color: #f9f9f9;
}
.action-btn {
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s ease;
}
.edit-btn {
  background-color: #ffc107;
  color: #333;
  margin-right: 5px;
}
.edit-btn:hover {
  background-color: #e0a800;
}
.delete-btn {
  background-color: #dc3545;
  color: white;
}
.delete-btn:hover {
  background-color: #c82333;
}

.form-section {
  margin-top: 40px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}
.form-section h4 {
  text-align: center;
  color: #34495e;
  margin-bottom: 20px;
}
</style>
