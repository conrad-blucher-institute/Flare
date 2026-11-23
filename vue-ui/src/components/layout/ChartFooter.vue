<!--
ChartFooter.vue

This component contains the footer section for pages with charts.
It has 2 components: the footer links, and the stakeholders list.

Created by: CJ Quintero
Created on: 11/23/2026
-->
<script setup>
import ChartFooterLinks from './ChartFooterLinks.vue'
import ChartFooterLogos from './ChartFooterLogos.vue'

// see the respective components for more details
// on the props and their expected structures
defineProps({
  links: {
    type: Array,
    default: () => []
  },
  logos: {
    type: Array,
    default: () => []
  }
})
</script>

<template>
<footer class="bg-navy-blue py-10 text-white space-y-2">
  <ChartFooterLinks :links="links" />
  <ChartFooterLogos :logos="logos" />
  <span class="flex justify-center py-10">© 2026 Flare. All rights reserved.</span>
</footer>
</template>
