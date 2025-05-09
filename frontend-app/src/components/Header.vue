<template>
  <header class="header">
    <!-- Right Buttons (Previously Left) -->
    <div class="buttons">
      <div class="button">
          <n-button class="icon-btn" :style="{ backgroundColor: '#E8ADB5' }" @click="goToHome">
              <n-icon size="32">
                  <Home />
              </n-icon>
          </n-button>
          <span>Home</span>
      </div>

      <div class="button">
          <n-button class="icon-btn" :style="{ backgroundColor: '#E8ADB5' }" @click="goToPreferences">
              <n-icon size="32">
                  <Cog />
              </n-icon>
          </n-button>
          <span>Preferences</span>
      </div>

      <div class="button">
          <n-button class="icon-btn" :style="{ backgroundColor: '#E8ADB5' }" @click="goToChat">
              <n-icon size="32">
                  <Inbox />
              </n-icon>
          </n-button>
          <span>Chats</span>
      </div>

      <div class="button">
          <n-button class="icon-btn" :style="{ backgroundColor: '#E8ADB5' }" @click="goToLikeHistory">
              <n-icon size="32">
                  <Users />
              </n-icon>
          </n-button>
          <span>Liked People</span>
      </div>
    </div>
  

    <!-- Left Dropdown Button (Previously Right) -->
    <n-dropdown trigger="click" :options="users" @select="switchUser" >
      <n-button class="dropdown-btn" :style="{ backgroundColor: '#EA8F8F' }">
        <div class="user-info">
          <span>{{ currentUser?.username}}</span>
          <n-icon>
            <ArrowDown />
          </n-icon>
        </div>
      </n-button>
    </n-dropdown>
  </header>
</template>

<script setup lang="ts">
import { NButton, NIcon, NDropdown  } from 'naive-ui';
import { Home, Cog, Inbox, Users, ArrowDown } from '@vicons/fa';
import { useRouter } from 'vue-router';
import { ref,  onMounted } from 'vue';
import axios from '@/axios';

const router = useRouter();
const users = ref<{ id: number; username: string }[]>([]);
const currentUser = ref<{ username: string } | null>(null);

const goToHome = () => {
  router.push('/');
};

const goToChat = () => {
  router.push('/chat');
};

const goToPreferences = () => {
  router.push('/preferences');
};

const goToLikeHistory = () => {
  router.push('/liked');
};


// Pobierz listę użytkowników
const fetchUsers = async () => {
  try {
    const response = await axios.get('/users/');
    users.value = response.data.map((user: { id: number, username: string }) => ({
    label: user.username,
    key: user.id,
    }));

    // Pobierz aktualnego użytkownika z sesji
    const currentUserResponse = await axios.get('/get_current_user/');
    currentUser.value = currentUserResponse.data;
  } catch (error) {
    console.error(error);
  }
};

onMounted(() => {
  fetchUsers();
});



// Przełączanie użytkownika
const switchUser = async (userId: number) => {
  console.log("Wybrano użytkownika z ID:", userId);
  try {
    await axios.post(`/switch_user/${userId}/`);
    const foundUser = users.value.find((user) => user.id === userId);
    if (foundUser) {
      currentUser.value = { username: foundUser.username };
    } else {
      currentUser.value = null;
    }
    location.reload();
  } catch (error) {
    console.error(error);
  }
};



</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  background: linear-gradient(to bottom, white, #FFFEFE);
  padding: 10px 20px;
  border-bottom: 2px solid #333; 
}

.buttons {
  display: flex;
  gap: 10px;
}

.button {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.icon-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 85px;
  height: 66px;
  border-radius: 8px;
  padding: 5px;
  font-size: 12px;
  text-align: center;
}

.icon-btn span {
  margin-top: 5px;
  color: #333;
}

.dropdown-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 140px;
  height: 66px;
  border-radius: 8px;
  padding: 5px;
  font-size: 12px;
  text-align: center;
}

.user-info {
  display: flex;
  align-items: center;
}

.user-info span {
  margin-right: 5px;
  font-weight: bold;
}
</style>
