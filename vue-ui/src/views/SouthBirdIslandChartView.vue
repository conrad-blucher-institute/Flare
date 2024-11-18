<!-- ===================================================
     View: SouthBirdIslandChart.vue
     Description: This view displays the air temperature trends and predictions for South Bird Island. 
                  Features include:
                  - A dynamically updating Highcharts line chart using live CSV data.
                  - Instructions for interacting with the chart.
                  - Informative sections about South Bird Island and its environmental significance.
                  - A team introduction section.
     Author: Anointiyae Beasley
     Date: 11/15/2024
======================================================= -->

<script setup>
// Import Highcharts and required modules
import Highcharts from 'highcharts';
import exportingInit from 'highcharts/modules/exporting';
import dataModule from 'highcharts/modules/data'; 
import { Chart } from 'highcharts-vue'; 

// Initialize Highcharts modules
exportingInit(Highcharts);
dataModule(Highcharts);

// Define the current date and time
const nowDate = new Date();// Current timestamp
const nowTime = new Date(nowDate); // Convert to a Date object

// Highcharts object
const southBirdIslandChart = {
  chart: {
    type: 'line', // Specifies a line chart
    styledMode: false, // Inline styles for better customizability
    zoomType: 'x', // Enable horizontal zooming
    panKey: 'alt', // Hold "Alt" to pan across the chart
  },
  title: {
    text: 'Temperature of Upper South Bird Island', // Main chart title
    style: {
      fontSize: '25px', // Large font for visibility
      fontWeight: 'bold',
      color: '#333', // Neutral black text
    },
  },
  subtitle: {
    text: '', // Optional subtitle
  },
  legend: {
    itemStyle: {
      fontSize: '19px', // Adjust legend font size
      fontWeight: 'bold', // Highlight legend items
    },
  },
  data: {
    // URL for fetching CSV data dynamically
    csvURL: window.location.href.replace(
      /localhost:5173\/south-bird-island-chart.*/,
      'localhost:8080'
    ) + '/csv-data/test.csv',
    enablePolling: true, // Refresh data periodically
    dataRefreshRate: 10, // Interval for refreshing (in seconds)
    complete: function (data) {
      // Parse and filter CSV data for the chart
      const waterTemperatureMeasurements = data.series[0]; // Series for water measurements
      const waterTemperaturePredictions = data.series[1]; // Series for water predictions
      const airTemperatureMeasurements = data.series[2]; // Series for air measurements
      const airTemperaturePredictions = data.series[3]; // Series for air predictions

      // Filter water measurements before the current time
      const filteredWaterMeasurementData = waterTemperatureMeasurements.data.filter(
        (point) => new Date(point[0]) <= nowTime
      );

      // Filter water predictions starting from the current time
      const filteredWaterPredictionData = waterTemperaturePredictions.data.filter(
        (point) => new Date(point[0]) >= nowTime
      );

      // Filter air measurements before the current time
      const filteredAirMeasurementData = airTemperatureMeasurements.data.filter(
        (point) => new Date(point[0]) <= nowTime
      );

      // Filter air predictions starting from the current time
      const filteredAirPredictionData = airTemperaturePredictions.data.filter(
        (point) => new Date(point[0]) >= nowTime
      );

      // Update the chart with filtered data
      data.series = [
        {
          name: 'Water Temperature Measurements',
          data: filteredWaterMeasurementData,
          color: 'black',
          lineWidth: 4, // Make line thicker
          marker: { enabled: false }, // Hide data markers
        },
        {
          name: 'Predicted Water Temperature',
          data: filteredWaterPredictionData,
          color: 'black',
          dashStyle: 'Dash', // Dashed line style
          lineWidth: 5, // Thicker line
          marker: { enabled: false },
        },
        {
          name: 'Air Temperature Measurements',
          data: filteredAirMeasurementData,
          color: 'blue',
          lineWidth: 4,
          marker: { enabled: false },
        },
        {
          name: 'Interpolated Predicted Air Temperature',
          data: filteredAirPredictionData,
          color: 'orange',
          dashStyle: 'Dash',
          lineWidth: 5,
          marker: { enabled: false },
        },
      ];
    },
  },
  yAxis: {
    labels: {
      style: {
        fontSize: '130%', // Larger labels for better visibility
        color: 'black',
      },
    },
    title: {
      text: 'Temperature (°F)', // Y-axis title
      style: {
        fontSize: '150%', // Adjusted font size
      },
    },
    max: 90, // Maximum temperature shown on the chart
    min: 20, // Minimum temperature shown on the chart
    plotLines: [
      {
        // Threshold for sea turtle safety
        color: 'red',
        width: 4,
        value: 45,
        dashStyle: 'Dash',
        label: {
          text: 'Sea Turtle Water Temperature Threshold',
          style: {
            color: 'black',
            fontSize: '20px',
          },
        },
      },
      {
        // Threshold for fisheries safety
        color: 'purple',
        width: 4,
        value: 40,
        dashStyle: 'Dash',
        label: {
          text: 'Fisheries Water Temperature Threshold',
          style: {
            color: 'black',
            fontSize: '20px',
          },
        },
      },
    ],
  },
  xAxis: {
    type: 'datetime', // Time-based x-axis
    dateTimeLabelFormats: {
      day: '%a %b %e', // Custom format for dates
    },
    labels: {
      format: '{value:%a %b %e}', // Display abbreviated date
      padding: 25, // Add spacing around labels
      style: {
        fontSize: '22px',
        fontWeight: 'bold',
      },
      step: 2, // Show every second label
    },
    title: {
      text: 'Time', // X-axis title
      style: {
        fontSize: '150%',
      },
    },
    maxPadding: 0.10, // Adjust axis padding
    plotLines: [
      {
        // Line to indicate the current time
        color: 'red',
        width: 2,
        value: nowDate, // Current time marker
        dashStyle: 'Solid',
        label: {
          text: `Now`, // Label for the current time
          style: {
            color: 'black',
            fontSize: '18px',
            fontWeight: 'bold',
          },
        },
      },
    ],
  },
  tooltip: {
    shared: true, // Combine tooltips for overlapping series
    crosshairs: true, // Display crosshairs on hover
    formatter: function () {
      // Format tooltip content
      return `<b>Date: ${Highcharts.dateFormat('%A, %b %e, %Y', this.x)}</b><br>
              Temperature: ${this.y}°F`;
    },
    style: {
      fontSize: '18px', // Larger tooltip font
      padding: '10px', // Add padding inside tooltip
    },
  },
};
</script>


<template>
  <div class="page-container">
    <section class="banner">
        <div class="banner-overlay">
          <!-- <img src="/OIP.jpg" alt="Background Image 1" class="overlay-image"> -->
        </div>
        <div class="banner-content">
          <h1 class="header-title">Air Temperature Trends and Predictions for South Bird Island, Texas</h1>
        </div>
    </section>

    <!--Display the Chart-->    
    <Chart  class="chart"  :options="southBirdIslandChart"/>

    <!--Information on how to use the chart--> 
    <ul>
      <li>Use the hamburger menu in the top-right corner of the chart to download the data, view it in full-screen mode, or explore additional options.</li>
      <li>Hover over the data points on the chart to see the exact temperature values for each measurement and prediction.</li>
    </ul>


    <!-- Section Divider -->
    <div class="section-divider"> </div>

    <!-- About Section -->
    <section class="about-section">
      <h2>South Bird Island Model</h2>
        <img src="@/assets/images/SBI.jpg" alt="Map of South Bird Island, Texas">
          <p>
            In the Laguna Madre, the longest hypersaline lagoon in the United States, the passage of cold fronts can lower air temperature by more than 10°C in less than 24 hours. 
            This can lead to a considerable decrease in water temperature. Some of these cold-water events result in large fish kills and sea turtle cold stunning. 
            To mitigate the impact of these cold events, local agencies, private sector companies and other stakeholders (logos below) voluntarily interrupt activities such as fishing and navigation in the Laguna Madre. 
            To manage these interruptions and mobilize resources, accurate predictions are very helpful. The live updating graph above combines the latest air and water temperatures and predicted air temperatures in the Laguna Madre; relatively uniform water temperatures have been measured throughout the Laguna during cold events. An automated neural network predicting water temperatures is in development and will be added in 2020.
          </p>
    </section>

    <!-- Map of Location -->
    <section class="map-section">
      <h2> South Bird Island Exact Location</h2>        
    </section>

        <!-- Meet the Team Section -->
        <section class="team-section">
          <h2>Meet the Team Behind This AI Model</h2>
          <div class="team-members">
            <div class="matthew">
              <img src="@/assets/images/MatthewKastl.png" alt="Matthew Kastl">
              <h1> Place Holder</h1>
              <p>Graduate Student</p>
            </div>

            <div class="beto">
              <img src="@/assets/images//BetoEstrada.png" alt="Beto Estrada">
              <h1> Place Holder</h1>
              <p>Graduate Student</p>
            </div>

            <div class="anointiyae">
              <img src="@/assets/images//AnointiyaeBeasley.png" alt="Anointiyae Beasley">
               <h1> Place Holder </h1>
                <p>Undergraduate Student</p>
            </div>

            <div class="savannah">
              <img src="@/assets/images//SavannahStephenson.png" alt="Savannah Stephenson">
              <h1> Place Holder </h1>
              <p>Graduate Student</p>
            </div>
          </div>
        </section>
  </div>
</template>

<style scoped>
.banner {
  position: relative;
  width: 100%; 
  background: linear-gradient(to bottom, #000000,#004184, #05c1d4); 
  color: #fff; 
  padding: 10px 0px;
  text-align: center;
  overflow: hidden; 
  margin: 0; /* Remove any default margin */
}

.chart{
  height: 700px;
}

.section-divider {
    background-color: #2c849b;
    padding: 30px 0px;
    width: 100%;; /* Full viewport width */
}
.team-section {
    background-color: white;
    color: black;
    left: 0;

}
.page-container {
    width: 100%;; /* Full viewport width */
    padding: 0;
    margin: 0; /* Remove any default margin */
    overflow: hidden; 
}
.about-section{
    padding: 200px 0px;
}

.map-section{
  background-color: #0f4f66;
  color: white;
  padding: 200px 0px;
}

.banner-content {
  position: relative;
  max-width: 1000px;
  margin: auto;
}

.header-title {
    font-size: 80px;
}


</style>

