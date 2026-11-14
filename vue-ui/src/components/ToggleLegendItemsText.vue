<!-- ===================================================
ToggleLegendItemsText.vue

This component has the text for how to toggle legend items
that goes below the legend on all charts

Created on: 11/14/2026
Created by: CJ Quintero

Usage:
	<ToggleLegendItemsText />
	<ToggleLegendItemsText text="Custom text here" textClass="text-red-500" bgClass="bg-gray-200" />
======================================================= -->
<script setup>
defineProps({
	/*
		Props:
			text: The text to display below the chart legend that accepts embedded HTML.
			
			textClass: The tailwind text color class.
				Defaults to the usual dark blue on all pages found in tailwind.config.js.
			
			bgClass: The tailwind background color class of the text. Defaults to white.
				This should match the background of the chart.
	*/

	text: {
		type: String,
		default: '<strong>To Show or Hide Chart Lines</strong>, click on the legend items above to turn lines on and off.',
	},
	textClass: {
		type: String,
		default: 'text-dark-text',
	},
	bgClass: {
		type: String,
		default: 'bg-white',
	},
});
</script>

<template>
	<div :class="['toggle-legend-items-text', textClass, bgClass]">
		<span v-html="text"></span>
	</div>
</template>

<style scoped>
.toggle-legend-items-text {
	/*
		Styling for the component that is always the same,
		regardless of the text and background colors
	*/

	@apply text-center text-base lg:text-lg;
}
</style>
