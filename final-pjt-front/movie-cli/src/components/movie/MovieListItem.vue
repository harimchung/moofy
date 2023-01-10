<template>
  <div>
    <div
      class="col"
      @click="changeSelected"
    >
      <div class="card h-100 border-0">
        <img
          :id="index"
          :src="`https://image.tmdb.org/t/p/w600_and_h900_bestv2${movie.poster_path}`"
          class="card-img-top"
          :class="isSelected ? 'isSelected' : ''"
          alt="..."
        />
        <div class="card-body">
          <h5 class="movie__title">{{ movie.title }}</h5>
          <p class="card-text">
            
          </p>
        </div>


      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "MovieListItem",
  props: {
    movie: Object,
    index: Number,
  },
  data() {
    return {
      isSelected: false,
    };
  },
  methods: {
    changeSelected() {
      this.isSelected = !this.isSelected;
    },
  },
};
</script>

<style>
@import '@/assets/styles/Random/MovieListItem.css';

</style>
