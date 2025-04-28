<script setup lang="ts">
import { ref, computed } from 'vue'
import useAuth from '@/composables/useAuth'
// Import PrimeVue components
import Card from 'primevue/card'
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import Button from 'primevue/button'
import Message from 'primevue/message'

// Form state variables
const username = ref('')
const password = ref('')
const formSubmitted = ref(false)

// Get auth methods from useAuth composable
const { login, error, isLoading } = useAuth()

// Form validation
const isFormValid = computed(() => {
  return username.value.trim() !== '' && password.value.trim() !== ''
})

// Form submission handler
const handleSubmit = () => {
  formSubmitted.value = true

  if (isFormValid.value) {
    login({
      username: username.value,
      password: password.value,
    })
  }
}
</script>

<template>
  <div class="login-container">
    <Card class="login-card">
      <template #title> Log In </template>

      <template #content>
        <form @submit.prevent="handleSubmit">
          <div class="form-field">
            <label for="username">Username</label>
            <InputText
              id="username"
              v-model="username"
              :class="{ invalid: formSubmitted && !username }"
            />
            <small v-if="formSubmitted && !username" class="error-text">Username required</small>
          </div>

          <div class="form-field">
            <label for="password">Password</label>
            <Password
              id="password"
              v-model="password"
              :toggleMask="true"
              :feedback="false"
              :class="{ invalid: formSubmitted && !password }"
            />
            <small v-if="formSubmitted && !password" class="error-text">Password required</small>
          </div>

          <div v-if="error" class="error-message">
            <Message severity="error">{{ error }}</Message>
          </div>

          <div class="button-container">
            <Button type="submit" label="Login" icon="pi pi-sign-in" :loading="isLoading" />
          </div>
        </form>
      </template>
    </Card>
  </div>
</template>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: var(--surface-ground);
}

.login-card {
  width: 100%;
  max-width: 400px;
  margin: 2rem;
}

.form-field {
  margin-bottom: 1.5rem;
}

.form-field label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.invalid {
  border-color: var(--red-500) !important;
}

.error-text {
  color: var(--red-500);
}

.error-message {
  margin: 1rem 0;
}

.button-container {
  margin-top: 2rem;
  text-align: right;
}
</style>
