<!-- ===================================================
     View: PortAransasWinds.vue
     Description: This view displays the air temperature trends and predictions for South Bird Island.
                  Features include:
                  - A dynamically updating Highcharts line chart using live CSV data.
                  - Instructions for interacting with the chart.
                  - Information on the data of the chart.
                  - Additional links
                  - Informative sections about South Bird Island and its environmental significance.
     Author: Beto Estrada
     Created: 04/13/2023
     Last Updated: 10/14/2025 by Christian Quintero
======================================================= -->
<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import Highcharts from 'highcharts'
import Chart from 'highcharts-vue'
import Data from 'highcharts/modules/data'
import Exporting from 'highcharts/modules/exporting'
import ExportData from 'highcharts/modules/export-data'
import Accessibility from 'highcharts/modules/accessibility'
import MissingDataWarningBanner from "@/components/MissingDataWarningBanner.vue"

// template ref for the banner component
const missingDataWarningBanner = ref(null)

// env and reactive state
const HOST_URL = import.meta.env.HOST_URL || 'http://localhost:8000'
const chartOptions = ref({})
const state = reactive({ isSmallScreen: window.innerWidth <= 600 })

let updateInterval = null

// the URLs to fetch data from
const URLs = [
  `${HOST_URL}/sailwind/api/ndbc/measurements/file_format=json/data_type=std/station_id=PTAT2/product=WSPD/units=mph/last45days`,
  `${HOST_URL}/sailwind/api/nwps/predictions/wind/file_format=json/location=hcp/cg=cg1/units=mph`,
]

const buildChart = (isSmallScreen) => {
  return {
    chart: { zoomType: "x", panKey: "alt" },
    title: { text: "Wind Speed Measurements and Predictions Over the Past Week", style: { fontSize: "170%" } },
    xAxis: {
      type: "datetime",
      dateTimeLabelFormats: { day: "%a %b %e" },
      title: { text: "Time (CDT)", style: { fontSize: "150%" } },
      plotLines: [{ enablePolling: true, color: "red", width: 2, value: Date.now(), dashStyle: "Solid", label: { text: "Now", color: "red" } }],
      labels: { padding: 25, style: { fontSize: "130%", color: "black" } }
    },
    yAxis: { title: { text: "Wind Speed (mph)", style: { fontSize: "150%" } } },
    colors: ["black", "grey", "orangered", "orange"],
    series: []
  }
};

onMounted(() => {
  // on mount, build the chart 
  chartOptions.value = buildChart(state.isSmallScreen)

  // call banner check if the component ref is available
  if (missingDataWarningBanner.value && typeof missingDataWarningBanner.value.checkForMissingDataAndWarn === 'function') {
    missingDataWarningBanner.value.checkForMissingDataAndWarn(chartOptions.value)
  }

  // set the interval update every 10 minutes
  updateInterval = setInterval(() => {
    chartOptions.value = buildChart(state.isSmallScreen)
    if (missingDataWarningBanner.value && typeof missingDataWarningBanner.value.checkForMissingDataAndWarn === 'function') {
      missingDataWarningBanner.value.checkForMissingDataAndWarn(chartOptions.value)
    }
  }, 600000);
});

// on dismount clear the interval
onUnmounted(() => { clearInterval(updateInterval) });
</script>


<template>
  <div class="overflow-hidden bg-primary-bg text-dark-text font-main">
    <!-- Banner Section -->
    <section class="bg-banner-gradient-2 w-full text-white h-[300px] lg:h-[500px]">
      <!-- Overlay image on the left -->
      <div class="relative w-full h-full" >
        <img
          src="@/assets/images/clouds.jpg"
          alt="Map Overlay"
          class="w-full h-full object-cover flex opacity-30"
        />
        <!-- Text content overlay -->
        <div class="absolute  inset-0 flex items-center justify-center">
          <h1 class=" max-w-[1500px] text-lg md:text-3xl lg:text-5xl font-bold text-center pr-5 pl-5">
            Port Aransas Winds
          </h1>
        </div>
      </div>
    </section>
    <MissingDataWarningBanner ref="missingDataWarningBanner" />
  </div>



  <!-- Footer -->
  <footer class="bg-navy-blue py-6 text-center">
    <div class="flex justify-center gap-2 lg:gap-10">
      <a href="https://github.com/conrad-blucher-institute/semaphore" target="_blank" class="hover:scale-110 transition-transform">
        <img src="@/assets/images/Semaphore-Logo.png" alt="Semaphore Logo" class="pt-4 lg:pt-5 w-[100px] lg:w-[200px] lg:h-[200px]">
      </a>
      <a href="https://www.conradblucherinstitute.org/" target="_blank" class="hover:scale-110 transition-transform">
        <img src="@/assets/images/CBI-Logo.png" alt="Conrad Blutcher Institute Logo" class="w-[230px] h-[75px] pt-5 lg:pt-10 lg:w-[550px] lg:h-[150px]">
      </a>
      <a href="https://www.weathercompany.com/" target="_blank" class="hover:scale-110 transition-transform">
        <img src="@/assets/images/TWC-Logo.png" alt="The Weather Company Logo" class="w-[100px] h-[100px] lg:w-[200px] lg:h-[200px]">
      </a>
    </div>
    <p class="mt-4 text-sm text-gray-300">&copy; 2024 Flare. All rights reserved.</p>
  </footer>
</template>