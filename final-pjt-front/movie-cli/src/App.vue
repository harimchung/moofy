<template>
  <div id="app">
    <nav
      id="nav"
      :class="{ white: whiteModeClass, change_color: scrollPosition > 5 }"
    >
      <div class="left">
        <div class="logo">
          <!-- <router-link :to="{ name: 'Main' }"> -->
          <img @click="goMain" src="@/assets/moofie_logo.png" alt="logo" class="nav__logo" />
          <!-- </router-link> -->
        </div>

      </div>

      <div class="right" style="display: flex">
        <div v-if="isLoggedIn" style="display: flex; align-items: center">
          <div class="search">
            <div class="search-bar">
              <font-awesome-icon
                icon="fa-solid fa-magnifying-glass"
                class="icon"
              />
              <input
                type="text"
                v-model="InputValue"
                @keyup.enter="searchInput"
                style="max-width: 180px"
                placeholder="제목, 배우를 입력하세요."
              />
            </div>
          </div>

          <router-link @click.native="logout" to="#">Logout</router-link>
          <button @click="changeUser" class="signup__button">
            회원정보수정
          </button>
        </div>

        <div v-else style="display: flex">
          <button @click="popLogin" class="login__button">Login</button>
          <button @click="popSignUp" class="signup__button">회원가입</button>
        </div>
      </div>
    </nav>

    <router-view :isLoggedIn="isLoggedIn" class="router-view" @not-found="notfound = true"/>

    <!-- 로그아웃 전용 페이지(랜덤으로 보여주기) -->
    <div v-if="isLoggedIn === false && notfound === false" class="logout-random-body">
      <logout-random />
    </div>

    <Modal v-if="isLoginModal === true" @modal-close="isLoginModal = false">
      <login-view @modal-close="isLoginModal = false" @login="loginCompleted" />
    </Modal>

    <Modal v-if="isSignUpModal === true" @modal-close="isSignUpModal = false">
      <signup-view @modal-close="isSignUpModal = false" />
    </Modal>

    <Modal v-if="isChangeModal === true" @modal-close="modalCloseChange">
      <change-user-view
        @modal-close="modalCloseChange"
        @modal-delete-user="isLoggedIn = false"
      />
    </Modal>
  </div>
</template>

<script>
import Modal from "./views/utils/Modal.vue";
import LoginView from "./views/accounts/LoginView.vue";
import SignupView from "./views/accounts/SignupView.vue";
import ChangeUserView from "./views/accounts/ChangeUserView.vue";
import LogoutRandom from "@/components/recommendation/LogoutRandom.vue";
export default {
  name: "App",
  components: {
    Modal,
    LoginView,
    SignupView,
    ChangeUserView,
    LogoutRandom,
  },
  data: function () {
    return {
      isLoginModal: false,
      isSignUpModal: false,
      scrollPosition: null,
      isChangeModal: false,
      isLoggedIn: false,
      InputValue: null,
      notfound:false,
    };
  },
  computed: {
    userPk() {
      return this.$store.state.userStore.userPk;
    },
    isLoggedIn() {
      return this.$store.state.userStore.isLoggedIn;
    },
  },
  methods: {
    logout() {
      this.isLoggedIn = false;
      //localStorage.removeItem("jwt");
      localStorage.clear();
      this.$router.push({ name: "Main" });
      // vuex에 저장되어있는 것들 초기화
      this.$store.dispatch("userStore/logout");
    },
    popLogin() {
      this.isLoginModal = true;
    },
    popSignUp() {
      this.isSignUpModal = true;
    },
    changeUser() {
      this.isChangeModal = true;
    },
    loginCompleted() {
      this.isLoggedIn = true;
      this.$store.dispatch("userStore/getUserPk");
    },
    modalCloseChange(){
      this.loginCompleted();
      this.isChangeModal = false;
    },
    updateScroll() {
      this.scrollPosition = window.scrollY;
    },
    searchInput() {
      this.$router
        .push({
          name: "Search",
          params: { keyword: this.InputValue },
        })
        .catch((error) => {
          if (error.name === "NavigationDuplicated") {
            location.reload();
          }
        });
      this.InputValue = null;
    },
    notFound(indicator){
      this.notfound = indicator
    },
    goMain(){
      this.notfound = false;
      this.$router.push({name:'Main'})
    }
  },
  created() {
    const token = localStorage.getItem("jwt");
    if (token) {
      this.isLoggedIn = true;
      this.$store.dispatch("userStore/getUserPk");
    }
    this.notfound = false;
  },
  mounted() {
    window.addEventListener("scroll", this.updateScroll);
  },
  computed: {
    whiteModeClass() {
      return !!this.$route.meta?.whiteMode;
    },
  },
};
</script>

<style>
@import "@/assets/styles/App.css";
@import "@/assets/styles/User/Modal.css";

#app {
  font-family: "Pretendard", sans-serif;
  /* -webkit-font-smoothing: antialiased; */
  -moz-osx-font-smoothing: grayscale;
  /* text-align: center; */
  color: #0d0d0d;
  box-sizing: border-box;
}
</style>

<style scoped>
#nav a {
  font-weight: 300;
  color: #0d0d0d;
  text-decoration: none;
}

.white {
  color: white;
  font-weight: 300;
  text-decoration: none;
  border: none;
}

.white button {
  border: white;
  color: white;
  transition: 0.2s;
}

.white a {
  color: white !important;
  transition: 0.2s;
}

.white .search {
  border: 1px solid white !important;
}
.white .search-bar input::placeholder {
  color: white !important;
}

.white .icon {
  color: white !important;
}

.change_color {
  background-color: white;
}

.change_color a {
  color: #0d0d0d !important;
  transition: 0.2s;
}

.change_color button {
  color: #0d0d0d !important;
  transition: 0.2s;
}

.change_color .search-bar input::placeholder {
  color: #0d0d0d !important;
}
.change_color .search {
  border: 1px solid #0d0d0d !important;
}

.change_color .icon {
  color: #0d0d0d !important;
}
</style>
