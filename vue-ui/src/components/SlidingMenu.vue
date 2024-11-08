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
  <div class="sliding-menu-container">
    <!-- Left Arrow -->
    <button @click="scrollLeft" class="arrow left-arrow">&laquo;</button>
    
    <!-- Sliding Menu -->
    <div class="sliding-menu" ref="menuContainer">
      <ul>
        <li v-for="option in menuStore.slidingMenuOptions" :key="option.link.name">
          <RouterLink :to="option.link">
            <img :src="option.image" :alt="option.label" class="menu-image" />
          </RouterLink>
          <h1>{{ option.location }}</h1>
          <p>{{option.message}}</p>
        </li>
      </ul>
    </div>

    <!-- Right Arrow -->
    <button @click="scrollRight" class="arrow right-arrow">&raquo;</button>
  </div>
</template>

