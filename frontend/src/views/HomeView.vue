<template>
  <div class="home">
    <!-- <button @click="getLocation">Get Location</button>
    <pre v-if="geoData.coords">
      latitude: {{ geoData.coords.latitude }}
      longitude: {{ geoData.coords.longitude }}
      accuracy: {{ geoData.coords.accuracy }}
      altitude: {{ geoData.coords.altitude }}
      altitudeAccuracy: {{ geoData.coords.altitudeAccuracy }}
      heading: {{ geoData.coords.heading }}
      speed: {{ geoData.coords.speed }}
    </pre>
    <br>
    <br>
    {{ center }}
    <br> -->
    <!-- <GoogleMap :key="`${center.lat}-${center.lng}`" api-key="AIzaSyCcX-UvqSA_VwA1SNm9VfAcVj38RmG9QlI" style="width: 100%; height: 500px" :center="center" :zoom="15">
      <Marker :options="{ position: center }" />
    </GoogleMap> -->
    <div class="relative flex justify-center items-center mx-auto m-12" style="width: 800px; height: 500px">
    <GMapAutocomplete
      placeholder="Search for place"
      @place_changed="setPlace"
      class="border border-black border-opacity-50 w-full top-[-45px] left-0 right-0  px-8 rounded py-2 absolute z-10"
    >
    </GMapAutocomplete>
    <br/>
    <br/>
    <br/>
    <div>
    <GMapMap
      :center="center"
      :zoom="15"
      map-type-id="terrain"
      style="width: 800px; height: 500px"
    >
      <GMapMarker :position="center" />
    </GMapMap>
  </div>
  </div>
  </div>
</template>

<script setup lang="ts">
import { defineComponent, reactive, watch } from "vue";
import { useGeolocation } from "@vueuse/core";
import { GoogleMap, Marker } from "vue3-google-map";

const geoData = reactive({
  coords: null,
  locatedAt: null,
  error: null,
  resume: null,
  pause: null,
});
const center = reactive({ lat: 19.426954760386632, lng: 72.80847745404989 });
function setPlace(data) {console.log(data); center.lat = data.geometry.location.lat(); center.lng = data.geometry.location.lng();}

// const getLocation = () => {
//   const { coords, locatedAt, error, resume, pause } = useGeolocation()

//   Object.assign(geoData, { coords, locatedAt, error, resume, pause })
// }

// watch(geoData, (val) => {
//   console.log(val.coords)
//   if(val.error?.code === 1){
//     alert('Please allow location access to continue!')
//   }
//   if(val.coords){
//     console.log(val.coords.latitude)
//     center.lat = val.coords?.latitude
//     center.lng = val.coords?.longitude
//   }
// })
</script>
