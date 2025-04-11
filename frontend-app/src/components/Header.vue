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
            <n-button class="icon-btn" :style="{ backgroundColor: '#E8ADB5' }">
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
            <n-button class="icon-btn" :style="{ backgroundColor: '#E8ADB5' }">
                <n-icon size="32">
                    <Users />
                </n-icon>
            </n-button>
            <span>Liked People</span>
        </div>
      </div>
    
  
      <!-- Left Dropdown Button (Previously Right) -->
      <n-button class="dropdown-btn" :style="{ backgroundColor: '#EA8F8F' }">
        <div class="user-info">
          <span>User 1#</span>
          <n-icon>
            <ArrowDown />
          </n-icon>
        </div>
      </n-button>
    </header>
  </template>
  
  <script setup lang="ts">
  import { NButton, NIcon } from 'naive-ui';
  import { Home, Cog, Inbox, Users, ArrowDown } from '@vicons/fa';
  import { useRouter } from 'vue-router';

  const router = useRouter();

  const goToHome = () => {
    router.push('/');
  };

  const goToChat = () => {
    router.push('/chat');
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
  