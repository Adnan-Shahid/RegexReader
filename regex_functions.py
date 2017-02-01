"""
# Copyright Nick Cheng, Adnan Shahid, Brian Harrington, Danny Heap,
# 2013, 2014, 2015, 2016
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 2, CSCA48, Winter 2016
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""

# Do not change this import statement, or add any of your own!
from regextree import RegexTree, StarTree, DotTree, BarTree, Leaf

# Do not change anything above this comment except for the copyright
# statement

# Student code below this comment.


def is_regex(s):
    '''(string) -> bool
    Determines if a string is a valid regex, for a string to be a valid regex
    it must follow these rules:
    1. If the string is of length 1, it must be one of these chars
        ['0', '1', '2', 'e']
    2. If the string has a * at the end (i.e. s = r1*), it can be valid so
        long as r1 is valid
    3. if there is a | within the string (i.e. s = r1|r2) then so long as
        r1 and r2 are valid, the regex is valid
    4. All expressions that are not single chars or single chars with
        *'s must contain brackets surrounding them to be valid (the inside
        of the brackets must also be valid)

    >>> is_regex('1')
    True
    >>> is_regex('5')
    False
    >>> is_regex('1*****')
    True
    >>> is_regex('****1')
    False
    >>> is_regex('(1|2)')
    True
    >>> is_regex('1|4')
    False
    >>> is_regex('1212112')
    False
    >>> is_regex('(((1.e)|(1|2)).(0|2))*')
    True
    >>> is_regex('((1.(0|2)*).0)')
    True
    >>> is_regex('(0*|2*)')
    True
    >>> is_regex('(0*|2*')
    False
    >>> is_regex('(1**.(l|0))')
    False
    >>> is_regex('(.1)')
    False
    '''

    # valid symbols for a regex of length 1
    valid_chars = ['0', '1', '2', 'e']
    regex = True
    # case where the length of the string is 1
    if len(s) <= 1:
        # set is_regex to false if the length 1 string doesn't have a
        # valid character
        if s not in valid_chars:
            regex = False

    # case where the end is a * symbol
    elif s[-1] == '*':
        # cuts the star out and determines if the rest is valid
        regex = is_regex(s[:-1])

    # any nonempty/nonsinglechar/not star end expression must start and end
    # with a bracket
    elif s[0] == '(' and s[-1] == ')':
        # check the inside of the bracket to see if it is valid
        regex = regex_inside(s[1:-1])

    # if it isn't any of the previous cases, the regex is not valid
    else:
        regex = False

    return regex


def regex_inside(s):
    '''(string) -> bool
    Checks the inside of the brackets of s and splits the expression
    by the symbols | and ., and determines if the left side of the expression
    and the right side, as well as the symbol are valid

    >>> regex_inside('(1.(0|2)*).0')
    True

    >>> regex_inside('(1.(0|2)*).0)')
    False

    >>> regex_inside('((0*.1)|2).(e|0*)')
    True

    >>> regex_inside('((0*.1)||2).(e|0*)')
    False

    >>> regex_inside('((0*.1)||2)(e|0*)')
    False
    '''
    # a try except is used here because if the regex is not of appropriate
    # format then it will crash, and if it's not of the appropriate format
    # then it isn't a valid regex and as such, it sets it to false
    try:

        # used to find r1 | r2 or r1 . r2 where s is split with a symbol
        # finds the position of the symbol
        symbol_val = find_r(s)
        # r1 is everything up to the symbol position
        r1 = s[:symbol_val]

        # stores the value of the symbol
        symbol = s[symbol_val]

        # r2 is everything after the symbol position
        r2 = s[(symbol_val+1):]

        # determine if r1, symbol and r2 are valid regexes
        r1_valid = is_regex(r1)
        symbol_valid = is_regex(symbol)
        r2_valid = is_regex(r2)

        valid_regex = (r1_valid and symbol and r2_valid)
    except:
        valid_regex = False
    return valid_regex


def find_r(s):
    '''(string) -> int
    Iterates through a string until it approaches a symbol | or . and returns
    the location of that symbol in the string.

    REQ: s is not an empty string

    >>> find_r('1')
    1
    >>> find_r('5')
    1
    >>> find_r('1*****')
    6
    >>> find_r('****1')
    5
    >>> find_r('1|2')
    1
    >>> find_r('1|4')
    1
    >>> find_r('1212112')
    7
    >>> find_r('(((1.e)|(1|2)).(0|2))*')
    22
    >>> find_r('((1.(0|2)*).0)')
    14
    >>> find_r('(0*|2*)')
    7
    >>> find_r('0*|2*')
    2
    >>> find_r('1**.(l|0)')
    3
    >>> find_r('(.1)')
    4

    '''
    if s == '':
        count = 0
    else:
        count = 0
        # placeholder val as false until the symbol or end of r is reached
        symbol = False
        # iterate through the entire string until the symbol is found
        # or the end of the string is reached
        while count < len(s) and not symbol:
            # get the value at s[count]
            val = s[count]

            # if a symbol was reached through iteration, save val
            # and stop iterating
            if val == '|' or val == '.':
                symbol = True

            # case where a bracket is reached
            # a bracket indicates a new regex expression and must be
            # evaluated seperately, is done recursively.
            # skips to the end of the bracket
            elif val == '(':
                # get to the end of the bracket
                bracket_depth = 1
                # go past the bracket
                count += 1

                while bracket_depth != 0 and count < len(s):
                    # get the value of s[count]
                    char = s[count]
                    # if the char is a left bracket, we have increased depth
                    # of brackets, so add to depth counter
                    if char == '(':
                        bracket_depth += 1
                    # if the char is a right bracket, we have decreased depth
                    # of brackets, so decrement the depth counter
                    elif char == ')':
                        bracket_depth -= 1
                    # keep iterating
                    count += 1

            else:
                # iterate forward
                count += 1

    return count


def all_regex_permutations(s):
    '''(string) -> set of strings
    Takes a string s and produces a set of valid regex permutations of it

    >>> all_regex_permutations('(1**.2)')
    {'(1.2)**', '(2**.1)', '(1*.2*)', '(1.2**)', '(2.1)**',
    '(2*.1*)', '(1**.2)', '(1*.2)*', '(2.1**)', '(1.2*)*',
    '(2*.1)*', '(2.1*)*'}

    >>> all_regex_permutations('(1.2)')
    {'(2.1)', '(1.2)'}

    >>> all_regex_permutations('(1.(2|3*))')
    set()

    >>> all_regex_permutations('(1.2*)')
    {'(1.2)*', '(2.1*)', '(1*.2)', '(1.2*)', '(2*.1)', '(2.1)*'}

    >>> all_regex_permutations('(1**.2')
    set()

    # check large case - output length - case should say 60
    >>> len(all_regex_permutations('(1*.(1|0))'))
    60
    '''
    # valid characters for regex
    valid_chars = ['0', '1', '2', 'e']
    # base cases
    if len(s) == 0:
        # if there's nothing in the string then there are no permutations
        permutations = set()
    elif len(s) == 1:
        permutations = set()
        # if the string is a valid regex, then add it to the set
        if s in valid_chars:
            permutations.add(s)
    else:
        # variable to hold valid regexes
        permutations = set()
        # get all permutations for s
        all_permutations = perms(s)
        # determine which permutations are valid regexes
        for i in all_permutations:
            # if the string is valid then add it to the set
            if is_regex(i):
                permutations.add(i)
    return permutations


def perms(s):
    '''(string) -> set of strings
    Given a string, determines all possible permutations of the string, then
    removes all duplicates and returns the set

    >>> perms('cat')
    {'cta', 'act', 'cat', 'atc', 'tac', 'tca'}

    >>> perms('dog')
    {'odg', 'dog', 'ogd', 'god', 'gdo', 'dgo'}

    >>> perms('abcc')
    {'ccab', 'abcc', 'bcac', 'cacb', 'cbac', 'cabc',
    'acbc', 'accb', 'bcca', 'ccba', 'cbca', 'bacc'}

    >>> perms('')
    set()

    >>> perms('a')
    {'a'}

    >>> perms('abbcc')
    {'cbcba', 'cabbc', 'bcbca', 'cbcab', 'abccb', 'bcabc', 'babcc',
    'bbcca', 'bccba', 'ccbab', 'cbabc', 'abcbc', 'acbcb', 'bacbc',
    'acbbc', 'bcbac', 'bbacc', 'cabcb', 'bbcac', 'abbcc', 'ccbba',
    'cacbb', 'bcacb', 'ccabb', 'baccb', 'cbbac', 'accbb', 'bccab',
    'cbbca', 'cbacb'}

    '''
    # base case of length 1
    if len(s) <= 1:
        # set the return value
        values = [s]
    else:
        # get the first character of the string
        char = s[0]
        # variable to hold values - is a set to avoid duplicates
        values = set()
        # get every permutation of every string not including the first char
        permutations = perms(s[1:])
        # iterate through all s[1:] permutations
        for perm in permutations:
            # add the first char to every permutation
            for i in range(len(perm) + 1):
                values.add(perm[i:] + char + perm[:i])
    return values


def regex_match(r, s):
    '''(RegexTree, string) -> bool
    returns True iff the string s matches the regular expression tree
    rooted at r

    >>> regex_match(build_regex_tree('2'), '2')
    True
    >>> regex_match(build_regex_tree('(0.1)'), '01')
    True
    >>> regex_match(build_regex_tree('((2.(1|0)*).0)'), '20110010')
    True
    >>> regex_match(build_regex_tree('((2.(1|0)*).0)'), '20')
    True
    >>> regex_match(build_regex_tree('((2.(1|0)*).0)'), '21')
    False
    >>> regex_match(build_regex_tree('((2.(1|0)*).0)'), '122')
    False
    >>> regex_match(build_regex_tree('(0|1)'), '1')
    True

    '''
    # start match as true
    match = True

    # base case
    if r.get_children() == []:
        # if it's a leaf node, check if the symbol matches the string
        match = (r.get_symbol() == s)

    elif r.get_symbol() == '*':
        # case where string is empty
        if s == '':
            # if the string is empty, any case with a star is automatically
            # true as a star either means s1...sk or ''
            match = True

        elif r.get_child().get_symbol() == '|':
            # case with bar as child of the star
            i = 0
            # check all string values and compare it to the left and right
            # child of the |
            while i < len(s) and match:
                match = (regex_match(r.get_child().get_children()[0], s[i]) or
                         regex_match(r.get_child().get_children()[1], s[i]))
                # iterate forward
                i += 1

        else:
            # case for when the star represents s1....sk
            # get the repeated character
            repeated = repetition(s)
            # determine if the symbol matches the repeated char and
            # returns true if so
            match = regex_match(r.get_child(), repeated)

    elif r.get_symbol() == '|':
        # case for bar
        # determine if the string matches either the left or right child
        # as the | symbol dictates
        match = (regex_match(r.get_children()[1], s) or
                 regex_match(r.get_children()[0], s))

    elif r.get_symbol() == '.':
        # case for .
        # variable for the counter
        i = 0
        # preset the match val to false
        match = False
        # iterate through all values of s
        while i < len(s):
            # check if the length of s matches  the left child
            # and then compares the right side with the string
            # saves the location where it sotps matching
            # doesnt not recurse if match is true
            if not match:
                # there are special cases if the left and right child are
                # star trees
                # if the left child is a Star tree
                if (len(s) == 1 and
                        r.get_children()[0].get_symbol() == '*'):
                    # if s is 1 char long then and the left child is a startree
                    # s1 has to be '' and s2 has to be s
                    match = (regex_match(r.get_children()[0], '') and
                             regex_match(r.get_children()[1], s))
                # elif the right child is a Star tree
                elif (len(s) == 1 and
                        r.get_children()[1].get_symbol() == '*'):
                    # if the string is 1 character long, and the
                    # and the right child is a stee
                    # s2 has to be '' and s1 has to be s
                    match = (regex_match(r.get_children()[0], s) and
                             regex_match(r.get_children()[1], ''))
                else:
                    # case where a child isn't a star tree
                    # checking both sides so long as it doesnt match
                    match = (regex_match(r.get_children()[0], s[:i]) and
                             regex_match(r.get_children()[1], s[i:]))
            # incrementing counter
            i += 1
    else:
        # doesn't work for operators that aren't valid
        match = False

    return match


def repetition(s):
    '''(string) -> string
    Given a string, determines what substring of the string is being repeated
    and returns that value

    REQ: the string is not empty

    >>> repetition('11111')
    '1'
    >>> repetition('111110')
    111110
    >>> repetition('00000')
    '0'
    repetition('1010101010')
    '10'

    '''
    # var to store the repeated chars
    repeated = ''
    # iterate through the string
    for i in s:
        # add i to the repeated chars as it has been used once
        repeated += i
        if len(s) % len(repeated) == 0:
            # determine if the repeated char * the length of s
            # actually makes s
            # if it does, returns it
            if (len(s) // len(repeated)) * repeated == s:
                return repeated


def build_regex_tree(regex):
    '''(string) -> RegexTree
    given a valid regular expression string regex, creates the corresponding
    regex tree and returns the root

    REQ: regex is a valid regular expression

    >>> build_regex_tree('(1|2)')
    BarTree(Leaf('1'), Leaf('2'))
    >>> build_regex_tree('1')
    Leaf('1')
    >>> build_regex_tree('1*')
    StarTree(Leaf('1'))
    >>> build_regex_tree('(1.2)')
    DotTree(Leaf('1'), Leaf('2'))
    >>> build_regex_tree('(1|2)*')
    StarTree(BarTree(Leaf('1'), Leaf('2')))
    >>> build_regex_tree('((1|2)*.0)')
    DotTree(StarTree(BarTree(Leaf('1'), Leaf('2'))), Leaf('0'))

    >>> build_regex_tree("(((1*.2)|0).(e|1*))")
    DotTree(BarTree(DotTree(StarTree(Leaf('1')), Leaf('2')), Leaf('0')),
    BarTree(Leaf('e'), StarTree(Leaf('1'))))

    '''
    # base case
    if len(regex) == 1:
        # assuming all valid regexes, if the length is 1, the regex must be
        # a possible leaf node of 0,1,2 or e
        tree = Leaf(regex)

    elif regex[-1] == '*':
        # create a star tree then evaluate the rest of the regex
        # not including the star
        tree = StarTree(build_regex_tree(regex[:-1]))

    else:
        # case with a binary operator
        # strip brackets
        regex = regex[1:-1]
        # find the location of the binary operator
        symbol_val = find_r(regex)
        # get the symbol of the binary operator
        symbol = regex[symbol_val]

        # if symbol is a |, create a bar tree
        if symbol == '|':
            # splice the tree with left and right children
            # left child being every val of regex up to the binary operator
            # right child being every val of regex past the binary operator
            tree = (BarTree(build_regex_tree(regex[:symbol_val]),
                            build_regex_tree(regex[symbol_val+1:])))
        # if the symbol is a ., create a dot tree
        elif symbol == '.':
            # splice the tree with left and right children
            # left child being every val of regex up to the binary operator
            # right child being every val of regex past the binary operator
            tree = (DotTree(build_regex_tree(regex[:symbol_val]),
                            build_regex_tree(regex[symbol_val+1:])))
    return tree
