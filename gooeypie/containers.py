from tkinter import ttk
from tkinter import filedialog
from gooeypie.error import *
import platform
import os

# Set to True to add colours to differentiate the frames and windows etc.
DEBUG = 0


class ContainerBase(ttk.Frame, ttk.LabelFrame):
    """Base class for Container and LabelContainer classes - provides functions for layout"""

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

        # For explicitly setting the size of containers
        self._preferred_container_width = 0
        self._preferred_container_height = 0

    def _init_container(self):
        """Called when a container is being added to the window (or another container) to set correct width"""

        # If the user has set preferred height/width, then calculate, otherwise it will be automatic
        if self._preferred_container_width or self._preferred_container_height:
            self.update_idletasks()
            min_width = self.winfo_reqwidth()
            min_height = self.winfo_reqheight()

            container_width = max(min_width, self._preferred_container_width)
            container_height = max(min_height, self._preferred_container_height)

            self.config(width=container_width)
            self.config(height=container_height)
            self.grid_propagate(False)

    @property
    def height(self):
        return self.cget('height')

    @height.setter
    def height(self, value):
        if type(value) != int or value < 0:
            raise ValueError(f'Height must be a positive integer')
        self._preferred_container_height = value

    @property
    def width(self):
        return self.cget('width')

    @width.setter
    def width(self, value):
        if type(value) != int or value < 0:
            raise ValueError(f'Width must be a positive integer')
        self._preferred_container_width = value

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
        """Sets the grid for the layout of all widgets, rows and columns indexed from 1
        The grid must be set before widgets can be added, all widgets must have a location specified.
        """
        # Initialise the grids with None
        self._grid = [[None for i in range(columns)] for j in range(rows)]

        # Set each column of the grid to stretch evenly when the window resizes
        for col in range(columns):
            self.columnconfigure(col, weight=1)

        for row in range(rows):
            self.rowconfigure(row, weight=1)

    def add(self, widget, row, column, **kwargs):
        """Add the given widget to the grid with arguments"""

        if type(widget) == LabelContainer:
            widget._init_container()

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

        except TypeError:
            raise GooeyPieError('The set_grid(rows, columns) function must be called before adding widgets')

        except IndexError:
            raise Exception(f'Row {row}, Column {column} is outside the bounds of the defined grid '
                            f'(Rows: {len(self._grid)}, Columns: {len(self._grid[0])})')

    def set_column_weights(self, *args):
        """Determines how the space of columns is allocated in the window or container"""
        if self._grid is None:
            raise GooeyPieError('Column weights cannot be set until set_grid() has been used to define the grid')
        if len(args) != len(self._grid[0]):
            raise ValueError(f'Number of arguments provided ({len(args)}) does not match the '
                             f'number of columns ({len(self._grid[0])})')

        for column, weight in enumerate(args):
            self.columnconfigure(column, weight=weight)

    def set_row_weights(self, *args):
        """Determines how the space of columns is allocated in the window or container"""
        if self._grid is None:
            raise GooeyPieError('Row weights cannot be set until set_grid() has been used to define the grid')
        if len(args) != len(self._grid):
            raise ValueError(f'Number of arguments provided ({len(args)}) does not match the '
                             f'number of rows ({len(self._grid)})')

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

    def __str__(self):
        return f"<Container widget>"

    def __repr__(self):
        return self.__str__()


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

    def __str__(self):
        return f"<LabelContainer \'{self.cget('text')}\'>"

    def __repr__(self):
        return self.__str__()
