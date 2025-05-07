<script>
import axios from 'axios';

export default {
  name: 'App',
  data() {
    return {
      messages: [],
      userInput: '',
      isLoading: false
    }
  },
  methods: {
    async sendMessage() {
      if (!this.userInput.trim() || this.isLoading) return;

      const userMessage = this.userInput.trim();
      this.messages.push({ type: 'user', content: userMessage });
      this.userInput = '';
      this.isLoading = true;

      try {
        const response = await axios.post('http://localhost:5000/chat', {
          message: userMessage
        });

        if (response.data.status === 'success') {
          this.messages.push({ 
            type: 'bot', 
            content: response.data.response 
          });
        } else {
          throw new Error(response.data.error || '请求失败');
        }
      } catch (error) {
        this.messages.push({ 
          type: 'error', 
          content: '抱歉，发生了错误：' + error.message 
        });
      } finally {
        this.isLoading = false;
      }
    }
  }
}
</script>

<template>
  <div class="chat-container">
    <div class="chat-messages" ref="messagesContainer">
      <div v-for="(message, index) in messages" :key="index" 
           :class="['message', message.type]">
        {{ message.content }}
      </div>
    </div>
    <div class="chat-input">
      <input 
        v-model="userInput" 
        @keyup.enter="sendMessage"
        placeholder="输入消息..."
        :disabled="isLoading"
      />
      <button @click="sendMessage" :disabled="isLoading">
        {{ isLoading ? '发送中...' : '发送' }}
      </button>
    </div>
  </div>
</template>

<style>
.chat-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #f5f5f5;
  border-radius: 8px;
  margin-bottom: 20px;
}

.message {
  margin: 10px 0;
  padding: 10px 15px;
  border-radius: 8px;
  max-width: 70%;
}

.user {
  background: #007bff;
  color: white;
  margin-left: auto;
}

.bot {
  background: white;
  color: #333;
  margin-right: auto;
}

.error {
  background: #dc3545;
  color: white;
  margin-right: auto;
}

.chat-input {
  display: flex;
  gap: 10px;
}

input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

button {
  padding: 10px 20px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

button:hover:not(:disabled) {
  background: #0056b3;
}
</style>
