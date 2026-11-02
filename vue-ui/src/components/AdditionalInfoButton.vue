<!--
Additional Info Button

This file holds the additional info button, transition, and information cards
displayed at the bottom of the screen. The button is always visible.

Created By: CJ Quintero
Created On: 09/24/2026

Usage:
  Import this component into the parent page and pass two arrays:

	<AdditionalInfoButton
		:data-on-this-graph="dataOnThisGraph"
		:additional-info="additionalInfo"
	/>

Props:
	dataOnThisGraph - Items displayed under "Data on this Graph:".
	additionalInfo  - Items displayed under "Additional Information:".

Item fields (shared by dataOnThisGraph and additionalInfo):
	dataOnThisGraph items render as paragraphs; additionalInfo items render as a bulleted list.

	header (str) - the bold header portion of the item, optional for additionalInfo

	body (str) - the body text

	links (array[{ text, href, linkTarget }]) - an optional array of links
		text (str) - the visible text shown on the page

		href (str) - the URL the link points to
			for internal links, the path should start with '/' such as '/crps' so the router can handle it correctly.
			for external links, the full URL should be provided, such as 'https://lighthouse.tamucc.edu/pq'

		linkTarget (str) - the target attribute for the link (e.g., '_self', '_blank')
			_self - open the link in the same tab, should be used for navigating to another Flare page
			_blank - open the link in a new tab, should be used for navigating to external pages not on Flare

	bulletLinks (bool) - whether to display the links as bullet points
		true: display links as bullet points in a block beneath the body text
		false: display links inline after the text, only recommended for a single link

Examples:
	const dataOnThisGraph = [
		{
			header: 'Observed Water and Air Temperatures:',
			body: 'Hourly observations in Upper Laguna Madre are obtained from the',
			links: [
				{ text: 'South Bird Island TCOON station', href: 'https://lighthouse.tamucc.edu/pq?_ga=2.37560803.210879303.1694296771-1722476858'}
			],
			bulletLinks: false // inline link
		}
	];

	const additionalInfo = [
		{
			body: 'Wind speed measurements and predictions (NWS-NDFD) for South Bird Island found',
			links: [
				{ text: 'here', href: 'https://cbigrid.tamucc.edu/tpw/graph-only-wind.html', linkTarget: '_blank' } // open in a new tab
			],
		},
	];
-->
<script setup>
import { ref } from 'vue';

const showInfoDrawer = ref(false);

// determine the link target for an item
// defaults to _blank
const getLinkTarget = (item) =>
    item.linkTarget === '_self' ? '_self' : '_blank';

// internal Flare paths start with '/' and are handled by the router
const isInternalLink = (link) => link.href?.startsWith('/');

defineProps({
    dataOnThisGraph: {
        type: Array,
        default: () => [],
    },
    additionalInfo: {
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
                       <div class="space-y-4 text-base lg:text-xl text-dark-text">
                            <div v-for="(item, index) in dataOnThisGraph" :key="index">
                                <p>
																	<!-- optional header for the item is displayed in bold -->
																	<template v-if="item.header">
																		<strong>{{ item.header }}</strong>
																		{{ ' ' }}
																	</template>
                                	{{ item.body }}

                                    <!-- Inline links -->
                                    <template v-if="!item.bulletLinks">
                                        <template v-for="(link, linkIndex) in item.links ?? []" :key="linkIndex">
                                            {{ linkIndex === 0 ? ' ' : ', ' }}
                                            <router-link v-if="isInternalLink(link)" :to="link.href" :target="getLinkTarget(link)" rel="noopener noreferrer"
                                            class="underline text-blue-600 hover:text-blue-800">{{ link.text }}</router-link>
                                            <a v-else :href="link.href" :target="getLinkTarget(link)" rel="noopener noreferrer"
                                            class="underline text-blue-600 hover:text-blue-800">{{ link.text }}</a>
                                        </template>
                                    </template>
                                </p>

                                <!-- Bulleted links -->
                                <ul v-if="item.bulletLinks && item.links?.length" class="list-disc pl-8 mt-1 space-y-1">
                                    <li v-for="(link, linkIndex) in item.links" :key="linkIndex">

                                        <router-link v-if="isInternalLink(link)" :to="link.href" :target="getLinkTarget(link)" rel="noopener noreferrer"
                                        class="underline text-blue-600 hover:text-blue-800">{{ link.text }}</router-link>

                                        <a v-else :href="link.href" :target="getLinkTarget(link)" rel="noopener noreferrer"
                                        class="underline text-blue-600 hover:text-blue-800">{{ link.text }}</a>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div> <!-- End Left Card -->

                    <!-- Right Card -->
                    <div class="lg:col-span-1 bg-white p-6 rounded-lg shadow-md">
                        <h3 class="text-xl lg:text-2xl font-extrabold text-center lg:text-left text-dark-text border-b-2 border-gray-500 pb-2 mb-3 lg:pb-4 lg:mb-6">
                            Additional Information:
                        </h3>
                        <ul class="list-disc space-y-2 pl-5 text-base lg:text-xl text-dark-text">
                            <li v-for="(item, index) in additionalInfo" :key="index">
																<!-- optional header for the item is displayed in bold -->
                                <template v-if="item.header">
                                    <strong>{{ item.header }}</strong>
                                    {{ ' ' }}
                                </template>
                                {{ item.body }}

                                <!-- Inline links -->
                                <template v-if="!item.bulletLinks">
                                    <template v-for="(link, linkIndex) in item.links ?? []" :key="linkIndex">
                                        {{ linkIndex === 0 ? ' ' : ', ' }}
                                        <router-link v-if="isInternalLink(link)" :to="link.href" :target="getLinkTarget(link)" rel="noopener noreferrer"
                                        class="underline text-blue-600 hover:text-blue-800">{{ link.text }}</router-link>
                                        <a v-else :href="link.href" :target="getLinkTarget(link)" rel="noopener noreferrer"
                                        class="underline text-blue-600 hover:text-blue-800">{{ link.text }}</a>
                                    </template>
                                </template>

                                <!-- Bulleted links, nested under this bullet -->
                                <ul v-if="item.bulletLinks && item.links?.length" class="list-[circle] pl-6 mt-1 space-y-1">
                                    <li v-for="(link, linkIndex) in item.links" :key="linkIndex">
                                        <router-link v-if="isInternalLink(link)" :to="link.href" :target="getLinkTarget(link)" rel="noopener noreferrer"
                                        class="underline text-blue-600 hover:text-blue-800">{{ link.text }}</router-link>
                                        <a v-else :href="link.href" :target="getLinkTarget(link)" rel="noopener noreferrer"
                                        class="underline text-blue-600 hover:text-blue-800">{{ link.text }}</a>
                                    </li>
                                </ul>
                            </li>
                        </ul>
                    </div> <!-- End Right Card -->
                </div> <!-- End Card Grid -->
            </div>
        </transition>
    </div> <!-- End Additional Info Modal -->
</template>
