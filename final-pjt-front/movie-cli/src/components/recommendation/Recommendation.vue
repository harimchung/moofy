<template>
  <div class="p-sm-1 p-md-2 p-lg-3">
      <CBRecommendation :cblist="recommendationList" />
  </div>
</template>

<script>
import CBRecommendation from '../recommendation/CBRecommendation.vue'
export default {
  components: { CBRecommendation },
    name:'Recommendation',
    computed:{
      recommendationList(){
        return this.$store.state.userStore.recommendationList
      }
    },
}
</script>

<style>

</style>
