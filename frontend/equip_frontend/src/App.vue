<script setup></script>

<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
import router from "@/router/index.js";

export default {
  data() {
    return {
      isAuthenticated: false,
    }
  },
  mounted() {
    this.checkAuthorization()
  },
  methods: {
    checkAuthorization() {
      const token = localStorage.getItem('token')
      this.isAuthenticated = !!token
      if (token) {
        try {
          // Расшифровка токена
          const tokenData = JSON.parse(atob(token.split('.')[1]))
          // Получение данных пользователя из токена
          const userId = tokenData.user_id
          const username = tokenData.name
          // Сохранение данных пользователя в localStorage или другом месте хранения
          localStorage.setItem('userId', userId)
          localStorage.setItem('username', username)
          // Сохранение других данных пользователя...
        } catch (error) {
          console.error('Ошибка при расшифровке токена:', error)
        }
      }
    },
  }
}
</script>
<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
