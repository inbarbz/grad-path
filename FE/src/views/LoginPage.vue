<template>
    <div class="grid" style="background-color:rgb(245,245,245); margin-bottom:10%;height:100%;">
        <!-- <img src="@/assets/title.png" alt="login Grad Path" style="position: fixed; height:15%; z-index: -1;" /> -->

        <div class="col-8">
            <h1
                style="margin-left: 0.8rem; color: rgb(63,19,192); font-family: 'Open Sans', sans-serif; font-size:x-large">
                Path Your Way
                For Success
            </h1>
            <h2
                style="color: rgb(63,19,192); margin-left: 0.8rem; font-family: 'Open Sans', sans-serif; font-size:medium">
                Embark on your
                career journey with us,
                where every step leads you closer to your dream job</h2>
            <form>
                <div class="card">
                    <div class="flex flex-column md:flex-row">
                        <div
                            class="w-full md:w-5 flex flex-column align-items-center justify-content-center gap-3 py-5">
                            <div>
                                <div class="flex-wrap justify-content-left align-items-center gap-2"
                                    style="padding-bottom: 15px;">
                                    <label class="w-8rem" style="padding-right:10px;">Email</label>
                                    <br />
                                    <InputText id="login_email" type="email" class="w-12rem" v-model="login_email"
                                        required />
                                    <br />
                                    <small class="p-error" id="login_email_error_id">{{ login_email_error || '&nbsp;'
                                        }}</small>
                                </div>

                                <div class="flex-wrap justify-content-left align-items-center gap-2"
                                    style="padding-bottom: 15px;">
                                    <label class="w-8rem" style="padding-right:10px;">Password</label>
                                    <br />
                                    <InputText id="login_password" class="w-12rem" type="password"
                                        v-model="login_password" required />
                                    <br />
                                    <small class="p-error" id="login_password_error_id">{{ login_password_error ||
                                        '&nbsp;'
                                        }}</small>
                                </div>


                                <Button label="Login" icon="pi pi-user" class="w-10rem mx-auto" @click="login"
                                    style="background-color: rgb(193,243,86); color: black;"></Button>
                            </div>
                        </div>
                        <div class="w-full md:w-2">
                            <Divider layout="vertical" class="hidden md:flex"><b
                                    style=" background-color: rgb(245,245,245); font-family: 'Open Sans', sans-serif; font-size:large">OR</b>
                            </Divider>
                            <Divider layout="horizontal" class="flex md:hidden" align="center"><b>OR</b></Divider>
                        </div>

                        <div class="w-full md:w-5 flex align-items-center justify-content-center py-5">

                            <Button label="Sign Up" icon="pi pi-user-plus" severity="success" class="w-10rem"
                                @click="showSignupModal = true"
                                style="background-color: rgb(193,243,86); color: black;"></Button>
                        </div>

                    </div>

                </div>
                <img src="@/assets/signup_buttom.png" alt="About Grad Path" style=" width: 100%; display: block; margin-left:0.9rem;
  margin-right: auto;" />
            </form>

        </div>

        <div class="col-4">
            <img src="@/assets/signup.png" alt="signup Grad Path" style="width:90%; margin-top: 2rem;" />
        </div>


        <Dialog v-model:visible="showSignupModal" header="Sign Up" class="w-20rem" modal>
            <div class="flex-wrap justify-content-center align-items-center gap-2" style="padding-bottom:15px">
                <label class="w-6rem">Email</label>
                <br />
                <InputText id="signup_email" type="email" class="w-12rem" v-model="signup_email"
                    :class="{ 'p-invalid': signup_email_error }" />
                <br />
                <small class="p-error" id="signup_email_error_id">{{ signup_email_error || '&nbsp;' }}</small>
            </div>

            <div class="flex-wrap justify-content-center align-items-center gap-2" style="padding-bottom:15px">
                <label class="w-6rem">Password</label>
                <br />
                <InputText id="signup_password" class="w-12rem" type="password" v-model="signup_password"
                    :class="{ 'p-invalid': signup_password_error }" />
                <br />
                <small class="p-error" id="signup_password_error_id">{{ signup_password_error || '&nbsp;' }}</small>
            </div>

            <Button label="Sign Up" icon="pi pi-user-plus" class="w-10rem mx-auto" @click="signUp"
                @hide="showSignupModal = true" style="background-color: rgb(193,243,86); color: black;"> </Button>

            <div class="card flex justify-content-center" v-if="showRegisterSpinner">
                <ProgressSpinner style="width: 50px; height: 50px" strokeWidth="8" fill="var(--surface-ground)"
                    animationDuration=".5s" aria-label="Custom ProgressSpinner" />
            </div>

        </Dialog>

        <ModalDialog title="Login Failed!" message="Username or Password are wrong. Please try again"
            v-model:visible="isDialogVisible" />
        <div style="background-color: rgb(245,245,245);">


        </div>
    </div>

</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import Divider from 'primevue/divider';
import Dialog from 'primevue/dialog';
import router from '@/router';
import ProgressSpinner from 'primevue/progressspinner';
import { useRecruitStore } from '../stores/recruit';
import ModalDialog from '../components/ModalDialog.vue';

import { useField } from 'vee-validate';

const store = useRecruitStore();
const showRegisterSpinner = ref(false);
const isDialogVisible = ref(false);


const openErrorDialog = () => {
    isDialogVisible.value = true;
};


const validateEmailField = (value) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(value)) {
        return 'Email must be valid';
    }
    return true;
}

const validatePasswordField = (value) => {
    if (value == undefined || value.length < 8) {
        return 'at least 8 characters';
    }
    return true;
}

const { value: signup_email, errorMessage: signup_email_error } = useField('signup_email', validateEmailField);
const { value: signup_password, errorMessage: signup_password_error } = useField('signup_password', validatePasswordField);

const { value: login_email, errorMessage: login_email_error } = useField('login_email', validateEmailField);
const { value: login_password, errorMessage: login_password_error } = useField('login_password', validatePasswordField);

watch(
    () => store.isLoggedIn,
    async (newVal, oldVal) => {
        const value = await newVal;
        console.log(`LoginPage.watch(store.isLoggedIn) value=${value}`);
        if (value) {
            console.log('LoginPage.watch(store.isLoggedIn) isLoggedIn=true! redirecting to home page.');
            router.push('/');
        }
    }
);

onMounted(async () => {
    console.log('LoginPage.onMounted()');
    if (await store.isLoggedIn) {
        console.log('LoginPage.onMounted() isLoggedIn=true! redirecting to home page.');
        router.push('/');
    }
});

const signUp = async () => {
    console.log('signUp ', signup_email.value, signup_password.value);
    showRegisterSpinner.value = true;
    const signupResult = await store.signup(signup_email.value, signup_password.value);
    showSignupModal.value = false;
    showRegisterSpinner.value = false;
}

const login = async () => {
    console.log('LoginPage.login() ', login_email.value, login_password.value);
    showRegisterSpinner.value = true;
    const loginResult = await store.login(login_email.value, login_password.value);
    showSignupModal.value = false;
    showRegisterSpinner.value = false;
    console.log('LoginPage.login() ', loginResult);
    if (loginResult) {
        console.log('LoginPage.login() Successfull!! navigate to HOME');
        // navigate to the home page
        router.push('/');
    } else {
        console.log('LoginPage.login() Failed!!');
        openErrorDialog();
    }
}


const showSignupModal = ref(false);
</script>
