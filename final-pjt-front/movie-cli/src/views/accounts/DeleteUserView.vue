<template>
  <div>
    <h5 class="modal--text">회원정보 탈퇴하기</h5>
    <div style="width: 80%">
      <p>비밀번호를 입력해주세요.</p>
      <label for="password">비밀번호: </label>
      <input type="password" id="password" v-model="password" class="password--input--form form-control"/>
      <div class="id input-danger" v-if="error_type === 3">
        <span>{{ error_message }}</span>
      </div>
      <!-- <div class="id" v-else-if="error_type === 3"><span>{{error_message}}</span></div> -->
      <div style="display: flex; justify-content: flex-end">
        <button @click="withdrawal" class="checkUser--button">탈퇴</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "DeleteUserView",

  data() {
    return {
      password: null,
      error_type: null,
      error_message: null,
    };
  },

  computed: {
    userPk() {
      return this.$store.state.userStore.userPk;
    },
  },

  methods: {
    modalCloseDelete: function () {
      this.$emit("modal-close-delete");
    },

    withdrawal() {
      const userId = this.userPk;

      axios({
        method: "delete",
        url: `http://127.0.0.1:8000/accounts/user/${userId}/`,
        data: { password: this.password },
      })
        .then((res) => {

          this.$store.dispatch("userStore/logout");

          localStorage.removeItem("jwt");

          // this.$router.push({ name: "Main" });
          // vuex에 저장되어있는 것들 초기화

          this.modalCloseDelete();
        })
        .catch((err) => {
          for (const [key, value] of Object.entries(err.response.data)) {
            if (key === "error") {
              this.error_type = 3;
              this.error_message = value;
              break;
            } else {
              alert("비밀번호를 올바르게 입력하세요");
              break;
            }
          }
        });
    },
  },
};
</script>

<style></style>
