<template>
    <div class="sign-up">
        <h1>Signup</h1>
        <form @submit.prevent="submitForm">
            <input  placeholder="Enter Email" type='email' name='username' v-model="username" required>
            <input  placeholder="Enter Password" type='password' name='password' v-model="password" required>
            <input  placeholder="Repeat Password" type='password' name='re_password' v-model="re_password" required>
            <button type="submit">Sign up</button>
        </form>
        <p v-for="message in messages">
            {{ message }}
        </p>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'Signup',
    data() {
        return {
            username: '',
            password: '',
            re_password: '',
            messages: [],
        }
    },
    methods: {
        submitForm(e) {
            const formData = {
                username: this.username,
                password: this.password,
                re_password: this.re_password,
            }
            
            if (formData.password === formData.re_password) {
                axios
                    .post('/api/v1/users/', formData)
                    .then(response => {
                        this.$router.push('/login')
                    })
                    .catch(error => {
                        for (const [k, v] of Object.entries(error.response.data)) {
                            for (let i = 0; i < v.length; i++) {
                                this.messages.push(v[i])
                            }
                        }
                    })
            } else {
                console.log("Password fields must match.")
            }
        }
    }
}
</script>





