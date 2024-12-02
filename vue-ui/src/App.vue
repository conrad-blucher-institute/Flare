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

    <header>
    
   <!-- DropDown Menu and header that appears on all pages -->
    <div class="dropdown-section">
      <img class="flare-logo" src="@/assets/images/Flare-Logo.png" alt="Flare Logo">

      <DropDownMenu/> 
    </div>
  </header>

  <!-- Displays page based on route-->
   <section class="router-section">
      <div>
        <RouterView/>
      </div>
   </section>

</template>

<style scoped>
  

/* Styles for screens wider than 768px (tablets and desktops) */
@media (min-width: 768px) {
  .page-container{
    overflow: hidden;
  }
    .dropdown-section{
    position: fixed; 
    top: 0;          /* Aligns it to the top of the viewport */
    left: 0;         /* Aligns it to the left of the viewport */
    width: 100%;     /* Full width across the screen */
    z-index: 1000;   /* Ensures it displays above other content */
    background-color: var(--navy-blue); 
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2); /* Adds a dropdown shadow */
    }

    /* Flare logo styling */
  .flare-logo {
    height: 90px; /* Adjust height as needed */
    margin-right: 20px; /* Adds spacing from the right edge of the header */
  }
}

  
/* Styles for screens narrower than 480px ( mobile phones) */
@media (max-width: 480px) {

  .dropdown-section {
    position: fixed; 
    top: 0;          /* Aligns it to the top of the viewport */
    left: 0;         
    width: 100%;     
    flex-direction: column; /* Stack items vertically */
    z-index: 1000;
    align-items: center;
    height: 70px;
    background-color: var(--navy-blue); 
  }

  .flare-logo {
    height: 60px; /* Reduce logo size */
    margin-bottom: 5px; /* Add spacing below the logo */
  }

  
  }

</style>
