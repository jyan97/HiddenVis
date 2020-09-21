# Consider a sequence consisting of the numbers 1, .., n,
# in some order, with n even and at least equal to 4.
# As an example, take the sequence 1, 3, 4, 2, 5, 6.
#
# View the sequence as alternating between x and y coordinates,
# starting with x:
#  1  3  4  2  5  6 
#  x  y  x  y  x  y
#
# Two successive numbers in the sequence, the first one being the
# successor of the last one by wrapping around, then define n points,
# each given by its x and y coordinates:
# (1, 3), (4, 3), (4, 2), (5, 2), (5, 6), (1, 6)
#
# We want to draw line segments that connect 2 successive points,
# the first one being the successor of the last one by wrapping around,
# so n lines segments altogether:
# (1, 3) -- (4, 3)
# (4, 3) -- (4, 2)
# (4, 2) -- (5, 2)
# (5, 2) -- (5, 6)
# (5, 6) -- (1, 6)
# (1, 6) -- (1, 3)
#
# Reading x coordinates from left to right and y coordinates from
# top to bottom, these line segments should be drawn as follows:
#     .  1 . 2 . 3  . 4 . 5 . 6 .
#   . ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
#   1 ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
#   . ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
#   2 ⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬜⬜⬜
#   . ⬜⬜⬜⬜⬜⬜⬜⬛⬜⬛⬜⬜⬜
#   3 ⬜⬛⬛⬛⬛⬛⬛⬛⬜⬛⬜⬜⬜
#   . ⬜⬛⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜
#   4 ⬜⬛⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜
#   . ⬜⬛⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜
#   5 ⬜⬛⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜
#   . ⬜⬛⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜
#   6 ⬜⬛⬛⬛⬛⬛⬛⬛⬛⬛⬜⬜⬜
#   . ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
#
# So we have to draw 2n+1 lines of 2n+1 white and black squares.
#
# You can assume that f is provided as argument the integers
# 1, ..., n, in some order, for some even n at least equal to 4. 


def f(*L):
    '''
    >>> f(1, 3, 4, 2, 5, 6)
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬛⬜⬛⬜⬜⬜
    ⬜⬛⬛⬛⬛⬛⬛⬛⬜⬛⬜⬜⬜
    ⬜⬛⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜
    ⬜⬛⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜
    ⬜⬛⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜
    ⬜⬛⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜
    ⬜⬛⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜
    ⬜⬛⬛⬛⬛⬛⬛⬛⬛⬛⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
    >>> f(1, 2, 3, 4)
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬛⬛⬛⬛⬛⬜⬜⬜
    ⬜⬛⬜⬜⬜⬛⬜⬜⬜
    ⬜⬛⬜⬜⬜⬛⬜⬜⬜
    ⬜⬛⬜⬜⬜⬛⬜⬜⬜
    ⬜⬛⬛⬛⬛⬛⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜
    >>> f(4, 3, 2, 1)
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬛⬛⬛⬛⬛⬜
    ⬜⬜⬜⬛⬜⬜⬜⬛⬜
    ⬜⬜⬜⬛⬜⬜⬜⬛⬜
    ⬜⬜⬜⬛⬜⬜⬜⬛⬜
    ⬜⬜⬜⬛⬛⬛⬛⬛⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜
    >>> f(1, 3, 2, 4)
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬛⬛⬛⬜⬜⬜⬜⬜
    ⬜⬛⬜⬛⬜⬜⬜⬜⬜
    ⬜⬛⬛⬛⬜⬜⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜
    >>> f(3, 1, 2, 6, 4, 5)
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬛⬜⬛⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬛⬜⬛⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬛⬜⬛⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬛⬜⬛⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬛⬜⬛⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬛⬜⬛⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬛⬜⬛⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬛⬜⬛⬛⬛⬜⬜⬜⬜⬜
    ⬜⬜⬜⬛⬜⬜⬜⬛⬜⬜⬜⬜⬜
    ⬜⬜⬜⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
    >>> f(1, 3, 6, 5, 4, 2)
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬛⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜
    ⬜⬛⬜⬜⬜⬜⬜⬛⬜⬜⬜⬜⬜
    ⬜⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬜
    ⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜⬛⬜
    ⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜⬛⬜
    ⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜⬛⬜
    ⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
    '''
    black_square = '\N{Black Large Square}'
    white_square = '\N{White Large Square}'
    # INSERT YOUR CODE HERE


            
if __name__ == '__main__':
    import doctest
    doctest.testmod()
