<template>
  <div class="home">
    <button @click="getLocation">Get Location</button>
    <pre v-if="geoData.coords">
      latitude: {{ geoData.coords.latitude }}
      longitude: {{ geoData.coords.longitude }}
      accuracy: {{ geoData.coords.accuracy }}
      altitude: {{ geoData.coords.altitude }}
      altitudeAccuracy: {{ geoData.coords.altitudeAccuracy }}
      heading: {{ geoData.coords.heading }}
      speed: {{ geoData.coords.speed }}
    </pre>
  </div>
</template>

<script setup lang="ts">
import { defineComponent, reactive, watch } from 'vue';
import { useGeolocation } from '@vueuse/core'

const geoData = reactive({
  coords: null,
  locatedAt: null,
  error: null,
  resume: null,
  pause: null,
})
const getLocation = () => {
  const { coords, locatedAt, error, resume, pause } = useGeolocation()

  Object.assign(geoData, { coords, locatedAt, error, resume, pause })
}

watch(geoData, (val) => {
  console.log(val.coords)
  if(val.error?.code === 1){
    alert('Please allow location access to continue!')
  }
})
</script>
