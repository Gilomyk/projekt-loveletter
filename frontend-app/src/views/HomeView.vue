<template>
  <div class="home-view">
    <button class="toggle-button" @click="useRecommendations = !useRecommendations">
      {{ useRecommendations ? 'Show All Users' : 'Filter By Recommendations' }}
    </button>
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
import { ref, watch, computed, onMounted } from 'vue'
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
const currentUser = ref<User | null>(null)
// Lista użytkowników pobieranych z bazy
const allUsers = ref<User[]>([])
const likedUsers = ref<User[]>([])
const likedUserIds = ref<number[]>([])
const useRecommendations = ref(false)

// Pobierz aktualnego użytkownika
async function fetchCurrentUser() {
  try {
    const response = await axios.get('/get_current_user/')
    currentUser.value = response.data
  } catch (error) {
    console.error('Nie udało się pobrać aktualnego użytkownika:', error)
  }
}

// Pobierz listę id polubionych użytkowników
async function fetchLikedUserIds() {
  try {
    const response = await axios.get('/likes/') // lub /matches/, zależnie od implementacji
    likedUserIds.value = response.data.map((u: User) => u.id)
  } catch (error) {
    console.error('Błąd podczas pobierania polubionych użytkowników:', error)
  }
}

// Pobierz listę wszystkich użytkowników
async function fetchAllUsers() {
  try {
    const response = await axios.get('/users/')
    const otherUsers = response.data.filter((u: User) => 
      u.id !== currentUser.value?.id && !likedUserIds.value.includes(u.id)
    )
    allUsers.value = otherUsers.map((u: User) => ({ ...u, status: null }))
  } catch (error) {
    console.error('Błąd podczas pobierania użytkowników:', error)
  }
}

// Pobierz listę rekomendowanych użytkowników
async function fetchRecommendedUsers() {
  try {
    const response = await axios.get('/recommendations/')
    const otherUsers = response.data.filter((u: User) => 
      u.id !== currentUser.value?.id && !likedUserIds.value.includes(u.id)
    )
    likedUsers.value = otherUsers.map((u: User) => ({ ...u, status: null }))
  } catch (error) {
    console.error('Błąd podczas pobierania rekomendowanych użytkowników:', error)
  }
}




// Reaktywne przeładowanie użytkowników po zmianie flagi
watch(useRecommendations, async (newVal) => {
  if (newVal) {
    await fetchRecommendedUsers()
  } else {
    await fetchAllUsers()
  }
})

onMounted(async () => {
  await fetchCurrentUser()
  await fetchLikedUserIds()
  if (useRecommendations.value) {
    await fetchRecommendedUsers()
  } else {
    await fetchAllUsers()
  }

})

// Widoczne karty
const visibleCards = computed<Card[]>(() => {
  const cards: Card[] = []
  const len = allUsers.value.length

  // jeśli nie ma jeszcze żadnych userów, nie próbuj nic renderować
  if (len === 0 || !currentUser.value) return cards

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
async function handleLike(payload: { user: User }) {
  payload.user.status = 'liked'
  
  try {
    const response = await axios.post(`/like/${payload.user.id}/`)
    console.log('Polubienie zapisane:', response.data)
  } catch (error) {
    console.error('Błąd podczas lajkowania:', error)
  }

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

.toggle-button {
  padding: 10px 20px;
  background-color: #FF96A4;
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  transition: background-color 0.3s ease, transform 0.2s ease;
  margin: 20px auto;
  display: block;
}

.toggle-button:hover {
  background-color: #ff7d90;
  transform: translateY(-2px);
}

.toggle-button:active {
  transform: translateY(1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

</style>