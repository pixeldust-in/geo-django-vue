<template>
  <div class="home">
    <div
      class="relative flex justify-center items-center mx-auto m-12"
      style="width: 800px; height: 500px"
    >
      <GMapAutocomplete
        placeholder="Search for place"
        @place_changed="setPlace"
        class="
          border border-black border-opacity-50
          w-full
          top-[-45px]
          left-0
          right-0
          px-8
          rounded
          py-2
          absolute
          z-10
        "
      >
      </GMapAutocomplete>
      <br />
      <br />
      <br />
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
    <div class="text-left mx-auto" style="width: 800px; height: 500px">
      <div v-for="(value, key) in cleanAddress" :key="key" v-show="value">
        {{ key }} : <strong> {{ value }}</strong>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineComponent, reactive, watch } from "vue";
import { GoogleMap, Marker } from "vue3-google-map";

const geoData = reactive({
  coords: null,
  locatedAt: null,
  error: null,
  resume: null,
  pause: null,
});
const center = reactive({ lat: 19.426954760386632, lng: 72.80847745404989 });
const cleanAddress = reactive({
  StreetNumber: null,
  StreetName: null,
  City: null,
  State: null,
  Zip: null,
  Country: null,
});
function placeToAddress(place: any) {
  var address: any = {};
  place.address_components.forEach(function (c: any) {
    switch (c.types[0]) {
      case "street_number":
        address.StreetNumber = c;
        break;
      case "route":
        address.StreetName = c;
        break;
      case "neighborhood":
      case "locality": // North Hollywood or Los Angeles?
        address.City = c;
        break;
      case "administrative_area_level_1": //  Note some countries don't have states
        address.State = c;
        break;
      case "postal_code":
        address.Zip = c;
        break;
      case "country":
        address.Country = c;
        break;
    }
  });
  return address;
}
function setPlace(data) {
  console.log(data);
  center.lat = data.geometry.location.lat();
  center.lng = data.geometry.location.lng();
  Object.keys(placeToAddress(data)).forEach((key) => {
    cleanAddress[key] = placeToAddress(data)[key].long_name;
  });
}
</script>
