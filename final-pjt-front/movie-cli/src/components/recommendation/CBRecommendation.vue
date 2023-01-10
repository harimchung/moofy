<template>
  <div class="cb-recommend-body">

      <!-- user 취향에 맞는 추천 -->
      <preference-recommend :cblist="cblist" />

      <!-- user 장르에 맞는 추천 -->
      <genre-recommend />

      <!-- 나이와 성별에 맞는 추천 -->
      <age-recommend :ageRecommendList="ageRecommendList"/>

      <!-- 시청기록에 기반한 추천 -->
      <best-recommend />

  </div>
</template>

<script>
import GenreRecommend from "./GenreRecommend.vue";
import PreferenceRecommend from "./PreferenceRecommend.vue";
import AgeRecommend from "./AgeRecommend.vue";
import BestRecommend from "./BestRecommend.vue";
import axios from 'axios'
import _ from "lodash"

export default {
  components: { PreferenceRecommend, GenreRecommend, AgeRecommend, BestRecommend },
  name: "CBRecommendation",
  props: {
    cblist: Array,
  },
  data() {
    return {
      ageRecommendList : null,
    };
  },
  computed: {
    userNickname() {
      return this.$store.state.userStore.userNickname;
    },
    recommendationGenre() {
      return this.$store.state.userStore.recommendationGenre;
    },
  },
  methods: {
    getUserInfo() {
      const token = localStorage.getItem("jwt");
      const config = {
        Authorization: `Bearer ${token}`,
      };
      axios({
        method: "get",
        url: "http://127.0.0.1:8000/accounts/profile/",
        headers: config,
      })
        .then((res) => {
          const sex = res.data.sex
          const age = res.data.age
          const lists = this.$store.state.ageLikeList

          // 성별, 나이 둘다 입력 안한 경우는 lodash로 랜덤으로 뽑는다.
          if (sex === null && age === null){
            const number = _.sample(_.range(10))
            this.ageRecommendList = lists[number]
          }
          // 성별만 입력한 경우
          else if (age === null){
            if(sex === "여자"){
              const number = _.sample(_.range(1, 10, 2))
              this.ageRecommendList = lists[number]
            } else{
              const number = _.sample(_.range(0, 10, 2))
              this.ageRecommendList = lists[number]
            }
          }
          // 나이만 입력한 경우
          else if (sex === null){
            if(age === "10대"){
              const number = _.sample([0, 1])
              this.ageRecommendList = lists[number]
            } else if(age === "20대"){
              const number = _.sample([2, 3])
              this.ageRecommendList = lists[number]
            } else if(age === "30대"){
              const number = _.sample([4, 5])
              this.ageRecommendList = lists[number]
            } else if(age === "40대"){
              const number = _.sample([6, 7])
              this.ageRecommendList = lists[number]
            } else if(age === "50대"){
              const number = _.sample([8, 9])
              this.ageRecommendList = lists[number]
            }
          }

          else{
            if(age === "10대"){
              if (sex === "남자"){
                this.ageRecommendList = lists[0]
              } this.ageRecommendList = lists[1]
            } else if(age ==="20대"){
              if (sex === "남자"){
                this.ageRecommendList = lists[2]
              } this.ageRecommendList = lists[3]
            } else if(age ==="30대"){
              if (sex === "남자"){
                this.ageRecommendList = lists[4]
              } this.ageRecommendList = lists[5]
            } else if(age ==="40대"){
              if (sex === "남자"){
                this.ageRecommendList = lists[6]
              } this.ageRecommendList = lists[7]
            } else if(age ==="50대"){
              if (sex === "남자"){
                this.ageRecommendList = lists[8]
              } this.ageRecommendList = lists[9]
            } 
          }


        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
  created(){
    this.getUserInfo()
  },

};
</script>

<style>
@import "@/assets/styles/Recommendation/RecommendItem.css";
</style>
