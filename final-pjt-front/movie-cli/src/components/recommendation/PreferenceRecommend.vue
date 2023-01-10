<template>
  <div class="recommendation--line">
    <div class="margin-by-fixed" style="position: relative">
      <h4>{{ userNickname }} 님을 위한 추천</h4>
      <div class="d-flex poster-container pe-2" id="now-playlist-box">
        <div
          v-for="movieObject in cblist"
          :key="movieObject.id"
          class="col-12 col-sm-4 col-lg-3 col-xxl-2"
          id="recommendation--line--item"
        >
          <div @click="goDetail(movieObject.movie.id)">
            <CBRecommendationItem :movieObject="movieObject.movie" />
          </div>
        </div>
      </div>
      <font-awesome-icon
        icon="fa-solid fa-chevron-left"
        class="fa-2x arrow-left cursor-pointer"
        @click="scrollLeft"
      />
      <font-awesome-icon
        icon="fa-solid fa-chevron-right"
        class="fa-2x arrow-right cursor-pointer"
        @click="scrollRight"
      />
    </div>
  </div>
</template>

<script>
import CBRecommendationItem from "../recommendation/CBRecommendationItem.vue";
export default {
  components: { CBRecommendationItem },
  name: "PreferenceRecommend",
  props:{
    cblist : Array,
  },
  computed: {
    userNickname() {
      return this.$store.state.userStore.userNickname;
    },
  },
  methods: {
    goDetail(id) {
      // detail 페이지로 이동
      this.$router.push({ name: "Detail", params: { movieid: id } });
      // watchedlist 갱신
      this.$store.dispatch("userStore/clickMovie", id);
    },
    scrollLeft() {
      const width = document.getElementById("now-playlist-box").clientWidth;
      document.getElementById("now-playlist-box").scrollLeft -= width;
    },
    scrollRight() {
      const width = document.getElementById("now-playlist-box").clientWidth;
      document.getElementById("now-playlist-box").scrollLeft += width;
    },
  },
};
</script>

<style>
</style>
