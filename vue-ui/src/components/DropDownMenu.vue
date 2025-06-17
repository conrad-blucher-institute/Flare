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
  <div class="relative inline-block float-right z-10">
    <!-- Hamburger Button -->
    <button
      @click="toggleDropdown"
      class="flex flex-col items-center justify-center p-2 bg-transparent border-none cursor-pointer"
    >
      <!-- Hamburger Bars -->
      <span class="block w-8 h-1 bg-white rounded mb-1 transition-transform duration-300"></span>
      <span class="block w-8 h-1 bg-white rounded mb-1 transition-transform duration-300"></span>
      <span class="block w-8 h-1 bg-white rounded transition-transform duration-300"></span>
    </button>

    <!-- Dropdown Content -->
    <div
      v-if="isOpen"
      class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg z-20"
    >
      <div
        v-for="option in menuStore.dropDownMenuOptions"
        :key="option.link.name"
        class="px-4 py-2 text-sm font-medium text-gray-800 hover:bg-gray-100 cursor-pointer"
      >
        <RouterLink :to="option.link" class="block text-inherit no-underline">
          {{ option.label }}
        </RouterLink>
      </div>
    </div>
  </div>
</template>



