<!-- ===================================================
     View: PortAransasWinds.vue
     Description: This view displays the air temperature trends and predictions for South Bird Island.
                  Features include:
                  - A dynamically updating Highcharts line chart using live CSV data.
                  - Instructions for interacting with the chart.
                  - Information on the data of the chart.
                  - Additional links
                  - Informative sections about South Bird Island and its environmental significance.
     Author: Beto Estrada
     Created: 04/13/2023
     Last Updated: 10/14/2025 by Christian Quintero
======================================================= -->
<script setup>

import Highcharts from 'highcharts';
import Data from 'highcharts/modules/data';
import Exporting from 'highcharts/modules/exporting';
import ExportData from 'highcharts/modules/export-data';
import Accessibility from 'highcharts/modules/accessibility';
// import Jquery 
 
function getAPIData(apiUrls) {
    // Fetch data from all APIs
    Promise.all(
        apiUrls.map((apiUrl) =>
        fetch(apiUrl).then((response) => response.json()))
    )
    .then((apiData) => {
        // Format data from each API
        const formattedData = apiData.map((data, i) => {
        // Extract the column names from the keys of the first element
        const columnNames = Object.keys(data[0]).filter(
        (column) => column !== "date"
        );
        // Find the index of the "date" column
        const dateColumnIndex = Object.keys(data[0]).indexOf("date");

        // Format data for all APIs
        const formattedData = data.map((d) => {
        const values = Object.values(d)
            .filter((column, index) => index !== dateColumnIndex)
            .map((value) => parseFloat(value));
            return [new Date(d.date).getTime(), ...values];
        });

        // Map over formattedData and create an array of objects with the date and the values for each column
        const seriesData = formattedData.map((row) => {
            const data = {};
            data["date"] = row[0];
            columnNames.forEach((name, index) => {
                data[name] = row[index + 1];
            });
            return data;
        });

        // Create Highcharts series
        return columnNames.map((name) => {
            return {
                name: name,
                data: seriesData.map((d) => [d.date, d[name]]),
                dashStyle: i === 0 ? "Solid" : "Dash"
            };
            });
        });

        // Create Highcharts chart using combined and sorted data
        Highcharts.setOptions({
            time: {
                useUTC: false,
                timezone: "America/Chicago",
            },
            lang: {
                shortWeekdays: [
                  "Sun",
                  "Mon",
                  "Tue",
                  "Wed",
                  "Thu",
                  "Fri",
                  "Sat",
                ],
              },
        });

        Highcharts.chart("container", {
            chart: {
                zoomType: "x",
                panKey: "alt",
            },
            title: {
                text: "Wind Speed Measurements and Predictions Over the Past Week",
                style: {
                    fontSize: "170%",
                },
            },
            xAxis: {
                type: "datetime",
                dateTimeLabelFormats: {
                  day: "%a %b %e",
                },
                title: {
                  text: "Time (CDT)",
                  style: {
                    fontSize: "150%",
                  },
                },
                plotLines: [
                  {
                    // Mark now
                    enablePolling: true,
                    color: "red",
                    width: 2,
                    value: Date.now(),
                    dashStyle: "Solid",
                    label: {
                      text: "Now",
                      color: "red",
                    },
                  },
                ],
                labels: {
                  padding: 25,
                  style: {
                    fontSize: "130%",
                    color: "black",
                  },
                },
              },
            yAxis: {
                title: {
                  text: "Wind Speed (mph)",
                  style: {
                    fontSize: "150%",
                  },
                },
            },

        colors: ["black", "grey", "orangered", "orange"],

        series: [...formattedData.flat()],
    });
    }) // end .then 
    .catch((error) => console.error(error));
} // end getAPIData

const HOST_URL = '<%= process.env.HOST_URL %>';
// Example function call with array of API URLs
getAPIData([
    `${HOST_URL}/sailwind/api/ndbc/measurements/file_format=json/data_type=std/station_id=PTAT2/product=WSPD/units=mph/last45days`,
    `${HOST_URL}/sailwind/api/nwps/predictions/wind/file_format=json/location=hcp/cg=cg1/units=mph`,
]);

// Refresh data every 10 minutes
setInterval(() => {
    getAPIData([
        `${HOST_URL}/sailwind/api/ndbc/measurements/file_format=json/data_type=std/station_id=PTAT2/product=WSPD/units=mph/last45days`,
        `${HOST_URL}/sailwind/api/nwps/predictions/wind/file_format=json/location=hcp/cg=cg1/units=mph`,
    ]);
}, 600000);

</script>


<template>
    <div class="container-fluid" style="background-color: white">
        <div id="container" class="chart">
        </div>
    </div>
</template>