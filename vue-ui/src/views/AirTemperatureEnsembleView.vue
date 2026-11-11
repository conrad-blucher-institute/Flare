<!-- ===================================================
View: AirTemperatureEnsembleView.vue

This view displays the air temperature ensemble trends and predictions for South Bird Island
found https://sherlock-prod.tamucc.edu/flare/air-temperature-ensemble

Authors: Anointiyae Beasley, Savannah Stephenson, Christian Quintero

Last Updated: 11/10/2026
======================================================= -->
<script setup>
import Highcharts from "highcharts";
import "highcharts/highcharts-more";
import "highcharts/modules/exporting";
import "highcharts/modules/export-data";
import "highcharts/modules/offline-exporting";
import { Chart } from "highcharts-vue";
import { ref, onMounted, reactive } from "vue";
import MissingDataWarningBanner from "@/components/MissingDataWarningBanner.vue";

const missingDataWarningBanner = ref(MissingDataWarningBanner);
const isSmallScreen = window.innerWidth <= 600;
const csvURL = ref(`${window.location.origin}/flare/csv-data/TWC-NDFD_Laguna-Madre_Air-Temperature-Predictions_240hrs.csv`);

const chartOptions = ref({});
const secondChartOptions = ref({});
const thirdChartOptions = ref({});

// Chart function for first chart that changes based on screen size
// spaghetti graph
const buildChart = (isSmallScreen) => {
  return {
    chart: {
      type: "line",
      zoomType: "x",
      backgroundColor: "white",
      style: { fontFamily: "Arial" },
      marginRight: 30,
      marginTop: 100, 
      events: {
        // tooltip.outside renders the tooltip on document.body, which is hidden in fullscreen,
        // so render it inside the chart while fullscreen is open
        fullscreenOpen: function () {
          this.update({ tooltip: { outside: false } });
        },
        fullscreenClose: function () {
          this.update({ tooltip: { outside: true } });
        },
      },
    },
    title: {
      text: "Ensemble Air Temperature Forecasts for the Upper Laguna Madre",
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
      filename: "TWC-NDFD_Laguna-Madre_Air-Temperature-Predictions_240hrs",
      sourceWidth: 1600,
      sourceHeight: 900,
      scale: 1,
      buttons: {
        contextButton: {
          menuItems: [
            "viewFullscreen",
            "separator",
            "downloadPNG",
            "downloadJPEG",
            "downloadPDF",
            "separator",
            "downloadCSV",
          ],
        },
      },
    },
    legend: {
      enabled: false,
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
    // Let Highcharts auto-calculate range with some padding
    startOnTick: true,
    endOnTick: true,
    tickInterval: 5, // Major ticks every 5 units
    },
    series: [], // Placeholder for data, dynamically updated
    tooltip: {
      outside: true,
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
}; // end buildChart (spaghetti graph)

// Chart function for second chart that changes based on screen size
// ribbon graph
const buildSecondChart = (isSmallScreen) => {
  return {
    chart: {
      type: "areaspline",
      zoomType: "x",
      backgroundColor: "white",
      style: { fontFamily: "Arial" },
      marginRight: 30,
      marginTop: 100,
      events: {
        // tooltip.outside renders the tooltip on document.body, which is hidden in fullscreen,
        // so render it inside the chart while fullscreen is open
        fullscreenOpen: function () {
          this.update({ tooltip: { outside: false } });
        },
        fullscreenClose: function () {
          this.update({ tooltip: { outside: true } });
        },
      },
    },
    title: {
      text: "Air Temperature Predictions from The Weather Company and<br>The National Digital Forecast Database",
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
      filename: "TWC-NDFD_Laguna-Madre_Air-Temperature-Predictions_240hrs",
      sourceWidth: 1600,
      sourceHeight: 900,
      scale: 1,
      buttons: {
        contextButton: {
          menuItems: [
            "viewFullscreen",
            "separator",
            "downloadPNG",
            "downloadJPEG",
            "downloadPDF",
            "separator",
            "downloadCSV",
          ],
        },
      },
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
      },
      series: {
        states: {
          inactive: { opacity: 1 } // do not dim other series when hovering over one
        }
      }
    },
    series: [], // Placeholder for data, dynamically updated
    tooltip: {
      outside: true,
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
}; // end buildSecondChart (ribbon graph)

// Chart function for third chart that changes based on screen size
// box plot graph
const buildThirdChart = (isSmallScreen) => {
  return {
    chart: {
      type: "boxplot",
      zoomType: "x",
      backgroundColor: "white",
      style: { fontFamily: "Arial" },
      marginRight: 30,
      marginTop: 100,
      events: {
        // tooltip.outside renders the tooltip on document.body, which is hidden in fullscreen,
        // so render it inside the chart while fullscreen is open
        fullscreenOpen: function () {
          this.update({ tooltip: { outside: false } });
        },
        fullscreenClose: function () {
          this.update({ tooltip: { outside: true } });
        },
      },
    },
    title: {
      text: "Box Plot for Air Temperature Predictions from The Weather Company<br>and The National Digital Forecast Database",
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
      filename: "TWC-NDFD_Laguna-Madre_Air-Temperature-Predictions_240hrs",
      sourceWidth: 1600,
      sourceHeight: 900,
      scale: 1,
      buttons: {
        contextButton: {
          menuItems: [
            "viewFullscreen",
            "separator",
            "downloadPNG",
            "downloadJPEG",
            "downloadPDF",
            "separator",
            "downloadCSV",
          ],
        },
      },
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
      outside: true,
      shared: true,
      crosshairs: true,
      formatter: function () {
        const localDate = new Date(this.x); 
        // Dynamically creating the tooltip based on what series are present
        // Box Plot is a special case since they have multiple values
        var displayInfo = ``;
        this.points.forEach(line => {
          if (line.series.name === "Box Plot Air Temperature Predictions") {
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
      series: {
        states: {
          inactive: { opacity: 1 } // do not dim other series when hovering over one
        }
      }
    },
  }
} // end buildThirdChart (box plot graph)

chartOptions.value = reactive(buildChart(isSmallScreen));
secondChartOptions.value = buildSecondChart(isSmallScreen);
thirdChartOptions.value = buildThirdChart(isSmallScreen);

// Function to fetch and process CSV data for first chart
const fetchAndFilterData = async () => {
  try {
    // Fetch CSV data
    const response = await fetch(csvURL.value);
    if (!response.ok) throw new Error("Failed to fetch CSV data");

    const csvText = await response.text();

    // Parse the CSV data
    const parsedData = parseCSV(csvText);
    const toFahrenheit = (celsius) => (celsius * 9/5) + 32;
    
    // one line per ensemble member, in Fahrenheit
    const spaghettiSeries = parsedData.members.map((memberData, i) => ({
      name: `Ensemble Member ${i + 1}`,
      data: memberData.map(([time, celsius]) => [time, +toFahrenheit(celsius).toFixed(1)]),
      color: Highcharts.getOptions().colors[i % 10],
      lineWidth: 1,
      marker: { enabled: false },
    }));

    // update chart options
    chartOptions.value.series = spaghettiSeries;

    // initialize series lists
    const p0 = parsedData.p0 || [];
    const p5 = parsedData.p5 || [];
    const p25 = parsedData.p25 || [];
    const p50 = parsedData.p50 || [];
    const p75 = parsedData.p75 || [];
    const p95 = parsedData.p95 || [];
    const p100 = parsedData.p100 || [];
    const ndfd = parsedData.ndfd || [];
    
    // convert to Fahrenheit
    const p0Fahrenheit = p0.map(([time, celsius]) => [time, +toFahrenheit(celsius).toFixed(1)]);
    const p5Fahrenheit = p5.map(([time, celsius]) => [time, +toFahrenheit(celsius).toFixed(1)]);
    const p25Fahrenheit = p25.map(([time, celsius]) => [time, +toFahrenheit(celsius).toFixed(1)]);
    const p50Fahrenheit = p50.map(([time, celsius]) => [time, +toFahrenheit(celsius).toFixed(1)]);
    const p75Fahrenheit = p75.map(([time, celsius]) => [time, +toFahrenheit(celsius).toFixed(1)]);
    const p95Fahrenheit = p95.map(([time, celsius]) => [time, +toFahrenheit(celsius).toFixed(1)]);
    const p100Fahrenheit = p100.map(([time, celsius]) => [time, +toFahrenheit(celsius).toFixed(1)]);
    const ndfdFahrenheit = ndfd.map(([time, celsius]) => [time, +toFahrenheit(celsius).toFixed(1)]);
    
    // combine into 1 series for the outer ribbon of p5 - p95
    const outerRibbon = p5Fahrenheit.map((point, index) => {
      const time = point[0];
      const p5 = p5Fahrenheit[index][1];
      const p95 = p95Fahrenheit[index][1];
      return [time, p5, p95];
    });

    // combine into 1 series for the inner ribbon of p25 - p75
    const innerRibbon = p25Fahrenheit.map((point, index) => {
      const time = point[0];
      const p25 = p25Fahrenheit[index][1];
      const p75 = p75Fahrenheit[index][1];
      return [time, p25, p75];
    });

    const boxPlot = p0Fahrenheit.map((point, index) => {
      const time = point[0];
      const p0 = p0Fahrenheit[index][1];
      const p25 = p25Fahrenheit[index][1];
      const p50 = p50Fahrenheit[index][1];
      const p75 = p75Fahrenheit[index][1];
      const p100 = p100Fahrenheit[index][1];
      return [time, p0, p25, p50, p75, p100];
    });

    // update chart 2
    secondChartOptions.value.series = [
      {
        name: "Median Air Temperature Predictions",
        type: "line",
        data: p50Fahrenheit,
        color: "blue",
        lineWidth: 4,
        marker: { enabled: false },
        zIndex: 3,
      },
      {
        name: '25th-75th Percentile',
        type: 'arearange',
        data: innerRibbon,
        color: '#9ACDFF',
        lineWidth: 1,
        marker: { enabled: false },
        zIndex: 1
      },
      {
        name: '5th-95th Percentile',
        type: 'arearange',
        data: outerRibbon,
        color: '#DDEEFF',
        lineWidth: 1,
        marker: { enabled: false },
        zIndex: 0
      },
      {
        name: "NDFD Air Temperature Predictions",
        type: "line",
        data: ndfdFahrenheit,
        color: "purple",
        lineWidth: 4,
        marker: { enabled: false },
        zIndex: 3,
      },
    ];
    
    // update chart 3
    thirdChartOptions.value.series = [
      {
        name: "Box Plot Air Temperature Predictions",
        type: "boxplot",
        data: boxPlot,
        medianColor: '#000000',
        stemColor: '#4A90E2',
        whiskerColor: '#4A90E2',
        whiskerLength: '150%',
        color: '#4A90E2',
        fillColor: 'rgba(74,144,226,0.35)',
        zIndex: 1,
        marker: { enabled: false },
      },
      {
        name: "Median Air Temperature Predictions",
        type: "line",
        data: p50Fahrenheit,
        color: "blue",
        lineWidth: 4,
        zIndex: 3,
        marker: { enabled: false },
      },
      {
        name: "NDFD Air Temperature Predictions",
        type: "line",
        data: ndfdFahrenheit,
        color: "purple",
        lineWidth: 4,
        zIndex: 3, 
        marker: { enabled: false }
      }
    ];
  } catch (error) {
    console.error("Error fetching or processing data:", error);
  }
};

const parseCSV = (csvText) => {
  const lines = csvText.trim().split("\n");
  const header = lines[0].split(",");
  const col = (name) => header.indexOf(name);

  // set up the arrays to return
  const result = {
    members: [],
    p0: [],
    p5: [],
    p25: [],
    p50: [],
    p75: [],
    p95: [],
    p100: [],
    ndfd: []
  };

  // map the CSV column names to the result keys
  const keys = {
    p0: "TWC Air Temperature Predictions p0",
    p5: "TWC Air Temperature Predictions p5",
    p25: "TWC Air Temperature Predictions p25",
    p50: "TWC Air Temperature Predictions p50",
    p75: "TWC Air Temperature Predictions p75",
    p95: "TWC Air Temperature Predictions p95",
    p100: "TWC Air Temperature Predictions p100",
    ndfd: "NDFD Air Temperature Predictions",
  };

  // skip the header row
  lines.slice(1).forEach((line) => {
    // pull out the quoted list so its commas don't split the row
    const listMatch = line.match(/"\[(.*?)\]"/);
    const list = listMatch ? listMatch[1].split(",").map(Number) : [];
    const fields = line.replace(/"\[.*?\]"/, "LIST").split(",");

    const [year, month, day, hour, minute, second] = fields[0].split(/[- :]/).map(Number);
    const time = Date.UTC(year, month - 1, day, hour, minute, second);
    if (isNaN(time)) return;

    // one series per ensemble member: members[i] holds member i's points
    list.forEach((value, i) => {
      if (!result.members[i]) result.members[i] = [];
      if (!isNaN(value)) result.members[i].push([time, value]);
    });

    for (const [key, name] of Object.entries(keys)) {
      const raw = fields[col(name)];
      if (raw && !isNaN(+raw)) result[key].push([time, +raw]);
    }
  });

  return result;
};

onMounted(() => {
  const loadCharts = () => {
    Promise.all([
      fetchAndFilterData(),
    ]).then(() => {
      missingDataWarningBanner.value.checkForMissingDataAndWarn([
        chartOptions.value, 
        secondChartOptions.value, 
        thirdChartOptions.value
      ]);
    });
  };
  
  // display charts
  loadCharts();
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
            Ensemble Air Temperature Trends and Forecasts for the Texas Upper Laguna Madre
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
              <Chart class="w-full h-full p-4" :options="chartOptions" />
            </div>
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
              <Chart class="w-full h-full p-4" :options="secondChartOptions" />
            </div>
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


      <!-- Third Chart Section: Box Plot Graph -->
      <section class="grid grid-cols-1 lg:grid-cols-5 gap-4 py-8 px-4 bg-white items-stretch">
        <!-- Chart -->
        <div class="lg:col-span-4 relative">
          <div class="w-full overflow-x-auto">
            <div class="min-w-[1000px] h-[500px] lg:h-[700px] lg:min-h-[650px]">
              <Chart class="w-full h-full p-4" :options="thirdChartOptions" />
            </div>
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
      </section> <!-- End of Third Chart Section: Box Plot Graph -->
    </div>

    <!-- Section Divider -->
    <div class="h-[50px] bg-section-gradient"></div>

    <!-- Ensemble Reasoning Section -->
    <section class="bg-white py-10 px-6 md:px-20 text-center lg:text-left">
      <div class="max-w-5xl mx-auto">
        <h2 class="text-lg lg:text-3xl font-extrabold text-dark-text mb-6 text-center">
          Why Use an Ensemble AI Model?
        </h2>
        <p class="text-md lg:text-xl text-dark-text mb-4">
          Weather and environmental conditions in coastal regions like the Laguna Madre are influenced by a complex interplay of atmospheric, oceanic, and terrestrial factors. Relying on a single predictive model can lead to inaccuracies, especially when that model is sensitive to specific data inputs or underlying assumptions.
        </p>
        <p class="text-md lg:text-xl text-dark-text mb-4">
          Ensemble models combine the predictions of multiple individual models — each with different strengths — to generate a more accurate, stable, and resilient forecast. By averaging or intelligently weighting the outputs, the ensemble reduces the impact of outlier predictions and adapts more robustly to noisy or incomplete data.
        </p>
        <p class="text-md lg:text-xl text-dark-text mb-4">
          This approach not only enhances forecast reliability but also provides a better representation of uncertainty, which is critical for decision-making during rapidly evolving weather events. For stakeholders managing cold-stunning response efforts, dredging suspensions, or public communication, ensemble predictions offer a more confident foundation for action.
        </p>
        <p class="text-md lg:text-xl text-dark-text mb-4">
          The use of an ensemble framework reflects best practices in modern climate and forecasting science and helps ensure that the Laguna Madre community is equipped with high-quality, actionable data — even when conditions are unpredictable.
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
      <br><br> <!-- space after logos and bottom of page -->
    </footer>
</template>