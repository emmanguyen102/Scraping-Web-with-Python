import codecademylib3_seaborn
from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# make a request to this site to get raw HTML,
# which can later turn into a BeautifulSoup object
webpage_requests = requests.get("https://content.codecademy.com/courses/beautifulsoup/cacao/index.html")

# Create a BeautifulSoup object called soup to
# transverse this HTML, parser = "html.parser"
soup = BeautifulSoup(webpage_requests.content, "html.parser")
print(soup)

# Find out how many terrible chocolate bars are out
# there, How many earned a perfect 5. Let's make a 
# histogram of this data

# First thing, get all of the tags contain the ratings
choco_ratings = soup.find_all(attrs={"class": "Rating"})

# create an empty list called ratings to store all ratings in
ratings = []

# loop through ratings tags and get the text contained 
# each on. Add it to ratings list
# convert rating to float, so that ratings list will be 
# numerical. This 'll help with calculations later
for rating in choco_ratings[1:]:
  text = float(rating.get_text())
  ratings.append(text)

# create a histogram of the ratings value
# shown in local host web browser...
plt.hist(ratings)
plt.show()

# find 10 most highly rated chocolates. 
# 1 way is to create a df that has chocolate companies
# in 1 column and ratings in another. Then using
# groupby to find the ones with highest average rating

# first, find all tags on the webpage that contain the
# company names
companies = soup.select(".Company")

# create empty list containing companies' name
companies_list = []

for company in companies[1:]:
  name = company.get_text()
  companies_list.append(name)

# create a df with 2 columns: Comapny and its 
# corresponding ratings
dict = {"Company": companies_list, "Rating": ratings}
df = pd.DataFrame.from_dict(dict)

# group df by Company and take 
mean_vals = df.groupby("Company").Rating.mean()
ten_best = mean_vals.nlargest(10)
print(ten_best)

# We want to see if the chocolate experts tend to rate 
# chocolate bars with higher levels of cacao to be better
# than those with lower levels of cacao

cacao_percent = soup.select(".CocoaPercent")
percents = []

for percent in cacao_percent[1:]:
  percentage = int(float(percent.get_text().strip("%")))
  percents.append(percentage)

dict.update({"Cocoa_Percentage": percents})
df = pd.DataFrame.from_dict(dict)
print(df)

# make a scatterplot of ratings 
plt.scatter(df.Cocoa_Percentage, df.Rating)
plt.show()
plt.clf()

z = np.polyfit(df.Cocoa_Percentage, df.Rating, 1)
line_function = np.poly1d(z)
plt.plot(df.Cocoa_Percentage, line_function(df.Cocoa_Percentage), "r--")
