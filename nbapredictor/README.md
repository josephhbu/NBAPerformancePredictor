# ???Predicting NBA team performance with machine learning using Python???
Joseph Bu
# Part 0: Saving the dataset
Season Standings: https://www.basketball-reference.com/leagues/NBA_2021_standings.html
Team Per Game Stats:https://www.basketball-reference.com/leagues/NBA_2021.html

You can navigate to get the dataset from a different season. Above the table, if you click share & export for a drop-down menu. Then click get table as CSV. Copy the table starting from 'Rk' till the end, and paste it to wherever you want to save, such as Excel. 

# Part 1: Using metrics to predicting the season standings:
* In order to run this script, you need to download data from 2010 to 2021 seasons for NBA Standings and NBA team per game stats in the same directory as the main file(nba_predictor). This is a total of 22 files.
* Install packages: pandas, sklearn.tree, numpy, dataframe_image, altair, altair_saver
* Open the file named nba_predictor.py. When you run the file, you will have to enter how many times you want to loop the model. The higher the number you input, the more likely you are to get more accurate results, but keep in mind that it is expected to take more time. You will get a png file of a table showing predicted results and an HTML file visualizing the difference between the predicted and the actual standings as the program's output. 

# Part 2: Predicting outcomes of individual games based on recent game averages:
* Install the library NBA API (can be found here: https://pypi.org/project/nba-api/), along with Pandas, numpy, Matplotlib, and Scikit learn
* Open the file named predict_outcome.py. This is the main file. Run it, and it will print the accuracy scores for one model run on the Chicago Bulls 2010-11 season, and generate the figures as mentioned in the specifications. Will save 4 .png figures in total.
* To predict the outcome of an upcoming game, open and run predict_next.py. Follow the instructions as detailed in the terminal to obtain the prediction for the next game of a given NBA team. The implementation is user-input-friendly and responds well to errors, so simply following the instructions will suffice.

# Part 3: Schedule Difficulty Effect Evaluation:
* If you have not already done so, install the libraries NBA API, pandas, seaborn, matplotlib
* Open the file named schedule_diff.py. This is the main file, and when you run it, it will generate a dataframe table for the 2016-17, 2017-18, and 2018-19 Seasons and show the mentioned stats for back-to-back games. It will also generate two figures, one showing the average back-to-back win percentage and another showing the non average back-to-back win percentage all from the 2016-17 season to the 2018-19 season.