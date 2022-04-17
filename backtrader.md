
a. The title of your site and a link to the URL where it is deployed
-Title of the site: Backtrader. 
-Once the UI and UX are polished and trading strategy functions are improved, I will deploy this app to Heroku

b. Describe what your website does
-This website allows users to view stocks and browse stock prices(high, low, close, open) of the last month. And most importantly, this website allow users to test their trading strategies. It will show users how much they would make or lose if they used a trading strategy on certain stock.  

c. List the features you implemented and explain why you chose those
features to implement

-Simplify Home Page Design
-Implement authentication and authorization for the purpose of security
-Prepopulate stock prices database to ensure speed
-Search options User can search within the app on stocks.




d. Walk someone through the standard user flow for the website
1. The user starts on the homepage
2. From the homepage the user either fill the login form or sign up. 
3. Once the user has logged in, the user will be taken to the stocks page
4. From stocks page, user clicks on individual stock to view the prices of certain stock or type in the search box to search a particular stock
5. From the stock price page, user can navigate to backtesting page
6. On the Backtesting page, user can fill the backtesting form to start testing
7. From the backtesting page, user can get to tests page, where the testing results can be browsed there. 
  
e. Keep the API in there, and if you have anything to say about the API then add some notes
-I used Alpaca API to get the historical price data of stocks. More specifically, I use alpaca python client. 

f. Identify the technology stack used to create your website
-The frontend stack consists of two main elements: HTML and CSS. I used a CSS framework: Bootstrap. 
-The backend of this application uses python, flask, and psql. For libraries, I used WTForms, and backtesting. 



   
