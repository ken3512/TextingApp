<template>
<div class="chat">
        <div style="width: 100%; text-align: left; margin: 10px;">
            <RouterLink style="margin-top: 10px;" class="no-underline" id="about" to="/"><n-button size="tiny" type="info" id="about-button">Back</n-button></RouterLink>
        </div>
        <div class="users">
            <h3 v-if="friends.length > 0">Friends:</h3>
            <p v-for="f in friends">
                {{ f.username }}
                <!-- <n-button style="display: inline; float: right; margin-left: 2px;" size="tiny" type="error" @:click="deleteRequest(f.id)">Unfriend</n-button> -->
                <n-popconfirm :negative-text="null" @positive-click="deleteRequest(f.id)">
                <template #trigger>
                    <n-button style="display: inline; float: right; margin-left: 2px;" size="tiny" type="error">Unfriend</n-button>
                </template>
                Are you sure you want to unfriend {{ f.username }}?
                </n-popconfirm>
            </p>
            <h3 v-if="users.length > 0">Make a friend:</h3>
            <p v-for="u in users">
                {{ u.username }}
                    <n-button style="display: inline; float: right;" size="tiny" type="info" @:click="addFriend(u.id)">Friend</n-button>
            </p>
            <h3 v-if="requested.length > 0">Sent to you:</h3>
            <p v-for="r in requested">
                {{ r.username }}
                    <n-button style="display: inline; float: right; margin-left: 2px;" size="tiny" type="error" @:click="deleteRequest(r.id)">Delete</n-button>
                    <n-button style="display: inline; float: right;" size="tiny" type="primary" @:click="confirmRequest(r.id)">Confirm</n-button>
            </p>
            <h3 v-if="sent.length > 0" >Pending Requests:</h3>
            <p v-for="s in sent">
                {{ s.username }}
                    <a style="display: inline; float: right;" type="info">Pending</a>
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
            sent: [],
            friends: [],
            requested: [],
        }
    },
    methods: {
        deleteRequest(id) {
            const data = {
                user_to: this.user,
                user_from: id,
            }

            axios
                .post('/api/v1/delete/', data)
                .then(response => {
                    this.updateUsers()
                    console.log(response)
                })
                .catch(error => {

                })
        },
        confirmRequest(id) {
            const data = {
                user_to: this.user,
                user_from: id,
            }

            axios
                .post('/api/v1/confirm/', data)
                .then(response => {
                    this.updateUsers()
                })
                .catch(error => {

                })
        },
        updateUsers()
        {
            axios
                .get('/api/v1/friends?id=' + this.user)
                .then(response => {
                    this.friends = response.data
                })
                .catch(error => {
                    console.log(error)
                })
            axios
                .get('/api/v1/all?id=' + this.user)
                .then(response => {
                    this.users = response.data
                })
                .catch(error => {
                    console.log(error)
                })
            axios
                .get('/api/v1/pending/sent?id=' + this.user)
                .then(response => {
                    this.sent = response.data
                })
                .catch(error => {
                    console.log(error)
                })
            axios
                .get('/api/v1/pending/requested?id=' + this.user)
                .then(response => {
                    this.requested = response.data
                })
                .catch(error => {
                    console.log(error)
                })
        },
        addFriend(id) {
            const data = {
                user_from: this.user,
                user_to: id,
            }

            axios
                .post('/api/v1/friend/', data)
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
                this.updateUsers()
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