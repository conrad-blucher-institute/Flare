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
  //TODO: Define shared styling variables for the Highcharts hamburger
  // menu to keep its appearance consistent across all charts and pages.
import { useMenuStore } from '@/stores/menuStore';
import { ref } from 'vue';

const menuStore = useMenuStore();

const isOpen = ref(false);
const activeSubmenu = ref(null);
const expandedSections = ref(['Laguna Madre']);

    // Toggle function to show or hide the dropdown
function toggleDropdown() {
  isOpen.value = !isOpen.value;

  if (!isOpen.value) {
    activeSubmenu.value = null;
  }
}

function toggleSubmenu(label) {
  activeSubmenu.value =
    activeSubmenu.value === label ? null : label;
}

function toggleSection(label) {
  if (expandedSections.value.includes(label)) {
    expandedSections.value =
      expandedSections.value.filter(item => item !== label);
  } else {
    expandedSections.value.push(label);
  }
}

function closeMenu() {
  isOpen.value = false;
  activeSubmenu.value = null;
}

function isExpanded(label) {
  return expandedSections.value.includes(label);
}
</script>

<template>
  <div class="relative inline-block float-right z-50">

    <!-- Hamburger Button -->
    <button
      @click="toggleDropdown"
      aria-label="Toggle navigation menu"
      :aria-expanded="isOpen"
      class="flex flex-col items-center justify-center
             p-2 bg-transparent border-none cursor-pointer"
    >
      <span class="block w-9 h-1 bg-white rounded mb-1.5"></span>
      <span class="block w-9 h-1 bg-white rounded mb-1.5"></span>
      <span class="block w-9 h-1 bg-white rounded"></span>
    </button>

    <!-- Main Dropdown -->
    <div
      v-if="isOpen"
      class="absolute right-0 mt-2 w-52
             bg-white rounded-xl shadow-xl
             border border-gray-200
             text-dark-text"
    >

      <!-- Quick Links Header -->
      <div
        class="px-4 py-2 rounded-t-xl
               bg-gradient-to-r
               from-[#B5E0E8] to-[#D3EDF0]
               text-lg font-bold"
      >
        Quick Links
      </div>

      <!-- Main Menu Options -->
      <template
        v-for="option in menuStore.dropDownMenuOptions"
        :key="option.label"
      >

        <!-- Expandable Menu -->
        <button
          v-if="option.children"
          @click="toggleSubmenu(option.label)"
          class="w-full flex items-center gap-3
                 px-4 py-3 text-left
                 border-b border-gray-200
                 hover:bg-[#D9EDF1]"
          :class="{
            'bg-[#D9EDF1]': activeSubmenu === option.label
          }"
        >
          <span class="text-xl font-bold text-[#006B83]">
            ‹
          </span>

          <span class="text-sm font-semibold">
            {{ option.label }}
          </span>
        </button>

        <!-- Normal Router Links -->
        <RouterLink
          v-else
          :to="option.link"
          @click="closeMenu"
          class="block px-5 py-3
                 text-base font-semibold
                 border-b border-gray-200
                 hover:bg-[#D9EDF1]
                 last:rounded-b-xl"
        >
          {{ option.label }}
        </RouterLink>

      </template>

      <!-- Left Submenu -->
      <div
        v-if="activeSubmenu"
        class="absolute
               top-20
               right-full
               mr-1
               w-72
               bg-white
               rounded-xl
               border-4 border-white
               shadow-xl
               overflow-hidden
               max-h-[80vh]
               overflow-y-auto

               max-sm:fixed
               max-sm:left-4
               max-sm:right-4
               max-sm:top-24
               max-sm:w-auto
               max-sm:mr-0"
      >

        <template
          v-for="section in
            menuStore.dropDownMenuOptions.find(
              option => option.label === activeSubmenu
            )?.children || []"
          :key="section.label"
        >

          <!-- Section Header -->
          <button
            @click="toggleSection(section.label)"
            class="w-full flex items-center gap-4
                   px-4 py-3
                   bg-gradient-to-r
                   from-[#B5E0E8] to-[#D3EDF0]
                   hover:from-[#A8D7E1]
                   hover:to-[#C5E5EA]
                   rounded-lg
                   text-left
                   font-bold
                   text-dark-text"
          >
            <span
              class="text-[#006B83] text-xl
                     transition-transform duration-200"
            >
              {{ isExpanded(section.label) ? '⌄' : '›' }}
            </span>

            <span>{{ section.label }}</span>
          </button>

          <!-- Expanded Section Content -->
          <div v-if="isExpanded(section.label)">

            <template
              v-for="item in section.children"
              :key="item.label"
            >

              <!-- Information Header -->
              <div
                v-if="item.isHeader"
                class="px-4 py-2
                       bg-[#E0EDF2]
                       font-bold
                       text-sm
                       border-b border-gray-200"
              >
                {{ item.label }}
              </div>

              <!-- Internal Links -->
              <RouterLink
                v-else-if="item.link"
                :to="item.link"
                @click="closeMenu"
                class="flex items-center justify-between
                       gap-3
                       px-5 py-3
                       text-sm font-medium
                       border-b border-gray-200
                       hover:bg-[#EAF5F7]"
              >
                <span>{{ item.label }}</span>

                <svg
                  class="w-4 h-4 shrink-0 text-[#006B83]"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M14 3h7v7m0-7-10 10"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                  <path
                    d="M21 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h6"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
              </RouterLink>

              <!-- External Links -->
              <a
                v-else-if="item.url"
                :href="item.url"
                target="_blank"
                rel="noopener noreferrer"
                class="flex items-center justify-between
                       gap-3
                       px-5 py-3
                       text-sm font-medium
                       border-b border-gray-200
                       hover:bg-[#EAF5F7]"

              
              >
              

                <span>{{ item.label }}</span>

                <svg
                  class="w-4 h-4 shrink-0 text-[#006B83]"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M14 3h7v7m0-7-10 10"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                  <path
                    d="M21 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h6"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
              </a>

              
              <div
                v-else
                class="px-5 py-3 text-sm font-medium
                      text-gray-500 bg-gray-50
                      border-b border-gray-200
                      cursor-not-allowed"
              >
                {{ item.label }}
              </div>


            </template>

          </div>

        </template>

      </div>

    </div>

  </div>
</template>
