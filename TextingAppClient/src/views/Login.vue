<template>
    <div class="login">
        <h1>Login</h1>
        <form @submit.prevent="submitForm">
            <input placeholder="Enter Email" type='email' name='username' v-model="username">
            <input placeholder="Enter Password" type='password' name='password' v-model="password">
            <button type="submit">Log in</button>
        </form>
        <p v-for="message in messages">
            {{ message }}
        </p>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'Login',
    data() {
        return {
            username: '',
            password: '',
            messages: [],
        }
    },
    methods: {
        submitForm(e) {
            this.messages = []
            const formData = {
                username: this.username,
                password: this.password,
            }
            
            axios
                .post('/api/v1/token/login', formData)
                .then(response => {
                    const token = response.data.auth_token
                    this.$store.commit('setToken', token)
                    axios.defaults.headers.common['Authorization'] = "Token " + token
                    localStorage.setItem("token", token)
                })
                .catch(error => {
                    for (const [k, v] of Object.entries(error.response.data)) {
                        for (let i = 0; i < v.length; i++) {
                            this.messages.push(v[i])
                        }
                    }
                })
        }
    }
}
</script>