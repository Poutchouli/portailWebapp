<template>
  <div class="user-management-container">
    <h3>User Management</h3>

    <div class="user-list-section">
      <h4>All Users</h4>
      <button @click="showAddUserForm = true" class="add-btn">Add New User</button>

      <p v-if="loading" class="loading-message">Loading users...</p>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

      <table v-if="users.length > 0 && !loading" class="users-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Roles</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.username }}</td>
            <td>{{ user.roles.join(', ') }}</td>
            <td>
              <button @click="editUser(user)" class="action-btn edit-btn">Edit</button>
              <button @click="confirmDelete(user.id)" class="action-btn delete-btn">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else-if="!loading && !errorMessage">No users found.</p>
    </div>

    <div v-if="showAddUserForm || showEditUserForm" class="form-section">
      <h4>{{ showEditUserForm ? 'Edit User' : 'Add New User' }}</h4>
      <UserForm
        :user="selectedUser"
        :isEditing="showEditUserForm"
        @submit="handleUserFormSubmit"
        @cancel="cancelUserForm"
      />
      <p v-if="formMessage" :class="{'success': isFormSuccess, 'error': !isFormSuccess}">{{ formMessage }}</p>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';
import UserForm from '@/components/UserForm.vue'; // Import the new form component

export default {
  name: 'UserManagementView',
  components: {
    UserForm
  },
  data() {
    return {
      users: [],
      loading: false,
      errorMessage: '',
      showAddUserForm: false,
      showEditUserForm: false,
      selectedUser: null, // User object for editing
      formMessage: '',
      isFormSuccess: false,
    };
  },
  computed: {
    ...mapState(['token'])
  },
  mounted() {
    this.fetchUsers();
  },
  methods: {
    async fetchUsers() {
      this.loading = true;
      this.errorMessage = '';
      try {
        const response = await fetch('/users/', {
          headers: {
            'Authorization': `Bearer ${this.token}`
          }
        });

        if (response.ok) {
          this.users = await response.json();
        } else {
          const errorData = await response.json();
          this.errorMessage = `Failed to load users: ${errorData.detail || response.statusText}`;
        }
      } catch (error) {
        this.errorMessage = `Network error: ${error.message}`;
        console.error("Fetch users error:", error);
      } finally {
        this.loading = false;
      }
    },
    editUser(user) {
      this.selectedUser = { ...user }; // Clone to avoid direct mutation
      this.showEditUserForm = true;
      this.showAddUserForm = false; // Ensure add form is hidden
      this.formMessage = '';
    },
    async handleUserFormSubmit(userData) {
      this.formMessage = ''; // Clear previous messages
      this.isFormSuccess = false;

      try {
        let response;
        if (this.showEditUserForm) {
          // Update existing user
          response = await fetch(`/users/${this.selectedUser.id}`, {
            method: 'PATCH',
            headers: {
              'Authorization': `Bearer ${this.token}`,
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
          });
          this.formMessage = 'User updated successfully!';
        } else {
          // Add new user
          response = await fetch('/users/', {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${this.token}`,
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
          });
          this.formMessage = 'User added successfully!';
        }

        if (response.ok) {
          this.isFormSuccess = true;
          this.fetchUsers(); // Refresh the list
          this.cancelUserForm(); // Hide form
        } else {
          const errorData = await response.json();
          this.formMessage = `Operation failed: ${errorData.detail || response.statusText}`;
          this.isFormSuccess = false;
        }
      } catch (error) {
        this.formMessage = `Network error: ${error.message}`;
        this.isFormSuccess = false;
        console.error("User form submit error:", error);
      }
    },
    async confirmDelete(userId) {
      if (confirm('Are you sure you want to delete this user? This action cannot be undone.')) {
        try {
          const response = await fetch(`/users/${userId}`, {
            method: 'DELETE',
            headers: {
              'Authorization': `Bearer ${this.token}`
            }
          });

          if (response.ok) {
            this.formMessage = 'User deleted successfully!';
            this.isFormSuccess = true;
            this.fetchUsers(); // Refresh the list
          } else {
            const errorData = await response.json();
            this.formMessage = `Deletion failed: ${errorData.detail || response.statusText}`;
            this.isFormSuccess = false;
          }
        } catch (error) {
          this.formMessage = `Network error: ${error.message}`;
          this.isFormSuccess = false;
          console.error("Delete user error:", error);
        }
      }
    },
    cancelUserForm() {
      this.showAddUserForm = false;
      this.showEditUserForm = false;
      this.selectedUser = null;
      this.formMessage = ''; // Clear form message on cancel
    }
  }
};
</script>

<style scoped>
.user-management-container {
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
.users-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}
.users-table th, .users-table td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
}
.users-table th {
  background-color: #f2f2f2;
  font-weight: bold;
}
.users-table tr:nth-child(even) {
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
