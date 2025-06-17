<!-- ===================================================
     File: App.vue
     Description: Root component for the Vue application. 
                  This component serves as the main layout for the app, 
                  containing the header with a dropdown menu that appears on 
                  all pages and a section for displaying route-based views.
                  
                  - <header>: Contains the dropdown menu, which remains fixed 
                    at the top of the viewport.
                  - <section>: Holds the <RouterView> component, which dynamically
                    loads the appropriate component based on the current route.
                  
     Components:
       - DropDownMenu: The dropdown menu component that appears on all pages.
       - RouterView: Vue Router component that renders the active route's view.

     Styles:
      - `.dropdown-section`: Styles the fixed dropdown menu header with a background color
         and shadow for separation, ensuring it stays above other content.
      - '@Media' query adjusts styles for mobile screens.
     Author: Anointiyae Beasley
     Date: 11/04/2024
======================================================= -->
<script setup>import DropDownMenu from './components/DropDownMenu.vue';</script>

<template>
  <!-- Header Section -->
  <header class="fixed top-0 left-0 w-full bg-navy-blue shadow-lg z-50 flex items-center justify-between px-4 py-3 sm:px-8 sm:py-4">
    <!-- Logo -->
    <img 
      class="h-12 sm:h-16 transition-all duration-300 ease-in-out" 
      src="@/assets/images/Flare-Logo.png" 
      alt="Flare Logo"
    />
    
    <!-- Dropdown Menu -->
    <DropDownMenu />
  </header>

  <!-- Main Content Section -->
  <main class="pt-16 sm:pt-20">
    <RouterView />
  </main>
</template>



