<!--
ChartBanner.vue

This component holds the page banner used at the top of chart pages.
It contains the title of the chart page with a background image of the clouds.

Created by: CJ Quintero
Created on: 11/23/2026
-->
<script setup>
/*
	Args:
		title: The title of the chart page to be displayed in the banner such as
			'Water Temperature Trends and Forecasts for Laguna Madre, TX'
*/
defineProps({
	title: {
		type: String,
		required: true,
	},
})
</script>

<template>
<section class="bg-banner-gradient-2 w-full text-white h-[200px] lg:h-[250px]">
	<div class="relative w-full h-full" >
		<img
			src="@/assets/images/clouds.jpg"
			alt=""
			class="w-full h-full object-cover opacity-30"
		/>

		<div class="absolute inset-0 flex items-center justify-center">
			<h1 class="max-w-[1500px] text-lg md:text-3xl lg:text-5xl font-bold text-center px-5">
				{{ title }}
			</h1>
		</div>
	</div>
</section>
</template>
