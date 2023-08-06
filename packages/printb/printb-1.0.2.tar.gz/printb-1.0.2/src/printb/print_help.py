import sys
from bidi.algorithm import get_display

# variable length print, the string constants are adjusted for bidi.
# an unrelated editor is that vs code doesn't support bidi.
# the workaround is to put bidi text into separate string variables.


#not entirely sure, if we need to swap each element seperately...
def printb(*args, sep=' ', end='\n', file=sys.stdout, flush=False):
    #lst = reversed( list( map( lambda arg  : get_display(arg) if isinstance(arg, str) else str(arg), args) ) )
    lst = reversed( list( map( lambda arg : get_display(str(arg)), args) ) )
    print( ' '.join( lst ), sep=sep, end=end, file=file, flush=flush)

#def printb(*args, sep=' ', end='\n', file=sys.stdout, flush=False):
#    print( get_display( ' '.join(map(str, args))), sep=sep, end=end, file=file, flush=flush)
#

def inputb(prompt=''):
    printb( prompt ,end="", flush=True)
    return input()
