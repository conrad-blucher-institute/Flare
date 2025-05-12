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

import { ref, onMounted, onUnmounted, reactive } from "vue";

// Using reactive state to track if the screen is small
const state = reactive({ 
  isSmallScreen: window.innerWidth <= 600
});

const csvURL = ref(`${window.location.origin}/flare/csv-data/TWC-Laguna-Madre_Air-Temperature-Predictions_240hrs.csv`);
const csvURL2 = ref(`${window.location.origin}/flare/csv-data/TWC-NDFD-Laguna-Madre_Air-Temperature-Predictions_240hrs.csv`);

// Add reactive state for dropdown visibility
const isExportMenuVisible = ref(false);
const isSecondExportMenuVisible = ref(false);
const userTimeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;
console.log("User's Time Zone:", userTimeZone);


// Define the current date and time
const nowDate = new Date(); // Current timestamp
const nowTime = nowDate.getTime();

const chartOptions = ref({});
const secondChartOptions = ref({});

// Chart function for first chart that changes based on screen size
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
      text: "Ensemble Air Temperature Predictions from The Weather Company",
      style: { 
        fontSize: isSmallScreen ? "20px" : "28px", 
        fontWeight: "bold", 
        color: "#0f4f66" 
      },
    },
    exporting: {
      enabled: true, // Enables the export menu
    },
    legend: {enabled: false,
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
          fontSize: isSmallScreen ? "14px" : "20px",
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
    max: 100,
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
        fontSize: isSmallScreen ? "12px" : "14px", 
        padding: isSmallScreen ? "5px" : "8px", 
        color: "#0f4f66",
        fontFamily: "Arial",
      },
    },
  };
};

// Chart function for second chart that changes based on screen size
const buildSecondChart = (isSmallScreen) => {
  return {
    chart: {
      type: "areaspline",
      zoomType: "x",
      backgroundColor: "white",
      style: { fontFamily: "Arial" },
      marginRight: 30
    },
    title: {
      text: "Ensemble Air Temperature Predictions from The Weather Company And The National Digital Forecast Database",
      style: { 
        fontSize: isSmallScreen ? "20px" : "28px", 
        fontWeight: "bold", 
        color: "#0f4f66" 
      },
    },
    exporting: {
      enabled: true,
    },
    legend: {
      enabled: true,
      align: 'center',
      verticalAlign: 'bottom',
      layout: 'horizontal',
      itemStyle: {
        color: "#0f4f66",
        fontWeight: 'normal',
        fontSize: isSmallScreen ? "12px" : "14px"
      }
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
          return `<span style="display: block; text-align: center; font-family: Arial;">
                    <b>${day}</b><br>${date}
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
      tickInterval: 24 * 3600 * 1000, // Main ticks every day
      title: {
        text: "Time",
        style: {
          fontSize: isSmallScreen ? "14px" : "20px",
          fontFamily: "Arial",
          color: "#0f4f66",
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
      max: 90,
      min: 60,
      tickInterval: 5, // Major ticks every 5 units
    },
    plotOptions: {
      areaspline: {
        fillOpacity: 0.3,
        marker: {
          enabled: false,
          radius: 3,
          states: {
            hover: {
              enabled: true
            }
          }
        },
        states: {
          hover: {
            lineWidth: 3
          }
        }
      }
    },
    series: [], // Placeholder for data, dynamically updated
    tooltip: {
      shared: true,
      crosshairs: true,
      formatter: function () {
        const localDate = new Date(this.x);
        let tooltipText = `<b>Date: ${localDate.toLocaleDateString("en-US", {
          weekday: "long",
          month: "short",
          day: "numeric",
          year: "numeric",
        })}</b><br>`;
        
        this.points.forEach(point => {
          tooltipText += `<span style="color:${point.color}">\u25CF</span> ${point.series.name}: <b>${point.y.toFixed(2)}°F</b><br>`;
        });
        
        return tooltipText;
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
  secondChartOptions.value = buildSecondChart(state.isSmallScreen);
}

// Setting chartOptions based on the returned screen size
chartOptions.value = buildChart(state.isSmallScreen);
secondChartOptions.value = buildSecondChart(state.isSmallScreen);

// Function to fetch and process CSV data for first chart
const fetchAndFilterData = async () => {
  try {
    // Fetch CSV data
    const response = await fetch(csvURL.value);
    if (!response.ok) throw new Error("Failed to fetch CSV data");
    console.log(`Fetched URL: ${response.url}`);

    const csvText = await response.text();
    console.log("Fetched CSV Data:", csvText);

    // Parse the CSV data
    const { airPredictionMembers } = parseCSV(csvText);
    console.log("Parsed Ensemble Models Data:", airPredictionMembers);

    const series = [];

    // Loop through each ensemble member
    airPredictionMembers.forEach((memberData, i) => {
      series.push({
        name: `Ensemble Member ${i + 1}`,
        data: memberData,
        color: Highcharts.getOptions().colors[i % 10], // Use Highcharts colors
        lineWidth: 1,
        marker: { enabled: false },
      });
    });

    // Update chart options
    chartOptions.value.series = series;
    console.log("Updated Chart Options:", chartOptions.value);
  } catch (error) {
    console.error("Error fetching or processing data:", error);
  }
};

// Function to fetch and process second CSV data
const fetchAndFilterSecondData = async () => {
  try {
    // Fetch CSV data
    const response = await fetch(secondCsvURL.value);
    if (!response.ok) throw new Error("Failed to fetch second CSV data");
    console.log(`Fetched second URL: ${response.url}`);

    const csvText = await response.text();
    console.log("Fetched Second CSV Data:", csvText);

    // Parse the CSV data for the second chart
    const { TemperatureData } = parseSecondCSV(csvText);
    console.log("Parsed Temperature Data:", TemperatureData);

    // Ensure parsed arrays are initialized
    const mean = parsedData.means || [];
    const lowerBounds = parsedData.lowerBounds || [];
    const upperBounds = parsedData.upperBounds || [];
    const NDFPredictions = parsedData.NDFPredictions || [];

    //Change to Fahrenheit 
    const toFahrenheit = (celsius) => (celsius * 9) / 5 + 32;
    const meanFahrenheit = mean.map(([time, celsius]) => [time, toFahrenheit(celsius)]);
    const lowerBoundsFahrenheit = lowerBounds.map(([time, celsius]) => [time, toFahrenheit(celsius)]);
    const upperBoundsFahrenheit = upperBounds.map(([time, celsius]) => [time, toFahrenheit(celsius)]);
    const NDFPredictionsFahrenheit = NDFPredictions.map(([time, celsius]) => [time, toFahrenheit(celsius)]);

    // For highcharts to do a shaded range, it wants the rage in the format of [date_index, lower_bound, upper_bound]
    // This just combines the lower and upper bound into one series of the above format
    const boundsFahrenheit = lowerBoundsFahrenheit.map((point, index) => {
      const dateIndex = point[0];
      const lowerBound = lowerBoundsFahrenheit[index][1];
      const upperBound = upperBoundsFahrenheit[index][1];
      return [dateIndex, upperBound, lowerBound];
    });

    // Update chart series with filtered data

    // Update second chart options
    // Update chart series with filtered data
    chartOptions.value.series = [
      {
        name: "Median Water Temperature Predictions",
        data: meanFahrenheit,
        color: "black",
        dashStyle: "Dash",
        lineWidth: isSmallScreen ? 2 : 4,
        zIndex: 1, // Ensure this is above the bounds
        marker: { enabled: false },
      },
      {
        name: "Bounds",
        data: boundsFahrenheit,
        type: 'arearange',
        linkedTo: "Air Temperature Predictions",
        lineWidth: 0, // No line for bounds
        color: Highcharts.getOptions().colors[0],
        fillOpacity: 0.3,
        zIndex: 0, // Ensure this is below the mean line
        marker: { enabled: false },
      },
      {
        name: "NDFD Air Temperature Predictions",
        data: NDFPredictionsFahrenheit,
        color: "purple",
        dashStyle: "2.5, 2.5", // Shorter dashes
        lineWidth: isSmallScreen ? 2 : 5,
        lineWidth: isSmallScreen ? 2 : 4,
        marker: {
          enabled: true,
          radius: isSmallScreen ? 2 : 4,
        },
      }
    ];
  } catch (error) {
    console.error("Error fetching or processing data:", error);
  }
};

// CSV parsing function first chart
const parseCSV = (csvText) => {
  const rows = csvText.split("\n").map((row) => {
    // Split the row into two parts: timestamp and JSON array
    const match = row.match(/^([^,]+),(.+)$/);
    return match ? [match[1].trim(), match[2].trim()] : [];
  });

  const airPredictionMembers = [];

  rows.forEach((row, rowIndex) => {
    // Skip the header row
    if (rowIndex === 0) return;

    const [timestamp, jsonArray] = row;

      // Skip rows with missing or invalid data
    if (!timestamp || !jsonArray) {
      console.warn(`Skipping invalid row at index ${rowIndex}:`, row);
      return;
    }

    // Parse timestamp as UTC
    const [year, month, day, hour, minute, second] = timestamp.split(/[- :]/).map(Number);
    const utcTimestamp = Date.UTC(year, month - 1, day, hour, minute, second); // Parse as UTC (subtract 1 from month as Date.UTC expects 0-based months)

    const localTimestamp = new Date(utcTimestamp).toLocaleString("en-US", {
      timeZone: userTimeZone,
    });

    const localDate = new Date(localTimestamp);

    if (!isNaN(localDate)) {
      if (localDate && jsonArray) {
        try {
          // Remove surrounding quotes from the JSON array
          const cleanedJsonArray = jsonArray.replace(/^"|"$/g, "");

          // Validate and parse the JSON array
          const parsedArray = JSON.parse(cleanedJsonArray);

          if (Array.isArray(parsedArray)) {
            parsedArray.forEach((tempCelsius, index) => {
              const tempFahrenheit = (tempCelsius * 9) / 5 + 32; // Convert Celsius to Fahrenheit
              if (!airPredictionMembers[index]) airPredictionMembers[index] = [];
              airPredictionMembers[index].push([localDate.getTime(), tempFahrenheit]);
            });
          } else {
            console.warn(`Parsed value is not an array: ${cleanedJsonArray}`);
          }
        } catch (error) {
          console.error(`Error parsing JSON array: ${jsonArray} -> ${error.message}`);
        }
      }
  }
  });

  return { airPredictionMembers };
};

// CSV parsing function for second chart - different parsing approach
const parseSecondCSV = (csvText) => {
  //stuff goes here
  pass
};

// Function to toggle the dropdown menu
const toggleExportMenu = () => {
  isExportMenuVisible.value = !isExportMenuVisible.value;
};

const toggleSecondExportMenu = () => {
  isSecondExportMenuVisible.value = !isSecondExportMenuVisible.value;
}

///Fetch and update chart data every 15 minutes
let updateInterval;
onMounted(() => {
  fetchAndFilterData(); 
  fetchAndFilterSecondData();
  updateInterval = setInterval(() => {
    console.log("Fetching and updating chart data...");
    fetchAndFilterData();
    fetchAndFilterSecondData();
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

      <!-- First Chart Section -->
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
              download="TWC-Laguna-Madre_Air-Temperature-Predictions_240hrs.csv"
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

      <!-- Second Chart Section -->
      <section class="grid grid-cols-1 lg:grid-cols-5 gap-4 py-8 px-4 bg-white items-stretch">
        <!-- Chart -->
        <div class="lg:col-span-4 relative">
          <div class="w-full overflow-x-auto">
            <div class="min-w-[1000px] h-[500px] lg:h-[700px] lg:min-h-[650px]">
              <Chart class="w-full h-full p-4" :options="secondChartOptions" />
            </div>
          </div>

          <!-- Custom Export Dropdown -->
          <div class="hidden lg:block absolute top-5 right-4">
            <button @click="toggleSecondExportMenu" class="bg-navy-blue text-white px-4 py-2 rounded-lg shadow-md hover:bg-blue-700">
              Download Water Temp Data
            </button>
            <ul v-if="isSecondExportMenuVisible" class="absolute mt-2 w-48 bg-white border border-gray-300 shadow-lg rounded-lg z-50">
              <li>
                <a 
                  :href="secondCsvURL"
                  download="Water-Temperature-Forecasts.csv"
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
      </section> <!-- End of Second Chart Section -->
    </div>
</template>