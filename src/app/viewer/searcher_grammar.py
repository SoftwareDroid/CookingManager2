# Imports, note that we skp the imports in other examples...
from pyleri import (
    Grammar,
    Token,
    Repeat,
    Regex,
    Sequence,
    Optional,
    Choice)

class _SearchGrammar(Grammar):
    """ The grammar which defined the search query"""
    # e.g. hello:, time_ward: or space_time42:
    identifier = Regex(r'[a-zA-Z]\w*:')
    # a quoted string with " or'
    string = Choice(Regex(r'"[^":]*"'), Regex(r"'[^':]*'"))
    # e.g Kuchen, Kuchen(Birne)
    #word_without_quotes = Regex(r'[^\"\':]+')
    # first search part is one word or a qouted string if needed e.g. "Apple Pie" or ApplePie
    #first_part = Choice(string)

    # math boolean logic
    and_token = Token("and")
    or_token = Token("or")
    not_token = Token("not")
    and_not_token = Sequence(and_token, not_token)
    or_not_token = Sequence(or_token, not_token)
    # only "not" make no sense and the simple "or" is default the conjunction
    boolean_operation = Choice(or_token, and_token, and_not_token, or_not_token)

    # number support
    # e.g 1.002, 53, 223.234
    t_float = Regex(r"\d*.\d+|\d+")
    # Some comparision Token
    token_equal = Token(r'=')
    token_smaller = Token(r'<')
    toke_greater = Token(r'>')
    token_smaller_equal = Token(r'<=')
    token_greater_equal = Token(r'>=')
    token_unequal = Token(r'!=')
    relation_token = Choice(token_unequal, token_equal, token_smaller, token_smaller_equal, toke_greater,
                            token_greater_equal)
    value_number = Sequence(Optional(relation_token), t_float)

    # Boolean support
    token_true = Choice(Token("1"), Token("true"), Token("True"))
    token_false = Choice(Token("0"), Token("false"), Token("False"))
    value_boolean = Choice(token_true, token_false)

    # Time / Duration support
    # e.g h,H, hour or hours
    token_day = Regex(r"d|day")
    token_hour = Regex(r"(h|H)(ours?)?")
    token_min = Token("min")
    unit_time = Choice(token_day, token_hour, token_min)
    # e.g 3 days or 2 h
    value_duration = Sequence(value_number, unit_time)

    part_value = Choice(value_number, string, value_boolean, value_duration)

    optional_part = Sequence(Optional(boolean_operation), identifier, Optional(part_value))

    # "Apple Pie" rating:>3 or name:"Apple"
    START = Repeat(optional_part, mi=1, ma=None)