<template>
<div class="chat">
        <div style="width: 100%; text-align: left; margin: 10px;">
            <RouterLink style="margin-top: 10px;" class="no-underline" id="about" to="/"><n-button size="tiny" type="info" id="about-button">Back</n-button></RouterLink>
        </div>
        <div class="add">
            <n-input v-model:value="title" style="text-align: left;" type="text" placeholder="Title" />
            <n-space vertical>
                <n-select
                v-model:value="participants"
                multiple
                :options="options"
                clearable
                />
            </n-space>
            <n-button style="margin-top: 10px;" size="large" @:click="createChat()" type="info">Create chat</n-button>

        </div>
        <br>
    </div>
    <br>
</template>

<script>
import axios from 'axios'

export default {
    name: 'AddChat',
    data() {
        return {
            title: '',
            participants: [],
            options: [],
            user: -1,
        }
    },
    methods: {
        createChat()
        {
            this.participants.push(this.user)
            var formData = {
                title: this.title,
                participants: this.participants,
            }
            axios
                .post('/api/v1/chat/', formData)
                .then(response => {
                    this.$router.push('/')
                })
                .catch(error => {
                    console.log(error)
                })
        }
    },
    mounted() {
         axios
            .get('/api/v1/users/me')
            .then(response => {
                this.user = response.data.id
                axios
                    .get('/api/v1/friends/?id=' + this.user)
                    .then(response => {
                        for(var i = 0; i < response.data.length; i++) {
                            if(response.data[i].id === this.user) continue
                                this.options.push({label: response.data[i].username, value: response.data[i].id})
                        }
                    })
                    .catch(error => {
                        console.log(error)
                    })
            })
            .catch(error => {
                this.$store.commit('removeToken')
                delete axios.defaults.headers.common["Authorization"]
                localStorage.removeItem("token")
            })
    },
}
</script>

<style lang="css" scoped>
    .add  {
        padding: 10px;
        padding-bottom: 0px;
        text-align: left;
        background-color: #F8F1F1;
        margin-bottom: 7px;
        margin-top: 5px;
        height: 290px;
        border-radius: 5px;
        overflow-y:scroll;
    }

    .chat {
        padding: 5px;
        text-align: center;
        background-color: #243964;
        margin: auto;
        margin-top: 20px;
        width: 92%;
        height: 380px;
        border-radius: 10px;
    }

</style>