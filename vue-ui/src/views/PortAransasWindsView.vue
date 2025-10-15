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
const FRONTEND_HOST_PORT = import.meta.env.FRONTEND_HOST_PORT
let updateInterval = null

// get the api data and build the chart 
function getAPIData (apiUrls) {
  // fetch data from all APIs
  Promise.all(
    apiUrls.map((apiUrl) =>
      fetch(apiUrl).then((response) => response.json())
    )
  )
  .then((apiData) => {
    // format data from each API
    const formattedData = apiData.map((data, i) => {
      // extract the column names from the keys of the first element
      const columnNames = Object.keys(data[0]).filter(
        (column) => column !== "date"
      );
      
      // find the index of the date column
      const dateColumnIndex = Object.keys(data[0].indexOf("date"))

      // format data for all APIs
      const formattedData = data.map((d) => {
        const values = Object.values(d)
        .filter((column, index) => index !== dateColumnIndex)
        .map((value) => parseFloat(value));
        return [new Date(d.date).getTime(), ...values];
      });

      // map over formattedData and create an array of objects with the date and the values for each column
      const seriesData = formattedData.map((row) => {
        const data = {};
        data["date"] = row[0];
        columnNames.forEach((name, index) => {
          data[name] = row[index + 1];
        });
        return data;
      });

      // create Highcharts series
      return columnNames.map((name) => {
        return {
          name: name,
          data: seriesData.map((d) => [d.date, d[name]]),
          dashStyle: i === 0 ? "Solid" : "Dash"
        }
      })
    }); // end formattedData map

    Highcharts.setOptions({
      time: { useUTC: false, timezone: "America/Chicago" },
      lang: { shortWeekday: [ "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat" ] }
    });

    Highcharts.chart("container", {
      chart: { zoomType: "x", panKey: "alt" },
      title: { 
        text: "Wind Speed Measurements and Predictions Over the Past Week",
        style: { fontSize: "170%" }
      },
      xAxis: {
        type: "datetime",
        dateTimeLabelFormats: { day: "%a %b %e" },
        title: { text: "Time (CDT)", style: { fontSize: "150% "} },
        plotLines: [{
          // mark now
          enablePolling: true,
          color: "red",
          width: 2,
          value: Date.now(),
          dashStyle: "Solid",
          label: { text: "Now", color: "red" }
        }],
        labels: {
          padding: 25,
          style: { fontSize: "130%", color:"black" }
        }
      },
      yAxis: {
         title: {
           text: "Wind Speed (mph)",
           style: { fontSize: "150%" }
          }
      },
      colors: ["black", "grey", "orangered", "orange"],
      series: [...formattedData.flat()]
    }); // end Highcharts.chart

  }) // end Promise.all
  .catch((error) => console.error(error));

} // end getAPIData

onMounted(() => {
  // on mount, build the chart and fetch data
  getAPIData([
        `${FRONTEND_HOST_PORT}/sailwind/api/ndbc/measurements/file_format=json/data_type=std/station_id=PTAT2/product=WSPD/units=mph/last45days`,
        `${FRONTEND_HOST_PORT}/sailwind/api/nwps/predictions/wind/file_format=json/location=hcp/cg=cg1/units=mph`,
  ])

  // set the interval update every 10 minutes
  updateInterval = setInterval(() => {
    getAPIData([
      `${FRONTEND_HOST_PORT}/sailwind/api/ndbc/measurements/file_format=json/data_type=std/station_id=PTAT2/product=WSPD/units=mph/last45days`,
      `${FRONTEND_HOST_PORT}/sailwind/api/nwps/predictions/wind/file_format=json/location=hcp/cg=cg1/units=mph`,
    ])
  }, 600000);

}); // end onMounted

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
            Wind Speed Measurements and Predictions Over the Past Week
          </h1>
        </div>
      </div>
    </section>
    <MissingDataWarningBanner ref="missingDataWarningBanner" />
  </div>


  <!-- Chart Section -->
  <div class="container-fluid" style="background-color: white">
    <div id="container" class="chart"></div>
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
    </div>
    <p class="mt-4 text-sm text-gray-300">&copy; 2024 Flare. All rights reserved.</p>
  </footer>
</template>