<!-- ===================================================
     View: SouthBirdIslandChartView.vue
     Description: This view displays the air temperature trends and predictions for South Bird Island.
                  Features include:
                  - A dynamically updating Highcharts line chart using live CSV data.
                  - Instructions for interacting with the chart.
                  - Information on the data of the chart.
                  - Additional links
                  - Informative sections about South Bird Island and its environmental significance.
     Author: Anointiyae Beasley
     Date: 01/05/2025
======================================================= -->
<script setup>
import Highcharts from "highcharts";
import { Chart } from "highcharts-vue";

import { ref, onMounted, onUnmounted, reactive } from "vue";

// Using reactive state to track if the screen is small
const state = reactive({
  isSmallScreen: window.innerWidth <= 600
});

const csvURL = ref(`${window.location.origin}/flare/csv-data/Laguna-Madre_Water-Level_Air-Temperature_120hrs.csv`);

// Add reactive state for dropdown visibility
const isExportMenuVisible = ref(false);
const userTimeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;
console.log("User's Time Zone:", userTimeZone);


// Define the current date and time
const nowDate = new Date();// Current timestamp
const nowTime = nowDate.getTime();

const chartOptions = ref({});

// Creating a single chart function that changes based on screen size
const buildChart = (isSmallScreen) => {
  return {
    chart: {
      type: "line",
      zoomType: "x",
      backgroundColor: "white",
      style: { fontFamily: "Arial" },
      marginRight: 30
    },
    title: {
      text: "Temperatures of the Upper Laguna Madre",
      style: { 
        fontSize: isSmallScreen ? "20px" : "28px", 
        fontWeight: "bold", 
        color: "#0f4f66" 
      },
    },
    exporting: {
    enabled: true, // Enables the export menu
  },
    legend: {
      itemStyle: {
        fontSize: isSmallScreen ? "12px" : "19px",
        fontWeight: "bold",
        fontFamily: "Arial",
        color: "#0f4f66",
      },
    },
    xAxis: {
      type: "datetime",
      dateTimeLabelFormats: {
        day: "%a %b %e",
      },
      labels: {
        formatter: function () {
          const localDate = new Date(this.value);
          const day = localDate.toLocaleDateString("en-US", { weekday: "short" }); 
          const date = localDate.toLocaleDateString("en-US", { month: "short", day: "numeric" });
          const time = localDate.toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit", hour12: true }); 
          return `<span style="display: block; text-align: center; font-family: Arial;">
                    <b>${day}</b><br>${date}<br><i>${time}</i>
                  </span>`;
        },
        useHTML: true,
        style: {
          fontSize: isSmallScreen ? "12px" : "16px", 
          fontFamily: "Arial",
          color: "#0f4f66",
          whiteSpace: "nowrap",
        },
      },
      labelsOverflow: "justify", // Prevent truncation
      maxPadding: 0.1, // Reduce extra space around labels
      minPadding: 0.1,
      tickInterval: 2 * 24 * 3600 * 1000, // Main ticks every 2 days
      minorTickInterval: 24 * 3600 * 1000, // Minor ticks every day
      minorTickWidth: 1, // Width of the minor tick lines
      minorTickLength: 5, // Length of the minor tick lines
      minorTickColor: "#888", // Color of the minor ticks
      // Ensure ticks align to 12 AM
      tickPositioner: function () {
        let positions = [];
        let timezoneOffset = new Date().getTimezoneOffset() * 60 * 1000;
        let start = Math.floor((this.min - timezoneOffset) / (24 * 3600 * 1000)) * (24 * 3600 * 1000) + timezoneOffset;
        let end = this.max;
        
        while (start <= end) {
          positions.push(start);
          start += 2 * 24 * 3600 * 1000; // Increment by 2 days
        }
        return positions;
      },
      title: {
        text: "Time",
        style: {
          fontSize: isSmallScreen ? "14px" : "20px",
          fontFamily: "Arial",
          color: "#0f4f66",
        },
      },
      plotLines: [
        {
          color: "red",
          width: 2,
          value: nowTime,
          dashStyle: "Solid",
          label: {
            text: "Now",
            y:20,
            style: {
              color: "#0f4f66",
              fontSize: isSmallScreen ? "12px" : "14px", 
              fontFamily: "Arial",
            },
          },
        },
      ],
      events: {
        afterSetExtremes: function () {
          const xAxis = this;
          const timezoneOffset = new Date().getTimezoneOffset() * 60 * 1000; // Ensure local time alignment
          const min = Math.floor((xAxis.min - timezoneOffset) / (24 * 3600 * 1000)) * (24 * 3600 * 1000) + timezoneOffset + (24 * 3600 * 1000);
          const max = xAxis.max;
          const plotLines = [];

          
          for (let time = min; time <= max; time += 2 * 24 * 3600 * 1000) {
            plotLines.push({
              color: "gray",
              dashStyle: "Dot",
              width: 1,
              value: time,
              label: {
                text: (() => {
                const localDate = new Date(time);
                const options = { weekday: "short", month: "short", day: "numeric" }; 
                return localDate.toLocaleDateString("en-US", options); 
              })(),
                align: "left",
                rotation: 0,
                y: 15, 
                style: {
                  color: "#0f4f66",
                  fontSize: isSmallScreen ? "10px" : "12px", 
                  fontFamily: "Arial",
                },
              },
            });
          }

          // Add the new plotlines dynamically
          plotLines.forEach((line) => xAxis.addPlotLine(line));
        },
      },
    },
    yAxis: {
      labels: {
          style: {
            fontSize: isSmallScreen ? "12px" : "26px",
            color: '#0f4f66',
            fontFamily: 'Arial', 
          },
        },
      title: {
        text: "Temperature (°F)",
        style: { 
          color: "#0f4f66", 
          fontSize: isSmallScreen ? "12px" : "20px", 
        },
      },
      max: maxDataValue > 90 ? 100 : 90, // if the max data value is greater than 90, set max to 100, else set to 90
      min: 20,
      tickInterval: 10, // Add ticks every 10 units
      plotLines: [
        {
          color: "red",
          width: 2,
          value: 46.4,
          dashStyle: "Dash",
          label: {
            text: "Sea Turtle Water Temperature Threshold",
            style: {
              color: "#0f4f66",
              fontSize: isSmallScreen ? "12px" : "16px",
              fontWeight: "bold",
            },
          },
        },
        {
          color: "#720000",
          width: 2,
          value: 40,
          dashStyle: "Dash",
          label: {
            text: "Fisheries Water Temperature Threshold",
            style: {
              color: "#0f4f66",
              fontSize: isSmallScreen ? "12px" : "16px",
              fontFamily: "Arial",
              fontWeight: "bold",
            },
          },
        },
      ],
    },
    series: [], // Placeholder for dynamically updated data
    tooltip: {
      shared: false,
      crosshairs: true,
      formatter: function () {
        const localDate = new Date(this.x); 
        return `<b>Date: ${localDate.toLocaleDateString("en-US", {
                    weekday: "long",
                    month: "short",
                    day: "numeric",
                    year: "numeric",
                })}</b><br>
                <b>Time: ${localDate.toLocaleTimeString("en-US", {
                    hour: "2-digit",
                    minute: "2-digit",
                })}</b><br>
                Temperature: ${this.y.toFixed(2)}°F`;
      },
      style: {
        fontSize: isSmallScreen ? "12px" : "14px", 
        padding: isSmallScreen ? "5px" : "8px", 
        color: "#0f4f66",
        fontFamily: "Arial",
      },
    },
  };
};


const handleResize = () => {
  state.isSmallScreen = window.innerWidth <= 600;
  chartOptions.value = buildChart(state.isSmallScreen);
}

// Setting chartOptions based on the returned screensize
chartOptions.value = buildChart(state.isSmallScreen);

// Function to fetch and process CSV data
const fetchAndFilterData = async () => {
  try {
    const response = await fetch(csvURL.value);
    if (!response.ok) throw new Error("Failed to fetch CSV data");

    const csvText = await response.text();
    console.log("UPDATED CSV Data:", csvText);

    const parsedData = parseCSV(csvText);
    console.log("Parsed CSV Data:", parsedData);

    // Ensure parsed arrays are initialized
    const WaterMeasurementData = parsedData.waterMeasurements || [];
    const AirMeasurementData = parsedData.airMeasurements || [];
    const InterpolatedAirPredictionData = parsedData.airPredictions || [];
    const InterpolatedWaterPredictionData = parsedData.waterPredictions || [];

     // Filter `InterpolatedAirPrediction` to only include hourly data
     const hoursToFilter = [3, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84, 90, 102, 114, 120];
    const AirPredictionData = InterpolatedAirPredictionData.filter((point) => {
      const pointTime = new Date(point[0]);
      const hoursDifference = Math.round((pointTime - nowTime) / (1000 * 60 * 60)); // Calculate hours difference
      return hoursToFilter.includes(hoursDifference);
    });

    // Filter `InterpolatedWaterPrediction` for specific intervals
    const WaterPredictionData = InterpolatedWaterPredictionData.filter((point) => {
      const pointTime = new Date(point[0]);
      const hoursDifference = Math.round((pointTime - nowTime) / (1000 * 60 * 60)); // Calculate hours difference
      return hoursToFilter.includes(hoursDifference);
    });

    // Convert all data to Fahrenheit
    const AirMeasurementDataFahrenheit = AirMeasurementData.map(([time, celsius]) => [
      time,
      (celsius * 9) / 5 + 32,
    ]);

    const WaterMeasurementDataFahrenheit = WaterMeasurementData.map(([time, celsius]) => [
      time,
      (celsius * 9) / 5 + 32,
    ]);

    const InterpolatedWaterPredictionDataFahrenheit = InterpolatedWaterPredictionData.map(
      ([time, celsius]) => [time, (celsius * 9) / 5 + 32]
    );

    const InterpolatedAirPredictionDataFahrenheit = InterpolatedAirPredictionData.map(
      ([time, celsius]) => [time, (celsius * 9) / 5 + 32]
    );

    const AirPredictionDataFahrenheit = AirPredictionData.map(([time, celsius]) => [
      time,
      (celsius * 9) / 5 + 32,
    ]);

    const WaterPredictionDataFahrenheit = WaterPredictionData.map(([time, celsius]) => [
      time,
      (celsius * 9) / 5 + 32,
    ]);

    // find the max of each data set
    const maxValuesArray = [
      Math.max(...WaterMeasurementDataFahrenheit.map(point => point[1])),
      Math.max(...InterpolatedWaterPredictionDataFahrenheit.map(point => point[1])),
      Math.max(...AirMeasurementDataFahrenheit.map(point => point[1])),
      Math.max(...InterpolatedAirPredictionDataFahrenheit.map(point => point[1])),
      Math.max(...AirPredictionDataFahrenheit.map(point => point[1])),
      Math.max(...WaterPredictionDataFahrenheit.map(point => point[1]))
    ];

    // then take the overall max of the max values
    const overallMax = Math.max(...maxValuesArray)

    // Update chart series with filtered data
    chartOptions.value.series = [
      {
        name: "Water Temperature Measurements",
        data: WaterMeasurementDataFahrenheit,
        color: "black",
        lineWidth: state.isSmallScreen ? 2 : 4,
        marker: { enabled: false },
      },
      {
        name: "Interpolated Predicted Water Temperature",
        data: InterpolatedWaterPredictionDataFahrenheit,
        color: "black",
        dashStyle: "2.5, 2.5", // Shorter dashes
        lineWidth: state.isSmallScreen ? 2 : 5,
        marker: { enabled: false },
      },
      {
        name: "Air Temperature Measurements",
        data: AirMeasurementDataFahrenheit,
        color: "#73c5da",
        lineWidth: state.isSmallScreen ? 2 : 4,
        marker: { enabled: false },
      },
      {
        name: "Interpolated Predicted Air Temperature",
        data: InterpolatedAirPredictionDataFahrenheit,
        color: "orange",
        dashStyle: "2.5, 2.5", // Shorter dashes
        lineWidth: state.isSmallScreen ? 2 : 5,
        marker: { enabled: false },
      },
      {
        name: "Air Temperature Predictions",
        data: AirPredictionDataFahrenheit,
        color: "green",
        dashStyle: "Dash",
        lineWidth: 0,
        marker: {
          enabled: true,
          radius: state.isSmallScreen ? 2 : 4,
        },
      },
      {
        name: "Water Temperature Predictions",
        data: WaterPredictionDataFahrenheit,
        color: "purple",
        dashStyle: "Dash",
        lineWidth: 0,
        marker: {
          enabled: true,
          radius: state.isSmallScreen ? 2 : 4,
        },
      },
    ];
  } catch (error) {
    console.error("Error fetching or processing data:", error);
  }
};


// CSV parsing function
const parseCSV = (csvText) => {
  const rows = csvText.split("\n").map((row) => row.split(","));
  const airMeasurements = [];
  const airPredictions = [];
  const waterMeasurements = [];
  const waterPredictions = [];

  rows.forEach((row, index) => {
    // Skip the header row
    if (index === 0) return;

    const [timestamp, waterMeasurement, waterPrediction, airMeasurement, airPrediction] = row;

    // Parse timestamp as UTC
    const [year, month, day, hour, minute, second] = timestamp.split(/[- :]/).map(Number);
    const utcTimestamp = Date.UTC(year, month - 1, day, hour, minute, second); // Parse as UTC (subtract 1 from month as Date.UTC expects 0-based months)

    const localTimestamp = new Date(utcTimestamp).toLocaleString("en-US", {
      timeZone: userTimeZone,
    });

    const localDate = new Date(localTimestamp);


    if (!isNaN(localDate)) {

      if (waterMeasurement && !isNaN(+waterMeasurement)) {
        waterMeasurements.push([localDate.getTime(), +waterMeasurement]);
      }
      if (waterPrediction && !isNaN(+waterPrediction)) {
        waterPredictions.push([localDate.getTime(), +waterPrediction]);
      }
      if (airMeasurement && !isNaN(+airMeasurement)) {
        airMeasurements.push([localDate.getTime(), +airMeasurement]);
      }
      if (airPrediction && !isNaN(+airPrediction)) {
        airPredictions.push([localDate.getTime(), +airPrediction]);
      }
    }
  });

  return { airMeasurements, airPredictions, waterMeasurements, waterPredictions };
};

// Function to toggle the dropdown menu
const toggleExportMenu = () => {
  isExportMenuVisible.value = !isExportMenuVisible.value;
};

///Fetch and update chart data every 15 minutes
let updateInterval;
onMounted(() => {
  fetchAndFilterData();
  window.addEventListener('resize', handleResize);
  updateInterval = setInterval(() => {
    console.log("Fetching and updating chart data...");
    fetchAndFilterData();
  }, 900000); 
});


onUnmounted(() => {
  clearInterval(updateInterval);
  window.removeEventListener('resize', handleResize);
});




</script>

<template>
  <div class="overflow-hidden bg-primary-bg text-dark-text font-main">

    <!-- Banner Section -->
  <section class="bg-banner-gradient-2 w-full text-white h-[300px] lg:h-[500px]">
    <!-- Overlay image on the left -->
    <div class="relative w-full h-full" >
      <img
        src="@/assets/images/LagunaMadreBay.jpg"
        alt="Map Overlay"
        class="w-full h-full object-crop flex opacity-30"
      />
      <!-- Text content overlay -->
      <div class="absolute  inset-0 flex items-center justify-center">
        <h1 class=" max-w-[1500px] text-lg md:text-3xl lg:text-5xl font-bold text-center pr-5 pl-5">
          Water and Air Temperature Trends and Forecasts for the Texas Upper Laguna Madre
        </h1>
      </div>
    </div>
  </section>

  <!-- Chart Section -->
  <section class="grid grid-cols-1 lg:grid-cols-5 gap-4 py-8 px-4 bg-white items-stretch">
  <!-- Chart -->
  <div class="lg:col-span-4 relative">
    <div class="w-full overflow-x-auto">
      <div class="min-w-[1000px] h-[500px] lg:h-[700px] lg:min-h-[650px]">
        <Chart class="w-full h-full p-4" :options="chartOptions" />
      </div>
    </div>

    <!-- Custom Export Dropdown -->
    <div class="hidden lg:block absolute top-5 right-4">
      <button @click="toggleExportMenu" class="bg-navy-blue text-white px-4 py-2 rounded-lg shadow-md hover:bg-blue-700">
        Download CSV Data
      </button>
      <ul v-if="isExportMenuVisible" class="absolute mt-2 w-48 bg-white border border-gray-300 shadow-lg rounded-lg z-50">
        <li>
          <a 
            :href="csvURL"
            download="Laguna-Madre_Water-Level_Air-Temperature_120hrs.csv"
            class="px-4 py-2 hover:bg-gray-100 cursor-pointer block">
            Download CSV
          </a>
        </li>
      </ul>
    </div>
  </div>

  <!-- Instructions -->
  <div class="bg-accent-bg p-6 rounded-lg shadow-md">
    <h2 class="text-lg text-xl  lg:text-3xl font-semibold text-center text-dark-text border-b-2 border-gray-500 pb-2 mb-3 lg:pb-4 lg:mb-6">
      How to Use the Interactive Chart
    </h2>
    <ul class="pt-5 space-y-4 list-none text-md lg:text-lg text-dark-text">
      <h3 class="text-lg lg:text-xl font-bold text-center">See Temperature Details:</h3>
      <li class="flex items-start space-x-2">
        <span class="text-blue-secondary">📊</span>
        <p>Move your mouse pointer over any dot or line on the chart to display the exact temperature value and the corresponding date or time.</p>
      </li>
      <h3 class="text-lg lg:text-xl font-bold text-center">Reset the View:</h3>
      <li class="flex items-start space-x-2">
        <span class="text-blue-secondary">🔄</span>
        <p>If you zoom in and want to go back to the original chart view, click the Reset View button in the top-right corner.
          Show or Hide Chart Lines</p>
      </li>
      <h3 class="text-lg lg:text-xl font-bold text-center">Show or Hide Chart Lines:</h3>
      <li class="flex items-start space-x-2">
        <span class="text-blue-secondary">👆</span>
        <p>Click on a label in the legend below the chart to turn a specific data series line or category on or off</p>
      </li>
    </ul>
  </div>

</section>


  <!-- Information Section -->
  <section class="grid grid-cols-1 lg:grid-cols-2 gap-8 bg-primary-bg py-8 px-10">
    <!-- Left Column -->
    <div class="lg:col-span-1 bg-white p-6 rounded-lg shadow-md">
      <h3 class="text-xl lg:text-2xl font-extrabold text-center lg:text-left text-dark-text border-b-2 border-gray-500 pb-2 mb-3 lg:pb-4 lg:mb-6">
        Data on this Graph:
      </h3>
      <ul class="list-disc list-inside space-y-2 text-md lg:text-l text-dark-text">
        <li>
          Past six-day air/water temperature from
          <a href="https://tidesandcurrents.noaa.gov/stationhome.html?id=8776139" 
            class="underline text-blue-600 hover:text-blue-800" target="_blank">NOAA's South Bird Island Station</a>
        </li>
        <li>
          Backup water temperature data from
          <a href="https://lighthouse.tamucc.edu/overview/171" 
            class="underline text-blue-600 hover:text-blue-800" target="_blank">National Park Service</a>
        </li>
        <li>Air temperature predictions from the National Digital Forecast Database (points)</li>
        <li>Cubic interpolation of predicted air temperature (dashed line)</li>
        <li>Water temperature predictions from Semaphore (dashed line)</li>
      </ul>
    </div>

    <!-- Right Column -->
    <div class="lg:col-span-1 bg-white p-6 rounded-lg shadow-md">
      <h3 class="text-xl lg:text-2xl font-extrabold text-center lg:text-left text-dark-text border-b-2 border-gray-500 pb-2 mb-3 lg:pb-4 lg:mb-6">
        Additional Information
      </h3>
      <ul class="list-disc space-y-2 pl-5 text-dark-text">
        <li>
          Wind speed graph available 
          <a href="https://cbigrid.tamucc.edu/tpw/graph-only-wind.html" target="_blank" class="underline text-blue-600 hover:text-blue-800">here</a>
        </li>
        <li>
          Ensemble air temperature predictions from The Weather Company available 
          <router-link 
            to="/air-temperature-ensemble" 
            class="underline text-blue-600 hover:text-blue-800">
            here
          </router-link>
        </li>
        <li>
          Ensemble water temperature predictions from Semaphore available 
          <router-link 
            to="/water-temperature-ensemble" 
            class="underline text-blue-600 hover:text-blue-800">
            here
          </router-link>
        </li>
        <li>
          Wind predictions for the Laguna Madre available
          <a href="https://cbigrid.tamucc.edu/tpw/graph-only-wind.html" target="_blank" class="underline text-blue-600 hover:text-blue-800">
            here
          </a>
        </li>
        <li>
          Ensemble air temperature predictions for Bird Island Basin available 
          <a href="https://cbigrid.tamucc.edu/tpw/graph-only-wind.html" target="_blank" class="underline text-blue-600 hover:text-blue-800">
            here
          </a>
        </li>
        <li>
          AI water temperature prediction models performance available
          <a href="https://lighthouse.tamucc.edu/supertool.php?stnid=013&elev=mwl&mode=nnwtp" target="_blank" class="underline text-blue-600 hover:text-blue-800">
            here
          </a>
        </li>
        <li>
          NOAA Sea Turtle Stranding and Salvage Network water temperature measurements
          <a href="https://connect.fisheries.noaa.gov/content/c0773132-9590-4e21-bb42-676e2140fbaa/" target="_blank" class="underline text-blue-600 hover:text-blue-800">
            here
          </a>
        </li>
      </ul>
    </div>

</section>

<!-- Section Divider -->
<div class="h-[50px] bg-section-gradient"></div>

  <!-- About Section -->
  <section class="grid grid-cols-1 lg:grid-cols-2 bg-white py-10 px-6 md:px-20 gap-10 items-center">
      <!-- Image Section -->
      <div class="flex flex-col items-center">
        <div class="flex justify-center">
          <img 
            src="@/assets/images/LagunaMadreMap.png" 
            alt="Map of Laguna Madre, Texas" 
            class="w-[90%] h-auto rounded-lg shadow-lg"
          >
        </div>
        <p class="text-xs text-center text-gray-600 mt-2">
          Map imagery © 2024 Google Earth, Data © Google, Maxar Technologies, U.S. Geological Survey, USDA Farm Service Agency.
        </p>
      </div>


      <!-- Text Content Section -->
      <div class="text-center lg:text-left">
        <h2 class="text-lg lg:text-3xl font-extrabold text-center text-dark-text mb-6">
          Laguna Madre AI Model
        </h2>
        <p class="text-md lg:text-xl text-dark-text mb-4">
          In the Laguna Madre, the longest hypersaline lagoon in the United States, the passage of cold fronts can lower air temperature by more than 
          10°C in less than 24 hours. This rapid drop can lead to significant decreases in water temperature. Some of these cold-water events have caused large-scale fish kills and cold-stunning of sea turtles.
        </p>
        <p class="text-md lg:text-xl text-dark-text mb-4">
          To mitigate the impact of these cold events, members of the Texas Marine Coldwater Response Collaboration (TCRC) — including local agencies, private-sector companies, and other stakeholders (logos below) — voluntarily interrupt activities such as fishing, navigation, and dredging in the Laguna Madre. Dredging, which involves the removal of sediments to maintain navigational channels, can contribute to changes in water circulation and temperature distribution. During extreme cold events, suspending dredging operations helps minimize further disturbances to the ecosystem and allows marine life to seek refuge in deeper, more stable waters. These proactive measures help protect marine life and mobilize resources during critical times.
        </p>
        <p class="text-md lg:text-xl text-dark-text mb-4">
          Accurate temperature predictions are essential for managing these interruptions effectively. The live-updating graph above displays the latest air and water temperature measurements, along with predicted air and water temperatures for the Laguna Madre. Research and development of improved model predictions are ongoing for improved collaborative decision-making during cold weather and cold-stunning events.
        </p>
        <p class="text-md lg:text-xl text-dark-text mb-4">
          This AI model was originally developed by Dr. Robyn Ball during her master's studies at Texas A&M University–Corpus Christi. Responsibility for the model has since been entrusted to the Cool Turtles team at the Coastal Dynamics Lab. The Cool Turtles team is led by PhD student 
          <a href="https://www.linkedin.com/in/miranda-white-859b2414a/" target="_blank" class="text-blue-500 hover:underline">Miranda White</a>, 
          alongside her talented teammates 
          <a href="https://www.linkedin.com/in/jarett-woodall-mba-8a3696224/" target="_blank" class="text-blue-500 hover:underline">Jarett Woodall</a>, 
          <a href="https://www.linkedin.com/in/christian-duff-898103211/" target="_blank" class="text-blue-500 hover:underline">Christian Duff</a>, 
          <a href="https://www.facebook.com/watch/?v=740721718150868" target="_blank" class="text-blue-500 hover:underline">Hector Marrero-Colominas</a>,
          <a href="https://www.linkedin.com/in/andrew-desimone-00170b24b/" target="_blank" class="text-blue-500 hover:underline">Andrew DeSimone</a>, 
          and Elisa Flores. 
        </p>

      </div>
  </section>



    <!-- Footer -->
    <footer class="bg-navy-blue py-10 text-dark-text space-y-2">
      <div class="flex flex-col justify-center items-center text-white text-sm lg:text-lg">
        <a href="https://tpwd.texas.gov/" target="_blank" class="hover:scale-110 transition-transform">
          <p>Texas Parks & Wildlife</p>
        </a>
        <a href="https://tpwd.texas.gov/" target="_blank" class="hover:scale-110 transition-transform">
          <p>NPS Sea Turtle Science and Recovery</p>
        </a>
        <a href="https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0173920" target="_blank" class="hover:scale-110 transition-transform">
          <p>PLOS One: Publication Defining Cold Stunning Threshold</p>
        </a>
        <a href="https://www.coastaldynamicslab.org/water-temperature-predictionse" target="_blank" class="hover:scale-110 transition-transform">
          <p>TAMUCC CBI Water Temperature Predictions Reports</p>
        </a>
      </div>
      <div class="flex flex-wrap justify-center items-center gap-8 lg:gap-16 mx-auto p-1 lg:p-4">
        <a href="https://www.conradblucherinstitute.org/" target="_blank" class="hover:scale-110 transition-transform">
          <img src="@/assets/images/CBI-Logo.png" alt="CBI Logo" class="max-w-[165px] lg:max-w-[250px] ">
        </a>
        <a href="https://github.com/conrad-blucher-institute/semaphore" target="_blank" class="hover:scale-110 transition-transform">
          <img src="@/assets/images/Semaphore-Logo.png" alt="Semaphore Logo" class="max-w-[80px] lg:max-w-[150px]">
        </a>
        <a href="https://www.usace.army.mil/" target="_blank" class="hover:scale-110 transition-transform">
          <img src="@/assets/images/USACE-Logo.jpg" alt="US Army Corps Logo" class="max-w-[80px] lg:max-w-[150px]">
        </a>
        <a href="https://www.nsf.gov/" target="_blank" class="hover:scale-110 transition-transform">
          <img src="@/assets/images/NSF-Logo.png" alt="National Science Foundation Logo" class="max-w-[80px] lg:max-w-[150px]">
        </a>
        <a href="https://www.gicaonline.com/" target="_blank" class="hover:scale-110 transition-transform">
          <img src="@/assets/images/GICA-Logo.png" alt="Gulf Intracoastal Canal Association Logo" class="max-w-[80px] lg:max-w-[150px]">
        </a>
        <a href="https://tpwd.texas.gov/" target="_blank" class="hover:scale-110 transition-transform">
          <img src="@/assets/images/TPWD-Logo.gif" alt="Texas Parks and Wildlife Logo" class="max-w-[80px] lg:max-w-[150px]">
        </a>
        <a href="https://www.coastaldynamicslab.org/" target="_blank" class="hover:scale-110 transition-transform">
          <img src="@/assets/images/CDL-Logo.png" alt="Coastal Dynamics Lab Logo" class="max-w-[80px] lg:max-w-[150px]">
        </a>
        <a href="https://www.nps.gov/index.htm" target="_blank">
          <img class="footer-logo" src="@/assets/images/NPS-Logo.png" alt="National Park Service Logo">
        </a>
        <a href="https://www.weather.gov/" target="_blank">
          <img src="@/assets/images/NWS-Logo.png" alt="National Weather Service Logo" class="max-w-[80px] lg:max-w-[150px]">
        </a>
        <a href="https://www.uscg.mil/" target="_blank">
          <img  src="@/assets/images/CG-Logo.png" alt="USA Coast Guard Logo" class="max-w-[80px] lg:max-w-[150px]">
        </a>
        <a href="https://www.joincca.org/" target="_blank">
          <img src="@/assets/images/CCA-Logo.png" alt="Coastal Conservation Association Logo" class="max-w-[80px] lg:max-w-[150px]">
        </a>
      </div>
      <p class="text-center text-sm text-light-text">(Click on the logos to visit each contributor's website)</p>
    </footer>
  </div>
</template>
