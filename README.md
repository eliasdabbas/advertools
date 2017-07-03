
## advertools: create, analyze, & manage campaigns better

### In brief: 

If you work in online marketing and you spend your day
generating keywords, writing text ads, analyzing, and 
managing marketing / advertising accounts, this package 
has a bunch of tools that can help you get more productive. 

### Installation: 

For some reason it's still not installing properly. Please try from 
GitHub directly for now. Sorry! 
```commandline
pip install advertools

```


### Main Features: 

- Setup search campaigns, ad groups, and keywords
- Get insights on keywords by getting the weighted word frequency
- Get insights on any social media posts (together with their metric), 
to see which words are creating more impact

### Examples: 

Let's say you want to set up a search advertising account
for a used cars website. 
You start by generatig a list of the possible elements of the thinking
process of researching used cars online. 
Possible elements: 
- car: different variations of the concept of a car; car, cars, autos, etc
- buy: words indicating purchase intent; buy, for sale, etc
- price: price, cost

Now all you need is to generate to full list of possible combinations
of all those elements. 
How about something like this: 

```pydocstring
>>> import advertools as adv
>>> import pandas as pd
  
  
>>> data_dict = {
        'car': ['car', 'cars', 'autos'],
        'buy': ['buy', 'for sale'],
        'price': ['price', 'cost'],
    }
    


>>> keywords = adv.kw_combinations(
        data_dict=data_dict,
        combos=adv.permute(data_dict.keys()),
        nesting=['car'])
        


>>> keywords.shape
    (240, 4)
        

>>> keywords.iloc[[1,2,100,101, 150,151,200,201,202], :] # sample

      car         Labels         Keyword Criterion Type
1    autos        Car;Buy       autos buy         Phrase
2    autos  Car;Buy;Price  autos buy cost          Exact
100    car      Car;Price        car cost          Exact
101    car      Car;Price        car cost         Phrase
150    car      Price;Car       price car          Exact
151    car      Price;Car       price car         Phrase
200   cars  Price;Buy;Car   cost buy cars          Exact
201   cars  Price;Buy;Car   cost buy cars         Phrase
202   cars      Price;Car       cost cars          Exact

```

So, with three variants of the word 'car', two variants of the words
'buy' and 'price', we were able to generate 240 keywords. 
Not only that, we now have a DataFrame that can immediately be saved 
as a csv file and uploaded through AdWords editor for launch. 

Almost! 

We still have some issues, and some clarifications to make. 

The 58th and 59th rows present a meaningless combination: 

```pydocstring
keywords.iloc[58:60,:]
 
      car     Labels        Keyword Criterion Type
58  autos  Buy;Price  for sale cost          Exact
59  autos  Buy;Price  for sale cost         Phrase

```

Let's solve this. Let's take a look at the ``adv.permute`` function. 
It is basically a wrapper for ``itertools.permutations``, and this is
the function responsible for generating the possible keyword 'templates'
for us. All we need to do is make sure it gives meaningful ones. 

```pydocstring
data_dict.keys()

dict_keys(['car', 'buy', 'price'])


combos = adv.permute(
            keys=data_dict.keys(),
            keys_to_keep=None,
            min_len=2,
            max_len=3
)
```

This is how we can generate all possible permutations of the keys
of our data_dict (which are the columns of our DataFrame).
The default ``itertools.permutations`` needs an n argument which 
determines the length of each permutation. In this function, we produce
all permutations from ``min_len`` up to ``max_len``.
``keys_to_keep`` simply restricts the keys to minimize clutter things. 

To make sure we are getting meaningful combinations, we will need to 
select which of the permutations make sense. 
For example `car buy`, and `buy car` make sense, but `buy price` does
not. So we only select the ones that make sense for us.
