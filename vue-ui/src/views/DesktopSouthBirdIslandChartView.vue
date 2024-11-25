<!-- ===================================================
     View: DesktopSouthBirdIslandChart.vue
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
      text: 'Temperature of Upper South Bird Island', 
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
      csvURL:`http://localhost:8080/csv-data/test.csv`, // Will be changed for production
      enablePolling: true, // Refresh data periodically
      dataRefreshRate: 3600, // Interval for refreshing in seconds
      complete: function (data) {
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
        <h1 class="header-title">Water and Air Temperature Trends and Forecasts for South Bird Island, Texas</h1>
      </div>
    </section>

    <div class="chart-container">
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
  background-color: var(--primary-background); /* Style for the instructions section */
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

/* Team Section Styles*/
.coldstunning-team-section {
  background: var(--section-gradient-background);
  color:var(--primary-background); 
  text-align: center;
  max-width: 100%;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); 
  padding: 40px 20px; 
  height: auto;
  overflow: hidden; 
}

.coldstunning-team-header {
  font-size: 2.6rem;
  color: var(--primary-text-dark-background);
  margin-bottom: 30px;
  padding: 50px;
}

.coldstunning-coldstunning-team-members {
  display: flex;
  flex-wrap: wrap; 
  justify-content: center;
  gap: 70px; 
  padding-bottom: 50px;
}

.coldstunning-team-member {
  background-color: var(--primary-background); 
  border-radius: 8px; /* Rounded corners for the card */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); 
  text-align: center;
  padding: 40px;

  width: 250px; 
  transition: transform 0.3s ease, box-shadow 0.3s ease; /* Hover effect */
}

.coldstunning-team-member:hover {
  transform: translateY(-5px); /* Slight lift on hover */
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2); /* Stronger shadow on hover */
}

.team-image {
  width: 80%;
  height: 80%;
  object-fit: cover; /* Crop the image to fit the container */
  border-radius: 8px; /* Rounded corners for the image */
  margin-bottom: 15px;
}

.coldstunning-team-name {
  font-size: 1.25rem;
  color: var(--primary-text-light-background); ;
  margin-bottom: 10px;
}

.coldstunning-team-role {
  font-size: 1rem;
  color: var(--secondary-text); 
}




</style>

