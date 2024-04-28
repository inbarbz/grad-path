<template>
    <div class="search-bar">
        <!-- Profile Fields -->
        <div class="card flex flex-column md:flex-row gap-3">
            <div class="card flex flex-column md:flex-row gap-3">
                <InputGroup>
                    <InputGroupAddon style="font-family: 'Open Sans', sans-serif;">
                        <i class="pi pi-user"> Location </i>
                    </InputGroupAddon>
                    <!-- <InputText class="w-12rem" v-model="location" placeholder="Location" /> -->
                    <AutoComplete :delay="200" dropdown class="w-20rem" v-model="location"
                        :suggestions="locationHistory" placeholder="Location" @complete="updateLocationHistory" />
                </InputGroup>
            </div>

            <div class="card flex flex-column md:flex-row gap-3">
                <InputGroup>
                    <InputGroupAddon>
                        <i class="pi pi-user"> Role </i>
                    </InputGroupAddon>
                    <!-- <InputText class="w-12rem" v-model="role" placeholder="Role" /> -->
                    <AutoComplete :delay="200" dropdown class="w-20rem" v-model="role" :suggestions="roleHistory"
                        placeholder="Role" @complete="updateRoleHistory" />
                </InputGroup>
            </div>
            <!-- Save Profile Button -->
            <div class="search-button">
                <Button label="Search!" @click="search" :disabled="loading"
                    style="background-color: rgb(193,243,86); color: black; font-family: 'Open Sans', sans-serif;"></Button>
            </div>

            <ProgressSpinner v-if="loading" style="width: 50px; height: 50px" strokeWidth="8"
                fill="var(--surface-ground)" animationDuration=".5s" aria-label="Custom ProgressSpinner" />
        </div>
        <div v-if="number_of_results > 0" class="result_statistics">
            {{ number_of_results }} jobs found for you!
        </div>
    </div>
</template>

<style scoped>
/* Add component-specific styles here */
.search-bar {
    display: flex;
    flex-direction: column;
    align-items: left;
    gap: 1rem;
    padding-left: 2x;
    padding-right: 2px;
    padding-top: 5px;
}

/* Ensure empty input still shows label */
.p-float-label span.p-input-label {
    display: block;
}
</style>


<script setup>
// Add the following import statement
import InputGroup from 'primevue/inputgroup';
import AutoComplete from 'primevue/autocomplete';
import InputGroupAddon from 'primevue/inputgroupaddon';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import ProgressSpinner from 'primevue/progressspinner';

import { useRecruitStore } from '../stores/recruit';

import { ref, watch, onMounted, onBeforeMount } from 'vue';

const store = useRecruitStore();
const location = ref('');
const role = ref('');
// is set to true when the search is in progress
const loading = ref(false);
// is set to the number of results found
const number_of_results = ref(0);
let locations = [
    "London, United Kingdom",
    "Manchester, United Kingdom",
    "Birmingham, United Kingdom",
    "Bristol, United Kingdom",
    "Cambridge, United Kingdom",
    "Nottingham, United Kingdom",
    "Edinburgh, United Kingdom",
    "Leeds, United Kingdom",
    "Belfast, United Kingdom",
    "Newcastle, United Kingdom",
    "Glasgow, United Kingdom",
    "Liverpool, United Kingdom"
];
let locationHistory = ref([]);
let roles = [
    "Product Manager Associate",
    "Data Scientist Associate",
    "Software Engineer Associate",
    "UX Designer Associate",
    "Business Analyst Associate",
    "Software Engineer Intern",
    "Product Manager Intern",



];
let roleHistory = ref([]);


const search = async () => {
    console.log('SearchBar.search()');
    loading.value = true;
    //addLocationToHistory(location.value);
    //addRoleToHistory(role.value);
    const results = await store.fetchJobs(location.value, role.value);
    number_of_results.value = store.jobs.length;
    console.log(`SearchBar.search() results.length=${number_of_results.value}`);
    loading.value = false;
};

const addLocationToHistory = (newVal) => {
    console.log(`location changed to ${newVal}`)
    if (!locationHistory.value.includes(newVal)) {
        locationHistory.value.unshift(newVal);
        console.log(`location was added! ${newVal}`)
        if (locationHistory.value.length > 5) {
            locationHistory.value.pop();
        }
    }
}

const addRoleToHistory = (newVal) => {
    if (!roleHistory.value.includes(newVal)) {
        roleHistory.value.unshift(newVal);
        console.log(`role was added! ${newVal}`)
        if (roleHistory.value.length > 5) {
            roleHistory.value.pop();
        }
    }
}

function updateLocationHistory(e) {
    console.log(`updateLocationHistory ${e.value}`);
    locationHistory.value = locations.filter((l) => {
        return l.toLowerCase().startsWith(location.value.toLowerCase());
    });
}

function updateRoleHistory(e) {
    console.log(`updateRoleHistory ${e.value}`);
    roleHistory.value = roles.filter((r) => {
        return r.toLowerCase().startsWith(role.value.toLowerCase());
    });
}

</script>
