<!-- ===================================================
     View: CrpsView.vue

     Description: This view displays the water temperature CRPS trends and predictions for South Bird Island.

                  Features include:
                  - A dynamically updating Highcharts spaghetti chart using live CSV data.
                  - Instructions for interacting with the chart.
                  - Information on the data of the chart.
                  - Additional links
     Author: Anointiyae Beasley, Savannah Stephenson, Christian Quintero

     Last Updated: 07/27/2025

======================================================= -->
<script setup>
import Highcharts from "highcharts";
import HighchartsMore from "highcharts/highcharts-more";
import { Chart } from "highcharts-vue";

import { ref, onMounted, onUnmounted, reactive } from "vue";

import MissingDataWarningBanner from "@/components/MissingDataWarningBanner.vue";
const missingDataWarningBanner = ref(MissingDataWarningBanner);
const isSmallScreen = window.innerWidth <= 600;


// ribbon graph
// box plot graph
const csvURL = ref(`http://localhost:8080/flare/csv-data/CRPS_120hrs.csv`);
console.log("CSV URL:", csvURL.value);




// Add reactive state for dropdown visibility
const isExportMenuVisible = ref(false);
const isSecondExportMenuVisible = ref(false);
const isThirdExportMenuVisible = ref(false);
const userTimeZone = Intl.DateTimeFormat().resolvedOptions().timeZone; 


// Define the current date and time
const nowDate = new Date(); // Current timestamp

const ribbonChartOptions = ref({});
const boxChartOptions = ref({});




// Chart function for first chart that changes based on screen size
// ribbon graph
const buildRibbonChart = (isSmallScreen) => {
  return {
    chart: {
      type: "areaspline",
      zoomType: "xy",
      backgroundColor: "white",
      style: { fontFamily: "Arial" },
      marginRight: 30,
      marginTop: 100,
    },
    title: {
      text: "Water Temperature Predictions with Uncertainty Estimates for Laguna Madre",
      style: { 
        fontSize: isSmallScreen ? "20px" : "28px", 
        fontWeight: "bold", 
        color: "#0f4f66" 
      },
      useHTML: true,
      align: 'center',
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
      plotLines: [
        {
          color: "red",
          width: 2,
          value: Date.now(),
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
      // Let Highcharts auto-calculate range with some padding
      startOnTick: true,
      endOnTick: true,
      tickInterval:15, // Major ticks every 5 units
      min: 30, // Minimum value for y-axis
      softMax: 90,
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
        // Dynamically creating the tooltip based on what series are present
        // Bounds are a special case since they are a range
        var displayInfo = ``;
        this.points.forEach(line => {
          if (line.series.name === "Bounds") {
            displayInfo += `
              <span style="color:${line.color}">\u25CF</span> 95th Percentile: <b>${line.high.toFixed(1)}°F</b><br>
              <span style="color:${line.color}">\u25CF</span> 5th Percentile: <b>${line.low.toFixed(1)}°F</b><br>`;
          }
          else
          displayInfo += `
            <span style="color:${line.color}">\u25CF</span> ${line.series.name}: <b>${line.y.toFixed(1)}°F</b><br>`;
          
        });
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
                ${displayInfo}`;
                
                
      },
      style: {
        fontSize: isSmallScreen ? "12px" : "14px", 
        padding: isSmallScreen ? "5px" : "8px", 
        color: "#0f4f66",
        fontFamily: "Arial",
      },
    },
  };
}; // end buildRibbonChart (ribbon graph)

// Chart function for box plot chart that changes based on screen size
// box plot graph
const buildBoxChart = (isSmallScreen) => {
  return {
    chart: {
      type: "boxplot",
      zoomType: "x",
      backgroundColor: "white",
      style: { fontFamily: "Arial" },
      marginRight: 30,
      marginTop: 100,
    },
    title: {
      text: "Water Temperature Predictions Box Plot for Laguna Madre",
      style: { 
        fontSize: isSmallScreen ? "20px" : "28px", 
        fontWeight: "bold", 
        color: "#0f4f66"
      },
      useHTML: true,
      align: 'center'
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
      // Let Highcharts auto-calculate range with some padding
      startOnTick: true,
      endOnTick: true,
      tickInterval: 5, // Major ticks every 5 units
    },
    series: [], // Placeholder for data, dynamically updated
    tooltip: {
      shared: true,
      crosshairs: true,
      formatter: function () {
        const localDate = new Date(this.x); 
        // Dynamically creating the tooltip based on what series are present
        // Box Plot is a special case since they have multiple values
        var displayInfo = ``;
        this.points.forEach(line => {
          if (line.series.name === "Box Plot Water Temperature Predictions") {
            displayInfo += `
              <span style="color:${line.color}">\u25CF</span> Maximum: <b>${line.high.toFixed(1)}°F</b><br>
              <span style="color:${line.color}">\u25CF</span> Upper Quartile: <b>${line.q3.toFixed(1)}°F</b><br>
              <span style="color:${line.color}">\u25CF</span> Median: <b>${line.median.toFixed(1)}°F</b><br>
              <span style="color:${line.color}">\u25CF</span> Lower Quartile: <b>${line.q1.toFixed(1)}°F</b><br>
              <span style="color:${line.color}">\u25CF</span> Minimum: <b>${line.low.toFixed(1)}°F</b><br>`;
          }
          else
          displayInfo += `
            <span style="color:${line.color}">\u25CF</span> ${line.series.name}: <b>${line.y.toFixed(1)}°F</b><br>`;
          
        });
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
                ${displayInfo}`;
                
                
      },
      style: {
        fontSize: isSmallScreen ? "12px" : "14px", 
        padding: isSmallScreen ? "5px" : "8px", 
        color: "#0f4f66",
        fontFamily: "Arial",
      },
    },
    plotOptions: {
      line: {
        lineWidth: 3
      },
      spline: {
      lineWidth: 3,
      },
    },
  }
} // end buildBoxChart (box plot graph)

ribbonChartOptions.value = reactive(buildRibbonChart(isSmallScreen));
boxChartOptions.value = reactive(buildBoxChart(isSmallScreen));




// Function to fetch and process second CSV data
const fetchAndFilterData = async () => {
  try {
    // Fetch CSV data
    const response = await fetch(csvURL.value);
    if (!response.ok) throw new Error("Failed to fetch ribbon CSV data");

    const csvText = await response.text();
    console.log("Fetched CSV data:", csvText); // Debug log`

    // Parse the CSV data for the ribbon chart
    const parsedData = parseCSV(csvText);

    // Ensure parsed arrays are initialized
    const waterMeasurements = parsedData.waterMeasurements || [];
    const airPredictions = parsedData.airPredictions || [];
    const waterPredictionsPercentile5 = parsedData.waterPredictionsPercentile5 || [];
    const waterPredictionsPercentile25 = parsedData.waterPredictionsPercentile25 || [];
    const waterPredictionsPercentile50 = parsedData.waterPredictionsPercentile50 || [];
    const waterPredictionsPercentile75 = parsedData.waterPredictionsPercentile75 || [];
    const waterPredictionsPercentile95 = parsedData.waterPredictionsPercentile95 || [];
    const waterPredictionsPercentileMin = parsedData.waterPredictionsPercentileMin || [];
    const waterPredictionsPercentileMax = parsedData.waterPredictionsPercentileMax || [];

    
    // Convert to Fahrenheit
    // and round to 1 decimal
    const toFahrenheit = (celsius) => (celsius * 9/5) + 32;
    const waterMeasurementsFahrenheit = waterMeasurements.map(([time, celsius]) => [time, +toFahrenheit(celsius).toFixed(1)]);
    const airPredictionsFahrenheit = airPredictions.map(([time, celsius]) => [time, +toFahrenheit(celsius).toFixed(1)]);
    const waterPredictionsPercentile5Fahrenheit = waterPredictionsPercentile5.map(([time, celsius]) => [time, +toFahrenheit(celsius).toFixed(1)]);
    const waterPredictionsPercentile25Fahrenheit = waterPredictionsPercentile25.map(([time, celsius]) => [time, +toFahrenheit(celsius).toFixed(1)]);
    const waterPredictionsPercentile50Fahrenheit = waterPredictionsPercentile50.map(([time, celsius]) => [time, +toFahrenheit(celsius).toFixed(1)]);
    const waterPredictionsPercentile75Fahrenheit = waterPredictionsPercentile75.map(([time, celsius]) => [time, +toFahrenheit(celsius).toFixed(1)]);
    const waterPredictionsPercentile95Fahrenheit = waterPredictionsPercentile95.map(([time, celsius]) => [time, +toFahrenheit(celsius).toFixed(1)]);
    const waterPredictionsPercentileMinFahrenheit = waterPredictionsPercentileMin.map(([time, celsius]) => [time, +toFahrenheit(celsius).toFixed(1)]);
    const waterPredictionsPercentileMaxFahrenheit = waterPredictionsPercentileMax.map(([time, celsius]) => [time, +toFahrenheit(celsius).toFixed(1)]);

    const futureAirPredictionsFahrenheit =
      airPredictionsFahrenheit.filter(([time]) => time >= Date.now());

    // === Calculate bounds for the ribbon chart ===
    // Outer Ribbon(5th-95th)
    const outerBoundsFahrenheit = waterPredictionsPercentile5Fahrenheit.map((point, index) => {
    const time = point[0];
    const low = waterPredictionsPercentile5Fahrenheit[index][1];
    const high = waterPredictionsPercentile95Fahrenheit[index][1];

    return [time, low, high];
    });
    // Inner ribbon (25th-75th)
    const innerBoundsFahrenheit = waterPredictionsPercentile25Fahrenheit.map((point, index) => {
    const time = point[0];
    const low = waterPredictionsPercentile25Fahrenheit[index][1];
    const high = waterPredictionsPercentile75Fahrenheit[index][1];

    return [time, low, high];
    });

    // === Calculate bounds for the box plot chart ===
    // Fences from min to max
    const boxPlotBoundsFahrenheit = waterPredictionsPercentileMinFahrenheit.map((point, index) => {
      const time = point[0];
      const low = waterPredictionsPercentileMinFahrenheit[index][1];
      const q1 = waterPredictionsPercentile25Fahrenheit[index][1];
      const median = waterPredictionsPercentile50Fahrenheit[index][1];
      const q3 = waterPredictionsPercentile75Fahrenheit[index][1];
      const high = waterPredictionsPercentileMaxFahrenheit[index][1];

      return [time, low, q1, median, q3, high];
    });


   
    // Update chart series with filtered data
    ribbonChartOptions.value.series = [

      {
        name: "Water Temperature Measurements",
        data: waterMeasurementsFahrenheit,
        type: "line",
        color: "black",
        lineWidth: isSmallScreen ? 2 : 4,
        zIndex: 1, // Ensure this is in front of the bounds
        marker: { enabled: false },
      },
      {
        name: "NDFD Air Temperature Predictions",
        data: futureAirPredictionsFahrenheit,
        type: "line",
        color: "purple",
        lineWidth: isSmallScreen ? 2 : 4,
        zIndex: 1, // Ensure this is in front of the bounds
        marker: { enabled: false },
      },
      {
        name: "Median (50th Percentile) Water Temperature Predictions",
        data: waterPredictionsPercentile50Fahrenheit,
        type: "line",
        color: "#5F98CA",
        lineWidth: isSmallScreen ? 2 : 4,
        zIndex: 3, // Ensure this is in front of the bounds
        marker: { enabled: true},
      },
      
      {
        name: '25th-75th Percentile',
        type: 'arearange',
        data: innerBoundsFahrenheit,
        color: '#9ACDFF',
        lineWidth: 1,
        marker: { enabled: false },
        zIndex: 1
      },
      {
        name: '5th-95th Percentile',
        type: 'arearange',
        data: outerBoundsFahrenheit,
        color: '#DDEEFF',
        lineWidth: 1,
        marker: { enabled: false },
        zIndex: 0
      },
    ];

    boxChartOptions.value.series = [
      {
        name: "NDFD Air Temperature Predictions",
        data: airPredictionsFahrenheit,
        type: "line",
        color: "purple",
        lineWidth: isSmallScreen ? 2 : 4,
        zIndex: 1, // Ensure this is in front of the bounds
        marker: { enabled: false },
      },
      {
        name: "Median (50th Percentile) Water Temperature Predictions",
        data: waterPredictionsPercentile50Fahrenheit,
        type: "line",
        color: "#4A90E2",
        lineWidth: isSmallScreen ? 3 : 5,
        zIndex: 1, // Ensure this is in front of the bounds
        marker: { enabled: false },
      },
      {
        name: 'Prediction Range (Box: 25th-75th Percentiles; Fence: Min/Max)',
        type: 'boxplot',
        data: boxPlotBoundsFahrenheit,
        lineWidth: 2,
        whiskerLength: '50%',
        medianColor: '#000000',
        stemColor: '#4A90E2',
        whiskerColor: '#4A90E2',
        color: '#4A90E2',
        fillColor: 'rgba(74,144,226,0.35)'
      }
    ];
  } catch (error) {
    console.error("Error fetching or processing data:", error);
  }
}; // end fetchAndFilterData


// CSV parsing function for ribbon chart
const parseCSV = (csvText) => {
  const rows = csvText.split("\n").map((row) => row.split(","));
  const waterMeasurements = [];
  const airPredictions = [];
  const waterPredictionsPercentile5= [];
  const waterPredictionsPercentile25 = [];
  const waterPredictionsPercentile50 = [];
  const waterPredictionsPercentile75 = [];
  const waterPredictionsPercentile95 = [];
  const waterPredictionsPercentileMin = [];
  const waterPredictionsPercentileMax = [];


  rows.forEach((row, index) => {
    // Skip the header row
    if (index === 0) return;

    const [
      timestamp,
      waterMeasurementValue,
      airPredictionValue,
      percentile5Value,
      percentile25Value,
      percentile50Value,
      percentile75Value,
      percentile95Value,
      minValue,
      maxValue
    ] = row;
    // Parse timestamp as UTC
    const [year, month, day, hour, minute, second] = timestamp.split(/[- :]/).map(Number);
    const utcTimestamp = Date.UTC(year, month - 1, day, hour, minute, second); // Parse as UTC (subtract 1 from month as Date.UTC expects 0-based months)
    const localTimestamp = new Date(utcTimestamp).toLocaleString("en-US", {
      timeZone: userTimeZone,
    });
    const localDate = new Date(localTimestamp);

    if (!isNaN(localDate)) {
      if (waterMeasurementValue && !isNaN(+waterMeasurementValue)) {
        waterMeasurements.push([localDate.getTime(), +waterMeasurementValue]);
      }
      if (airPredictionValue && !isNaN(+airPredictionValue)) {
        airPredictions.push([localDate.getTime(), +airPredictionValue]);
      }
      if (percentile5Value && !isNaN(+percentile5Value)) {
        waterPredictionsPercentile5.push([localDate.getTime(), +percentile5Value]);
      }
      if (percentile25Value && !isNaN(+percentile25Value)) {
        waterPredictionsPercentile25.push([localDate.getTime(), +percentile25Value]);
      }
      if (percentile50Value && !isNaN(+percentile50Value)) {
        waterPredictionsPercentile50.push([localDate.getTime(), +percentile50Value]);
      }
      if (percentile75Value && !isNaN(+percentile75Value)) {
        waterPredictionsPercentile75.push([localDate.getTime(), +percentile75Value]);
      }
      if (percentile95Value && !isNaN(+percentile95Value)) {
        waterPredictionsPercentile95.push([localDate.getTime(), +percentile95Value]);
      }
      if (minValue && !isNaN(+minValue)) {
        waterPredictionsPercentileMin.push([localDate.getTime(), +minValue]);
      }
      if (maxValue && !isNaN(+maxValue)) {
        waterPredictionsPercentileMax.push([localDate.getTime(), +maxValue]);
      }

    }
  });

  return {
    waterMeasurements,
    airPredictions,
    waterPredictionsPercentile5,
    waterPredictionsPercentile25,
    waterPredictionsPercentile50,
    waterPredictionsPercentile75,
    waterPredictionsPercentile95,
    waterPredictionsPercentileMin,
    waterPredictionsPercentileMax
  };
}; // end parseRibbonCSV


// Function to toggle the dropdown menu
const toggleExportMenu = () => {
  isExportMenuVisible.value = !isExportMenuVisible.value;
};

const toggleSecondExportMenu = () => {
  isSecondExportMenuVisible.value = !isSecondExportMenuVisible.value;
}


///Fetch and update chart data every 15 minutes
onMounted(() => {
  Promise.all([
    fetchAndFilterData()
  ]).then(() => {
    missingDataWarningBanner.value.checkForMissingDataAndWarn([ribbonChartOptions.value, boxChartOptions.value]);
  });

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
          class="w-full h-full object-cover flex opacity-30"
        />
        <!-- Text content overlay -->
        <div class="absolute  inset-0 flex items-center justify-center">
          <h1 class=" max-w-[1500px] text-lg md:text-3xl lg:text-5xl font-bold text-center pr-5 pl-5">
            CRPS Water Temperature Trends and Forecasts for the Texas Upper Laguna Madre
          </h1>
        </div>
      </div>
      </section>
      <MissingDataWarningBanner ref="missingDataWarningBanner" />
      <!-- First Chart Section: Spaghetti Graph -->
      <section class="grid grid-cols-1 lg:grid-cols-5 gap-4 py-8 px-4 bg-white items-stretch">
        <!-- Chart -->
        <div class="lg:col-span-4 relative">
          <div class="w-full overflow-x-auto">
            <div class="min-w-[1000px] h-[500px] lg:h-[700px] lg:min-h-[650px]">
              <Chart class="w-full h-full p-4" :options="ribbonChartOptions" />
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
                  download="CRPS_120hrs.csv"
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
              <p>If you zoom in and want to go back to the original chart view, click the Reset View button in the top-right corner.</p>
            </li>
            <h3 class="text-lg lg:text-xl font-bold text-center">Show or Hide Chart Lines:</h3>
            <li class="flex items-start space-x-2">
              <span class="text-blue-secondary">👆</span>
              <p>Click on a label in the legend below the chart to turn a specific data series line or category on or off.</p>
            </li>
          </ul>
        </div>
      </section>

      <!-- Second Chart Section: Ribbon Graph -->
      <section class="grid grid-cols-1 lg:grid-cols-5 gap-4 py-8 px-4 bg-white items-stretch">
        <!-- Chart -->
        <div class="lg:col-span-4 relative">
          <div class="w-full overflow-x-auto">
            <div class="min-w-[1000px] h-[500px] lg:h-[700px] lg:min-h-[650px]">
              <Chart class="w-full h-full p-4" :options="boxChartOptions" />
            </div>
          </div>

          <!-- Custom Export Dropdown -->
          <div class="hidden lg:block absolute top-5 right-4">
            <button @click="toggleSecondExportMenu" class="bg-navy-blue text-white px-4 py-2 rounded-lg shadow-md hover:bg-blue-700">
              Download CSV
            </button>
            <ul v-if="isSecondExportMenuVisible" class="absolute mt-2 w-48 bg-white border border-gray-300 shadow-lg rounded-lg z-50">
              <li>
                <a 
                  :href="csvURL"
                  download="CRPS_120hrs.csv"
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
              <p>If you zoom in and want to go back to the original chart view, click the Reset View button in the top-right corner.</p>
            </li>
            <h3 class="text-lg lg:text-xl font-bold text-center">Show or Hide Chart Lines:</h3>
            <li class="flex items-start space-x-2">
              <span class="text-blue-secondary">👆</span>
              <p>Click on a label in the legend below the chart to turn a specific data series line or category on or off.</p>
            </li>
          </ul>
        </div>
      </section> <!-- End of Second Chart Section: Ribbon Graph -->
    </div>

    <!-- Section Divider -->
    <div class="h-[50px] bg-section-gradient"></div>
        <!-- CRPS Explanation Section -->
        <section class="bg-white py-10 px-6 md:px-20 text-center lg:text-left">
        <div class="max-w-5xl mx-auto">
            <h2 class="text-lg lg:text-3xl font-extrabold text-dark-text mb-6 text-center">
            Understanding the CRPS AI Ensemble Model
            </h2>
                 <p class="text-md lg:text-xl text-dark-text mb-4">
                  The CRPS (Continuous Ranked Probability Score) ensemble model provides probabilistic water temperature forecasts rather than a single predicted value. Instead of producing one forecasted temperature, the model generates a distribution of possible water temperatures, allowing users to view both the median forecast and the uncertainty surrounding it.
                </p>

                <p class="text-md lg:text-xl text-dark-text mb-4">
                 To estimate this uncertainty, the CRPS Ensemble system uses 100 air temperature forecast scenarios provided by The Weather Company. For each scenario, an ensemble of 10 CRPS AI models generates water temperature forecasts, with each model producing 100 possible water temperature outcomes. These predictions are combined across atmospheric scenarios, AI models, and 21 forecast lead times to create a probabilistic forecast of water temperature for the Laguna Madre.
                </p>

                <p class="text-md lg:text-xl text-dark-text mb-4">
                  These outcomes are combined to produce a forecast distribution for water temperature in the Laguna Madre. The charts above display the median forecast along with percentile ranges that summarize the spread of possible outcomes. Narrower ranges indicate greater agreement among predictions, while wider ranges indicate greater forecast uncertainty.
                </p>

                <p class="text-md lg:text-xl text-dark-text mb-4">
                  By visualizing both the median forecast and the range of possible water temperatures, the CRPS model helps coastal stakeholders involved with managing ecological and economic cold-stunning event impacts better understand water temperature forecast uncertainty when planning for changing environmental conditions.
                </p>

        </div>
        </section>



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