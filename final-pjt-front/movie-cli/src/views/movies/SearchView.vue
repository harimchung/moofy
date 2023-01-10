<template>
  <div class="search--body">
    <h4> {{this.keyword}}(으)로 검색한 결과입니다.</h4>

    <div v-if="IsSearched" class="search-result">
        <search-movie-list :filtered-movie-list = "filteredMovieList"/>
    </div>

    <div v-else class="search-result">
        <h6>검색 결과가 없습니다.</h6>
    </div>

  </div>
</template>

<script>
import SearchMovieList from '@/components/search/SearchMovieList.vue'
export default {
  components: { SearchMovieList },
    name:'SearchView',
    data(){
        return{
            IsSearched : false,
            filteredMovieList : null,
            keyword : this.$route.params.keyword 
        }
    },
    computed:{
        movieList(){
            return this.$store.state.movieList
        },
        userProfile(){
            return this.$store.state.userStore.userProfile
        }
        // keyword(){
        //     return this.$route.params.keyword 
        // },
    },
    methods:{
           // 내적을 수행하는 함수
        innerProduct(list1, list2) {

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

        },

        searchMovie(){
            const keyword = this.keyword

            //제목이나 배우가 매칭되는 경우만 찾는다

            const filteredMovieList = this.movieList.filter((movie) => {

                //배우 문자열을 배우만 나오게 구분한다

                const actor_list = movie.actors.split(',')

                const real_actor_list = []

                for(const actor of actor_list){

                    const target_ind = actor.indexOf('(')

                    if (target_ind === -1){
                        real_actor_list.push(actor.trim())
                    } else {
                    real_actor_list.push(actor.slice(0,target_ind).trim())
                    }
                }

                const title = movie.title
                
                if(movie.title.includes(keyword) || real_actor_list.includes(keyword)){

                    return movie
                }
                })
            
            //userProfile이 존재한다면, cosine similarity를 구해서, 관련도가 높은 순서대로 출력할 수 있도록 한다

            if(this.userProfile.length >= 1){

            const bestFilteredMovieList = []

            for(const movie of filteredMovieList){

                const innerproduct = this.innerProduct(movie.profile, this.userProfile)

                bestFilteredMovieList.push({'movie':movie, 'innerproduct':innerproduct})
            }

            //innerproduct순으로 정렬

            bestFilteredMovieList.sort(function(movie1,movie2){

                return movie2.innerproduct-movie1.innerproduct
            })

            const filteredMovie = []

            for(const movieObject of bestFilteredMovieList){

                filteredMovie.push(movieObject.movie)
            
            }

            if (filteredMovie.length >= 1){
                this.IsSearched = true
                this.filteredMovieList = filteredMovie
        
            }} else{

                //userprofile이 존재하지 않는다면... 그냥 출력

                if (filteredMovieList.length >= 1){
                this.IsSearched = true
                this.filteredMovieList = filteredMovieList

            }

            
            }

        }
    },
    mounted() {
        this.searchMovie()
    },
    beforeRouteUpdate(to, from, next){
        this.filteredMovieList = null
        this.keyword = to.params.keyword
        this.IsSearched = false
        this.searchMovie()
        next()
    }
}
</script>

<style>
@import "@/assets/styles/Search.css";
</style>