# MLFoodPairing

Food pairing is an art in and of itself. Combining ingredients - their texture, aroma and taste - goes a long way when it comes to creating an enjoyable meal.
        
In this project, I wanted to know if the internet had the answer to the common question: `"What goes well with ...?"`. While the question of food pairing can be tackled by trying to identify key flavor components that ingredients have in common or that compliment each other, I was interested in taking a different approach. I first collected data from thousands of popular online recipes and used Natural Language Processing (NLP) and Machine Learning (ML) to extract the ingredients for each recipe. I then simply computed the most common food combinations in the most popular recipes.

## Data source

I used the [Food2Fork API](http://food2fork.com/about/api) to gather information about some of the most popular online recipes. The [Food2Fork API](http://food2fork.com/about/api) allows to view the top socially-ranked recipes across a database of popular publishers (All Recipes, Epicurious and many others) or to search through all recipes by name or ingredient.
Using this API, I was able to collect a list of ingredients for the 30,000 most popular recipes, where populaity is measured by social media ranking.

## Ingredient parsing

Online recipes can be messy. Ingredient lists can be messy too: they come in many flavors. For example, `"1/4 cup cooked shredded chicken"`, or `"1/3 cup chopped fresh cilantro"` or `"Fresh avocado cubes, for garnish, if desired"`. While, in fact, all we are interested to get from these is `chicken`, `cilantro` and `avocado`. For humans, parsing these ingredient lists and figuring out what we need to buy at the grocery store is trivial. For a computer, not so much.

Natural Language Processing allows computers to extract data from human languages. I used NLP and, in particular, the Python [NLTK](https://www.nltk.org) package (Natural Language ToolKit) to split phrases into words and categorize these words into word classes (noun, verb, adjectives, ...): this is a process known as part-of-speech tagging or POS-tagging.

Using the words themselves, their POS tags and various combinations of consecutive words and tags as features, we can build a Machine Learning model. Such a model will then be able to predict what kind of word is a specific word in a phrase. Is it an ingredient name, a quantity, a unit of measurement or some other word that can be ignored for this project? In order to achieve this, I used a model called Conditional Random Field (often used for labeling or parsing sequential data, such as natural language text or biological sequences) and the Python [python-crfsuite](https://python-crfsuite.readthedocs.io/en/latest/) package.

For training the model, I used 1000 recipes for which I semi-manually tagged every word of every ingredient phase as `QTY` (quantity), `UNIT` (unit of measurement), `NAME` (ingredient name) or `COM` (comment). I split this data into 80% training and 20% testing data. After training the model, the precision for ingredient name prediction for the testing data was about 94%.

I then wrote a small [Flask API](http://frenetic.pythonanywhere.com/) that will return the model prediction from an ingredient phrase.

## Cleaning up
          
First, I parsed all ingredients for each recipe, using the model discussed in the previous section. Each ingredient name was also lemmatized (see NLP stemming/lemmatization). For example, `tomato` and `tomatoes` are the same ingredient. Lemmatization will transform `tomatoes` into `tomato`.

I then counted all ingredients in all recipes and discarded the less common ingredients. This will get rid of most misspelled ingredients and most ML prediction errors.

With this new list of ingredients, I built another Machine Learning model (a logistic regression model) to categorize recipes between desserts and non-desserts. I was then able to filter out dessert recipes from the rest.

Then, I filtered out some of the least interesting ingredients, like salt, pepper, oil, sugar, water, flour, ... and I mapped some ingredients to take care of the last ingredient name prediction errors, spelling mistakes and other examples like `eggplant` and `aubergine` depending on where in the world the recipe came form.

With the remaining list of ingredient, I manually categorized them into "produce", "meat/fish", "nut", "spice", "herb", "dairy" or "other" and filter out all of the "other" ingredients to keep a total of 251 different ingredients.

## Data visualization

Finally, I used d3.js for data visualization. Check it out on the [results](results.html) page.

## Authors

* **Julien Spronck** - [https://frenetic.be](https://frenetic.be)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* This project was powered by [Food2Fork.com](http://food2fork.com).

* This project made use of [MongoDB](https://www.mongodb.com) and [pymongo](https://api.mongodb.com/python/current/).

* The following blog post was very helpful for tagging recipe ingredients: ["Structuring text – Sequence tagging using Conditional Random Field (CRF). Tagging recipe ingredient phrases"](https://rajmak.wordpress.com/2016/02/19/structuring-text-using-conditional-random-field-crf-tagging-recipe-ingredient-phrases/).

* So was the original NYT blog post about ["Extracting Structured Data From Recipes Using Conditional Random Fields"](http://open.blogs.nytimes.com/2015/04/09/extracting-structured-data-from-recipes-using-conditional-random-fields/?_r=0).

* Other Python packages used:
    * [python-crfsuite](https://python-crfsuite.readthedocs.io/en/latest/)
    * [Flask](http://flask.pocoo.org)
    * [Scikit-learn](http://scikit-learn.org/stable/)
    * [Pandas](https://pandas.pydata.org)
    * [NLTK](https://www.nltk.org)
    * [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
    * [Colorama](https://pypi.python.org/pypi/colorama)
    * ...