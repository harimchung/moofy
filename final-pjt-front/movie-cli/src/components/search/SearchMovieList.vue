<template>
  <div>
    <div v-for="movie in filteredMovieList" :key="movie.id">
        <search-movie-list-item :movie="movie" />
    </div>

  </div>
</template>

<script>
import SearchMovieListItem from '../search/SearchMovieListItem.vue'
export default {
  components: { SearchMovieListItem },
    name : 'SearchMovieList',
    props: {
        filteredMovieList: Array,
    }
}
</script>

<style>

</style>