// ===================================================
// File: main.js
// Description: The entry point for the Vue application, responsible for
//              initializing the app, setting up global plugins, and mounting
//              the root component.
//              
//              - Imports global CSS styles for the app.
//              - Creates the Vue application instance using `createApp`.
//              - Sets up Pinia for state management and registers Vue Router 
//                for client-side routing.
//              - Mounts the App component to the #app element in the HTML.
//
// Modules Used:
//   - Vue: Provides the framework for creating reactive applications.
//   - Pinia: State management library for managing global state.
//   - Router: Manages client-side navigation within the app.
//   - HighchartsVue: Displays advanced charts
//
// Author: Anointiyae Beasley
// Date: 11/04/2024
// ===================================================
import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'


import App from './App.vue'
import router from './router'
import Highcharts from 'highcharts';

const app = createApp(App)

app.use(createPinia())
app.use(router)



app.mount('#app')

  
