<template>
    <div class="card">
        <DataView :value="store.jobs">
            <template #list="slotProps">
                <div class="grid grid-nogutter">
                    <div v-for="(item, index) in slotProps.items" :key="index" class="col-12">
                        <div class="flex flex-column xl:flex-row xl:align-items-start p-4 gap-4"
                            :class="{ 'border-top-1 surface-border': index !== 0 }">

                            <!-- company icon -->
                            <img class="w-9 sm:w-16rem xl:w-6rem shadow-2 block xl:block mx-auto border-round"
                                :src="getCompanyIcon(item)" :alt="item.name" />
                            <div
                                class="flex flex-column sm:flex-row justify-content-between align-items-center xl:align-items-start flex-1 gap-4">
                                <div class="flex flex-column align-items-center sm:align-items-start gap-3">

                                    <div class="text-2xl font-bold text-900" style="color:rgb(0, 255, 0);">{{ item.title
                                        }}
                                    </div>
                                    <div class="text-2xl text-900">{{ item.company }}</div>

                                    <!-- <Rating :modelValue="3" readonly :cancel="false"></Rating> -->

                                    <div class="flex align-items-center gap-3">
                                        <span class="flex align-items-center gap-2">
                                            <i class="pi pi-building"></i>
                                            <span class="font-semibold">{{ item.location }}</span>
                                        </span>
                                        <span class="flex align-items-center gap-2">
                                            <i class="pi pi-briefcase"></i>
                                            <span class="font-semibold">{{ getExperience(item) }}</span>
                                        </span>
                                        <span class="flex align-items-center gap-2">
                                            <i class="pi pi-calendar"></i>
                                            <span class="font-semibold">{{ item.posted_date }}</span>
                                        </span>
                                        <span class="flex align-items-center gap-2">
                                            <MatchScore :score="item.match_score"></MatchScore>
                                        </span>
                                        <!-- <Tag :value="item.status" :severity="getSeverity(item)"></Tag> -->
                                    </div>

                                    <!-- technical_skills -->
                                    <div v-if="item.extracted_data" class="flex align-items-center gap-3">
                                        <strong>Technical Skills:</strong>
                                        <span v-for="(skill, index) in item.extracted_data.technical_skills"
                                            :key="index">
                                            {{ skill }}<span v-if="index !== item.extracted_data.technical_skills - 1">,
                                            </span>
                                        </span>
                                    </div>

                                    <!-- soft_skills -->
                                    <div v-if="item.extracted_data" class="flex align-items-center gap-3">
                                        <strong>Soft Skills:</strong>
                                        <span v-for="(skill, index) in item.extracted_data.soft_skills" :key="index">
                                            {{ skill }}<span v-if="index !== item.extracted_data.soft_skills - 1">,
                                            </span>
                                        </span>
                                    </div>

                                    <!-- social_skills -->
                                    <div v-if="item.extracted_data" class="flex align-items-center gap-3">
                                        <strong>Social Skills:</strong>
                                        <span v-for="(skill, index) in item.extracted_data.social_skills" :key="index">
                                            {{ skill }}<span v-if="index !== item.extracted_data.social_skills - 1">,
                                            </span>
                                        </span>
                                    </div>

                                    <ScrollPanel header="Description" style="width: 100%; height: 200px">
                                        <p class="m-0">
                                            <strong>Description:</strong>
                                            {{ item.description }}
                                        </p>
                                    </ScrollPanel>

                                </div>
                                <div class="flex sm:flex-column align-items-center sm:align-items-end gap-3 sm:gap-2">
                                    <!-- <span class="text-2xl font-semibold">${{ item.salary }}</span> -->
                                    <Button icon="pi pi-briefcase" rounded @click="navigateTo(item.url)"></Button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </template>
        </DataView>
    </div>
</template>

<script setup>
import { useRecruitStore } from '../stores/recruit'
import MatchScore from './MatchScore.vue'

import DataView from 'primevue/dataview';
import Button from 'primevue/button';
import Rating from 'primevue/rating';
import Panel from 'primevue/panel';
import ScrollPanel from 'primevue/scrollpanel';
import Tag from 'primevue/tag';
import { ref, watch } from 'vue'

const store = useRecruitStore()

watch(() => store.jobs, (newVal, oldVal) => {
    console.log('JobsList.watch(store.jobs) newVal=', newVal)
})


const navigateTo = (url) => {
    window.open(url, '_blank');
};

const getExperience = (item) => {
    let result = "";
    if ("extracted_data" in item && item.extracted_data !== null) {
        result += "mandatory_experience_years" in item.extracted_data ? `${item.extracted_data.mandatory_experience_years}` : "";
        result += "optional_experience_years" in item.extracted_data ? ` (+${item.extracted_data.optional_experience_years})` : "";
        result += " years";
    }
    return result;
}

const getCompanyIcon = (job) => {
    if (job.thumbnail !== null) {
        return job.thumbnail;
    }

    switch (job.company.toLowerCase()) {
        case 'google':
            return 'https://lh3.googleusercontent.com/COxitqgJr1sJnIDe8-jiKhxDx1FrYbtRHKJ9z_hELisAlapwE9LUPh6fcXIfb5vwpbMl4xl9H9TRFPc5NOO8Sb3VSgIBrfRYvW6cUA';

        case 'facebook':
            return 'https://cdn.iconscout.com/icon/free/png-512/free-facebook-262-721949.png?f=webp&w=512';

        case 'barclays':
            return 'https://logos-world.net/wp-content/uploads/2021/08/Barclays-Logo.png';

        case 'visa':
            return 'https://logos-world.net/wp-content/uploads/2020/05/Visa-Logo.png';

        case 'bbc':
            return 'https://logos-world.net/wp-content/uploads/2022/01/BBC-Logo.png';

        case 'pion':
            return 'https://media.licdn.com/dms/image/D4E0BAQFktv9bPE57Ng/company-logo_200_200/0/1706019041756/wearepionglobal_logo?e=1719446400&v=beta&t=n-eqxY8YipBK7yPWyjyv10E0ymNwxqn3Yu8nqZ0H6Zs';

        case 'method resourcing':
            return 'https://media.licdn.com/dms/image/D4E0BAQEw6nnrHpPpww/company-logo_200_200/0/1702980662902/method_resourcing_logo?e=1719446400&v=beta&t=6vfzDh07olQm4ttLA_L6Ie0dX_tZX6znUpjJcIfA4wY';

        case 'thomson reuters':
            return 'https://media.licdn.com/dms/image/D560BAQE19sMyPAjgtg/company-logo_200_200/0/1710205707612/thomson_reuters_logo?e=1719446400&v=beta&t=ubNe7LF2aJGL87kos1ecUmHbLF12EjXXCO_qr7oXgro';

        case 'aicpa':
            return 'https://www.aicpa-cima.com/static/media/aicpa-cima-logo.2028af8b.svg';

        case 'leverton search':
            return 'https://media.licdn.com/dms/image/C560BAQF755xIRCSedQ/company-logo_200_200/0/1631381457306?e=1719446400&v=beta&t=xKOM7537-N0PDcDscr_Ll8YOdZBgI-ZirS3Nv6bpS08';

        case 'warnermedia':
            return 'https://www.dexigner.com/images/news/xxw/32564.jpg';

        case 'search 5.0':
            return 'https://media.licdn.com/dms/image/C4E0BAQHYdHwvJ0CL5w/company-logo_200_200/0/1669818244921/search5point0_logo?e=1719446400&v=beta&t=Idg0ut8lnc-wMQI24-lflNHaOsRH_-2eBNRZjmvRinM';

        case 'monday.com':
            return 'https://dapulse-res.cloudinary.com/image/upload/f_auto,q_auto/remote_mondaycom_static/img/monday-logo-x2.png';

        case 'citi':
            return 'https://www.fintechfutures.com/files/2016/09/Citi-logo.jpg';

        case 'zynga':
            return 'https://upload.wikimedia.org/wikipedia/en/thumb/7/7b/Zynga.svg/440px-Zynga.svg.png';

        default:
            return null;
    }
};

const getSeverity = (job) => {
    switch (job.location) {
        case 'Remote':
            return 'success';

        case 'In Office':
            return 'warning';

        case 'Other':
            return 'danger';

        default:
            return null;
    }
};

const jobs = store.jobs
</script>

<style scoped>
/* Add your custom styles here */
.card {
    background: var(--surface-card);
    padding: 2rem;
    border-radius: 10px;
    margin-bottom: 1rem;
}

p {
    line-height: 1.75;
}
</style>
