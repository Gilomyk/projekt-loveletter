<!-- Widok karty z nagłówkiem karty bocznej -->
<template>
  <div class="card">
    <img :src="user?.profile_picture" alt="Profile" class="profile-image" />
    <div class="card-footer">
      <div class="card-header">
        <span class="name-age">{{ user?.first_name }}, {{ user?.age }}</span>
      </div>
      <div class="more-info">
          <n-button class="icon-btn" :style="{ backgroundColor: '#E8ADB5' }" @click="goToProfile">
            <n-icon class="arrow-down" :size="24"><ArrowDown /></n-icon>
          </n-button>
          <span>More info</span>
      </div>
      <div class="button" @click="unsendLetter">
          <n-button class="icon-btn" :style="{ backgroundColor: '#E8ADB5' }">
            <n-icon size="24"><PaperPlane/></n-icon>
          </n-button>
          <span>Unsend letter</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'
import { NButton, NIcon } from 'naive-ui'
import { ArrowDown, LongArrowAltLeft, PaperPlane } from '@vicons/fa'
import { useRouter } from 'vue-router';
import axios from 'axios'
// message = useMessage()

interface User {
  id: number;
  first_name: string;
  age: number;
  profile_picture: string;
}

const props = defineProps<{
  user: User;
}>()

const emit = defineEmits<{
(e: 'unsend', payload: { user: User }): void;
}>()

const router = useRouter();
const goToProfile = () => {
  router.push({name: 'profile', params: {id: props.user.id}});
};

async function unsendLetter() {
  try {
    await axios.post(`/api/unlike/${props.user.id}/`, {}, { withCredentials: true })
    emit('unsend', { user: props.user })
  } catch (error) {
    console.error('Błąd przy usuwaniu polubienia:', error)
  }
}
</script>

<style scoped>
.card {
  width: 30vw;
  max-width: 400px;
  height: fit-content;
  border: 3px solid transparent;
  border-image: linear-gradient(135deg, #cd7373, #000000) 1;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.card:hover {
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

@media (max-width: 768px) {
  .card {
    width: 80vw;
  }
}

@media (max-width: 480px) {
  .card {
    width: 90vw;
  }
}

.profile-image {
  width: 100%;
  height: 60vh;
  object-fit: cover;
  object-position: center;
}

.card-footer {
  height: 50%;
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
</style>
