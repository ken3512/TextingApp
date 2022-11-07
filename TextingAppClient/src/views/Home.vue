<template>
    <div class="home">
        <div v-for="chat in chats">
            <n-button @:click="get_chat(chat.id)" style="width:100%; margin-bottom: 10px;" size="large" id="about-button">{{ chat.title }}</n-button>
        </div>
        <RouterLink class="no-underline" id="contact"  to="/add"><n-button style="width:100%; margin-bottom: 10px;" size="large" id="about-button">+</n-button></RouterLink>
    </div>
    <br>
</template>

<script>
import axios from 'axios'

export default {
    name: 'Home',
    data() {
        return {
            chats: [],
        }
    },
    methods: {
        get_chat(chat_id) {
            console.log(chat_id)
            this.$router.push('/chat?id=' + chat_id)
        }
    },
    mounted() {
        if (localStorage.getItem("token") !== null) {
            const token = localStorage.getItem("token")
            this.$store.commit('setToken', token)
            axios.defaults.headers.common['Authorization'] = "Token " + token
            axios
                .get('/api/v1/users/me')
                .then(response => {
                    axios
                        .get('/api/v1/chat?user_id=' + response.data.id)
                        .then(res => {
                            this.chats = res.data
                        })
                        .catch(err => {
                            console.log(err)
                        })
                })
                .catch(error => {
                    this.$store.commit('removeToken')
                    delete axios.defaults.headers.common["Authorization"]
                    localStorage.removeItem("token")
                })
        }
    },
}
</script>

<style lang="css" scoped>
.home{
        text-align: center;
        background-color: #F8F1F1;
        margin: auto;
        margin-top: 20px;
        width: min(90%, 600px);
        height: 500px;
        border-radius: 10px;
        overflow-y:scroll;
    }

</style>