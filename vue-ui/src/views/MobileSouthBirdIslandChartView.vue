<!-- ===================================================
     View: MobileSouthBirdIslandChart.vue
     Description: This view displays the air temperature trends and predictions for South Bird Island. 
                  Features include:
                  - A dynamically updating Highcharts line chart using live CSV data.
                  - Instructions for interacting with the chart.
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
      height: 500, // Reduce chart height 
    },
    title: {
      text: 'Temperature of Upper South Bird Island', // Simplified title for smaller screens
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
      csvURL: `http://localhost:8080/csv-data/test.csv`, // Will be changed for production
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
          fontSize: '12px', // Smaller font size for x-axis labels
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
        <h1 class="header-title">Water and Air Temperature Trends and Forecasts for South Bird Island, Texas</h1>
      </div>
    </section>

    <div class="chart-container">
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
    </div>
    
    <!-- Section Divider -->
    <div class="section-divider"> </div>

    <!-- About Section -->
    <section class="about-section">
      
      <div class="about-container">
        <img src="@/assets/images/SouthBirdIslandMap.jpg" alt="Map of South Bird Island, Texas" class="about-image">
        <div class="about-content">
          <h2 class="about-header">South Bird Island Model</h2>

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

   <!-- Meet the Team Section -->
   <section class="coldstunning-team-section">
     <h2 class="coldstunning-team-header">Meet the Team Behind This AI Model</h2>
     <div class="coldstunning-coldstunning-team-members">
       <div class="coldstunning-team-member">
         <img src="@/assets/images/MatthewKastl.png" alt="Matthew Kastl" class="team-image">
         <h3 class="coldstunning-team-name">Matthew Kastl</h3>
         <p class="coldstunning-team-role">Graduate Student</p>
       </div>

       <div class="coldstunning-team-member">
         <img src="@/assets/images/BetoEstrada.png" alt="Beto Estrada" class="team-image">
         <h3 class="coldstunning-team-name">Beto Estrada</h3>
         <p class="coldstunning-team-role">Graduate Student</p>
       </div>

       <div class="coldstunning-team-member">
         <img src="@/assets/images/AnointiyaeBeasley.png" alt="Anointiyae Beasley" class="team-image">
         <h3 class="coldstunning-team-name">Anointiyae Beasley</h3>
         <p class="coldstunning-team-role">Undergraduate Student</p>
       </div>

       <div class="coldstunning-team-member">
         <img src="@/assets/images/SavannahStephenson.png" alt="Savannah Stephenson" class="team-image">
         <h3 class="coldstunning-team-name">Savannah Stephenson</h3>
         <p class="coldstunning-team-role">Graduate Student</p>
       </div>
     </div>
   </section>
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
  padding-right: 10px;
  

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
  background-color: var(--primary-background);
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

/* About Section */
.about-section {
  padding: 20px 10px;
  margin: 10px auto;
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

/* Team Section */
.coldstunning-team-section {
  background: var(--section-gradient-background);
  color: var(--primary-background);
  text-align: center;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.coldstunning-team-header {
  font-size: 1.2rem;
  margin-bottom: 20px;
}

.coldstunning-coldstunning-team-members {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 30px;
}

.coldstunning-team-member {
  width: 70%;
  background-color: var(--primary-background);
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
  padding: 20px;
}

.team-image {
  width: 200px;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 15px;
}

.coldstunning-team-name {
  font-size: 1rem;
  color: var(--primary-text-light-background);
  margin-bottom: 10px;
}

.coldstunning-team-role {
  font-size: 0.85rem;
  color: var(--secondary-text);
}
</style>
