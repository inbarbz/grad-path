import { ref, computed } from "vue";
import router from "@/router";
import { defineStore } from "pinia";
import { fake_jobs, fake_profile, fake_skills } from "./fake_data.js";

const use_fake_data = false;
const localStoreFilePath = "../local_store.json";

// get the URL from the .env file
const backendUrl = import.meta.env.VITE_BACKEND_API_URL;
const viteEnvironment = import.meta.env.VITE_ENVIRONMENT;
//const backendUrl = "http://localhost:8000";

export const useRecruitStore = defineStore("recruit", {
  state: () => ({
    jobs: [],
    profile: null,
    skills: [],
    loading: true,
    profileImage: null,
  }),
  getters: {
    async isLoggedIn() {
      if (this.loading) {
        console.log("store.isLoggedIn() loading profile...");
        if (await this.fetchProfile()) {
          await this.fetchSkills();
        }
      }
      console.log("store.isLoggedIn() returning " + (this.profile !== null));
      return this.profile !== null;
    },
    getProfile() {
      return this.profile;
    },
    getSkills() {
      console.log("store.getSkills() returning skills=", this.skills);
      return this.skills;
    },
    isLoading() {
      return this.loading;
    },
  },
  // actions
  actions: {
    initializeFakeDataIfNeeded() {
      if (use_fake_data) {
        this.jobs = fake_jobs;
        this.profile = fake_profile;
        this.skills = fake_skills;
      }
    },
    // apply for a job
    apply(job_id) {
      console.log("apply for job", job_id);
    },
    async login(email, password) {
      console.log(
        `recruit.store.login() userName=${email} password=${password} backendUrl=${backendUrl} ...`
      );
      this.profile = null;
      if (use_fake_data) {
        return new Promise((resolve, reject) => {
          setTimeout(() => {
            this.profile = fake_profile;
            resolve(true);
          }, 1000);
        });
      } else {
        try {
          const response = await fetch(backendUrl + "/login", {
            method: "POST",
            body: JSON.stringify({ email, password }),
            headers: {
              "Content-Type": "application/json",
            },
            credentials: "include", // This is important for handling cookies
          });
          console.log(
            `recruit.store.login() response=${JSON.stringify(response)}`
          );
          if (response.ok) {
            console.log(`recruit.store.login() response.ok=${response.ok}!!!`);
            const profileResult = await this.fetchProfile();
            return true;
          } else {
            return false;
          }
        } catch (error) {
          console.error(`recruit.store.login() error=${error}`);
          return false;
        }
      }
    },
    async signup(email, password) {
      console.log(`signup() userName=${email} password=${password}`);
      this.profile = null;
      if (use_fake_data) {
        return new Promise((resolve, reject) => {
          setTimeout(() => {
            this.profile = fake_profile;
            resolve(true);
          }, 1000);
        });
      } else {
        const response = await fetch(backendUrl + "/signup", {
          method: "POST",
          body: JSON.stringify({ email, password }),
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include", // This is important for handling cookies
        });
        if (response.ok) {
          return await this.login(email, password);
        } else {
          return false;
        }
      }
    },
    async logout() {
      console.log(`logout() ...`);
      const response = await fetch(backendUrl + "/logout", {
        method: "POST",
        //mode: 'no-cors', // no-cors mode
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include", // This is important for handling cookies
      });
      console.log(`logout() response=${response}`);
      this.profile = null;
      this.profileImage = null;
      // redirect to the home page using the router
      router.push("/login");
      console.log(`logout() done. navigating to home page...`);
    },
    async getProfileImage() {
      const response = await fetch(backendUrl + "/profile_image", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include", // This is important for handling cookies
      });
      if (response.ok) {
        console.log("getProfileImage() response.ok=true");
        const blob = await response.blob();
        this.profileImage = URL.createObjectURL(blob);
        console.log(`getProfileImage() profileImage=${this.profileImage}`);
      } else {
        console.log("getProfileImage() response.ok=false");
      }
    },
    loadFromLocalStore() {
      fetch(localStoreFilePath)
        .then((response) => response.json())
        .then((data) => {
          console.log(`loadFromLocalStore() data.length=${data.length}`);
          jobs.value = data;
        })
        .catch((err) => {
          console.error(`loadFromLocalStore() error loading json file ${err}`);
        });
    },
    async fetchProfile() {
      console.log(
        `fetchProfile() with backendUrl=${backendUrl}, and viteEnvironment=${viteEnvironment}`
      );
      this.profile = null;
      this.profileImage = null;

      const response = await fetch(backendUrl + "/profile/", {
        method: "GET",
        //mode: 'no-cors', // no-cors mode
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include", // This is important for handling cookies
      });
      if (response.ok) {
        console.log(
          `fetchProfile() response=${response}, response.ok=${response.ok}, viteEnvironment=${viteEnvironment}`
        );
        const data = await response.json();
        console.log(`fetchProfile() profile=${data}`);
        //this.profile = JSON.parse(data)[0].fields;
        this.profile = data;
        console.log(
          `fetchProfile() this.profile=${this.profile} skills=${this.profile.skills}`
        );
        this.loading = false;
        await this.getProfileImage();
        return true;
      }
      console.log(
        `fetchProfile() FAILED! with response.ok=false. response=${response}`
      );
      this.loading = false;
      return false;
    },
    async updateProfile(
      name,
      dob,
      university,
      graduationDate,
      gpa,
      resume,
      profileImage,
      skills
    ) {
      const formData = new FormData();
      formData.append("name", name);
      formData.append("dob", dob);
      formData.append("university", university);
      formData.append("graduationDate", graduationDate);
      formData.append("gpa", gpa);
      formData.append("resume", resume);
      formData.append("profileImage", profileImage);
      formData.append("skills", skills);

      console.log(
        `updateProfile(POST) calling BE with formData=${formData}, name=${name}, dob=${dob}, university=${university}, graduationDate=${graduationDate}, gpa=${gpa}, resume=${resume}, profileImage=${profileImage}, skills=${skills}`
      );

      const response = await fetch(backendUrl + "/profile/", {
        method: "POST",
        body: formData,
        credentials: "include", // This is important for handling cookies
      });
      if (response.ok) {
        console.log(
          `updateProfile(POST) response=${response}, response.ok=${response.ok}`
        );
        const data = await response.json();
        console.log(`updateProfile(POST) updating profile to =${data}`);
        this.profile = data;
        return true;
      } else {
        return false;
      }
    }, // updateProfile
    async fetchSkills() {
      this.skills = [];
      const response = await fetch(backendUrl + "/skills/", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include", // This is important for handling cookies
      });
      if (response.ok) {
        console.log(
          `fetchSkills() response=${response}, response.ok=${response.ok}`
        );
        const data = await response.json();
        console.log(`fetchSkills() skills=${data}`);
        this.skills = data;
        return true;
      }
      console.log(
        `fetchSkills() FAILED! with response.ok=false. response=${response}`
      );
      return false;
    }, // fetchSkills
    async fetchJobs(location, role) {
      this.jobs = [];
      console.log(`fetchJobs() location=${location} role=${role}`);
      const response = await fetch(
        backendUrl + `/search_jobs/${location}/${role}/`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include", // This is important for handling cookies
        }
      );
      if (response.ok) {
        console.log(
          `fetchJobs() response=${response}, response.ok=${response.ok}`
        );
        const data = await response.json();
        console.log(`fetchJobs() jobs=${data}`);
        this.jobs = JSON.parse(data);
        // sort jobs by match_score in descending order
        this.jobs.sort((a, b) => {
          if (a.match_score === null && b.match_score === null) {
            // return "0" to keep the order as is
            return 0;
          }
          if (a.match_score === null) {
            // a is less than b
            return 1;
          }
          if (b.match_score === null) {
            // a is greater than b
            return -1;
          }
          // sort by match_score in descending order
          return b.match_score - a.match_score;
        });
        return true;
      }
      console.log(
        `fetchJobs() FAILED! with response.ok=false. response=${response}`
      );
      return false;
    }, // fetchJobs
  }, // actions
}); // useRecruitStore
