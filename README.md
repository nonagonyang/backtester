
## BackTester visit 👉 https://strategy-backtester.herokuapp.com 



https://user-images.githubusercontent.com/28469448/198850050-6a27522d-394f-411f-8f3c-c11a72b369d4.mp4


## About
* This website allows users to view QQQ stocks and browse stock prices(high, low, close, open) of the recent month. And most importantly, this website allows users to test their trading strategies on their selected stock. It will show users how much they would earn or lose if they used a trading strategy on a certain stock over a certain period.    

## Features
* Prepopulate stock prices database to ensure speed
* Search options User can search within the app on stocks.
* Browsing Stock Prices through Chart and Table
![](https://github.com/nonagonyang/backtester/blob/main/Browse%20Stocks%20.gif)
* Test Trading Strategies and View their trading logs
![](https://github.com/nonagonyang/backtester/blob/main/Test%20Trading%20Strategies.gif)

## ER Diagram
![](https://github.com/nonagonyang/backtester/blob/main/docs/ER_Diagram.png)

## Standard user flow:
1. The user starts on the homepage
2. From the homepage the user either fill out the login form or sign up. 
3. Once the user has logged in, the user will be taken to the stocks page
4. From stocks page, user clicks on individual stock to view the prices of certain stock or type in the search box to search a particular stock
5. From the stock price page, user can navigate to backtesting page
6. On the Backtesting page, user can fill the backtesting form to start testing
7. From the backtesting page, user can get to tests page, where the testing results can be browsed there. 
  
## External API:
* I used Alpaca API to get the historical price data of stocks. More specifically, I use alpaca python client. 

## Technology stacks used to create the website:
* The frontend stack consists of two main elements: HTML and CSS. I used a CSS framework: Bootstrap. 
* The backend of this application uses python, flask, and psql. For libraries, I used WTForms, and backtesting. 



   
