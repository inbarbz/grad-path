import { createRouter, createWebHistory } from "vue-router";
import Page1 from "../views/Page1.vue";
//import LandingPage from "../views/LandingPage.vue";
import { useRecruitStore } from "../stores/recruit";
import ContactView from "../views/ContactView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.VITE_BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: Page1,
      meta: {
        title: "Home",
      },
    },
    {
      path: "/contactus",
      name: "Contact Us",
      component: ContactView,
      meta: {
        title: "Contact Us",
      },
    },
    {
      path: "/about",
      name: "about",
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import("../views/AboutView.vue"),
      meta: {
        title: "About",
      },
    },
    {
      path: "/login",
      name: "login",
      //component: LoginPage
      component: () => import("../views/LoginPage.vue"),
      meta: {
        title: "Login/Signup",
      },
    },
    {
      path: "/profile",
      name: "profile",
      //component: ProfilePage
      component: () => import("../views/ProfilePage.vue"),
      meta: {
        title: "Profile",
      },
    },
    {
      path: "/landing",
      name: "landing",
      //component: LandingPage
      component: () => import("../views/LandingPage.vue"),
      meta: {
        title: "Landing",
      },
    },
    {
      path: "/help",
      name: "help",
      //component: HelpPage
      component: () => import("../views/HelpPage.vue"),
      meta: {
        title: "Help",
      },
    },

  ],
});

var didOnce = false;
router.beforeEach(async (to, from, next) => {
  const store = useRecruitStore();
  if (!didOnce && (store.isLoading || !(await store.isLoggedIn))) {
    console.log(
      `router.beforeEach() isLoading=${store.isLoading} isLoggedIn=${store.isLoggedIn}, from=${from.path}, to=${to.path} REDIRECT TO LOGIN`
    );
    console.log("Router index.js Base URL:", import.meta.env.VITE_BASE_URL);
    didOnce = true;
    next("/login");
  } else {
    next();
  }
});

export default router;
