<!-- ===================================================
     View: DesktopSouthBirdIslandChart.vue
     Description: This view displays the air temperature trends and predictions for South Bird Island. 
                  Features include:
                  - A dynamically updating Highcharts line chart using live CSV data.
                  - Instructions for interacting with the chart.
                  - Information on the data of the chart.
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
  console.log("Highcharts data module initialized:", dataModule);


  // Define the current date and time
  const nowDate = new Date();// Current timestamp
  const nowTime = new Date(nowDate); // Convert to a Date object

  // Highcharts object for Desktop
  const desktopSouthBirdIslandChart = {
    chart: {
      type: 'line', // Specifies a line chart
      styledMode: false, // Inline styles for better customizability
      zoomType: 'x', // Enable horizontal zooming
      panKey: 'alt', // Hold "Alt" to pan across the chart
      backgroundColor: 'white',
      style: {
        fontFamily: 'Georgia',
      },
    },
    title: {
      text: 'Temperature of Upper Laguna Madre', 
      style: {
        fontSize: '30px', 
        fontWeight: 'bold',
        color: '#0f4f66', 
        fontFamily: 'Georgia', 
      },
    },
    subtitle: {
      text: '', 
      style: {
        fontFamily: 'Georgia', 
      },
    },
    legend: {
      itemStyle: {
        fontSize: '19px', 
        fontWeight: 'bold', 
        fontFamily: 'Georgia',
        color: '#0f4f66', 
        
      },
    },
    data: {
      // URL for fetching CSV data dynamically
      csvURL:`${window.location.origin}/flare/csv-data/test.csv`, 
      enablePolling: true, // Refresh data periodically
      dataRefreshRate: 3600, // Interval for refreshing in seconds
      complete: function (chartData) {
        // Parse and filter CSV data for the chart
        const waterTemperatureMeasurements = chartData.series?.[0] || { data: [] };
        const waterTemperaturePredictions = chartData.series?.[1] || { data: [] };
        const airTemperatureMeasurements = chartData.series?.[2] || { data: [] };
        const airTemperaturePredictions = chartData.series?.[3] || { data: [] };

        //Check for valid date entries
        const filterDataBefore = (data) =>
          data.filter((point) => point[0] && new Date(point[0]) <= nowTime);
        const filterDataAfter = (data) =>
          data.filter((point) => point[0] && new Date(point[0]) >= nowTime);

        // Filter measurements and predictions
        const filteredWaterMeasurementData = filterDataBefore(waterTemperatureMeasurements.data);
        const filteredWaterPredictionData = filterDataAfter(waterTemperaturePredictions.data);
        const filteredAirMeasurementData = filterDataBefore(airTemperatureMeasurements.data);
        const filteredAirPredictionData = filterDataAfter(airTemperaturePredictions.data);

        // Update the chart with filtered data
        chartData.series = [
          {
            name: 'Water Temperature Measurements',
            data: filteredWaterMeasurementData,
            color: 'blue',
            lineWidth: 4,
            marker: { enabled: false }, // Hide data markers
          },
          {
            name: 'Predicted Water Temperature',
            data: filteredWaterPredictionData,
            color: 'blue',
            dashStyle: 'Dash', 
            lineWidth: 5, 
            marker: { enabled: false },
          },
          {
            name: 'Air Temperature Measurements',
            data: filteredAirMeasurementData,
            color: 'black',
            lineWidth: 4,
            marker: { enabled: false },
          },
          {
            name: 'Interpolated Predicted Air Temperature',
            data: filteredAirPredictionData,
            color: 'black',
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
          fontSize: '130%', 
          color: '#0f4f66',
          fontFamily: 'Georgia', 
        },
      },
      title: {
        text: 'Temperature (°F)', 
        style: {
          fontSize: '150%', 
          fontFamily: 'Georgia',
          
          
        },
      },
      max: 90, // Maximum temperature shown on the chart
      min: 20, // Minimum temperature shown on the chart
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
              fontSize: '20px',
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
              fontSize: '20px',
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
        fontSize: '22px',
        fontWeight: 'bold',
        fontFamily: 'Georgia', 
        color: '#0f4f66',
      },
      step: 2, // Show every second label
    },
    title: {
      text: 'Time',
      style: {
        fontSize: '150%',
        fontFamily: 'Georgia', 
        color: '#0f4f66',
      },
    },
    maxPadding: 0.10, 
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
            fontSize: '18px',
            fontWeight: 'bold',
            fontFamily: 'Georgia', 
          },
        },
      },
    ],
  },

    tooltip: {
      shared: false, 
      crosshairs: true, // Display crosshairs on hover
      formatter: function () {
        return `<b>Date: ${Highcharts.dateFormat('%A, %b %e, %Y', this.x)}</b><br>
                Temperature: ${this.y}°F`;
      },
      style: {
        fontSize: '18px', 
        padding: '10px', 
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
        <img src="@/assets/images/MapOverlayDesktop.png" alt="Map Overlay" class="overlay-image">
      </div>

      <!-- Text content on the right of the overlay image-->
      <div class="banner-content">
        <h1 class="header-title">Water and Air Temperature Trends and Forecasts for the Texas Upper Laguna Madre</h1>
      </div>
    </section>

    <section class="chart-container">
      <!-- Display the Chart -->
        <Chart class="chart" :options="desktopSouthBirdIslandChart" />

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
    margin: 0; /* Remove any default margin */
    overflow: hidden; 
}

 /* Banner Section */
.chart-banner {
  background: var(--banner-gradient-background);
  color: var(--primary-background);
  padding: 0px;
  display: flex; 
  justify-content: space-between; /* Position overlay on the left and text on the right */
  align-items: center; 
  height: 500px; 
  overflow: hidden;
}

.overlay-image {
  width: 1500px; 
  height: 510px;
  object-fit: cover;
  opacity: 100%;

}

.banner-content {
  flex: 2; 
  text-align: right; 

}

.header-title {
  font-size: 2.5rem; 
  text-align: center; 
  line-height: 1.4;
  margin: 0;
  padding-bottom: 70px;


}

/* Chart Section Styles */
.chart-container {
  display: grid;
  grid-template-columns: 17fr 3fr; /* 85% for chart and 15% for instructions */
  align-items: flex-start; /* Align items to the top of the grid */
  gap: 16px; 
  overflow: hidden;
  height: 900px; 
}

.chart {
  width: 100%; 
  height: 100%; 
  padding: 20px;
}



.instructions-list {
  background-color: var(--accent-background); /* Style for the instructions section */
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden; 
  font-size: 1rem;
  height: 100%; /* Instructions take full height of the grid cell */
}

/* Instructions List Styles */
.instructions-list h2 {
  font-size: 1.8rem; 
  margin-bottom: 15px; 
  color: var(--primary-text-light-background);
  text-align: center;
}
.instructions-list ul {
  list-style: none; /* Remove default list styling */
  padding: 0;
  margin: 0;


}

.instructions-list li {
  margin-bottom: 12px; /* Add spacing between list items */
}

.instructions-list .icon {
  margin-right: 8px; 
  font-size: 1.2em; 
}

.instructions-list li:last-child {
  margin-bottom: 0; /* Remove bottom margin for the last item */
}

li {
  display: flex; 
  align-items: flex-start; /* Align items at the top */
  margin-bottom: 15px;
  font-size: 1.1rem; 
  line-height: 1.6; 
}

li .icon {
  font-size: 1.5rem; 
  margin-right: 10px; 
  color: var(--primary-text-light-background); 
}

/* Chart Data Info Section */
.chart-data-info {
  background-color: var(--accent-background); 
  padding: 25px 30px;
  box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15); /* Slightly deeper shadow for a modern look */
  font-size: 1rem;
  line-height: 1.8;
  border: 1px solid rgba(0, 0, 0, 0.1); 
}

/* Section Title */
.chart-data-info h3 {
  font-size: 1.6rem; 
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
  padding-left: 0; /* Align to container */
}

.chart-data-info li {
  display: flex; 
  align-items: center; /* Vertically center items */
  margin-bottom: 15px;
  color: var(--secondary-text);
  font-size: 1.1rem; 
}

.chart-data-info li:before {
  content: "•"; /* Add custom bullet */
  font-size: 1.5rem; /* Larger bullet size */
  color: var(--primary-text-light-background); 
  margin-right: 10px; /* Space between bullet and text */
}



/* About Section Styles */
.about-section {
  max-width: 1200px; 
  margin: 20px auto; 
  height: auto;
}

.about-header {
  text-align: center; 
  font-size: 2rem; 
  color: var(--primary-text-light-background);  
  margin-bottom: 20px; 
}

.about-container {
  display: flex; 
  align-items: left; 
  gap: 100px; 
  padding:40px;
}

.about-image {
  flex-shrink: 0; /* Prevent the image from shrinking */
  width: auto; 
  max-width: 1000px; 
  border-radius: 8px; /* Rounded corners */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); 
  align-items: left;
  max-height: 600px;
}

.about-content {
  flex: 1; 
  text-align: center;
  max-width: 900px; 
  color: var(--secondary-text);
 
}

.about-content p {
  margin-bottom: 15px; 
  line-height: 1.6; 
  width: 800px;
  font-size: 1.5rem;
}

.about-content strong {
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
  max-width: 150px;
  max-height: 150px;
  object-fit: contain;
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
  max-width: 150px;
  max-height: 150px;
  object-fit: contain;
}

/* Specific Style for CBI Logo */
.cbi-logo {
  max-width: 300px; /* Larger width for the CBI logo */
  max-height: auto;
}


/* Footer Info */
.footer-info {
  font-size: 14px;
  color: var(--primary-text-dark-background);
  margin-top: 30px;
  text-align: center;
}

</style>

