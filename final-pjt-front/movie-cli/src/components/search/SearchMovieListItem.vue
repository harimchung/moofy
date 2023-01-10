<template>
  <div>
    <div @click="goDetail(movie.id)">
  <main class="search">
    <div class="search-result">
      <div class="search-result__card">
        <div class="search-result__img">
          <img :src="`https://image.tmdb.org/t/p/w92${movie.poster_path}`">
        </div>
      <div class="search-result__text">
        <div class="search-text">{{movie.title}}</div>
        <div class="search-result__actor">
          <p>{{movie.actors}}</p>
        </div>
      </div>
      </div>
    </div>
  </main>
    </div>
  </div>
</template>

<script>
export default {
    name:'SearchMovieListItem',
    props:{
        movie:Object,
    },
    methods:{
        goDetail(id){
          // detail 페이지로 이동
          this.$router.push({name:'Detail', params: {movieid:id} })
          
          // watchedlist 갱신
          this.$store.dispatch('userStore/clickMovie', id)
        }
    }
}
</script>

<style scoped>

.search {
  padding: 0;
  margin: 0;
  box-sizing: border-box;
}

.search {
  width: 80%;
  min-width: 350px;
  max-width: 1000px;
  margin-left: auto;
  margin-right: auto;
}

.search-result__card {
  display : flex;
  padding: 12px;
  margin-bottom: 12px;
  border-radius: 12px;
  background-color: #F9FAFB;
}

/* .search-result__img{
  text-align: center;
} */

.search-result__text {
  display: flex;
  flex-direction: column;
  justify-content:center;
  margin: 0 auto;
}

.search-text{
  font-weight: 700;
  font-size: large;
}

.search-result__actor{
  padding-top : 20px;
}

/* .search-result__card {
  display: flex;
  padding: 12px;
  margin-bottom: 12px;
  border-radius: 12px;
  background-color: #F9FAFB;
} */

@media (max-width: 768px){

  .search {
  width: 70%;

}
.search-result__card {
/* display: flex; */
display: block;
}
.search-result__actor{
display: none;
}

.search-text{
  padding-top: 10px;
  font-weight: 600;
  font-size: 1.2rem;
}


}


.search-result__card:hover  {
  cursor: pointer;
  color: white;
  background-color: #D91E50; 
  transition: 0.5s;
}

.search-result__card > img {
  margin-right: 24px;
}


</style>