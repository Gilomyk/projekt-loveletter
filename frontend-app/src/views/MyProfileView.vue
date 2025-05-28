<template>
    <div class="profile-container">
        <div class="profile-grid">
            <div class="data-first-name inherit">
                <h1>{{ user?.first_name }}, {{ user?.age }}</h1>
            </div>
            <div class="profile-go-back-btn inherit">
                <n-button class="icon-btn" @click="goBack" :style="{ backgroundColor: '#82F7FB' }">
                    <n-icon size="24"><LongArrowAltLeft /></n-icon>
                </n-button>
                <span>Go Back</span>
              <div class="preferences-save-button">
        <n-button class="icon-btn" :style="{ backgroundColor: '#58CCD0' }" @click="saveProfile">
          <span>Save Profile</span>
        </n-button>
      </div>
            </div>

            <div class="data-picture inherit">
                <img :src="user?.profile_picture" alt="Profile" class="profile-image"/>
            </div>
            <div class="data-list inherit color-a">
                <div class="header">
                    <h1>Basic Information</h1>
                    <n-icon size="32"><InfoCircle /></n-icon>
                </div>
                <ul>
                    <li>
                        <n-icon size="32"><MapMarkerAlt /></n-icon>
                      <span>Location:</span>
                        <div class="text-area">
                            <input type="text" class="short-field" v-model="location" />
                        </div>
                    </li>
                    <!-- <li>
                        <n-icon size="32"><BookOpen /></n-icon>
                        <span>Education: PLACEHOLDER</span>
                    </li>
                    <li>
                        <n-icon size="32"><Suitcase /></n-icon>
                        <span>Occupation: PLACEHOLDER</span>
                    </li> -->
                    <li>
                        <n-icon size="32"><User /></n-icon>
                        <span>About Me:</span>
                    </li>
                </ul>
                <div class="text-area">
                    <input type="text" class="description-field" v-model="bio" />
                </div>
            </div>
            <div class="data-plain inherit color-a">
                <div class="header">
                    <h1>Dating Goals</h1>
                    <n-icon size="32"><Heart /></n-icon>
                </div>
                <div class="preference-field dropdown-field">

       <n-space vertical>
          <n-select v-model:value="dating_goal"
          :options="dating_goals"
          placeholder="What are you looking for?"/>
        </n-space>
      </div>
            </div>
            <div class="data-plain-multiple inherit color-c">
                <div class="header">
                    <h1>Hobbies</h1>
                    <n-icon size="32"><Dumbbell /></n-icon>
                </div>
                <div class="preference-field multiplie-choice-field">

        <n-space vertical>
          <n-select v-model:value="filtered_hobbies"
          multiple :options="hobbies" />
        </n-space>
      </div>
            </div>
            <div class="data-plain inherit color-b">
                <div class="header">
                    <h1>Lifestyle Choices</h1>
                    <n-icon size="32"><Home /></n-icon>
                </div>
                <div class="preference-field dropdown-field">
                    <n-space vertical>
                      <n-select v-model:value="lifestyle"
                      :options="lifestyles"
                      placeholder="What is your lifestyle?"/>
                    </n-space>
                </div>
            </div>
            <div class="data-plain inherit color-a">
                <div class="header">
                    <h1>Languages</h1>
                    <n-icon size="32"><Language /></n-icon>
                </div>
                <div class="text-area">
                    <input type="text" class="short-field" v-model="language" />
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">

import { ref, onMounted } from 'vue'
import axios from '@/axios'
import {NButton, NIcon, NSelect, NSpace} from 'naive-ui'
import { LongArrowAltLeft, User, InfoCircle, Heart, Dumbbell, Home, Language, MapMarkerAlt } from '@vicons/fa'
import { useRouter } from 'vue-router'

const first_name = ref('')
const age = ref(18)
const location = ref('')
const bio = ref('')
const language = ref('')
const lifestyle = ref(null)
const dating_goal = ref(null)
const filtered_hobbies = ref<string[]>([])
const profilePicture = ref<File | null>(null)

const userId = ref<number | null>(null)

const hobbies = ref([])
const lifestyles = ref([])
const dating_goals = ref([])


// Typ pojedynczego użytkownika
interface User {
  id: number
  first_name: string
  age: number
  location: string
  profile_picture: string
  lifestyle: string
  relationship_goal: string
  hobbies: string[]
  bio: string
  language: string
}

const user = ref<User>()

onMounted(async () => {
  try {
    const [lifestylesRes, goalsRes, traitsRes, userRes] = await Promise.all([
      axios.get('/lifestyles/'),
      axios.get('/relationship-goals/'),
      axios.get('/traits/'),
      axios.get('/get_current_user/')
    ])

    lifestyles.value = lifestylesRes.data.map((item: any) => ({
      label: item.name,
      value: item.id.toString()
    }))

    dating_goals.value = goalsRes.data.map((item: any) => ({
      label: item.name,
      value: item.id.toString()
    }))

    hobbies.value = traitsRes.data.map((item: any) => ({
      label: item.name,
      value: item.id.toString()
    }))

    const u = userRes.data
    user.value = u
    userId.value = u.id
    first_name.value = u.first_name || ''
    age.value = u.age || 18
    location.value = u.location || ''
    bio.value = u.bio?.content || ''
    language.value = u.language?.name || ''
    lifestyle.value = u.lifestyle?.id?.toString() || null
    dating_goal.value = u.relationship_goal?.id?.toString() || null
    filtered_hobbies.value = u.hobbies.map((h: any) => h.id.toString())

  } catch (error) {
    console.error('Błąd ładowania danych profilu:', error)
  }
})

async function saveProfile() {
  try {
    const formData = new FormData();

    //formData.append('first_name', first_name.value);
    //formData.append('age', age.value);
    if(location.value)
      formData.append('location', location.value);
    formData.append('bio', bio.value  );
    if(language.value)
      formData.append('language', language.value);
    if(lifestyle.value) {
      formData.append('lifestyle', lifestyle.value);
    }
    if(dating_goal.value) {
      formData.append('relationship_goal', dating_goal.value);
    }
    // Dodaj hobby jako listę ID
    filtered_hobbies.value.forEach(id => {
      formData.append('hobbies', id);
    });

    // Jeśli edytujesz też zdjęcie profilowe:
    //if (profilePicture.value) {
    //  formData.append('profile_picture', profilePicture.value);
    //}

    await axios.post(`/update_current_user_profile/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    alert('Profil zapisany!');
  } catch (err) {
    console.error('Błąd zapisu profilu:', err);
    alert('Nie udało się zapisać profilu.');
  }
}




const router = useRouter()
const goBack = () => {
  router.back()
}
</script>


<style scoped>
.profile-container {
    background-color: #FFDADA;
    margin: 20px;
    height: 100%;
    border-radius: 10px;
    font-weight: bold;
}
.preference-field {
  background-color: #FFFFFF;
  margin: 10px;
  margin-bottom: 50px;
  border-radius:10px;
  padding: 10px;
}

.description-field{
  flex: 1;
  padding: 10px;
  border-radius: 5px;
  border: none;
  margin-right: 10px;
}
.short-field{
  height: 30px;
  flex: 1;
}
.preferences-save-button {
  border-radius: 10px;
  align-self: flex-end;
}
.profile-grid {
    padding: 2%;
    max-width: 100%;
    margin: 20px;
    display: grid;
    grid-template-columns: [col] 40% [col] auto;
    grid-template-rows: [row] auto [row] 500px [row] auto [row] auto ;
    grid-column-gap: 10vh;
    grid-row-gap: 5vh;
    align-content: start end;
    align-items: start end;
    border-radius: 10px;
}

.inherit {
    border-radius: inherit;
}

.lighter-color {
    background-color: #FFDADA;
}

.color-a {
    background-color: #FF9191;
}

.color-b {
    background-color: #FFFFFF;
}

.color-c {
    background-color: #82F7FB;
}

.inherit h1 {
    margin-left: 5%;
}

.header {
    margin-right: 5%;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
}

.inherit span {
    font-size: large;
}

.inherit li {
    font-size: large;
}

.data-first-name {
    background-color: #FFFFFF;
    text-wrap-mode: nowrap;
    justify-content: center;
}

.data-first-name h1 {
    padding-left: 1vw
}

.profile-go-back-btn {
    display: flex;
    flex-direction: column;
    align-items: end;
    align-content: stretch;
    justify-content: space-between;
}

.icon-btn {
    padding: auto;
    background-color: #82F7FB;
    border-radius: inherit;
}

.data-picture {
    position: relative;
    height: 100%;
    width: 100%;
    display: flex;
    justify-content: center;
    background-color: #21263a;
    border: 6px solid;
    border-image: linear-gradient(135deg, #cd7373, #000000) 6;
    box-sizing: border-box;
    overflow: hidden;
}

.data-picture img {
    border-radius: inherit;
    height: 100%;
}

.data-list {
    display: flex;
    flex-direction: column;
}

.data-list ul {
    font-size: x-large;
    list-style: none;
}

.data-list li {
    margin-bottom: 2%;
    margin-right: 10%;
    display: flex;
    flex-direction: row;
    gap: 10px;
}

.about-me {
    display: flex;
    flex-direction: column;
}

.about-me-header {
    display: flex;
    flex-direction: row;
    text-wrap-mode: nowrap;
}

.text-area {
    margin: 0 5% 5% 5%;
    border-radius: 5px;
    background-color: #FFEFEF;
    height: 100%;
    display: flex;
    justify-items: center;
    justify-content: center;
}

.text-area span {
    margin: 2%;
    text-wrap-mode: wrap;
    max-height: auto;
    font-size: large;
}

.data-plain {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.data-plain span {
    margin-bottom: 5%;
    background-color: #FFCCCC;
    width: fit-content;
    padding: 1%;
    border-radius: inherit;
    margin-left: 5%;
}

.data-plain-multiple {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    border-radius: inherit;
}

.data-plain-multiple ul {
    list-style: none;
    display: flex;
    flex-direction: row;
    border-radius: inherit;
    gap: 2%;
}

.data-plain-multiple li {
    background-color: #FFEFEF;
    width: fit-content;
    padding: 1%;
    border-radius: inherit;
    margin-bottom: 2%;
}
</style>