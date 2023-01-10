<template>
  <div>
    <h5 class="modal--text">회원정보 수정</h5>
    <div v-if="isAuthenticated === false">
      <p>비밀번호를 입력해주세요.</p>

      <label for="authenticated_password">비밀번호: </label>
      <div style="width: 80%">
        <div>
          <input
            type="password"
            id="authenticated_password"
            v-model="authenticated_password"
            class="password--input--form form-control"
          />
        </div>
        <div class="id input-danger" v-if="error_type === 3">
          <span>{{ error_message }}</span>
        </div>

        <div style="display: flex; justify-content: flex-end">
          <button @click="checkUser" class="checkUser--button">
            회원정보 수정
          </button>
        </div>
        
      </div>
    </div>

    <!-- 인증완료 된 경우 -->
    <div v-else >
      <!-- 변경할 비밀번호 -->
      <form class="row g-3 user--info--form" @submit.prevent>
        <!-- 변경할 비밀번호 -->
        <div>
          <input
            type="password"
            id="password"
            v-model="credentials.password"
            placeholder="변경 할 비밀번호"
            class="form-control"
            :class="{ 'is-invalid': passwordHasError }"
          />
          <div v-show="valid.password" class="input-danger valid-form">
            대문자, 특수문자, 숫자를 포함해야 합니다.
          </div>

        </div>

        <!-- 변경할 비밀번호 확인 -->
        <div>
          <input
            v-model="credentials.passwordConfirm"
            @keyup.enter="signup"
            type="password"
            id="passwordConfirmation"
            placeholder="변경 할 비밀번호 확인"
            class="form-control"
            :class="{ 'is-invalid ': passwordConfirmHasError }"
          />
          <div v-show="valid.passwordConfirm" class="input-danger valid-form">
            비밀번호가 일치하지 않습니다.
          </div>

        </div>

        <div>
          <input
            type="nickname"
            id="nickname"
            v-model="credentials.nickname"
            placeholder="변경 닉네임"
            class="form-control"
            :class="{ 'is-invalid ': nicknameHasError }"
          />
          <div class="id" v-if="error_type === 7">
            <span>{{ error_message }}</span>
          </div>
        </div>

        <!-- 나이 -->
        <div class="col form-floating">
          <select
            name="age"
            id="age"
            v-model="credentials.age"
            class="form-select"
          >
            <option :value="age" v-for="(age, idx) in this.ages" :key="idx">
              {{ age }}
            </option>
          </select>
          <label for="age">나이</label>
        </div>

        <!-- 성별 -->
        <div class="col form-floating">
          <select
            name="sex"
            id="sex"
            v-model="credentials.sex"
            class="form-select"
          >
            <option :value="sex" v-for="(sex, idx) in this.sex" :key="idx">
              {{ sex }}
            </option>
          </select>
          <label for="sex">성별</label>
        </div>


        <div>
          <input type="email" id="eamil" v-model="credentials.email" class="form-control" placeholder="이메일"/>
        </div>
        <div class="row " style="padding-top:25px;">
          <div class="col" style="text-align:center">
            <button @click="updateUser" class="user--update--button">수정</button>
          </div>
          <div class="col" style="text-align:center">
            <button @click="deleteModal" class="user--delete--button">회원탈퇴</button>

          </div>
        </div>
      </form>

      <Modal v-if="isDeleteModal === true" @modal-close="isDeleteModal = false">
        <delete-user-view
          @modal-close="isDeleteModal = false"
          @modal-close-delete="modalClose"
        />
      </Modal>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Modal from "@/views/utils/Modal.vue";
import DeleteUserView from "@/views/accounts/DeleteUserView.vue";

export default {
  name: "ChangeUserView",

  components: {
    Modal,
    DeleteUserView,
  },
  data() {
    return {
      isDeleteModal: false,
      isAuthenticated: false,
      authenticated_password: null,
      ages: ["10대", "20대", "30대", "40대", "50대"],
      sex: ["남자", "여자"],
      credentials: {
        password: null,
        passwordConfirm: null,
        nickname: null,
        age: null,
        sex: null,
        email: null,
      },
      error_type: null,
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
  computed: {
    userPk() {
      return this.$store.state.userStore.userPk;
    },
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
    deleteModal() {
      this.isDeleteModal = true;
    },
    modalClose: function () {
      this.$emit("modal-close");
      this.$emit("modal-delete-user");
    },
    modalCloseChange: function(){
      this.$emit("modal-close")
    },
    checkUser: function () {

      axios({
        // get으로 하면 안됨
        method: "post",
        url: `http://127.0.0.1:8000/accounts/user/${this.userPk}/`,
        data: { password: this.authenticated_password },
      })
        .then((res) => {
          alert("인증 완료");

          this.isAuthenticated = true;
        })
        .catch((err) => {
          for (const [key, value] of Object.entries(err.response.data)) {
            if (key === "error") {
              this.error_type = 3;
              this.error_message = value;
              break;
            } else {
              alert("올바르게 정보를 입력하세요!");
              break;
            }
          }
        });
    },
    updateUser: function () {
      axios({
        method: "put",
        url: `http://127.0.0.1:8000/accounts/user/${this.userPk}/`,
        data: this.credentials,
      })
        .then((res) => {
          alert("회원정보 수정 완료");
          this.modalCloseChange();
        })
        .catch((err) => {
          for (const [key, value] of Object.entries(err.response.data)) {

            if (key === "error_type") {
              this.error_type = value;
              this.error_message = err.response.data["error"];
            } else {
              alert("정보를 올바르게 입력하세요");
            }
            break;
          }
        });
    },
  },
};
</script>

<style></style>
