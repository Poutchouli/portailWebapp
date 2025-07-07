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
      <!-- Future link for app management -->
      <!-- <router-link to="/admin/apps" class="nav-link">
        <span class="nav-icon">📱</span>
        Manage Web Apps
      </router-link> -->
    </nav>

    <div class="admin-content">
      <router-view></router-view>
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
</style>
