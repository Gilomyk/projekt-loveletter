<template>
  <div class="chat-view-when-matches" v-if="allUsers.length > 0">
    <div class="chat-title">
      <h1>Your Matches</h1>
    </div>
    <div class="chat-container">
      <!-- Lewa kolumna z listą czatów -->
      <div class="chat-list">
        <div
          class="chat-item"
          v-for="(user, index) in allUsers"
          :key="user.id"
          :class="{ active: selectedUserIndex === index }"
          @click="selectUser(index)"
        >
          <div class="profile-gradient">
            <img class="chat-image" :src="user.profile_picture" alt="Profile" />
          </div>
          <div class="chat-details">
            <span class="chat-name">{{ user.first_name }}</span>
            <span class="chat-last-message">{{ user.lastMessage || '' }}</span>
          </div>
        </div>
      </div>

      <!-- Okno czatu -->
      <div class="chat-window" v-if="selectedUser">
        <!-- Nagłówek -->
        <div class="chat-header">
          <div class="chat-info">
            <div class="profile-gradient">
              <img class="profile-image" :src="selectedUser.profile_picture" alt="Profile" />
            </div>
            <span class="current-chat-name">{{ selectedUser.first_name }}</span>
          </div>
          <!-- <n-icon size="24" color="#fff" class="call-icon">
            <Phone />
          </n-icon> -->
        </div>

        <!-- Główna część czatu -->
        <div class="chat-content">
          <div
            v-for="(message, idx) in messages"
            :key="idx"
            :class="['message-' + (message.sender === currentUserId ? 'right' : 'left'), 'message-bubble']"
          >
            <p>{{ message.content }}</p>
            <small v-if="message.sender === currentUserId" class="read-status">
              {{ message.is_read ? 'Read' : 'Unread' }}
            </small>
          </div>
          <div v-if="isTyping" class="typing-indicator">{{ selectedUser.first_name }} is typing...</div>
        </div>

        <!-- Stopka czatu -->
        <div class="chat-footer">
          <input type="text" class="message-input" v-model="newMessage" placeholder="Type a message" @input="sendTypingSignal">
          <n-icon size="24" color="#fff" class="icebreaker-icon" @click="getRandomIcebreaker">
            <Hammer />
          </n-icon>
          <n-icon size="24" color="#fff" class="send-icon" @click="sendMessage">
            <Send16Regular />
          </n-icon>
        </div>
      </div>
    </div>
  </div>
  <div class="chat-view-no-matches" v-else>
    <div class="chat-title">
      <h1>Your Matches</h1>
    </div>
    <div class="chat-container-no-matches">
      <div class="no-matches-text">
        <h1>No matches!</h1>
        <p>It seems you haven’t got any maches! <br>Go ahead to the homepage and change that!</p>        
      </div>
      <n-button class="home-button" :style="{ backgroundColor: '#E8ADB5' }" @click="goToHome">
        <p>Go to Homepage</p>
      </n-button>
    </div>
  </div>
</template>

<script>
import { defineComponent, computed } from "vue";
import axios from "@/axios";
import { NIcon, NButton } from "naive-ui";
import { Phone, Hammer } from "@vicons/fa";
import { Send16Regular } from "@vicons/fluent";
import { useRouter } from 'vue-router';

let socket = null;

export default defineComponent({
  name: "ChatView",
  components: {
    NIcon,
    NButton,
    Phone,
    Send16Regular,
    Hammer
  },
  data() {
    return {
      currentUserId: null,
      selectedUserIndex: 0,
      matchId: null,
      allUsers: [],
      matches: [],
      messages: [],
      newMessage: "",
      isTyping: false,
      router: useRouter(),
    };
  },
  watch: {
    messages: {
      handler() {
        this.markMessagesAsRead();
      },
      deep: true
    }
  },
  computed: {
    selectedUser() {
      return this.allUsers[this.selectedUserIndex];
    },
  },
  methods: {
    /** UI methods */
    selectUser(index) {
      this.selectedUserIndex = index;
      const selected = this.allUsers[index];

      const foundMatch = this.matches.find(match =>
        (match.user1.id === this.currentUserId && match.user2.id === selected.id) ||
        (match.user2.id === this.currentUserId && match.user1.id === selected.id)
      );

      if (!foundMatch) return console.error("❌ No match found for selected user");

      this.matchId = foundMatch.id;
      this.connectWebSocket(this.matchId);
      this.fetchMessages(this.matchId);
      this.markMessagesAsRead();
    },

    /** Networking */
    fetchMessages(matchId) {
      axios.get(`/messages/${matchId}/`).then(response => {
        this.messages = response.data;
      });
    },

    goToHome() {
      this.router.push('/');
    },

    connectWebSocket(matchId) {
      try {
        socket = new WebSocket(`ws://127.0.0.1:8000/ws/chat/${matchId}/`);

        socket.onopen = () => {
          console.log("✅ WebSocket connected.");
          this.markMessagesAsRead();
        }
        socket.onerror = error => console.error("❌ WebSocket error:", error);
        socket.onclose = event => console.warn(`⚠️ WebSocket closed (${event.code}):`, event.reason || "No reason");

        socket.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);

            if (data.type === "new_message") {
              const msg = {
                ...data.message,
                sender: data.message.sender_id,
                receiver: data.message.receiver_id,
              };

              this.messages.push(msg);

            } else if (data.type === "typing") {
              if (data.user_id !== this.currentUserId) {
                this.isTyping = true;
                setTimeout(() => (this.isTyping = false), 1500);
              }

            } else if (data.type === "message_read") {
              const messageId = data.message_id;

              const msg = this.messages.find(m => m.id === messageId);
              if (msg && !msg.is_read) {
                msg.is_read = true;
              }

            } else {
              console.warn("⚠️ Unknown message type:", data);
            }
          } catch (err) {
            console.error("❌ Error parsing WebSocket message:", event.data, err);
          }
        };
      } catch (err) {
        console.error("❌ WebSocket connection failed:", err);
      }
    },

    /** Messaging */
    sendMessage() {
      if (!this.newMessage) return;

      socket.send(JSON.stringify({
        type: "new_message",
        content: this.newMessage,
        receiver_id: this.selectedUser.id,
        sender_id: this.currentUserId
      }));

      this.newMessage = "";
    },

    sendTypingSignal() {
      socket.send(JSON.stringify({
        type: "typing",
        user_id: this.currentUserId
      }));
    },

    markMessagesAsRead() {
      const unreadIds = this.messages
        .filter(msg => !msg.is_read && msg.sender === this.selectedUser.id)
        .map(msg => msg.id);

      if (!unreadIds.length) return;

      const sendAll = () => {
        if (socket && socket.readyState === WebSocket.OPEN) {
          unreadIds.forEach(id => {
            socket.send(JSON.stringify({ type: "message_read", message_id: id }));
          });
        } else {
          setTimeout(sendAll, 100);
        }
      };

      sendAll();
    },
    async getRandomIcebreaker() {
      try {
        const response = await axios.get('/icebreaker/');
        this.newMessage = response.data.question;
      } catch (error) {
        console.error('Błąd podczas pobierania pytania:', error);
        this.newMessage = 'Błąd: nie udało się pobrać pytania.';
      }
    }
  },

  mounted() {
    axios.get("/get_current_user/")
      .then(userResponse => {
        this.currentUserId = userResponse.data.id;

        axios.get("/chat/")
          .then(matchResponse => {
            this.matches = matchResponse.data;

            this.allUsers = matchResponse.data.map(match => {
              const matchedUser = match.user1.id === this.currentUserId ? match.user2 : match.user1;
              return { ...matchedUser, lastMessage: '', messages: [] };
            });

            this.selectUser(0);
          });
      });
  }
});
</script>


<style scoped>
.chat-view-when-matches {
  background-color: #FFCBCB;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 20px;
  height: 82vh;
  border-radius: 10px;
}

.chat-view-no-matches {
  background-color: #FFCBCB;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 20px;
  height: 100%;
  border-radius: 10px;
}

.chat-container-no-matches {
  padding-top: 10%;
  padding-bottom: 10%;
  background-color: #FFDFDF;
  height: 100%;
  width: 95%;
  border-radius: 10px;
  margin: 1vh;
  text-align: center;
  align-items: center;
  font-size: 20px;
}

.no-matches-text {
  margin: auto;
}

.home-button {
  padding: 2%;
  border-radius: 10px;
  font-size: 30px;
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
  position: relative;
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
  position: relative;
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

/* Nowe */
.read-status {
  display: none;
  font-size: 10px;
  color: #555;
  position: absolute;
  bottom: -14px;
  right: 4px;
  font-weight: normal;
}

.message-left:hover .read-status,
.message-right:hover .read-status {
  display: inline;
}

.typing-indicator {
  font-size: 12px;
  color: #ccc;
  margin: 5px;
  font-style: italic;
}

.chat-footer {
  background-color: #58CCD0;
  display: flex;
  padding: 10px;
  align-items: center;
  justify-items: space-around;
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

.icebreaker-icon {
  margin-right: 1%;
  cursor: pointer;
  font-size: 24px;
}
</style>