<template>
    <div class="chat">
        <div style="width: 100%; text-align: left; margin: 10px;">
            <RouterLink style="margin-top: 10px;" class="no-underline" id="about" to="/"><n-button size="tiny" type="info" id="about-button">Back</n-button></RouterLink>
        </div>
        <div class="messages">
            <div v-for="message in messages" >
                <div v-if="message.user != user">
                <a style="font-size: 12px;">{{ usertags[message.user] }}</a>
                    <div style="background-color: #2080F0; color: white; padding: 4px; width: fit-content; border-radius: 7px; margin-bottom: 5px;">
                {{ message.text }}
                    </div>
                </div>
                <div v-else style="">
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

export default {
    name: 'Chat',
    data() {
        return {
            messages: [],
            message: '',
            usertags: {},
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
            })
            .catch(error => {
                this.$store.commit('removeToken')
                delete axios.defaults.headers.common["Authorization"]
                localStorage.removeItem("token")
            })
        this.chat = this.$route.query.id 
        axios
            .get('/api/v1/message?chat_id=' + this.chat)
            .then(response => {
                this.messages = response.data.messages
                for(var i = 0; i < response.data.users.length; i++)
                    this.usertags[response.data.users[i].id] = response.data.users[i].username
            })
            .catch(error => {
                console.log(error)
            })
    },
    methods: {
        updateMessages() {
            axios
                .get('/api/v1/message?chat_id=' + this.chat)
                .then(response => {
                    this.messages = response.data.messages
                    for(var i = 0; i < response.data.users.length; i++)
                        this.usertags[response.data.users[i].id] = response.data.users[i].username
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