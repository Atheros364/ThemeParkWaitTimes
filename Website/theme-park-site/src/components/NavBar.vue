<template>
    <ul>
        <li class="dropdown-li">
            <div class="dropdown">
                <button @click="showParks" class="park-dropdown-btn">{{parkName}}</button>
                <div v-show="parksToggle" class="park-dropdown">
                    <a href="#" @click="changePark(park.name)" class="park-dropdown-item" v-for="park in parks" :key="park.id">
                        {{park.name}}
                    </a>
                </div>
            </div>
        </li>
        <li class="view-toggle-li">
            <button @click="toggleView" class="view-btn">{{chosenView}}</button>
        </li>
    </ul>
</template>

<script>
export default {
    props: ['parks'],
    data () {
        return {
            parksToggle: false,
            parkName: 'Choose a park',
            chosenPark: 'none',
            chosenView: 'Map'
        }
    },
    methods: {
        showParks() {
            this.parksToggle = !this.parksToggle
        },
        changePark(name) {
            this.$emit('changePark',name)
            this.parkName = name
            this.parksToggle = false
        },
        toggleView() {
            this.$emit('changeView',this.chosenView)
            if (this.chosenView === 'Map'){
                this.chosenView = 'List'
            }
            else{
                this.chosenView = 'Map'
            }
        }
    }
    
}
</script>

<style>
ul {
    list-style-type: none;
    margin: 0;
    padding: 0;
    background-color: #333;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
}

.dropdown-li {
    float: left;
}

.dropdown {
    float: left;
    position: relative;
}

.park-dropdown-btn {
    background-color: #1B3262;
    color: white;
    padding: 16px;
    font-size: 16px;
    border: none;
    cursor: pointer;
}

.park-dropdown {
    display: block;
    position: absolute;
    min-width: 160px;
    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
    z-index: 1;
    background-color: #333;
}

.park-dropdown-item {
    color: white;
    font-size: larger;
    display: block;
    text-decoration: none;
}

.view-toggle-li {
    float: right;
}

.view-btn {
    background-color: #1B3262;
    color: white;
    padding: 16px;
    font-size: 16px;
    border: none;
    cursor: pointer;
    width: 80px;
}
</style>