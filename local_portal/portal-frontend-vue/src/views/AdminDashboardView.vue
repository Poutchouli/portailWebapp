<template>
  <div class="admin-dashboard">
    <div class="admin-header">
      <h2>Admin Dashboard</h2>
      <p>Manage users, applications, and system settings.</p>
    </div>

    <nav class="admin-nav">
      <router-link to="/admin/users" class="nav-link">
        <span class="nav-icon">👥</span>
        Manage Users
      </router-link>
      <router-link to="/admin/apps" class="nav-link">
        <span class="nav-icon">📱</span>
        Manage Web Apps
      </router-link>
      <router-link to="/admin/roles" class="nav-link">
        <span class="nav-icon">🔑</span>
        Manage Roles
      </router-link>
    </nav>

    <div class="admin-content">
      <router-view></router-view>
      <div v-if="$route.path === '/admin'" class="admin-welcome">
        <h3>👋 Welcome to the Admin Dashboard</h3>
        <p>Select an option above to manage your portal:</p>
        <ul class="admin-features">
          <li><strong>👥 Manage Users</strong> - Create, edit, and delete user accounts, assign roles</li>
          <li><strong>📱 Manage Web Apps</strong> - Add, configure, and manage portal applications</li>
          <li><strong>🔑 Manage Roles</strong> - Create and modify user roles and permissions</li>
        </ul>
        <div class="quick-links">
          <router-link to="/admin/users" class="quick-link">👥 Go to User Management</router-link>
          <router-link to="/admin/apps" class="quick-link">📱 Go to App Management</router-link>
          <router-link to="/admin/roles" class="quick-link">🔑 Go to Role Management</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminDashboardView'
};
</script>

<style scoped>
.admin-dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.admin-header {
  text-align: center;
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.admin-header h2 {
  color: #2c3e50;
  margin-bottom: 10px;
}

.admin-header p {
  color: #6c757d;
  margin: 0;
}

.admin-nav {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
  justify-content: center;
  flex-wrap: wrap;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px 25px;
  background-color: #007bff;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: bold;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.nav-link:hover {
  background-color: #0056b3;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.nav-link.router-link-active {
  background-color: #28a745;
}

.nav-icon {
  font-size: 18px;
}

.admin-content {
  min-height: 400px;
}

.admin-welcome {
  background-color: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  text-align: center;
}

.admin-welcome h3 {
  color: #2c3e50;
  margin-bottom: 15px;
  font-size: 24px;
}

.admin-welcome p {
  color: #6c757d;
  margin-bottom: 20px;
  font-size: 16px;
}

.admin-features {
  list-style: none;
  text-align: left;
  max-width: 600px;
  margin: 0 auto 30px;
  padding: 0;
}

.admin-features li {
  padding: 10px 0;
  border-bottom: 1px solid #eee;
  color: #555;
}

.admin-features li:last-child {
  border-bottom: none;
}

.quick-links {
  display: flex;
  gap: 15px;
  justify-content: center;
  flex-wrap: wrap;
}

.quick-link {
  display: inline-block;
  padding: 12px 20px;
  background-color: #17a2b8;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  font-weight: bold;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.quick-link:hover {
  background-color: #138496;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}
</style>
