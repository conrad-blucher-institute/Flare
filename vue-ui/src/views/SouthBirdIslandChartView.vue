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
      /localhost:6100\/south-bird-island-chart.*/,
      'localhost:8080'
    ) + '/csv-data/test.csv',
    enablePolling: true, // Refresh data periodically
    dataRefreshRate: 3600, // Interval for refreshing (in seconds)
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
    <section class="chart-banner">
      <!-- Overlay image on the left -->
      <div class="map-overlay">
        <img src="@/assets/images/MapOverlay-copy.png" alt="Map Overlay" class="overlay-image">
      </div>

      <!-- Text content on the right -->
      <div class="banner-content">
        <h1 class="header-title">Water and Air Temperature Trends and Forecasts for South Bird Island, Texas</h1>
      </div>
    </section>

    <!--Display the Chart-->    
    <Chart  class="chart"  :options="southBirdIslandChart"/>

    <!--Information on how to use the chart--> 
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
          Click and drag across a section of the datapoints to zoom into the selected datapoints. 
        </li>
        <li>
          <span class="icon">🔍</span>
          Click the  <strong> Reset Zoom </strong>  button on the top-right to reset the zoom.
        </li>
        
      </ul>
    </div>
    


    <!-- Section Divider -->
    <div class="section-divider"> </div>

    <!-- About Section -->
    <section class="about-section">
      <h2 class="about-header">South Bird Island Model</h2>
      <div class="about-container">
        <img src="@/assets/images/SBI.jpg" alt="Map of South Bird Island, Texas" class="about-image">
        <div class="about-content">
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

    <!-- Map of Location
    <section class="map-section">
      <h2> South Bird Island Exact Location</h2>        
    </section> -->

        <!-- Meet the Team Section -->
        <section class="team-section">
          <h2 class="team-header">Meet the Team Behind This AI Model</h2>
          <div class="team-members">
            <div class="team-member">
              <img src="@/assets/images/MatthewKastl.png" alt="Matthew Kastl" class="team-image">
              <h3 class="team-name">Matthew Kastl</h3>
              <p class="team-role">Graduate Student</p>
            </div>

            <div class="team-member">
              <img src="@/assets/images/BetoEstrada.png" alt="Beto Estrada" class="team-image">
              <h3 class="team-name">Beto Estrada</h3>
              <p class="team-role">Graduate Student</p>
            </div>

            <div class="team-member">
              <img src="@/assets/images/AnointiyaeBeasley.png" alt="Anointiyae Beasley" class="team-image">
              <h3 class="team-name">Anointiyae Beasley</h3>
              <p class="team-role">Undergraduate Student</p>
            </div>

            <div class="team-member">
              <img src="@/assets/images/SavannahStephenson.png" alt="Savannah Stephenson" class="team-image">
              <h3 class="team-name">Savannah Stephenson</h3>
              <p class="team-role">Graduate Student</p>
            </div>
          </div>
        </section>
  </div>
</template>

<style>


.chart{
  height: 800px;
  padding: 40px;
}
.chart-banner {
  background: var(--dark-blue-gradient); /* Assuming gradient background */
  color: var(--off-white);
  padding: 0px;
  display: flex; /* Use Flexbox for layout */
  justify-content: space-between; /* Position overlay on the left and text on the right */
  align-items: center; /* Vertically align items */
  height: 500px; /* Adjust as needed */
  overflow: hidden;
}

.map-overlay {

  width: 60%; /* Adjust the width as needed */
  height: 100%; /* Make the image as tall as the banner */
  display: flex;
  align-items: center; /* Ensure the image is centered vertically */
  justify-content: flex-start; /* Align the image content to the left */
  overflow: hidden; /* Crop any overflowed part of the image */
}

.overlay-image {
  width: 100%; /* Ensures the image fills the overlay horizontally */
  height: 100%; /* Ensures the image fills the overlay vertically */
  object-fit: cover; /* Crop the image to cover the container */
}

.banner-content {
  flex: 1; /* Allow the text to take available space */
  padding-right: 20px; /* Adds spacing from the right edge */
  text-align: right; /* Align text to the right */
}

.header-title {
  font-size: 2.5rem; /* Adjust for your design */
  text-align: center; /* Align text to the right */
  line-height: 1.4;
  margin: 0;
}


.team-section {
  background-color: var(--deep-teal); /* Light background for contrast */
  text-align: center; /* Center-align text */
  max-width: 100%; /* Limit the width for better readability */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
  padding: 20px;
  height: 500px;
}

.team-header {
  font-size: 2rem;
  color: var(--off-white); /* Accent color for the header */
  margin-bottom: 30px;
}

.team-members {
  display: flex;
  flex-wrap: wrap; /* Allow wrapping on smaller screens */
  justify-content: center; /* Center the cards */
  gap: 50px; /* Space between team members */
}

.team-member {
  background-color: var(--off-white); /* White card background */
  border-radius: 8px; /* Rounded corners for the card */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow for the card */
  text-align: center;
  padding: 20px;
  width: 250px; /* Fixed width for consistency */
  transition: transform 0.3s ease, box-shadow 0.3s ease; /* Hover effect */
}

.team-member:hover {
  transform: translateY(-5px); /* Slight lift on hover */
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2); /* Stronger shadow on hover */
}

.team-image {
  width: 100%;
  height: 200px; /* Fixed height for images */
  object-fit: cover; /* Crop the image to fit the container */
  border-radius: 8px; /* Rounded corners for the image */
  margin-bottom: 15px;
}

.team-name {
  font-size: 1.25rem;
  color: #333; /* Darker text for the name */
  margin-bottom: 10px;
}

.team-role {
  font-size: 1rem;
  color: #666; /* Subtle text color for the role */
}

.page-container {
    padding: 0;
    margin: 0; /* Remove any default margin */
    overflow: hidden; 
}
.about-section {
  background-color: #f9f9f9; /* Light background for contrast */
  border-radius: 8px; /* Rounded corners */
  padding: 20px;
  max-width: 1200px; /* Limit width for better readability */
  margin: 20px auto; /* Center the section horizontally */
}

.about-header {
  text-align: center; /* Center the header text */
  font-size: 2rem; /* Larger font size for the header */
  color: #0f4f66; /* Accent color */
  margin-bottom: 20px; /* Space between the header and the content */
}

.about-container {
  display: flex; /* Flexbox layout for image and text */
  align-items: center; /* Vertically center the image and text */
  gap: 50px; /* Space between the image and text */
}

.about-image {
  flex-shrink: 0; /* Prevent the image from shrinking */
  width: 40%; /* Image occupies 40% of the section */
  max-width: 500px; /* Maximum image width */
  border-radius: 8px; /* Rounded corners */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Subtle shadow for the image */
}

.about-content {
  flex: 1; /* Allow the text to take up the remaining space */
  text-align: center; /* Align text to the left */
  max-width: 900px; /* Maximum image width */
  font-family: 'Arial', sans-serif; /* Clean, readable font */
  padding: 50px;
  color: #333; /* Text color */
}

.about-content p {
  margin-bottom: 15px; /* Space between paragraphs */
  line-height: 1.6; /* Increase line height for better readability */
}

.about-content strong {
  color: #0f4f66; /* Highlight important text with the accent color */
}



.map-section{
  background-color: #0f4f66;
  color: var(--off-white);
  padding: 200px 0px;
}

.instructions-list {
  background-color: #f9f9f9; /* Light background for contrast */
  border-radius: 8px; /* Rounded corners for a softer look */
  padding: 20px; /* Space around the content */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
  font-family: 'Arial', sans-serif; /* Clean, readable font */
  color: #333; /* Text color */
  max-width: 700px; /* Limit the width for better readability */
  margin: 20px auto; /* Center the container on the page */
}

.instructions-list h2 {
  font-size: 1.8rem; /* Larger heading font size */
  margin-bottom: 15px; /* Space below the heading */
  color: #0f4f66; /* Accent color for the heading */
  text-align: center; /* Center-align the heading */
}

.instructions-list ul {
  list-style-type: none; /* Remove default bullet points */
  padding: 0; /* Remove default padding */
  margin: 0; /* Remove default margin */
}

.instructions-list li {
  display: flex; /* Use flexbox for alignment */
  align-items: flex-start; /* Align items at the top */
  margin-bottom: 15px; /* Space between list items */
  font-size: 1.1rem; /* Slightly larger font size */
  line-height: 1.6; /* Better line spacing for readability */
}

.instructions-list li .icon {
  font-size: 1.5rem; /* Larger icon size */
  margin-right: 10px; /* Space between icon and text */
  color: #0f4f66; /* Accent color for the icons */
}

.instructions-list li:last-child {
  margin-bottom: 0; /* Remove bottom margin for the last item */
}

li {
  display: flex; /* Align the icon and text in a single row */
  align-items: flex-start; /* Align items at the top */
  margin-bottom: 15px; /* Space between list items */
  font-size: 1.1rem; /* Adjust font size */
  line-height: 1.6; /* Increase line spacing for readability */
}

li .icon {
  font-size: 1.5rem; /* Larger size for the icon */
  margin-right: 10px; /* Space between the icon and the text */
  color: #0f4f66; /* Accent color for the icon */
}

</style>

