<template>
<div class="chat">
        <div style="width: 100%; text-align: left; margin: 10px;">
            <RouterLink style="margin-top: 10px;" class="no-underline" id="about" to="/"><n-button size="tiny" type="info" id="about-button">Back</n-button></RouterLink>
        </div>
        <div class="users">
            <p v-for="u in users">
                {{ u.username }}
                    <n-button style="display: inline; float: right;" size="tiny" type="info" id="about-button" @:click="addFriend(u.id)">Friend</n-button>
            </p>
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
            user: -1,
            users:[],
        }
    },
    methods: {
        updateUsers()
        {
            axios
                .get('/api/v1/all?id=' + this.user)
                .then(response => {
                    this.users = response.data
                })
                .catch(error => {
                    console.log(error)
                })
        },
        addFriend(id) {
            const formData = {
                user_from: this.user,
                user_to: id,
            }

            axios
                .post('/api/v1/friend/', formData)
                .then(response => {
                    this.updateUsers()
                })
                .catch(error => {

                })
        }
    },
    mounted() {
         axios
            .get('/api/v1/users/me')
            .then(response => {
                this.user = response.data.id
                axios
                    .get('/api/v1/all?id=' + this.user)
                    .then(response => {
                        this.users = response.data
                    })
                    .catch(error => {
                        console.log(error)
                    })
            })
            .catch(error => {
                console.log(error)
            })
    },
}
</script>

<style lang="css" scoped>
    .users  {
        padding: 10px;
        padding-bottom: 0px;
        text-align: left;
        background-color: #F8F1F1;
        margin-bottom: 10px;
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