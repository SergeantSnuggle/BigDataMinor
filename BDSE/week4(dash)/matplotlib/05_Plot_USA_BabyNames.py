import pandas as pd
import matplotlib.pyplot as plt

names1880 = pd.read_csv('names/yob1880.txt', names=['name', 'sex', 'births'])

names1880[:5]


# Since we have numerous data files, the following snippet combines all of these data into a single pandas DataFrame and add a *year* field. 
# Refer to *Python for Data Analysis - page 33* for an extended description of the code below. Note that all .txt files must be stored as *./names*.

years = range(1880, 2013)
pieces = []
columns = ['name', 'sex', 'births']

for year in years:
    path = 'names/yob%d.txt' % year
    frame = pd.read_csv(path, names=columns)
    frame['year'] = year
    pieces.append(frame)

# Concatenate everything into a single DataFrame
names = pd.concat(pieces, ignore_index=True)

names[:5]


# We can now perform several types of aggregation. For example, let's create a new DataFrame containing the total number of births per year, split by sex.


total_births = names.pivot_table('births', index='year', columns='sex', aggfunc=sum)


total_births.head()

total_births.plot(figsize=(10,5),title='Total births by sex and year')


# Now suppose we would like to analyse how frequently the names *John*, *Michael*, *Mary*, *Mark*,*Jeremy* and *Amelia* occurr over time.

# First we redefine *total_births*, this time aggregating data by *name* rather than *sex*. Then we grab the subset of names that we are interested in and plot it.

total_births = names.pivot_table('births', index='year', columns='name', aggfunc=sum)
subset = total_births[['John', 'Michael', 'Mary', 'Mark','Jeremy','Amelia']]
subset.plot(subplots=True, figsize=(15, 17), grid=False,title="Number of births per year")


# We can also look at how the distribution of boy names by final letter has changed over the last 100 years. To see this, we first aggregate all of the births in the full dataset by year, sex, and final letter.

# extract last letter from name column
get_last_letter = lambda x: x[-1]

last_letters = names['name'].map(get_last_letter)
last_letters['name'] = 'last_letter'

table = names.pivot_table('births', index=last_letters,columns=['sex', 'year'], aggfunc=sum)


# Then we select a few representative years, spanning 100 years in total:

subtable = table.reindex(columns=[1912, 1962, 2012], level='year')
subtable.head()


# Further, we normalize the table by the number of births, so as to obtain the proportion of total births for each sex ending in each letter:


letter_prop = subtable / subtable.sum().astype(float)
letter_prop.head()


# With the letter proportions now in hand, we can make bar plots for each sex broken-down by year
# 


fig, axes = plt.subplots(2, 1, figsize=(11, 10))
letter_prop['M'].plot(kind='bar', rot=0, ax=axes[0], title='Male')
letter_prop['F'].plot(kind='bar', rot=0, ax=axes[1], title='Female',legend=False)


