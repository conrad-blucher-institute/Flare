<!--
MagnoliaView.vue

Creates the page for the Magnolia charts. This file holds the template
for the page with minimal JS logic.

The JS logic for the magnolia page is found in the useMagnolia.js composable
and the static content for the page is found in the MagnoliaContent.js file.

Created by: CJ Quintero
Created on: 11/20/2026
-->
<script setup>
import { useMagnolia } from "@/composables/useMagnolia.js"
import ChartBanner from "@/components/layout/ChartBanner.vue"
import MissingDataWarningBanner from "@/components/MissingDataWarningBanner.vue"
import ChartSection from "@/components/layout/ChartSection.vue"
import ChartFooter from "@/components/layout/ChartFooter.vue"
import { footerLinks, footerLogos, graphInfo } from "@/content/MagnoliaContent.js"

const { chartOptions, missingDataWarningBanner } = useMagnolia()
</script>

<template>
	<div class="overflow-hidden bg-primary-bg text-dark-text font-main">
		<ChartBanner title="Water Level Trends and Predictions for Magnolia Beach, TX" />
		<MissingDataWarningBanner ref="missingDataWarningBanner" />
		<ChartSection :chartOptions="chartOptions" :graphInfo="graphInfo" />
		<ChartFooter :links="footerLinks" :logos="footerLogos" />
	</div>
</template>
