<template>
  <div class="chat-view">
    <div class="chat-title">
      <h1>Your Matches</h1>
    </div>

    <div class="chat-container">
      <!-- Lewa kolumna z listą czatów -->
      <div class="chat-list">
        <div class="chat-item" v-for="(user, index) in allUsers" :key="index" :class="{ active: selectedUserIndex === index }" @click="selectedUserIndex = index">
          <div class="profile-gradient">
            <img class="chat-image" :src="user.image" alt="Profile" />
          </div>
          <div class="chat-details">
            <span class="chat-name">{{ user.name }}</span>
            <span class="chat-last-message">{{ user.lastMessage || '' }}</span>
          </div>
        </div>
      </div>

      <!-- Okno czatu -->
      <div class="chat-window">
        <!-- Nagłówek -->
        <div class="chat-header">
          <div class="chat-info">
            <div class="profile-gradient">
              <img class="profile-image" :src="allUsers[selectedUserIndex].image" alt="Profile">
            </div>
            <span class="current-chat-name">{{ allUsers[selectedUserIndex].name }}</span>
          </div>
            <n-icon size="24" color="#fff" class="call-icon">
              <Phone />
            </n-icon>
        </div>

        <!-- Główna część czatu -->
        <div class="chat-content">
          <div
            v-for="(message, idx) in allUsers[selectedUserIndex].messages"
            :key="idx"
            :class="['message-' + message.side]"
          >
            <p>{{ message.text }}</p>
          </div>
        </div>

        <!-- Stopka czatu -->
        <div class="chat-footer">
          <input type="text" class="message-input" placeholder="Type a message">
          <n-icon size="24" color="#fff" class="send-icon">
            <Send16Regular />
          </n-icon>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent } from "vue";
import { NIcon } from "naive-ui";
import { Phone } from "@vicons/fa";
import { Send16Regular }from "@vicons/fluent"

export default defineComponent({
  name: "ChatView",
  components: {
    NIcon,
    Phone,
    Send16Regular
  },
  data() {
    return {
      selectedUserIndex: 0,
      allUsers: [
        {
          name: 'Alice',
          age: 24,
          image: 'https://randomuser.me/api/portraits/women/0.jpg',
          messages: [
            { text: 'Cześć, jak się masz?', side: 'left' },
            { text: 'Hej! Wszystko dobrze, a Ty?', side: 'right' },
            { text: 'Super, dzięki że pytasz!', side: 'left' },
          ],
          lastMessage: 'Super, dzięki że pytasz!'
        },
        {
          name: 'Bob',
          age: 27,
          image: 'https://randomuser.me/api/portraits/men/0.jpg',
          messages: [
            { text: 'Siemka, dawno się nie widzieliśmy!', side: 'left' },
            { text: 'Prawda, trzeba to nadrobić', side: 'right' },
          ],
          lastMessage: 'Prawda, trzeba to nadrobić'
        },
        { name: 'Charlie', age: 22, image: 'https://randomuser.me/api/portraits/men/1.jpg' },
        { name: 'David', age: 29, image: 'https://randomuser.me/api/portraits/men/2.jpg' },
        { name: 'Eva', age: 26, image: 'https://randomuser.me/api/portraits/women/1.jpg' },
        { name: 'Frank', age: 31, image: 'https://randomuser.me/api/portraits/men/3.jpg' }
      ]
    };
  }
});
</script>

<style scoped>
.chat-view {
  background-color: #FFCBCB;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 20px;
  height: 82vh;
}

.chat-title {
  height: auto;
  width: 95%;
  flex-shrink: 0;
  margin-left: 10px;
}

.chat-container {
  display: flex;
  justify-content: space-between;
  width: 95%;
  flex: 1;
  overflow: hidden;
}

.chat-list {
  background-color: #FFEAEA;
  width: 25%;
  max-height: 100%;
  height: 100%;
  overflow-y: auto;
  border-radius: 10px;
  padding: 10px;
  display: flex;
  flex-direction: column;
}

.chat-item {
  background-color: white;
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  border: 2px solid #CD6969;
  padding: 10px;
  border-radius: 10px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.chat-item:hover {
  background-color: #f3d0d5;
}

.chat-item.active {
  background-color: #e8adb5;
  font-weight: bold;
  color: white;
}

.profile-gradient {
  background: linear-gradient(to right, #FF7F50, #CD6969);
  padding: 3px;
  border-radius: 10%;
  display: inline-block;
}

.chat-image {
  width: 40px;
  height: 40px;
  border-radius: 10%;
  display: block;
}


.chat-details {
  display: flex;
  flex-direction: column;
  margin-left: 10px;
}

.chat-name {
  font-weight: bold;
}

.chat-last-message {
  font-size: 0.9em;
  color: #888;
}

.chat-window {
  background-color: #ffffff;
  width: 75%; /* Prawa kolumna */
  max-height: 100%;
  height: 100%;
  overflow-y: auto;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
}

.chat-header {
  background-color: #EA8F8F;
  display: flex;
  justify-content: space-between;
  padding: 10px;
  align-items: center;
}

.chat-info {
  display: flex;
  align-items: center;
}

.profile-image {
  width: 40px;
  height: 40px;
  border-radius: 10%;
  display: block;
}

.current-chat-name {
  font-weight: bold;
  padding: 10px;
}

.call-icon {
  cursor: pointer;
}

.chat-content {
  flex: 2;
  overflow-y: auto;
  padding: 15px;
  display: flex;
  flex-direction: column;
}

.message-left {
  background-color: #FF8484;
  border-radius: 10px;
  padding-inline: 10px;
  max-width: 40%;
  margin-bottom: 10px;
  align-self: flex-start;
  word-wrap: break-word;
  white-space: normal;
  font-weight: bold;
}

.message-right {
  background-color: #D5D5D5;
  border-radius: 10px;
  padding-inline: 10px;
  max-width: 40%;
  margin-bottom: 10px;
  align-self: flex-end;
  word-wrap: break-word;
  white-space: normal;
  font-weight: bold;
}

.chat-footer {
  background-color: #58CCD0;
  display: flex;
  padding: 10px;
  align-items: center;
}

.message-input {
  flex: 1;
  padding: 10px;
  border-radius: 5px;
  border: none;
  margin-right: 10px;
}

.send-icon {
  cursor: pointer;
  font-size: 24px;
}
</style>
