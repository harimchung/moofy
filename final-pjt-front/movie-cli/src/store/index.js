import Vue from "vue";
import Vuex from "vuex";
import userStore from "./modules/userStore.js";
import createPersistedState from "vuex-persistedstate";
import _ from "lodash";

Vue.use(Vuex);


export default new Vuex.Store({
  state: {
    movieList: [],
    ageLikeList: [],
    LogoutList: [],

  },
  getters: {},
  mutations: {
    LOAD_MOVIE(state, movieList) {
      state.movieList = movieList;
    },

    LOAD_AGE_MOVIE(state,ageList) {
      state.ageLikeList = ageList;
    },

    LOAD_LOGOUT_MOVIE(state,LogoutList){
      state.LogoutList = LogoutList
    }
  },
  actions: {

    calculateLogout(context) {

      context.commit('LOAD_LOGOUT_MOVIE',_.sampleSize(context.state.movieList,12))
    
    },

    calculateAge(context) {

      const ageList = []
      
      const movieList = _.cloneDeep(context.state.movieList)

      // 10대 남자 기준으로 정렬

      movieList.sort(function(movie1,movie2){

        if (movie2.vote_10 === movie1.vote_10){
          return movie2.man_vote - movie1.man_vote;
        } else {
        return movie2.vote_10 - movie1.vote_10;
        }
      
      })

      ageList.push(_.sampleSize(movieList.slice(0,20),10))

      //10대 여자 기준으로 정렬

      movieList.sort(function(movie1,movie2){

        if (movie2.vote_10 === movie1.vote_10){
          return movie2.woman_vote - movie1.woman_vote;
        } else {
        return movie2.vote_10 - movie1.vote_10;
        }
      
      })

      ageList.push(_.sampleSize(movieList.slice(0,20),10))



      //20대 남자 기준으로 정렬

      movieList.sort(function(movie1,movie2){

        if (movie2.vote_20 === movie1.vote_20){
          return movie2.man_vote - movie1.man_vote;
        } else {  
        return movie2.vote_20 - movie1.vote_20;
        }
      })

      ageList.push(_.sampleSize(movieList.slice(0,20),10))

      //20대 여자 기준으로 정렬

      movieList.sort(function(movie1,movie2){

        if (movie2.vote_20 === movie1.vote_20){
          return movie2.woman_vote - movie1.woman_vote;
        } else {  
        return movie2.vote_20 - movie1.vote_20;
        }
      })

      ageList.push(_.sampleSize(movieList.slice(0,20),10))

      //30대 남자 기준으로 정렬

      movieList.sort(function(movie1,movie2){
        
        if (movie2.vote_30 === movie1.vote_30){
          return movie2.man_vote - movie1.man_vote;
        } else {
  
        return movie2.vote_30 - movie1.vote_30;
        }      
      })

      ageList.push(_.sampleSize(movieList.slice(0,20),10))

      //30대 여자 기준으로 정렬

      movieList.sort(function(movie1,movie2){
        
        if (movie2.vote_30 === movie1.vote_30){
          return movie2.woman_vote - movie1.woman_vote;
        } else {
  
        return movie2.vote_30 - movie1.vote_30;
        }      
      })

      ageList.push(_.sampleSize(movieList.slice(0,20),10))

      //40대 남자 기준으로 정렬

      movieList.sort(function(movie1,movie2){
        
        if (movie2.vote_40 === movie1.vote_40){
          return movie2.man_vote - movie1.man_vote;
        } else {
  
        return movie2.vote_40 - movie1.vote_40;
        }      
      })

      ageList.push(_.sampleSize(movieList.slice(0,20),10))

      //40대 여자 기준으로 정렬

      movieList.sort(function(movie1,movie2){
        
        if (movie2.vote_40 === movie1.vote_40){
          return movie2.woman_vote - movie1.woman_vote;
        } else {
  
        return movie2.vote_40 - movie1.vote_40;
        }      
      })

      ageList.push(_.sampleSize(movieList.slice(0,20),10))

      //50대 남자 기준으로 정렬

      movieList.sort(function(movie1,movie2){
        
        if (movie2.vote_50 === movie1.vote_50){
          return movie2.man_vote - movie1.man_vote;
        } else {
  
        return movie2.vote_50 - movie1.vote_50;
        }      
      })

      ageList.push(_.sampleSize(movieList.slice(0,20),10))

      //50대 여자 기준으로 정렬

      movieList.sort(function(movie1,movie2){
        
        if (movie2.vote_50 === movie1.vote_50){
          return movie2.woman_vote - movie1.woman_vote;
        } else {
  
        return movie2.vote_50 - movie1.vote_50;
        }      
      })

      ageList.push(_.sampleSize(movieList.slice(0,20),10))

      context.commit('LOAD_AGE_MOVIE',ageList)

    }


  },
  modules: {
    userStore,
  },
  plugins: [
    createPersistedState(),
  ],
});
