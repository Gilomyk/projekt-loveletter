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
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import axios from '@/axios'
import LikedUserCard from '@/components/LikedUserCard.vue'

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
    return likes
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
</style>