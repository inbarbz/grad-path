<template>
    <!-- Your template code here -->
    <NavBar class="navbar" />
    <div class="hero">
        <div class="hero-content">

            <h1 class="text-4xl text-white font-bold" style="font-family: 'Open Sans', sans-serif;">Path your way
                towards a successful career with <nobr>GradPath</nobr>
            </h1>
            <h2 class="text-2xl text-white font-semibold" style="font-family: 'Open Sans', sans-serif;">Tailored Job
                Matching Experience for Graduates</h2>
        </div>
    </div>
</template>

<script setup>
// Your script code here
import NavBar from './NavBar.vue';
</script>

<style scoped>
.hero {
    background-image: url('../assets/gradpath.png');
    background-size: 10%;
    background-position: left 20px top 70px;
    background-repeat: no-repeat;
    background-color: #3F13C0;
    height: 250px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.navbar {
    position: absolute;
    top: 20px;
    left: 0px;
}

.p-tabmenu .p-tabmenu-nav .p-reset .ui-tabmenu .ui-tabmenu-nav .ui-tabmenuitem.ui-state-active :host ::ng-deep .ui-tabmenu .ui-tabmenu-nav .ui-tabmenuitem.ui-state-active {
    background-color: red !important;
}

.hero-content {
    width: 100%;
    align-items: center;
}

.hero-content h1 {
    font-size: 3rem;
    text-align: center;

}

.hero-content h2 {
    font-size: 2rem;
    text-align: center;
}

.hero-content-h1-nobr {
    font-size: 2rem;
    text-align: center;
    color: rgb(160, 234, 12);
}

.hero-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
}
</style>