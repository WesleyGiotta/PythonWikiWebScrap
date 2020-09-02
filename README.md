# Python Wiki Web Scrapping Assignment
Final Project from my data wrangling class at UCF.

For full paper see [Giotta_Final](./Documents/Giotta_Final.pdf) in the Documents directory. To see the original assignment see [HW5](./Documents/HW5.pdf) in the Documents directory.

I started in Python3 and then finished in R. I found that all the urls were the same with the exception of the year, so I made a list of all the urls by adding the appropriate number to the year for the census and election urls.
After that I used BeautifulSoup and made functions to grab the needed table from a url and then looped through it for them all. Because the length for the election tables were not all the same I made the range for the loop very long but had it break when it hit the total at the bottom of the tables. Also, I had to make sure that the democrat and republican data went in the correct columns by having the function check if the first column had democratic or not. The census table was much nicer with the exception of the column for population sometimes swapping.
Then the nested lists that the functions gave me were insterted into a SQL database using sqlite3 and an index was made to make sure I did not insert the data twice by accident.
Lastly, I selected the asked for results and used Rstudio's ggplot2, dplyr, and RSQLite packages to make the graphs.
