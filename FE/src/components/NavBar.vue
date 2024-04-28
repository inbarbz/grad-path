<template>
    <div class="card menu-container">
        <TabMenu :model="items" class="clear-tab-menu my-menu">
        </TabMenu>
        <div v-if="loggedIn" class="card flex justify-content-center">
            <a href="#" @click="toggle" aria-haspopup="true" aria-controls="overlay_menu">
                <Avatar v-if="store.profileImage" :image="store.profileImage" shape="circle" class="user-avatar" />
                <Avatar v-else image="src/assets/avatar.jpeg" shape="circle" class="user-avatar" size="xlarge" />
            </a>
            <Menu ref="menu" id="overlay_menu" :model="loggedin_items" :popup="true" />
        </div>
        <div v-else>
            <a href="#" @click="router.push('/login');">
                <Avatar :image="defaultAvatar" shape="circle" class="user-avatar" />
            </a>
        </div>
    </div>
</template>

<script setup>
import router from '@/router';
//import Menubar from 'primevue/menubar';
import TabMenu from 'primevue/tabmenu';
import Avatar from 'primevue/avatar';
import Menu from 'primevue/menu';
import { ref, watch } from "vue";
import { useRecruitStore } from '../stores/recruit';

const store = useRecruitStore();
const menu = ref();
const loggedIn = ref(false);

// get path to the assets dir from environment variables
const assetsDir = import.meta.env.VITE_ASSETS_DIR;
const defaultAvatar = ref(`${assetsDir}/default-avatar.jpeg`);

watch(
    () => store.isLoggedIn,
    async (newVal, oldVal) => {
        const value = await newVal;
        console.log(`Navbar.watch(store.isLoggedIn) value=${value}`);
        if (value) {
            loggedIn.value = true;
        } else {
            loggedIn.value = false;
        }
    }
);

const isLoggedIn = async () => {
    const loginResult = await store.isLoggedIn;
    console.log('Navbar.isLoggedIn ', loginResult);
    return loginResult
}

const toggle = () => {
    menu.value.toggle(event);
}

const loggedin_items = ref([
    {
        label: 'Profile',
        icon: 'pi pi-user',
        command: () => {
            router.push('/profile');
        }
    },
    {
        label: 'Logout',
        icon: 'pi pi-sign-out',
        command: () => {
            store.logout();
            router.push('/login');
        }
    }
]);

const items = ref([
    {
        label: 'Home',
        icon: 'pi pi-home',
        command: () => {
            router.push('/');
        }
    },
    {
        label: 'About',
        icon: 'pi pi-info-circle',
        command: () => {
            router.push('/about');
        }

    },
    {
        label: 'Contact',
        icon: 'pi pi-envelope',
        command: () => {
            router.push('/contactus');
        }
    },
    {
        label: 'Help',
        icon: 'pi pi-question-circle',
        command: () => {
            router.push('/help');
        }
    },
]);
</script>

<style scoped>
/* Your component's styles go here */
.navbar {
    width: 100%;
    padding: 0 2rem;
}

.right-aligned-item {
    text-align: right;
    /* Align content to the right */
}

.menu-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.my-menu {
    flex: 1;
    /* Allows the menu to take up the available space */
    background-color: transparent !important;
    /* Override background color */
}

:v-deep .p-tabmenu .p-tabmenu-nav {
    background-color: transparent !important;
}

:v-deep .p-tabmenuitem {
    background-color: transparent !important;
}

.user-avatar {
    float: right;
    margin-right: 10px;
    width: 50px;
    height: 50px;
    padding: 1px;
    background-color: white;
    margin-left: 1px;
}
</style>
