<template>
  <div class="login-form">

    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <input
            v-model="email"
            class="form-input"
            name="email"
            placeholder="Введите email"
            type="email"
        />
        <div v-if="errors.email" class="error-message">{{ errors.email }}</div>
      </div>
      <div class="form-group">
        <input
            v-model="password"
            class="form-input"
            name="password"
            placeholder="Введите пароль"
            type="password"
        />
        <div v-if="errors.password" class="error-message">{{ errors.password }}</div>
      </div>
      <button class="form-button" type="submit">Войти</button>
    </form>
    <div v-if="loginError" class="error-message">{{ loginError }}</div>
  </div>
</template>

<script>
import axios from 'axios'
import {toast} from 'vue3-toastify'

export default {
  name: 'UserLogin',
  data() {
    return {
      email: '',
      password: '',
      errors: {},
      loginError: ''
    }
  },
  methods: {
    errorToast(text) {
      toast(text, {
        theme: 'colored',
        type: 'error',
        position: toast.POSITION.BOTTOM_RIGHT
      })
    },
    async handleLogin() {
      this.errors = {}
      this.loginError = ''
      try {
        const link = `/api/user/login/`
        const data = {
          email: this.email,
          password: this.password
        }
        axios
            .post(link, data, {
              headers: {
                'Content-Type': 'application/json'
              }
            })
            .then((response) => {
              const json = response.data
              this.token = json.access
              this.refresh = json.refresh
              localStorage.setItem('token', this.token)
              localStorage.setItem('refresh', this.refresh)
              this.$router.push('/')
            })
            .catch((error) => {
              if (error.response && error.response.status === 400) {
                if (error.response.data.non_field_errors) {
                  this.loginError = error.response.data.non_field_errors[0]
                  this.errorToast('Проверьте введённые данные.')
                } else {
                  this.errors = error.response.data
                }
              } else {
                this.errorToast('Проверьте введённые данные.')
              }
            })
      } catch (error) {
        this.errorToast('Ошибка входа на сайт.')
      }
    }
  }
}
</script>

<style scoped>
.login-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

.form-group {
  margin-bottom: 1rem;
  width: 100%;
  max-width: 500px;
  display: flex;
  flex-direction: column;
}

.form-input {
  padding: 0.5rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 100%;
}

.error-message {
  color: red;
  font-size: 0.8rem;
  margin-top: 0.2rem;
}

.form-button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  width: 100%;
  max-width: 500px;
}

.form-button:hover {
  background-color: #2980b9;
}

.forgot-password-link {
  margin-top: 1rem;
  font-size: 0.9rem;
  color: #3498db;
  text-decoration: none;
  cursor: pointer;
}

.forgot-password-link:hover {
  text-decoration: underline;
}

</style>
