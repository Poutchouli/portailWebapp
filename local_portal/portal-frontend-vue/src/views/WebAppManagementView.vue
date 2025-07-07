<template>
  <div class="webapp-management-container">
    <h3>Web Application Management</h3>

    <div class="webapp-list-section">
      <h4>All Web Applications</h4>
      <button @click="showAddWebAppForm = true" class="add-btn">Add New WebApp</button>

      <p v-if="loading" class="loading-message">Loading web applications...</p>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

      <table v-if="webapps.length > 0 && !loading" class="webapps-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>URL</th>
            <th>Required Roles</th>
            <th>Description</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="app in webapps" :key="app.id">
            <td>{{ app.id }}</td>
            <td>{{ app.name }}</td>
            <td><a :href="app.url" target="_blank">{{ app.url }}</a></td>
            <td>{{ app.required_roles.join(', ') }}</td>
            <td>{{ app.description || '-' }}</td>
            <td>
              <button @click="editWebApp(app)" class="action-btn edit-btn">Edit</button>
              <button @click="confirmDelete(app.id)" class="action-btn delete-btn">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else-if="!loading && !errorMessage">No web applications found.</p>
    </div>

    <div v-if="showAddWebAppForm || showEditWebAppForm" class="form-section">
      <h4>{{ showEditWebAppForm ? 'Edit WebApp' : 'Add New WebApp' }}</h4>
      <WebAppForm
        :webapp="selectedWebApp"
        :isEditing="showEditWebAppForm"
        @submit="handleWebAppFormSubmit"
        @cancel="cancelWebAppForm"
      />
      <p v-if="formMessage" :class="{'success': isFormSuccess, 'error': !isFormSuccess}">{{ formMessage }}</p>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';
import WebAppForm from '@/components/WebAppForm.vue'; // Import the new form component

export default {
  name: 'WebAppManagementView',
  components: {
    WebAppForm
  },
  data() {
    return {
      webapps: [],
      loading: false,
      errorMessage: '',
      showAddWebAppForm: false,
      showEditWebAppForm: false,
      selectedWebApp: null, // WebApp object for editing
      formMessage: '',
      isFormSuccess: false,
    };
  },
  computed: {
    ...mapState(['token'])
  },
  mounted() {
    this.fetchWebApps();
  },
  methods: {
    async fetchWebApps() {
      this.loading = true;
      this.errorMessage = '';
      try {
        // Note: This calls the admin /apps/ endpoint that lists ALL apps
        // The /apps/ endpoint used by AppsView filters by user roles.
        const response = await fetch('/apps/', {
          headers: {
            'Authorization': `Bearer ${this.token}`
          }
        });

        if (response.ok) {
          this.webapps = await response.json();
        } else {
          const errorData = await response.json();
          this.errorMessage = `Failed to load web applications: ${errorData.detail || response.statusText}`;
        }
      } catch (error) {
        this.errorMessage = `Network error: ${error.message}`;
        console.error("Fetch webapps error:", error);
      } finally {
        this.loading = false;
      }
    },
    editWebApp(app) {
      this.selectedWebApp = { ...app }; // Clone to avoid direct mutation
      this.showEditWebAppForm = true;
      this.showAddWebAppForm = false; // Ensure add form is hidden
      this.formMessage = '';
    },
    async handleWebAppFormSubmit(appData) {
      this.formMessage = '';
      this.isFormSuccess = false;

      try {
        let response;
        if (this.showEditWebAppForm) {
          // Update existing web app
          response = await fetch(`/apps/${this.selectedWebApp.id}`, {
            method: 'PATCH',
            headers: {
              'Authorization': `Bearer ${this.token}`,
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(appData)
          });
          this.formMessage = 'Web application updated successfully!';
        } else {
          // Add new web app
          response = await fetch('/apps/', {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${this.token}`,
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(appData)
          });
          this.formMessage = 'Web application added successfully!';
        }

        if (response.ok) {
          this.isFormSuccess = true;
          this.fetchWebApps(); // Refresh the list
          this.cancelWebAppForm(); // Hide form
        } else {
          const errorData = await response.json();
          this.formMessage = `Operation failed: ${errorData.detail || response.statusText}`;
          this.isFormSuccess = false;
        }
      } catch (error) {
        this.formMessage = `Network error: ${error.message}`;
        this.isFormSuccess = false;
        console.error("Web app form submit error:", error);
      }
    },
    async confirmDelete(appId) {
      if (confirm('Are you sure you want to delete this web application? This action cannot be undone.')) {
        try {
          const response = await fetch(`/apps/${appId}`, {
            method: 'DELETE',
            headers: {
              'Authorization': `Bearer ${this.token}`
            }
          });

          if (response.ok) {
            this.formMessage = 'Web application deleted successfully!';
            this.isFormSuccess = true;
            this.fetchWebApps(); // Refresh the list
          } else {
            const errorData = await response.json();
            this.formMessage = `Deletion failed: ${errorData.detail || response.statusText}`;
            this.isFormSuccess = false;
          }
        } catch (error) {
          this.formMessage = `Network error: ${error.message}`;
          this.isFormSuccess = false;
          console.error("Delete webapp error:", error);
        }
      }
    },
    cancelWebAppForm() {
      this.showAddWebAppForm = false;
      this.showEditWebAppForm = false;
      this.selectedWebApp = null;
      this.formMessage = ''; // Clear form message on cancel
    }
  }
};
</script>

<style scoped>
/* Reusing styles from UserManagementView for consistency. Adjust as needed. */
.webapp-management-container {
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
.webapps-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}
.webapps-table th, .webapps-table td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
}
.webapps-table th {
  background-color: #f2f2f2;
  font-weight: bold;
}
.webapps-table tr:nth-child(even) {
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
