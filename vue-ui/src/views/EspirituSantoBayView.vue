<!-- ===================================================
     View: CrpsView.vue

     Description: This view displays the water temperature CRPS trends and predictions for South Bird Island.

                  Features include:
                  - 3 dynamically updating charts
                  - Instructions for interacting with the chart.
                  - Information on the data of the chart.
                  - Additional links
     Author: Anointiyae Beasley

     Last Updated: 07/29/2026

======================================================= -->
<script setup>
import { Chart } from "highcharts-vue";
import Highcharts from "highcharts";
import HighchartsMore from "highcharts/highcharts-more";
import { ref, onMounted, onUnmounted, reactive } from "vue";

import MissingDataWarningBanner from "@/components/MissingDataWarningBanner.vue";
const missingDataWarningBanner = ref(MissingDataWarningBanner);
const isSmallScreen = window.innerWidth <= 600;


// ribbon graph
// box plot graph
const csvURL = ref(`http://localhost:8080/flare/csv-data/espiritu-santo-bay.csv`);
const showChartHelp = ref(false);




// Add reactive state for dropdown visibility
const isExportMenuVisible = ref(false);
const isSecondExportMenuVisible = ref(false);
const userTimeZone = Intl.DateTimeFormat().resolvedOptions().timeZone; 
let chartTitle = "";

const chartOptions = ref({});


// Chart function for first chart that changes based on screen size
// ribbon graph
const buildChart = (isSmallScreen, chartTitle) => {
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
      text: chartTitle,
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
          const time = localDate.toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit", hour12: true }); 
          return `<span style="display: block; text-align: center; font-family: Arial;">
                    <b>${day}</b><br>${date}<br><i>${time}</i>
                  </span>`;
        },
        useHTML: true,
        style: {
          fontSize: isSmallScreen ? "10px" : "16px", 
          fontFamily: "Arial",
          color: "#0f4f66",
          whiteSpace: "nowrap",
        },
      },
      tickInterval: 12 * 3600 * 1000, // Main ticks every 12 hours

// Align ticks to 12 AM and 12 PM
tickPositioner: function () {
  const positions = [];
  const hours = 24 * 3600 * 1000;
  const timezoneOffset =
    new Date().getTimezoneOffset() * 60 * 1000;

  let tick =
    Math.ceil(
      (this.min - timezoneOffset) / hours
    ) *
      hours +
    timezoneOffset;

  while (tick <= this.max) {
    positions.push(tick);
    tick += hours;
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
      tickInterval: 10, // Major ticks every 10 units
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
        let displayInfo = "";

        this.points.forEach(point => {

            if (point.series.type === "arearange") {
              if (point.series.name === "5th-95th Percentile") {  
                displayInfo += `
                    <span style="color:${point.color}">\u25CF</span>
                    <b>${point.series.name}</b><br>
                    &nbsp;&nbsp;High(95%): <b>${point.high.toFixed(1)}°F</b><br>
                    &nbsp;&nbsp;Low(5%): <b>${point.low.toFixed(1)}°F</b><br> `;
              }
              else if (point.series.name === "25th-75th Percentile") {
                displayInfo += `
                    <span style="color:${point.color}">\u25CF</span>
                    <b>${point.series.name}</b><br>
                    &nbsp;&nbsp;High(75%): <b>${point.high.toFixed(1)}°F</b><br>
                    &nbsp;&nbsp;Low(25%): <b>${point.low.toFixed(1)}°F</b><br> `;
              }
              else {
                displayInfo += `
                <span style="color:${point.color}">\u25CF</span>
                    <b>${point.series.name}</b><br>
                    &nbsp;&nbsp;High: <b>${point.high.toFixed(1)}°F</b><br>
                    &nbsp;&nbsp;Low: <b>${point.low.toFixed(1)}°F</b><br> `;
              }

                

            } else {

                displayInfo += `
                    <span style="color:${point.color}">\u25CF</span>
                    ${point.series.name}: <b>${point.y.toFixed(1)}°F</b><br>`;
            }
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
        fontSize: isSmallScreen ? "10px" : "12px", 
        padding: isSmallScreen ? "5px" : "8px", 
        color: "#0f4f66",
        fontFamily: "Arial",
      },
    },
  };
}; // end buildChart 

chartOptions.value = reactive(buildChart(isSmallScreen, "Water Temperature Trends and Forecasts"));



// Function to fetch and process second CSV data
const fetchAndFilterData = async () => {
  try {
    // Fetch CSV data
    const response = await fetch(csvURL.value);
    if (!response.ok) throw new Error("Failed to fetch ribbon CSV data");

    const csvText = await response.text();


    // Parse the CSV data for the ribbon chart
    const parsedData = parseCSV(csvText);

    const seadriftMeasurements =
      parsedData.seadriftMeasurements || [];

    const portOConnorMeasurements =
      parsedData.portOConnorMeasurements || [];

    const portLavacaMeasurements =
      parsedData.portLavacaMeasurements || [];

    const wildlifeRefugeMeasurements =
      parsedData.wildlifeRefugeMeasurements || [];

    const waterPredictions =
      parsedData.waterPredictions || [];

    
    // Convert to Fahrenheit
    // and round to 1 decimal
    const toFahrenheit = (celsius) => {
      return (celsius * 9 / 5) + 32;
    };

    const convertSeriesToFahrenheit = (data) => {
      return data.map(([time, celsius]) => [
        time,
        Number(toFahrenheit(celsius).toFixed(1))
      ]);
    };

    const seadriftMeasurementsFahrenheit =
      convertSeriesToFahrenheit(seadriftMeasurements);

    const portOConnorMeasurementsFahrenheit =
      convertSeriesToFahrenheit(portOConnorMeasurements);

    const portLavacaMeasurementsFahrenheit =
      convertSeriesToFahrenheit(portLavacaMeasurements);

    const wildlifeRefugeMeasurementsFahrenheit =
      convertSeriesToFahrenheit(wildlifeRefugeMeasurements);

    const waterPredictionsFahrenheit =
      convertSeriesToFahrenheit(waterPredictions);


   
    // Update chart series with filtered data
    chartOptions.value.series = [
    {
      name: "Seadrift Water Temperature Measurements",
      data: seadriftMeasurementsFahrenheit,
      type: "line",
      color: "#000000",
      lineWidth: isSmallScreen ? 1 : 2,
      zIndex: 1,
      marker: {
        enabled: false
      }
    },
    {
      name: "Port O'Connor Water Temperature Measurements",
      data: portOConnorMeasurementsFahrenheit,
      type: "line",
      color: "#0072B2",
      lineWidth: isSmallScreen ? 1 : 2,
      zIndex: 1,
      marker: {
        enabled: false
      }
    },
    {
      name: "Port Lavaca Water Temperature Measurements",
      data: portLavacaMeasurementsFahrenheit,
      type: "line",
      color: "#009E73",
      lineWidth: isSmallScreen ? 1 : 2,
      zIndex: 1,
      marker: {
        enabled: false
      }
    },
    {
      name: "Aransas Wildlife Refuge Water Temperature Measurements",
      data: wildlifeRefugeMeasurementsFahrenheit,
      type: "line",
      color: "#CC79A7",
      lineWidth: isSmallScreen ? 1 : 2,
      zIndex: 1,
      marker: {
        enabled: false
      }
    },
    {
      name: "ESB Water Temperature Predictions",
      data: waterPredictionsFahrenheit,
      type: "line",
      color: "#D55E00",
      dashStyle: "LongDash",
      lineWidth: isSmallScreen ? 1 : 2,
      zIndex: 3,
      marker: {
        enabled: false
      }
    }
  ];
    
  } catch (error) {
    console.error("Error fetching or processing data:", error);
  }
}; // end fetchAndFilterData


// CSV parsing function 
const parseCSV = (csvText) => {
  // Split the CSV into rows and columns.
  const rows = csvText
    .trim()
    .split("\n")
    .map((row) => row.trim().split(","));

  // Arrays that will hold each chart series.
  const seadriftMeasurements = [];
  const portOConnorMeasurements = [];
  const portLavacaMeasurements = [];
  const wildlifeRefugeMeasurements = [];
  const waterPredictions = [];

  // Add a point only when the CSV cell contains a valid number.
  const addDataPoint = (dataArray, timestamp, value) => {
    const numericValue = Number(value);

    if (value !== "" && !isNaN(numericValue)) {
      dataArray.push([timestamp, numericValue]);
    }
  };

  // Start at 1 to skip the header row.
  for (let index = 1; index < rows.length; index++) {
    const row = rows[index];

    // Assign each CSV column based on its position.
    const timestamp = row[0];
    const seadriftValue = row[1];
    const portOConnorValue = row[2];
    const portLavacaValue = row[3];
    const wildlifeRefugeValue = row[4];
    const waterPredictionValue = row[5];

    // Skip rows without a timestamp.
    if (!timestamp) {
      continue;
    }

    // Break "2026-08-27 10:30:00" into date parts.
    const dateParts = timestamp.split(/[- :]/).map(Number);

    const year = dateParts[0];
    const month = dateParts[1];
    const day = dateParts[2];
    const hour = dateParts[3];
    const minute = dateParts[4];
    const second = dateParts[5];

    // Create a UTC timestamp in milliseconds.
    const utcTimestamp = Date.UTC(
      year,
      month - 1,
      day,
      hour,
      minute,
      second
    );

    // Skip rows with an invalid timestamp.
    if (isNaN(utcTimestamp)) {
      continue;
    }

    // Add the values to their matching chart arrays.
    addDataPoint(
      seadriftMeasurements,
      utcTimestamp,
      seadriftValue
    );

    addDataPoint(
      portOConnorMeasurements,
      utcTimestamp,
      portOConnorValue
    );

    addDataPoint(
      portLavacaMeasurements,
      utcTimestamp,
      portLavacaValue
    );

    addDataPoint(
      wildlifeRefugeMeasurements,
      utcTimestamp,
      wildlifeRefugeValue
    );

    addDataPoint(
      waterPredictions,
      utcTimestamp,
      waterPredictionValue
    );
  }

  return {
    seadriftMeasurements,
    portOConnorMeasurements,
    portLavacaMeasurements,
    wildlifeRefugeMeasurements,
    waterPredictions
  };
};// end parseRibbonCSV


// Function to toggle the dropdown menu
const toggleExportMenu = () => {
  isExportMenuVisible.value = !isExportMenuVisible.value;
};


///Fetch and update chart data every 15 minutes
let updateInterval;

onMounted(() => {
  const loadCharts = () => {
    Promise.all([
      fetchAndFilterData()
    ]).then(() => {
      missingDataWarningBanner.value.checkForMissingDataAndWarn([
        chartOptions.value,
      ]);
    });
  };

  // Initial load
  loadCharts();

  // Refresh every 15 minutes
  updateInterval = setInterval(loadCharts, 900000);
});

onUnmounted(() => {
  clearInterval(updateInterval);
});


</script>
 
<template>
    <div class="overflow-hidden  text-dark-text font-main">

      <!-- Banner Section -->
      <section class="bg-banner-gradient-2 w-full text-white h-[200px] lg:h-[250px]">
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
            Water Temperature Trends and Forecasts for Espiritu Santo Bay, TX
          </h1>
        </div>
      </div>
      </section>
      <MissingDataWarningBanner ref="missingDataWarningBanner" />

       <!-- How to Use Chart Section -->
      <div class="flex justify-end mb-3 pr-8 pt-3 ">
        <div class="relative inline-block">

          <button
            @click="showChartHelp = !showChartHelp"
            class="flex items-center gap-2 text-blue-secondary hover:text-blue-600 font-medium"
          >
            <span
              class="flex items-center justify-center w-6 h-6 rounded-full border-2 border-current font-bold text-xs lg:text-sm"
            >
              ?
            </span>

            <span class="text-xs md:text-lg">How to Use the Interactive Chart</span>
          </button>

          <div
            v-show="showChartHelp"
            class="chart-help-popup absolute bottom-5 right-0 w-full max-h-[150px] lg:max-h-[250px] overflow-y-auto mb-3 lg:w-[450px] bg-white rounded-sm shadow-2xl border border-gray-300 p-6 z-50 "
          >
            <h2 class=" text-l lg:text-xl font-semibold border-b pb-2 mb-4">
              How to Use the Interactive Chart
            </h2>

            <div class="space-y-5">
              <div>
                <h3 class="font-bold">📊 See Temperature Details</h3>
                <p>
                  Move your mouse over any line to display the exact
                  temperature, date, and time.
                </p>
              </div>

              <div>
                <h3 class="font-bold">🔄 Reset the View</h3>
                <p>
                  After zooming, click <strong>Reset View</strong> in the
                  upper-right corner of the chart.
                </p>
              </div>

              <div>
                <h3 class="font-bold">👆 Show or Hide Chart Lines</h3>
                <p>
                  Click a legend item below the chart to toggle a data series.
                </p>
              </div>

              <div>
                <h3 class="font-bold">👆Time</h3>
                <p>
                  Time is relevant to the user's local timezone.
                </p>
              </div>
            </div>
          </div>

        </div>            
      </div>
      <!-- First Chart Section-->
      <section class="grid grid-cols-1 lg:grid-cols-5 gap-2  px-2 lg:py-8 lg:px-4 bg-white items-stretch">
        <!-- Chart -->
        <div class="chart lg:col-span-4 relative border sm:w-full ">
          <div class="w-full overflow-x-auto">
            <div class="min-w-[600px]  min-h-[350px] lg:min-w-[1000px] lg:h-[700px] lg:min-h-[650px]">
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
                  download="espiritu-santo-bay.csv"
                  class="px-4 py-2 hover:bg-gray-100 cursor-pointer block">
                  Download CSV
                </a>
              </li>
            </ul>
          </div>
        </div>

        <!-- Graph Information -->
        <div class="graph-info max-h-[500px] lg:max-h-[750px] p-6 rounded-lg flex flex-col">
          <h2 class="text-lg lg:text-3xl font-semibold text-center text-dark-text border-b-2 border-dark-text pb-2 mb-6">
            Graph-Specific Information
          </h2>

          <!-- Scrollable Content -->
          <div class="graph-scroll flex-1 overflow-y-auto space-y-8 text-dark-text pr-2">

            <!-- Purpose -->
            <div>
              <h3 class="text-lg lg:text-xl font-bold mb-2">
                Purpose
              </h3>

              <p class="leading-relaxed">
                Shows recent observed temperatures alongside an AI water temperature forecast and NWS-NDFD air temperature forecasts. This provides a simple view of how water temperatures are expected to change over the next five days.
              </p>
            </div>
            <hr class="border-t border-dark-text">

            
            <div>
              <h3 class="text-lg lg:text-xl font-bold mb-2">
                How to Read
              </h3>

              <ul class="list-disc list-inside space-y-2 text-dark-text">
                <li>
                  The black dashed line shows the water temperature forecast from the AI model predictions.
                </li>
                <li>
                  The vertical “Now” line separates recent temperature observations from future predictions.
                </li>
              </ul>
            </div>
            <hr class="border-t border-dark-text">

           
            <div>
              <h3 class="text-lg lg:text-xl font-bold mb-2">
                What to Look For
              </h3>

              <p class="leading-relaxed">
                Best for tracking the predicted water temperature trend and observing whether it approaches, crosses, or remains below critical cold-stunning thresholds.
              </p>
            </div>

             <hr class="border-t border-dark-text">

            <div>
              <h3 class="text-lg lg:text-xl font-bold mb-2">
                Keep in Mind
              </h3>

              <p class="leading-relaxed">
                This forecast shows only one possible outcome and does not display the uncertainty of the AI water temperature predictions.
              </p>
            </div>

          </div>
        </div>
      </section>
      <div class="h-[30px] bg-gray-100"></div>
    </div>

    <!-- Section Divider -->
    <div class="h-[50px] bg-section-gradient"></div>

    <!-- About Section -->
    <section class="grid grid-cols-1 lg:grid-cols-2 bg-white py-10 px-6 md:px-20 gap-10 items-center">
        <!-- Image Section -->
        <div class="flex flex-col items-center">
          <div class="flex justify-center">
            <img 
              src="@/assets/images/ESB.jpg" 
              alt="Map of Laguna Madre, Texas" 
              class="w-[90%] h-auto rounded-lg shadow-lg"
            >
          </div>
          <p class="text-xs text-center text-gray-600 mt-2">
            Map courtesy of Western Michigan University via Avenza Maps.
          </p>
        </div>


        <!-- Text Content Section -->
        <div class="text-center lg:text-left">
          <h2 class="text-lg lg:text-3xl font-extrabold text-center text-dark-text mb-6">
            Espiritu Santo Bay AI Water Temperature Model
          </h2>

          <p class="text-md lg:text-xl text-dark-text mb-4">
            Espiritu Santo Bay is a shallow coastal system connected to San Antonio Bay
            and the Gulf of Mexico. During the cold-front season, typically November
            through March, its shallow waters can cool rapidly and place green sea turtles
            and other marine life at risk. When water temperatures approach or fall below
            8°C, green sea turtles may become cold-stunned, leaving them weak, lethargic,
            and vulnerable to prolonged cold exposure, vessel strikes, and predation.
          </p>

          <p class="text-md lg:text-xl text-dark-text mb-4">
            Preparing for these events requires time to organize volunteers, deploy rescue
            boats, coordinate field operations, and arrange transportation to
            rehabilitation facilities. The Espiritu Santo Bay water temperature model was
            developed to provide advance guidance about when hazardous water temperatures
            may occur. It produces water temperature predictions up to 120 hours, or five
            days, into the future, helping responders and other stakeholders anticipate
            the possible onset, severity, and duration of cold-water conditions.
          </p>

          <h3 class="text-lg lg:text-2xl font-bold text-dark-text mt-6 mb-3">
            Supporting Cold-Stunning Preparation
          </h3>

          <p class="text-md lg:text-xl text-dark-text mb-4">
            By providing several days of advance notice, the model can help sea turtle
            responders determine when to increase monitoring, begin coordinating personnel
            and equipment, prepare vessels, and plan the transportation and rehabilitation
            of recovered turtles. The predictions may also support broader coordination
            among organizations whose environmental, economic, or recreational activities
            could be affected by extreme cold conditions in and around the bay.
          </p>

          <h3 class="text-lg lg:text-2xl font-bold text-dark-text mt-6 mb-3">
            Development and Collaboration
          </h3>

          <p class="text-md lg:text-xl text-dark-text mb-4">
            The Espiritu Santo Bay model was developed through the Coastal Dynamics Lab at
            Texas A&amp;M University–Corpus Christi. Hector Marrero-Colominas and Ayesha
            Khan led the model’s development, with assistance from Drs. Miranda White and
            Philippe Tissot. The model is currently maintained by the CDL Semaphore Team.
          </p>

          <p class="text-md lg:text-xl text-dark-text mb-4">
            Foundational field observations were made possible through collaboration with
            <strong>Mid-Coast Sea Turtle Rescue</strong> and
            <strong>NOAA Fisheries</strong>. These efforts included multiple boat trips to
            deploy air and water temperature sensors within Espiritu Santo Bay, providing
            preliminary measurements that informed the design of the model.
          </p>

          <p class="text-md lg:text-xl text-dark-text mb-4">
            The resulting prediction system reflects a collaborative effort among
            university AI researchers, network partners, sea turtle responders, and other
            coastal stakeholders working to improve preparation for cold-stunning events.
          </p>

        </div>
    </section>

     <!-- Information Section -->



    <!--  MOBILE -->

    <div
      class="fixed inset-x-0 bottom-0 z-50"
    >

      <!-- Always-visible Handle -->
      <button
        @click="showInfoDrawer = !showInfoDrawer"
        class="w-full bg-navy-blue text-white shadow-xl py-3"
      >
        <div class="w-12 h-1 bg-gray-300 rounded-full mx-auto mb-2"></div>

        <div class="font-semibold">
          {{ showInfoDrawer ? "Hide Additional Information ▼" : "Additional Information ▲" }}
        </div>
      </button>

      <transition
        enter-active-class="transition-transform duration-300 ease-out"
        leave-active-class="transition-transform duration-300 ease-in"
        enter-from-class="translate-y-full"
        enter-to-class="translate-y-0"
        leave-from-class="translate-y-0"
        leave-to-class="translate-y-full"
      >
        <div
          v-if="showInfoDrawer"
          class="bg-blue-50
                max-h-[75vh]
                overflow-y-auto
                shadow-2xl
                p-5"
        >

          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">

            <!-- LEFT CARD -->
              <div class="lg:col-span-1 bg-white p-6 rounded-lg shadow-md">
          <h3 class="text-xl lg:text-2xl font-extrabold text-center lg:text-left text-dark-text border-b-2 border-gray-500 pb-2 mb-3 lg:pb-4 lg:mb-6">
            Data on this Graph:
          </h3>
          <ul class="list-disc list-inside space-y-2 text-md lg:text-xl text-dark-text">
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
            Additional Information:
          </h3>
          <ul class="list-disc space-y-2 pl-5 text-md lg:text-xl text-dark-text">
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
              CRPS (Continuous Ranked Probability Score) ensemble model from Semaphore available
              <router-link 
                to="/crps" 
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

          </div>

        </div>

      </transition>

    </div>


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
          <a href="https://www.nps.gov/index.htm" target="_blank" class="hover:scale-110 transition-transform">
            <img class="max-w-[80px] lg:max-w-[150px]" src="@/assets/images/NPS-Logo.png" alt="National Park Service Logo">
          </a>
          <a href="https://www.weather.gov/" target="_blank" class="hover:scale-110 transition-transform">
            <img src="@/assets/images/NWS-Logo.png" alt="National Weather Service Logo" class="max-w-[80px] lg:max-w-[150px]">
          </a>
          <a href="https://www.uscg.mil/" target="_blank" class="hover:scale-110 transition-transform">
            <img  src="@/assets/images/CG-Logo.png" alt="USA Coast Guard Logo" class="max-w-[80px] lg:max-w-[150px]">
          </a>
          <a href="https://www.joincca.org/" target="_blank" class="hover:scale-110 transition-transform">
            <img src="@/assets/images/CCA-Logo.png" alt="Coastal Conservation Association Logo" class="max-w-[80px] lg:max-w-[150px]">
          </a>
        </div>
        <p class="text-center text-sm text-light-text">(Click on the logos to visit each contributor's website)</p>
      </footer>
</template>

<style scoped>
  .chart-help-popup::-webkit-scrollbar {
  width: 10px;
}

.chart-help-popup::-webkit-scrollbar-track {
  background: #818183;
}

.chart-help-popup::-webkit-scrollbar-thumb {
  background: #5F98CA;
  border-radius: 9999px;
}

.chart-help-popup::-webkit-scrollbar-thumb:hover {
  background: #4a82b3;
}

.chart-info-section::-webkit-scrollbar {
  width: 10px;
}

.chart-info-section::-webkit-scrollbar-track {
  background: #818183;
}

.chart-info-section::-webkit-scrollbar-thumb {
  background: #5F98CA;
  border-radius: 9999px;
}

.chart-info-section::-webkit-scrollbar-thumb:hover {
  background: #4a82b3;
}

.chart{
  background-color: rgba(15, 130, 245, 0.06);
  border-radius: 20px;

  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}

.graph-info {
  background-color: rgba(15, 130, 245, 0.06);
  border-radius: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}

.graph-scroll::-webkit-scrollbar {
  width: 6px;
}
.graph-scroll::-webkit-scrollbar-track {
  background: #404048;
}

.graph-scroll::-webkit-scrollbar-thumb {
  background: #1c76c5;
  border-radius: 9999px;
}

.graph-scroll::-webkit-scrollbar-thumb:hover {
  background: #4a82b3;
}


.chart-2{
  background-color: #ffc27d49;
  border-radius: 20px;

  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}
/* Hide scrollbar but keep scrolling */
.hide-scrollbar {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;     /* Firefox */
}

.hide-scrollbar::-webkit-scrollbar {
  display: none;             /* Chrome, Safari, Opera */
}

.graph-info-2{
  background-color: #ffc27d49;
  border-radius: 20px;

  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
  
}
.chart-3{
  background-color: rgba(25, 167, 0, 0.09);
  border-radius: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}

.graph-info-3{
  background-color: rgba(25, 167, 0, 0.09);
  border-radius: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}
  </style>