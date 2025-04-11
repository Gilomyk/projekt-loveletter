<template>
  <div class="home-view">
    <div class="card-container">
      <UserCard
        v-for="(user, index) in visibleUsers"
        :key="user.id"
        :user="user"
        :position="getPosition(index)"
        @swipe="handleSwipe"
      />
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

import UserCard from '@/components/UserCard.vue'
import { ref, computed } from 'vue'

const allUsers = ref([
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

const startIndex = ref(0)
const visibleUsers = computed(() => {
  const result = []
  for (let i = 0; i < 3; i++) {
    const index = (startIndex.value + i) % allUsers.value.length
    result.push(allUsers.value[index])
  }
  return result
})

function getPosition(index) {
  if (index === 0) return 'left'
  if (index === 1) return 'center'
  return 'right'
}

// Oceń Maciek czy to jest prawo-lewo czy lewo-prawo, na razie klikasz jeden z dwóch guzików na karcie i sie przesuwa
// W razie czego zmienię w drugą stronę i oczywiście jakoś zwizualizuję jak kliknięto "Send a letter"

function handleSwipe({ direction, user }) {
  console.log(`Swiped ${direction} on`, user)

  // Po przesunięciu: zwiększamy indeks, czyli idziemy do kolejnych użytkowników
  if (direction === 'right') {
    startIndex.value = (startIndex.value + 1) % allUsers.value.length
  }
}



</script>

<style scoped>
.home-view {
  display: flex;
  align-items: center;
  flex-direction: column;
  height: 90vh;
  width: 100%;
}

.card-container {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

</style>
