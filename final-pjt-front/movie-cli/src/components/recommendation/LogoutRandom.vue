<template>
  <div class="p-sm-1 p-md-2 p-lg-3">
    <div class="cb-recommend-body">
      <random-movie :randomMovie1="randomMovie1" />
        <div>
        </div>
    </div>
  </div>
</template>

<script>
import RandomMovie from "@/components/recommendation/Logout/RandomMovie.vue";
import _ from 'lodash'
export default {
  components: { RandomMovie },
    name:'LogoutRandom',
    computed:{
      randomMovie1(){
        return _.sampleSize(this.$store.state.movieList, 10);
      },
      randomMovie2(){
        return _.sampleSize(this.$store.state.movieList, 10);
      }
    },
}
</script>

<style>
@import "@/assets/styles/Recommendation/RecommendItem.css";
</style>