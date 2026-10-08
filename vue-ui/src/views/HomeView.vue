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
  const menuOpen = ref(false)
  const inundationOpen = ref(false)
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
      <div class="relative flex justify-center mt-8">
        <!-- Inner Dropdown Menu Wrapper -->
        <div class="relative">
          <button
            class="bg-navy-blue border border-white/20 text-white font-semibold text-xl px-6 py-2 rounded-md"
            :aria-expanded="menuOpen"
            @click="menuOpen = !menuOpen; inundationOpen = false"
          >
            Additional CDL Products ▾
          </button>

          <!-- Main menu -->
          <div
            v-if="menuOpen"
            class="absolute left-0 top-full mt-2 w-72 bg-navy-blue text-white border border-white/20 rounded-md shadow-lg z-50 p-2 space-y-2"
          >
          
            <!-- Menu Contents -->
            <div class="relative">
              <button
                class="flex items-center justify-between gap-2 w-full border border-white/20 px-4 py-3 text-left rounded-md transition-colors hover:bg-white/10 hover:border-white/40"
                :aria-expanded="inundationOpen"
                @click="inundationOpen = !inundationOpen"
              >
                <span>Inundation Prediction Models</span>
                <span aria-hidden="true">▸</span>
              </button>

              <!-- Inundation Submenu -->
              <div
                v-if="inundationOpen"
                class="absolute left-full top-0 ml-2 w-56 bg-navy-blue border border-white/20 rounded-md shadow-lg p-2 space-y-2"
              >
                <a
                  href="https://sherlock-prod.tamucc.edu/cbocp/"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="block border border-white/20 px-4 py-3 text-center rounded-md transition-colors hover:bg-white/10 hover:border-white/40"
                >
                  <span class="block font-semibold">Production</span>
                  <span class="block mt-1 text-xs text-white/70">
                    Public access
                  </span>
                </a>

                <a
                  href="https://sherlock-dev.tamucc.edu/cbocp/"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="block border border-white/20 px-4 py-3 text-center rounded-md transition-colors hover:bg-white/10 hover:border-white/40"
                >
                  <span class="block font-semibold">In Development</span>
                  <span class="block mt-1 text-xs text-white/70">
                    TAMU-CC VPN required
                  </span>
                </a>
              </div><!-- Inundation Submenu End -->
            </div> <!-- Menu Contents End -->

            <a
              href="https://cbigrid.tamucc.edu/fog-predictions/"
              target="_blank"
              rel="noopener noreferrer"
              class="block border border-white/20 px-4 py-3 rounded-md transition-colors hover:bg-white/10 hover:border-white/40"
            >
              Fog Prediction Models
            </a>
          </div> <!-- Main Menu End -->
        </div> <!-- Inner Dropdown Menu Wrapper End -->
      </div> <!-- Dropdown menu End -->
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
