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
const csvURL = ref(`${window.location.origin}/flare/csv-data/CRPS_120hrs.csv`);
const showChartHelp = ref(false);




// Add reactive state for dropdown visibility
const isExportMenuVisible = ref(false);
const isSecondExportMenuVisible = ref(false);
const userTimeZone = Intl.DateTimeFormat().resolvedOptions().timeZone; 
let chartTitle = "";

const ribbonChartOptions = ref({});
const secondRibbonChartOptions = ref({});
const boxChartOptions = ref({});
const showInfoDrawer = ref(false);




// Chart function for first chart that changes based on screen size
// ribbon graph
const buildRibbonChart = (isSmallScreen, chartTitle) => {
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
      tickInterval: 24 * 3600 * 1000, // Main ticks every day
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
        fontSize: isSmallScreen ? "10px" : "16px", 
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
      zoomType: "xy",
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
      tickInterval: 24 * 3600 * 1000, // Main ticks every day
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
      startOnTick: true,
      endOnTick: true,
      tickInterval: 10, // Major ticks every 10 units
      min: 30, // Minimum value for y-axis
      softMax: 90,
      title: {
        text: "Temperature (°F)",
        style: { 
            color: "#0f4f66", 
            fontSize: isSmallScreen ? "12px" : "20px", 
        },
      },
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
      // Let Highcharts auto-calculate range with some padding
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
          if (line.series.name === "Water Temperature Predictions Box Plot for Laguna Madre") {
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
        fontSize: isSmallScreen ? "12px" : "16px", 
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

ribbonChartOptions.value = reactive(buildRibbonChart(isSmallScreen, "Water Temperature Predictions for Laguna Madre"));
secondRibbonChartOptions.value = reactive(buildRibbonChart(isSmallScreen , "Water Temperature Predictions with Uncertainty Estimates for Laguna Madre"));
boxChartOptions.value = reactive(buildBoxChart(isSmallScreen));




// Function to fetch and process second CSV data
const fetchAndFilterData = async () => {
  try {
    // Fetch CSV data
    const response = await fetch(csvURL.value);
    if (!response.ok) throw new Error("Failed to fetch ribbon CSV data");

    const csvText = await response.text();


    // Parse the CSV data for the ribbon chart
    const parsedData = parseCSV(csvText);

    // Ensure parsed arrays are initialized
    const waterMeasurements = parsedData.waterMeasurements || [];
    const airMeasurements = parsedData.airMeasurements || [];
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
    const airMeasurementsFahrenheit = airMeasurements.map(([time, celsius]) => [time, +toFahrenheit(celsius).toFixed(1)]);
    const airPredictionsFahrenheit = airPredictions.map(([time, celsius]) => [time, +toFahrenheit(celsius).toFixed(1)]);
    const waterPredictionsPercentile5Fahrenheit = waterPredictionsPercentile5.map(([time, celsius]) => [time, +toFahrenheit(celsius).toFixed(1)]);
    const waterPredictionsPercentile25Fahrenheit = waterPredictionsPercentile25.map(([time, celsius]) => [time, +toFahrenheit(celsius).toFixed(1)]);
    const waterPredictionsPercentile50Fahrenheit = waterPredictionsPercentile50.map(([time, celsius]) => [time, +toFahrenheit(celsius).toFixed(1)]);
    const waterPredictionsPercentile75Fahrenheit = waterPredictionsPercentile75.map(([time, celsius]) => [time, +toFahrenheit(celsius).toFixed(1)]);
    const waterPredictionsPercentile95Fahrenheit = waterPredictionsPercentile95.map(([time, celsius]) => [time, +toFahrenheit(celsius).toFixed(1)]);
    const waterPredictionsPercentileMinFahrenheit = waterPredictionsPercentileMin.map(([time, celsius]) => [time, +toFahrenheit(celsius).toFixed(1)]);
    const waterPredictionsPercentileMaxFahrenheit = waterPredictionsPercentileMax.map(([time, celsius]) => [time, +toFahrenheit(celsius).toFixed(1)]);

    /*
    filter NDFD predictions to only include hours that align with CRPS lead time intervals
    so the tooltip displays correctly
    */
    const crpsTimestamps = waterPredictionsPercentile50Fahrenheit.map(([time]) => time);
    const futureAirPredictionsFahrenheit = airPredictionsFahrenheit.filter(([time]) => crpsTimestamps.includes(time) && time >= Date.now());

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
      const low = waterPredictionsPercentile5Fahrenheit[index][1];
      const q1 = waterPredictionsPercentile25Fahrenheit[index][1];
      const median = waterPredictionsPercentile50Fahrenheit[index][1];
      const q3 = waterPredictionsPercentile75Fahrenheit[index][1];
      const high = waterPredictionsPercentile95Fahrenheit[index][1];

      return [time, low, q1, median, q3, high];
    });


   
    // Update chart series with filtered data
    ribbonChartOptions.value.series = [

      {
        name: "Water Temperature Measurements",
        data: waterMeasurementsFahrenheit,
        type: "line",
        color: "black",
        lineWidth: isSmallScreen ? 1 : 2,
        zIndex: 1, // Ensure this is in front of the bounds
        marker: { enabled: false },
      },
      {
        name: "Air Temperature Measurements",
        data: airMeasurementsFahrenheit,
        type: "line",
        color: "orange",
        lineWidth: isSmallScreen ? 1 : 2,
        zIndex: 1,
        marker: { enabled: false },
      },
      {
        name: "NDFD Air Temperature Predictions",
        data: futureAirPredictionsFahrenheit,
        type: "line",
        color: "orange",
        dashStyle: "LongDash",
        lineWidth: isSmallScreen ? 1 : 2,
        zIndex: 1, // Ensure this is in front of the bounds
        marker: { enabled: false },
      },
      {
        name: "Median (50th Percentile) Water Temperature Predictions",
        data: waterPredictionsPercentile50Fahrenheit,
        type: "line",
        dashStyle: "LongDash",
        color: "black",
        lineWidth: isSmallScreen ? 1 : 2,
        zIndex: 3, // Ensure this is in front of the bounds
        marker: { enabled: false},
      }
      
    ];

     secondRibbonChartOptions.value.series = [

      {
        name: "Water Temperature Measurements",
        data: waterMeasurementsFahrenheit,
        type: "line",
        color: "black",
        lineWidth: isSmallScreen ? 1 : 2,
        zIndex: 1, // Ensure this is in front of the bounds
        marker: { enabled: false },
      },
      {
        name: "Air Temperature Measurements",
        data: airMeasurementsFahrenheit,
        type: "line",
        color: "orange",
        lineWidth: isSmallScreen ? 1 : 2,
        zIndex: 1,
        marker: { enabled: false },
      },
      {
        name: "NDFD Air Temperature Predictions",
        data: futureAirPredictionsFahrenheit,
        type: "line",
        color: "orange",
        dashStyle: "LongDash",
        lineWidth: isSmallScreen ? 1 : 2,
        zIndex: 1, // Ensure this is in front of the bounds
        marker: { enabled: false },
      },
      {
        name: "Median (50th Percentile) Water Temperature Predictions",
        data: waterPredictionsPercentile50Fahrenheit,
        type: "line",
        dashStyle: "LongDash",
        color: "black",
        lineWidth: isSmallScreen ? 1 : 2,
        zIndex: 3, // Ensure this is in front of the bounds
        marker: { enabled: false},
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
        name: "Water Temperature Measurements",
        data: waterMeasurementsFahrenheit,
        type: "line",
        color: "black",
        lineWidth: isSmallScreen ? 1 : 2,
        zIndex: 1, // Ensure this is in front of the bounds
        marker: { enabled: false },
      },
      {
        name: "Air Temperature Measurements",
        data: airMeasurementsFahrenheit,
        type: "line",
        color: "orange",
        lineWidth: isSmallScreen ? 1 : 2,
        zIndex: 1,
        marker: { enabled: false },
      },
      {
        name: "NDFD Air Temperature Predictions",
        data: futureAirPredictionsFahrenheit,
        type: "line",
        color: "orange",
        dashStyle: "LongDash",
        zIndex: 0,
        findnearestPoint: false,
        enablemouseTracking: false, // Disable tooltip for this series
        lineWidth: isSmallScreen ? 1 : 2,
        marker: { enabled: false },
      },
      {
        name: "Median (50th Percentile) Water Temperature Predictions",
        data: waterPredictionsPercentile50Fahrenheit,
        type: "line",
        color: "#4A90E2",
        lineWidth: isSmallScreen ? 1 : 2,
        zIndex: 1, // Ensure this is in front of the bounds
        marker: { enabled: false },
      },
      {
        name: 'Prediction Range Max',
        data: waterPredictionsPercentileMaxFahrenheit,
        type: "line",
        color: "#4A90E2",
        lineWidth: 0,
        zIndex: 1, // Ensure this is in front of the bounds
        marker: { enabled: true,symbol: 'triangle-down', radius: 3.5},
      },
      {
        name: 'Predicition Range Min',
        data: waterPredictionsPercentileMinFahrenheit,
        type: "line",
        color: "#4A90E2",
        lineWidth: 0,
        zIndex: 1, // Ensure this is in front of the bounds
        marker: { enabled: true, symbol: 'triangle', radius: 3.5},
      },
      {
        name: 'Prediction Range (Box: 25th-75th Percentiles; Fence: 5th-95th)',
        type: 'boxplot',
        pointWidth: 10,
        data: boxPlotBoundsFahrenheit,
        lineWidth: isSmallScreen ? 2 : 3,
        medianColor: '#000000',
        stemColor: '#4A90E2',
        whiskerColor: '#4A90E2',
        whiskerLength: '150%',
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
  const airMeasurements = [];
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
      airMeasurementValue,
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
    const localDate = new Date(utcTimestamp);

    if (!isNaN(localDate)) {
      if (waterMeasurementValue && !isNaN(+waterMeasurementValue)) {
        waterMeasurements.push([localDate.getTime(), +waterMeasurementValue]);
      }
      if (airMeasurementValue && !isNaN(+airMeasurementValue)) {
        airMeasurements.push([localDate.getTime(), +airMeasurementValue]);
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
    airMeasurements,
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
let updateInterval;

onMounted(() => {
  const loadCharts = () => {
    Promise.all([
      fetchAndFilterData()
    ]).then(() => {
      missingDataWarningBanner.value.checkForMissingDataAndWarn([
        ribbonChartOptions.value,
        secondRibbonChartOptions.value,
        boxChartOptions.value
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
            Water Temperature Trends and Forecasts for the Texas Upper Laguna Madre
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
                Displays the median (50th percentile) water temperature predictions for the next 120 hours, along with the most recent water and air temperature measurements. 
              </p>
            </div>
            <hr class="border-t border-dark-text">

            <!-- Limitations -->
            <div>
              <h3 class="text-lg lg:text-xl font-bold mb-2">
                Limitations
              </h3>

              <ul class="list-disc list-inside space-y-2 text-dark-text">
                <li>
                  Shows only the most likely forecast. It does not display the uncertainty
                  or the range of other possible temperature predictions.
                </li>
                <li>
                  Semaphore water temperature predictions are generated every six hours.
                </li>
                <li>
                  National Digital Forecast Database (NDFD) air temperature predictions are
                  interpolated as needed.
                </li>
              </ul>
            </div>
            <hr class="border-t border-dark-text">

            <!-- Key Insight -->
            <div>
              <h3 class="text-lg lg:text-xl font-bold mb-2">
                Key Insight
              </h3>

              <p class="leading-relaxed">
                Use this graph for a quick view of the expected temperature trend.
                For forecast confidence and possible temperature ranges, view the
                Ribbon or Box Plot graphs.
              </p>
            </div>

          </div>
        </div>
      </section>
      <div class="h-[30px] bg-gray-100"></div>

       <!-- Second Chart Section-->
      <section class="grid grid-cols-1 lg:grid-cols-5 gap-4 px-2 lg:py-8 lg:px-4  bg-white items-stretch">
        <!-- Chart -->
        <div class="chart-2 lg:col-span-4 relative border sm:w-full ">
          <div class="w-full overflow-x-auto">
            <div class="min-w-[600px] lg:min-w-[1000px] lg:h-[700px] lg:min-h-[650px]">
              <Chart class="w-full h-full p-4" :options="secondRibbonChartOptions" />
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

      <!-- Graph Information -->
        <div class="graph-info-2 max-h-[500px] lg:max-h-[750px] p-6 rounded-lg flex flex-col ">
          <h2 class="text-lg lg:text-3xl font-semibold text-center text-dark-text border-b-2 border-dark-text pb-2 mb-6">
            Graph-Specific Information
          </h2>

          <!-- Scrollable Content -->
          <div class="graph-scroll flex-1 overflow-y-auto space-y-8 text-dark-text pr-2">

            <!-- Uncertainty Meaning -->
            <div>
              <h3 class="text-lg lg:text-xl font-bold mb-2">
                Uncertainty Meaning
              </h3>

              <p class="leading-relaxed mb-3">
                The model predicts many possible temperatures. The shaded bands show how closely those predictions agree.
              </p>

              <ul class="space-y-2 ml-5 list-disc leading-relaxed">
                <li><strong>Black line:</strong> Most likely predicted temperature.</li>
                <li><strong>Dark blue band:</strong> Where most predictions fall.</li>
                <li><strong>Light blue band:</strong> A wider range of possible temperatures.</li>
                <li><strong>Narrow bands:</strong> Higher confidence.</li>
                <li><strong>Wide bands:</strong> Lower confidence.</li>
              </ul>
            </div>
            <hr class="border-t border-dark-text">

            <!-- Limitations -->
            <div>
              <h3 class="text-lg lg:text-xl font-bold mb-2">
                Limitations
              </h3>
              <ul class="list-disc list-inside space-y-2 text-dark-text">
                <li>
                  The shaded bands show likely temperature ranges, not guaranteed outcomes.
                Actual temperatures may still fall outside these ranges.
                </li>
                <li>
                  Semaphore water temperature predictions are generated every six hours.
                </li>
                <li>
                  National Digital Forecast Database (NDFD) air temperature predictions are
                  interpolated as needed.
                </li>
              </ul>
            </div>
            <hr class="border-t border-dark-text">

            <!-- Key Insight -->
            <div>
              <h3 class="text-lg lg:text-xl font-bold mb-2">
                Key Insight
              </h3>

              <p class="leading-relaxed">
                Narrow bands mean the forecast is more certain, while wider bands indicate
                greater uncertainty. Use this graph to understand both the expected
                forecast and its confidence.
              </p>
            </div>

          </div>
        </div>  
      </section>


      
      <div class="h-[30px] bg-gray-100"></div>

      <!-- Third Chart Section-->
      <section class="grid grid-cols-1 lg:grid-cols-5 gap-4 px-2 lg:py-8 lg:px-4 bg-white items-stretch">
        <!-- Chart -->
        <div class="chart-3 lg:col-span-4 relative border sm:w-full ">
          <div class="w-full overflow-x-auto">
            <div class="min-w-[600px] lg:min-w-[1000px] lg:h-[700px] lg:min-h-[650px]">
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

         <!-- Graph Information -->
         <div class="graph-info-3 max-h-[500px] lg:max-h-[750px] p-6 rounded-lg shadow-md flex flex-col">
              <h2 class="text-lg lg:text-3xl font-semibold text-center text-dark-text border-b-2 border-gray-500 pb-2 mb-6">
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
                Summarizes the range of predicted temperatures at each forecast time,
                making it easy to compare forecast uncertainty.
              </p>
            </div>
            <hr class="border-t border-dark-text">

            <!-- Understanding the Box Plot -->
            <div>
              <h3 class="text-lg lg:text-xl font-bold mb-2">
                Understanding the Box Plot
              </h3>

              <ul class="space-y-2 ml-5 list-disc leading-relaxed">
                <li><strong>—</strong> Center line: Most likely predicted temperature.</li>
                <li><strong>▭</strong> Box: Middle 50% of predictions.</li>
                <li><strong>│</strong> Whiskers: Typical prediction range.</li>
                <li><strong>▲ / ▼</strong> Highest and lowest predicted temperatures.</li>
              </ul>
            </div>
            <hr class="border-t border-dark-text">

            <!-- Limitations -->
            <div>
              <h3 class="text-lg lg:text-xl font-bold mb-2">
                Limitations
              </h3>
              <ul class="list-disc list-inside space-y-2 text-dark-text">
                <li>
                  Shows a summary of the predictions instead of every individual forecast.
                </li>
                <li>
                  Semaphore water temperature predictions are generated every six hours.
                </li>
                <li>
                  National Digital Forecast Database (NDFD) air temperature predictions are
                  interpolated as needed.
                </li>
              </ul>
            </div>
            <hr class="border-t border-dark-text">

            <!-- Key Insight -->
            <div>
              <h3 class="text-lg lg:text-xl font-bold mb-2">
                Key Insight
              </h3>

              <p class="leading-relaxed">
                Taller boxes and longer whiskers indicate greater uncertainty, while
                shorter ones indicate higher confidence.
              </p>
            </div>

          </div>
        </div>                              
      </section> 
    </div>

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
            ColdStunning AI Model
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

    <!-- Information Section -->



    <!--  MOBILE -->

    <div
      class="fixed inset-x-0 bottom-0 z-50"
    >

      <!-- Always-visible Handle -->
      <button
        @click="showInfoDrawer = !showInfoDrawer"
        class="w-[calc(100%-2rem)] mx-4 rounded-lg bg-[#1895a3] text-white border-4 border-black shadow-xl py-3"
      >
        <div class="w-12 h-1 bg-gray-300 rounded-full mx-auto mb-2"></div>

        <div class="font-semibold text-xl">
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
              <!-- Left Card -->
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
              </div> <!-- End Left Card -->

            <!-- Right Card -->
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
                <li>
                  Fog Prediction Model coming soon
                </li>
                <li>
                  Inundation Prediction Model coming soon
                </li>
              </ul>
            </div> <!-- End Right Card -->
          </div> <! -- End Card Grind -->

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