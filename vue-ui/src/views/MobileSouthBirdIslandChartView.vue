<!-- ===================================================
     View: MobileSouthBirdIslandChart.vue
     Description: This view displays the air temperature trends and predictions for South Bird Island. 
                  Features include:
                  - A dynamically updating Highcharts line chart using live CSV data.
                  - Instructions for interacting with the chart.
                  - Information on the data of the chart.
                  - Informative sections about South Bird Island and its environmental significance.
                  - A team introduction section.
     Author: Anointiyae Beasley
     Date: 11/24/2024
======================================================= -->

<script setup>
  // Import Highcharts and required modules
  import Highcharts from 'highcharts';
  import { ref } from 'vue';
  import exportingInit from 'highcharts/modules/exporting';
  import dataModule from 'highcharts/modules/data'; 
  import { Chart } from 'highcharts-vue';


  // Initialize Highcharts modules
  exportingInit(Highcharts);
  dataModule(Highcharts);
  console.log("Highcharts data module initialized:", dataModule);

  // Reactive variable for chart options
  const chartOptions = ref({}); // Initialize as an empty object

  // Define the current date and time
  const nowDate = new Date();// Current timestamp
  const nowTime = new Date(nowDate); // Convert to a Date object


    // ------ Highcharts object for mobile -------
    const mobileSouthBirdIslandChart = {
    chart: {
      type: 'line', // Specifies a line chart
      styledMode: false,
      zoomType: 'x',
      panning: true, // Enable panning
      backgroundColor: 'white',
      pinchType: 'x', // Allow pinch-to-zoom (important for mobile)
      style: {
        fontFamily: 'Georgia',
      },
      spacing: [30, 30, 30, 30], // Add padding: [top, right, bottom, left]
      height: 500, // Reduce chart height 
    },
    title: {
      text: 'Temperature of Upper Laguna Madre', // Simplified title for smaller screens
      style: {
        fontSize: '16px', // Smaller font size
        fontWeight: 'bold',
        color: '#0f4f66',
        fontFamily: 'Georgia', 
      },
    },
    subtitle: {
      text: '',
    },
    legend: {
      itemStyle: {
        fontSize: '12px', // Smaller font size for legend items
        fontWeight: 'bold',
        fontFamily: 'Georgia',
        color: '#0f4f66',
      },
    },
    data: {
      csvURL: `http://localhost:8080/flare/csv-data/test.csv`, // Will be changed for production
      enablePolling: true,
      dataRefreshRate: 10,
      complete: function (data) {
        if (!data || !data.series || data.series.length === 0) {
        console.error("No data available to process.");
        return;
  }
        // Parse and filter CSV data for the chart
        const waterTemperatureMeasurements = data.series[0]; 
        const waterTemperaturePredictions = data.series[1]; 
        const airTemperatureMeasurements = data.series[2]; 
        const airTemperaturePredictions = data.series[3]; 

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
            color: 'blue',
            lineWidth: 2,
            marker: { enabled: false }, // Hide data markers
          },
          {
            name: 'Predicted Water Temperature',
            data: filteredWaterPredictionData,
            color: 'blue',
            dashStyle: 'Dash', 
            lineWidth: 3, 
            marker: { enabled: false },
          },
          {
            name: 'Air Temperature Measurements',
            data: filteredAirMeasurementData,
            color: 'black',
            lineWidth: 2,
            marker: { enabled: false },
          },
          {
            name: 'Interpolated Predicted Air Temperature',
            data: filteredAirPredictionData,
            color: 'black',
            dashStyle: 'Dash',
            lineWidth: 3,
            marker: { enabled: false },
          },
        ];
      },
    },
    yAxis: {
      labels: {
        style: {
          fontSize: '12px', // Smaller font size for labels
          color: '#0f4f66',
          fontFamily: 'Georgia', 
        },
      },
      title: {
        text: 'Temperature (°F)',
        style: {
          fontSize: '14px', // Smaller font size for the y-axis title
          fontFamily: 'Georgia',
        },
      },
      max: 90,
      min: 20,
      plotLines: [
        {
          // Threshold for sea turtle safety
          color: '#00815e',
          width: 4,
          value: 45,
          dashStyle: 'Dash',
          label: {
            text: 'Sea Turtle Water Temperature Threshold',
            style: {
              color: '#0f4f66',
              fontSize: '14px',
              fontWeight:'bold', 
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
              color: '#0f4f66',
              fontSize: '14px',
              fontFamily: 'Georgia', 
              fontWeight:'bold', 
            },
          },
        },
      ],
    },
    xAxis: {
      type: 'datetime',
      dateTimeLabelFormats: {
      day: '%a %b %e', 
      },
      labels: {
      formatter: function () {
        const day = Highcharts.dateFormat('%A', this.value); 
        const date = Highcharts.dateFormat('%b %e', this.value); 
        const time = Highcharts.dateFormat('%l:%M %p', this.value); 
        return `<span style="display: block; text-align: center; font-family: Georgia;">
                  <b>${day}</b><br>${date}<br><i>${time}</i>
                </span>`;
      },
      useHTML: true, // Enable HTML for custom label formatting
      style: {
          fontSize: '10px', // Smaller font size for x-axis labels
          color: '#0f4f66',
          fontWeight: 'bold',
          fontFamily: 'Georgia', 
        },
        step: 2, // Show every 4th label
      },
      title: {
        text: 'Time',
        style: {
          fontSize: '14px',
          fontFamily: 'Georgia', 
          color: '#0f4f66',
        },
      },
      events: {
        afterSetExtremes: function () {
          const chart = this.chart;
          const xAxis = this;
          const min = Math.ceil(xAxis.min / (24 * 3600 * 1000)) * (24 * 3600 * 1000); // Start of the next day
          const max = xAxis.max;
          const plotLines = [];

          // Iterate over each day in the range and create a plotline
          for (let time = min; time <= max; time += 24 * 3600 * 1000) {
            plotLines.push({
              color: 'gray',
              dashStyle: 'Dot',
              width: 1,
              value: time,
              label: {
                text: Highcharts.dateFormat('%a %b %e', time), // Display day and date
                align: 'left',
                rotation: 0,
                style: {
                  color: '#0f4f66',
                  fontSize: '12px',
                  fontFamily: 'Georgia',
                },
              },
            });
          }

          // Remove old plotlines and add the new ones
          xAxis.removePlotLine('daily-plotlines'); 
          plotLines.forEach((line) => xAxis.addPlotLine(line));
        },
      },
      plotLines: [
        {
          // Line that shows now time
          color: 'black',
          width: 2,
          value: nowDate, 
          dashStyle: 'Solid',
          label: {
            text: `Now`, 
            style: {
              color: '#0f4f66',
              fontSize: '12px',
              fontWeight: 'bold',
              fontFamily: 'Georgia', 
            },
          },
        },
      ],
    },
      tooltip: {
        shared: false,
        formatter: function () {
          return `<b>${Highcharts.dateFormat('%b %e', this.x)}</b><br>Temp: ${this.y}°F`;
        },
        style: {
          fontSize: '12px',
          color: '#0f4f66',
          fontFamily: 'Georgia', 
        },
      },
  };



</script>


<template>
  

  

  <div class="page-container">
    
     <!-- Banner Section -->
    <section class="chart-banner">
      <!-- Overlay image on the left -->
      <div class="map-overlay">
        <img src="@/assets/images/MapOverlayMobile.png" alt="Map Overlay" class="overlay-image">
      </div>

      <!-- Text content on the right of the overlay image-->
      <div class="banner-content">
        <h1 class="header-title">Water and Air Temperature Trends and Forecasts for the Texas Upper Laguna Madre</h1>
      </div>
    </section>

    <section class="chart-container">
      <!-- Display the Chart -->
      <div class="chart-scroll-container" v-if="chartOptions">
        <div class="chart-wrapper">
          <Chart class="chart" :options="mobileSouthBirdIslandChart" />
        </div>
      </div>
      <!-- Information on how to use the chart -->
      <div class="instructions-list">
        <h2>How to Use the Chart</h2>
        <ul>
          <li>
            <span class="icon">☰</span>
            Use the hamburger menu in the top-right corner of the chart to download the data, view it in full-screen mode, or explore additional options.
          </li>
          <li>
            <span class="icon">📊</span>
            Hover over the data points on the chart to see the exact temperature values for each measurement and prediction.
          </li>
          <li>
              <span class="icon">🔍</span>
              Pinch to zoom into the chart using two fingers to explore data points in greater detail.
          </li>
          <li>
            <span class="icon">🔄</span>
            Use the "Reset Zoom" button in the top-right corner of the chart to return to the default view.
          </li>
          <li>
            <span class="icon">👆</span>
            Click on a legend item below the chart to toggle the visibility of specific data series.
          </li>
        </ul>
      </div>
    </section>

    <!-- Data on The Chart -->
    <section class="chart-data-info">
      <h3>Data on This Graph:</h3>
      <ul>
        <li>
          Past six-day measurement of air and water temperature from&nbsp;  
          <a href="https://tidesandcurrents.noaa.gov/stationhome.html?id=8776139" target="_blank" rel="noopener noreferrer">
             NOAA's South Bird Island Station (8776139)
          </a>.
        </li>
        <li>Backup water temperature data from&nbsp;
          <a href="https://lighthouse.tamucc.edu/overview/171" target="_blank" rel="noopener noreferrer">
            National Park Service South Bird Island station
          </a>.
        </li>
        <li>Backup air temperature data from&nbsp;  
          <a href="https://tidesandcurrents.noaa.gov/stationhome.html?id=8776604" target="_blank" rel="noopener noreferrer">
               NOAA's Baffin Bay Station (8776604)
          </a>.
        </li>
        <li>Air temperature predictions from the National Digital Forecast Database (points).</li>
        <li>Cubic interpolation of predicted air temperature (dashed line).</li>
        <li>Water temperature predictions from Semaphore (dashed line).</li>
      </ul>
    </section>
    
    <!-- Section Divider -->
    <div class="section-divider"> </div>

    <!-- About Section -->
    <section class="about-section">
      
      <div class="about-container">
        <img src="@/assets/images/SouthBirdIslandMap.jpg" alt="Map of South Bird Island, Texas" class="about-image">
        <div class="about-content">
          <h2 class="about-header">Laguna Madre AI Model</h2>

          <p>
            In the Laguna Madre, the longest hypersaline lagoon in the United States, the passage of cold fronts can lower air temperature by more than <strong>10°C</strong> in less than 24 hours. 
            This can lead to a considerable decrease in water temperature. Some of these cold-water events result in large fish kills and sea turtle cold stunning.
          </p>
          <p>
            To mitigate the impact of these cold events, local agencies, private sector companies, and other stakeholders (logos below) voluntarily interrupt activities such as fishing and navigation in the Laguna Madre. 
            To manage these interruptions and mobilize resources, accurate predictions are very helpful. The live updating graph above combines the latest air and water temperatures and predicted air temperatures in the Laguna Madre; relatively uniform water temperatures have been measured throughout the Laguna during cold events.
          </p>
          <p>
            An automated neural network predicting water temperatures is in development and will be added in <strong>2020</strong>.
          </p>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
    <div class="footer-container">
      <div class="footer-logos">
        <a href="https://www.conradblucherinstitute.org/" target="_blank">
          <img class="footer-logo cbi-logo" src="@/assets/images/CBI-Logo.png" alt="CBI Logo">
        </a>
        <a href="https://github.com/conrad-blucher-institute/semaphore" target="_blank">
        <img class="footer-logo" src="@/assets/images/Semaphore-Logo.png" alt="Semaphore Logo">
        </a>
        <a href="https://www.usace.army.mil/" target="_blank">
          <img class="footer-logo" src="@/assets/images/USACE-Logo.jpg" alt="US Army Corps Logo">
        </a>
        <a href="https://www.nsf.gov/" target="_blank">
          <img class="footer-logo" src="@/assets/images/NSF-Logo.png" alt="National Science Foundation Logo">
        </a>
        <a href="https://www.gicaonline.com/" target="_blank">
          <img class="footer-logo" src="@/assets/images/GICA-Logo.png" alt="Gulf Intracoastal Canal Association Logo">
        </a>
        <a href="https://tpwd.texas.gov/" target="_blank">
          <img class="footer-logo" src="@/assets/images/TPWD-Logo.gif" alt="Texas Parks and Wildlife Logo">
        </a>
        <a href="https://www.coastaldynamicslab.org/" target="_blank">
          <img class="footer-logo" src="@/assets/images/CDL-Logo.png" alt="Coastal Dynamics Lab Logo">
        </a>
        <a href="https://www.nps.gov/index.htm" target="_blank">
          <img class="footer-logo" src="@/assets/images/NPS-Logo.png" alt="National Park Service Logo">
        </a>
        <a href="https://www.weather.gov/" target="_blank">
          <img class="footer-logo" src="@/assets/images/NWS-Logo.png" alt="National Weather Service Logo">
        </a>
        <a href="https://www.uscg.mil/" target="_blank">
          <img class="footer-logo" src="@/assets/images/CG-Logo.png" alt="USA Coast Guard Logo">
        </a>
        <a href="https://www.joincca.org/" target="_blank">
          <img class="footer-logo" src="@/assets/images/CCA-Logo.png" alt="Coastal Conservation Association Logo">
        </a>
      </div>
      <div class="footer-info">
        <p>Photos courtesy of the National Park Service, Division of Sea Turtle Science and Recovery.</p>
        <p>(Click on a logo to visit the respective website.)</p>
      </div>
    </div>
  </footer>

  </div>
</template>

<style scoped>
.page-container {
  padding: 0;
  margin: 0;
  overflow: hidden;
}

/* Banner Section */
.chart-banner {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  background: var(--banner-gradient-background);
  color: var(--primary-background);
  height: 300px;
  padding: 20px 10px;
  width: 100%;
}

.overlay-image {
  width: auto;
  align-items: left;
  height: 400px;
  object-fit: cover;
  opacity: 100%;
  overflow: hidden;
  padding-right: 60px;
  

}

.banner-content {
  text-align: center;
  padding: 10px;
  align-items: left;
}

.header-title {
  flex: 0;
  position: absolute;
  padding-right: 140px;
  font-size: 1.1rem;
  line-height: 1.4;
  padding-bottom: 10px;
}

/* Chart Section */
.chart-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  padding: 20px 10px;
}

.chart-scroll-container {
  overflow-x: auto;
  overflow-y: hidden;
  -webkit-overflow-scrolling: touch;
  width: 100%;
}

.chart-wrapper {
  min-width: 800px;
  display: inline-block;
}

.chart {
  max-width: 100%;
  height: auto;
  padding: 0;
}

/* Instructions Section */
.instructions-list {
  width: 100%;
  background-color: var(--accent-background);
  padding: 10px;
  font-size: 0.5rem;
  line-height: 1.4;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.instructions-list h2 {
  font-size: 1.5rem;
  margin-bottom: 10px;
  color: var(--primary-text-light-background);
  text-align: center;
}

.instructions-list ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.instructions-list li {
  display: flex;
  align-items: flex-start;
  margin-bottom: 8px;
  font-size: 1rem;
}

.instructions-list .icon {
  font-size: 1.2rem;
  margin-right: 10px;
  color: var(--primary-text-light-background);
}

/* Chart Data Info Section */
.chart-data-info {
  background-color: var(--accent-background); /* Match the overall theme */
  padding: 25px 30px;
  box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15); /* Slightly deeper shadow for a modern look */
  font-size: 1rem;
  line-height: 1.8;
  border: 1px solid rgba(0, 0, 0, 0.1); 
}

/* Section Title */
.chart-data-info h3 {
  font-size: 1.1rem; 
  color: var(--primary-text-light-background); 
  margin-bottom: 20px;
  text-align: center;
  letter-spacing: 1px; /* Slightly spaced letters */
  border-bottom: 2px solid var(--secondary-text); /* Underline title*/
  display: inline-block; /* Adjust inline alignment */
  padding-bottom: 5px;
}

/* List Styling */
.chart-data-info ul {
  list-style: none; /* Remove default list bullets */
  margin: 0;
  padding: 0; /* Align to container */
}

.chart-data-info li {
  display: flex; 
  flex-wrap: wrap;
  align-items: center; /* Vertically center items */
  margin-bottom: 15px;
  color: var(--secondary-text);
  font-size: 1rem; 
}

.chart-data-info li:before {
  content: "•"; /* Add custom bullet */
  font-size: 1.5rem; /* Larger bullet size */
  color: var(--primary-text-light-background); 
  margin-right: 10px; /* Space between bullet and text */
}


/* About Section */
.about-section {
  padding: 20px 10px;
  margin: 10px auto;
}

strong {
  color: var(--primary-text-light-background);
}

.about-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.about-image {
  max-width: 90%;
  max-height: 300px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.about-content {
  text-align: center;
  width: 100%;
}

.about-content p {
  font-size: 1rem;
  line-height: 1.5;
}

.about-header {
  font-size: 1.6rem;
  margin-bottom: 15px;
  color: var(--primary-text-light-background);
}

/* Footer Styles */
.footer {
  background-color: var(--navy-blue);
  padding: 40px 20px;
  text-align: center;
}

.footer-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

/* Footer Logos */
.footer-logos {
  display: flex;
  flex-wrap: wrap;
  gap: 40px;
  justify-content: center;
}

.footer-logos a {
  display: inline-block;
  transition: transform 0.3s ease;
}

.footer-logos a:hover {
  transform: scale(1.1);
}

.footer-logo {
  max-width: 70px;
  max-height: 70px;
  object-fit: contain;
}

/* Footer Info */
.footer-info {
  font-size: 14px;
  color: var(--primary-text-dark-background);
  margin-top: 30px;
  text-align: center;
}

/* Specific Style for CBI Logo */
.cbi-logo {
  max-width: 200px; 
  max-height: auto;
}


@media (min-width: 830px) {
    .header-title {
    font-size: 1.5rem;
    padding-bottom: 40px;
  }

  .chart-container {
    gap: 10px;
    padding: 0; 
    width: 100%; 
    overflow: hidden; /* Prevent overflow issues */
  }

  .chart-wrapper {
    width: 100%; 
    min-width: 0; /* Reset min-width */
  }

  .chart {
    width: 100%; 
    max-width: 100%; 
    height: auto;
  }

  .overlay-image{
    padding-right: 20px;
    height: 500px;
  }


}


</style>
