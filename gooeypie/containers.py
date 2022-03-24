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
        """Gets or sets the height of the container as an integer in pixels"""
        return self.cget('height')

    @height.setter
    def height(self, value):
        if type(value) != int or value < 0:
            raise ValueError(f'Height must be a positive integer')
        self._preferred_container_height = value

    @property
    def width(self):
        """Gets or sets the height of the container as an integer in pixels"""
        return self.cget('width')

    @width.setter
    def width(self, value):
        if type(value) != int or value < 0:
            raise ValueError(f'Width must be a positive integer')
        self._preferred_container_width = value

    @property
    def margin_top(self):
        """Gets or sets the top margin of the container"""
        return self.margins[0]

    @margin_top.setter
    def margin_top(self, value):
        self.margins[0] = value

    @property
    def margin_right(self):
        """Gets or sets the right margin of the container"""
        return self.margins[1]

    @margin_right.setter
    def margin_right(self, value):
        self.margins[1] = value

    @property
    def margin_bottom(self):
        """Gets or sets the bottom margin of the container"""
        return self.margins[2]

    @margin_bottom.setter
    def margin_bottom(self, value):
        self.margins[2] = value

    @property
    def margin_left(self):
        """Gets or sets the left margin of the container"""
        return self.margins[3]

    @margin_left.setter
    def margin_left(self, value):
        self.margins[3] = value

    def set_grid(self, rows, columns):
        """Defines the dimensions of the grid for the layout of all widgets

        The grid must be defined before any widgets can be added, rows and columns are numbered from 1.

        Args:
            rows (int): The number of rows of the container
            columns (int):  The number of columns of the container
        """
        # Initialise the grids with None
        self._grid = [[None for i in range(columns)] for j in range(rows)]

        # Set each column of the grid to stretch evenly when the window resizes
        for col in range(columns):
            self.columnconfigure(col, weight=1)
        for row in range(rows):
            self.rowconfigure(row, weight=1)

    def add(self, widget, row, column, **kwargs):
        """Add a widget to the container

        Args:
            widget: The GooeyPieWidget or container being added
            row (int): The row the widget is being added to
            column (int): The column the widget is being added to
            kwargs: Layout options for the widget/container being added

        Raises:
            GooeyPieError: If the grid has not been defined with a call to set_grid()
            # TODO TypeError: If widget is not a valid GooeyPieWidget
            TypeError: If row and column are not positive integers
            ValueError: If the row or column specified is outside the bounds of the grid, or the row_span and
                column_span specified exceed the grid size
        """
        # Dictionary for all settings related to calling tkinter's .grid() method
        grid_settings = {'row': row - 1, 'column': column - 1}

        # Check that widget is a valid GooeyPieWidget or Container
        # TODO: This won't work until containers.py and widgets.py are consolidated
        # if not isinstance(widget, (GooeyPieWidget, ContainerBase)):
        #     raise TypeError('Not a valid widget or Container')

        # Check that the grid has been defined
        if self._grid is None:
            raise GooeyPieError('The set_grid(rows, columns) function must be called before adding widgets')

        # Check that row and column are integers
        if type(row) != int or type(column) != int or row < 1 or column < 1:
            raise TypeError('row and column must be positive integers')

        total_rows = len(self._grid)
        total_columns = len(self._grid[0])

        # Check that row and column are valid for the set grid
        if row > total_rows or column > total_columns:
            raise ValueError(f'Row {row}, Column {column} is outside the bounds of the defined grid '
                             f'({total_rows} rows, {total_columns} columns)')

        # Check that the row and column is not occupied
        # TODO: Use self.get_widget when that gets written
        cell_contents = self._grid[row - 1][column - 1]
        if cell_contents is not None:
            raise ValueError(f'Cannot add {widget} to row {row}, column {column} as it is currently occupied by'
                             f' {cell_contents}')

        # Get row span and column span
        row_span = kwargs.get('row_span', 1)
        column_span = kwargs.get('column_span', 1)

        # Check that the row span and column span don't extend beyond the limits of the grid
        if row + row_span - 1 > total_rows:
            raise ValueError(f'Cannot add {widget}. The row span specified causes the widget to extend beyond the '
                             f'bounds of the grid.')
        if column + column_span - 1 > total_columns:
            raise ValueError(f'Cannot add {widget}. The column span specified causes the widget to extend beyond the '
                             f'bounds of the grid.')

        # Add row span and column span to grid settings
        grid_settings['rowspan'] = row_span
        grid_settings['columnspan'] = column_span

        # If it's a container being added, initialise the container first to set any set width and height
        if isinstance(widget, ContainerBase):
            widget._init_container()

        # Determine if fill and stretch properties have been set
        grid_settings['sticky'] = ''
        if kwargs.get('fill'):
            grid_settings['sticky'] += 'ew'
        if kwargs.get('stretch'):
            grid_settings['sticky'] += 'ns'

        # Determine alignment to top/bottom and left/right if fill/stretch is not set
        if 'ew' not in grid_settings['sticky']:
            grid_settings['sticky'] += self.tk_align_mappings[kwargs.get('align', 'left')]
        if 'ns' not in grid_settings['sticky']:
            grid_settings['sticky'] += self.tk_valign_mappings[kwargs.get('valign', 'top')]

        # Default margins
        margin_horizontal = self.spacing['widget_spacing_x'].copy()
        margin_vertical = self.spacing['widget_spacing_y'].copy()

        # If widgets are on the first and last row or column, double the margins for more consistent spacing
        # between widgets and the window edge
        if row == 1:
            margin_vertical[0] *= 2
        if row + (row_span - 1) == total_rows:
            margin_vertical[1] *= 2

        if column == 1:
            margin_horizontal[0] *= 2
        if column + (column_span - 1) == total_columns:
            margin_horizontal[1] *= 2

        # For a plain Container, set the margin on the edges of each widget to 0 or the contents of the Container
        # will appear inset compared to other widgets in the window
        if type(self) == Container:
            if row == 1:
                margin_vertical[0] = 0
            if row + (row_span - 1) == total_rows:
                margin_vertical[1] = 0

            if column == 1:
                margin_horizontal[0] = 0
            if column + (column_span - 1) == total_columns:
                margin_horizontal[1] = 0

        # Determine any margins or use the default
        margins = kwargs.get('margins') or widget.margins  # margin = [top, right, bottom, left]
        if margins:
            top, right, bottom, left = margins
            if top != 'auto':
                margin_vertical[0] = top
            if right != 'auto':
                margin_horizontal[1] = right
            if bottom != 'auto':
                margin_vertical[1] = bottom
            if left != 'auto':
                margin_horizontal[0] = left

        # Add margins to grid settings dict
        grid_settings['padx'] = margin_horizontal
        grid_settings['pady'] = margin_vertical

        # Determine any padding
        padding = getattr(widget, '_padding', None)
        if padding:
            grid_settings['ipadx'] = padding[0]
            grid_settings['ipady'] = padding[1]

        # Use the row span and column span properties to populate all applicable cells in the internal grid
        for i in range(row, row + row_span):
            for j in range(column, column + column_span):
                self._grid[i - 1][j - 1] = widget

        widget.grid(**grid_settings)

    def get_widget(self, row, column):
        """Returns the widget at the given location in the grid"""
        if type(row) != int or type(column) != int:
            raise TypeError('row and column must be integers')
        if row not in range(1, len(self._grid) + 1):
            raise ValueError(f'row value must be an integer between 1 and {len(self._grid) + 1}')
        if column not in range(1, len(self._grid[0]) + 1):
            raise ValueError(f'column value must be an integer between 1 and {len(self._grid[0]) + 1}')
        return self._grid[row - 1][column - 1]

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
    def __init__(self, window):
        """Create a new Container

        Args:
            window: The window or container the label container is being added to
        """
        ContainerBase.__init__(self, window)

        if DEBUG:
            import random
            rand_style = f'MyStyle{random.randrange(100, 999)}.TFrame'
            bg_col = random.choice(('red', 'blue', 'green', 'grey', 'orange'))
            s = ttk.Style()
            s.configure(rand_style, background=bg_col)
            print(f'Container is {bg_col}')
            ttk.Frame.__init__(self, window, style=rand_style)
        else:
            ttk.Frame.__init__(self, window)

    def __str__(self):
        return f"<Container widget>"

    def __repr__(self):
        return self.__str__()


class LabelContainer(ContainerBase):
    """Labeled frame that other widgets can be placed in"""
    def __init__(self, window, text):
        """Create a new LabelContainer with caption

        Args:
            window: The window or container the label container is being added to
            text (str): The caption that appears on the LabelContainer
        """
        ContainerBase.__init__(self, window, text)

        if DEBUG:
            import random
            rand_style = f'MyStyle{random.randrange(100, 999)}.TFrame'
            bg_col = random.choice(('red', 'blue', 'green', 'grey', 'orange'))
            s = ttk.Style()
            s.configure(rand_style, background=bg_col)
            print(f'LabelContainer is {bg_col}')
            ttk.LabelFrame.__init__(self, window, text=text, style=rand_style)
        else:
            ttk.LabelFrame.__init__(self, window, text=text)

    def __str__(self):
        return f"<LabelContainer \'{self.cget('text')}\'>"

    def __repr__(self):
        return self.__str__()
