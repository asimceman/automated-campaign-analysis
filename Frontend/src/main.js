import App from "./App.vue";
import { createApp } from "vue";
import PrimeVue from "primevue/config";
import Aura from "@primeuix/themes/aura";
import Button from "primevue/button";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import InputText from "primevue/inputtext";
import Card from "primevue/card";
import Chart from "primevue/chart";
import "./assets/styles.css";

const app = createApp(App);
app.component("Button", Button);
app.component("DataTable", DataTable);
app.component("Column", Column);
app.component("InputText", InputText);
app.component("Card", Card);
app.component("Chart", Chart);
app.use(PrimeVue, {
  theme: {
    preset: Aura,
  },
});
app.mount("#app");
