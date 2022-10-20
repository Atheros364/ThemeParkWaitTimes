<template>
    <div>
        <RideCard v-for="ride in parkData.rides.filter(ride => ride.favorite == true)" :rideData="ride" :key="ride.name"></RideCard>
        <RideCard v-for="ride in parkData.rides.filter(ride => ride.favorite == false)" :rideData="ride" :key="ride.name"></RideCard>
    </div>
</template>

<script>
import RideCard from './RideCard.vue'

export default {
    components: { 
        RideCard
    },
    props: ["parkData"],
    data() {
        return {};
    },
    methods: {}
}
</script>

<style>

</style>