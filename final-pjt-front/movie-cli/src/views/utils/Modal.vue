<template>
    <div id="modal">
        <!-- modalbox class 얘를 씌우면 뒤에 내용이 안보이는것 같고... 안씌우면 뒤에 내용이 보이는것 같고.. -->
    <div class="modalbox"> 
      <div class="overlay" @click="modalClose"></div>
      <div class="modal-card">
        <slot></slot>
      </div>
    </div>
    </div>
</template>

<script>
export default {

    name:"Modal",
    methods:{
        modalClose: function() {
        this.$emit('modal-close')
      }
    }

}
</script>

<style>

.modalbox, .overlay{
  width:100%;
  height:100%;
  position:fixed;
  left:0;
  top:0;
}

.overlay {
  opacity:0.5;
  background-color:black;
}

.modal-card {

  position:relative;
  max-width:80%;
  margin:auto;
  margin-top:30px;
  padding:20px;
  background-color:white;
  min-height:500px;
  z-index:10;
  opacity:1;
}

</style>