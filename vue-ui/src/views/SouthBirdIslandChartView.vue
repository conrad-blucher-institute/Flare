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

import { ref, onMounted, onUnmounted } from "vue";

const isSmallScreen = window.innerWidth <= 600;
const csvURL = ref(`${window.location.origin}/flare/csv-data/Laguna-Madre_Water-Level_Air-Temperature_120hrs.csv`);
// Add reactive state for dropdown visibility
const isExportMenuVisible = ref(false);


// Define the current date and time
const nowDate = new Date();// Current timestamp
const nowTime = Date.UTC(
  nowDate.getUTCFullYear(),
  nowDate.getUTCMonth(),
  nowDate.getUTCDate(),
  nowDate.getUTCHours(),
  nowDate.getUTCMinutes()
);

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
        const day = Highcharts.dateFormat("%a", this.value);
        const date = Highcharts.dateFormat("%b %e", this.value);
        const time = Highcharts.dateFormat("%l:%M %p", this.value);
        return `<span style="display: block; text-align: center; font-family: Arial;">
                  <b>${day}</b><br>${date}<br><i>${time}</i>
                </span>`;
      },
      useHTML: true,
      style: {
        fontSize: "12px", // Adjusted for small screens
        fontFamily: "Arial",
        color: "#0f4f66",
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
        const min = Math.ceil(xAxis.min / (24 * 3600 * 1000)) * (24 * 3600 * 1000); // Start of the next day
        const max = xAxis.max;
        const plotLines = [];

        // Iterate over every 2 days in the range
        for (let time = min; time <= max; time += 2 * 24 * 3600 * 1000) {
          plotLines.push({
            color: "gray",
            dashStyle: "Dot",
            width: 1,
            value: time,
            label: {
              text: Highcharts.dateFormat("%a %b %e", time),
              align: "left",
              rotation: 0,
              y: 15,
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

  series: [], // Placeholder for dynamically updated data
  tooltip: {
    shared: false,
    crosshairs: true,
    formatter: function () {
      return `<b>Date: ${Highcharts.dateFormat("%A, %b %e, %Y", this.x)}</b><br>
              Temperature: ${this.y}°F`;
    },
    style: {
      fontSize: "14px",
      padding: "8px",
      color: "#0f4f66",
      fontFamily: "Arial",
    },
  },
  series: [], // Placeholder for data, dynamically updated
  tooltip: {
    shared: false,
    crosshairs: true,
    formatter: function () {
      return `<b>Date: ${Highcharts.dateFormat("%A, %b %e, %Y", this.x)}</b><br>
              Temperature: ${this.y}°F`;
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
        const day = Highcharts.dateFormat("%a", this.value);
        const date = Highcharts.dateFormat("%b %e", this.value);
        const time = Highcharts.dateFormat("%l:%M %p", this.value);
        return `<span style="display: block; text-align: center; font-family: Arial;">
                  <b>${day}</b><br>${date}<br><i>${time}</i>
                </span>`;
      },
      useHTML: true,
      style: {
        fontSize: "16px",
        fontFamily: "Arial",
        color: "#0f4f66"
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
        const min = Math.ceil(xAxis.min / (24 * 3600 * 1000)) * (24 * 3600 * 1000); // Start of the next day
        const max = xAxis.max;
        const plotLines = [];

        // Iterate over every 2 days in the range
        for (let time = min; time <= max; time += 2 * 24 * 3600 * 1000) {
          plotLines.push({
            color: "gray",
            dashStyle: "Dot",
            width: 1,
            value: time,
            label: {
              text: Highcharts.dateFormat("%a %b %e", time),
              align: "left",
              rotation: 0,
              y: 15, // Lower the dynamic plotline labels
              style: {
                color: "#0f4f66",
                fontSize: "14px",
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
      return `<b>Date: ${Highcharts.dateFormat("%A, %b %e, %Y", this.x)}</b><br>
              <b>Time: ${Highcharts.dateFormat("%H:%M", this.x)}</b><br>
              Temperature: ${this.y}°F`;
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

    console.log("---------NOW TIME---------");
    console.log(nowTime);

    // Ensure parsed arrays are initialized
    const WaterMeasurementData = parsedData.waterMeasurements || [];
    const AirMeasurementData = parsedData.airMeasurements || [];
    const InterpolatedAirPredictionData = parsedData.airPredictions || [];
    const InterpolatedWaterPredictionData = parsedData.waterPredictions || [];

    // Filter `InterpolatedAirPrediction` to only include hourly data
    const AirPredictionData = InterpolatedAirPredictionData.filter((point) => {
      const pointTime = new Date(point[0]);
      return pointTime >= nowTime && pointTime.getMinutes() === 0; // Include only hourly points
    });

    // Filter `InterpolatedWaterPrediction` for specific intervals
    const hoursToFilter = [3, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84, 90, 102, 114, 120];
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
        dashStyle: "Dash",
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
        dashStyle: "Dash",
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
          enabled: false,
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
    const parsedTimestamp = Date.UTC(year, month - 1, day, hour, minute, second); // Parse as UTC (subtract 1 from month as Date.UTC expects 0-based months)

    if (!isNaN(parsedTimestamp)) {

      if (waterMeasurement && !isNaN(+waterMeasurement)) {
        waterMeasurements.push([parsedTimestamp, +waterMeasurement]);
      }
      if (waterPrediction && !isNaN(+waterPrediction)) {
        waterPredictions.push([parsedTimestamp, +waterPrediction]);
      }
      if (airMeasurement && !isNaN(+airMeasurement)) {
        airMeasurements.push([parsedTimestamp, +airMeasurement]);
      }
      if (airPrediction && !isNaN(+airPrediction)) {
        airPredictions.push([parsedTimestamp, +airPrediction]);
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
        src="@/assets/images/LagunaMadreBay.jpg"
        alt="Map Overlay"
        class="w-full h-full object-crop flex opacity-30"
      />
      <!-- Text content overlay -->
      <div class="absolute  inset-0 flex items-center justify-end pr-10">
        <h1 class=" w-[150px] lg:w-[550px] text-lg lg:pt-10 md:text-3xl lg:text-5xl font-bold text-center ">
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
    <ul class="pt-5 space-y-4 list-none text-md lg:text-lg">
      <h3 class="text-dark-text text-lg lg:text-xl font-bold text-center">See Temperature Details:</h3>
      <li class="flex items-start space-x-2">
        <span class="text-blue-secondary">📊</span>
        <p>Move your mouse pointer over any dot or line on the chart to display the exact temperature value and the corresponding date or time.</p>
      </li>
      <h3 class="text-dark-text text-lg lg:text-xl font-bold text-center">Reset the View:</h3>
      <li class="flex items-start space-x-2">
        <span class="text-blue-secondary">🔄</span>
        <p>If you zoom in and want to go back to the original chart view, click the Reset View button in the top-right corner.
          Show or Hide Chart Lines</p>
      </li>
      <h3 class="text-dark-text text-lg lg:text-xl font-bold text-center">Show or Hide Chart Lines:</h3>
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
      <ul class="list-disc list-inside space-y-4 text-base md:text-lg text-gray-700">
        <li>
          Past six-day air/water temperature from
          <a href="https://tidesandcurrents.noaa.gov/stationhome.html?id=8776139" 
            class="underline text-blue-600 hover:text-blue-800" target="_blank">NOAA's South Bird Island Station</a>.
        </li>
        <li>
          Backup water temperature data from
          <a href="https://lighthouse.tamucc.edu/overview/171" 
            class="underline text-blue-600 hover:text-blue-800" target="_blank">National Park Service</a>.
        </li>
        <li>Air temperature predictions from the National Digital Forecast Database (points).</li>
        <li>Cubic interpolation of predicted air temperature (dashed line).</li>
        <li>Water temperature predictions from Semaphore (dashed line).</li>
      </ul>
    </div>

    <!-- Right Column -->
    <div class="lg:col-span-1 bg-white p-6 rounded-lg shadow-md">
      <h3 class=" text-xl lg:text-2xl font-extrabold  text-center lg:text-left text-dark-text border-b-2 border-gray-500 pb-2 mb-3 lg:pb-4 lg:mb-6">
        Additional Information
      </h3>
      <p class="text-base md:text-lg text-gray-700 mb-4">
        Wind speed graph available 
        <a href="https://example.com/wind-speed" target="_blank" 
          class="underline text-blue-600 hover:text-blue-800">here</a>. 
      </p>
      <p class="text-base md:text-lg text-gray-700">
        Ensemble air temperature predictions from The Weather Company available 
        <a href="https://example.com/temperature-predictions" target="_blank" 
          class="underline text-blue-600 hover:text-blue-800">here</a>. 
      </p>
    </div>
</section>

<!-- Section Divider -->
<div class="h-[50px] bg-section-gradient"></div>

  <!-- About Section -->
  <section class="grid grid-cols-1 lg:grid-cols-2 bg-white py-10 px-6 md:px-20 gap-10 items-center">
      <!-- Image Section -->
      <div class="flex justify-center">
        <img 
          src="@/assets/images/SouthBirdIslandMap.jpg" 
          alt="Map of South Bird Island, Texas" 
          class="w-[70%] h-auto rounded-lg shadow-lg"
        >
      </div>

      <!-- Text Content Section -->
      <div class="text-center lg:text-left">
        <h2 class="text-lg lg:text-3xl font-extrabold text-center text-dark-text mb-6">
          Laguna Madre AI Model
        </h2>
        <p class="text-md lg:text-xl text-gray-700 mb-4">
          In the Laguna Madre, the longest hypersaline lagoon in the United States, the passage of cold fronts can lower air temperature by more than 
          <strong class="font-semibold text-dark-text">10°C</strong> in less than 24 hours. This rapid drop can lead to significant decreases in water temperature. Some of these cold-water events have caused large-scale fish kills and cold-stunning of sea turtles.
        </p>
        <p class="text-md lg:text-xl text-gray-700 mb-4">
          To mitigate the impact of these cold events, members of the Texas Marine Coldwater Response Collaboration (TCRC) — including local agencies, private-sector companies, and other stakeholders (logos below) — voluntarily interrupt activities such as fishing and navigation in the Laguna Madre. These proactive measures help protect marine life and mobilize resources during critical times.
        </p>
        <p class="text-md lg:text-xl text-gray-700 mb-4">
          Accurate temperature predictions are essential for managing these interruptions effectively. The live-updating graph above displays the latest air and water temperature measurements, along with predicted air and water temperatures for the Laguna Madre. Research and development of improved model predictions are ongoing for improved collaborative decision-making during cold weather and cold-stunning events.
        </p>
        <p class="text-md lg:text-xl text-gray-700 mb-4">
          This AI model was developed by the Cool Turtles team from the Coastal Dynamics Lab. The Cool Turtles team is led by PhD student 
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
    <footer class="bg-navy-blue py-10 text-dark-text">
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
      </div>
      <p class="text-center mt-6 text-sm text-light-text">
        Photos courtesy of the National Park Service. 
      </p>
      <p class="text-center text-sm text-light-text">(Click logos to visit.)</p>
    </footer>
  </div>
</template>
