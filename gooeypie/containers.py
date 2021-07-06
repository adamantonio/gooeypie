from tkinter import ttk
from gooeypie.error import *

# Set to True to add colours to differentiate the frames and windows etc.
DEBUG = 0


class ContainerBase(ttk.Frame, ttk.LabelFrame):
    """Abstract base class for Container and LabelContainer classes - provides functions for layout"""

    spacing = {
        'window_padding': 0,
        'widget_spacing_x': [8, 8],
        'widget_spacing_y': [8, 8]
    }

    tk_align_mappings = {
        'left': 'w',
        'center': '',
        'right': 'e'
    }

    tk_valign_mappings = {
        'top': 'n',
        'middle': '',
        'bottom': 's'
    }

    def __init__(self, master, text=None):
        """Depending on whether text is specified, the container is either a ttk.Frame or a ttk.LabelFrame"""
        if text:
            ttk.LabelFrame.__init__(self, master, text=text)
        else:
            ttk.Frame.__init__(self, master)

        self._grid = None
        self.margins = ['auto', 'auto', 'auto', 'auto']  # top, right, bottom, left

    @property
    def height(self):
        return self.cget('height')

    @height.setter
    def height(self, value):
        if type(value) != int or value < 0:
            raise ValueError(f'Height must be a positive integer')
        self.config(height=value)
        self.grid_propagate(False)

    # TODO: add property for width, check for type properly, try to avoid widths that are too small

    @property
    def margin_top(self):
        return self.margins[0]

    @margin_top.setter
    def margin_top(self, value):
        self.margins[0] = value

    @property
    def margin_right(self):
        return self.margins[1]

    @margin_right.setter
    def margin_right(self, value):
        self.margins[1] = value

    @property
    def margin_bottom(self):
        return self.margins[2]

    @margin_bottom.setter
    def margin_bottom(self, value):
        self.margins[2] = value

    @property
    def margin_left(self):
        return self.margins[3]

    @margin_left.setter
    def margin_left(self, value):
        self.margins[3] = value

    def set_grid(self, rows, columns):
        """
        Sets the grid for the layout of all widgets, rows and columns indexed from 1
        The layout manager is unforgiving: the grid must be set before
        widgets can be added, all widgets must have a location specified.
        """
        # Initialise the grids with None's
        self._grid = [[None for i in range(columns)] for j in range(rows)]

        # Set each column of the grid to stretch evenly when the window resizes
        for col in range(columns):
            self.columnconfigure(col, weight=1)

        for row in range(rows):
            self.rowconfigure(row, weight=1)

    def add(self, widget, row, column, **kwargs):
        """Add the given widget to the grid with arguments"""

        # Determine the tkinter sticky property
        sticky = ''
        if kwargs.get('fill'):
            sticky += 'ew'
        if kwargs.get('stretch'):
            sticky += 'ns'
        sticky += self.tk_align_mappings[kwargs.get('align', 'left')]
        sticky += self.tk_valign_mappings[kwargs.get('valign', 'top')]

        # Column span and row span
        column_span = kwargs.get('column_span', 1)
        row_span = kwargs.get('row_span', 1)

        try:
            # TODO: use the column_span/row_span attribute to check that all widgets fit inside the given grid
            self._grid[row-1][column-1] = widget

            padx = self.spacing['widget_spacing_x'].copy()
            pady = self.spacing['widget_spacing_y'].copy()

            # If widgets are on the first and last row or column, double the spacing
            # for more consistent spacing between widgets and the window edge
            if column == 1:
                padx[0] *= 2
            if column + (column_span - 1) == len(self._grid[0]):
                padx[1] *= 2

            if row == 1:
                pady[0] *= 2
            if row + (row_span - 1) == len(self._grid):
                pady[1] *= 2

            # For a Container, set the padding on the edges to 0 or the contents will
            # appear inset compared to other widgets in the window
            # override_spacing is an ugly hacky solution so that radiobuttons don't inset in their Container
            if type(self) == Container:
                if column == 1:
                    padx[0] = 0
                if column + (column_span - 1) == len(self._grid[0]):
                    padx[1] = 0

                if row == 1:
                    pady[0] = 0
                if row + (row_span - 1) == len(self._grid):
                    pady[1] = 0

            # Margins can be overridden - currently used internally by RadioGroup
            # margin = [top, right, bottom, left]
            margins = kwargs.get('margins') or widget.margins
            if margins:
                top, right, bottom, left = margins
                if top != 'auto':
                    pady[0] = top
                if right != 'auto':
                    padx[1] = right
                if bottom != 'auto':
                    pady[1] = bottom
                if left != 'auto':
                    padx[0] = left

            widget.grid(padx=padx, pady=pady, sticky=sticky,
                        row=row-1, column=column-1, columnspan=column_span, rowspan=row_span)

        except ValueError:
            raise GooeyPieError('The set_grid(rows, columns) function must be called before adding widgets')

        except IndexError:
            raise Exception(f'Row {row}, Column {column} is outside the bounds of the defined grid '
                            f'(Rows: {len(self._grid)}, Columns: {len(self._grid[0])})')

    def set_column_weights(self, *args):
        try:
            if len(args) != len(self._grid[0]):
                raise ValueError
            for column, weight in enumerate(args):
                self.columnconfigure(column, weight=weight)
                # print(f'self.columnconfigure({column}, weight={weight})')

        except ValueError:
            raise ValueError(f'Number of arguments provided ({len(args)}) does not match the '
                             f'number of columns ({len(self._grid[0])})')
        except TypeError:
            raise TypeError('Column weights cannot be set until set_grid() has been used to define the grid')

    def set_row_weights(self, *args):
        """
        As above - need to do some checks and balances. Might be better
        to split out to a separate function
        """
        for row, weight in enumerate(args):
            self.rowconfigure(row, weight=weight)


class Container(ContainerBase):
    """Transparent frame that other widgets can be placed in"""
    def __init__(self, master):
        ContainerBase.__init__(self, master)

        if DEBUG:
            import random
            rand_style = f'MyStyle{random.randrange(100, 999)}.TFrame'
            bg_col = random.choice(('red', 'blue', 'green', 'grey', 'orange'))
            s = ttk.Style()
            s.configure(rand_style, background=bg_col)
            print(f'Container is {bg_col}')
            ttk.Frame.__init__(self, master, style=rand_style)
        else:
            ttk.Frame.__init__(self, master)


class LabelContainer(ContainerBase):
    """Labeled frame that other widgets can be placed in"""
    def __init__(self, master, text):
        ContainerBase.__init__(self, master, text)

        if DEBUG:
            import random
            rand_style = f'MyStyle{random.randrange(100, 999)}.TFrame'
            bg_col = random.choice(('red', 'blue', 'green', 'grey', 'orange'))
            s = ttk.Style()
            s.configure(rand_style, background=bg_col)
            print(f'LabelContainer is {bg_col}')
            ttk.LabelFrame.__init__(self, master, text=text, style=rand_style)
        else:
            ttk.LabelFrame.__init__(self, master, text=text)
