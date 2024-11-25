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


   <footer class="footer">
  <div class="footer-container">
    <!-- Logo Block -->
    <div class="logo-block">
      <img class="semaphore-logo" src="@/assets/images/Semaphore-Logo.png" alt="Semaphore Logo">
      <img class="cbi-logo" src="@/assets/images/CBI+Logo+White.png" alt="Conrad Blutcher Institute Logo">
    </div>

    <!-- Links or Credits Block -->
    <div class="footer-info">
      <p>&copy; 2024 Flare. All rights reserved.</p>
    </div>
  </div>
</footer>

  
  
</template>

<style scoped>
  

/* Styles for screens wider than 768px (tablets and desktops) */
@media (min-width: 768px) {
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

  .footer {
    background-color: var(--navy-blue); 
    color: var(--primary-text-dark-background); 
    padding: 20px 0; /* Vertical padding */
    text-align: center; 
  }

  .footer-container {
    display: flex;
    flex-wrap: wrap; 
    align-items: center; 
    justify-content: space-between; 
    max-width: 1200px; 
    margin: 0 auto; 
    padding: 0 20px; 
  }

  .logo-block {
    display: flex;
    align-items: center; /* Vertically align logos */
    gap: 20px; 
  }

  .semaphore-logo {
    height: 70px; 
    object-fit: contain;
  }
  .cbi-logo {
    height: 70px; 
    object-fit: contain; 
  }
  .footer-info {
    text-align: center; 
    font-size: 0.9rem; 
    line-height: 1.6; 
  }

  .footer-info p {
    margin: 5px 0; 
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

  .footer {
    padding: 15px 10px; 
    background-color: var(--navy-blue); 
  }

  .footer-container {
    flex-direction: column; /* Stack footer content */
    text-align: center;
    gap: 10px; /* Add spacing between sections */
    
  }
  .logo-block{
    align-items: center;
  }

  .semaphore-logo{
    height: 90px;
  }
  .cbi-logo{
    height: 70px;
  }
  .footer-info {
    font-size: 0.8rem; /* Slightly smaller font size */
    margin-top: 10px; /* Add spacing above footer text */
    color: var(--primary-text-dark-background);
  }
  
    
  }


</style>
