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

            # For a container, set the padding on the edges to 0 or the contents will
            # appear inset compared to other widgets in the window
            # override_spacing is an ugly hacky solution so that radiobuttons don't inset in their Container
            if type(self) == Container or kwargs.get('override_spacing'):
                if column == 1:
                    padx[0] = 0
                if column + (column_span - 1) == len(self._grid[0]):
                    padx[1] = 0

                if row == 1:
                    pady[0] = 0
                if row + (row_span - 1) == len(self._grid):
                    pady[1] = 0

            # Will check here for spacing args - e.g. kwargs.get('spacing_x'):
            # Actually I should use that to set defaults above

            widget.grid(padx=padx, pady=pady, sticky=sticky,
                        row=row-1, column=column-1, columnspan=column_span, rowspan=row_span)

        except ValueError:
            raise Exception('The set_grid(rows, columns) function must be called before adding widgets')

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

        # if DEBUG:
        #     import random
        #     rand_style = f'MyStyle{random.randrange(100, 999)}.TFrame'
        #     bg_col = random.choice(('red', 'blue', 'green', 'grey', 'orange'))
        #     s = ttk.Style()
        #     s.configure(rand_style, background=bg_col)
        #     print(f'Container is {bg_col}')
        #     ttk.Frame.__init__(self, master, style=rand_style)
        # else:
        #     ttk.Frame.__init__(self, master)


class LabelContainer(ContainerBase):
    """Labeled frame that other widgets can be placed in"""
    def __init__(self, master, text):
        ContainerBase.__init__(self, master, text)

        # if DEBUG:
        #     import random
        #     rand_style = f'MyStyle{random.randrange(100, 999)}.TFrame'
        #     bg_col = random.choice(('red', 'blue', 'green', 'grey', 'orange'))
        #     s = ttk.Style()
        #     s.configure(rand_style, background=bg_col)
        #     print(f'LabelContainer is {bg_col}')
        #     ttk.LabelFrame.__init__(self, master, text=text, style=rand_style)
        # else:
        #     ttk.LabelFrame.__init__(self, master, text=text)
