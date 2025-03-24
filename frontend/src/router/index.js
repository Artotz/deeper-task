import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import UserView from "@/views/UserView.vue";
import NotFoundView from "@/views/NotFoundView.vue";

const routes = [
  { path: "/", component: HomeView },
  { path: "/user/:username", component: UserView },
  { path: "/:pathMatch(.*)*", component: NotFoundView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
