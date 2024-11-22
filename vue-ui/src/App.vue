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


   <footer class="footer">
  <div class="footer-container">
    <!-- Logo Block -->
    <div class="logo-block">
      <img class="logo semaphore-logo" src="@/assets/images/Semaphore-Logo.png" alt="Semaphore Logo">
      <img class="logo cbi-logo" src="@/assets/images/CBI+Logo+White.png" alt="Conrad Blutcher Institute Logo">
    </div>

    <!-- Links or Credits Block -->
    <div class="footer-info">
      <p>&copy; 2024 Flare. All rights reserved.</p>
    </div>
  </div>
</footer>

  
  
</template>

<style>
  .dropdown-section{
  position: fixed; 
  top: 0;          /* Aligns it to the top of the viewport */
  left: 0;         /* Aligns it to the left of the viewport */
  width: 100%;     /* Full width across the screen */
  z-index: 1000;   /* Ensures it displays above other content */
  background-color: var(--navy-blue); 
  }

  /* Flare logo styling */
.flare-logo {
  height: 90px; /* Adjust height as needed */
  margin-right: 20px; /* Adds spacing from the right edge of the header */
}

.footer {
  background-color: #02172f; /* Professional dark background */
  color: #f4f4f4; /* Light text color for contrast */
  padding: 20px 0; /* Vertical padding */
  text-align: center; /* Center-align content */
}

.footer-container {
  display: flex;
  flex-wrap: wrap; /* Allows wrapping for responsiveness */
  align-items: center; /* Vertically align items */
  justify-content: space-between; /* Space between logo block and info */
  max-width: 1200px; /* Limit width for a clean layout */
  margin: 0 auto; /* Center the container */
  padding: 0 20px; /* Add padding for smaller screens */
}

.logo-block {
  display: flex;
  align-items: center; /* Vertically align logos */
  gap: 20px; /* Space between logos */
}

.semaphore-logo {
  height: 70px; /* Consistent logo size */
  object-fit: contain; /* Maintain logo proportions */
}
.cbi-logo {
  height: 70px; /* Consistent logo size */
  object-fit: contain; /* Maintain logo proportions */
}
.footer-info {
  text-align: center; /* Center-align text for smaller screens */
  font-size: 0.9rem; /* Slightly smaller text for subtlety */
  line-height: 1.6; /* Improve readability */
}

.footer-info p {
  margin: 5px 0; /* Space between lines */
}

.footer-link {
  color: #4fc3f7; /* Highlight links with a subtle color */
  text-decoration: none; /* Remove underline for links */
}

.footer-link:hover {
  text-decoration: underline; /* Add underline on hover */
}


</style>
