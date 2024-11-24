## TonDeck
TonDeck is a simple tool for tracking prices and information about tokens on the TON network. It allows you to get up-to-date data on the cost of tokens and their changes in real time. Suitable for those who want to monitor tokens in the TON network.

## Project structure

```
.
├── README.md # This file
├── UpdateGecko.py # Script for updating token information
├── bot.py # Script for working with the bot (if used)
├── main.py # Main executable script
└─ ─ server # Folder with the server part
├── App # Main application logic
│ ├── Storage # Data storage
│ │ ├── config.py # Configuration
│ │ └── data.json # Token data
│ ├── Web3 # Module for working with TON API
│ │ └── tonapi.py # Code for accessing the TON API
│ ├── routes # API routes
│ │ └── tondeck_api.py # API request handler
│ ├── templates # HTML templates for the frontend
│ └── utils # Helper functions
└── __init__.py # Initialize the backend
```

## Installation
  
  1. Clone the repository:
  ```bash
  git clone https://github.com/ganyamede/TonDeck.git
  ```
  
  2. Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
  
  ## Usage
  
  ### Starting the application
  To start the server, run:
  
  ```bash
  python main.py
  ```
  
  ### Updating token data
  Script for updating token data (should always run)
  
  ```bash
  nohup python UpdateGecko.py
  ```

## More about TonDeck

# 1. Main menu

![telegram-cloud-photo-size-2-5341472160146908841-y](https://github.com/user-attachments/assets/21838992-52ca-4c54-bdf1-1a7268e4d0e7) 

  - The main menu has a search, sorting in descending order and all the main information
  - There are no pools here, only natural tokens

# 2. Search
  
  ![telegram-cloud-photo-size-2-5341472160146908845-y](https://github.com/user-attachments/assets/9ac22bae-9678-4f3e-94d7-6ae0cc2ed04b)
  
  - Search works in both directions, as well as by token name and by address
  
  <img width="484" alt="image" src="https://github.com/user-attachments/assets/95ce1369-727f-40e1-9772-4bfdb428d3eb">
  
  - Search by address will be if the search length reaches 48 characters, otherwise it will be empty

# 3. Token page

![telegram-cloud-photo-size-2-5341472160146908844-y](https://github.com/user-attachments/assets/ff87b060-c0bf-41ed-b841-a3d3897933ff)

- In the main menu, when you click on the token, you are redirected to a tab with detailed information
