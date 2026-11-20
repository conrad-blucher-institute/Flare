<!--
ChartHelp.vue

This component has the button and toggle for the "How to Use the Interactive Chart" instructions.
It is a constant component that can be used on any page with a chart and doesn't
accept any props.

Created by: CJ Quintero
Created on: 11/19/2026
-->

<script setup>
/*
  state variable to control the visibility of the chart help popup.
  starts closed and toggles open/closed when the button is clicked
*/
import { ref } from 'vue';
const showChartHelp = ref(false);
</script>

<template>
  <div class="help-wrapper">
    <div class="help-anchor">
      <button @click="showChartHelp = !showChartHelp" class="help-button">
        <span class="help-icon">?</span>
        <span class="help-button-text">How to Use the Interactive Chart</span>
      </button>

      <div v-show="showChartHelp" class="chart-help-popup">
        <h2 class="help-title">How to Use the Interactive Chart</h2>

        <div class="space-y-5">
          <div>
            <h3 class="help-heading">📊 See Temperature Details</h3>
            <p>Hover over any line to see the exact temperature, date, and time.</p>
          </div>

          <div>
            <h3 class="help-heading">🔍 Zoom In</h3>
            <p>Click and drag a box around the area you want to zoom in on.</p>
          </div>

          <div>
            <h3 class="help-heading">🔄 Reset the View</h3>
            <p>After zooming in, click <strong>Reset View</strong> in the top-right corner to zoom back out.</p>
          </div>

          <div>
            <h3 class="help-heading">👆 Show or Hide Chart Lines</h3>
            <p>Click a name in the legend below the chart to show or hide that line.</p>
          </div>

          <div>
            <h3 class="help-heading">🕒 Time</h3>
            <p>Times are shown in your local time zone.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.help-wrapper {
  @apply flex justify-end mb-3 pr-8 pt-3;
}

.help-anchor {
  @apply relative inline-block;
}

.help-button {
  @apply flex items-center gap-2 text-blue-secondary hover:text-blue-600 font-medium;
}

.help-icon {
  @apply flex items-center justify-center w-6 h-6 rounded-full border-2 border-current font-bold text-xs lg:text-sm;
}

.help-button-text {
  @apply text-xs md:text-lg;
}

.chart-help-popup {
  @apply absolute bottom-5 right-0 w-full max-h-[150px] lg:max-h-[250px] overflow-y-auto mb-3
         lg:w-[450px] bg-white rounded-sm shadow-2xl border border-gray-300 p-6 z-50;
}

/* custom scrollbar for the popup (Chrome, Edge, Safari) */
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

.help-title {
  @apply text-lg lg:text-xl font-semibold border-b pb-2 mb-4;
}

.help-heading {
  @apply font-bold;
}
</style>
