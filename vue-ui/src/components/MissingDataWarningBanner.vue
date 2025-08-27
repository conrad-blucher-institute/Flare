<!-- ===================================================
     Component: MissingDataWarningBanner.vue
     Description: 
        This is a warning data to be used on pages with charts. 
        checkForMissingDataAndWarn can be called to show the chart if 
        any charts contain missing data.
     Author: Matthew Kastl
     Date: 8/27/2025
======================================================= -->

<template>
    <div class="missing-data-warning-banner">
        {{ bannerText }}
    </div>
</template>

<script setup>
import { ref } from 'vue';
const bannerText = ref('');

// Functions to show and hide the banner on a page
function showBanner(text) {
    bannerText.value = text;
    const banner = document.querySelector('.missing-data-warning-banner');
    if (banner) {
        banner.style.display = '';
    }
}

function hideBanner() {
    const banner = document.querySelector('.missing-data-warning-banner');
    if (banner) {
        banner.style.display = 'none';
    }
}

 /**
 * This function is to be called externally to check for missing data in a pages charts
 * and show the warning banner if any missing data is found
 * @param {Array.<Object>} charts A list of each chart to check for missing data
 * @returns {void}
 */
const checkForMissingDataAndWarn = (charts) => {
    const moreThanOneChart = charts.length > 1;
    charts.forEach(chart => {
        let chartHasMissingData = false;
        if (!chart.series || chart.series.length === 0) {
            console.warn("A Warning banner will be displayed to user. No series found in chart:", chart);
            chartHasMissingData = true;
        }
        else {
            chart.series.forEach(series => {
                if (!series.data || series.data.length === 0) {
                    console.warn("A Warning banner will be displayed to user. Missing data in series:", series);
                    chartHasMissingData = true;
                }
            });
        }

        if (chartHasMissingData) {
            showBanner(`⚠️ Warning: ${moreThanOneChart ? 'Charts' : 'Chart'} may be inaccurate due to missing data.`);
        } else {
            hideBanner();
        }
    });
}
defineExpose({ checkForMissingDataAndWarn });

hideBanner(); // Hide by default
</script>


<style scoped>
.missing-data-warning-banner {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100vw;
    background-color: #fffbe6;
    text-align: center;
    color: #856404;
    padding: 16px;
    text-align: center;
    border: 1px solid #ffe58f;
    box-sizing: border-box;
    position: relative;
    left: 50%;
    right: 50%;
    margin-left: -50vw;
    margin-right: -50vw;
}

</style>
