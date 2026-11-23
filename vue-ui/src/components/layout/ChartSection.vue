<!--
ChartSection.vue

This component is a wrapper for the Highcharts chart component and bundles
the chart with the sidebar information for the chart

Created by: CJ Quintero
Created on: 11/23/2026
-->
<script setup>
import { Chart } from "highcharts-vue"
import ToggleLegendItemsText from "@/components/ToggleLegendItemsText.vue"
import GraphSpecificInfo from "./GraphSpecificInfo.vue"

/*
	Args:
		chartOptions (Object) - The options for the chart

		graphInfo (Object) - An object containing the purpose, howToRead, whatToLookFor, and keepInMind text for the graph
			that is passed to the GraphSpecificInfo component
		
		bgColor (String) - The background color for the chart and sidebar panels.
			Default is "rgba(15, 130, 245, 0.06)"
*/
defineProps({
	chartOptions: {
		type: Object,
		required: true,
	},
	graphInfo: {
		type: Object, // { purpose, howToRead, whatToLookFor, keepInMind }
		required: true
	},
	bgColor: {
		type: String,
		required: false,
		default: "rgba(15, 130, 245, 0.06)"
	}
})
</script>

<!--
NOTE: v-bind="graphInfo" passes each key in graphInfo (purpose, howToRead,
whatToLookFor, keepInMind) as its own prop, so they don't have to be listed
one by one.
-->
<template>
<section class="grid grid-cols-1 lg:grid-cols-5 gap-4 px-2 lg:py-8 lg:px-4 bg-white items-stretch">
	<!-- the chart takes up 4 of the 5 columns -->
	<div class="panel lg:col-span-4 relative border sm:w-full" :style="{ '--panel-bg': bgColor}">
		<div class="w-full overflow-x-auto">
			<div class="flex flex-col p-4 min-w-[600px] min-h-[350px] lg:min-w-[1000px] lg:h-[700px] lg:min-h-[650px]">
				<Chart class="w-full flex-1 min-h-0" :options="chartOptions" />
				<ToggleLegendItemsText />
			</div>
		</div>
	</div>

	<!-- the sidebar takes up the last column and is to the right of the chart -->
	<div class="panel flex flex-col h-full min-h-0" :style="{ '--panel-bg': bgColor}">
		<GraphSpecificInfo v-bind="graphInfo" />
	</div>
</section>
</template>

<style scoped>
.panel {
	background-color: var(--panel-bg);
	border-radius: 20px;
	box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}
</style>