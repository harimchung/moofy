<template>
  <div class="recommendation--line">
    <div class="margin-by-fixed" style="position: relative">
      <h4>{{ userNickname }} 님의 친구들이 많이 보고있어요</h4>
      <div class="d-flex poster-container pe-2" id="age-movie-list">
        
        <div
          v-for="movieObject in ageRecommendList"
          :key="movieObject.id"
          class="col-12 col-sm-4 col-lg-3 col-xxl-2"
          id="recommendation--line--item"
        >
          <div @click="goDetail(movieObject.id)">
            <CBRecommendationItem :movieObject="movieObject" />
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
  name: "AgeRecommend",
  components: { CBRecommendationItem },
  props:{
    ageRecommendList:Array,
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
      const width = document.getElementById("age-movie-list").clientWidth;
      document.getElementById("age-movie-list").scrollLeft -= width;
    },
    scrollRight() {
      const width = document.getElementById("age-movie-list").clientWidth;
      document.getElementById("age-movie-list").scrollLeft += width;
    },
  },

};
</script>

<style></style>
