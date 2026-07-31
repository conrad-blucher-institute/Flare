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
import { useMenuStore } from '@/stores/menuStore'
import { ref } from 'vue'

const menuStore = useMenuStore()

const menuContainer = ref(null)
const childContainers = ref({})

const selectedOption = ref(null)

function selectOption(option) {
  if (selectedOption.value === option) {
    selectedOption.value = null
  } else {
    selectedOption.value = option
  }
}

function scrollLeft() {
  menuContainer.value?.scrollBy({
    left: -350,
    behavior: 'smooth'
  })
}

function scrollRight() {
  menuContainer.value?.scrollBy({
    left: 350,
    behavior: 'smooth'
  })
}

function setChildContainer(el, key) {
  if (el) {
    childContainers.value[key] = el
  }
}

function childLeft(key) {
  childContainers.value[key]?.scrollBy({
    left: -220,
    behavior: 'smooth'
  })
}

function childRight(key) {
  childContainers.value[key]?.scrollBy({
    left: 220,
    behavior: 'smooth'
  })
}
</script>

<template>
  <div class="relative flex items-center w-full">

    <!-- Left Arrow -->
    <button
      v-if="menuStore.slidingMenuOptions.length > 1"
      @click="scrollLeft"
      class="absolute left-2 top-1/2 -translate-y-1/2 text-4xl text-blue-600 hover:text-blue-800 z-20"
    >
      &laquo;
    </button>

    <!-- Main Slider -->
    <div
      ref="menuContainer"
      class="flex w-full justify-center py-6"
    >
      <ul class="flex gap-10">

        <li
          v-for="option in menuStore.slidingMenuOptions"
          :key="option.location"
          class="flex flex-col items-center text-center min-w-[320px]"
        >

          <!-- Main Button -->
          <button
            @click="selectOption(option)"
            class="focus:outline-none"
          >
            <img
              :src="option.image"
              :alt="option.label"
              class="w-[200px] h-[200px] lg:w-[400px] lg:h-[400px] rounded-full object-cover transition-transform duration-300 hover:scale-105 cursor-pointer"
            >
          </button>

          <h2 class="mt-4 text-xl lg:text-4xl font-semibold text-dark-text">
            {{ option.location }}
          </h2>

          <p class="text-md lg:text-3xl text-gray-600 pt-2">
            {{ option.message }}
          </p>

          <div class=" scale-75 lg:origin-top lg:scale-[1.5] "> 
              <!-- Mini Menu -->
          <Transition name="fade">

            <div
              v-if="selectedOption === option && option.children?.length"
              class="mt-2 flex justify-center w-full"
            >

              <div class="flex items-center">

                <!-- Left Arrow -->
                <button
                  v-if="option.children.length > 3"
                  @click="childLeft(option.location)"
                  class="text-3xl text-dark-text hover:text-blue-800 px-2"
                >
                  &laquo;
                </button>

               <!-- Child Slider -->
              <div
                  :ref="el => setChildContainer(el, option.location)"
                  :class="[
                    'py-3 px-2 no-scrollbar',
                    option.children.length <= 3
                      ? 'flex justify-center gap-5'
                      : 'flex gap-3 py-1 px-1 overflow-x-auto  scroll-smooth w-[540px]  no-scrollbar'
                  ]"
                >
                <RouterLink
                  v-for="child in option.children"
                  :key="child.label"
                  :to="child.link"
                  class="
                    flex-none
                    w-[168px] 
                    text-center
                    px-4
                    py-2
                    rounded-full
                    border-2
                    border-dark-text
                    ring-2
                    ring-dark-text
                    ring-offset-2
                    bg-white
                    hover:bg-blue-100
                    hover:ring-blue-700
                    transition
                  "
                >
                  {{ child.label }}
                </RouterLink>
              </div>

                <!-- Right Arrow -->
                <button
                  v-if="option.children.length > 3"
                  @click="childRight(option.location)"
                  class="text-3xl text-dark-text hover:text-blue-800 px-2"
                >
                  &raquo;
                </button>

              </div>

            </div>

          </Transition>
          </div>
       
        </li>

      </ul>
    </div>

    <!-- Right Arrow -->
    <button
      v-if="menuStore.slidingMenuOptions.length > 1"
      @click="scrollRight"
      class="absolute right-2 top-1/2 -translate-y-1/2 text-4xl text-dark-text hover:text-blue-800 z-20"
    >
      &raquo;
    </button>

  </div>
</template>

<style scoped>
.no-scrollbar::-webkit-scrollbar {
  display: none;
}

.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.fade-enter-active,
.fade-leave-active {
  transition: all 0.25s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-12px);
}
</style>