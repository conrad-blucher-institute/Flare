<!--
ChartFooterLogos.vue

This component contains the footer stakeholder logos that are
displayed in the footer section of pages with charts.

Created by: CJ Quintero
Created on: 11/23/2026
-->
<script setup>

/*
  each logo in the array should be as:
  {
    href: "https://example.com",
    src: "logo.png",
    alt: "Example Logo",
    class: "max-w-[80px] lg:max-w-[150px]"
  }

  Args:
    href (str) - the stakeholder's website URL to link to
    src (str) - the image file name in src/assets/images, e.g. 'CBI-Logo.png'
    alt (str) - the alt text for the logo image
    class (str) - optional class styling for the logo image to override the default.
      Defaults to 'max-w-[80px] lg:max-w-[150px]'
*/
defineProps({
  logos: {
    type: Array,
    default: () => []
  }
})

const images = import.meta.glob("@/assets/images/*", {
  // fetches all images in the folder
  eager: true,
  import: "default",
})

const logoUrl = (name) => {
  // get the image URL from the imported images object
  const url = images[`/src/assets/images/${name}`]
  if (!url) { console.warn(`ChartFooterLogos: no image named "${name}" in src/assets/images`) }
  return url
}
</script>


<template>
<div class="flex flex-wrap justify-center items-center gap-8 lg:gap-16 mx-auto p-1 lg:p-4">
  <!-- create an anchor for each logo -->
  <a v-for="(logo, index) in logos"
  :key="index"
  :href="logo.href"
  class="hover:scale-110 transition-transform"
  target="_blank"
  rel="noopener noreferrer"
  >
    <img :src="logoUrl(logo.src)" :alt="logo.alt" :class="logo.class || 'max-w-[80px] lg:max-w-[150px]'">
  </a>
</div>
</template>
