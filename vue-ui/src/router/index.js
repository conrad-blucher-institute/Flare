// ===================================================
// File: router/index.js
// Description: Configures the Vue Router for managing client-side navigation
//              within the application. Defines the application's routes,
//              including path, name, and component for each route.
//
//              - Imports `createRouter` and `createWebHistory` from Vue Router
//                to set up the router with HTML5 history mode.
//              - Defines routes for the "Home" and "Test Chart" views.
//              - Implements lazy loading for the "Test Chart" view, optimizing
//                the app by loading this route only when it’s accessed.
//
// Routes:
//   - Home ('/'): Loads `HomeView.vue`.
//   - Test Chart ('/test-chart'): Loads `TestChartView.vue` on demand.
//
// Author: Anointiyae Beasley
// Date: 11/04/2024
// ===================================================
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/south-bird-island',
      name: 'southBirdIsland',

      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => {
        // Check the screen size and load the appropriate component
        if (window.innerWidth <= 930) {
          return import('../views/MobileSouthBirdIslandChartView.vue');
        } else {
          return import('../views/DesktopSouthBirdIslandChartView.vue');
        }
      },
    }
  ],
})

export default router
