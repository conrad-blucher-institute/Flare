<template>
    <div>
      <h2>CSV Data</h2>
      <div v-if="loading">Loading CSV data...</div>
      <div v-else-if="error">{{ error }}</div>
      <div v-else>
        <pre>{{ csvData }}</pre> <!-- Display raw CSV data here -->
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        csvData: null,
        loading: true,
        error: null,
      };
    },
    mounted() {
      this.fetchCSVData();
    },
    methods: {
      fetchCSVData() {
        fetch('http://localhost:8080/test-chart/test.csv')
          .then((response) => response.text())
          .then((data) => {
            this.csvData = data;
            console.log(data); // Log CSV data to console
            this.loading = false;
          })
          .catch((error) => {
            this.error = 'Error fetching CSV data';
            console.error('Error fetching CSV data:', error);
            this.loading = false;
          });
      },
    },
  };
  </script>
  
  <style scoped>
  /* Add component-specific styles if needed */
  </style>
  