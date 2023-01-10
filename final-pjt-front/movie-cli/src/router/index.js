import Vue from "vue";
import VueRouter from "vue-router";
import MainView from "../views/movies/MainView";
import MovieDetailView from "@/views/movies/MovieDetailView";
import SearchView from "@/views/movies/SearchView";
import NotFound404 from "@/views/error/NotFound404";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Main",
    component: MainView,
  },
  // search로 이동하는 router-link
  {
    path: "/search/:keyword",
    name: "Search",
    component: SearchView,
  },
  // movie detail로 이동하는 router-link
  {
    path: "/movie/:movieid",
    name: "Detail",
    component: MovieDetailView,
    meta: {
      whiteMode: true,
    },
  },
  //404 not found
  {
    path: "/404",
    name: "NotFound404",
    component: NotFound404,
  },
  //반드시 최하단부에 작성해야함
  {
    path: "*",
    redirect: "/404",
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
  scrollBehavior(to, from, savedPosition) {
    return { x: 0, y: 0 };
  },
});

router.beforeEach((to, from, next) => {
  const movieDataNumber = 302;
  const params = to.params.movieid;
 
  let token = localStorage.getItem("jwt")

  if (to.name == "Detail" & !token){
    return
  }

  else if (to.name == "Detail" && params > movieDataNumber) {
    next({ name: "NotFound404" });
  }
  next();
});

export default router;
