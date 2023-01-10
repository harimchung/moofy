<template>
  <div class="random__body">
    <div class="please__select__movie" > 좋아하는 영화를 선택해주세요. </div>
    <!-- <button @click="getMovie">random 영화 가져오기</button> -->
    <!-- 전체 card 담은 container -->
    <div class="row g-4 row-cols-1 row-cols-md-4  row-cols-sm-3  random-movie__list">
      <!-- card 각각 -->
      <div v-for="movie in randomList" :key="movie.id" class="col ">
        <movie-list-item :movie="movie" :index="movie.id" />
      </div>
    </div>
    <button @click="selectComplete" class="complete__button">선택완료</button>
  </div>
</template>

<script>
import _ from "lodash";
import MovieListItem from "@/components/movie/MovieListItem.vue";

const notification = document.getElementById('notification-container')
const showNotification = () => {
  notification.classList.add('show')
  setTimeout(() => {
    notification.classList.remove('show')
  }, 2000)
}

export default {
  name: "Random",
  components: {
    MovieListItem,
  },
  data() {
    return {
      randomList: [],
      selectedList: [],
      calculated_profile: [0, 0, 0, 0, 0, 0],
      watched_list: [],
      selectedGenre: [],
    };
  },
  computed: {
    movieList() {
      return this.$store.state.movieList;
    },
  },
  methods: {
    getMovie() {
      this.randomList = _.sampleSize(this.movieList, 12);
    },
    selectComplete() {

  

      const watchedList = Array(310).fill(0);
      const selectedGenre = Array(30).fill(0);
      const movie_list = document.querySelectorAll(".card-img-top");

      for (const movie of movie_list) {
        const movie_class_list = Array.from(movie.classList);

        
        if (movie_class_list.includes("isSelected") === true) {
          const selectedMovieId = Number(movie.getAttribute("id"));

          this.selectedList.push(this.movieList[selectedMovieId-1].profile);
          watchedList[this.movieList[selectedMovieId-1].id] += 1.5;

          selectedGenre[this.movieList[selectedMovieId-1].genre_ids] += 1.5
        }
      }

      if (this.selectedList.length < 1){
        alert("영화를 1개 이상 선택해주세요!")
        return
      }

      const weight = 1 / this.selectedList.length;
      for (const movie_profile of this.selectedList) {
        for (let i = 0; i < this.calculated_profile.length; i++) {
          this.calculated_profile[i] += movie_profile[i] * weight;
        }
      }
      this.watched_list = watchedList;
      // 중앙에 저장
      this.$store.dispatch("userStore/saveCalculation",{profile: this.calculated_profile, watched_list : this.watched_list, selectedGenre:selectedGenre});

      this.$store.dispatch("userStore/movieRecommend")
      this.$store.dispatch("userStore/movieRecommendGenre")
      this.$store.dispatch("userStore/movieRecommendBest")
    },
  },
  created(){
    showNotification
    this.getMovie()

  }
};
</script>

<style>
@import '@/assets/styles/Random/Random.css';
</style>
