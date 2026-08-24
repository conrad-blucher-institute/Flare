<!-- ===================================================
     View: HomeView.vue
     Description: This view serves as the main page for the Flare application. It includes:
                  - A Banner section with the application title and description.
                  - A Sliding Menu component for navigation between sections.
                  - A Section Divider for visual separation.
                  - An About Section detailing the purpose and goals of Flare.
                  - A Team Section introducing the team members with their roles.
     Author: Anointiyae Beasley
     Date: 11/04/2024
======================================================= -->
<script setup>
  import { ref } from 'vue';
  import SlidingMenu from '@/components/SlidingMenu.vue';
  import { useMenuStore } from '@/stores/menuStore'; 

  const menuStore = useMenuStore(); // Instance of useMenuStore
  const showDropdown = ref(false); // State to track dropdown visibility
</script>

<template>
  <div class="overflow-hidden">
    <!-- Banner Section -->
    <section class="relative flex flex-col items-center justify-center h-[200px] lg:h-[400px] bg-banner-gradient">
      <!-- Overlay Image -->
      <div class="absolute inset-y-0 left-0 w-full opacity-20">
        <img src="@/assets/images/StatisticsOverlay.png" alt="Statistics Overlay" class="w-full h-full object-cover">
      </div>
      <!-- Text Content -->
      <div class="relative text-center">
        <h1 class="text-4xl font-bold text-white leading-tight lg:text-8xl">Flare</h1>
        <h2 class="mt-4 text-md font-medium text-gray-200 lg:text-2xl">Showcasing the visualization of AI models operationalized by Semaphore</h2>
      </div>
      <!-- Dropdown menu -->
      <div class="relative text-center mt-8">
        <button
          @click="showDropdown = !showDropdown"
          class="bg-navy-blue hover:bg-opacity-80 text-white font-semibold text-xl px-6 py-2 rounded-md mb-4 transition-colors"
        >
          {{ showDropdown ? "Hide Additional CDL Resources ▲" : "Additional CDL Resources ▼" }}
        </button>

        <!-- Dropdown menu contents -->
        <ul
          v-if="showDropdown"
          class="absolute left-1/2 -translate-x-1/2 mt-2 w-96 bg-white text-navy-blue text-left rounded-md shadow-lg py-4 px-6 list-disc list-inside z-10"
        >
          <li class="py-2 text-lg">
            <a
              href="https://www.coastaldynamicslab.org/"
              target="_blank"
              rel="noopener noreferrer"
              class="text-blue-800 hover:text-blue-400 underline"
            >Coastal Dynamics Lab (CDL) Homepage</a>
          </li>
          <li class="py-2 text-lg">Inundation Prediction Models coming soon</li>
          <li class="py-2 text-lg">Fog Prediction Models coming soon</li>
        </ul>
      </div>
    </section>

    <!-- Sliding Menu Section -->
    <section class="flex items-center justify-center lg:min-h-[500px] lg:h-[800px]">
      <SlidingMenu :options="menuStore.slidingMenuOptions" />
    </section>

    <!-- Section Divider -->
    <div class="h-[40px] bg-section-gradient"></div>


    <!-- Footer -->
    <footer class="bg-navy-blue py-6 text-center h-[200px] lg:h-[300px]">
      <div class="flex justify-center gap-2 lg:gap-10">
        <img src="@/assets/images/Semaphore-Logo.png" alt="Semaphore Logo" class="w-[100px] lg:w-[200px] lg:h-[200px]">
        <img src="@/assets/images/CBI-Logo.png" alt="Conrad Blutcher Institute Logo" class="w-[230px] h-[75px] pt-5 lg:pt-10 lg:w-[550px] lg:h-[150px]">
         <img src="@/assets/images/CDL-Logo.png" alt="Coastal Dynamics Lab Logo" class=" lg:pt-3 lg:w-[190px] lg:h-[200px]">
      </div>
      <p class="mt-4 text-sm text-gray-300">
        &copy; 2024 Flare. Powered by
        <a
          href="https://www.coastaldynamicslab.org/livepredictions"
          target="_blank"
          rel="noopener noreferrer"
          class="text-blue-400 hover:text-blue-300 underline"
        >
          CDL
        </a>.
        All rights reserved.
      </p>
    </footer>
  </div>
</template>
