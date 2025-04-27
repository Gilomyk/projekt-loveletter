<template>
  <div class="home-view">
    <div class="card-container">
      <UserCard
        v-for="card in visibleCards"
        :key="card.user.id"
        :user="card.user"
        :position="card.position"
        @like="handleLike"
        @reject="handleReject"
      />
    </div>
    <div v-if="noMoreUsers">
      <p>Nie ma więcej użytkowników. Zmień preferencje.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import UserCard from '@/components/UserCard.vue'

// Typ pojedynczego użytkownika
interface User {
  id: number;
  name: string
  age: number
  image: string
  status: 'liked' | 'rejected' | null
}

// Typ pojedynczej karty
interface Card {
  user: User
  position: 'left' | 'center' | 'right' | 'hidden-right'
}

// Statyczna lista użytkowników
const allUsers = ref<User[]>([
  { id: 1, name: 'Alice', age: 24, image: 'https://randomuser.me/api/portraits/women/44.jpg', status: null },
  { id: 2, name: 'Bob', age: 27, image: 'https://randomuser.me/api/portraits/men/18.jpg', status: null },
  { id: 3, name: 'Charlie', age: 22, image: 'https://randomuser.me/api/portraits/men/45.jpg', status: null },
  { id: 4, name: 'David', age: 29, image: 'https://randomuser.me/api/portraits/men/53.jpg', status: null },
  { id: 5, name: 'Eva', age: 26, image: 'https://randomuser.me/api/portraits/women/21.jpg', status: null },
  { id: 6, name: 'Frank', age: 31, image: 'https://randomuser.me/api/portraits/men/6.jpg', status: null },
  { id: 7, name: 'Grace', age: 28, image: 'https://randomuser.me/api/portraits/women/64.jpg', status: null },
  { id: 8, name: 'Helen', age: 34, image: 'https://randomuser.me/api/portraits/women/16.jpg', status: null },
  { id: 9, name: 'Ivy', age: 25, image: 'https://randomuser.me/api/portraits/women/29.jpg', status: null },
  { id: 10, name: 'Jack', age: 32, image: 'https://randomuser.me/api/portraits/men/80.jpg', status: null },
  { id: 11, name: 'Liam', age: 23, image: 'https://randomuser.me/api/portraits/men/10.jpg', status: null },
  { id: 12, name: 'Mia', age: 27, image: 'https://randomuser.me/api/portraits/women/11.jpg', status: null }
])

const noMoreUsers = ref(false)
const startIndex = ref(0)

// Widoczne karty
const visibleCards = computed<Card[]>(() => {
  const cards: Card[] = []
  const len = allUsers.value.length

  // Ukryta prawa karta
  if (startIndex.value > 1) {
    cards.push({
      user: allUsers.value[startIndex.value - 2],
      position: 'hidden-right',
    })
  }
  // karta po prawej
  if (startIndex.value > 0) {
    cards.push({ 
      user: allUsers.value[startIndex.value - 1], 
      position: 'right' 
    })
  }
  // karta środkowa
  cards.push({ 
    user: allUsers.value[startIndex.value], 
    position: 'center' 
  })
  // karta po lewej
  if (startIndex.value < len - 1) {
    cards.push({ 
      user: allUsers.value[startIndex.value + 1], 
      position: 'left' 
    })
  }
  return cards
})

// Obsługa polubienia
function handleLike(payload: { user: User }): void {
  payload.user.status = 'liked'
  nextUser()
}

// Obsługa odrzucenia
function handleReject(payload: { user: User }): void {
  payload.user.status = 'rejected'
  nextUser()
}

// Przejście do następnego użytkownika
function nextUser(): void {
  if (startIndex.value < allUsers.value.length - 1) {
    startIndex.value++
  } else {
    noMoreUsers.value = true
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
