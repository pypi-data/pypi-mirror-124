# A package that allows you to get world and country pouplation data

Population Data of the world

Developed by Anshu from Techi Tutorials (c) 2021

How To Use

```python
from population_data import Population_data

# YOUR API KEY(Get it from here https://rapidapi.com/aldair.sr99/api/world-population/)

my_api = YOUR API KEY

# country population data
country_population = Population_data.get_country_population(my_api, "Canada")
print(country_population)

# world population data
world_population = Population.get_world_population(my_api)
print(world_population)

```

get_country_population() method takes additional argument of the query string, that is country name
and returns the json response

Check out: https://techitutorials.com
