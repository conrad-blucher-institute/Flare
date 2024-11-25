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
  <div class="sliding-menu-container">
    <!-- Left Arrow -->
    <button v-if="menuStore.slidingMenuOptions.length > 1" @click="scrollLeft" class="arrow left-arrow">&laquo;</button>
    
    <!-- Sliding Menu -->
    <div class="sliding-menu" ref="menuContainer">
      <ul>
        <li v-for="option in menuStore.slidingMenuOptions" :key="option.link.name">
          <RouterLink :to="option.link">
            <img :src="option.image" :alt="option.label" class="menu-image" />
          </RouterLink>
          <h1>{{ option.location }}</h1>
          <p>{{ option.message }}</p>
        </li>
      </ul>
    </div>

    <!-- Right Arrow -->
    <button v-if="menuStore.slidingMenuOptions.length > 1" @click="scrollRight" class="arrow right-arrow">&raquo;</button>
  </div>
</template>


<style scoped>
.sliding-menu {
  display: flex;
  justify-content: center; /* Center single item */
  gap: 20px;
  overflow-x: hidden; /* Remove scroll since we only have one item*/
  padding: 40px 0;
  width: 100%;
}

.arrow {
  background: none;
  border: none;
  color: #5c779d; 
  font-size: 30px;
  cursor: pointer;
  padding: 5px;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 2;
  transition: color 0.3s ease;
}

.arrow:hover {
  color: #3b5a7d; 
}

.left-arrow {
  left: 10px;
  padding: 10px;
}

.right-arrow {
  right: 15px;
  padding: 20px;
}

.sliding-menu {
  display: flex;
  gap: 20px;
  overflow-x: auto;
  scroll-behavior: smooth;
  width: 100%;
}

.sliding-menu::-webkit-scrollbar {
  display: none; /* Hide scrollbar */
}

.sliding-menu ul {
  display: flex;
  gap: 20px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.sliding-menu li {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  min-width: 250px; /* Set consistent width */
  color:var(--primary-text-light-background);
}

.menu-image {
  width: 300px;
  height: auto;
  border-radius: 50%;
  padding: 10px;
  object-fit: contain;
  transition: transform 0.3s ease; 
}

.menu-image:hover {
  transform: scale(1.05); /* Slightly enlarge on hover */
}

h1 {
  font-size: 1.5rem;
  margin: 10px 0 5px;
  color:var(--primary-text-light-background);
  font-weight: 600;
}

p {
  font-size: 1.3rem;
  color: var(--blue-secondary-text);
  margin: 0;
}
@media (max-width: 480px) {
  .sliding-menu {
    flex-direction: column; /* Stack items vertically */
    gap: 15px; 
    padding: 20px 0; 
    overflow-x: hidden; /* Prevent horizontal scrolling */
  }

  .arrow {
    font-size: 20px; 
    padding: 5px;
    top: auto; 
    position: static; 
  }

  .left-arrow,
  .right-arrow {
    display: none; /* Hide arrows */
  }

  .sliding-menu ul {
    flex-direction: column; 
    gap: 15px; /* Reduce spacing between items */
    margin: 0 auto; /* Center the menu */
    width: 100%; 
  }

  .sliding-menu li {
    min-width: auto; /* Allow list items to adjust based on content */
    width: 90%;
    margin: 0 auto; 
  }

  .menu-image {
    width: 150px;
    height: auto; 
    margin: 0 auto; 
    animation: vibrate 0.6s ease-in 0.35s;
  }

  h1 {
    font-size: 1.2rem; 
    margin: 5px 0; 
  }

  p {
    font-size: 1rem; 
    text-align: center; 
  }
}

</style>



