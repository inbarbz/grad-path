<template>
    <form>
        <div v-if="showSpinner" class="spinner_div">
            <ProgressSpinner strokeWidth="8" fill="var(--surface-ground)" animationDuration=".5s"
                aria-label="Custom ProgressSpinner" />
        </div>

        <div class="profile-management">
            <h1 style="font-family: 'Open Sans', sans-serif;">Profile Management</h1>
            <div style="width: 83%;">


                <!-- Profile Fields -->
                <div class="card flex flex-column md:flex-row gap-3">
                    <InputGroup>
                        <InputGroupAddon>
                            <i class="pi pi-user"> Name </i>
                        </InputGroupAddon>
                        <InputText class="w-5rem" v-model="profile.name" placeholder="Name" />
                    </InputGroup>
                </div>
                <br />
                <div class="card flex flex-column md:flex-row gap-3">
                    <InputGroup>
                        <InputGroupAddon>
                            <i class="pi pi-building"> University name </i>
                        </InputGroupAddon>
                        <InputText class="w-12rem" v-model="profile.university" placeholder="University name" />
                    </InputGroup>
                </div>
                <br />
                <div class="p-field card">
                    <InputGroup>
                        <InputGroupAddon>
                            <i class="pi pi-calendar-plus"> Graduation date </i>
                        </InputGroupAddon>
                        <Calendar id="graduationDate" v-model="profile.graduationDate" placeholder="Graduation date"
                            :minDate="minGraduationDate" :maxDate="maxGraduationDate" />
                    </InputGroup>
                </div>
                <br />
                <div class="card flex flex-column md:flex-row gap-3">
                    <InputGroup>
                        <InputGroupAddon>
                            <i class="pi-star-fill"> GPA </i>
                        </InputGroupAddon>

                        <InputNumber class="w-12rem" v-model="profile.GPA" placeholder="GPA" mode="decimal"
                            :minFractionDigits=2 :min=0 :max=5 />
                    </InputGroup>
                </div>
            </div>

            <!-- Profile Image Upload-->
            <div class="grid">
                <div class="col-7">
                    <div class="card flex flex-column md:flex-row gap-3 vertical-align-middle">
                        <InputGroup class="align-items-center">
                            <InputGroupAddon>
                                <i class=" pi pi-image"> Profile Image Upload </i>
                            </InputGroupAddon>
                            <FileUpload id="profileImage" mode="basic" name="profileImage" accept="image/jpeg" auto
                                chooseLabel="Choose Image" @select="onProfileImageUpload"
                                style="background-color: rgb(160, 234, 12); width:12rem; color:black;" />
                            <div style="padding-left: 5px;">
                                {{ profile.profileImage ? profile.profileImage.name : '' }}
                            </div>
                        </InputGroup>
                    </div>
                    <br />
                    <div class="card flex flex-column md:flex-row gap-3">
                        <InputGroup class="align-items-center">
                            <InputGroupAddon>
                                <i class="pi pi-file-pdf"> Resume / CV Upload </i>
                            </InputGroupAddon>
                            <FileUpload id="resume" mode="basic" name="resume" accept=".pdf" auto
                                chooseLabel="Choose File" @select="onResumeUpload"
                                style="background-color: rgb(160, 234, 12); width:11.8rem; color:black;" />
                            <div style="padding-left: 5px;">
                                {{ profile.resume ? profile.resume.name : '' }}
                            </div>
                        </InputGroup>
                    </div>
                </div>
                <div class="col-5">
                    <img src="@/assets/apply.png" alt="About Grad Path" style=" max-width: 60%; left:0;">

                </div>
            </div>
            <div class="experience">
                <h2 style="font-family: 'Open Sans', sans-serif;">Experience</h2>
                <ul>
                    <li v-for="experience in experienceHistory" :key="experience.company_name">
                        <strong>{{ experience.company_name }}</strong> - {{ experience.job_title }} ({{
            experience.start_date }} - {{ experience.end_date }})
                    </li>
                </ul>
            </div>

            <div class="education" style="margin-bottom: 0rem;">
                <h2 style="font-family: 'Open Sans', sans-serif;">Education</h2>
                <ul>
                    <li v-for="education in educationHistory" :key="education.institution_name">
                        <strong>{{ education.institution_name }}</strong> - {{ education.degree }}, {{
            education.field_of_study }} ({{
            education.graduation_date }})
                    </li>
                </ul>
            </div>
            <div class="skills">
                <h2 style="font-family: 'Open Sans', sans-serif;">Skills</h2>
                <strong>Social Skills:</strong> {{ socialSkills.join(', ') }}
                <br>
                <strong>Technical Skills:</strong> {{ technicalSkills.join(', ') }}
                <br>
                <strong>Soft Skills:</strong> {{ softSkills.join(', ') }}
            </div>
            <div style="width: 80%;">

                <div class="Skills">
                    <label style="padding-bottom: 3px;padding-left: 3px;">Skills:</label>
                    <ChipSelector :chip-names="store.getSkills" :selectedChipNames="selectedChips"
                        @update:selectedChips="updateSelected" />
                </div>
            </div>

            <div class="certifications">
                <h2 style="font-family: 'Open Sans', sans-serif;">Certifications</h2>
                <ul>
                    <li v-for="certification in certificationHistory" :key="certification.certification_name">
                        <strong>{{ certification.certification_name }} by {{ certification.issuing_organization
                            }}</strong> - {{ date_issued }}
                    </li>
                </ul>
            </div>

            <!-- Save Profile Button -->
            <div class="save-profile">
                <Button label="Save Profile" @click="handleSubmit" :disabled="showSpinner"
                    style="background-color: rgb(160, 234, 12); color:black; margin-top: 4rem;"></Button>
            </div>
        </div>
        <img src="@/assets/buttom_banner.png" alt="About Grad Path" style="bottom: 0; right: 0; width: 100%; " />
    </form>
</template>

<style scoped>
/* Add component-specific styles here */
.profile-management {
    display: flex;
    flex-direction: column;
    align-items: left;
    gap: 1rem;
    padding-left: 10px;
    padding-right: 10px;
}

/* Ensure empty input still shows label */
.p-float-label span.p-input-label {
    display: block;
}

.Skills {
    padding: 3px;
    border: 1px solid #000;
    /* Change the color as needed */
    border-radius: 10px;
    /* Adjust the radius as needed */
}


.spinner_div {
    display: flex;
    justify-content: center;
    align-items: center;
    position: fixed;
    /* Fixed position, relative to the page, not the parent container */
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(245, 245, 220, 0.5);
}
</style>


<script setup>
// Add the following import statement
import InputGroup from 'primevue/inputgroup';
import InputGroupAddon from 'primevue/inputgroupaddon';
import InputText from 'primevue/inputtext';
import InputNumber from 'primevue/inputnumber';
import Calendar from 'primevue/calendar';
import FileUpload from 'primevue/fileupload'
import Button from 'primevue/button';
import ProgressSpinner from 'primevue/progressspinner';


import ChipSelector from '../components/ChipSelector.vue';
import { useRecruitStore } from '../stores/recruit';

import { ref, onMounted, onBeforeMount } from 'vue';

const showSpinner = ref(false);

const experienceHistory = ref([])
const educationHistory = ref([])
const certificationHistory = ref([])
const socialSkills = ref([])
const technicalSkills = ref([])
const softSkills = ref([])


const profile = ref({
    name: '',
    DOB: null,
    university: '',
    GPA: null,
    degree: '',
    graduationDate: null,
    intern_work_experience_years: 0,
    full_time_work_experience_years: 0,
    // Use refs to handle file data
    resume: ref(null),
    profileImage: ref(null),
    original_resume_file_name: ref(null),
    original_image_file_name: ref(null),
});

const uploadURL = 'http://127.0.0.1:8000/profile/';

const store = useRecruitStore();

const updateFromStore = async () => {
    console.log('ProfilePage.updateFromStore()');
    const storeProfile = await store.getProfile;
    if (storeProfile == null || "name" in storeProfile == false) {
        console.log('ProfilePage.onBeforeMount() storeProfile is null or not initialized');
        return;
    }
    profile.value.name = storeProfile.name;
    profile.value.DOB = storeProfile.DOB;
    profile.value.university = storeProfile.university;
    profile.value.degree = storeProfile.degree;
    profile.value.GPA = storeProfile.gpa;
    profile.value.graduationDate = storeProfile.graduation_date;
    profile.value.intern_work_experience_years = storeProfile.intern_work_experience_years;
    profile.value.full_time_work_experience_years = storeProfile.full_time_work_experience_years;
    profile.value.resume = storeProfile.resume;
    profile.value.profileImage = storeProfile.profile_image;
    profile.value.original_resume_file_name = storeProfile.original_resume_file_name;
    profile.value.original_image_file_name = storeProfile.original_image_file_name;
    experienceHistory.value = storeProfile.resume_parameters ? storeProfile.resume_parameters.experience : [];
    educationHistory.value = storeProfile.resume_parameters ? storeProfile.resume_parameters.education : [];
    socialSkills.value = storeProfile.resume_parameters ? storeProfile.resume_parameters.social_skills : [];
    certificationHistory.value = storeProfile.resume_parameters ? storeProfile.resume_parameters.certifications : [];
    technicalSkills.value = storeProfile.resume_parameters ? storeProfile.resume_parameters.technical_skills : [];
    softSkills.value = storeProfile.resume_parameters ? storeProfile.resume_parameters.soft_skills : [];
    updateSelected(storeProfile.skills);
}

onBeforeMount(async () => {
    await updateFromStore();
});

const oneYear = 365 * 24 * 60 * 60 * 1000
const minGraduationDate = ref(new Date(Date.now() - 3 * oneYear))
const maxGraduationDate = ref(new Date(Date.now() + 2 * oneYear))
const minDOBDate = ref(new Date(Date.now() - 50 * oneYear))
const maxDOBDate = ref(new Date(Date.now() - 12 * oneYear))

const selectedChips = ref([]);


const updateSelected = (newSelectedChips) => {
    selectedChips.value = newSelectedChips;
    console.log("updateSelected() Selected chips: ", selectedChips.value);
};

const onResumeUpload = (event) => {
    profile.value.resume = event.files[0];
};

const onProfileImageUpload = (event) => {
    profile.value.profileImage = event.files[0];
};

const handleSubmit = async () => {
    try {
        // Form validation would go here
        showSpinner.value = true;

        const response = await store.updateProfile(
            profile.value.name,
            profile.value.DOB,
            profile.value.university,
            profile.value.graduationDate,
            profile.value.GPA,
            profile.value.resume,
            profile.value.profileImage,
            selectedChips.value
        );

        await store.fetchProfile();
        await updateFromStore();


        showSpinner.value = false;

        if (response.ok) {
            console.log(`Profile submitted successfully! with response = ${response}`);
            // Optionally clear the form after submission
        } else {
            console.error('Error submitting data: ', response);
        }
    } catch (error) {
        showSpinner.value = false;
        console.error('Submission error:', error);
    }
};

</script>
