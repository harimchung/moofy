<template>
  <div class="comment--update--form">
    
    <div class="row" style="padding-top:10px; padding-left:20px; padding-bottom:15px;">
            <div class="col col-md-11">
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
              <button class="comment__button" @click="toggle">수정완료</button>
            </div>
          </div>
        </div>


  </div>
</template>

<script>
export default {
  name: "CommentItemUpdate",
  methods: {
    toggle() {
      this.$emit("toggle-div", { rating: this.rating, content: this.content });
    },
  },
  props: {
    comment: Object,
  },
  data() {
    return {
      rating: this.comment.rating,
      content: this.comment.content,
    };
  },
};
</script>

<style>
@import "@/assets/styles/Comment/Comment.css";
</style>
