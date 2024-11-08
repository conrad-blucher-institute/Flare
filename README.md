##Flare

## Description

Flare is a student-built and maintained web application that visualizes data generated by Artificial Intelligence models. Flare helps stakeholders and researchers track model progress, assess performance, and gain valuable information from AI outputs.

## Prerequisites
 - Docker Desktop: Ensure Docker Desktop is installed and running to manage containerized applications.
 - Linux/WSl: Required to ensure permissions are handled appropriately.
    - Installation for Windows:https://learn.microsoft.com/en-us/windows/wsl/install
 - NVM: Use Node Version Manager (NVM) to manage Node versions, ensuring compatibility with the frontend Vue app. 
    - Installation: Detailed below in Vue Development Setup
 - Node.js: A JavaScript runtime for running server-side code.
    - Installation: Detailed below in Vue Development Setup
 - Vite: A development server and build tool optimized for Vue.
    - Installation: Detailed below in Vue Development Setup

## To set up and run Flare in a Docker container:
0. Set Up Environment Variables and Nginx:
    - Create a .env file in the project’s root directory. This file will contain environment variables needed by Docker.
    - Copy the contents from env.dist and update the values with your own variables.
    - Create a nginx.conf file in the project's root directory.
    - Copy and paste nginx.conf.template's contents into nginx.conf
    - Replace __Port__ and __ServerName__ with the correct variables.
1. Ensure that Docker Desktop is running on your machine.
2. Ensure you are using a Linux/WSL terminal.
3. Start in the root directory: 'cd CDL-Broadcast'
4. Run 'docker compose build' and 'docker compose up' (run 'docker compose up -d' to run in the background)
5. If you make changes to the code make sure you 'docker compose down' and then repeat step 4.

## Vue Development Setup(Frontend)
1. Use NVM to switch to the Node version specified in the frontend container.
    - Linux/WSL Installation:
        - Install:'curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash'
        - Install node using nvm : 'nvm install node '
        -Install node version: 'nvm install 22.10.0'
        - Switch to the version used in the frontend container  : 'nvm use 22.10.0'
        - Check the node version: node -v
        - Install vite: 'nvm install vite'
2. Change to the Vue app directory 'cd CDL-Broadcast/vue-ui'
3. Run the development enviornment : 'npm run dev'


## Authors
* [@Anointiyae Beasley](https://github.com/abeasley1722) - anointiyae.beasley@tamucc.edu
* [@Matthew Kastl](https://github.com/matdenkas) - mkastl@islander.tamucc.edu
* [@Beto Estrada](https://github.com/bestrada33) - bestrada4@islander.tamucc.edu
* [@Savannah Stephenson](https://github.com/lovelysandlonelys) - sstephenson2@islander.tamucc.edu
* [@Florence Tissot](https://github.com/ccftissot)


