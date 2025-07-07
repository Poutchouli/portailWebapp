import { createStore } from 'vuex'

const store = createStore({
  state: {
    user: null,
    token: localStorage.getItem('token') || null,
    isAuthenticated: false
  },
  
  mutations: {
    SET_USER(state, user) {
      state.user = user
      state.isAuthenticated = !!user
    },
    
    SET_TOKEN(state, token) {
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
        
        const response = await fetch('/token', {
          method: 'POST',
          body: formData
        })
        
        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.detail || 'Login failed')
        }
        
        const data = await response.json()
        
        // Store the token
        commit('SET_TOKEN', data.access_token)
        
        // Fetch user info
        const userResponse = await fetch('/users/me', {
          headers: {
            'Authorization': `Bearer ${data.access_token}`
          }
        })
        
        if (userResponse.ok) {
          const userData = await userResponse.json()
          commit('SET_USER', userData)
        }
        
        return { success: true }
      } catch (error) {
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
    isAdmin: state => state.user && state.user.roles && state.user.roles.includes('admin')
  }
})

export default store
