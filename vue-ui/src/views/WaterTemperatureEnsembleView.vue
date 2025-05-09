<!-- ===================================================
     View: WaterTemperatureEnsembleView.vue

     Description: This view displays the water temperature ensemble trends and predictions for South Bird Island.

                  Features include:
                  - A dynamically updating Highcharts spaghetti chart using live CSV data.
                  - Instructions for interacting with the chart.
                  - Information on the data of the chart.
                  - Additional links
     Author: Anointiyae Beasley and Savannah Stephenson

     Date: 04/03/2025

======================================================= -->
<script setup>
import Highcharts from "highcharts";
import { Chart } from "highcharts-vue";

import { ref, onMounted, onUnmounted } from "vue";

const isSmallScreen = window.innerWidth <= 600;
const csvURL = ref(`${window.location.origin}/flare/csv-data/Laguna-Madre_Water-Level_Air-Temperature_120hrs.csv`);

// Add reactive state for dropdown visibility
const isExportMenuVisible = ref(false);
const userTimeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;
console.log("User's Time Zone:", userTimeZone);


// Define the current date and time
const nowDate = new Date();// Current timestamp
const nowTime = nowDate.getTime();

const chartOptions = ref({});
// Small screen chart options
const smallScreenChartOptions = ref({
  chart: {
    type: "line",
    zoomType: "x",
    backgroundColor: "white",
    style: { fontFamily: "Arial" },
    marginRight: 30, // Adjust right margin'
  },
  title: {
    text: "Temperatures of the Upper Laguna Madre",
    style: { fontSize: "20px", fontWeight: "bold", color: "#0f4f66" }, // Adjusted for small screens
  },
  legend: {
    itemStyle: {
      fontSize: "12px", // Adjusted for small screens
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
        fontSize: "12px", // Adjusted for small screens
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
        fontSize: "14px", // Adjusted for small screens
        fontFamily: "Arial",
        color: "#0f4f66",
      },
    },
    plotLines: [
      {
        color: "red",
        width: 2, // Line width
        value: nowTime, // Use timestamp for correct placement
        dashStyle: "Solid",
        label: {
          text: "Now",
          y:20,
          style: {
            color: "#0f4f66",
            fontSize: "12px",
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
                  const localDate = new Date(time); // Convert timestamp to local time
                  const options = { weekday: "short", month: "short", day: "numeric" }; // Format options
                  return localDate.toLocaleDateString("en-US", options); // Format as "Mon Jan 27"
                })(),
              align: "left",
              rotation: 0,
              y: 15,
              style: {
                color: "#0f4f66",
                fontSize: "10px",
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
      fontSize: '12px',
      color: '#0f4f66',
      fontFamily: 'Arial',
    },
  },
  title: {
    text: "Temperature (°F)",
    style: { color: "#0f4f66", fontSize: "12px" },
  },
  max: 90,
  min: 20,
  tickInterval: 10, // Major ticks every 10 units
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
          fontSize: "12px",
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
          fontSize: "12px",
          fontFamily: "Arial",
          fontWeight: "bold",
        },
      },
    },
  ],
},

  series: [], // Placeholder for data, dynamically updated
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
      fontSize: "12px",
      padding: "5px",
      color: "#0f4f66",
      fontFamily: "Arial",
    },
  },
});


// Reactive variables for chart options
const largeScreenChartOptions = ref({
  chart: {
    type: "line",
    zoomType: "x",
    backgroundColor: "white",
    style: { fontFamily: "Arial" },
    marginRight: 30
  },
  title: {
    text: "Temperatures of the Upper Laguna Madre",
    style: { fontSize: "28px", fontWeight: "bold", color: "#0f4f66" },
  },
  exporting: {
  enabled: true, // Enables the export menu
},
  legend: {
    itemStyle: {
      fontSize: "19px",
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
        fontSize: "16px",
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
        fontSize: "20px",
        fontFamily: "Arial",
        color: "#0f4f66"
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
            fontSize: "14px",
            fontFamily: "Arial"
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
              y: 15, // Lower the dynamic plotline labels
              style: {
                color: "#0f4f66",
                fontSize: "12px",
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
          fontSize: '26px', 
          color: '#0f4f66',
          fontFamily: 'Arial', 
        },
      },
    title: {
      text: "Temperature (°F)",
      style: { color: "#0f4f66", fontSize: "20px" },
    },
    max: 90,
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
            fontSize: "16px",
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
            fontSize: "16px",
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
      fontSize: "14px",
      padding: "8px",
      color: "#0f4f66",
      fontFamily: "Arial",
    },
  },
});


if (isSmallScreen) {
  chartOptions.value = smallScreenChartOptions.value;
} else {
  chartOptions.value = largeScreenChartOptions.value;
}

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

    // Update chart series with filtered data
    chartOptions.value.series = [
      {
        name: "Water Temperature Measurements",
        data: WaterMeasurementDataFahrenheit,
        color: "black",
        lineWidth: isSmallScreen ? 2 : 4,
        marker: { enabled: false },
      },
      {
        name: "Interpolated Predicted Water Temperature",
        data: InterpolatedWaterPredictionDataFahrenheit,
        color: "black",
        dashStyle: "2.5, 2.5", // Shorter dashes
        lineWidth: isSmallScreen ? 2 : 5,
        marker: { enabled: false },
      },
      {
        name: "Air Temperature Measurements",
        data: AirMeasurementDataFahrenheit,
        color: "#73c5da",
        lineWidth: isSmallScreen ? 2 : 4,
        marker: { enabled: false },
      },
      {
        name: "Interpolated Predicted Air Temperature",
        data: InterpolatedAirPredictionDataFahrenheit,
        color: "orange",
        dashStyle: "2.5, 2.5", // Shorter dashes
        lineWidth: isSmallScreen ? 2 : 5,
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
          radius: isSmallScreen ? 2 : 4,
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
          radius: isSmallScreen ? 2 : 4,
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
  updateInterval = setInterval(() => {
    console.log("Fetching and updating chart data...");
    fetchAndFilterData();
  }, 900000); 
});


onUnmounted(() => {
  clearInterval(updateInterval);
});
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
          class="w-full h-full object-crop flex opacity-30"
        />
        <!-- Text content overlay -->
        <div class="absolute  inset-0 flex items-center justify-center">
          <h1 class=" max-w-[1500px] text-lg md:text-3xl lg:text-5xl font-bold text-center pr-5 pl-5">
           Ensemble Water Temperature Trends and Forecasts for the Texas Upper Laguna Madre
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
    </div>
</template>





