import axios from "axios";

const state = () => {
  return {
    userPk: null,
    userNickname: null,
    userProfile: [],
    watchedList: [],
    seletedGenre: [],
    recommendationList: [],
    recommendationGenre: [],
    recommendationBest: [],
    isLoggedIn:false,
  };
};

const mutations = {
  GET_USER_PK: function (state, data) {
    state.userPk = data["id"];
    state.userNickname = data["nickname"];
    state.userProfile = data["profile"];
    state.watchedList = data["watched_list"];
    state.selectedGenre = data["selectedGenre"];

    
    state.isLoggedIn = true;

    
    this.dispatch("userStore/movieRecommend");
    this.dispatch("userStore/movieRecommendGenre");
    this.dispatch("userStore/movieRecommendBest");
  },
  SAVE_CALCULATION: function (state, payload) {
    state.userProfile = payload["profile"];
    state.watchedList = payload["watched_list"];
    state.selectedGenre = payload["selectedGenre"];
    this.dispatch("userStore/updateProfile");
  },
  UPDATE_WATCHED_LIST: function (state, updatedlist) {
    state.watchedList = updatedlist;
  },
  LOGOUT: function (state) {
    this.dispatch("userStore/updateProfile");

    (state.userPk = null), (state.userProfile = []), (state.watchedList = []);
    state.userNickname = null;
    state.selectedGenre = [];
    state.recommendationList = [];
    state.recommendationGenre = [];
    state.recommendationBest = [];
    state.isLoggedIn = false;
  },
  MOVIE_RECOMMEND: function (state, recommendationList) {
    
    state.recommendationList = recommendationList.slice(-10);
  },
  MOVIE_RECOMMEND_GENRE: function(state,recommendationList){

    state.recommendationGenre = recommendationList.slice(-10);
  
  },
  MOVIE_RECOMMEND_BEST: function(state,recommendationList){

    state.recommendationBest = recommendationList.slice(-10);
  },

  UPDATED_USER_PROFILE: function(state,updatedUserProfile){

    state.userProfile = updatedUserProfile
    this.dispatch("userStore/updateProfile"); //업데이트를 해줘야하나???
    this.dispatch("userStore/movieRecommend");
    //여기//
    this.dispatch("userStore/movieRecommendGenre");
    this.dispatch("userStore/movieRecommendBest");

  },
  CLICK_MOVIE : function(state, movie_id){

    const movieList = this.state.movieList

    const genre_id = Number(movieList[movie_id].genre_ids)

    state.selectedGenre[genre_id] += 1

    state.watchedList[movie_id] += 1

    this.dispatch("userStore/calculateUserProfile");
  },
  // CLICK_TRAILER : function(state,movie_id){

  //   state.watchedList[movie_id] += 1.5

  //   this.dispatch("userStore/calculateUserProfile");

  // },
  COMMENT_MOVIE: function(state,data){

    const movie_id = data.movieId
    const rating = data.rating

    if (rating >= 5 && rating <= 7) {

      state.watchedList[movie_id] += 1 //평범하게 관심있다

    } else if (rating >= 8){

      state.watchedList[movie_id] += 2 //매우 좋아한다
    }

    this.dispatch("userStore/calculateUserProfile");
  }
};

const actions = {
  getUserPk: function (context) {
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
        context.commit("GET_USER_PK", res.data);

      })
      .catch((err) => {
        console.log(err);
      });
  },
  saveCalculation: function (context, calculation) {
    context.commit("SAVE_CALCULATION", calculation);
  },
  updateProfile: function (context) {
    const userPk = context.state.userPk;
    const userProfile = context.state.userProfile;
    const watchedList = context.state.watchedList;
    const selectedGenre = context.state.selectedGenre;
    if (userPk != null)
    axios({
      method: "put",
      url: `http://127.0.0.1:8000/accounts/profile/${userPk}/`,
      data: {
        profile: userProfile,
        watched_list: watchedList,
        selectedGenre: selectedGenre,
      },
    })
      .then((res) => {
        //console.log(res);
      })
      .catch((err) => {
        console.log(err);
      });

  },

  logout: function (context) {
    context.commit("LOGOUT");
  },
  // 영화추천을 미리 계산

  movieRecommend: function (context) {

    // 내적을 수행하는 함수
    function innerProduct(list1, list2) {
      let innerProductSum = 0;
      let list1Norm = 0;
      let list2Norm = 0;
      for (let i = 0; i < list1.length; i++) {
        innerProductSum += list1[i] * list2[i];
        list1Norm += list1[i] ** 2
        list2Norm += list2[i] ** 2
      }
      list1Norm = Math.sqrt(list1Norm)
      list2Norm = Math.sqrt(list2Norm)

      return (innerProductSum)/(list1Norm * list2Norm);
    }

    //로그변환

    function logTransform(list) {

      const logList = list.map(function(e) {

        if (e > 1){ //1이면 0이 되니까.. 1보다 크면 로그변환
         return Math.log(e)
        } else {
          return e
        }
      })

      return logList

    }

    const innerProductResultList = [];
    const movieList = this.state.movieList;
    const logWatchedList = logTransform(context.state.watchedList)

    //최솟값을 찾는다

    let min_value = Infinity

    for(const like of logWatchedList) {
        if(min_value > like){
          min_value = like
        }
    }

    for (let i = 1; i < movieList.length; i++) {
        
        //일정 개수를 보장하기 위해 최솟값 보정
      if (logWatchedList[i] >= min_value && logWatchedList[i] <= min_value + 1) {
        // 내적 함수 만들기
        const innerProductResult = innerProduct(
          movieList[i].profile,
          context.state.userProfile
        );
        const notWatchedMovie = {
          movie: movieList[i],
          innerproduct: innerProductResult,
        };
        innerProductResultList.push(notWatchedMovie);
        
      }
    }
    // 내적 값을 기준으로 정렬하기
    innerProductResultList.sort(function (movie1, movie2) {
      return movie1.innerproduct - movie2.innerproduct;
    });

    context.commit("MOVIE_RECOMMEND", innerProductResultList);
  },

  //선택한 장르에 따른 영화 추천
  movieRecommendGenre(context) {

    // 내적을 수행하는 함수
    function innerProduct(list1, list2) {
      let innerProductSum = 0;
      let list1Norm = 0;
      let list2Norm = 0;
      for (let i = 0; i < list1.length; i++) {
        innerProductSum += list1[i] * list2[i];
        list1Norm += list1[i] ** 2
        list2Norm += list2[i] ** 2
      }
      list1Norm = Math.sqrt(list1Norm)
      list2Norm = Math.sqrt(list2Norm)
      

      return (innerProductSum)/(list1Norm * list2Norm);
    }

    //로그 변환을 하고 장르 id max값을 찾는다

    let max_genre_id = 0
    let max_value = 0

    for(let i = 0; i < 30; i++){

      if(context.state.selectedGenre[i] > 1){
      
        var value = Math.log(context.state.selectedGenre[i])

        if (value > max_value){
          max_value = value
          max_genre_id = i
        }

      }else {
        var value = context.state.selectedGenre[i]

        if (value > max_value){
          max_value = value
          max_genre_id = i
        }
      }
    }

    //max_genre_id에 해당하는 movie를 모두 가져온다

    const max_movie_list = []

    for(const movie of this.state.movieList){

      if(movie.genre_ids === max_genre_id){

        max_movie_list.push({'movie':movie, 'innerproduct': innerProduct(movie.profile,context.state.userProfile)})
      }
    }

    //innerproduct 순으로 정렬

    max_movie_list.sort(function(data1,data2){
      return data1.innerproduct - data2.innerproduct
    })

    context.commit('MOVIE_RECOMMEND_GENRE',max_movie_list)

  },
  //가장 관심있어한 영화와 비슷한 영화를 추천

  movieRecommendBest(context){

      // 내적을 수행하는 함수
      function innerProduct(list1, list2) {
        let innerProductSum = 0;
        let list1Norm = 0;
        let list2Norm = 0;
        for (let i = 0; i < list1.length; i++) {
          innerProductSum += list1[i] * list2[i];
          list1Norm += list1[i] ** 2
          list2Norm += list2[i] ** 2
        }
        list1Norm = Math.sqrt(list1Norm)
        list2Norm = Math.sqrt(list2Norm)
      
        return (innerProductSum)/(list1Norm * list2Norm);
      }

      //로그 변환을 하고 watchedlist의 max값의 id를 찾는다

      const movieList = this.state.movieList;
      const watchedList = context.state.watchedList;

      let max_watch_id = 0
      let max_value = 0
  
      for(let i = 1; i < watchedList.length; i++){
  
        if(watchedList[i] > 1){
        
          var value = Math.log(watchedList[i])
  
          if (value > max_value){
            max_value = value
            max_watch_id = i
          }
  
        }else {
          var value = watchedList[i]
  
          if (value > max_value){
            max_value = value
            max_watch_id = i
          }
        }
      }

    //max_watch_id가 아닌 다른 movie와의 내적을 모두 구한다

    const max_movie = movieList[max_watch_id]

    const max_movie_list = []

    for(const movie of movieList){

      if(movie.id !== max_watch_id){

        max_movie_list.push({'movie':movie, 'innerproduct': innerProduct(movie.profile,max_movie.profile)})
      }
    }

    //innerproduct 순으로 정렬

    max_movie_list.sort(function(data1,data2){
      return data1.innerproduct - data2.innerproduct
    })

    context.commit('MOVIE_RECOMMEND_BEST',max_movie_list)


  },
  
  //USER profile을 계산하는 액션
  calculateUserProfile(context) {

    const updatedUserProfile = Array(6).fill(0)

    //로그변환

    function logTransform(list) {

      const logList = list.map(function(e) {

        if (e > 1){ //1이면 0이 되니까.. 1보다 크면 로그변환
          return Math.log(e)
        } else {
          return e
        }
      })

      return logList

    }

    const logWatchedList = logTransform(context.state.watchedList)
    const movieList = this.state.movieList

    const sumWatchedList = logWatchedList.reduce(function(a,b){return a+b},0)
    const weight = 1/sumWatchedList

    for(let i = 1; i < movieList.length; i++){ //movie의 id와 리스트 인덱스는 다름 movieList[id-1]

      if(logWatchedList[i] != 0){
        
        for(let j=0; j<6; j++){
          updatedUserProfile[j] += (movieList[i].profile[j])*weight
        }
      }
    }

    context.commit("UPDATED_USER_PROFILE",updatedUserProfile)


  },

  // 영화 클릭(디테일로 이동시에 watchlist 갱신)
  clickMovie(context, movie_id){
    context.commit("CLICK_MOVIE", movie_id)
  },

  // 영화에 대한 코멘트 입력
  commentMovie(context, data){

    
    context.commit("COMMENT_MOVIE", data)
  },
  // clickTrailer(context,movie_id){
  //   context.commit('CLICK_TRAILER',movie_id)
  // }
};

const getters = {};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
