# Imports, note that we skip the imports in other examples...
from pyleri import (
    Grammar,
    Keyword,
    Regex,
    Sequence)

# Create a Grammar Class to define your language
class MyGrammar(Grammar):
    r_name = Regex(r'[^\n0-9][^\n]*')
    START = Sequence(r_name)

# Compile your grammar by creating an instance of the Grammar Class.
my_grammar = MyGrammar()

# Use the compiled grammar to parse 'strings'
print(my_grammar.parse('ä').is_valid) # => True
print(my_grammar.parse('bye "Iris"').is_valid) # => False
print(my_grammar.parse('bye "Iris"').as_str()) # => error at position 0, expecting: hi