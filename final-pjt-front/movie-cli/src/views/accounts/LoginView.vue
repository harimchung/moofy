<template>
  <div>
    <h5 class="modal--text">로그인</h5>
    <form class="row g-3 user--info--form" @submit.prevent>
      <div>
        <!-- <label for="username">사용자 이름: </label> -->
        <input type="text" id="username" v-model="credentials.username" class="form-control" placeholder="아이디"/>
      </div>
      <div>
        <!-- <label for="password">비밀번호: </label> -->
        <input
          type="password"
          id="password"
          v-model="credentials.password"
          @keyup.enter="login"
          class="form-control"
          placeholder="비밀번호"
        />
      </div>
      <div class="error input-danger valid-form"><span>{{ error_message }}</span></div>

      <div class="row button--box" > 
        <button @click="login" class="form--button">로그인</button>
      </div>

    </form>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    name: "LoginView",
    data: function() {
      return {
        error_message: null,
        credentials: {
          username: null,
          password: null,
        },
      };
    },
    methods: {
      modalClose: function() {
      this.$emit('modal-close')
      },
      login: function() {
        axios({
          method: "post",
          url: "http://127.0.0.1:8000/api/token/",
          data: this.credentials,
        })
          .then((res) => {
            localStorage.setItem("jwt", res.data.access);
            this.$emit("login");
            this.modalClose();
            // this.$router.push({ name: "Main" });
          })
          .catch((err) => {
            
            this.error_message = "일치하는 정보가 없습니다."
          });
      },
    },
  };
  </script>
  