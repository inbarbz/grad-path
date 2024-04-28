<script setup>
import { onMounted } from 'vue';
import { RouterLink, RouterView } from 'vue-router'
import Hero from './components/Hero.vue'
import { useRecruitStore } from './stores/recruit';

const store = useRecruitStore();

onMounted(async () => {
  await store.fetchProfile();
});

</script>

<template>
  <header>
    <Hero />
  </header>
  <RouterView />
</template>
