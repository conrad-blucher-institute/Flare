<!-- ===================================================
     Component: SlidingMenu.vue
     Description: This component creates a horizontally scrollable menu with left and right arrow buttons.
                  The menu displays a list of options retrieved from `menuStore.slidingMenuOptions`, 
                  each with an image, location, and message.

                  - Left and right arrows allow smooth horizontal scrolling.
                  - Each option displays an image, a location heading, and a message.
                  - Clicking an option's image or link navigates to a specified route.

     Functions:
       - scrollLeft: Scrolls the menu left by 250px.
       - scrollRight: Scrolls the menu right by 250px.

     Styles:
       - `.sliding-menu-container` wraps the entire menu and arrows.
       - `.sliding-menu` enables horizontal scrolling for the list of options.
       - `.arrow`, `.menu-image`, and other styles can be customized for layout and appearance.
       - '@Media' query adjusts styles for mobile screens.
     Author: Anointiyae Beasley
     Date: 11/04/2024
======================================================= -->

<script setup>
import { useMenuStore } from '@/stores/menuStore';
import { ref } from 'vue';

const menuStore = useMenuStore(); // Instance of useMenuStore
const menuContainer = ref(null); //reference to the menu container

function scrollLeft() {
  if (menuContainer.value) {
    menuContainer.value.scrollBy({ left: -250, behavior: 'smooth' });
  }
}

function scrollRight() {
  if (menuContainer.value) {
    menuContainer.value.scrollBy({ left: 250, behavior: 'smooth' });
  }
}


</script>

<template>
  <div class="relative flex items-center w-full">
    <!-- Left Arrow -->
    <button
      v-if="menuStore.slidingMenuOptions.length > 1"
      @click="scrollLeft"
      class="absolute left-2 top-1/2 transform -translate-y-1/2 text-3xl text-blue-500 hover:text-blue-700 focus:outline-none z-10"
    >
      &laquo;
    </button>

    <!-- Sliding Menu -->
    <div
      class="flex gap-6 overflow-x-auto scroll-smooth w-full py-4 items-center justify-center"
      ref="menuContainer"
    >
      <ul class="flex gap-6">
        <li
          v-for="option in menuStore.slidingMenuOptions"
          :key="option.link.name"
          class="flex flex-col items-center text-center min-w-[300px]"
        >
          <RouterLink :to="option.link">
            <img
              :src="option.image"
              :alt="option.label"
              class="lg:min-w-[300px] lg:min-h-[300px] rounded-full object-cover transition-transform duration-300 hover:scale-105"
            />
          </RouterLink>
          <h1 class="mt-4 text-lg lg:text-2xl font-semibold text-dark-text">
            {{ option.location }}
          </h1>
          <p class="mt-2 text-sm lg:text-xl text-gray-600">{{ option.message }}</p>
        </li>
      </ul>
    </div>


    <!-- Right Arrow -->
    <button
      v-if="menuStore.slidingMenuOptions.length > 1"
      @click="scrollRight"
      class="absolute right-2 top-1/2 transform -translate-y-1/2 text-3xl text-blue-500 hover:text-blue-700 focus:outline-none z-10"
    >
      &raquo;
    </button>
  </div>
</template>
