<template>
    <div class="activate">
        <br>
            <h1>Thanks for registering!</h1>
            <h2>Your email has been succeffully verified.</h2>
            <h3>Login <RouterLink class="no-underline" id="about" to="/login">HERE</RouterLink> to start chatting!</h3>
        <br>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'Activate',
    data() {
        return {
        }
    },
    mounted()
    {
        let uid = this.$route.query.uid
        let token = this.$route.query.token

        console.log(uid)
        console.log(token)

        if(uid === undefined || token === undefined) {
            this.$router.push('/login')
        }

        const data = {
            uid: uid,
            token: token,
        }
        axios
        .post('/api/v1/users/activation/', data)
        .then(response => {
            console.log(response)
        })
        .catch(error => {
            console.log(error)
        })
    }
}
</script>


<style lang="css" scoped>
    .activate{
        text-align: center;
        background-color: #F8F1F1;
        margin: auto;
        margin-top: 20px;
        width: 90%;
        border-radius: 10px;
    }

</style>