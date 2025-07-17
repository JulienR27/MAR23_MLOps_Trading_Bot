# Trading Bot

To run this stocks prediction service, type ```docker build -t trading_bot .``` in your terminal to build the docker image and ```docker run -p 8000:8000 trading_bot``` to run it.\
Once running go to http://127.0.0.1:8000/docs on your your web browser.\
Then :
- Type a valid ticker from SP500 stocks market
- choose 1d (one day), 1w (one week), 2w (two weeks) or 1m (one month) for time_horizon
- write market, fundamental or market_and_fundamental to choose the type of data you want to make the prediction
The app will return the model's prediction for the stock's performance at the chosen time horizon.
