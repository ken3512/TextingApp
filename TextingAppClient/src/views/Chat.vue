<template>
    <div class="chat">
        <div style="display: flex; text-align: left; margin: 10px;">
                <div style="width: fit-content">
                    <RouterLink style="margin-top: 10px;" class="no-underline" id="about" to="/"><n-button size="tiny" type="info" id="about-button">Back</n-button></RouterLink>
                </div>
                <div style=" width: fit-content; border-radius: 7px; margin-left: auto; margin-right: 0;">
                    <n-dropdown v-if="add.length > 0" trigger="click" :options="add" @select="add_part">
                        <n-button style="margin-left: 10px;"  size="tiny" type="primary">Add</n-button>
                    </n-dropdown>
                    <n-dropdown  v-if="participants.length > 0" trigger="click" :options="participants" @select="handleSelect">
                        <n-button style="margin-left: 10px;" size="tiny" type="info">Participants</n-button>
                    </n-dropdown>
                    <n-popconfirm  :negative-text="null" @positive-click="deleteChat(chat)">
                    <template #trigger>
                        <n-button style="margin-left: 10px;" size="tiny" type="error">Delete chat</n-button>
                    </template>
                    Are you want to delete this chat?
                    </n-popconfirm>
                </div>
        </div>
        <div class="messages">
            <div v-for="message in messages" >
                <div v-if="message.user != user">
                <a style="font-size: 12px;">{{ usertags[message.user] }}</a>
                    <div style="background-color: #2080F0; color: white; padding: 4px; width: fit-content; border-radius: 7px; margin-bottom: 5px;">
                {{ message.text }}
                    </div>
                </div>
                <div v-else>
                    <div style="background-color: #E4E6EB; color: black; padding: 4px; width: fit-content; border-radius: 7px; margin-bottom: 5px; margin-left: auto; margin-right: 0;">
                {{ message.text }}
                    </div>
                </div>
            </div>
        </div>
            <input type='textfield' style="width: 70%;" name='message' v-model="message" required>
            <n-button style="margin-left: 10px;" size="tiny" @:click="sendMessage()" type="info">Send</n-button>
        <br>
    </div>
    <br>
</template>

<script>
import axios from 'axios'
import router from '../router/index.js'

export default {
    name: 'Chat',
    data() {
        return {
            messages: [],
            add: [],
            message: '',
            usertags: {},
            participants: [],
            chat: -1,
            user: -1,
        }
    },
    mounted()
    {
        axios
            .get('/api/v1/users/me')
            .then(response => {
                this.user = response.data.id
                this.chat = this.$route.query.id 
                this.updateMessages()
            })
            .catch(error => {
                this.$store.commit('removeToken')
                delete axios.defaults.headers.common["Authorization"]
                localStorage.removeItem("token")
            })
    },
    methods: {
        add_part(key)
        {
                let ids = key.split(',')
                const formData = {
                    chat_id: parseInt(ids[1]),
                    user_id: parseInt(ids[0]),
                }
                axios
                    .post('/api/v1/add/', formData)
                    .then(response => {
                        this.updateMessages()
                    })
                    .catch(error => {

                    })
        },
        deleteChat(id)
        {
            axios
                .delete('/api/v1/chat?chat_id=' + this.chat)
                .then(response => {
                    this.$router.push('/')
                })
                .catch(error => {
                    console.log(error)
                })
        },
        updateMessages() {
            this.participants = []
            this.add = [];
            axios
                .get('/api/v1/message?chat_id=' + this.chat)
                .then(response => {
                    this.messages = response.data.messages
                    for(var i = 0; i < response.data.users.length; i++) {
                        if(response.data.users[i].id === this.user) continue
                        this.usertags[response.data.users[i].id] = response.data.users[i].username
                        this.participants.push({label: response.data.users[i].username, key: response.data.users[i].id});
                    }
                    axios
                        .get('/api/v1/friends/?id=' + this.user)
                        .then(response => {
                            for(var i = 0; i < response.data.length; i++) {
                                if(response.data[i].id === this.user || this.usertags[response.data[i].id]) continue
                                this.add.push({label: response.data[i].username, key: response.data[i].id + "," + this.chat})
                            }
                        })
                        .catch(error => {
                            console.log(error)
                        })
                })
                .catch(error => {
                    console.log(error)
                })
        },
        sendMessage() {
            if(this.message === "") return;

            const formData = {
                text: this.message,
                user: this.user,
                chat: parseInt(this.chat),
            }
            axios
                .post('/api/v1/message/', formData)
                .then(response => {
                    this.updateMessages()
                })
                .catch(error => {

                })
            this.message = ""
        }
    },
}
</script>

<style lang="css" scoped>
.no-underline{
  text-decoration: none;
}
    .messages  {
        padding: 10px;
        padding-bottom: 0px;
        text-align: left;
        background-color: #F8F1F1;
        margin-bottom: 7px;
        margin-top: 5px;
        height: 85%;
        overflow-y:scroll;
    }

    .chat {
        padding-top:1px;
        text-align: center;
        background-color: #243964;
        margin: auto;
        margin-top: 20px;
        width: min(90%, 600px);
        height: 600px;
        border-radius: 10px;
    }

</style>