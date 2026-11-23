<!--
ChartFooterLinks.vue

This component contains the footer links that are displayed in the footer
section of pages with charts.

NOTE: This component is setup to only work with external links. These
will use target="_blank" to open in a new tab, and will use anchor tags <a>
instead of router links <router-link>.

Created by: CJ Quintero
Created on: 11/23/2026
-->
<script setup>

/*
  each link in the array should be as:
  {
    href: "https://example.com",
    text: "Example Link"
  }

  Args:
    href (str) - the URL to link to
    text (str) - the visible text on the page for the link
*/
defineProps({
  links: {
    type: Array,
    default: () => []
  }
})
</script>


<template>
<div class="flex flex-col justify-center items-center text-white text-sm lg:text-lg">
  <!-- creates a footer link for each link -->
  <a v-for="(link, index) in links"
  :key="index"
  :href="link.href"
  target="_blank"
  rel="noopener noreferrer"
  class="hover:scale-110 transition-transform">
    {{ link.text }}
  </a>
</div>
</template>
