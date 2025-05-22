<template>
  <div class="likes-view">
    <div class="likes-header">
     <h1>Your Likes</h1>
    </div>
    <div class="likes-container">
      <LikedUserCard
        v-for="(user) in displayedLikes"
        :key="user.id"
        :user="user"
      />
      <div v-if="noLikes" class="no-likes-container">
        <div class="no-likes">
          <h1>No like history!</h1>
          <p>It seems you haven’t got anyone in your liked history! Go ahead to the homepage and change that!</p>
          <n-button class="home-button" :style="{ backgroundColor: '#E8ADB5' }" @click="goToHome">
              <n-icon size="32">
                  <span>Go to Homepage</span>
                  <Home />
              </n-icon>
          </n-button>
        </div>
    </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { NButton, NIcon, NDropdown } from 'naive-ui';
import { ref, computed, onMounted } from 'vue';
import axios from '@/axios'
import LikedUserCard from '@/components/LikedUserCard.vue'
import { useRouter } from 'vue-router';

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

const noLikes = ref(false)

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
  const len = allLikes.value.length

  // jeśli nie ma jeszcze żadnych userów, nie próbuj nic renderować
  if (len === 0) {
    noLikes.value = true
    return likes
  } else {
    noLikes.value = false
  }

  allLikes.value.forEach(like => {
    likes.push(like)
  });

  likes.reverse()

  return likes
})
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
  background-color: #FFDFDF;
  width: 95%;
  border-radius: 10px;
  display:block;
  height:auto;
}

.no-likes {
  align-items: center;
}

.home-button {
  padding: 5cap;
  border-radius: 10px;
  align-items:justify;
}

.home-button span {
  font-size: 30px;
  margin: 50%;
}
</style>