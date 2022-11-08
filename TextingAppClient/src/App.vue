<script setup>
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
import $ from 'jquery'
</script>


<template>

  <header>
      <nav v-if="this.$route.path !== '/activate'">
        <h1 class="logo">
          TextingApp
        </h1>
        <div v-if="!this.$store.state.isAuthenticated" class="buttons">
          <input id="menu-toggle" type="checkbox"/>
          <label class='menu-button-container' for="menu-toggle">
            <div class='menu-button'></div>
          </label>
          <ul class="menu">
                <li><RouterLink class="no-underline" id="about" to="/signup"><n-button quaternary size="large" id="about-button">Sign up</n-button></RouterLink></li>
                <li><RouterLink class="no-underline" id="contact"  to="/login"><n-button quaternary size="large" id="contact-button">Login</n-button></RouterLink></li>
          </ul>
        </div>
        <div v-else class="buttons">
          <input id="menu-toggle" type="checkbox"/>
          <label class='menu-button-container' for="menu-toggle">
            <div class='menu-button'></div>
          </label>
          <ul class="menu">
                <li><RouterLink class="no-underline" id="contact"  to="/add_friend"><n-button quaternary size="large" id="contact-button">Add Friend</n-button></RouterLink></li>
              <li><n-button @:click="logout()" quaternary size="large" id="about-button">Log out</n-button></li>
          </ul>
        </div>
      </nav>
  </header>
  <RouterView />
</template>



<script>
import axios from 'axios'

export default {
  name: 'App',
  mounted()
  {
    // console.log(this.$cookies.get('csrftoken'))
    axios.defaults.headers['X-CSRFToken'] = this.$cookies.get('csrftoken')
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
        axios
          .post('/api/v1/token/logout')
          .then(response => {
              this.$store.commit('removeToken')
              delete axios.defaults.headers.common["Authorization"]
              localStorage.removeItem("token")
              this.$router.push('/login')
          })
          .catch(error => {
              console.log(error)
          })
    },
    get()
    {
      axios
          .get('/api/v1/message?chat_id=1')
          .then(response => {
              console.log(response)
          })
          .catch(error => {
              console.log(error)
          })
    }
  }
}
</script>

<style>
.no-underline{
  text-decoration: none;
}
</style>

<style lang="scss" scoped>
  @import url(https://fonts.googleapis.com/css?family=Raleway);
  .active-button{
    background-color: #E6E0E0;
    cursor: default;
  }
* {
  box-sizing: border-box;
}
.no-underline{
  text-decoration: none;
}
.menu {
  z-index:10;
  position:relative;
  display: flex;
  flex-direction: row;
  list-style-type: none;
  margin: 0;
  padding: 0;
}
.menu > li {
  margin: 0 0.1rem;
  overflow: hidden;
}
.menu-button-container {
  display: none;
  height: 100%;
  width: 30px;
  cursor: pointer;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
#menu-toggle {
  display: none;
}
.menu-button,
.menu-button::before,
.menu-button::after {
  display: block;
  background-color: #000000;
  position: absolute;
  height: 4px;
  width: 30px;
  transition: transform 400ms cubic-bezier(0.23, 1, 0.32, 1);
  border-radius: 2px;
}
.menu-button::before {
  content: '';
  margin-top: -8px;
}
.menu-button::after {
  content: '';
  margin-top: 8px;
}
#menu-toggle:checked + .menu-button-container .menu-button::before {
  margin-top: 0px;
  transform: rotate(405deg);
}
#menu-toggle:checked + .menu-button-container .menu-button {
  background: rgba(255, 255, 255, 0);
}
#menu-toggle:checked + .menu-button-container .menu-button::after {
  margin-top: 0px;
  transform: rotate(-405deg);
}
@media (max-width: 0px) {
  .menu-button-container {
    display: flex;
  }
  .menu {
    position: absolute;
    top: 0;
    margin-top: 68px;
    left: 0;
    flex-direction: column;
    width: 100%;
    justify-content: center;
    align-items: center;
  }
  #menu-toggle ~ .menu li {
    height: 0;
    margin: 0;
    padding: 0;
    border: 0;
    transition: height 400ms cubic-bezier(0.23, 1, 0.32, 1);
  }
  #menu-toggle:checked ~ .menu li {
    height: 3.5em;
    padding: 0.4em;
    transition: height 400ms cubic-bezier(0.23, 1, 0.32, 1);
  }
  #menu-toggle:checked ~ .menu .border {
    border-bottom: 1px solid #000;
  }
  .menu > li {
    display: flex;
    justify-content: center;
    margin: 0;
    padding: 0.5em 0;
    width: 100%;
    color: white;
    background-color: rgb(248,241,241);
  }
  .menu > li:not(:last-child) {
    border-bottom: 1px solid #444;
  }
}
  #about{
    text-decoration:none
  }
  #about-button{
    text-decoration:none
  }
  .icons{
    padding-top: 4px;
    padding-left: 9px;
  }
  .icon{
    width: 30px;
  }
  .logo {
    justify-content: left;
    padding-left: 30px;
  }
  
  nav{
    background: rgb(248,241,241);
    display: flex;
    width: 100%;
  }
  .buttons {
    justify-content: right;
    padding: 15px;
    display: flex;
    width: 100%;
  }
  .nav_element
  {
    margin-right: 10px;
    opacity: 1;
    color: black;
    text-decoration: none;
  }
</style>