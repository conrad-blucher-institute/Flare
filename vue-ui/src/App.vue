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

     Author: Anointiyae Beasley
     Date: 11/04/2024
======================================================= -->
<script setup>import DropDownMenu from './components/DropDownMenu.vue';</script>

<template>

  <header>
   <!-- DropDown Menu and header that appears on all pages -->
    <div class="dropdown-section">
      <DropDownMenu/> 
    </div>
  </header>

  <!-- Displays page based on route-->
   <section>
      <div>
        <RouterView/>
      </div>
   </section>
  
</template>

<style scoped>
  .dropdown-section{
  position: fixed; 
  top: 0;          /* Aligns it to the top of the viewport */
  left: 0;         /* Aligns it to the left of the viewport */
  width: 100%;     /* Full width across the screen */
  z-index: 1000;   /* Ensures it displays above other content */
  background-color: #02172f; 
  }
</style>
