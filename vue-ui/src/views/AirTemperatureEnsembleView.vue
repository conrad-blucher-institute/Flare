<!-- ===================================================
     View: AirTemperatureEnsembleView.vue
     Description: This view displays the air temperature ensemble trends and predictions for South Bird Island.
                  Features include:
                  - A dynamically updating Highcharts line chart using live CSV data.
                  - Instructions for interacting with the chart.
                  - Information on the data of the chart.
                  - Additional links
                  - Informative sections about South Bird Island and its environmental significance.
     Author: Anointiyae Beasley
     Date: 03/31/2025
======================================================= -->
<script setup>

</script>

<template>
  <div class="overflow-hidden bg-primary-bg text-dark-text font-main">

    <!-- Banner Section -->
  <section class="bg-banner-gradient-2 w-full text-white h-[300px] lg:h-[500px]">
    <!-- Overlay image on the left -->
    <div class="relative w-full h-full" >
      <img
        src="@/assets/images/LagunaMadreBay.jpg"
        alt="Map Overlay"
        class="w-full h-full object-crop flex opacity-30"
      />
      <!-- Text content overlay -->
      <div class="absolute  inset-0 flex items-center justify-center">
        <h1 class=" max-w-[1500px] text-lg md:text-3xl lg:text-5xl font-bold text-center pr-5 pl-5">
         Ensemble Air Temperature Trends for the Texas Upper Laguna Madre
        </h1>
      </div>
    </div>
  </section>

  


     


    <!-- Footer -->
    <footer class="bg-navy-blue py-10 text-dark-text space-y-2">
      <div class="flex flex-col justify-center items-center text-white text-sm lg:text-lg">
        <a href="https://tpwd.texas.gov/" target="_blank" class="hover:scale-110 transition-transform">
          <p>Texas Parks & Wildlife</p>
        </a>
        <a href="https://tpwd.texas.gov/" target="_blank" class="hover:scale-110 transition-transform">
          <p>NPS Sea Turtle Science and Recovery</p>
        </a>
        <a href="https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0173920" target="_blank" class="hover:scale-110 transition-transform">
          <p>PLOS One: Publication Defining Cold Stunning Threshold</p>
        </a>
        <a href="https://www.coastaldynamicslab.org/water-temperature-predictionse" target="_blank" class="hover:scale-110 transition-transform">
          <p>TAMUCC CBI Water Temperature Predictions Reports</p>
        </a>
      </div>
      <div class="flex flex-wrap justify-center items-center gap-8 lg:gap-16 mx-auto p-1 lg:p-4">
        <a href="https://www.conradblucherinstitute.org/" target="_blank" class="hover:scale-110 transition-transform">
          <img src="@/assets/images/CBI-Logo.png" alt="CBI Logo" class="max-w-[165px] lg:max-w-[250px] ">
        </a>
        <a href="https://github.com/conrad-blucher-institute/semaphore" target="_blank" class="hover:scale-110 transition-transform">
          <img src="@/assets/images/Semaphore-Logo.png" alt="Semaphore Logo" class="max-w-[80px] lg:max-w-[150px]">
        </a>
        <a href="https://www.usace.army.mil/" target="_blank" class="hover:scale-110 transition-transform">
          <img src="@/assets/images/USACE-Logo.jpg" alt="US Army Corps Logo" class="max-w-[80px] lg:max-w-[150px]">
        </a>
        <a href="https://www.nsf.gov/" target="_blank" class="hover:scale-110 transition-transform">
          <img src="@/assets/images/NSF-Logo.png" alt="National Science Foundation Logo" class="max-w-[80px] lg:max-w-[150px]">
        </a>
        <a href="https://www.gicaonline.com/" target="_blank" class="hover:scale-110 transition-transform">
          <img src="@/assets/images/GICA-Logo.png" alt="Gulf Intracoastal Canal Association Logo" class="max-w-[80px] lg:max-w-[150px]">
        </a>
        <a href="https://tpwd.texas.gov/" target="_blank" class="hover:scale-110 transition-transform">
          <img src="@/assets/images/TPWD-Logo.gif" alt="Texas Parks and Wildlife Logo" class="max-w-[80px] lg:max-w-[150px]">
        </a>
        <a href="https://www.coastaldynamicslab.org/" target="_blank" class="hover:scale-110 transition-transform">
          <img src="@/assets/images/CDL-Logo.png" alt="Coastal Dynamics Lab Logo" class="max-w-[80px] lg:max-w-[150px]">
        </a>
        <a href="https://www.nps.gov/index.htm" target="_blank">
          <img class="footer-logo" src="@/assets/images/NPS-Logo.png" alt="National Park Service Logo">
        </a>
        <a href="https://www.weather.gov/" target="_blank">
          <img src="@/assets/images/NWS-Logo.png" alt="National Weather Service Logo" class="max-w-[80px] lg:max-w-[150px]">
        </a>
        <a href="https://www.uscg.mil/" target="_blank">
          <img  src="@/assets/images/CG-Logo.png" alt="USA Coast Guard Logo" class="max-w-[80px] lg:max-w-[150px]">
        </a>
        <a href="https://www.joincca.org/" target="_blank">
          <img src="@/assets/images/CCA-Logo.png" alt="Coastal Conservation Association Logo" class="max-w-[80px] lg:max-w-[150px]">
        </a>
      </div>
      <p class="text-center text-sm text-light-text">(Click on the logos to visit each contributor's website)</p>
    </footer>
  </div>
</template>
