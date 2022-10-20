<template>
  <NavBar v-bind:parks="parks" @changePark="navChangePark" @changeView="navChangeView"/>
  <img v-if="chosenPark==''" src="./assets/rollercoaster-clock.png"/>
  <RideList v-if="chosenView=='List'" v-bind:parkData="parkData"/>
  <RideMap v-if="chosenView=='Map'"  v-bind:parkData="parkData"/>
</template>

<script>
import NavBar from './components/NavBar.vue'
import RideList from './components/RideList.vue'
import RideMap from './components/RideMap.vue'

export default {
  name: 'ThemeParkWaitTimes',
  components: {
    NavBar,
    RideList,
    RideMap
  },
  data () {
    return {
      parks: [{id:1, name:'Disneyland'},{id:2, name:'Universal Orlando'}],
      chosenPark: "",
      chosenView: "List",
      parkData: {name: "", rides: []}
    }
  },
  methods: {
    navChangePark(parkName){
      this.chosenPark = parkName
      //Get park data from api and pass to children !!DUMMY DATA!!
      if(parkName == "Disneyland"){
        this.parkData = {name: parkName, rides: 
        [
          {name:'Splash Mountain',favorite:true,picture:"./assets/rollercoaster-clock.png",waitTime:10,estWaitTime:15,futureWaitTimes:[15,12,42]},
          {name:"Peter Pan",favorite:false,picture:"./assets/rollercoaster-clock.png",waitTime:35,estWaitTime:60,futureWaitTimes:[45,52,42,67]}]}
      }
      if(parkName == "Universal Orlando"){
        this.parkData = {name: parkName, rides: 
        [
          {name:'Transformers',favorite:false,picture:"./assets/rollercoaster-clock.png",waitTime:10,estWaitTime:15,futureWaitTimes:[15,12,42]},
          {name:"Harry Potter",favorite:true,picture:"./assets/rollercoaster-clock.png",waitTime:40,estWaitTime:40,futureWaitTimes:[35,32,62,54]}]}
      }
      
    },
    navChangeView(view) {
      this.chosenView = view
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
