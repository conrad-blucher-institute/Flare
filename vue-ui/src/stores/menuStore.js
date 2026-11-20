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
import TurtleImage from '@/assets/images/turtle_and_fish.png';
//Ensure names match the route names in router/index.js for proper navigation.
export const useMenuStore = defineStore('menu', {
  state: () => ({
    
    dropDownMenuOptions: [
      {
        label: 'Home',
        link: { name: 'home' }
      },
      {
        label: 'Cold Stunning Links',
        children: [
          {
            label: 'Laguna Madre',
            children: [
              {
                label: 'Graph',
                isHeader: true
              },
              {
                label: 'Laguna Madre Coldstunning Graph',
                link: { name: 'crps' }
              },
              {
                label: 'Additional Information',
                isHeader: true
              },
              {
                label: 'Wind Speed Graph',
                url: 'https://cbigrid.tamucc.edu/tpw/graph-only-wind.html' 
              },
              {
                label: 'Ensemble Air Temperature Predictions',
                link: { name: 'airTemperatureEnsemble' }
              },
              {
                label: 'Old Version of Ensemble Water Temperature Predictions ',
                link: { name: 'waterTemperatureEnsemble' }
              },
              {
                label: 'TPW AI Water Temperature Prediction Model',
                url: 'https://cbigrid.tamucc.edu/tpw/'
              },
              {
                label: 'AI Model Performance SuperTool',
                url: 'https://lighthouse.tamucc.edu/supertool.php?stnid=013&elev=mwl&mode=nnwtp'
              },
              {
                label: 'NOAA Sea Turtle Stranding And Salvage Network',
                url: 'https://www.fisheries.noaa.gov/national/marine-life-distress/sea-turtle-stranding-and-salvage-network'
              }
            ]
          },
         
            {
              label: 'Espiritu Santo Bay',
              children: [
                {
                  label: 'Graph',
                  isHeader: true
                },
                {
                  label: 'Espiritu Santo Bay Graph',
                  link: { name: 'esb' }
                },
                {
                  label: 'Additional Information',
                  isHeader: true
                },
                {
                  label: "Port O'Connor Wind Speed Measurements and Predictions (Coming Soon)",
                  url: ''
                },
                {
                  label: "TWC Port O'Connor Ensemble Air Temperature Predictions ",
                  url: "https://cbigrid.tamucc.edu/tpw/ibm-charts.html?location=port-o%27connor"
                },
                {
                  label: 'NOAA Sea Turtle Stranding and Salvage Network',
                  url: 'https://www.fisheries.noaa.gov/national/marine-life-distress/sea-turtle-stranding-and-salvage-network'
                },
                {
                  label: 'Mid-Coast Sea Turtle Rescue',
                  url: 'https://www.sabaypartnership.org/program/mid-coast-sea-turtle-rescue/'
                },
                {
                  label: 'TWC Additional Locations for Ensemble Air Temperature Predictions',
                  url: 'https://cbigrid.tamucc.edu/tpw/map-index.html'
                }
              ]
            }

        ]
      },
      {
        label: 'About Flare',
        link: { name: 'about' }
      }
    ],

    slidingMenuOptions: [
      {
        label: 'Cold Stunning Group',
        link: { name: 'coldstunning' },
        image: TurtleImage,
        location: 'Cold-Stunning Models',
        message: '120-hour predictions of water and air temperatures',
        children: [
          {
            label: 'Laguna Madre',
            link: { name: 'crps' }
          },
          {
            label: 'Espiritu Santo Bay',
            link: { name: 'esb' }
          }
        ]
      }
    ]
  })
});
