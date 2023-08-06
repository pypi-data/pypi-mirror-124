'''Removes any formatting within notes in an odt or ds document.'''

# ------------------------------------------------------------------------------
import sys

from appy.bin.odfgrep import Grep

# ------------------------------------------------------------------------------
usage = '''Usage: python2 odfclean.py file.

 Updates *file*, that must be the absolute path to an odt or ods file, by
 removing any formatting within its notes.
'''

# ------------------------------------------------------------------------------
class Cleaner:
    '''Cleans notes within an ODT or ODS file'''

    def __init__(self, path):
        self.path = path

    def run(self):
        '''Does the job by (mis)using a Grep instance'''
        # Perform a silly find & replace with a Grep instance (replacing a term
        # with itself): it will also have the effect of cleaning the notes with
        # p_self.path, because it is one of the default tasks performed by Grep.
        term = 'do '
        grep = Grep(term, self.path, repl=term, zone='pod', silent=True)
        grep.run()
        if grep.cleaned:
            print '%d styled text part(s) unstyled.' % grep.cleaned
        else:
            print 'No styled text part was found within doc statements.'
        return grep.cleaned

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    if len(sys.argv) !=  2:
        print(usage)
        sys.exit(1)
    Cleaner(*sys.argv[1:]).run()
# ------------------------------------------------------------------------------
