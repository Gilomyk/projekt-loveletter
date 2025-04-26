<template>
    <div
      :class="['card', cardClass]"
      :style="cardStyle"
    >
      <img :src="user.image" alt="Profile" class="profile-image" />
  
      <!-- Center card layout -->
      <div v-if="position === 'center'" class="card-footer-center-card">
        <div class="card-header">
          <span class="name-age">{{ user.name }}, {{ user.age }}</span>
        </div>
        <div class="bottom-bar">
          <div class="button" @click="swipeRight">
            <n-button class="icon-btn" :style="{ backgroundColor: '#E8ADB5' }">
              <n-icon size="24"><LongArrowAltLeft /></n-icon>
            </n-button>
            <span>Not For Me</span>
          </div>
          <div class="more-info">
            <n-icon class="arrow-down" :size="24"><ArrowDown /></n-icon>
            <span>More info</span>
          </div>
          <div class="button" @click="swipeRight">
            <n-button class="icon-btn" :style="{ backgroundColor: '#E8ADB5' }">
              <n-icon size="24"><Feather /></n-icon>
            </n-button>
            <span>Send a letter</span>
          </div>
        </div>
      </div>
  
      <!-- Left or right card layout -->
      <div v-else class="card-footer">
        <div class="card-header">
          <span class="name-age">{{ user.name }}, {{ user.age }}</span>
        </div>
        <div class="more-info">
          <n-icon class="arrow-down" :size="24"><ArrowDown /></n-icon>
        <span>More info</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, computed } from 'vue'
import { NButton, NIcon } from 'naive-ui'
import { ArrowDown, LongArrowAltLeft, Feather } from '@vicons/fa';

const props = defineProps({
  user: Object,
  position: String, // 'left' | 'center' | 'right'
})
const emit = defineEmits(['swipe'])

const cardClass = computed(() => {
  if (props.position === 'center') return 'center-card'
  if (props.position === 'left') return 'left-card'
  return 'right-card'
})

const cardStyle = computed(() => {
  let base = {
    transition: 'transform 0.5s ease, opacity 0.5s ease',
  }

  if (props.position === 'center') {
    return {
      ...base,
      transform: 'scale(1.0) translateY(0)',
    }
  }

  if (props.position === 'left') {
    return {
      ...base,
      transform: 'scale(0.9) translateX(-35vw)',
    }
  }

  // right
  return {
    ...base,
    transform: 'scale(0.9) translateX(35vw)',
  }
})


function swipeRight() {
  emit('swipe', { direction: 'right', user: props.user })
}
</script>

<style scoped>

.card{
  position: absolute;
  width: 30vw;
  max-width: 400px;
  height: fit-content;
  border: 3px solid transparent;
  border-image: linear-gradient(135deg, #cd7373, #000000) 1;
  border-radius: 15px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

/* Dodanie cienia */
.card:hover {
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

@media (max-width: 768px) {
  .card {
      width: 80vw;  /* Karty zajmują 80% szerokości dla mniejszych ekranów */
  }
}

@media (max-width: 480px) {
  .card {
      width: 90vw;  /* Karty zajmują 90% szerokości dla bardzo małych ekranów */
  }
}

.profile-image {
  width: 100%;
  object-fit: cover;
}

.card-footer {
  height:50%;
  display: flex;
  justify-content: space-between;
  background-color: #58CCD0;
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
}

.name-age {
  color: #fff;
  font-size: 25px;
  font-weight: bold;
}

.arrow-down {
  color: #000;
}

.more-info {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.more-info span {
  color: #fff;
  font-size: 14px;
  font-weight: bold;
  word-wrap: break-word;
}



.card-footer-center-card {
  height:50%;
  display: flex;
  justify-content: space-between;
  flex-direction: column;
  background-color: #58CCD0;
  padding: 20px;
}

.bottom-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
}
.icons {
  display: flex;
  justify-content: space-between;
  margin: 10px 0;
}

.button {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.button span {
  color: #fff;
  font-size: 14px;
  font-weight: bold;
  word-wrap: break-word;
}

.icon-btn {
  padding: 25%;
  background-color: #FF96A4;
  border-radius: 8px;
}
</style>
  