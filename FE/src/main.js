//select a theme
import "primeflex/primeflex.css";
import "primevue/resources/themes/lara-light-green/theme.css";
import "primevue/resources/primevue.min.css"; /* Deprecated */
import "primeicons/primeicons.css";

//import './assets/main.css'

import { createApp } from "vue";
import { createPinia } from "pinia";
import VueGtag from "vue-gtag";
import PrimeVue from "primevue/config";

import App from "./App.vue";
import router from "./router";

const app = createApp(App);

app.use(createPinia());
app.use(router);
app.use(PrimeVue).use(VueGtag, {
  config: { id: "G-7TCKHSFMC2" },
});

app.mount("#app");

router.afterEach((to) => {
  document.title = to.meta.title || "Default Page";

  app.config.globalProperties.$gtag.pageview({
    page_title: to.meta.title,
    page_path: to.path,
  });
});
