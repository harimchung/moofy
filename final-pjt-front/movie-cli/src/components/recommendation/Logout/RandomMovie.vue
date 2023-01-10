<template>
  <div class="recommendation--line">
    <div class="margin-by-fixed" style="position: relative">
      <h4>회원 가입 후에 더 많은 추천을 받아보세요.</h4>
      <div class="d-flex poster-container pe-2" id="random--movie--box--1">
        
        <div
          v-for="movieObject in randomMovie1"
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
import CBRecommendationItem from "@/components/recommendation/CBRecommendationItem.vue";
export default {
    name : 'RandomMovie',
    components: { CBRecommendationItem },
    props:{
      randomMovie1:Array,
  },
  methods: {
    goDetail(id) {
      // detail 페이지로 이동
      this.$router.push({ name: "Detail", params: { movieid: id } });
      // watchedlist 갱신
      this.$store.dispatch("userStore/clickMovie", id);
    },
    scrollLeft() {
      const width = document.getElementById("random--movie--box--1").clientWidth;
      document.getElementById("random--movie--box--1").scrollLeft -= width;
    },
    scrollRight() {
      const width = document.getElementById("random--movie--box--1").clientWidth;
      document.getElementById("random--movie--box--1").scrollLeft += width;
    },
  },
}
</script>

<style>

</style>