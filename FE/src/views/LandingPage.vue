<template>
  <div class="login-container">
    <h1>Path your way towards a successful career</h1>
    <p>Embark on your career journey with us, where every step leads you closer to your dream job</p>
    <form class="login-form">
      <InputText v-model="email" placeholder="E-mail" />
      <Password v-model="password" placeholder="Password" />
      <Button label="Login" />
      <Button label="Register" class="p-button-secondary" />
    </form>
    <div class="job-categories">
      <h2>Find the right job or internship position for you:</h2>
      <Button label="UX Design" class="p-button-success" />
      <Button label="Engineering" class="p-button-success" />
      <Button label="Product Management" class="p-button-success" />
      <Button label="Data Analyst" class="p-button-success" />
    </div>
  </div>
</template>

<script>
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import Button from 'primevue/button';

export default {
  data() {
    return {
      email: '',
      password: ''
    };
  },
  components: {
    InputText,
    Password,
    Button
  }
};
</script>

<style>
.login-container {
  max-width: 600px;
  margin: auto;
  text-align: center;
}

.login-form {
  margin-top: 20px;
}

.job-categories {
  margin-top: 40px;
}

/* Add additional styles here */
</style>
