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
                        <span>Location: {{ user?.location }}</span>
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
                    <span>{{ user?.bio["content"] }}</span>
                </div>
            </div>
            <div class="data-plain inherit color-a">
                <div class="header">
                    <h1>Dating Goals</h1>   
                    <n-icon size="32"><Heart /></n-icon>                 
                </div>
                <span>{{ user?.relationship_goal["name"] }}</span>
            </div>    
            <div class="data-plain-multiple inherit color-c">
                <div class="header">
                    <h1>Hobbies</h1>   
                    <n-icon size="32"><Dumbbell /></n-icon>                 
                </div>
                <ul>
                    <li v-for="(index, item) in user?.hobbies">
                        {{ index["name"] }}
                    </li>
                </ul>
            </div>  
            <div class="data-plain inherit color-b">
                <div class="header">
                    <h1>Lifestyle Choices</h1>   
                    <n-icon size="32"><Home /></n-icon>                 
                </div>
                <span>{{ user?.lifestyle["name"] }}</span>
            </div>
            <div class="data-plain inherit color-a">
                <div class="header">
                    <h1>Languages</h1>   
                    <n-icon size="32"><Language /></n-icon>                 
                </div>
                <span>{{ user?.language["name"] }}</span>
            </div> 
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, watch, computed, onMounted } from 'vue'
import axios from '@/axios'
import { NButton, NIcon } from 'naive-ui'
import { LongArrowAltLeft, User, InfoCircle, Heart, Dumbbell, Home, Language, MapMarkerAlt, Suitcase, BookOpen } from '@vicons/fa'
import { useRoute } from 'vue-router'
import { useRouter } from 'vue-router'

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

const route = useRoute()
const user = ref<User>()
onMounted(async () => {
  try {
    const response = await axios.get('/users/') 
    console.log('id: ', route.params.id)
    console.log('Profile otrzymane - Otrzymany JSON:', response.data)
    const values = response.data.filter((u: User) => u.id == route.params.id).map((u: User) => ({ ...u}))
    const valuesMapped = values.map((u: User) => ({ ...u}))
    console.log('Profile przetworzone - Otrzymany JSON:', valuesMapped)
    user.value = valuesMapped[0]
  } catch (error) {
    console.error('Error fetching users:', error)
  }
})

const router = useRouter();
const goBack = () => {
  router.back();
};
</script>

<style scoped>
.profile-container {
    background-color: #FFDADA;
    margin: 20px;
    height: 100%;
    border-radius: 10px;
    font-weight: bold;
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