<template>
  <div
    :class="['card', cardClass]"
    :style="cardStyle"  
  >
    <div v-if="liked" class="indicator liked">
      <NIcon :size="20"><Heart /></NIcon>
    </div>
    <div v-if="rejected" class="indicator rejected">
      <NIcon :size="20"><Times /></NIcon>
    </div>
    <img :src="user?.profile_picture" alt="Profile" class="profile-image" />

    <!-- Center card layout -->
    <div v-if="position === 'center'" class="card-footer-center-card">
      <div class="card-header">
        <span class="name-age">{{ user?.first_name }}, {{ user?.age }}</span>
      </div>
      <div class="bottom-bar">
        <div class="button" @click="rejectUser">
          <n-button class="icon-btn" :style="{ backgroundColor: '#E8ADB5' }">
            <n-icon size="24"><LongArrowAltLeft /></n-icon>
          </n-button>
          <span>Not For Me</span>
        </div>
        <div class="more-info">
          <n-icon class="arrow-down" :size="24"><ArrowDown /></n-icon>
          <span>More info</span>
        </div>
        <div class="button" @click="likeUser">
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
        <span class="name-age">{{ user?.first_name }}, {{ user?.age }}</span>
      </div>
      <div class="more-info">
        <n-icon class="arrow-down" :size="24"><ArrowDown /></n-icon>
      <span>More info</span>
    </div>
  </div>
</div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits, ref, computed } from 'vue'
import { NButton, NIcon } from 'naive-ui'
import { Heart, Times } from '@vicons/fa'
import { ArrowDown, LongArrowAltLeft, Feather } from '@vicons/fa'

// Definicja typów:
interface User {
id: number;
first_name: string;
age: number;
profile_picture: string;
status: 'liked' | 'rejected' | null;
}

type CardPosition = 'left' | 'center' | 'right' | 'hidden-right';

const props = defineProps<{
user: User;
position: CardPosition;
}>()

const emit = defineEmits<{
(e: 'swipe', payload: { direction: 'left' | 'right'; user: User }): void;
(e: 'like', payload: { user: User }): void;
(e: 'reject', payload: { user: User }): void;
}>()

const cardClass = computed(() => {
if (props.position === 'center') return 'center-card'
if (props.position === 'left') return 'left-card'
if (props.position === 'right') return 'right-card'
return 'hidden-right-card'
})

const liked = ref(false)
const rejected = ref(false)

const cardStyle = computed(() => {
const base = {
  transition: 'transform 0.5s ease, opacity 0.5s ease',
}

if (props.position === 'center') {
  return {
    ...base,
    transform: 'scale(1.0) translateY(0)',
    zIndex: 2,
  }
}

if (props.position === 'left') {
  return {
    ...base,
    transform: 'scale(0.9) translateX(-35vw)',
    zIndex: 1,
  }
}

if (props.position === 'right') {
  return {
    ...base,
    transform: 'scale(0.9) translateX(35vw)',
    zIndex: 1,
  }
}

return {
  ...base,
  transform: 'scale(0.9) translateX(35vw)',
  zIndex: 0,
}
})

function likeUser() {
if (props.user.status === null){
  liked.value = true
  emit('like', { user: props.user });
  emit('swipe', { direction: 'right', user: props.user });
}
}

function rejectUser() {
if (props.user.status === null){
  rejected.value = true
  emit('reject', { user: props.user });
  emit('swipe', { direction: 'left', user: props.user }); // poprawiłem swipe na left przy reject
}
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

.hidden-right-card{
transition: opacity 0.5s ease, transform 0.5s ease;
box-shadow: none
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
height: 50vh;
object-fit: cover;
object-position: center;
}

.indicator {
position: absolute;
top: 10px;
right: 10px;
opacity: 0;
}

.liked {
color: green;
}

.rejected {
color: red;
}

.card .indicator {
transition: opacity 0.5s ease;
opacity: 1;
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
