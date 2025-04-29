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
import axios from '@/axios'
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

// Statyczna lista użytkowników
// const allUsers = ref<User[]>([
//   { id: 1, first_name: 'Alice', age: 24, profile_picture: 'https://randomuser.me/api/portraits/women/44.jpg', status: null },
//   { id: 2, first_name: 'Bob', age: 27, profile_picture: 'https://randomuser.me/api/portraits/men/18.jpg', status: null },
//   { id: 3, first_name: 'Charlie', age: 22, profile_picture: 'https://randomuser.me/api/portraits/men/45.jpg', status: null },
//   { id: 4, first_name: 'David', age: 29, profile_picture: 'https://randomuser.me/api/portraits/men/53.jpg', status: null },
//   { id: 5, first_name: 'Eva', age: 26, profile_picture: 'https://randomuser.me/api/portraits/women/21.jpg', status: null },
//   { id: 6, first_name: 'Frank', age: 31, profile_picture: 'https://randomuser.me/api/portraits/men/6.jpg', status: null },
//   { id: 7, first_name: 'Grace', age: 28, profile_picture: 'https://randomuser.me/api/portraits/women/64.jpg', status: null },
//   { id: 8, first_name: 'Helen', age: 34, profile_picture: 'https://randomuser.me/api/portraits/women/16.jpg', status: null },
//   { id: 9, first_name: 'Ivy', age: 25, profile_picture: 'https://randomuser.me/api/portraits/women/29.jpg', status: null },
//   { id: 10, first_name: 'Jack', age: 32, profile_picture: 'https://randomuser.me/api/portraits/men/80.jpg', status: null },
//   { id: 11, first_name: 'Liam', age: 23, profile_picture: 'https://randomuser.me/api/portraits/men/10.jpg', status: null },
//   { id: 12, first_name: 'Mia', age: 27, profile_picture: 'https://randomuser.me/api/portraits/women/11.jpg', status: null }
// ])

// Lista użytkowników pobieranych z bazy
const allUsers = ref<User[]>([])
onMounted(async () => {
  try {
    const response = await axios.get('/users/') 
    console.log('Otrzymany JSON:', response.data)
     // Endpoint, który zwraca użytkowników
    allUsers.value = response.data.filter((u: User) => u.id !== 1).map((u: User) => ({ ...u, status: null }))  // Załaduj dane użytkowników
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
