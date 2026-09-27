<!--
Additional Info Button

This file holds the additional info button, transition, and information cards
displayed at the bottom of the screen. The button is always visible.

Created By: CJ Quintero
Created On: 09/24/2026
-->
<script setup>
import { ref } from 'vue';

const showInfoDrawer = ref(false);
</script>

<template>
    <div class="fixed inset-x-0 bottom-0 z-50">
        <!-- Always-visible Handle -->
        <button
            @click="showInfoDrawer = !showInfoDrawer"
            class="w-[calc(100%-2rem)] mx-4 rounded-lg bg-[#1895a3] text-white border-4 border-black shadow-xl py-3"
        >
            <div class="w-12 h-1 bg-gray-300 rounded-full mx-auto mb-2"></div>
            <div class="font-semibold text-xl">
                {{ showInfoDrawer ? "Hide Additional Information ▼" : "Additional Information ▲" }}
            </div>
        </button>

        <transition
            enter-active-class="transition-transform duration-300 ease-out"
            leave-active-class="transition-transform duration-300 ease-in"
            enter-from-class="translate-y-full"
            enter-to-class="translate-y-0"
            leave-from-class="translate-y-0"
            leave-to-class="translate-y-full"
        >
            <div
                v-if="showInfoDrawer"
                class="bg-blue-50
                    max-h-[75vh]
                    overflow-y-auto
                    shadow-2xl
                    p-5"
            >
                <!-- Card Grid -->
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <!-- Left Card -->
                    <div class="lg:col-span-1 bg-white p-6 rounded-lg shadow-md">
                        <h3 class="text-xl lg:text-2xl font-extrabold text-center lg:text-left text-dark-text border-b-2 border-gray-500 pb-2 mb-3 lg:pb-4 lg:mb-6">
                            Data on this Graph:
                        </h3>
                        <ul class="list-disc list-inside space-y-2 text-md lg:text-xl text-dark-text">
                            <li>
                                Past six-day air/water temperature from
                                <a href="https://tidesandcurrents.noaa.gov/stationhome.html?id=8776139" 
                                    class="underline text-blue-600 hover:text-blue-800" target="_blank">NOAA's South Bird Island Station</a>
                            </li>
                            <li>
                                Backup water temperature data from
                                <a href="https://lighthouse.tamucc.edu/overview/171" 
                                    class="underline text-blue-600 hover:text-blue-800" target="_blank">National Park Service</a>
                            </li>
                            <li>Air temperature predictions from the National Digital Forecast Database (points)</li>
                            <li>Cubic interpolation of predicted air temperature (dashed line)</li>
                            <li>Water temperature predictions from Semaphore (dashed line)</li>
                        </ul>
                    </div> <!-- End Left Card -->

                    <!-- Right Card -->
                    <div class="lg:col-span-1 bg-white p-6 rounded-lg shadow-md">
                        <h3 class="text-xl lg:text-2xl font-extrabold text-center lg:text-left text-dark-text border-b-2 border-gray-500 pb-2 mb-3 lg:pb-4 lg:mb-6">
                            Additional Information:
                        </h3>
                        <ul class="list-disc space-y-2 pl-5 text-md lg:text-xl text-dark-text">
                            <li>
                                Wind speed graph available 
                                <a href="https://cbigrid.tamucc.edu/tpw/graph-only-wind.html" target="_blank" class="underline text-blue-600 hover:text-blue-800">here</a>
                            </li>
                            <li>
                                Ensemble air temperature predictions from The Weather Company available 
                                <router-link 
                                    to="/air-temperature-ensemble" 
                                    class="underline text-blue-600 hover:text-blue-800"
                                >
                                    here
                                </router-link>
                            </li>
                            <li>
                                Ensemble water temperature predictions from Semaphore available 
                                <router-link 
                                    to="/water-temperature-ensemble" 
                                    class="underline text-blue-600 hover:text-blue-800"
                                >
                                    here
                                </router-link>
                            </li>
                            <li>
                                CRPS (Continuous Ranked Probability Score) ensemble model from Semaphore available
                                <router-link 
                                    to="/crps" 
                                    class="underline text-blue-600 hover:text-blue-800"
                                >
                                    here
                                </router-link>
                            </li>
                            <li>
                                Wind predictions for the Laguna Madre available
                                <a href="https://cbigrid.tamucc.edu/tpw/graph-only-wind.html" target="_blank" class="underline text-blue-600 hover:text-blue-800">
                                    here
                                </a>
                            </li>
                            <li>
                                Ensemble air temperature predictions for Bird Island Basin available 
                                <a href="https://cbigrid.tamucc.edu/tpw/graph-only-wind.html" target="_blank" class="underline text-blue-600 hover:text-blue-800">
                                    here
                                </a>
                            </li>
                            <li>
                                AI water temperature prediction models performance available
                                <a href="https://lighthouse.tamucc.edu/supertool.php?stnid=013&elev=mwl&mode=nnwtp" target="_blank" class="underline text-blue-600 hover:text-blue-800">
                                    here
                                </a>
                            </li>
                            <li>
                                NOAA Sea Turtle Stranding and Salvage Network water temperature measurements
                                <a href="https://connect.fisheries.noaa.gov/content/c0773132-9590-4e21-bb42-676e2140fbaa/" target="_blank" class="underline text-blue-600 hover:text-blue-800">
                                    here
                                </a>
                            </li>
                        </ul>
                    </div> <!-- End Right Card -->
                </div> <!-- End Card Grid -->
            </div>
        </transition>
    </div> <!-- End Additional Info Modal -->
</template>
