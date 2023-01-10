<template>
  <div>
    <h5 class="modal--text">회원가입</h5>

    <form class="row g-3 user--info--form" @submit.prevent>
      <!-- 아이디 -->
      <div>
        <input
          type="text"
          id="username"
          v-model="credentials.username"
          placeholder="아이디"
          class="form-control"
        />
        <div class="id input-danger" v-if="error_type === 0">
          <span>{{ error_message }}</span>
        </div>
        <div class="id input-danger" v-else-if="error_type === 2">
          <span>{{ error_message }}</span>
        </div>
        <div class="id input-danger" v-else-if="error_type === 5">
          <span>{{ error_message }}</span>
        </div>
      </div>


      <div>
        <input
          type="password"
          id="password"
          v-model="credentials.password"
          placeholder="비밀번호"
          class="form-control"
          :class="{ 'is-invalid' : passwordHasError }"
        />
        <div
          v-show="valid.password"
          class="input-danger valid-form">
          대문자, 특수문자, 숫자를 포함해야 합니다.
        </div>

      </div>
      <div>
        <input
          v-model="credentials.passwordConfirm"
          @keyup.enter="signup"
          type="password"
          id="passwordConfirmation"
          placeholder="비밀번호 확인"
          class="form-control"
          :class="{ 'is-invalid ' : passwordConfirmHasError }"
        />
        <div
        v-show="valid.passwordConfirm"
        class="input-danger valid-form">
          비밀번호가 일치하지 않습니다.
        </div>

      </div>
      <div>

        <input
          type="nickname"
          id="nickname"
          v-model="credentials.nickname"
          placeholder="닉네임"
          class="form-control"
          :class="{ 'is-invalid ' : nicknameHasError }"
        />
        <div
        v-show="valid.nickname"
        class="input-danger valid-form">
          2글자 이상의 닉네임을 입력하세요.
        </div>

      </div>

      <!--  옵션으로 받는 구역 -->
      <hr>
      <h5 class="modal--text">옵션</h5>
      <!-- 나이 -->
      <div class="col form-floating">
        <select name="age" id="age" v-model="credentials.age" class="form-select" >
          <!-- <option selected> 나이 </option> -->
          <option :value="age" v-for="(age, idx) in this.ages" :key="idx">
            {{ age }}
          </option>
        </select>
        <label for="age">나이</label>
      </div>


      <div class="col form-floating">
        <select name="sex" id="sex" v-model="credentials.sex" class="form-select">
          <option :value="sex" v-for="(sex, idx) in this.sex" :key="idx">
            {{ sex }}
          </option>
        </select>
        <label for="sex">성별</label>
      </div>
      
      <div>
        <!-- <label for="eamil">이메일 : </label> -->
        <input type="email" id="eamil" v-model="credentials.email" class="form-control" placeholder="이메일"/>
      </div>

      <div class="row button--box" > 
        <button @click="signup" class="form--button">회원가입</button>
      </div>
    </form>

  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "SignupView",
  data: function () {
    return {
      ages: ["10대", "20대", "30대", "40대", "50대"],
      sex: ["남자", "여자"],
      credentials: {
        username: null,
        password: null,
        passwordConfirm: null,
        nickname: null,
        age: null,
        sex: null,
        email: null,
      },
      error_type: null, //0: 아이디 입력, 1: 비밀번호 입력, 2: 올바른 아이디 입력
      error_message: null,
      valid: {
        password : false,
        passwordConfirm : false,
        nickname : false,
      },
      passwordHasError : false,
      passwordConfirmHasError : false,
      nicknameHasError : false,
    };
  },
  watch:{
    'credentials.password' : function() {
      this.checkPassword()
    },
    'credentials.passwordConfirm' : function() {
      this.checkPasswordConfirm(this.credentials.password, this.credentials.passwordConfirm)
    },
    'credentials.nickname' : function() {
      this.checkNicknameConfirm(this.credentials.nickname)
    },
  },
  methods: {
    checkPassword() {
      // 비밀번호 형식 검사(영문, 숫자, 특수문자)
      const validatePassword = /^(?=.*[a-zA-z])(?=.*[0-9])(?=.*[$`~!@$!%*#^?&\\(\\)\-_=+]).{8,16}$/

      if (!validatePassword.test(this.credentials.password) || !this.credentials.password ){
        this.valid.password = true
        this.passwordHasError = true
        return
      } this.valid.password = false
        this.passwordHasError = false
    },
    checkPasswordConfirm(password, confirm){
      if (password != confirm){
        this.valid.passwordConfirm = true
        this.passwordConfirmHasError = true
        return
      } 
        this.valid.passwordConfirm = false
        this.passwordConfirmHasError = false
    },
    checkNicknameConfirm(nickname){
      if(nickname.length < 2){
        this.valid.nickname = true
        this.nicknameHasError = true
        return
      } this.valid.nickname = false
        this.nicknameHasError = false
    },
    modalClose: function () {
      this.$emit("modal-close");
    },
    signup: function () {
      axios({
        method: "post",
        url: "http://127.0.0.1:8000/accounts/signup/",
        data: this.credentials,
      })
        .then(() => {
          alert("회원가입 성공!");
          this.modalClose();
        })
        .catch((err) => {
          //올바른 정보를 입력하도록 에러 처리

          console.log(err.response.data);

          for (const [key, value] of Object.entries(err.response.data)) {
            if (key === "error") {
              this.error_type = value[0];

              this.error_message = value[1];
            } else {
              if (value[0].slice(-7) === "exists.") {

                if (key === "username") {
                  this.error_type = 5;
                  this.error_message = "이미 존재하는 아이디입니다.";
                }
              }  else {
                //예상할 수 없는 에러
                alert("올바르게 정보를 입력하세요!");
                break;
              }
            }
          }
        });
    },
  },
};
</script>

<style>

</style>