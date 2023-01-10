<template>
  <div>
    <!-- 영화 정보는 중앙저장소에 있는 정보를 가져온다 -->

    <movie-detail-item :movie="movieList[movieId-1]" />
    <!-- <comment :movieId="movieId" :userId="userId"/> -->

  </div>
</template>

<script>
import MovieDetailItem from '@/components/movie/MovieDetailItem.vue'

export default {
  components: { MovieDetailItem },
    name:'MovieDetailView',
    computed:{
      movieList(){
        return this.$store.state.movieList
      },
      // userId(){
      //   return this.$store.state.userStore.userPk
      // }
    },
    data(){
      return{
        // route의 params는 str으로 들어오기 때문에 int로 변환
        movieId: parseInt(this.$route.params.movieid),
      }
    },
}
</script>

<style>

</style>