<template>
    <div>
        <SearchBar />
        <JobsList />
    </div>
    <img
    src="@/assets/buttom_banner.png"
    alt="About Grad Path"
    style="position: fixed; bottom: 0; right: 0; width: 100%; z-index: -1;"
  />
</template>

<script setup>
//import { defineComponent } from 'vue';

import { useRecruitStore } from '../stores/recruit';
import JobsList from '@/components/JobsList.vue';
import SearchBar from '@/components/SearchBar.vue';


const store = useRecruitStore();

const profile = store.getProfile;
</script>

<style>
/* Add your styles here */
</style>
