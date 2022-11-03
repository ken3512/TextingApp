<template>
    <div class="sign-up">
        <h1>Signup</h1>
        <form @submit.prevent="submitForm">
            <input type='email' name='username' v-model="username" required>
            <input type='password' name='password' v-model="password" required>
            <input type='password' name='re_password' v-model="re_password" required>
            <button type="submit">Sign up</button>
        </form>
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
                        console.log(response)
                    })
                    .catch(error => {
                        console.log(error.response.data.password)
                    })
            } else {
                console.log("Password fields must match.")
            }
        }
    }
}
</script>





