<!-- ===================================================
Component: MissingDataWarningBanner.vue
Description: 
  This is a warning banner to be used on pages with charts. 
  checkForMissingDataAndWarn can be called to show the banner if 
  any charts contain missing data.
Author: Matthew Kastl
Date: 8/27/2025
======================================================= -->

<template>
  <div v-show="isVisible" class="missing-data-warning-banner">
    <p>⚠️ Warning: Some data is currently unavailable and missing from the charts below:</p>
    <p class="missing-list">{{ missingSeries.join(', ') }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const isVisible = ref(false);   // hidden by default
const missingSeries = ref([]);  // names of series with no data

/**
 * Checks a page's charts for missing data and shows the banner
 * listing any series that have no data.
 * @param {Array.<Object>} charts A list of each chart's options to check
 * @returns {void}
 */
const checkForMissingDataAndWarn = (charts) => {
  // a Set removes duplicates, so a series that appears
  // on several charts is only listed once
  const missing = new Set();

  charts.forEach(chart => {
    // some series in this chart have no data
    chart.series.forEach(series => {
      if (!series.data || series.data.length === 0) {
        console.warn("Missing data for series:", series);
        missing.add(series.name);
      }
    });
  });

  missingSeries.value = [...missing];
  isVisible.value = missing.size > 0;
};

defineExpose({ checkForMissingDataAndWarn });
</script>

<style scoped>
.missing-data-warning-banner {
  display: flex;
  flex-direction: column;   /* stack the two lines */
  align-items: center;
  justify-content: center;
  width: 100vw;
  background-color: #fffbe6;
  text-align: center;
  color: #856404;
  padding: 16px;
  border: 1px solid #ffe58f;
  box-sizing: border-box;
  position: relative;
  left: 50%;
  right: 50%;
  margin-left: -50vw;
  margin-right: -50vw;
  gap: 4px;
}

.missing-list {
  font-weight: bold;
}
</style>
