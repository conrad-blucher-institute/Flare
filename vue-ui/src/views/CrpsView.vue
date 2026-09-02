<!-- ===================================================
     View: CrpsView.vue

     Description: This view displays the water temperature CRPS trends and predictions for South Bird Island.

                  Features include:
                  - 3 dynamically updating charts
                  - Instructions for interacting with the chart.
                  - Information on the data of the chart.
                  - Additional links
     Author: Anointiyae Beasley

     Last Updated: 08/24/2026

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
      type: "line",
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
      softMin: 30,  // softMin for y axis
      softMax: 90,  // softMax for y axis
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
      line: {
        fillOpacity: 0.3,
        marker: {
          enabled: false,
          radius: 3,
          states: {
            hover: {
              enabled: true
            }
          }
        }
      },
      series: {
        states: {
          inactive: { opacity: 1 } // do not dim other series when hovering over one
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
      text: "Water Temperature Predictions with Uncertainty Estimates<br/>(Percentile Box Plot) for Laguna Madre",
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
      softMin: 30,
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
      series: {
        states: {
          inactive: { opacity: 1 } // do not dim other series when hovering over one
        }
      }
    }
  }
} // end buildBoxChart (box plot graph)

ribbonChartOptions.value = reactive(buildRibbonChart(isSmallScreen, "Water Temperature Predictions for Laguna Madre"));
secondRibbonChartOptions.value = reactive(buildRibbonChart(isSmallScreen , "Water Temperature Predictions with Uncertainty Estimates<br/>(Fan Plot) for Laguna Madre"));
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

    // filter air predictions to only include future predictions
    const futureAirPredictionsFahrenheit = airPredictionsFahrenheit.filter(([time]) => time >= Date.now());

    /*
      We do not interpolate min and max since they are only for the box plot,
      so those timestamps are genuine lead times. For the box plot, we want to
      filter to remove the interpolated values.
    */
    const boxplotTimestampSet = new Set(waterPredictionsPercentileMaxFahrenheit.map(([time]) => time));
    const boxplotWaterPredictionsPercentile5Fahrenheit = waterPredictionsPercentile5Fahrenheit.filter(([time]) => boxplotTimestampSet.has(time));
    const boxplotWaterPredictionsPercentile25Fahrenheit = waterPredictionsPercentile25Fahrenheit.filter(([time]) => boxplotTimestampSet.has(time));
    const boxplotWaterPredictionsPercentile50Fahrenheit = waterPredictionsPercentile50Fahrenheit.filter(([time]) => boxplotTimestampSet.has(time));
    const boxplotWaterPredictionsPercentile75Fahrenheit = waterPredictionsPercentile75Fahrenheit.filter(([time]) => boxplotTimestampSet.has(time));
    const boxplotWaterPredictionsPercentile95Fahrenheit = waterPredictionsPercentile95Fahrenheit.filter(([time]) => boxplotTimestampSet.has(time));

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
      const low = boxplotWaterPredictionsPercentile5Fahrenheit[index][1];
      const q1 = boxplotWaterPredictionsPercentile25Fahrenheit[index][1];
      const median = boxplotWaterPredictionsPercentile50Fahrenheit[index][1];
      const q3 = boxplotWaterPredictionsPercentile75Fahrenheit[index][1];
      const high = boxplotWaterPredictionsPercentile95Fahrenheit[index][1];

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
        dashStyle: "Dash",
        lineWidth: isSmallScreen ? 1 : 2,
        zIndex: 1, // Ensure this is in front of the bounds
        marker: { enabled: false },
      },
      {
        name: "Water Temperature Predictions",
        data: waterPredictionsPercentile50Fahrenheit,
        type: "line",
        dashStyle: "Dash",
        color: "black",
        lineWidth: isSmallScreen ? 1 : 2,
        zIndex: 3, // Ensure median is in front of the other lines
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
        dashStyle: "Dash",
        lineWidth: isSmallScreen ? 1 : 2,
        zIndex: 1, // Ensure this is in front of the bounds
        marker: { enabled: false },
      },
      {
        name: "Water Temperature Median Predictions (50th percentile)",
        data: waterPredictionsPercentile50Fahrenheit,
        type: "line",
        dashStyle: "Dash",
        color: "black",
        lineWidth: isSmallScreen ? 1 : 2,
        zIndex: 3, // Ensure the median is in front of the other lines
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
        dashStyle: "Dash",
        zIndex: 0,
        findnearestPoint: false,
        enablemouseTracking: false, // Disable tooltip for this series
        lineWidth: isSmallScreen ? 1 : 2,
        marker: { enabled: false },
      },
      {
        name: "Water Temperature Median Predictions (50th percentile)",
        data: boxplotWaterPredictionsPercentile50Fahrenheit,
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
        marker: { enabled: true, symbol: 'triangle-down', radius: 3.5 },
      },
      {
        name: 'Prediction Range Min',
        data: waterPredictionsPercentileMinFahrenheit,
        type: "line",
        color: "#4A90E2",
        lineWidth: 0,
        zIndex: 1, // Ensure this is in front of the bounds
        marker: { enabled: true, symbol: 'triangle', radius: 3.5 },
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
            Water Temperature Trends and Forecasts for Laguna Madre, TX
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
                Shows recent temperature measurements alongside a central (median) AI water temperature
                forecast and air temperature forecasts from The Weather Company (TWC) and 
                National Weather Service National Digital Forecast Database (NWS-NDFD). 
                This provides a simple view of how water temperatures are expected to change over the next five days.
              </p>
            </div>
            <hr class="border-t border-dark-text">
            
            <!-- How to Read -->
            <div>
              <h3 class="text-lg lg:text-xl font-bold mb-2">
                How to Read
              </h3>

              <p class="leading-relaxed">
                The black dashed line shows the central water temperature forecast from the AI ensemble model predictions.
                This line represents the median, or middle, of the possible predictions. The vertical “Now” line separates
                recent temperature measurements from future predictions. 
              </p>
            </div>
            <hr class="border-t border-dark-text">

            <!-- What to Look For -->
            <div>
              <h3 class="text-lg lg:text-xl font-bold mb-2">
                What to Look For
              </h3>

              <p class="leading-relaxed">
                Best for tracking the predicted water temperature trend and observing whether it approaches,
                crosses, or remains below critical cold-stunning thresholds.
              </p>
            </div>
            <hr class="border-t border-dark-text">

            <!-- Keep in Mind -->
            <div>
              <h3 class="text-lg lg:text-xl font-bold mb-2">
                Keep in Mind
              </h3>

              <p class="leading-relaxed">
                This forecast shows only one possible outcome and does not display the uncertainty of the AI water
                temperature predictions. Use the Fan Plot or Percentile Box Plot to see the range of water
                temperatures predicted by the AI ensemble model.
              </p>
            </div>

          </div> <!-- End Scrollable Content -->
        </div> <!-- End Graph Information -->
      </section> <!-- End First Chart Section -->
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

            <!-- Purpose -->
            <div>
              <h3 class="text-lg lg:text-xl font-bold mb-2">
                Purpose
              </h3>

              <p class="leading-relaxed mb-3">
                Shows recent temperature measurements alongside the central (median) AI water temperature forecast,
                a range of possible water temperature outcomes, and air temperature forecasts from TWC and NWS-NDFD.
                This provides information about the central predicted trend with forecast uncertainty over the next five days.
              </p>
            </div>
            <hr class="border-t border-dark-text">

            <!-- How to Read -->
            <div>
              <h3 class="text-lg lg:text-xl font-bold mb-2">
                How to Read
              </h3>
              
              <p class="leading-relaxed mb-3">
                The black dashed line shows the central, or median, water temperature forecast.
                The darker shaded area (25th [lower temperature] - 75th [higher temperature] percentile range)
                shows the most likely range, containing the middle 50% of AI water temperature predictions.
                The lighter shaded area (5th [lower temperature] - 95th [higher temperature] percentile range])
                shows a broader range of less likely but possible temperatures, containing 90% of AI water temperature predictions.
              </p>
            </div>
            <hr class="border-t border-dark-text">

            <!-- What to Look For -->
            <div>
              <h3 class="text-lg lg:text-xl font-bold mb-2">
                What to Look For
              </h3>

              <p class="leading-relaxed">
                Look at where the central forecast and shaded ranges fall relative to critical cold-stunning thresholds.
                Also watch how the shaded ranges widen or narrow over time. Wider ranges indicate greater predictive uncertainty,
                while narrower ranges indicate greater confidence on future water temperatures.
              </p>
            </div>
            
            <!-- Keep in Mind -->
            <div>
              <h3 class="text-lg lg:text-xl font-bold mb-2">
                Keep in Mind
              </h3>

              <p class="leading-relaxed">
                Actual water temperatures may occur anywhere within or occasionally outside the displayed ranges (about 10% of the time).
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
                Summarizes how possible water temperature predictions are distributed at each forecast time,
                making it easier to compare the central forecast and forecast uncertainty across the next five days.
              </p>
            </div>
            <hr class="border-t border-dark-text">

            <!-- How to Read -->
            <div>
              <h3 class="text-lg lg:text-xl font-bold mb-2">
                How to Read
              </h3>

              <p class="leading-relaxed">
                The center blue line shows the central, or median, water temperature forecast.
                The box (25th-75th percentiles) shows the most likely range, containing the middle 50% of AI water temperature predictions.
                The whiskers (5th-95th percentiles) show a wider range of possible temperatures, containing 90% of predictions.
                The points beyond the whiskers show the minimum and maximum predicted temperatures.
              </p>
            </div>
            <hr class="border-t border-dark-text">

            <!-- What to Look For -->
            <div>
              <h3 class="text-lg lg:text-xl font-bold mb-2">
                What to Look For
              </h3>
              
              <p class="leading-relaxed">
                Compare the central forecast and ranges with critical cold-stunning thresholds.
                Taller boxes and longer whiskers indicate greater predictive uncertainty,
                while shorter ones indicate greater confidence on future water temperatures.
              </p>
            </div>
            <hr class="border-t border-dark-text">

            <!-- Keep in Mind -->
            <div>
              <h3 class="text-lg lg:text-xl font-bold mb-2">
                Keep in Mind
              </h3>

              <p class="leading-relaxed">
                The minimum and maximum points represent the most extreme AI predictions and may be influenced by only
                a small number of predictions and are driven also by future air temperature conditions.
                Interpret these points alongside the ranges displayed by the boxes rather than on their own.
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
            Laguna Madre AI Ensemble Water Temperature Model
          </h2>
          <p class="text-md lg:text-xl text-dark-text mb-4">
            The Laguna Madre is a shallow, hypersaline lagoon where strong winter cold fronts can lower air temperatures
            by more than 10°C in less than 24 hours. These rapid changes can cause substantial declines in water temperature, 
            creating hazardous conditions for marine life. Past extreme cold-water events have resulted in large-scale fish
            kills and the cold-stunning of sea turtles.
          </p>
          <p class="text-md lg:text-xl text-dark-text mb-4">
            During these events, members of the Texas Marine Coldwater Response Collaboration (TCRC)—including government agencies,
            researchers, private-sector organizations, and other coastal stakeholders—coordinate preparations and response activities. 
            These efforts may include mobilizing sea turtle rescue resources and voluntarily modifying or suspending activities such as 
            fishing, navigation, and dredging to reduce additional risks to marine life.
          </p>
          <p class="text-md lg:text-xl text-dark-text mb-4">
            Accurate and timely temperature predictions help TCRC members determine when preparations may be needed and how long hazardous 
            conditions could persist. The live-updating graph above displays recent air and water temperature observations alongside 
            predicted conditions for the Laguna Madre. The water temperature predictions extend up to 120 hours, or five days, into the future.
          </p>
          <p class="text-md lg:text-xl text-dark-text mb-4">
            Users should pay particular attention to how quickly water temperatures are predicted to decrease, 
            whether they approach important cold-stunning thresholds, and how long hazardous conditions may persist. 
            Predictions should be interpreted as decision-support guidance rather than exact guarantees. 
            Because forecast conditions can change, users should review the latest model update alongside current observations,
            official weather information, and local operational expertise.
          </p>
          <p class="text-md lg:text-xl text-dark-text mb-4">
            By providing advance notice of potentially hazardous water temperatures, 
            the model supports coordinated decisions about monitoring, resource mobilization, 
            rescue preparations, and temporary operational changes. Research and development are ongoing to 
            improve the accuracy, reliability, and usefulness of the predictions during extreme cold-weather events.
          </p>
          <p class="text-md lg:text-xl text-dark-text mb-4">
            The original AI water temperature model was developed by Dr. Robyn Ball during her master's research at 
            Texas A&M University-Corpus Christi (TAMU-CC). Responsibility for its continued development and maintenance was later 
            entrusted to the Cool Turtles team within the Coastal Dynamics Lab at TAMU-CC.
          </p>
          <h3 class="text-lg lg:text-xl font-bold mb-2">
            Model Development and Maintenance
          </h3>
          <p class="text-md lg:text-xl text-dark-text mb-4">
            The Cool Turtles team is led by
            <a href="https://www.linkedin.com/in/miranda-white-859b2414a/" target="_blank" class="text-blue-500 hover:underline">Dr. Miranda White</a>, 
            alongside her talented teammates 
            <a href="https://www.linkedin.com/in/jarett-woodall-mba-8a3696224/" target="_blank" class="text-blue-500 hover:underline">Jarett Woodall</a>, 
            <a href="https://www.linkedin.com/in/christian-duff-898103211/" target="_blank" class="text-blue-500 hover:underline">Christian Duff</a>, 
            <a href="https://www.facebook.com/watch/?v=740721718150868" target="_blank" class="text-blue-500 hover:underline">Hector Marrero-Colominas</a>,
            <a href="https://www.linkedin.com/in/andrew-desimone-00170b24b/" target="_blank" class="text-blue-500 hover:underline">Andrew DeSimone</a>, 
            and Elisa Flores. The team works with TCRC members and other collaborators to evaluate and improve the model
            and its accompanying visualizations for operational decision-making.
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
              </ul>
            </div> <!-- End Right Card -->
          </div> <!-- End Card Grid -->

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
            <img src="@/assets/images/NSF-Logo.png" alt="NSF Logo" class="max-w-[80px] lg:max-w-[150px]">
          </a>
          <a href="https://www.ai2es.org/" target="_blank" class="hover:scale-110 transition-transform">
            <img src="@/assets/images/ai2es-logo.png" alt="AI2ES Logo" class="max-w-[80px] lg:max-w-[150px]">
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
          <a href="https://www.weathercompany.com/" target="_blank" class="hover:scale-110 transition-transform">
            <img src="@/assets/images/TWC-Logo.png" alt="The Weather Company Logo" class="max-w-[80px] lg:max-w-[150px]">
          </a>
          <a href="https://ccme.famu.edu/" target="_blank" class="hover:scale-110 transition-transform">
            <img src="@/assets/images/CCME-Logo.png" alt="Florida A&M University Logo" class="max-w-[80px] lg:max-w-[150px]">
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