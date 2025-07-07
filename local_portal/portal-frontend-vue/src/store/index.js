import { createStore } from 'vuex'

const store = createStore({
  state: {
    user: null,
    token: localStorage.getItem('token') || null,
    isAuthenticated: false
  },
  
  mutations: {
    SET_USER(state, user) {
      console.log("SET_USER mutation called with:", user); // DEBUG
      console.log("User roles in mutation:", user ? user.roles : "No user"); // DEBUG
      state.user = user
      state.isAuthenticated = !!user
    },
    
    SET_TOKEN(state, token) {
      console.log("SET_TOKEN mutation called with token:", token ? "Token present" : "No token"); // DEBUG
      state.token = token
      if (token) {
        localStorage.setItem('token', token)
        state.isAuthenticated = true
      } else {
        localStorage.removeItem('token')
        state.isAuthenticated = false
      }
    },
    
    LOGOUT(state) {
      state.user = null
      state.token = null
      state.isAuthenticated = false
      localStorage.removeItem('token')
    }
  },
  
  actions: {
    async login({ commit }, credentials) {
      try {
        const formData = new FormData()
        formData.append('username', credentials.username)
        formData.append('password', credentials.password)
        
        console.log("Attempting login for:", credentials.username); // DEBUG
        console.log("Sending form data:", formData); // DEBUG
        
        const response = await fetch('/token', {
          method: 'POST',
          body: formData
        })
        
        console.log("Login response status:", response.status); // DEBUG
        
        if (!response.ok) {
          const errorData = await response.json()
          console.error("Login API Error Data:", errorData); // DEBUG
          throw new Error(errorData.detail || 'Login failed')
        }
        
        const data = await response.json()
        console.log("Login response data:", data); // DEBUG
        
        // Debug JWT token parsing
        if (data.access_token) {
          console.log("JWT Token received:", data.access_token); // DEBUG
          
          // Decode JWT payload (without verification, just for debugging)
          try {
            const tokenParts = data.access_token.split('.');
            console.log("JWT parts count:", tokenParts.length); // DEBUG
            
            if (tokenParts.length === 3) {
              const payload = JSON.parse(atob(tokenParts[1]));
              console.log("JWT Payload decoded:", payload); // DEBUG
              console.log("JWT Payload roles:", payload.roles); // DEBUG
              console.log("JWT Payload sub (user):", payload.sub); // DEBUG
              console.log("JWT Payload exp:", payload.exp); // DEBUG
            }
          } catch (jwtError) {
            console.error("Failed to decode JWT:", jwtError); // DEBUG
          }
        }
        
        // Store the token
        commit('SET_TOKEN', data.access_token)
        
        // Fetch user info
        console.log("Fetching user info..."); // DEBUG
        const userResponse = await fetch('/users/me', {
          headers: {
            'Authorization': `Bearer ${data.access_token}`
          }
        })
        
        console.log("User info response status:", userResponse.status); // DEBUG
        
        if (userResponse.ok) {
          const userData = await userResponse.json()
          console.log("User data received:", userData); // DEBUG
          console.log("User roles from API:", userData.roles); // DEBUG
          commit('SET_USER', userData)
        }
        
        return { success: true }
      } catch (error) {
        console.error("Login action caught error:", error.message); // DEBUG
        commit('LOGOUT')
        return { success: false, error: error.message }
      }
    },
    
    async fetchUserInfo({ commit, state }) {
      if (!state.token) return
      
      try {
        const response = await fetch('/users/me', {
          headers: {
            'Authorization': `Bearer ${state.token}`
          }
        })
        
        if (response.ok) {
          const userData = await response.json()
          commit('SET_USER', userData)
        } else {
          commit('LOGOUT')
        }
      } catch (error) {
        console.error('Failed to fetch user info:', error)
        commit('LOGOUT')
      }
    },
    
    logout({ commit }) {
      commit('LOGOUT')
    }
  },
  
  getters: {
    isAuthenticated: state => state.isAuthenticated,
    user: state => state.user,
    token: state => state.token,
    isAdmin: state => {
      const result = state.user && state.user.roles && state.user.roles.includes('admin');
      console.log("isAdmin getter called - user:", state.user); // DEBUG
      console.log("isAdmin getter called - roles:", state.user ? state.user.roles : "No user"); // DEBUG
      console.log("isAdmin getter result:", result); // DEBUG
      return result;
    }
  }
})

export default store
