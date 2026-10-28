<!--
Additional Info Button

This file holds the additional info button, transition, and information cards
displayed at the bottom of the screen. The button is always visible.

Created By: CJ Quintero
Created On: 09/24/2026

Usage:
    Import this component into the parent page and pass two arrays:

    <AdditionalInfo
        :graph-items="graphItems"
        :additional-items="additionalItems"
    />

Props:
    graphItems      - Items displayed under "Data on this Graph:".
    additionalItems - Items displayed under "Additional Information:".
    Both default to empty arrays and use the same item format.

Item fields:
    text       - Plain text displayed before the optional link.
    parts      - Text segments used instead of text for bold formatting.
                 Each segment has text and an optional bold: true.
                 Include spaces between words in the segment strings.
    linkText   - Clickable text; required when providing a link.
    href       - External URL.
    to         - Internal Vue Router destination. Takes priority over href.
    linkTarget - Defaults to a new tab. Set to '_self' for the current tab.

Examples:
    const graphItems = [
        {
            text: 'Water temperature predictions are updated daily.',
        },
        {
            parts: [
                { text: 'Observed temperatures:', bold: true },
                { text: ' Hourly observations are available from the' },
            ],
            linkText: 'South Bird Island TCOON station',
            href: 'https://lighthouse.tamucc.edu/pq',
        },
    ];

    const additionalItems = [
        {
            linkText: 'Ensemble air temperature predictions',
            to: '/air-temperature-ensemble',
            linkTarget: '_self',
        },
    ];

Notes:
    - Card headers stay fixed inside the component.
    - Links appear after the text or parts.
    - If parts is provided, text is ignored.
    - Items without href or to display only their text.
    - Text is rendered literally; HTML strings are not interpreted.
-->
<script setup>
import { ref } from 'vue';

const showInfoDrawer = ref(false);
const getLinkTarget = (item) =>
    item.linkTarget === '_self' ? '_self' : '_blank';

defineProps({
    graphItems: {
        type: Array,
        default: () => [],
    },
    additionalItems: {
        type: Array,
        default: () => [],
    },
});
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
                            <li v-for="(item, index) in graphItems" :key="index">
                                <template v-if="item.parts">
                                    <template v-for="(part, partIndex) in item.parts" :key="partIndex">
                                        <strong v-if="part.bold">{{ part.text }}</strong>
                                        <span v-else>{{ part.text }}</span>
                                    </template>
                                </template>
                                <template v-else>{{ item.text }}</template>

                               <template v-if="item.to || item.href">
                                    {{ ' ' }}

                                    <router-link
                                        v-if="item.to"
                                        :to="item.to"
                                        custom
                                        v-slot="{ href }"
                                    >
                                        <a
                                            :href="href"
                                            :target="getLinkTarget(item)"
                                            rel="noopener noreferrer"
                                            class="underline text-blue-600 hover:text-blue-800"
                                        >
                                            {{ item.linkText }}
                                        </a>
                                    </router-link>

                                    <a
                                        v-else
                                        :href="item.href"
                                        :target="getLinkTarget(item)"
                                        rel="noopener noreferrer"
                                        class="underline text-blue-600 hover:text-blue-800"
                                    >
                                        {{ item.linkText }}
                                    </a>
                                </template>
                            </li>
                        </ul>
                    </div> <!-- End Left Card -->

                    <!-- Right Card -->
                    <div class="lg:col-span-1 bg-white p-6 rounded-lg shadow-md">
                        <h3 class="text-xl lg:text-2xl font-extrabold text-center lg:text-left text-dark-text border-b-2 border-gray-500 pb-2 mb-3 lg:pb-4 lg:mb-6">
                            Additional Information:
                        </h3>
                        <ul class="list-disc space-y-2 pl-5 text-md lg:text-xl text-dark-text">
                            <li v-for="(item, index) in additionalItems" :key="index">
                                <template v-if="item.parts">
                                    <template v-for="(part, partIndex) in item.parts" :key="partIndex">
                                        <strong v-if="part.bold">{{ part.text }}</strong>
                                        <span v-else>{{ part.text }}</span>
                                    </template>
                                </template>
                                <template v-else>{{ item.text }}</template>

                                <template v-if="item.to || item.href">
                                    {{ ' ' }}

                                    <router-link
                                        v-if="item.to"
                                        :to="item.to"
                                        custom
                                        v-slot="{ href }"
                                    >
                                        <a
                                            :href="href"
                                            :target="getLinkTarget(item)"
                                            rel="noopener noreferrer"
                                            class="underline text-blue-600 hover:text-blue-800"
                                        >
                                            {{ item.linkText }}
                                        </a>
                                    </router-link>

                                    <a
                                        v-else
                                        :href="item.href"
                                        :target="getLinkTarget(item)"
                                        rel="noopener noreferrer"
                                        class="underline text-blue-600 hover:text-blue-800"
                                    >
                                        {{ item.linkText }}
                                    </a>
                                </template>
                            </li>
                        </ul>
                    </div> <!-- End Right Card -->
                </div> <!-- End Card Grid -->
            </div>
        </transition>
    </div> <!-- End Additional Info Modal -->
</template>