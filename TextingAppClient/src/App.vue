<script setup>
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <header>
    <div class="wrapper">
      <nav v-if="!this.$store.state.isAuthenticated">
        <RouterLink to="/signup">Sign up</RouterLink>
        <RouterLink to="/login">Log in</RouterLink>
      </nav>
      <button v-else @:click="logout()">Login out</button>
    </div>
  </header>

  <RouterView />
</template>



<script>
import axios from 'axios'

export default {
  name: 'App',
  mounted()
  {
    if (localStorage.getItem("token") !== null) {
      const token = localStorage.getItem("token")
      this.$store.commit('setToken', token)
      axios.defaults.headers.common['Authorization'] = "Token " + token
      axios
        .get('/api/v1/users/me')
        .then(response => {
            console.log(response.data)
        })
        .catch(error => {
            this.$store.commit('removeToken')
            delete axios.defaults.headers.common["Authorization"]
            localStorage.removeItem("token")
        })
    }
  },
  methods: {
    logout() {
      console.log(this.$store.state.isAuthenticated)
        axios
          .post('/api/v1/token/logout')
          .then(response => {
              this.$store.commit('removeToken')
              delete axios.defaults.headers.common["Authorization"]
              localStorage.removeItem("token")
              console.log(response)
          })
          .catch(error => {
              console.log(error)
          })
    }
  }
}
</script>


<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>
