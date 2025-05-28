<template>
  <div class="likes-view">
    <div class="likes-header">
     <h1>Your Likes</h1>
    </div>
    <div v-if="noLikes === true" class="no-likes-container">
      <div class="no-likes-text">
        <h1>No like history!</h1>
        <p>It seems you haven’t got anyone in your liked history!<br> Go ahead to the homepage and change that!</p>        
      </div>
      <n-button class="home-button" :style="{ backgroundColor: '#E8ADB5' }" @click="goToHome">
        <p>Go to Homepage</p>
      </n-button>
    </div>
    <div v-else class="likes-container">
      <LikedUserCard
        v-for="(user) in displayedLikes"
        :key="user.id"
        :user="user"
        @unsend="handleUnsend"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { NButton, NIcon, NDropdown } from 'naive-ui';
import { ref, computed, onMounted } from 'vue';
import axios from '@/axios'
import LikedUserCard from '@/components/LikedUserCard.vue'
import { useRouter } from 'vue-router';
import { User } from '@vicons/fa';

const router = useRouter();
const goToHome = () => {
  router.push('/');
};

interface LikedUser {
  id: number;
  first_name: string
  age: number
  profile_picture: string
}

const noLikes = computed<boolean>(() => {
  if (allLikes.value.length === 0) {
    return true
  } else {
    return false
  }
})

// lista polubień z bazy
const allLikes = ref<LikedUser[]>([])
onMounted(async () => {
  try {
    const response = await axios.get('/likes/') 
    console.log('LikedHistory - Otrzymany JSON:', response.data)
    // Endpoint, który zwraca like
    allLikes.value = response.data.filter((u: LikedUser) => u.id !== 1).map((u: LikedUser) => ({ ...u, status: null }))  // Załaduj dane użytkowników
  } catch (error) {
    console.error('Error fetching users:', error)
  }
})

const displayedLikes = computed<LikedUser[]>(() => {
  const likes: LikedUser[] = []

  allLikes.value.forEach(like => {
    likes.push(like)
  });

  likes.reverse()

  return likes
})

function handleUnsend(payload: { user: LikedUser }): void {
  // powołanie endpointu usunięcia osoby z historii liked danego użytkownika

  // usunięcie danej osoby z frontendowej listy liked userów
  const index = allLikes.value.indexOf(payload.user, 0);
  if (index > -1) {
    allLikes.value.splice(index, 1);
  }
}
</script>

<style scoped>
.likes-view {
  background-color: #F09D9D;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 20px;
  height: 100%;
  border-radius: 10px;
}

.likes-header {
  display: flex;
  justify-content: space-between;
  width: 95%;
  align-items: center;
}

.likes-container {
  background-color: #FFDFDF;
  display: flex;
  flex-direction: row; /* Zmieniono z column na row */
  flex-wrap: nowrap; /* zamieniono z wrap na no-wrap*/
  height: 100%;
  width: 95%;
  border-radius: 10px;
  overflow-x: scroll;
  margin: 1vh;
}

.card {
  flex-shrink: 0; /* żeby karty się nie ściskały */
  margin-left: 2vh;
  margin-top: 2vh;
  align-self: flex-end;
}

.no-likes-container {
  padding-top: 10%;
  padding-bottom: 10%;
  background-color: #FFDFDF;
  height: 100%;
  width: 95%;
  border-radius: 10px;
  margin: 1vh;
  text-align: center;
  align-items: center;
  font-size: 20px;
}

.no-likes-text {
  margin: auto;
}

.home-button {
  padding: 2cap;
  border-radius: 10px;
  font-size: 30px;
}
</style>