import plotly.express as px
import extract


# group by items in facilities dataframe for "countery" and count the number of studies in each country, then sort by the number of studies
# note that in facilities dataframe one study that is identified by nct_id can have multiple rows, each row has a country in country column
# so we need to group by nct_id and count the number of unique countries in each study
def getCountryDist(facilities):
    facilities = facilities.dropna(subset=['country'])
    country_dist = facilities.groupby('nct_id')['country'].nunique().reset_index(name='counts')#.groupby('counts').size().reset_index(name='counts')
    country_dist = country_dist.rename(columns={'counts': 'number of countries'})
    return country_dist

# plot bar chart of the distribution of studies in each country
def getChart(country_dist):
    expert_bar_country = px.bar(country_dist, x='number of countries', y='counts', title='Distribution of Studies in Each Country',
                                labels={'number of countries':'#countries', 'counts':'#studies'})
    return expert_bar_country

# merge the two functions above to get the bar chart of the distribution of studies in each country
def getCountryBar(facilities):
    country_dist = getCountryDist(facilities)
    expert_bar_country = getChart(country_dist)
    return expert_bar_country

facilities = extract.load_all_data()[2]
getCountryDist(facilities).head()

'''# Define a function to get the number of unique countries in each facility
def getCountryDist(facilities):
    # Group facilities by the 'nct_id' column and get the number of unique countries in each group
    country_dist = facilities.groupby('nct_id')['country'].nunique()
    
    # Reset the index of the resulting DataFrame and rename the 'counts' column to 'number of countries'
    country_dist = country_dist.reset_index(name='number of countries')
    
    # Group the DataFrame by the 'number of countries' column and count the number of occurrences of each value
    country_dist = country_dist.groupby('number of countries').size().reset_index(name='counts')
    
    return country_dist'''
