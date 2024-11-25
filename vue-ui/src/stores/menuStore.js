// ===================================================
// File: menuStore.js
// Description: This Pinia store manages menu options for the dropdown menu 
//              and sliding menu in the application. The store provides:
//                - `dropDownMenuOptions`: Options for a dropdown menu, with labels and routes.
//                - `slidingMenuOptions`: Options for a sliding menu, including labels, routes, 
//                   images, locations, and messages related to environmental predictions.
//
// Dependencies:
//   - Pinia for state management (`defineStore`).
//   - TurtleImage: A sample image imported from assets.
//
// Author: Anointiyae Beasley
// Date: 11/05/2024
// ===================================================
import { defineStore } from 'pinia';
import TurtleImage from '@/assets/images/Turtle.png';

export const useMenuStore = defineStore('menu', {
  state: () => ({
    dropDownMenuOptions: [
      { label: 'Home', link: { name: 'home' }}
    ],
    slidingMenuOptions: [
      { label: 'South Bird Island Chart', link: { name: 'southBirdIslandChart' }, image: TurtleImage, location: 'South Bird Island, Texas', message: '120 hour predictions of water and air temperature'}
    ]
  })
});
