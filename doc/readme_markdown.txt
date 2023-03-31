#Advarmap
*Avarmap* stands for Advanced Recipe Manager for Programmer.
Avarmap is a multiplatform recipe viewer and creater.

## Motivation
Motivation behind Avarmap:
1. Loads recipes in a human-readable format. For easily saving in GIT repository.
2. Recipes should support style annotations like bold or italic text.
3. Recipes should support semantic annotations like duration, rating or author.
4. New recipes should be easy to add.
5. Export recipes as PDF, if Advar isn't available on a system. 

Avarmap use as mixing of XML with some supported html tags as a recipe format. Creation of recipes is supported by different text parsers.
 Which can create automatically the Advarmap recipe format from plain text.
 
### The Advar File Format
The following code shows an example of Advar recipe format.
<pre><code class="language-html">
`
<root>	
<header>
		<format-version>1.0</format-version>
		<name>Example recipe</name>
		<tags>
			<author>Patrick Mispelhorn</author>
			<rating>5.0</rating>
			<time>4 h</time>
		</tags>
	</header>
	<ingredients>
      <ingredient amount="300" name="Corn flower" unit="UnitGram"/>
      <ingredient amount="6" name="little Egg(s)"/>
      <ingredient name="some herbs"/>
	<ingredients/>
	<method>
		The cooking method for the recipe. At this point we <b>can</b> use some HTML tags.
	<method/>
</root>
`</code></pre>
 The complete recipe is wrapped in a *root* tag. The root tag has three tags:
 **header:** defines semantic annotations
 **ingredients:** the needed ingredients for the recipe
 **method:** Some text which support the b, i, u, h1, h2, h3 and h4 HTML tags.
 
### Search Field

The search in advar based on the search in  the free E-book managment software [Calibre](https://manual.calibre-ebook.com/gui.html#search-sort).

**Synopsis:**  *tagname* **:** *query*  [[*boolean connection*] *tagname* **:** *query* ]...

| Variable |Description  | 
|---|:-------|
|**boolean connection**|	**and** \| **and not** \| **or** \| **or not** or connect tag queries. These queries will left    						associative bracketed. If the boolean connection is ommited the **or** operator is used.|
|**tagname**|	The name of tag defined in *my_tags.py*.|
|**query**		| *number_query* \| *string_query* \| *void_query* \| *boolean_query* \| *duration_query*|
|**number_query**	|A  relational operator followed by a number e.g. > 10|
|**duration_query**	|A  relational operator followed by a number followed by a time suffix (**h** \| **min**) e.g. < 2 h|
|**string_query**	|	Some text in quotes e.g "warm" or 'A simple query'|
|**void_query** | Omit the query.|
|**boolean_query** | **true** \| **false** |

**Quicksearch Format**
If the search query none of charakters (', " or : ) then the search query *s* is transformed to: <pre>name: "*s*" or ingredient: "*s*"</pre> (see predefined tags) 
 
**Example 1:**  *\"Apple\" rating:>3* search for the keyword Apple and all recipes must have a higher rating than 3.

**Example 2:** *\"Apple\" rating:>3* or name:"orange" search for the keyword Apple and all recipes must have a higher rating than 3 or the name orange.

**Example 3:**  'Curry' vegetarian:true duration: > 30 min and author:'Me'
Search for a recipe with the name *Curry* which is either vegearian or takes longer as 30 minutes. The author has to be *Me*.
### Tags
Tags define key value pairs to recipes e.g. rating of this recipe is 5.
These key value pairs can be queried in the search field. Every used tag in a recipe must be defined in xml and has a datatype. The datatype defines which values can have a tag and defines the possible search terms for the tag. The name of every should contains the lower case letters a to z and the underscore. For example *vegan*, "test_tag" or *todo* are valid tag names. The following table shows all supported tag types with examples.

| Tag name |Query Example   |      XML Definition Example     |  Notes |
|---|:-------|:-------------:|------:|
| Boolean| ```todo: true``` |  ```<todo>true</todo>``` |  |
| Number|```rating: > 4``` |    <rating>5</rating>   |    relational operator |
| Duration|```duration: < 1 h``` |    <duration>1 h</duration>   |    relational operator, *h* or *min* suffix |
| String|```author: Patrick``` | ```<author>Patrick</author>``` |     |
| Void|```vegetarian:``` | ```<vegetarian/>``` |    Hierachy possible |

A *hierachiy* defines superset tags over other e.g *vegetarian* is a super set of *vegan*. If we search for vegetarian recipes, we find also all vegan recipes. Another example is that the *asian* tag is a superset of the *japanse* and *chinese* tag. Hierachiy queries ar only supported by tags of type *void*.

The *relational operators* are used before dates and numbers are: 
< (smaller), <= (smaller or equal),>= (greater or equal), > (greater), != (unequal), = (equal).

*tag absence* is tag is missing its default value is used.
### Predefined special tags
**all** match agiants every recipe e.g. all:
**name:** match a string against the recipe name e.g name: "spinach"
**random:** returns *k* random recipes e.g. random: *k*
**ingredient:** match the ingredient list against a string e.g. ingredient: "spinach"

#### TODO
Tag absence 
all: or not rating: -1

#### Install
Install following packages (tested of Ubuntu 18.4)
sudo apt-get install pkg-config libcairo2-dev gcc python3-dev
libgirepository1.0-dev

### Windows
https://pypi.org/project/PyGObject/