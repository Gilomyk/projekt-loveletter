<template>
  <div class="likes-view">
    <div class="likes-header">
     <h1>Your Likes</h1>
    </div>
    <div class="likes-container">
      <LikedUserCard
        v-for="(user, index) in likedUsers"
        :key="user.id"
        :user="user"
        :position="getPosition(index)"
        @swipe="handleSwipe"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { defineProps } from 'vue'

import LikedUserCard from '@/components/LikedUserCard.vue'
import { ref, computed } from 'vue'

const likedUsers = ref([
  { name: 'Alice', age: 24, image: 'https://randomuser.me/api/portraits/women/44.jpg' },
  { name: 'Bob', age: 27, image: 'https://randomuser.me/api/portraits/men/18.jpg' },
  { name: 'Charlie', age: 22, image: 'https://randomuser.me/api/portraits/men/45.jpg' },
  { name: 'David', age: 29, image: 'https://randomuser.me/api/portraits/men/53.jpg' },
  { name: 'Eva', age: 26, image: 'https://randomuser.me/api/portraits/women/21.jpg' },
  { name: 'Frank', age: 31, image: 'https://randomuser.me/api/portraits/men/6.jpg' },
  { name: 'Grace', age: 28, image: 'https://randomuser.me/api/portraits/women/64.jpg' },
  { name: 'Helen', age: 34, image: 'https://randomuser.me/api/portraits/women/16.jpg' },
  { name: 'Ivy', age: 25, image: 'https://randomuser.me/api/portraits/women/29.jpg' },
  { name: 'Jack', age: 32, image: 'https://randomuser.me/api/portraits/men/80.jpg' },
  { name: 'Liam', age: 23, image: 'https://randomuser.me/api/portraits/men/10.jpg' },
  { name: 'Mia', age: 27, image: 'https://randomuser.me/api/portraits/women/11.jpg' }
]);
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
  flex-direction: column;
  flex-wrap: wrap;
  height: 100%;
  width: 95%;
  border-radius: 10px;
  overflow-x: scroll;
}
</style>