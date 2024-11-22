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
  .dropdown {
    position: relative;
    display: inline-block;
    float: right; /* Align to the right */
    margin: 10px; /* Add some margin for spacing */
  }
  
  .dropbtn {
    background-color: transparent;
    border: none;
    cursor: pointer;
    padding: 10px; 
  }
  
  .bar {
    display: block;
    width: 25px; 
    height: 3px; /* Height of the hamburger bars */
    background-color: white; /* Color of the bars */
    margin: 4px auto; /* Spacing between the bars */
  }
  
  .dropdown-content {
    display: block;
    position: absolute;
    right: 0; /* Align dropdown to the right */
    background-color: white;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    z-index: 1;
    min-width: 160px;
  }
  
  .dropdown-content div {
    color: black;
    padding: 12px 16px;
    text-decoration: none;
    cursor: pointer;
  }
  
  .dropdown-content div:hover {
    background-color: #f1f1f1;
  }
  </style>
  