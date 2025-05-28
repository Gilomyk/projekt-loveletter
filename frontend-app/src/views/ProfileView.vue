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
            <div class="data-list inherit">
                <h1>Basic Information</h1>
                <ul>
                    <li>Location: {{ user?.location }}</li>
                    <li>Education: PLACEHOLDER</li>
                    <li>Occupation: PLACEHOLDER</li>
                    <li>About Me: </li>
                </ul>
                <div class="text-area">
                    <span>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</span>                    
                </div>
            </div>
            <div class="data-plain inherit">
                <h1>Dating Goals</h1>
                <span>{{ user?.relationship_goal["name"] }}</span>
            </div>    
            <div class="data-plain-multiple inherit">
                <h1>Hobbies</h1>  
                <ul>
                    <li v-for="(index, item) in user?.hobbies">
                        {{ index["name"] }}
                    </li>
                </ul>
            </div>  
            <div class="data-plain inherit">
                <h1>Lifestyle Choices</h1>
                <span>{{ user?.lifestyle["name"] }}</span>
            </div>
            <div class="data-plain-multiple inherit">
                <h1>Languages</h1>
                <ul>
                    <li>English</li>
                    <li>German</li>
                </ul>
            </div> 
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, watch, computed, onMounted } from 'vue'
import axios from '@/axios'
import { NButton, NIcon } from 'naive-ui'
import { LongArrowAltLeft, User } from '@vicons/fa'
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
}

interface Component {
    name: string;
    fields: string[];
    icon: typeof NIcon;
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
    grid-template-columns: [col] auto [col] auto;
    grid-template-rows: [row] auto [row] auto [row] auto [row] auto ;
    grid-column-gap: 10vh;
    grid-row-gap: 5vh;
    align-content: start end;
    align-items: start end;
    border-radius: 10px;
}

.inherit {
    border-radius: inherit;
}

.inherit h1 {
    margin-left: 5%;
}

.inherit span {
    margin-left: 5%;
}

.data-first-name {
    background-color: #FFEFEF;
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
    border-radius: inherit
}

.data-picture {
    border-radius: inherit;
}

.data-picture img {
    border-radius: inherit;
    max-width: 100%;
}

.data-list {
    background-color: #FF9191;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.data-list ul {
    font-size: x-large;
    list-style: none;
}

.data-list li {
    margin-bottom: 5%;
}

.text-area {
    margin: 5%;
    border-radius: inherit;
    background-color: #FFEFEF;
    max-height: 100%;
}

.text-area span {
    padding: 5%;
    font-size: large;
    text-wrap-mode: wrap;
    text-align: center;
}

.data-plain {
    background-color: #FFF8F8;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.data-plain span {
    margin-bottom: 5%;
}

.data-plain-multiple {
    background-color: #FFF8F8;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.data-plain-multiple ul {
    list-style: none;
    display: flex;
    flex-direction: row;
    gap: 2vw;
}
</style>