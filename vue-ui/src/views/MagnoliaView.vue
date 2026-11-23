<!--
MagnoliaView.vue

Creates the page for the Magnolia charts. This file holds the template
for the page with minimal JS logic. The logic is contained in the useMagnolia.js composable.

Created by: CJ Quintero
Created on: 11/20/2026
-->
<script setup>
import { Chart } from "highcharts-vue"
import { useMagnolia } from "@/composables/useMagnolia.js"

import ChartBanner from "@/components/layout/ChartBanner.vue"
import MissingDataWarningBanner from "@/components/MissingDataWarningBanner.vue"
import ChartFooter from "@/components/layout/ChartFooter.vue"

const { chartOptions, missingDataWarningBanner, footerLinks, footerLogos } = useMagnolia()
</script>

<template>
	<div class="overflow-hidden bg-primary-bg text-dark-text font-main">
		<ChartBanner title="Water Level Trends and Predictions for Magnolia Beach, TX" />
		<MissingDataWarningBanner ref="missingDataWarningBanner" />
		<Chart class="w-full p-4" :options="chartOptions" />
		<ChartFooter :links="footerLinks" :logos="footerLogos" />
	</div>
</template>
