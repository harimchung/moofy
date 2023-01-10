<template>
  <div>
    <div class="recommend__card">
      <div class="recommend__card__img__box">
        <img
          :src="`https://image.tmdb.org/t/p/w600_and_h900_bestv2${movieObject.poster_path}`"
          class="recommend__card__img"
          alt="..."
        />
      </div>
      <div class="recommend__card__text">
        <div class="recommend__card__text__title">
          {{ movieObject.title }}
        </div>
        <div class="recommend__card__content">
          <div class="recommend__card__year__and__nation">
            <p>{{ movieObject.release_date.slice(0, 4) }}</p>
            <p>·</p>
            <p>{{ movieObject.nation }}</p>
          </div>
          <div class="recommend__card__rating">
            <font-awesome-icon
              icon="fa-solid fa-star fa-sm"
              style="color: #262626"
            />
            <p>{{ movieObject.actual_vote_average }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CBRecommendationItem",
  props: {
    movieObject: Object,
  },
};
</script>

<style>
@import "@/assets/styles/Recommendation/Recommendation.css";
</style>
