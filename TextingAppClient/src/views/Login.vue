<template>

<div class="container">
	<div class="card">
		<form class="card-form" @submit.prevent="submitForm">
			<div class="input">
                <input class="input-field" type='text' name='username' v-model="username" required>
				<label class="input-label">Email</label>
			</div>
            <div class="input">
                <input  class="input-field" type='password' name='password' v-model="password" required>
				<label class="input-label">Password</label>
			</div>
			<div class="action">
				<button class="action-button" type="submit">Log in</button>
			</div>
		</form>
        <div class="messages">
            <p v-for="message in messages">
                {{ message }}
            </p>
        </div>
	</div>
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
                    this.$router.push('/')
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


<style lang="scss" scoped>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap');
*, *:after, *:before {
	box-sizing: border-box;
}

body {
	font-family: "DM Sans", sans-serif;
	line-height: 1.5;
	background-color: #f1f3fb;
	padding: 0 2rem;
}

img {
	max-width: 100%;
	display: block;
}


// iOS Reset 
input {
	appearance: none;
	border-radius: 0;
}

.card {
	margin: auto;
	display: flex;
	flex-direction: column;
	width: min(90%, 600px);
	max-width: 425px;
	border-radius: 10px;
    height: 570px;
    text-align: center;

}

.input {
	display: flex;
	flex-direction: column-reverse;
	position: relative;
	padding-top: 1.1rem;
	&+.input {
		margin-top: 1.5rem;
	}
}

.input-label {
	color: #243964;
	position: absolute;
	top: 1.5rem;
	transition: .25s ease;
}

.input-field {
	border: 0;
	z-index: 1;
	background-color: transparent;
	border-bottom: 2px solid #243964; 
	font: inherit;
	font-size: 1.125rem;
	padding: .25rem 0;
	&:focus, &:valid {
		outline: 0;
		border-bottom-color: #243964;
		&+.input-label {
			color: #243964;
			transform: translateY(-1.5rem);
		}
	}
}

.action {
	margin-top: 2rem;
}

.action-button {
	font: inherit;
	font-size: 1rem;
	padding: 1em;
	width: 100%;
	font-weight: 500;
	background-color: #243964;
	border-radius: 6px;
	color: #FFF;
	border: 0;
	&:focus {
		outline: 0;
	}
}

.card-info {
	padding: 1rem 1rem;
	text-align: center;
	font-size: .875rem;
	color: #8597a3;
	a {
		display: block;
		color: #6658d3;
		text-decoration: none;
	}
}
</style>
