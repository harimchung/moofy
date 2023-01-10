<template>
  <div class="col col-md-7 comment--list--item">

    <!-- 작성자 -->
    <p style="font-weight:600;">{{ comment.nickname }}</p>
    <!-- 별 아이콘, 별점 -->
    <div style="display: flex; align-items: center">
      <font-awesome-icon icon="fa-solid fa-star fa-sm" style="color: #ffd055" />
      <p class="comment--rating">{{ comment.rating }}</p>
    </div>
    <p>{{ comment.content }}</p>
    <div
      v-if="comment.user === this.$store.state.userStore.userPk"
      class="update__delete__box"
    >
      <button @click="toggle" class="update__button">수정</button>
      <button @click="deleteComment" class="delete__button">삭제</button>
    </div>
    <div v-if="editmode">
      <comment-item-update @toggle-div="commentUpdate" :comment="comment" />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import CommentItemUpdate from "../comment/CommentItemUpdate.vue";
export default {
  components: { CommentItemUpdate },
  name: "CommentItem",
  data() {
    return {
      editmode: false,
    };
  },
  props: {
    comment: Object,
  },

  methods: {
    deleteComment() {
      axios({
        method: "delete",
        url: `http://127.0.0.1:8000/movies/comment/${this.comment.id}/`,
      })
        .then((res) => {
          this.$emit("delete-comment");
        })
        .catch((err) => {
          console.log(err);
        });
    },
    toggle() {
      this.editmode = !this.editmode;
    },
    commentUpdate(payload) {
      this.toggle();
      axios({
        method: "put",
        url: `http://127.0.0.1:8000/movies/comment/${this.comment.id}/`,
        data: {
          movie: this.comment.movie,
          user: this.comment.user,
          content: payload["content"],
          rating: payload["rating"],
          // nickname : this.comment.nickname
        },
      })
        .then((res) => {
          this.$emit("update-comment");
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

<style>
@import "@/assets/styles/Comment/Comment.css";
</style>
