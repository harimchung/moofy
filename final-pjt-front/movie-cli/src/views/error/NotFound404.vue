<template>
    <div style="margin-top:150px; text-align:center;">
      <img 
      src="@/assets/404_error_image.png" 
      alt=""
      style="width:50%; max-width: 600px;">
      <h2>없는 페이지 입니다.</h2>
    </div>
  </template>
  
  <script>
  export default {
      name: 'NotFound404',
      data() {
        return {
          notfound:true
        }
      },
      methods: {
        notFound() {
          this.$emit('not-found',this.notfound)
        }
      },
      created(){
        this.notFound()
      }
  }
  </script>
  
  <style>
  
  </style>
  