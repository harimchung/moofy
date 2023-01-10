<template>
  <div>
    <div style="display:flex;">
      <h5 style="margin-right: 0.4em;">코멘트</h5>
      <h5 style="color:#bfbfbf">{{comments_count}}</h5>
    </div>
    <div class="star--box">
      <star-rating 
        :increment="0.1"
        v-model="halfRating"
        :rounded-corners="true"
        :star-size="38"
        :read-only="true"
        :show-rating="false"
        ></star-rating>
        <div>
          <div style="margin-top: 0.1rem; font-weight: 300; font-size:large; margin-left:15px;"
          > {{average_rating}}</div>
        </div>
    </div>

    <div class="container">
    <form @submit.prevent="createComment" class="form-floating">
          <div class="row" style="padding-top:30px; padding-left:0px; padding-bottom:10px;">
            <div class="col col-md-7">
              <!-- 평점 -->
              <div style="margin-bottom:10px">
                <label for="rating">평점</label>
                <input type="number" class="form-control" id="rating" min="1" max="10" v-model="rating">
              </div>

              <!-- 내용 -->
              <div class="form-floating" style="margin-bottom: 10px;">
                <textarea class="form-control" placeholder="댓글을 남겨주세요" id="content" style="height: 100px" v-model="content"></textarea>
                <label for="content">내용을 입력해주세요.</label>
            </div>

            <!-- 작성하기 -->
            <div style="display:flex; justify-content:flex-end">
              <button class="comment__button">작성하기</button>
            </div>
          </div>
        </div>
      </form>

      <div class="row" style="padding-top:30px; padding-left:0px; padding-bottom:10px;">
        <div v-for="comment in comments" :key="comment.id" >
            <comment-item :comment="comment" @delete-comment="getComment" @update-comment="getComment"/>
        </div>
      </div>
    </div>



  </div>
</template>

<script>
import axios from 'axios'
import CommentItem from '../comment/CommentItem.vue'
import StarRating from 'vue-star-rating'

export default {
    components: { CommentItem, StarRating },
    name:'Comment',
    data(){
      return{
        rating : null,
        content: null,
        comments : null,
        comments_count : null,
        average_rating : null,
      }
    },
    props:{
      movieId:Number,
      userId:Number,
    },
    methods: {
      getComment(){
            axios({
                method:'get',
                url:`http://127.0.0.1:8000/movies/${this.movieId}/`
            }).then(res=>{
                this.comments = res.data.comment_set
                this.comments_count = res.data.comments_count

                let ratingSum = 0
                for(const comment of this.comments){
                  ratingSum += comment.rating
                }
                if (this.comments_count === 0){
                  this.average_rating = 0
                } else{
                  this.average_rating = (ratingSum / this.comments_count).toFixed(2)
                }
            }).catch(err=>{
                console.log(err)
            })
        },
      createComment(){
        const content = this.content
        const rating = this.rating
        if(!content){
          alert("내용을 입력해주세요")
          return
        } else if (!rating){
          alert("평점을 입력해주세요")
          return
        }
        axios({
          method : 'post',
          url : `http://127.0.0.1:8000/movies/${this.movieId}/`,
          data: {content:content, rating:rating, movie:this.movieId, user:this.userId,}
        }).then(() => {


          //comment 입력에 대한 watchedlist 개선
          this.$store.dispatch("userStore/commentMovie",{movieId:this.movieId, rating:Number(this.rating)})
          
          this.rating = null,
          this.content = null,
          this.getComment()


        }).catch(err => {
          console.log(err)
        })
      }
    },
  created(){
    this.getComment()
  },
  computed:{
    halfRating(){
      return (this.average_rating)/2
    }

  }

}
</script>

<style>
@import "@/assets/styles/Comment/Comment.css";
</style>