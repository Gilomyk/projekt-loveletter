<template>
  <div class="home-view">
    <div class="card-container">
      <UserCard
        v-for="card in visibleCards"
        :key="card.user?.id"
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
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import UserCard from '@/components/UserCard.vue'

// Typ pojedynczego użytkownika
interface User {
  id: number;
  first_name: string
  age: number
  profile_picture: string
  status: 'liked' | 'rejected' | null
}

// Typ pojedynczej karty
interface Card {
  user: User
  position: 'left' | 'center' | 'right' | 'hidden-right'
}

const noMoreUsers = ref(false)
const startIndex = ref(0)

// Lista użytkowników pobieranych z bazy przez endpoint
const allUsers = ref<User[]>([])
onMounted(async () => {
  try {
    const response = await axios.get('http://localhost:8000/users/') 
    console.log('Otrzymany JSON:', response.data)
    allUsers.value = response.data.filter((u: User) => u.id !== 1).map(u => ({ ...u, status: null }))  // Załaduj dane użytkowników
  } catch (error) {
    console.error('Error fetching users:', error)
  }
})

// Widoczne karty
const visibleCards = computed<Card[]>(() => {
  const cards: Card[] = []
  const len = allUsers.value.length

  // jeśli nie ma jeszcze żadnych userów, nie próbuj nic renderować
  if (len === 0) return cards

  // zabezpiecz, żeby startIndex nigdy nie wyszedł poza zakres
  if (startIndex.value >= len) {
    startIndex.value = 0
  }

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
