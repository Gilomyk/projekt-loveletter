<!-- Widok karty z nagłówkiem karty bocznej -->
<template>
  <div class="card">
    <img :src="user?.profile_picture" alt="Profile" class="profile-image" />

    <div class="card-footer">
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
import { defineProps } from 'vue'
import { NIcon } from 'naive-ui'
import { ArrowDown } from '@vicons/fa'

interface User {
  id: number;
  first_name: string;
  age: number;
  profile_picture: string;
}

defineProps<{
  user: User;
}>()
// dodać na początku 'const props = 'jeśli będą zmiany w renderowaniu

</script>

<style scoped>
.card {
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
  height: 50vh;
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
</style>
