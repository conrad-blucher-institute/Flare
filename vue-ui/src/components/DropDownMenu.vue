<!-- ===================================================
     Component: DropdownMenu.vue
     Description: This component displays a dropdown menu with a "hamburger" icon button that toggles
                  the visibility of a list of options. Each option is linked to a route, allowing
                  navigation within the application.
                  
                  - Button with three bars (hamburger icon) toggles the dropdown menu.
                  - Dropdown content displays a list of options from the menuStore.
                  - Clicking an option navigates to the specified route using Vue Router.

     Props:
       - Options are pulled from `menuStore.dropDownMenuOptions` and displayed as links.

     Functions:
       - toggleDropdown: Toggles the visibility of the dropdown menu.

     Styles:
       - `.dropdown` positions the button and content.
       - `.dropbtn` styles the button, `.bar` creates the hamburger icon.
       - `.dropdown-content` displays options and styles them with hover effects.
       - '@Media' query adjusts styles for mobile screens.
     Author: Anointiyae Beasley
     Date: 11/04/2024
======================================================= -->

 <script setup>
    import { useMenuStore } from '@/stores/menuStore';
    import { ref } from 'vue';

    const menuStore = useMenuStore(); // Instance of useMenuStore
    const isOpen = ref(false); // State to track dropdown visibility

    // Toggle function to show or hide the dropdown
    function toggleDropdown() {
    isOpen.value = !isOpen.value;
}

  </script>

<template>
  <!-- The button that displays 3 bars-->
    <div class="dropdown">
      <button class="dropbtn" @click="toggleDropdown">
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
      </button>
      <!-- If the dropdown menu is open, show the different options passed from App.vue
         and when one is clicked, the selectOption function is triggered -->
      <div class="dropdown-content" v-if="isOpen">
        <div v-for="option in menuStore.dropDownMenuOptions" :key="option.link.name">
            <RouterLink :to="option.link">{{ option.label }}</RouterLink> <!-- Display each option -->
        </div>
      </div>
    </div>
  </template>
  
 
  
  <style scoped>

/* Hamburger Button */
.dropbtn {
  background-color: transparent;
  border: none;
  cursor: pointer;
  padding: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.bar {
  display: block;
  width: 30px; 
  height: 4px;
  background-color: var(--primary-text-dark-background); 
  margin: 4px 0;
  border-radius: 2px; /* Rounded corners*/
  transition: transform 0.3s ease, opacity 0.3s ease;
}


/* Dropdown Container */
.dropdown {
  position: relative;
  display: inline-block;
  float: right; /* Align to the right */
  margin: 10px;
  z-index: 10;
}


/* Dropdown Content */
.dropdown-content {
  position: absolute;
  right: 0;
  top: 100%; /* Position the dropdown below the button */
  background-color: var(--secondary-background);
  border-radius: 8px;
  overflow: hidden; 
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.06);
  z-index: 20;
  min-width: 200px; 
  animation: fadeIn 0.3s ease-out; /* Referencing the animation in main.css */
}

/* Dropdown Options */
.dropdown-content div {
  color: var(--primary-text-light-background);
  padding: 12px 16px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: background-color 0.2s ease, color 0.2s ease;  
}

.dropdown-content div:hover {
  background-color: var(--secondary-background); 
  color: var(--primary-text-light-background);
}


.dropdown-content a {
  text-decoration: none; /* Remove underline */
  color: inherit; /* Inherit the color from the parent */
}

.dropdown-content a:hover {
  color:var(--primary-text-light-background);
}
/* Media Query for Mobile Screens */
@media (max-width: 480px) {

  .dropbtn {
  position: fixed; /* Keeps the button in a fixed position on the screen */
  top: 5px; 
  right: 10px; /* Keeps it near the right edge */
  padding: 10px; 
  background-color: transparent;
  border: none;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 10000; /* Ensures the button is above other elements */
}
  .dropdown {
    float: none; 
    width: 50%; 
    height: 10px;
    text-align: center;
  }

  .dropdown-content {
    min-width: 10%;
    border-radius: 0.8; 
    position: fixed; 
    top: 50px; 
    right: 10px; /* Keeps it near the right edge */
    padding: 10px;
  }

  .dropdown-content div {
    font-size: 16px; 
    padding: 14px 20px; 
  }

  .bar {
    width: 25px; /* Slightly smaller hamburger icon for mobile */
    height: 3px;
  }
}



</style>

  