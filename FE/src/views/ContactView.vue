<template>
    <div class="p-fluid contact-form">
        <div class="p-field contact-field">
            <label for="name">Name</label>
            <InputText id="name" v-model="form.name" />
        </div>
        <div class="p-field contact-field">
            <label for="email">Email</label>
            <InputText id="email" v-model="form.email" />
        </div>
        <div class="p-field contact-field">
            <label for="message">Message</label>
            <Textarea id="message" v-model="form.message" />
        </div>
        <Button label="Submit" @click="submitForm" style=" background-color: rgb(193,243,86); color: black;" />
    </div>

    <ModalDialog title="Contact Us" message="Message sent successfully!" v-model:visible="showModal" />
    <img src="@/assets/buttom_banner.png" alt="About Grad Path"
        style="position: fixed; bottom: 0; right: 0; width: 100%; z-index: -1;" />
</template>

<style scoped>
.contact-form {
    padding-top: 20px;
    max-width: 500px;
    margin: auto;
}

.contact-field {
    margin-bottom: 1.5rem;
}
</style>

<script setup>
import { ref } from 'vue';
import InputText from 'primevue/inputtext';
import Textarea from 'primevue/textarea';
import Button from 'primevue/button';
import ModalDialog from '../components/ModalDialog.vue';

const form = ref({
    name: '',
    email: '',
    message: ''
});

const showModal = ref(false);

const submitForm = () => {
    console.log(form.value);
    form.value = {
        name: '',
        email: '',
        message: ''
    };
    showModal.value = true;
};
</script>