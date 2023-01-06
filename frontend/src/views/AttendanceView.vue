<template>
  <div class="w-[800px] mx-auto">
    <div class="text-left mb-12">
      <div class="mb-1">Today's Attendance:</div>
      <div class="mb-2" v-if="userAttedance.todayAttendance">
        Checked In @ {{ userAttedance?.todayAttendance?.check_in }}
        <div class="mb-2" v-if="userAttedance.todayAttendance?.formatted_address">
          Location: {{userAttedance.todayAttendance?.formatted_address}}
        </div>
        <div class="mb-2" v-if="userAttedance?.todayAttendance?.check_out">
          Checked out @ {{ userAttedance?.todayAttendance?.check_out }}
        </div>
        <button
        v-else
          class="
            bg-slate-900
            hover:bg-slate-700
            focus:outline-none
            focus:ring-2
            focus:ring-slate-400
            focus:ring-offset-2
            focus:ring-offset-slate-50
            text-white
            font-semibold
            h-12
            px-6
            rounded-lg
            w-full
            flex
            items-center
            justify-center
            sm:w-auto
            dark:bg-sky-500 dark:highlight-white/20 dark:hover:bg-sky-400
          "
          @click="checkOut"
        >
          Check Out for the day
        </button>
      </div>
      <div v-else>
        <button
          class="
            bg-slate-900
            hover:bg-slate-700
            focus:outline-none
            focus:ring-2
            focus:ring-slate-400
            focus:ring-offset-2
            focus:ring-offset-slate-50
            text-white
            font-semibold
            h-12
            px-6
            rounded-lg
            w-full
            flex
            items-center
            justify-center
            sm:w-auto
            dark:bg-sky-500 dark:highlight-white/20 dark:hover:bg-sky-400
          "
          @click="checkIn"
        >
          Check In for Today
        </button>
      </div>
    </div>
    <hr />
    <div class="text-lg font-bold">
      Attendance History:
      <hr />
  </div>
    <div class="flex items-center justify-center">

      <div class="overflow-x-auto w-full">
        <table class="min-w-full">
          <thead class="border-b">
            <tr>
              <th
                scope="col"
                class="text-sm font-medium text-gray-900 px-6 py-4 text-left"
              >
                #
              </th>
              <th
                scope="col"
                class="text-sm font-medium text-gray-900 px-6 py-4 text-left"
              >
                Date
              </th>
              <th
                scope="col"
                class="text-sm font-medium text-gray-900 px-6 py-4 text-left"
              >
                Check In
              </th>
              <th
                scope="col"
                class="text-sm font-medium text-gray-900 px-6 py-4 text-left"
              >
                Checkout
              </th>
              <th
                scope="col"
                class="text-sm font-medium text-gray-900 px-6 py-4 text-left"
              >
                Location
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              class="border-b"
              v-for="(att, index) in userAttedance.attendanceHistory"
              :key="att.uuid"
            >
              <td
                class="
                  px-6
                  py-4
                  whitespace-nowrap
                  text-sm
                  font-medium
                  text-gray-900
                "
              >
                {{ index + 1 }}
              </td>
              <td
                class="
                  text-sm text-gray-900
                  font-light
                  px-6
                  py-4
                  whitespace-nowrap
                "
              >
                {{ att.date }}
              </td>
              <td
                class="
                  text-sm text-gray-900
                  font-light
                  px-6
                  py-4
                  whitespace-nowrap
                "
              >
                {{ att.check_in }}
              </td>
              <td
                class="
                  text-sm text-gray-900
                  font-light
                  px-6
                  py-4
                  whitespace-nowrap
                "
              >
                {{ att.check_out }}
              </td>
              <td
              class="
                text-sm text-gray-900
                font-light
                px-6
                py-4
                whitespace-nowrap
              "
            >
            {{ att.formatted_address }}
            </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
<script lang="ts" setup>
import { computed, onMounted, reactive, watch } from "vue";
import { useFetch } from "@vueuse/core";
import { useGeolocation } from "@vueuse/core";
import api from "../hooks/api";

const userAttedance = reactive({
  attendanceHistory: null,
  todayAttendance: null,
});

const attendanceFormData = {
  location: {
    type: "Point",
    coordinates: [],
  },
};

const getLocation = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else {
    alert("Geolocation is not supported by this browser.");
  }
};

async function postCheckIn() {
  const {data} = await api.post("user-attedance/", attendanceFormData);
  userAttedance.todayAttendance = data
}

function showPosition(position: GeolocationPosition) {
  const { coords } = position;
  attendanceFormData.location.coordinates = [
    coords?.latitude,
    coords?.longitude,
  ];
  postCheckIn();
}

function checkIn() {
  getLocation();
}

async function fetchToday() {
  const { data } = await api.get("user-attedance/today/");
  userAttedance.todayAttendance = data?.data;
}

async function checkOut() {
const { data } = await api.put(`user-attedance/${userAttedance.todayAttendance?.uuid}/`);
  userAttedance.todayAttendance.check_out = data?.check_out;
}

onMounted(async () => {
  const { data } = await api.get("user-attedance/");
  userAttedance.attendanceHistory = data;
  await fetchToday()
});
</script>
