<!--
GraphSpecificInfo.vue

This component contains the sidebar for the graph specific information
that is displayed to the right of the chart.

Created by: CJ Quintero
Created on: 11/23/2026
-->
<script setup>
/*
	Accepts embedded HTML for advanced formatting of each section.
	The text is displayed in a scrollable container to the right of the chart.

	Args:
		purpose (String) - The purpose section text
		howToRead (String) - How to read section text
		whatToLookFor (String) - What to look for section text
		keepInMind (String) - Things to keep in mind section text
*/
defineProps({
	purpose: {
		type: String,
		required: true,
	},
	howToRead: {
		type: String,
		required: true,
	},
	whatToLookFor: {
		type: String,
		required: true,
	},
	keepInMind: {
		type: String,
		required: true,
	},
})
</script>

<template>
	<div class="max-h-[500px] lg:max-h-[750px] p-6 flex flex-col">
		<!-- header -->
		<h2 class="text-lg lg:text-3xl font-semibold text-center text-dark-text border-b-2 border-dark-text pb-2 mb-6">
			Graph-Specific Information
		</h2>

		<!-- scrollable content -->
		<div class="graph-scroll flex-1 overflow-y-auto space-y-8 text-dark-text pr-2">
			
			<!-- Purpose -->
			<div>
				<h3 class="text-lg lg:text-xl font-bold mb-2">Purpose</h3>
				<p class="leading-relaxed" v-html="purpose"></p>
			</div>
			<hr class="border-t border-dark-text">

			<!-- How to Read -->
			<div>
				<h3 class="text-lg lg:text-xl font-bold mb-2">How to Read</h3>
				<p class="leading-relaxed" v-html="howToRead"></p>
			</div>
			<hr class="border-t border-dark-text">

			<!-- What to Look For -->
			<div>
				<h3 class="text-lg lg:text-xl font-bold mb-2">What to Look For</h3>
				<p class="leading-relaxed" v-html="whatToLookFor"></p>
			</div>
			<hr class="border-t border-dark-text">

			<!-- Keep in Mind -->
			<div>
				<h3 class="text-lg lg:text-xl font-bold mb-2">Keep in Mind</h3>
				<p class="leading-relaxed" v-html="keepInMind"></p>
			</div>

		</div>
	</div>
</template>

<style scoped>
/* scroll bar styling */
.graph-scroll::-webkit-scrollbar { width: 6px; }
.graph-scroll::-webkit-scrollbar-track { background: #404048; }
.graph-scroll::-webkit-scrollbar-thumb { background: #1c76c5; border-radius: 9999px; }
.graph-scroll::-webkit-scrollbar-thumb:hover { background: #4a82b3; }
</style>
