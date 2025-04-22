<!-- ===================================================
     View: AirTemperatureEnsembleView.vue

     Description: This view displays the air temperature ensemble trends and predictions for South Bird Island.

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
//const csvURL = ref(`${window.location.origin}/flare/csv-data/TWC-Laguna-Madre_Air-Temperature-Predictions_120hrs.csv`);
const csvURL = ref(`https://cbigrid.tamucc.edu/tpw/ibm/ibm-predictions-sbirdisland.csv`); 

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
    text: "Ensemble Air Temperature Predictions from The Weather Company",
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
    maxPadding: 0, // Fitting lines exactly to graph size
    minPadding: 0,
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

    plotLines: [],
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
  min: 65,
  tickInterval: 10, // Major ticks every 10 units
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
    text: "Ensemble Air Temperature Predictions from The Weather Company",
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
    maxPadding: 0, // Fitting lines exactly to graph x axis
    minPadding: 0,
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
    plotLines: [],
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
    min: 65,
    tickInterval: 10, // Add ticks every 10 units
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
    // Fetch CSV data
    const response = await fetch(csvURL.value);
    if (!response.ok) throw new Error("Failed to fetch CSV data");

    const csvText = await response.text();
    console.log("Fetched CSV Data:", csvText);

    // Parse the CSV data
    const { airPredictionMembers } = parseCSV(csvText);
    console.log("Parsed Ensemble Models Data:", airPredictionMembers);

    const series = [];

    // Loop through each ensemble member
    airPredictionMembers.forEach((memberData, i) => 
    {
      // Convert to Fahrenheit
      const converted = memberData.map(([timestamp, tempC]) => [
        Number(timestamp), //convert timestamp to date
        tempC,
      ]);

      // Push series
      series.push({
        name: `Ensemble Member ${i + 1}`,
        data: converted,
        color: Highcharts.getOptions().colors[i % 100], 
        lineWidth: 1,
        marker: { enabled: false },
      });
    });

    // Assign to chart
    console.log("Final series:", series);
    chartOptions.value.series = series;
    chartOptions.value.legend = {enabled: false};
    console.log("Updated Chart Options:", chartOptions.value);

  } catch (error) {
    console.error("Error fetching or processing data:", error);
  }
};

// CSV parsing function
const parseCSV = (csvText) => 
{
  const rows = csvText.split("\n").map((row) => row.split(","));
  
  //Create arrays for ensembles
  const airPredictionMembers = Array.from({length:100}, () => []);

  rows.forEach((row, rowIndex) => 
  {
    // Skip the header row
    if (rowIndex === 0) return;

    const [timestamp,] = row

    row.forEach((cell, colIndex) => 
    {
      console.log(`Row ${rowIndex}, Column ${colIndex}: ${cell}`);
      if (!(colIndex === 0) && !(colIndex === 101) &&cell && !isNaN(+cell)) 
        {
          // offset of colIndex because the first column of the data is timestamps
          // and skip the last column because it's the average
          airPredictionMembers[colIndex - 1].push([timestamp, +cell]);
        }
      
    }); //End of iterating columns 
  }); //End of iterating Rows
  return {airPredictionMembers};
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
            Ensemble Air Temperature Trends and Forecasts for the Texas Upper Laguna Madre
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
              download="ibm-predictions-sbirdisland.csv"
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