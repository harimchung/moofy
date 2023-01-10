<template>
  <div class="movie__detail">
    <!-- back drop path 영화 -->
    <div class="movie__banner">
      <img :src="getImageUrl(movie.backdrop_path)"
      />
      <!-- :src="getImageUrl(movie.backdrop_path)" -->
      <!-- :src="`https://image.tmdb.org/t/p/original${movie.backdrop_path}`" -->
      <!-- @error="setAltImage" -->
    </div>

    <!-- 영화의 상세정보 적을 곳 -->
    <div class="container movie__detail__body">
      <div class="row movie__head">
        <div class="col-sm-4 col-md-3">
          <div class="movie__poster">
            <img
              :src="`https://image.tmdb.org/t/p/w600_and_h900_bestv2${movie.poster_path}`"
              class=""
              alt="..."
            />
          </div>
        </div>
        <div class="col-sm-8 col-md-9">
          <h5 class="movie__title">{{ movie.title }}</h5>
          <div class="movie__info">
            <div class="movie__info_line1">
              <p>{{ movie.release_date.slice(0, 4) }} ·</p>
              <p>{{ movie.nation }} ·</p>
              <p>{{ movie.genres[0] }}</p>
            </div>
            <div class="movie__info_line2">
              <p>{{ movieGrade }}</p>
              <p style="padding-left:5px; padding-right: 5px">|</p>
              <p>{{ movie.running_time }}분</p>
            </div>
            <div class="movie__info_line3">
              <p>캐스팅 : {{ movie.actors }}</p>
            </div>
            <div class="movie__info_line4">
              <font-awesome-icon
              icon="fa-solid fa-star fa-sm"
              style="color: #262626"
            />
              <p>{{ movie.actual_vote_average }}</p>
            </div>

          </div>

          <!-- 차트 영역 -->
          <div class="movie__chart">
            <div class="bar__chart">
              <apexchart
                type="bar"
                :options="chartOptions"
                :series="barseries"
              ></apexchart>
            </div>

            <div class="pie__chart">
              <apexchart
                type="pie"
                :options="pieOptions"
                :series="pieseries"
              ></apexchart>
            </div>
          </div>
        </div>
      </div>

      <div class="movie__overview">
        <!-- overview가 담길 곳 -->
        <div class="row">
          <div class="col-md-7">
            <p class="movie__overview__explain">
              {{ movie.overview }}
            </p>
          </div>
          <div class="col-md-5 movie__video">
            <iframe style="width:100%;aspect-ratio: 16/9;"
             :src="movie.video_url" title="YouTube video player"></iframe>
          </div>

        </div>
        <div class="row comment__box">
          <hr>

          <comment :movieId="movieId" :userId="userId" />
        </div>
      </div>


    </div>
  </div>
</template>


<script>
import Comment from "@/components/comment/Comment.vue";

export default {
  components: { Comment },
  name: "MovieDetailItem",
  props: {
    movie: Object,
  },
  methods: {
    // watchTrailer() {

    // // const iframe = document.querySelector('iframe')

    // // iframe.contentWindow.postMessage('click', 'http://localhost:8080/' )

    // // window.addEventListener('message',function(event){

    // //   if (event.origin === 'http://localhost:8080/'){

    // //   }
    // // })
    
    // // watchedlist 갱신
    // this.$store.dispatch('userStore/clickTrailer')
    // },
    getImageUrl(url){
      if(url==null){
        return require(`@/assets/films.jpg`)
      }
      else{
        return (`https://image.tmdb.org/t/p/original${url}`)
      }
    },
    getGrade(){
      const grade = this.movie.grade
      if (grade === 0){
        this.movieGrade = "전체 관람가"
      } else if (grade === 1){
        this.movieGrade = "12세 관람가"
      } else if (grade === 2){
        this.movieGrade = "15세 관람가"
      } else if (grade === 3){
        this.movieGrade = "청소년 관람 불가"
      } else if (grade === 4){
        this.movieGrade = "제한상영가"
      } else{
        this.movieGrade = "등급보류"
      }
    }
  },
  data() {
    return {
      // route의 params는 str으로 들어오기 때문에 int로 변환
      movieId: parseInt(this.$route.params.movieid),
      movieGrade: null,
      chartOptions: {
        chart: {
          id: "age-preference",
        },
        xaxis: {
          categories: ["10대", "20대", "30대", "40대", "50대"],
        },
        grid: {
          show: false,
        },
        yaxis: {
          show: false,
        },
        colors: ["#D91E50", "#D91E50", "#D91E50", "#D91E50", "#D91E50"],
        bar: {
          columnWidth: "50%",
        },
      },
      barseries: [
        {
          name: "age-preference",
          data: [
            this.movie.vote_10,
            this.movie.vote_20,
            this.movie.vote_30,
            this.movie.vote_40,
            this.movie.vote_50,
          ],
        },
      ],

      pieOptions: {
        chart: {
          id: "sex-preference",
          type: "pie",
        },

        colors: ["#2968DB", "#D91E50"],
        pie: {
          startAngle: 0,
          endAngle: 0,
        },

        labels: ["남", "여"],
      },
      pieseries: [this.movie.man_vote, this.movie.woman_vote],
    };
  },
  computed: {
    userId() {
      return this.$store.state.userStore.userPk;
    },
  },
  created(){
    this.getGrade()
  }
};
</script>

<style>
@import "@/assets/styles/Movie/detail.css";
.apexcharts-toolbar{
  display : none !important;
}
</style>
