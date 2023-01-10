<template>
  <div class="recommendation--line">
    <div class="margin-by-fixed" style="position: relative">
      <h4>{{ userNickname }} 님이 좋아하는 장르</h4>
      <div class="d-flex poster-container pe-2" id="genre-playlist-box">
        <div
          v-for="movieObject in recommendationGenre"
          :key="movieObject.movie.id"
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
  name: "GenreRecommend",
  computed: {
    userNickname() {
      return this.$store.state.userStore.userNickname;
    },
    recommendationGenre(){
      return this.$store.state.userStore.recommendationGenre
    }
  },
  methods: {
    goDetail(id) {
      // detail 페이지로 이동
      this.$router.push({ name: "Detail", params: { movieid: id } });
      // watchedlist 갱신
      this.$store.dispatch("userStore/clickMovie", id);
    },
    scrollLeft() {
      const width = document.getElementById("genre-playlist-box").clientWidth;
      document.getElementById("genre-playlist-box").scrollLeft -= width;
    },
    scrollRight() {
      const width = document.getElementById("genre-playlist-box").clientWidth;
      document.getElementById("genre-playlist-box").scrollLeft += width;
    },
  },
};
</script>

<style></style>
