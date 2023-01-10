<template>
  <div class="main-body">
    <!-- 로그인 전용 페이지 -->

      <!-- 로그인 이후에 유저 profile이 존재하는 경우 -->
      <div v-if="isLoggedIn && userProfile">
        <recommendation />
      </div>

      <!-- 로그인 하고 처음으로 들어온 경우 -->
      <div v-else-if="isLoggedIn">
        <random />
      </div>

  </div>
</template>

<script>
import Random from "@/components/recommendation/Random.vue";
import Recommendation from "@/components/recommendation/Recommendation.vue";
// @ is an alias to /src

export default {
  components: { Recommendation, Random },
  name: "MainView",
  props:{
    isLoggedIn: Boolean,
  },
  computed: {
    userProfile() {
      const userProfile = this.$store.state.userStore.userProfile;
      if (userProfile.length === 0) {
        return false;
      } else {
        return true;
      }
    },
  },
  created: function () {
    const token = localStorage.getItem("jwt");
    if (token) {
      this.$store.dispatch("userStore/getUserPk");
    }
  },

};
</script>

<style>
@import '@/assets/styles/Main.css';
</style>
