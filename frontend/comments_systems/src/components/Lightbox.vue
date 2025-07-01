<template>
  <transition name="lightbox">
    <div v-if="visible" class="lightbox" @click.self="close">
      <div class="lightbox-content">
        <img :src="imageUrl" alt="Enlarged view">
        <button class="close-btn" @click="close">×</button>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  name: 'Lightbox',
  props: {
    imageUrl: String
  },
  data() {
    return {
      visible: true
    }
  },
  methods: {
    close() {
      this.visible = false
      this.$emit('close')
    }
  }
}
</script>

<style scoped>
.lightbox {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.lightbox-content {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
}

.lightbox-content img {
  max-width: 100%;
  max-height: 80vh;
  border-radius: 4px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.5);
}

.close-btn {
  position: absolute;
  top: -40px;
  right: 0;
  background: none;
  border: none;
  color: white;
  font-size: 40px;
  cursor: pointer;
  opacity: 0.7;
  transition: opacity 0.2s;
}

.close-btn:hover {
  opacity: 1;
}

.lightbox-enter-active, .lightbox-leave-active {
  transition: opacity 0.3s;
}

.lightbox-enter, .lightbox-leave-to {
  opacity: 0;
}

.lightbox-enter-to, .lightbox-leave {
  opacity: 1;
}
</style>