<template>
  <div class="likes-view">
    <div class="likes-header">
     <h1>Your Likes</h1>
    </div>
    <div class="likes-container">
      <LikedUserCard
        v-for="(user) in likedUsers"
        :key="user.id"
        :user="user"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import LikedUserCard from '@/components/LikedUserCard.vue'

interface LikedUser {
  id: number;
  first_name: string
  age: number
  profile_picture: string
}

const likedUsers = ref<LikedUser[]>([
  { id: 1, first_name: 'Alice', age: 24, profile_picture: 'https://randomuser.me/api/portraits/women/44.jpg'},
  { id: 2, first_name: 'Bob', age: 27, profile_picture: 'https://randomuser.me/api/portraits/men/18.jpg'},
  { id: 3, first_name: 'Charlie', age: 22, profile_picture: 'https://randomuser.me/api/portraits/men/45.jpg'},
  { id: 4, first_name: 'David', age: 29, profile_picture: 'https://randomuser.me/api/portraits/men/53.jpg'},
  { id: 5, first_name: 'Eva', age: 26, profile_picture: 'https://randomuser.me/api/portraits/women/21.jpg'},
  { id: 6, first_name: 'Frank', age: 31, profile_picture: 'https://randomuser.me/api/portraits/men/6.jpg'},
  { id: 7, first_name: 'Grace', age: 28, profile_picture: 'https://randomuser.me/api/portraits/women/64.jpg'},
  { id: 8, first_name: 'Helen', age: 34, profile_picture: 'https://randomuser.me/api/portraits/women/16.jpg'},
  { id: 9, first_name: 'Ivy', age: 25, profile_picture: 'https://randomuser.me/api/portraits/women/29.jpg'},
  { id: 10, first_name: 'Jack', age: 32, profile_picture: 'https://randomuser.me/api/portraits/men/80.jpg'},
  { id: 11, first_name: 'Liam', age: 23, profile_picture: 'https://randomuser.me/api/portraits/men/10.jpg'},
  { id: 12, first_name: 'Mia', age: 27, profile_picture: 'https://randomuser.me/api/portraits/women/11.jpg'}
])
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
}

.card {
  flex-shrink: 0; /* żeby karty się nie ściskały */
}
</style>