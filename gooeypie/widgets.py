import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import font
from functools import partial
from PIL import Image as PILImage, ImageTk
import platform
import datetime
import calendar
import re

if platform.system() == 'Windows':
    OS = 'Windows'
elif platform.system() == 'Darwin':
    OS = 'Mac'
elif platform.system() == 'Linux':
    OS = 'Linux'
else:
    OS = 'Other'


class GooeyPieError(Exception):
    pass


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

        # Set tabs to display at their implicit size by setting the last row/column to weight of 1,
        # since there might be additional space due to the size of other tabs.
        if isinstance(self, Tab):
            column_weights = (0,) * (columns - 1) + (1,)
            row_weights = (0,) * (rows - 1) + (1,)
            self.set_column_weights(*column_weights)
            self.set_row_weights(*row_weights)

    def add(self, widget, row, column, **kwargs):
        """Add a widget to the container

        Args:
            widget: The GooeyPieWidget or container being added
            row (int): The row the widget is being added to
            column (int): The column the widget is being added to
            kwargs: Layout options for the widget/container being added

        Raises:
            GooeyPieError: If the grid has not been defined with a call to set_grid()
            TypeError: If widget is not a valid GooeyPieWidget
            TypeError: If row and column are not positive integers
            ValueError: If the row or column specified is outside the bounds of the grid, or the row_span and
                column_span specified exceed the grid size
        """
        # Dictionary for all settings related to calling tkinter's .grid() method
        grid_settings = {'row': row - 1, 'column': column - 1}

        # if isinstance(widget, TabContainer):
        #     widget.grid(row=0, column=0, sticky='nsew')
        #     return

        # Check that widget is a valid GooeyPieWidget or Container
        if not isinstance(widget, (GooeyPieWidget, ContainerBase, ttk.Radiobutton, TabContainer)):
            raise TypeError(f'Could not add {repr(widget)} as it is not a valid GooeyPie widget or Container')

        # Date selectors need to be initialised
        if isinstance(widget, Date):
            widget._init_date_container()

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

        # Set the fill and stretch properties of separators automatically
        if isinstance(widget, Separator):
            grid_settings['sticky'] = ''
            if widget._orientation == 'horizontal':
                grid_settings['sticky'] += 'ew'
            else:
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

        # If widget.hide() has been called prior to app.run(), immediately ungrid
        if getattr(widget, '_start_hidden', False):
            widget.grid_remove()
        else:
            # Re-grid but only if the widget has already been hidden once
            if hasattr(widget, '_start_hidden'):
                widget.grid()

    def get_widget(self, row, column):
        """Returns the widget at the given location in the grid

        Args:
            row (int): the row number of the grid
            column (int): the column number of the grid

        Raises:
            TypeError: the row or column are not integers
            ValueError: the row or column and outside the bounds of the current grid
        """
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

    def disable_all(self):
        """Disables all widgets in a container"""

        # This might be the hackiest part of the entire codebase. Windows and the main app inherit from Container,
        # but their contents cannot be accessed like container widgets are as the call to winfo_children() fails.
        # It is also not possible to check for WindowBase types here as they are defined in __init__.py
        if str(self).startswith('<GooeyPieApp') or str(self).startswith('<Window'):
            widgets = self.children.values()
            # Disable each top level menu
            top_level_menus = [menu for menu in self._menu if type(menu) == str]  # top level menus only
            for menu in top_level_menus:
                self.disable_menu(menu)

        else:
            widgets = self.winfo_children()
            self.state(['disabled'])  # Disables the container (for LabelContainer text and border)

        for widget in widgets:
            if isinstance(widget, GooeyPieWidget):
                widget.disabled = True
            elif isinstance(widget, ContainerBase):
                widget.disable_all()

    def enable_all(self):
        """Enables all widgets in a container"""
        if str(self).startswith('<GooeyPieApp') or str(self).startswith('<Window'):
            widgets = self.children.values()
            # Enable each top level menu
            top_level_menus = [menu for menu in self._menu if type(menu) == str]  # top level menus only
            for menu in top_level_menus:
                self.enable_menu(menu)

        else:
            widgets = self.winfo_children()
            self.state(['!disabled'])  # Enables the container (for LabelContainer text and border)

        for widget in widgets:
            if isinstance(widget, GooeyPieWidget):
                widget.disabled = False
            elif isinstance(widget, ContainerBase):
                widget.enable_all()


class Container(ContainerBase):
    """Transparent frame that other widgets can be placed in"""
    def __init__(self, window):
        """Create a new Container

        Args:
            window: The window or container the label container is being added to
        """
        ContainerBase.__init__(self, window)

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

    def __str__(self):
        return f"<LabelContainer \'{self.cget('text')}\'>"

    def __repr__(self):
        return self.__str__()


class TabContainer(ttk.Notebook):
    """"""
    def __init__(self, window):
        """Create a new TabContainer

        Args:
            window: the window or container the TabContainer is being added to
        """
        ttk.Notebook.__init__(self, window)

        # Give the tab titles a bit more breathing room
        style = ttk.Style()
        current_theme = style.theme_use()
        style.theme_settings(current_theme, {"TNotebook.Tab": {"configure": {"padding": [8, 4]}}})

        # Internal list of all Tab objects as a 2-tuple (window name, Tab object) added to the container
        self._tabs = []

        # Store the last selected tab so that it can be focused when the Tab Container is enabled
        self._last_selected_tab = None

        # Outer margins of the container
        self.margins = ['auto', 'auto', 'auto', 'auto']  # top, right, bottom, left

        # Keep track of the currently selected tab
        self.bind('<<NotebookTabChanged>>', self._set_last_selected_index)

    def _set_last_selected_index(self, e):
        """Sets the index of the tab most recently selected Tab.
        Used to restore the last selected tab when enabling all"""
        for window_name, tab in self._tabs:
            if window_name == super().select():
                self._last_selected_tab = tab

    def __str__(self):
        return f"<TabContainer widget>"

    def __repr__(self):
        return self.__str__()

    @property
    def selected(self):
        """Gets the currently selected Tab object"""
        for window_name, tab in self._tabs:
            if self.select() == window_name:
                return tab

    @property
    def width(self):
        """Gets or sets the preferred width of the TabContainer. The actual width may be larger
        if the width of the contents exceed this value"""

        # Note - this returns the set width, not necessarily the actual width
        return self.cget('width')

    @width.setter
    def width(self, value):
        if type(value) != int or value < 1:
            raise ValueError(f'Width must be a positive integer')
        self.configure(width=value)

    @property
    def height(self):
        """Gets or sets the height of the container as an integer in pixels. The actual height may be larger
        if the height of the contents exceed this value"""

        # Note - this returns the set height, not necessarily the actual width
        return self.cget('height')

    @height.setter
    def height(self, value):
        if type(value) != int or value < 0:
            raise ValueError(f'Height must be a positive integer')
        self.configure(height=value)

    @property
    def disabled(self):
        """Gets or sets the state of the widget

        Disabled TabContainers show all tabs but not their contents. When disabled is set to False, all hidden
        tabs will be shown and the last selected tab will be selected
        """
        return not all([tab.disabled for tab in self.tabs])

    @disabled.setter
    def disabled(self, value):
        for tab in self.tabs:
            tab.disabled = bool(value)
        if not value:
            self._last_selected_tab.select()

    @property
    def tabs(self):
        """Gets a list of all tab objects in the tab container"""
        return list(tab[1] for tab in self._tabs)

    def add(self, tab):
        """Adds a new tab to the TabContainer"""

        if not isinstance(tab, Tab):
            raise ValueError(f"Only Tab objects can be added to a TabContainer. Got type '{type(tab)}'.")

        # Add tab to ttk.Notebook
        super().add(tab, text=tab._title, compound='left')

        # This method is used to both initially add a tab or show it if tab if it has been hidden
        # The presence of a tabs _id indicates whether it has already been added or not
        if tab._id is None:

            tab._id = len(self.tabs)  # Set tabId according to the order the Tab was added
            self._tabs.append((str(tab), tab))

            # Add icon if there is one
            if tab._icon:
                self.tab(tab._id, image=tab._icon)

            # Ensure that the width of the TabContainer is large enough for the contents
            self.update_idletasks()
            self.width = max(self.width, tab.winfo_reqwidth())
            self.height = max(self.height, tab.winfo_reqheight())


class Tab(ContainerBase):
    """Frame for adding to a TabContainer"""
    def __init__(self, tab_container, title, icon=None):
        """Create a new Tab with title

        Args:
            tab_container: The tab_container
            title (str): The text on the tab
            icon (str): The path and filename of an image to use as the tab icon
        """

        if not isinstance(tab_container, TabContainer):
            raise TypeError(f"A tab can only be added to a TabContainer object. Got type '{type(tab_container)}'.")

        self._parent = tab_container
        self._title = title

        self._icon_filename = icon
        if icon:
            self._icon = ImageTk.PhotoImage(PILImage.open(icon))
        else:
            self._icon = None

        # Tab index from 0, set when the tab is added to the tab container
        self._id = None

        ContainerBase.__init__(self, tab_container)

        # Alias the container methods enable_all and disable_all
        self.disable_contents = self.disable_all
        self.enable_contents = self.enable_all

    # Note: __str__() cannot be implemented, because the default __str__ is the window path which is required by
    # the add() method of the TabContainer class
    # def __str__(self):
    #     return f"<Tab '{self._title}'>"

    def __repr__(self):
        return f"<Tab '{self._title}'>"

    @property
    def icon(self):
        """Gets or sets the icon that appears alongside the title of the tab"""
        return self._icon_filename

    @icon.setter
    def icon(self, icon):
        if icon:
            self._icon = ImageTk.PhotoImage(PILImage.open(icon))
            self._parent.tab(self._id, image=self._icon)
            self._icon_filename = icon
        else:
            # Unresolved issue: removing an icon can take between 5-15 seconds to take effect
            # Issue present on both Windows and Mac
            self._parent.tab(self._id, image=None)
            self._icon_filename = self._icon = None

    @property
    def disabled(self):
        """Gets or sets the disabled state of the tab

        A disabled tab cannot be selected and the contents are hidden. To allow the tab to be selected but have
        the contents disabled, use the disable_all() method on the tab.

        When a selected tab is disabled, the focus will switch to the first enabled tab.
        """
        return self._parent.tab(self._id, option='state') == 'disabled'

    @disabled.setter
    def disabled(self, value):
        state = 'normal' if not value else 'disabled'
        self._parent.tab(self._id, state=state)

    def select(self):
        """Selects (brings to the front) the tab

        If the tab is disabled, enable it
        """
        if self.disabled:
            self.disabled = False
        self._parent.select(self._id)

    def hide(self):
        """Hides the tab from the TabContainer"""
        if self._id is not None:
            self._parent.hide(self._id)
        else:
            raise GooeyPieError(f'{repr(self)} cannot be hidden until it has been added to a TabContainer')

    def show(self):
        """Shows the tab from the TabContainer. Has no effect if the Tab is already visible"""
        self._parent.add(self)


class GooeyPieEvent:
    """Event objects are passed to callback functions"""

    def __init__(self, event_name, gooeypie_widget, tk_event=None, menu=None):
        """Creates a GooeyPie event object

        All event functions receive a GooeyPieEvent that includes details of the event name,
        the widget that initiated the event, the mouse position and key pressed info

        Args:
            event_name (str): The name of the event
            gooeypie_widget: The widget that initiates the event, or the window object for menu events
            tk_event(tkinter.Event): The associated tkinter event object if applicable
            menu(tuple): THe menu path of the generated event
        """
        self.event_name = event_name
        self.widget = gooeypie_widget

        if tk_event:
            # All tk events report mouse position
            self.mouse = {
                'x': tk_event.x,
                'y': tk_event.y,
                'x_root': tk_event.x_root,
                'y_root': tk_event.y_root
            }

            # Mouse events set character information to the string '??'. Set to None in this case.
            # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/key-names.html
            if tk_event.char == '??':
                self.key = None
            else:
                self.key = {
                    'key_code': tk_event.char,  # single character representing the key
                    'name': tk_event.keysym,  # a string representing the key pressed
                    'code': tk_event.keycode  # numerical keycode
                }
        else:
            self.mouse = None
            self.key = None

        # The menu path if a menu event was triggered
        self.menu = menu

    def __str__(self):
        return str({
            'event_name': self.event_name,
            'widget': self.widget,
            'mouse': self.mouse,
            'key': self.key,
            'menu': self.menu
        })

    def __repr__(self):
        return self.__str__()


class GooeyPieWidget:
    """Base class for other GooeyPie widget classes, mostly for event handling"""

    # Event names in GooeyPie mapped to their corresponding tkinter events
    _tk_event_mappings = {
        'mouse_down': '<Button-1>',
        'mouse_up': '<ButtonRelease-1>',
        'double_click': '<Double-Button-1>',
        'triple_click': '<Triple-Button-1>',
        'middle_click': '<Button-2>',
        'right_click': '<Button-3>',
        'mouse_over': '<Enter>',
        'mouse_out': '<Leave>',
        'key_press': '<Key>',
        'focus': '<FocusIn>',
        'blur': '<FocusOut>'
    }

    def __init__(self, container=None):
        """Creates a new GooeyPieWidget object

        Args:
            container(ContainerBase): The Container to which the widget is being added

        Raises:
            TypeError: If container is not a valid Container object
        """

        # Check that the container is valid
        if not isinstance(container, ContainerBase):
            raise TypeError(f'A widget can only be added to a GooeyPieApp, Window or container')

        self._container = container

        # All events initially set to None
        self._events = {event_name: None for event_name in self._tk_event_mappings.keys()}

        self._disabled = False
        self._padding = [0, 0]
        self.margins = ['auto', 'auto', 'auto', 'auto']  # top, right, bottom, left

    def _set_padding(self, horizontal, vertical):
        """Sets padding for the widget. Only exposed for certain widgets, this method exists here for error checking"""
        if type(horizontal) != int or type(vertical) != int:
            raise TypeError('Padding values must be integers')
        if horizontal < 0 or vertical < 0:
            raise ValueError('Padding values cannot be negative')

        self._padding[0] = horizontal
        self._padding[1] = vertical

    def _event(self, event_name, tk_event=None):
        """Constructs a GooeyPieEvent object and calls the registered callback

        Args:
            event_name(str): The name of the event
            tk_event(tkinter.Event): The tkinter.Event object if applicable

        Raises:
            AttributeError: If the given event_name is not an event or cannot be associated with this widget
        """
        try:
            gooeypie_event = GooeyPieEvent(event_name, self, tk_event)
            self._events[event_name](gooeypie_event)
        except KeyError:
            raise AttributeError(f"'{event_name}' listener not associated with this widget")
        except TypeError:
            raise TypeError(f"The event function {self._events[event_name].__name__}() must accept a single"
                            f" argument for the event object")

    def _slider_change_event(self, event_name, slider_value):
        """Event function for slider change events

        In tkinter, slider change events send the new value of the slider to the callback. This is ignored in
        GooeyPie but can be accessed through the passed Event object.
        """

        # The slider's change event will be called whenever a movement is detected on the widget, even if the
        # movement does not actually change the value. This checks whether or not a change has actually been made.
        if self._value.get() != self._previous_value:
            self._previous_value = self._value.get()  # Update the previous value
            self._event(event_name)

    def _number_change_event(self, event_name, tkinter_event_object):
        """For implementing a change event on change in the Number ttk.Spinbox widget"""
        self._event(event_name)

    def _text_change_event(self, event_name, a, b, c):
        """To implement the change event for the Input widget

        For the ttk.Entry widget, a trace must be added to the variable associated with the Input.
        The trace command sends 3 arguments to the callback. These are ignored in GooeyPie.
        """
        self._event(event_name)

    def _textbox_change_event(self, event_name, key_code):
        """To implement the change event on the Textbox widget

        For the tkinter.ScrolledText widget, the <KeyRelease> event is bound to this method, which checks if the
        contents of the widget have changed by interrogating the sentinel StringVar associated with it.

        Note: <KeyRelease> is not exposed as a GooeyPie event, so no clashes are possible with other events.
        """
        if self.text != self._sentinel.get():
            # Only process the event if the key release was a change in content, thus ignoring modifier keys etc
            self._sentinel.set(self.text)
            self.text = self._sentinel.get()  # just in case
            self._event(event_name)

    def _newtextbox_change_event(self, key_code):
        """This event function is always set when a textbox is created, performing two functions:
        1. Updates the scrollbar visibility if it is set to 'auto'
        2. Handles the 'change' event if it has been set by the user
        """

        # Update the scrollbar if required
        if self._scrollbar_visibility == 'auto':
            self._update_scrollbar()

        # If the user has set a change event, process the event
        if self._events['change']:
            # But only if the text has actually changed (i.e. ignore modifier keys)
            if self.text != self._sentinel:
                self._sentinel = self.text
                self._event('change')

    def _date_change_event(self, event):
        """To implement the change event on the Date widget.

        This event function is called independently of whether a 'change' event has been registered. This
        is so that the dropdowns are updated to reflect the correct number of days in that month
        """
        # With every change to any selector, update the day selector
        self._update_day_select()

        # If the user has defined a 'change' event function, call the event function
        # but only if there is an actual date
        if self._events['change'] and self.date is not None:
            self._event('change')

    def add_event_listener(self, event_name, event_function):
        """Registers an event function to respond to an event

        Args:
            event_name(str): The name of the event that will trigger the function.
            event_function(function): The function called when the event is triggered

        Raises:
            ValueError: The given event_name is not an event or cannot be associated with this widget
            TypeError: The event_function is not a function
            ValueError: The event_function does not accept a single argument
            GooeyPieError: A Hyperlink widget is assigned the mouse_down or mouse_over event
        """

        # Check that the event is valid for the given widget
        if event_name not in self._events:
            raise ValueError(f"The event '{event_name}' is not valid for widget {self}")

        # Check that the callback is a function
        if not callable(event_function):
            raise TypeError(f"The second argument does not appear to be the name of a function. "
                            f"Remember, no brackets - you don't want to *call* the function")

        # Hyperlinks have default events for mouse_down (activating the link)
        # and mouse_over (showing a hand icon) which cannot be overridden
        if isinstance(self, Hyperlink):
            if event_name in ('mouse_down', 'mouse_over'):
                raise GooeyPieError(f"The '{event_name}' event cannot be associated with a Hyperlink")

        # Store the callback function in the widgets events dictionary
        self._events[event_name] = event_function

        # Events in self._tk_event_mappings are associated with the bind() method
        if event_name in self._tk_event_mappings:
            if isinstance(self, (Table, Listbox)):
                # Bind the event to the treeview part of the Table & Listbox widgets
                self._treeview.bind(self._tk_event_mappings[event_name], partial(self._event, event_name))

            elif isinstance(self, Textbox):
                # Bind the event to the textbox part of the Textbox widget (ignore scrollbar)
                self._tk_text_widget.bind(self._tk_event_mappings[event_name], partial(self._event, event_name))

            else:
                self.bind(self._tk_event_mappings[event_name], partial(self._event, event_name))

        # Change events are different depending on the widget
        if event_name == 'change':
            if isinstance(self, RadiogroupBase):
                # Add the event to each radiobutton in the group
                for radiobutton in self.winfo_children():
                    radiobutton.configure(command=partial(self._event, event_name))

            if isinstance(self, Slider):
                # The tk callback for a slider passes an argument that is the value of the slider
                self.configure(command=partial(self._slider_change_event, event_name))

            if isinstance(self, Checkbox):
                # change method available on Radiobutton and Checkbox objects
                self.configure(command=partial(self._event, event_name))

            if isinstance(self, Number):
                # Two ways to trigger the change event on a Number widget:
                # 1. Using the arrows on the widget (or arrow keys on keyboard)
                # 2. Pressing 'enter' in the text entry
                self.configure(command=partial(self._event, event_name))
                # bind() passes an event object
                self.bind('<Return>', partial(self._number_change_event, event_name))

            if isinstance(self, Input):
                # Add a trace to the string variable associated with the Input for listening for the 'change' event
                # Returns an internal string required to remove the listener
                self._observer = self._value.trace('w', partial(self._text_change_event, event_name))

            # Note: no specific actions needed for Textbox as the change event is set when the widget is created

        if event_name == 'press':
            # press event only on buttons
            self.configure(command=partial(self._event, event_name))

        if event_name == 'select':
            # Select event associated with Listboxes, Dropdowns and Tables
            if isinstance(self, Dropdown):
                self.bind('<<ComboboxSelected>>', partial(self._event, event_name))
            elif isinstance(self, (Table, Listbox)):
                self._treeview.bind('<<TreeviewSelect>>', partial(self._event, event_name))

    def remove_event_listener(self, event_name):
        """Removes an event listener from a widget. Has no effect if the event is not currently set.

        Args:
            event_name (str): The name of the event

        Raises:
            ValueError: The given event_name is not an event or cannot be associated with this widget
        """
        if event_name not in self._events:
            raise ValueError(f"Event '{event_name}' is not valid for {self}")

        if event_name in self._tk_event_mappings:
            # Unbind standard events like mouse_down, right_click etc
            if isinstance(self, (Table, Listbox)):
                # Unbind the event to the treeview part of the Table & Listbox widgets
                self._treeview.unbind(self._tk_event_mappings[event_name])
            elif isinstance(self, Textbox):
                self._tk_text_widget.unbind(self._tk_event_mappings[event_name])
            elif not (isinstance(self, Hyperlink) and event_name in ('mouse_down', 'mouse_over')):
                # Default unbind for all widgets unless it will break the hyperlink functionality
                self.unbind(self._tk_event_mappings[event_name])

        if event_name == 'change':
            if isinstance(self, RadiogroupBase):
                # Unbind the event function from each radiobutton in the group
                for radiobutton in self.winfo_children():
                    radiobutton.configure(command='')

            if isinstance(self, (Slider, Checkbox)):
                self.configure(command='')

            if isinstance(self, Number):
                self.configure(command='')
                self.unbind('<Return>')

            if isinstance(self, Input):
                # If there is a change event, then delete the trace
                if self._observer:
                    self._value.trace_vdelete('w', self._observer)
                    self._observer = None

            if isinstance(self, (Date, Textbox)):
                self._events['change'] = None

        if event_name == 'press':
            # press event on buttons
            self.configure(command='')

        if event_name == 'select':
            # Select event associated at the moment with Listboxes, Tables and Dropdowns
            if isinstance(self, Dropdown):
                self.unbind('<<ComboboxSelected>>')
            elif isinstance(self, (Table, Listbox)):
                self._treeview.unbind('<<TreeviewSelect>>')

    # All widgets can be enabled and disabled
    @property
    def disabled(self):
        """Gets or sets the state of the widget as either disable or not"""
        return self._disabled

    @disabled.setter
    def disabled(self, value):
        self._disabled = bool(value)

        if isinstance(self, Textbox):
            # tk widgets disabled with config
            state = 'disabled' if self._disabled else 'normal'
            self._tk_text_widget.config(state=state)
            if OS == "Windows":
                background = "SystemButtonFace" if state == 'disabled' else 'SystemWindow'
                self._tk_text_widget.config(bg=background)
            if OS == "Mac":
                background = "SystemUtilityWindowBackgroundInactive" if state == 'disabled' else 'SystemWindowBody'
                self._tk_text_widget.config(bg=background)

        elif isinstance(self, (Table, Listbox)):
            # The treeview is a member of the Table and Listbox widgets
            # Note: events still fire when the table is disabled
            state = ['disabled'] if self._disabled else ['!disabled']
            self._treeview.state(state)
            # When disabled, clicking on the widget still selects items, so clear any selections
            self.select_none()

        elif isinstance(self, RadiogroupBase):
            # Both the container and each radiobutton are disabled
            state = ['disabled'] if self._disabled else ['!disabled']
            self.state(state)  # disable the container
            for radio in self.winfo_children():
                radio.state(state)  # disable each radiobutton

        elif isinstance(self, Hyperlink):
            # Change the hand cursor to the 'no' cursor for a disabled Hyperlink
            self.cursor = 'no' if self._disabled else 'hand2'
            state = ['disabled'] if self._disabled else ['!disabled']
            self.state(state)

        else:
            # most other widgets are ttk widgets disabled with the state() method
            state = ['disabled'] if self._disabled else ['!disabled']
            self.state(state)

    @property
    def margin_top(self):
        """Gets or sets the top margin of the widget as a value in pixels"""
        return self.margins[0]

    @margin_top.setter
    def margin_top(self, value):
        self.margins[0] = value

    @property
    def margin_right(self):
        """Gets or sets the right margin of the widget as a value in pixels"""
        return self.margins[1]

    @margin_right.setter
    def margin_right(self, value):
        self.margins[1] = value

    @property
    def margin_bottom(self):
        """Gets or sets the bottom margin of the widget as a value in pixels"""
        return self.margins[2]

    @margin_bottom.setter
    def margin_bottom(self, value):
        self.margins[2] = value

    @property
    def margin_left(self):
        """Gets or sets the left margin of the widget as a value in pixels"""
        return self.margins[3]

    @margin_left.setter
    def margin_left(self, value):
        self.margins[3] = value

    def set_focus(self):
        """Gives focus to the current widget"""

        # If tkinter's focus() method is called during an event, it is ignored. This hackiness fixes that.
        self.winfo_toplevel().after(0, self.focus)


class Label(ttk.Label, GooeyPieWidget):
    def __init__(self, container, text):
        """Creates a new label widget

        Args:
            container: The window or container to which the widget will be added
            text (str): The text of the label
        """
        GooeyPieWidget.__init__(self, container)
        ttk.Label.__init__(self, container, text=str(text))

        # Mapping between GooeyPie and tkinter for alignment options
        self._tk_settings = {
            'left': 'w',
            'center': 'center',
            'right': 'e'
        }
        # Need to add style information here to be able to look up for wrapping
        # Also used more extensively in the child class StyleLabel to add formatting
        self._style = ttk.Style()
        self._style_id = f'{str(id(self))}.TLabel'  # Need a custom id for each instance
        self.configure(style=self._style_id)

        self._wrap = False

    def __str__(self):
        return f"<Label '{self.text}'>"

    def __repr__(self):
        return self.__str__()

    @property
    def text(self):
        """Gets or sets the text of the label"""
        return self.cget('text')

    @text.setter
    def text(self, content):
        self.configure(text=str(content))

    @property
    def align(self):
        """Gets or sets the alignment of the label (left, right or center). Has no effect if the width of the
        label has not been set to exceed the number of character in the label.
        """
        tk_setting = str(self.cget('anchor'))
        if tk_setting == 'w':
            return 'left'
        elif tk_setting == 'e':
            return 'right'
        else:
            return 'center'

    @align.setter
    def align(self, setting):
        try:
            self.configure(anchor=self._tk_settings[setting])
        except KeyError:
            raise ValueError(f"Value for align must be 'left', 'right' or 'center' (value given was {repr(setting)})")

    @property
    def justify(self):
        """Gets or sets the justify property of the label (left, center or right) which determines the horizontal
        alignment or each line of text if the label contains newline characters.
        """
        return self.cget('justify')

    @justify.setter
    def justify(self, value):
        self.configure(justify=value)

    @property
    def width(self):
        """Returns the width of the label in characters if it has been set. Returns None if width has not been set"""
        return self.cget('width') or None

    @width.setter
    def width(self, value):
        """Set the width of the label in characters.
        If the label is longer than the given width, it will be truncated unless the wrap property is set to True
        If the label is shorter than the given width, extra space will be allocated
        """
        self.configure(width=value)

    @property
    def wrap(self):
        """Returns a boolean to indicate whether label text longer than its set width will wrap onto other lines"""
        return self._wrap

    @wrap.setter
    def wrap(self, value):
        """Sets whether label text that extends beyond its width is truncated (wrap = False) or continued
        on to the next line (wrap = True)

        Notes:
            + If the label has no width set, setting the wrap property has no effect
            + If wrap is dynamically changed during the execution of the program, the label will
              not resize vertically as needed.
        """
        self._wrap = bool(value)
        if self._wrap:
            # Setting wrap has no effect if the width of the label has not been set
            if self.width:
                # self.wrap_width = self.width
                self.configure(wraplength=self._pixels_per_character() * self.width)
        else:
            self._wrap = False
            self.configure(wraplength='')

    def _pixels_per_character(self):
        """Estimates the average width of a character in pixels by naively calculating the length of
        all ASCII characters in the label
        """
        from string import ascii_letters
        fudge_factor = 0.91  # value found through trial and error to get a more accurate measure
        f = font.Font(font=self._style.lookup(self._style_id, 'font'))
        return f.measure(ascii_letters) / len(ascii_letters) * fudge_factor


class Button(ttk.Button, GooeyPieWidget):
    def __init__(self, container, text, event_function, min_size=10):
        """Creates a button

        Args:
            container: The window or container to which the widget will be added
            text (str): The text on the button
            event_function: The function called when the button is activated

        """
        GooeyPieWidget.__init__(self, container)
        ttk.Button.__init__(self, container, text=text)
        size = max(min_size, len(text) + 2)
        self.configure(width=size)
        self._events['press'] = None
        if event_function:
            self.add_event_listener('press', event_function)

    def __str__(self):
        return f"<Button '{self.text}'>"

    def __repr__(self):
        return self.__str__()

    @property
    def width(self):
        """Gets or sets the width of the button in pixels"""
        return self.cget('width')

    @width.setter
    def width(self, value):
        if type(value) != int or int(value) < 1:
            raise ValueError('Width must be a positive integer')
        self.configure(width=value)

    @property
    def text(self):
        """Gets or sets the text on the button"""
        return self.cget('text')

    @text.setter
    def text(self, text):
        self.configure(text=text)


class Slider(ttk.Scale, GooeyPieWidget):
    def __init__(self, container, low, high, orientation='horizontal'):
        """Creates a slider

        Args:
            container: The window or container to which the widget will be added
            low: An integer or float for the minimum value of the slider
            high: An integer or float for the maximum value of the slider
            orientation (str): either 'horizontal' or 'vertical'

        Raises:
            TypeError: low or high are not numbers
            ValueError: low is greater than high
        """
        if not isinstance(low, (int, float)) or not isinstance(high, (int, float)):
            raise TypeError('low and high must be numerical types')
        if low >= high:
            raise ValueError('low must be less than high')
        if orientation not in ('horizontal', 'vertical'):
            raise ValueError("Slider orientation must be either 'horizontal' or 'vertical'")

        GooeyPieWidget.__init__(self, container)
        self._events['change'] = None

        # The slider's value will be a float or int depending on the low/high parameter data type
        if isinstance(low, float) or isinstance(high, float):
            self._value = tk.DoubleVar()
        else:
            self._value = tk.IntVar()

        # The previous value is stored so that the change event is called only when the actual value changes
        self._previous_value = self._value.get()

        # Swap low and high for vertical orientation to change the weird default behaviour of up means lower
        if orientation == 'vertical':
            low, high = high, low

        ttk.Scale.__init__(self, container, from_=low, to=high, orient=orientation, variable=self._value)

        # Set the initial value of the slider to the low value, or it defaults to 0
        self.set(low)

    def __str__(self):
        return f'<Slider from {self.cget("from")} to {self.cget("to")}>'

    def __repr__(self):
        return self.__str__()

    @property
    def value(self):
        """Gets or sets the current value of the slider"""
        return self._value.get()

    @value.setter
    def value(self, val):
        self.set(val)

    @property
    def length(self):
        """Gets or sets the length of the slider in pixels"""
        return self.cget('length')

    @length.setter
    def length(self, value):
        self.configure(length=value)


class StyleLabel(Label):
    """A StyleLabel can be customised with colours (foreground and background), fonts and size

    Two helper functions exist in the main GooeyPieApp application object:
      fonts() returns all available fonts on the user's system
      font_available(name) returns True if name is installed on the current system
    """

    def __init__(self, container, text):
        """Creates a new StyleLabel

        A StyleLabel can be customised with fonts, styles and colours

        Args:
            container: The window or container to which the widget will be added
            text (str): The text of the label
        """
        super().__init__(container, text)

    def __str__(self):
        return f"<StyleLabel '{self.text}'>"

    def __repr__(self):
        return self.__str__()

    def _get_current_font(self):
        """Returns a dictionary representing the current font"""
        return font.Font(font=self._style.lookup(self._style_id, 'font')).actual()

    def _set_font(self, font_dict):
        font_string = [font_dict['family'], font_dict['size']]
        options = []
        if font_dict['weight'] == 'bold':
            options.append('bold')
        if font_dict['slant'] == 'italic':
            options.append('italic')
        if font_dict['underline'] == 1:
            options.append('underline')
        if font_dict['overstrike'] == 1:
            options.append('overstrike')

        font_string.append(' '.join(options))
        self._style.configure(self._style_id, font=font_string)

    def _set_font_property(self, key, value):
        new_font = self._get_current_font()
        new_font[key] = value
        self._set_font(new_font)

    def set_font(self, font_name, size, options=''):
        """Sets the font with name, size and other options

        Args:
            font_name (str): The font name
            size: The font size as an integer, measured in points (pt), or the string 'default'
            options (str): A list of options separated by spaces. Must be one or more of 'bold', 'italic',
                'underline' or 'strikethrough'-
        """
        self.font_name = font_name
        self.font_size = size
        if options:
            options = options.replace(',', '').split(' ')
            # Check if the supplied options are valid
            if not set(options).issubset({'bold', 'italic', 'underline', 'strikethrough'}):
                raise ValueError(f"'{' '.join(options)}' is not a valid options string. Options can include "
                                 f"'bold', 'italic', 'underline' or 'strikethrough'. ")
            else:
                self.font_weight = 'bold' if 'bold' in options else 'normal'
                self.font_style = 'italic' if 'italic' in options else 'normal'
                self.underline = 'underline' if 'underline' in options else 'normal'
                self.strikethrough = 'strikethrough' if 'strikethrough' in options else 'normal'

    def set_padding(self, horizontal, vertical):
        """Sets the spacing between the contents of the label and the edge of the label

        Args:
            horizontal (int): The distance in pixels between the left and right of the label and the widget edge
            vertical (int): The distance in pixels between the top and bottom of the label and the widget edge
        """
        self._set_padding(horizontal, vertical)

    def clear_styles(self):
        """Sets all fonts back to the default styles"""
        self._style.configure(self._style_id, font=font.nametofont('TkDefaultFont'))
        self.colour = 'default'
        self.background_color = 'default'

    @property
    def font_name(self):
        """Gets or sets the font name, or 'default'"""
        return self._get_current_font()['family']

    @font_name.setter
    def font_name(self, value):
        if value == 'default':
            self._set_font_property('family', font.nametofont('TkDefaultFont').actual()['family'])
        else:
            # Only change font if it is on the users system, otherwise do nothing
            if value.lower() in [font_name.lower() for font_name in font.families()]:
                self._set_font_property('family', value)

    @property
    def font_size(self):
        """Gets or sets the font size in points (pt), or 'default'"""
        return self._get_current_font()['size']

    @font_size.setter
    def font_size(self, value):
        if value == 'default':
            self._set_font_property('size', font.nametofont('TkDefaultFont').actual()['size'])
        else:
            if type(value) != int:
                raise ValueError(f"Font size must be an integer or the string 'default' "
                                 f"(value specified was {value})")
            self._set_font_property('size', value)

    @property
    def font_weight(self):
        """Gets or sets the font weight as either 'bold' or 'normal'"""
        return self._get_current_font()['weight']

    @font_weight.setter
    def font_weight(self, value):
        if value not in ('bold', 'normal'):
            raise ValueError(f"Font weight must be either 'bold' or 'normal' (value specified was '{value}')")
        self._set_font_property('weight', value)

    @property
    def font_style(self):
        """Gets or sets the font style as either 'italic' or 'normal'"""
        if self._get_current_font()['slant'] == 'roman':
            return 'normal'
        else:
            return 'italic'

    @font_style.setter
    def font_style(self, value):
        if value not in ('italic', 'normal'):
            raise ValueError(f"Font style must be either 'italic' or 'normal' (value specified was '{value}')")
        self._set_font_property('slant', value)

    @property
    def underline(self):
        """Gets or sets the underline setting as either 'underline' or 'normal'"""
        current_font = self._style.lookup(self._style_id, 'font')
        if font.Font(font=current_font).actual()['underline'] == 0:
            return 'normal'
        else:
            return 'underline'

    @underline.setter
    def underline(self, value):
        if value not in ('normal', 'underline'):
            raise ValueError(f"Underline must be either 'underline' or 'normal' (value specified was '{value}')")
        # 0 for normal, 1 for underline
        self._set_font_property('underline', ('normal', 'underline').index(value))

    @property
    def strikethrough(self):
        """Gets or sets the strikethrough setting as either 'strikethrough' or 'normal'"""
        current_font = self._style.lookup(self._style_id, 'font')
        if font.Font(font=current_font).actual()['overstrike'] == 0:
            return 'normal'
        else:
            return 'strikethrough'

    @strikethrough.setter
    def strikethrough(self, value):
        if value not in ('normal', 'strikethrough'):
            raise ValueError(f"Strikethrough style must be either 'strikethrough' or 'normal' "
                             f"(value specified was '{value}')")
        # 0 for normal, 1 for strikethrough (overstrike in tk-land)
        self._set_font_property('overstrike', ('normal', 'strikethrough').index(value))

    @property
    def colour(self):
        """Gets or sets the colour as a hex string, named colour or 'default'"""
        current_colour = self._style.lookup(self._style_id, 'foreground')
        if current_colour == 'SystemWindowText':
            return 'default'
        else:
            return current_colour

    @colour.setter
    def colour(self, value):
        if value == 'default':
            self._style.configure(self._style_id, foreground='SystemWindowText')
        else:
            self._style.configure(self._style_id, foreground=value)

    @property
    def background_colour(self):
        """Gets or sets the background colour as a hex string, named colour or 'default'"""
        current_colour = self._style.lookup(self._style_id, 'background')
        if current_colour == 'SystemButtonFace':
            return 'default'
        else:
            return current_colour

    @background_colour.setter
    def background_colour(self, value):
        if value == 'default':
            self._style.configure(self._style_id, background='SystemButtonFace')
        else:
            self._style.configure(self._style_id, background=value)

    @property
    def border(self):
        """Gets or sets whether the label has a border or not"""
        border_setting = str(self._style.lookup(self._style_id, 'relief'))
        return border_setting == 'solid'

    @border.setter
    def border(self, value):
        border_setting = 'solid' if value else 'flat'
        self._style.configure(self._style_id, relief=border_setting)

    # Function aliases for alternate spellings of colour
    color = colour
    background_color = background_colour

    # Helper function
    def _elements_available(self):
        # Get widget elements
        style = self._style
        layout = str(style.layout('custom.TLabel'))
        print('Stylename = {}'.format('custom.TLabel'))
        print('Layout    = {}'.format(layout))
        elements = []
        for n, x in enumerate(layout):
            if x == '(':
                element = ""
                for y in layout[n + 2:]:
                    if y != ',':
                        element += str(y)
                    else:
                        elements.append(element[:-1])
                        break
        print('\nElement(s) = {}\n'.format(elements))

        # Get options of widget elements
        for element in elements:
            print('{0:30} options: {1}'.format(element, style.element_options(element)))


class Hyperlink(StyleLabel):
    def __init__(self, container, text, url):
        """Create a new hyperlink which opens the specified URL when activated in the default browser

        Args:
            container: The window or container to which the widget will be added
            text (str): The text on the hyperlink
            url (str): The URL that the hyperlink will open to
        """
        StyleLabel.__init__(self, container, text)
        self.url = url
        self.colour = 'blue'
        self.underline = 'underline'
        self.cursor = 'hand2'
        self.bind('<Enter>', lambda e: self.configure(cursor=self.cursor))
        self.bind('<Button-1>', self._open_link)
        self.configure(takefocus=True)  # Labels don't normally take focus when tabbing

    def __str__(self):
        return f"<Hyperlink '{self.text}'>"

    def __repr__(self):
        return self.__str__()

    def _open_link(self, e):
        if not self.disabled:
            import webbrowser
            webbrowser.open(self.url)


class Image(Label):
    def __init__(self, container, image):
        """Creates a new image

        Args:
            container: The window or container to which the widget will be added
            image (str): The path to the image file
        """
        Label.__init__(self, container, None)
        self.image = image

    def __str__(self):
        return f"""<Image '{self.image}'>"""

    def __repr__(self):
        return self.__str__()

    @property
    def image(self):
        """Gets or sets the image path and filename"""
        return self._image

    @image.setter
    def image(self, image_path):
        self._image = image_path
        self._tk_image = ImageTk.PhotoImage(PILImage.open(image_path))
        self.configure(image=self._tk_image)


class Input(ttk.Entry, GooeyPieWidget):
    def __init__(self, container):
        """Creates a new Input widget

        Args:
            container: The window or container to which the widget will be added
        """
        GooeyPieWidget.__init__(self, container)
        self._value = tk.StringVar()
        ttk.Entry.__init__(self, container, textvariable=self._value)
        self._events['change'] = None
        self._observer = None  # Used in tkinter's trace method, for the 'change' event

    def __str__(self):
        return f"""<Input widget>"""

    def __repr__(self):
        return self.__str__()

    @property
    def width(self):
        """Gets or sets the width of the Input in characters"""
        return self.cget('width')

    @width.setter
    def width(self, value):
        if type(value) != int or int(value) < 1:
            raise ValueError('Width must be a positive integer')
        self.configure(width=value)

    @property
    def text(self):
        """Gets or sets the text in the Input"""
        return self._value.get()

    @text.setter
    def text(self, value):
        self._value.set(value)

    @property
    def secret(self):
        """Gets or sets whether to hide the characters in the Input with dots"""
        return self.cget('show') == '●'

    @secret.setter
    def secret(self, value):
        if value:
            self.configure(show='●')
        else:
            self.configure(show='')

    @property
    def justify(self):
        """Aligns the text horizontally within in the widget, either 'left', 'right' or 'center'"""
        return self.cget('justify')

    @justify.setter
    def justify(self, value):
        self.configure(justify=value)

    def select(self):
        """Selects (highlights) the contents of the Input"""
        self.focus()
        self.select_range(0, tk.END)

    def clear(self):
        """Clears any text in the Input"""
        self.text = ''


class Secret(Input):
    def __init__(self, container):
        """Creates a new Secret Input

        Args:
            container: The window or container to which the widget will be added
        """
        Input.__init__(self, container)
        self.configure(show='●')

    def __str__(self):
        return f"""<Secret widget>"""

    def __repr__(self):
        return self.__str__()

    def unmask(self):
        """Shows the characters in the Secret"""
        self.configure(show='')

    def mask(self):
        """Hides the characters in the Secret"""
        self.configure(show='●')

    def toggle(self):
        """Toggles between showing and hiding the characters in the Secret"""
        if self.cget('show'):
            self.unmask()
        else:
            self.mask()


class Listbox(Container, GooeyPieWidget):
    """Listbox widget"""
    def __init__(self, container, items=()):
        """Creates a new Listbox

        Args:
            container: The window or container to which the widget will be added
            items (list): Optional, a list of the items in the Listbox.
        """
        Container.__init__(self, container)

        # Set container to fill cell
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Create treeview and configure to act as listbox
        self._treeview = ttk.Treeview(self, columns=('0',), show='tree', selectmode='browse')
        self._treeview.column('#0', width=0, minwidth=0, stretch=False)

        # Create and configure scrollbar
        self._scrollbar = tk.Scrollbar(self, orient='vertical')
        self._scrollbar.config(command=self._treeview.yview)
        self._treeview.config(yscrollcommand=self._scrollbar.set)
        self._scrollbar_visible = 'auto'

        # Add to parent Container
        self._treeview.grid(row=0, column=0, sticky='nsew')
        self._scrollbar.grid(row=0, column=1, sticky='nsew')

        GooeyPieWidget.__init__(self, container)
        self._events['select'] = None

        # Populate listbox
        self.items = items
        self._treeview.bind('<Configure>', self._update_scrollbar)

    def __str__(self):
        return f"<Listbox widget>"

    def __repr__(self):
        return self.__str__()

    def _update_scrollbar(self, _event=None):
        """Updates the visibility of the scrollbar in response to resize events, changes to the contents
        of the listbox and changes to the scrollbar setting using the scrollbar property.
        The _event parameter is needed so it can be used as the 'Configure' callback, which is triggered when the
        listbox changes size in response to a window resize event.
        """
        if self._scrollbar_visible == 'visible':
            self._show_scrollbar()
        elif self._scrollbar_visible == 'hidden':
            self._hide_scrollbar()
        else:
            scrollbar_value = self._scrollbar.get()
            if scrollbar_value == (0.0, 1.0) or scrollbar_value == (0.0, 0.0, 0.0, 0.0):
                self._hide_scrollbar()
            else:
                self._show_scrollbar()

    def _hide_scrollbar(self):
        """Hides the scrollbar from the listbox"""
        self._treeview.grid_remove()
        self._treeview.grid(row=0, column=0, sticky='nsew', columnspan=2)
        self._scrollbar.grid_remove()

    def _show_scrollbar(self):
        """Shows the scrollbar on the side of the listbox"""
        self._treeview.grid_remove()
        self._treeview.grid(row=0, column=0, sticky='nsew', columnspan=1)
        self._scrollbar.grid()

    @property
    def scrollbar(self):
        """Gets or sets the scrollbar setting. Must be one of either 'auto', 'hidden' or 'visible'"""
        return self._scrollbar_visible

    @scrollbar.setter
    def scrollbar(self, setting):
        if setting not in ('auto', 'visible', 'hidden'):
            raise ValueError("Invalid scrollbar option - must be set to 'auto', 'hidden' or 'visible'")
        self._scrollbar_visible = setting
        self._update_scrollbar()

    @property
    def height(self):
        """Gets or sets the minimum height of the Listbox as the number of visible lines"""
        return self._treeview.cget('height')

    @height.setter
    def height(self, lines):
        self._treeview.configure(height=lines)

    @property
    def width(self):
        """Gets or sets the width of the listbox in pixels. Default is 200"""
        return self._treeview.column(0, option='width')

    @width.setter
    def width(self, pixels):
        if type(pixels) != int or int(pixels) < 1:
            raise ValueError('Width must be a positive integer')
        self._treeview.column(0, width=pixels)

    @property
    def items(self):
        """Gets or sets all data in the table as a list of lists"""
        return [self._treeview.item(line)['values'][0] for line in self._treeview.get_children()]

    @items.setter
    def items(self, values):
        if type(values) not in (list, tuple):
            raise ValueError('Listbox items must be lists or tuples')

        self.clear()
        for item in values:
            self._treeview.insert('', 'end', values=(item,))
        self._update_scrollbar()

    @property
    def multiple_selection(self):
        """Gets or sets the ability to select multiple items in the Listbox

        Allows multiple rows to be selected with shift-click or ctrl-click"""
        return str(self._treeview.cget('selectmode')) == 'extended'

    @multiple_selection.setter
    def multiple_selection(self, multiple):
        mode = 'extended' if multiple else 'browse'
        self._treeview.config(selectmode=mode)
        # Clear the selection if single selection is enabled
        if not multiple:
            self.select_none()

    @property
    def selected(self):
        """Gets or sets the item(s), starting from 0, of the currently selected line. Returns None
        if nothing is selected. Returns a list of items if multiple selections are enabled.
        """
        selected_ids = self._treeview.selection()
        if not selected_ids:
            return None
        if self.multiple_selection:
            return [self._treeview.item(row_id)['values'][0] for row_id in selected_ids]
        else:
            return self._treeview.item(selected_ids[0])['values'][0]

    @selected.setter
    def selected(self, value):
        """Sets the value at the current selection. Raises an error if zero or multiple items are selected"""
        selected_ids = self._treeview.selection()
        if len(selected_ids) > 1:
            raise ValueError('Cannot set value when multiple items in the listbox are selected')
        if len(selected_ids) == 0:
            raise ValueError('Cannot set value - no item selected in the listbox')

        # if multiple selection is enabled, the selected index is in a list
        if self.multiple_selection:
            selected_index = self.selected_index[0]
        else:
            selected_index = self.selected_index

        # change the selected item
        updated_items = self.items
        updated_items[selected_index] = value
        self.items = updated_items
        self.selected_index = selected_index

    @property
    def selected_index(self):
        """Gets or sets the index(es), starting from 0, of the selected line. Returns None if nothing
        is selected. Returns a list of indexes if multiple selections are enabled.
        """
        selected_ids = self._treeview.selection()
        all_ids = self._treeview.get_children()

        if not selected_ids:
            return None
        if self.multiple_selection:
            return [all_ids.index(selected) for selected in selected_ids]
        else:
            return all_ids.index(selected_ids[0])

    @selected_index.setter
    def selected_index(self, index):
        """Adds to the current selection if multiple selection is set"""
        all_rows = self._treeview.get_children()
        if len(self._treeview.get_children()) == 0:
            raise ValueError(f'No items in Listbox to select')
        if index not in range(len(all_rows)):
            raise ValueError(f'The index must be in the range 0 to {len(all_rows) - 1}. '
                             f'The value of the index specified was {index}.')

        # Clear the current selection if single selection only
        if not self.multiple_selection:
            self.select_none()

        # Select the item specified by the index
        item_id = all_rows[index]
        self._treeview.selection_add(item_id)
        self._treeview.see(item_id)  # Show the selected row (in case it is not be in view)

    def add_item(self, item):
        """Adds an item to the end of the listbox

        Args:
            item (str): The item to add to the Listbox
        """
        self.add_item_at('end', item)

    def add_item_to_start(self, item):
        """Adds an item to the top of the listbox

        Args:
            item (str): The item to add to the Listbox
        """
        self.add_item_at(0, item)

    def add_item_at(self, index, item):
        """Adds an item to the given index

        Args:
            index (int): The index of the listbox
            item (str): The item to add to the Listbox

        Raises:
            TypeError: index is not an integer
            ValueError: index is out of bounds
        """
        if type(index) != int and index != 'end':
            raise TypeError(f'index must be an integer. The value provided was {index}')
        if index != 'end' and (index < 0 or index > len(self.items)):
            raise ValueError(f'Index out of bounds. Value must be in the range 0 to {len(self.items)}.')

        self._treeview.insert('', index, values=(item,))
        self._update_scrollbar()

    def remove_item(self, index):
        """Removes and returns the item at the given index

        Args:
            index (int): The index of the item to remove from the Listbox

        Returns:
            str: The item in the Listbox at index

        Raises:
            TypeError: Index is not an integer
            ValueError: Index is negative
            ValueError: Index is larger than the number of items in the listbox
        """
        row_ids = self._treeview.get_children()
        if type(index) != int:
            raise TypeError(f'index must be an integer. The value provided was {index}')
        if index < 0 or index > len(row_ids) - 1:
            raise ValueError(f'The index must be in the range 0 to {len(row_ids) - 1}. '
                             f'The value of index was {index}')
        removed = self._treeview.item(row_ids[index])['values'][0]
        self._treeview.delete(row_ids[index])
        self._update_scrollbar()
        return removed

    def remove_selected(self):
        """Removes and returns all items from the selected index(es)

        Returns:
            A string or list of strings, depending on whether multiple items is enabled. None if nothing is selected
        """
        row_data = self.selected
        self._treeview.delete(*self._treeview.selection())
        self._update_scrollbar()
        return row_data

    def select_all(self):
        """Selects (highlights) all items in the listbox. Multiple selection must be enabled"""
        if self.multiple_selection:
            self._treeview.selection_set(*self._treeview.get_children())

    def select_none(self):
        """Deselects any items that may be selected in the listbox"""
        self._treeview.selection_remove(*self._treeview.selection())

    def clear(self):
        """Removes all items from the Listbox"""
        for row_id in self._treeview.get_children():
            self._treeview.delete(row_id)
        self._update_scrollbar()


class ImageButton(Button):
    """An ImageButton widget is a button with an image and, optionally, text"""
    def __init__(self, container, image, event_function, text=''):
        """Create a new ImageButton

        Args:
            container: The window or container to which the widget will be added
            image (str): The path and filename of the image
            event_function: The function to call when the button is activated
            text (str): Optional text that appears on the button
        """
        super().__init__(container, text, event_function, 0)

        self._image = image
        self._padding = [4, 4]  # default spacing between the image and button border

        self._tk_image = ImageTk.PhotoImage(PILImage.open(image))
        self.configure(image=self._tk_image, compound='left' if text else 'image')

    def __str__(self):
        return f"""<ImageButton '{self._image}'>"""

    def __repr__(self):
        return self.__str__()

    @property
    def image(self):
        """Gets of sets the image on the button"""
        return self._image

    @image.setter
    def image(self, filename):
        self._tk_image = ImageTk.PhotoImage(PILImage.open(filename))
        self.configure(image=self._tk_image)
        self._image = filename

    @property
    def image_position(self):
        """Gets or sets the location of the image relative to the button text, either 'top', 'bottom', 'left'
            or 'right'.
        """
        return self.cget('compound')

    @image_position.setter
    def image_position(self, position):
        self.configure(compound=position)

    def set_padding(self, horizontal, vertical):
        """Sets the spacing between the image on the button and button border

        Args:
            horizontal (int): The distance in pixels to the left and right of the image and the button border
            vertical (int): The distance in pixels to the top and bottom of the image and the button border
        """
        self._set_padding(horizontal, vertical)


class Checkbox(ttk.Checkbutton, GooeyPieWidget):
    """A checkbox indicates a boolean state"""
    def __init__(self, container, text, checked=False):
        """Creates a new checkbox

        Args:
            container: The window or container to which the widget will be added
            text (str): The text that appears alongside the checkbox
            checked (bool): The initial state of the checkbox
        """
        GooeyPieWidget.__init__(self, container)
        self._checked = tk.BooleanVar(value=checked)
        ttk.Checkbutton.__init__(self, container, text=text, variable=self._checked)
        self.state(['!alternate'])
        self._events['change'] = None  # Checkboxes support the 'change' event

    def __str__(self):
        return f'''<Checkbox '{self.cget("text")}'>'''

    def __repr__(self):
        return self.__str__()

    @property
    def checked(self):
        """Gets or sets the state of the checkbox"""
        return self._checked.get()

    @checked.setter
    def checked(self, state):
        self._checked.set(state)


class RadiogroupBase(GooeyPieWidget):
    """Base class used by Radiogroup and LabelledRadiogroup"""

    def __init__(self, container, choices, orientation):
        """Creates a new group of RadioButtons"""
        GooeyPieWidget.__init__(self, container)
        self._events['change'] = None  # Radiobuttons support the 'change' event
        self._selected = tk.StringVar()

        # If images are used (to be implemented, need to support passing a list of 2-tuples,
        # where first item is the image, second is the value returned

        if not isinstance(choices, (list, tuple)):
            raise TypeError('Radiogroup choices must be a list')
        length = len(choices)
        if length < 2:
            raise ValueError('Radiogroups must have at least 2 options')

        # Set the appropriate grid based on the orientation. Create associated lists used when calling add()
        if orientation == 'vertical':
            self.set_grid(length, 1)
            rows = [n + 1 for n in range(length)]
            columns = [1] * length
        else:
            self.set_grid(1, length)
            rows = [1] * length
            columns = [n + 1 for n in range(length)]

        for pos, choice in enumerate(choices):
            radiobutton = ttk.Radiobutton(self, text=choice, variable=self._selected, value=choice)

            # default margins from ContainerBase: [top, right, bottom, left]
            padx = ContainerBase.spacing['widget_spacing_x']
            pady = ContainerBase.spacing['widget_spacing_y']

            if isinstance(self, Radiogroup):
                # Container already has margins around the frame, set margins to zero
                margins = [0, 0, 0, 0]
                if pos != length - 1:
                    # Add appropriate spacing between radio items by changing horizontal or vertical margin
                    # (depending on orientation) on all items except for the last one
                    if orientation == 'vertical':
                        margins[2] = pady[1]
                    else:
                        # Add a bit more spacing between horizontal items
                        margins[1] = padx[1] * 2

            if isinstance(self, LabelRadiogroup):
                margins = ['auto'] * 4
                # For vertically aligned radiogroups, reduce the vertical spacing between items.
                if orientation == 'vertical':
                    if pos != length - 1:
                        margins[2] = 0

            self.add(radiobutton, rows[pos], columns[pos], align='left', margins=margins)

    @property
    def options(self):
        """Gets the list of options for the radiobuttons"""
        return tuple(widget.cget('text') for widget in self.winfo_children())

    @property
    def selected(self):
        """Gets or sets the selected option. Returns None if no Radiobutton has been selected"""
        if self._selected.get():
            return self._selected.get()
        else:
            return None

    @selected.setter
    def selected(self, value):
        if value:
            if value not in self.options:
                raise ValueError(f"'{value}' is not one of the options in the radio group")
            self._selected.set(value)
        else:
            self._selected.set('')

    @property
    def selected_index(self):
        """Gets or sets the selected index from 0. Returns None if no Radiobutton has been selected"""
        if self._selected.get():
            return self.options.index(self._selected.get())
        else:
            return None

    @selected_index.setter
    def selected_index(self, index):
        if type(index) != int:
            raise TypeError(f'index must be a positive integer')
        if index < 0 or index >= len(self.options):
            raise ValueError(f'index must be an integer from 0 to {len(self.options) - 1}')
        self._selected.set(self.options[index])

    def deselect(self):
        """Deselects all options"""
        self._selected.set('')

    def disable_index(self, index):
        """Disables a single Radiobutton

        Args:
            index (int): the RadioButton to disable, indexed from 0
        """
        if type(index) != int:
            raise TypeError(f'index must be a positive integer')
        if index < 0 or index >= len(self.options):
            raise ValueError(f'index must be an integer from 0 to {len(self.options) - 1}')
        self.winfo_children()[index].configure(state='disabled')

    def enable_index(self, index):
        """Enables a single Radiobutton

        Args:
            index (int): the RadioButton to disable, indexed from 0
        """
        if type(index) != int:
            raise TypeError(f'index must be a positive integer')
        if index < 0 or index >= len(self.options):
            raise ValueError(f'index must be an integer from 0 to {len(self.options) - 1}')
        self.winfo_children()[index].configure(state='enabled')

    def disable_item(self, item):
        """Disables a single Radiobutton

        Args:
            item (str): the text of the radiobutton to disable
        """
        if item not in self.options:
            raise ValueError(f"'{item}' is not one of the options in the radio group")
        index = self.options.index(item)
        self.winfo_children()[index].configure(state='disabled')

    def enable_item(self, item):
        """Enables a single Radiobutton

        Args:
            item (str): the text of the radiobutton to enable
        """
        if item not in self.options:
            raise ValueError(f"'{item}' is not one of the options in the radio group")
        index = self.options.index(item)
        self.winfo_children()[index].configure(state='enabled')


class Radiogroup(Container, RadiogroupBase):
    """A group of RadioButtons"""
    def __init__(self, container, choices, orientation='vertical'):
        """Create a new group of RadioButtons

        Args:
            container: The window or container to which the widget will be added
            choices: A list of the text alongside each RadioButton
            orientation (str): The orientation of the RadioGroup, either 'horizontal' or 'vertical'
        """
        Container.__init__(self, container)
        RadiogroupBase.__init__(self, container, choices, orientation)

    def __str__(self):
        return f'<Radiogroup {tuple(self.options)}>'

    def __repr__(self):
        return self.__str__()


class LabelRadiogroup(LabelContainer, RadiogroupBase):
    """A set of radio buttons, surrounded by a labelled frame"""

    def __init__(self, container, title, choices, orientation='vertical'):
        """Create a new group of LabelRadioButtons

        Args:
            container: The window or container to which the widget will be added
            title (str): The text on the frame surrounding the RadioButtons
            choices: A list of the text alongside each RadioButton
            orientation (str): The orientation of the RadioGroup, either 'horizontal' or 'vertical'
        """
        LabelContainer.__init__(self, container, title)
        RadiogroupBase.__init__(self, container, choices, orientation)

    def __str__(self):
        return f'<LabelRadiogroup {tuple(self.options)}>'

    def __repr__(self):
        return self.__str__()


class Dropdown(ttk.Combobox, GooeyPieWidget):
    """A Dropdown widget holds a list of options, of which one can be selected"""

    def __init__(self, container, items):
        """Create a new Dropdown widget. The initial selection will be blank unless it is explicitly set

        Args:
            container: The window or container to which the widget will be added
            items: A list of the text of each item in the Dropdown
        """
        GooeyPieWidget.__init__(self, container)
        ttk.Combobox.__init__(self, container, values=items, exportselection=0)
        self.state(['readonly'])
        self._events['select'] = None

    def __str__(self):
        return f'<Dropdown {tuple(self.items)}>'

    def __repr__(self):
        return self.__str__()

    @property
    def items(self):
        """Gets or sets the contents of the Dropdown"""
        return self.cget('values')

    @items.setter
    def items(self, values):
        """Sets the contents of the Dropdown"""
        self.deselect()
        self.configure(values=values)

    @property
    def selected(self):
        """Gets or sets the selected item in the Dropdown"""
        index = self.current()
        if index == -1:
            return None
        else:
            return self.cget('values')[index]

    @selected.setter
    def selected(self, value):
        if value is None:
            self.deselect()
        else:
            try:
                self.cget('values').index(value)
                self.set(value)
            except ValueError:
                raise ValueError(f"Cannot set Dropdown to '{value}' as it is not one of the options")

    @property
    def selected_index(self):
        """Gets or sets the index of the selected item in the Dropdown, or None if no item is selected"""
        index = self.current()
        if index == -1:
            return None
        else:
            return index

    @selected_index.setter
    def selected_index(self, index):
        try:
            self.current(index)
        except Exception:
            raise IndexError(f"Index {index} out of range")

    @property
    def width(self):
        """Gets or sets the width of the dropdown in characters (includes the control button)"""
        return self.cget('width')

    @width.setter
    def width(self, value):
        if type(value) != int or int(value) < 1:
            raise ValueError('Width must be a positive integer')
        self.configure(width=value)

    def deselect(self):
        """Deselects the currently selected item and shows an empty selection in the Dropdown"""
        self.set('')


class Number(ttk.Spinbox, GooeyPieWidget):
    """A Number widget contains a numerical value that can be directly edited or adjusted with up/down arrows"""
    def __init__(self, container, low, high, increment=1):
        """Create a new Number widget

        Args:
            container: The window or container to which the widget will be added
            low: The smallest value the widget can contain
            high: The largest value the widget can contain
            increment: The amount by which the number changes when the arrow buttons on the widget are pressed
            """
        GooeyPieWidget.__init__(self, container)

        ttk.Spinbox.__init__(self, container, from_=low, to=high, increment=increment, wrap=True)
        self.set(low)
        self.width = len(str(high)) + 4
        self._read_only = False  # Used to track state, since GooeyPie treats read_only and disabled as separate states
        self._events['change'] = None

    def __str__(self):
        low = type(self.cget("increment"))(self.cget("from"))  # format low and high with appropriate type
        high = type(self.cget("increment"))(self.cget("to"))
        return f'<Number widget from {low} to {high}>'

    def __repr__(self):
        return self.__str__()

    @property
    def value(self):
        """Gets or sets the value in the Number widget. When setting the value, type is not enforced"""
        val = self.get()  # Note: The ttk.Spinbox widget get() method always returns a string
        try:
            if type(self.cget('increment')) == float:
                # If the increment is a float, attempt to return a float
                return float(val)
            else:
                # if the increment is an int, still return a float if the user has
                # entered one. Otherwise, attempt to return an int.
                val_as_float = float(val)
                if val_as_float.is_integer():
                    return int(val_as_float)
                else:
                    return val_as_float

        except ValueError:
            # If the user has modified the value to be non-numeric, return the value as a string (tkinter default)
            return val

    @value.setter
    def value(self, value):
        """Sets the value of the number widget, but does not enforce typing in line with the increment"""
        self.set(value)

    @property
    def width(self):
        """Gets or sets the width of the spinbox in characters (includes the control buttons)"""
        return self.cget('width')

    @width.setter
    def width(self, value):
        if type(value) != int or int(value) < 1:
            raise ValueError('Width must be a positive integer')
        self.configure(width=value)

    # The underlying ttk widget (Spinbox) has 3 states: normal, disabled and readonly, so the read_only getter/setter
    # and disabled getter/setter is overridden to deal with GooeyPie supporting both properties 'separately'. In short,
    # a disabled widget cannot have its read_only property altered, but no error is raised if that happens
    @property
    def read_only(self):
        """Gets or sets the readonly state of the Number

        When the readonly state is enabled, the user can change the value in the Number widget by using the arrowheads
        on the widget, but cannot edit the value with the keyboard.
        """
        return self._read_only

    @read_only.setter
    def read_only(self, state):
        # read_only state change only available when the widget is not disabled
        if not self.disabled:
            self._read_only = bool(state)
            if self._read_only:
                setting = 'readonly'
            else:
                setting = 'normal'
            self.configure(state=setting)

    @property
    def disabled(self):
        """Gets or sets the disabled state of the Number widget.

        The value cannot be changed by the user when it is disabled
        """
        return self._disabled

    @disabled.setter
    def disabled(self, value):
        self._disabled = bool(value)
        if self._disabled:
            self.configure(state='disabled')
        else:
            # restore the read only state of the Number to its previously set value
            if self._read_only:
                self.configure(state='readonly')
            else:
                self.configure(state='normal')

    @property
    def wrap(self):
        """Gets or sets the wrap property of the widget

        When wrap is enabled, clicking the up arrow beyond the maximum value will cause the value displayed to
        wrap to the minimum value. Likewise, clicking the down arrow on the minimum value will cause the value
        displayed to wrap to the maximum value.

        If wrap is disabled, clicking the up arrow on the maximum or the down arrow on the minimum has no effect.
        """
        return bool(self.cget('wrap'))

    @wrap.setter
    def wrap(self, state):
        self.configure(wrap=bool(state))


class Table(Container, GooeyPieWidget):
    """For displaying tabular data"""
    icon_spacing = '   '
    sort_ascending_icon = f'{icon_spacing}▲'
    sort_descending_icon = f'{icon_spacing}▼'

    def __init__(self, container, headings):
        """Creates a new Table widget

        Args:
            container: The window or container to which the widget will be added
            headings: A list of strings corresponding the heading of the Table
        """
        Container.__init__(self, container)

        # Check that the heading are in a list
        if type(headings) != list and type(headings) != tuple:
            raise ValueError(f'Headings must be a list. Argument was: {type(headings)}')

        # Set container to fill cell
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Create and configure treeview
        self._num_columns = len(headings)
        column_ids = tuple(range(self._num_columns))  # tuple of form (0, 1, 2, etc)
        self._treeview = ttk.Treeview(self, columns=column_ids, show='headings', selectmode='browse')
        for index, heading in enumerate(headings):
            self._treeview.heading(index, text=heading, command=lambda col_id=index: self._sort_data(col_id))

        # Left align cell contents to center by default
        for col_id in column_ids:
            self._treeview.column(col_id, anchor='w')

        # Table is sortable by default
        self._sortable = True

        # Create vertical scrollbar configure behaviour
        self._v_scrollbar = ttk.Scrollbar(self, orient='vertical')
        self._v_scrollbar.config(command=self._treeview.yview)
        self._treeview.config(yscroll=self._v_scrollbar.set)

        # create horizontal scrollbar and configure behaviour
        self._h_scrollbar = ttk.Scrollbar(self, orient='horizontal')
        self._h_scrollbar.config(command=self._treeview.xview)
        self._treeview.config(xscroll=self._h_scrollbar.set)

        # Add to parent Container
        self._treeview.grid(row=0, column=0, sticky='nsew')
        self._v_scrollbar.grid(row=0, column=1, sticky='nsew')
        self._h_scrollbar.grid(row=1, column=0, sticky='nsew')

        # Default scrollbar settings and bindings to update visibility of scrollbars
        self._treeview.bind('<Configure>', self._update_scrollbar)  # Update scrollbar visibility when widget changes size
        self._treeview.bind('<ButtonRelease-1>', self._update_scrollbar)

        GooeyPieWidget.__init__(self, container)
        self._events['select'] = None

    def __str__(self):
        # Identified by column names

        headings = [self._treeview.heading(col_id)['text'] for col_id in range(self._num_columns)]

        # Remove any sort icons from the headings
        for index, heading in enumerate(headings):
            if heading.endswith(self.sort_ascending_icon) or heading.endswith(self.sort_descending_icon):
                headings[index] = heading[:-len(self.sort_descending_icon)]

        return f"<Table {tuple(headings)}>"

    def __repr__(self):
        return self.__str__()

    @property
    def height(self):
        """Gets or sets the height of the Table as the number of visible lines"""
        return self._treeview.cget('height')

    @height.setter
    def height(self, lines):
        self._treeview.configure(height=lines)

    @property
    def sortable(self):
        """Gets or sets whether the data can be sorted by clicking on the headings"""
        return self._sortable

    @sortable.setter
    def sortable(self, value):
        self._sortable = bool(value)
        if not self._sortable:
            self._clear_sort_icons()

    def _update_scrollbar(self, _event=None):
        """Adds/removes the horizontal scrollbar as needed"""
        horizontal_scrollbar_needed = self._treeview.xview() != (0.0, 1.0)
        row_span = 1 if horizontal_scrollbar_needed else 2

        self._treeview.grid_remove()
        self._v_scrollbar.grid_remove()
        self._h_scrollbar.grid_remove()

        self._treeview.grid(row=0, column=0, rowspan=row_span)
        self._v_scrollbar.grid(row=0, column=1, rowspan=row_span)
        if horizontal_scrollbar_needed:
            self._h_scrollbar.grid()

    def _sort_data(self, column_id):
        """When the column heading is clicked on, the data are sorted according to that column"""

        # Do not allow sorting if the table is disabled
        if self._disabled or not self._sortable:
            return

        # Update heading text with icon
        sort_descending = False
        for col_id in range(self._num_columns):
            heading = self._treeview.heading(col_id)['text']
            if col_id == column_id:
                # Set the sort icon according to whatever is already there
                if heading.endswith(self.sort_ascending_icon):
                    # Change from ascending icon to descending
                    heading_descending = f'{heading[:-len(self.sort_descending_icon)]}{self.sort_descending_icon}'
                    self._treeview.heading(col_id, text=heading_descending)
                    sort_descending = True
                elif heading.endswith(self.sort_descending_icon):
                    # Change from descending icon to ascending
                    heading_ascending = f'{heading[:-len(self.sort_descending_icon)]}{self.sort_ascending_icon}'
                    self._treeview.heading(col_id, text=heading_ascending)
                else:
                    # No current icon - set to descending by default
                    heading_ascending = f'{heading}{self.sort_ascending_icon}'
                    self._treeview.heading(col_id, text=heading_ascending)
            else:
                # Clear the icon from the heading text if it exists
                if heading.endswith(self.sort_ascending_icon) or heading.endswith(self.sort_descending_icon):
                    self._treeview.heading(col_id, text=heading[:-len(self.sort_descending_icon)])

        # Sort the data
        self.data = sorted(self.data, key=lambda l: l[column_id], reverse=sort_descending)

    def _clear_sort_icons(self):
        """Clear any icons that have been appended to column headings"""
        for col_id in range(self._num_columns):
            heading = self._treeview.heading(col_id)['text']
            if heading.endswith(self.sort_ascending_icon) or heading.endswith(self.sort_descending_icon):
                self._treeview.heading(col_id, text=heading[:-len(self.sort_descending_icon)])

    @property
    def data(self):
        """Gets or sets all data in the table as a list of lists"""
        return [self._treeview.item(line)['values'] for line in self._treeview.get_children()]

    @data.setter
    def data(self, values):
        if not all(type(row) in (list, tuple) for row in values):
            raise ValueError('Table data must be a list of lists')
        if not all(len(row) == self._num_columns for row in values):
            raise ValueError('Could not set table data - the number of columns of the table does not match')

        self.clear()
        for line in values:
            self._treeview.insert('', 'end', values=line)

    @property
    def multiple_selection(self):
        """Gets or sets the ability to select multiple items in the Table

        Allows multiple rows to be selected with shift-click or ctrl-click"""
        return str(self._treeview.cget('selectmode')) == 'extended'

    @multiple_selection.setter
    def multiple_selection(self, multiple):
        mode = 'extended' if multiple else 'browse'
        self._treeview.config(selectmode=mode)
        # Clear the selection if single selection is enabled
        if not multiple:
            self.select_none()

    @property
    def selected(self):
        """Returns the selected data in the table

        Returns:
            The selected row as a list, or a list of lists for multiple selection, or None if no row is selected.
        """
        selected_ids = self._treeview.selection()
        if not selected_ids:
            return None
        if self.multiple_selection:
            return [self._treeview.item(row_id)['values'] for row_id in reversed(selected_ids)]
        else:
            return self._treeview.item(selected_ids)['values']

    @property
    def selected_row(self):
        """Gets or sets the index(es), starting from 0, of the selected row. Returns None if nothing
        is selected. Returns a list of indexes if multiple selections are enabled.
        """
        selected_ids = self._treeview.selection()
        all_ids = self._treeview.get_children()

        if not selected_ids:
            return None
        if self.multiple_selection:
            return [all_ids.index(selected) for selected in selected_ids]
        else:
            return all_ids.index(selected_ids[0])

    @selected_row.setter
    def selected_row(self, index):
        """Adds to the current selection if multiple selection is set"""
        all_rows = self._treeview.get_children()
        if len(self._treeview.get_children()) == 0:
            raise ValueError(f'No items in Table to select')
        if index not in range(len(all_rows)):
            raise ValueError(f'The index must be in the range 0 to {len(all_rows) - 1}. '
                             f'The value of the index specified was {index}.')

        # Clear the current selection if single selection only
        if not self.multiple_selection:
            self.select_none()

        # Select the item specified by the index
        item_id = all_rows[index]
        self._treeview.selection_add(item_id)
        self._treeview.see(item_id)  # Show the selected row (in case it is not be in view)

    def add_row_at(self, index, data):
        """Adds a row of data to the table at a given index

        Args:
            index (int): The index at which to add the row
            data: A list of strings of data to add to the Table

        Raises:
            TypeError: index is not an integer
            TypeError: data is not a list type
            ValueError: the length of data does not match the number of columns in the table
        """

        # Check if location is an integer
        if type(index) != int and index != 'end':
            raise TypeError(f'index must be an integer. The value provided was {index}')
        if not type(data) in (list, tuple):
            raise TypeError(f'row data must be a list')
        # Check if the number of columns in the data is correct
        if len(data) != self._num_columns:
            raise ValueError(f'The number of data arguments given ({len(data)}) does not match '
                             f'the number of columns in the table ({self._num_columns})')

        self._treeview.insert('', index, values=data)

        # Clear any sort icons if new data is added
        self._clear_sort_icons()

    def add_row(self, data):
        """Adds a row of data to the end of the table

        Args:
            data: A list of strings of data to add to the Table
        """
        self.add_row_at('end', data)

    def add_row_to_top(self, data):
        """Adds a row of data to the top of the table

        Args:
            data: A list of strings of data to add to the Table
        """
        self.add_row_at(0, data)

    def clear(self):
        """Removes all data from the table"""
        for row_id in self._treeview.get_children():
            self._treeview.delete(row_id)

    def remove_row(self, index):
        """Removes the specified row from the table

        Args:
            index (int): the index at which to remove the row

        Raises:
            TypeError: index is not an integer
            ValueError: index is not in a valid range
        """
        row_ids = self._treeview.get_children()
        if type(index) != int:
            raise TypeError(f'index must be an integer. The value provided was {index}')
        if index < 0 or index > len(row_ids) - 1:
            raise ValueError(f'The index must be between 0 and {len(row_ids) - 1}. '
                             f'The value of index was {index}')
        row_data = self._treeview.item(row_ids[index])['values']
        self._treeview.delete(row_ids[index])
        return row_data

    def remove_selected(self):
        """Removes the currently selected row from the table

        Returns:
            A list of strings of the data from the table, a list of lists if multiple rows are selected or
                None if no rows are selected
        """
        row_data = self.selected
        self._treeview.delete(*self._treeview.selection())
        return row_data

    def set_column_width(self, column, width):
        """Sets the width in pixels of the specified column, indexed from 0

        Args:
            column (int): The columns to set the width of, indexed from 0
            width (int): The width in pixels of the column

        Raises:
            TypeError: The column number is invalid
            TypeError: The width is invalid
        """
        if type(column) != int or column < 0:
            raise TypeError(f'Column number must be a positive integer. The value given was {column}.')
        if type(width) != int or width <= 0:
            raise TypeError(f'Column width must be a positive integer. The value given was {width}.')
        self._treeview.column(column, width=width)

    def set_column_widths(self, *widths):
        """Sets the width in pixels of all columns of the table

        Args:
            widths: The widths of each column, measured in pixels

        Raises:
            ValueError: The number of arguments does not match the number of columns
        """
        if len(widths) != self._num_columns:
            raise ValueError(f'The number of arguments supplied ({len(widths)}) does not match '
                             f'the number of columns in the table ({self._num_columns})')
        for column, width in enumerate(widths):
            self.set_column_width(column, width)

    def set_column_alignment(self, column, align):
        """Sets the alignment of the content in the specified column, indexed from 0

        Args:
            column (int): The columns to set the alignment of, indexed from 0
            align (str): The alignment value, must be one of 'left', 'center' or 'right'

        Raises:
            TypeError: The column number is invalid
            ValueError: The alignment value was not one of the possible options.
        """
        alignment_mapping = {'left': 'w', 'center': 'center', 'right': 'e'}

        if type(column) != int or column < 0:
            raise TypeError(f'Column number must be a positive integer. The value given was {column}')
        if align not in alignment_mapping.keys():
            raise ValueError(f'Column alignment value must be either "left", "right" or "center". '
                             f'The value provided was "{align}"')
        self._treeview.column(column, anchor=alignment_mapping[align])

    def set_column_alignments(self, *aligns):
        """Sets the alignment of all columns

        Args:
            aligns: The alignment value of each column

        Raises:
            ValueError: The number of arguments does not match the number of columns
        """
        if len(aligns) != self._num_columns:
            raise ValueError(f'The number of arguments supplied ({len(aligns)}) does not match '
                             f'the number of columns in the table ({self._num_columns})')
        for column, align in enumerate(aligns):
            self.set_column_alignment(column, align)

    def select_row(self, index):
        """Selects a given row in the table

        Args:
            index (int): the index of the row to select, starting from 0

        Raises:
            ValueError: there are no rows in the table to select
            ValueError: the index is invalid
        """
        all_rows = self._treeview.get_children()
        if len(self._treeview.get_children()) == 0:
            raise ValueError(f'Table has no rows to select')
        if index not in range(len(all_rows)):
            raise ValueError(f'The index must be between 0 and {len(all_rows) - 1}. '
                             f'The value of the index specified was {index}.')
        row_id = all_rows[index]
        self._treeview.selection_set(row_id)
        self._treeview.see(row_id)  # Show the selected row (in case it is not be in view)

    def select_all(self):
        """Selects all rows of the table if multiple selection is enabled. Has no effect if multiple selection
        is not enabled"""
        if self.multiple_selection:
            self._treeview.selection_set(*self._treeview.get_children())

    def select_none(self):
        """Clears any selected rows in the table"""
        self._treeview.selection_remove(*self._treeview.selection())


class Separator(ttk.Separator, GooeyPieWidget):
    """A horizontal or vertical bar used to add a visual separator between elements"""

    def __init__(self, container, orientation):
        """Create a new Separator, either horizontal or vertical

        Args:
            container: The window or container to which the widget will be added
            orientation: Either 'vertical' or 'horizontal' to specify the orientation of the separator
        """

        # Check that the orientation is a valid value
        if orientation not in ('horizontal', 'vertical'):
            raise ValueError(f"Separator orientation must be either 'horizontal' or 'vertical'")

        GooeyPieWidget.__init__(self, container)
        ttk.Separator.__init__(self, container, orient=orientation)

        # Internal variable set here to ensure orientation is accessible by ContainerBase.add()
        self._orientation = orientation

    def __str__(self):
        return f"<{self._orientation} Separator>"

    def __repr__(self):
        return self.__str__()


class Progressbar(ttk.Progressbar, GooeyPieWidget):
    """Put a description here later

     """

    def __init__(self, container, mode='determinate'):
        """Creates a new ProgressBar widget

        Args
            container: The window or container to which the widget will be added
            mode (str): Optional - the mode of the progress bar, either 'determinate' or 'indeterminate'
        """
        GooeyPieWidget.__init__(self, container)

        self._value = tk.IntVar()
        ttk.Progressbar.__init__(self, container, variable=self._value)
        self.mode = mode

    def __str__(self):
        return f"<Progressbar widget>"

    def __repr__(self):
        return self.__str__()

    @property
    def value(self):
        """Gets or sets the value of the progress bar as a number between 0 and 100"""
        return self._value.get()

    @value.setter
    def value(self, value):
        if type(value) not in (int, float):
            raise ValueError('Progressbar value must be an integer')
        if not (0 <= value <= 100):
            raise ValueError('Progressbar value must be an integer between 0 and 100 (inclusive)')

        self._value.set(value)

    @property
    def mode(self):
        """Gets or sets the mode of the progress bar - either 'determinate' or 'indeterminate'"""
        return self.cget('mode')

    @mode.setter
    def mode(self, mode):
        if mode not in ('determinate', 'indeterminate'):
            raise ValueError("mode must be either 'determinate' or 'indeterminate'")
        self.config(mode=mode)

    @property
    def width(self):
        """Gets or sets the width of the progress bar in pixels"""
        return self.cget('length')

    @width.setter
    def width(self, width):
        if type(width) != int:
            raise ValueError('width must be a positive integer')
        if width <= 0:
            raise ValueError('width must be a positive integer')

        self.config(length=width)


class Date(Container, GooeyPieWidget):
    """For selecting a date using three individual selectors"""

    _month_names = list(calendar.month_name)[1:]
    _month_names_short = [name[:3] for name in _month_names]
    _month_numbers = [str(month_number) for month_number in range(1, 13)]
    _days = list(range(1, 32))
    _date_pattern = re.compile("^\d{4}-\d{1,2}-\d{1,2}$")

    def __init__(self, container):
        """Creates a new Date select widget

        Args:
            container: The window or container to which the widget will be added

        """
        GooeyPieWidget.__init__(self, container)
        Container.__init__(self, container)

        # Default year range: current year +/- 100 years
        self._current_year = datetime.datetime.now().year
        _years = list(range(self._current_year - 100, self._current_year + 101))

        # Create widgets for year, month and day
        self._year_select = Dropdown(self, _years)
        self._year_select.width = 5
        self._month_select = Dropdown(self, self._month_names)
        self._month_select.width = 12
        self._day_select = Dropdown(self, self._days)
        self._day_select.width = 3

        # Widgets as separators if needed
        self._separator_1 = Label(self, '')
        self._separator_2 = Label(self, '')

        # Event listeners for each dropdown to dynamically change the contents of the day
        self._year_select.add_event_listener('select', self._date_change_event)
        self._month_select.add_event_listener('select', self._date_change_event)
        self._day_select.add_event_listener('select', self._date_change_event)

        # Widget order
        self._order = [self._year_select, self._month_select, self._day_select]

        # Whether the widget is rendered with separators, e.g. / or -
        self._separator = None

        # Whether months are displayed as full names, short names or numbers
        self._month_display = 'full'

        # Set to true when the widget is added to the window
        self._added = False

        self._events['change'] = None

    def _init_date_container(self):
        """Adds all widgets to the base container depending on the options set
        Called by the parent container's .add() method
        """

        # Add the separator widgets if required
        if self._separator:
            self._order.insert(1, self._separator_1)
            self._order.insert(3, self._separator_2)

        # Set grid and add each widget (including separators)
        self.set_grid(1, len(self._order))

        # Set appropriate column weights if there are separators
        if self._separator:
            self.set_column_weights(1, 0, 1, 0, 1)

        # Add dropdowns and possibly separators
        for pos, widget in enumerate(self._order):
            # Right margin is 8 unless it's the last widget in the date
            right_margin = 8 if (pos < len(self._order) - 1) else 0
            self.add(widget, 1, pos + 1, margins=(0, right_margin, 0, 0), fill=True)
            widget.lift()  # Sets the correct tab order
        self._added = True

    def _update_day_select(self):
        """When the year or month changes, update the days select that it shows the correct number of days
        for that month"""

        # Save the current day selection and restore/modify it when the days list changes
        current_day_selection = self.day

        # Can only update the days if something is selected for month
        if self.month:
            # Get the days in the month for the selected year or 2000 (a leap year so that Feb 29 is available)
            if self.year:
                days_in_month = calendar.monthrange(self.year,  self.month)[1]
            else:
                days_in_month = calendar.monthrange(2000,  self.month)[1]

            # If the current day list is no longer correct for the given month/year, change it
            if len(self._day_select.items) != days_in_month:
                self._day_select.items = list(range(1, days_in_month + 1))

                # If the previous date selection was bigger than the new highest day, set it to the new highest
                if current_day_selection and current_day_selection >= days_in_month:
                    self.day = days_in_month
                else:
                    self.day = current_day_selection

        else:
            # Restore the day selector to its maximum
            self._day_select.items = self._days
            self.day = current_day_selection

    def __str__(self):
        return f"<Date widget>"

    def __repr__(self):
        return self.__str__()

    @property
    def date(self):
        """Gets or sets the date in the date selector"""
        try:
            selected_date = (int(self._year_select.selected),
                             self._month_select.selected_index + 1,
                             self._day_select.selected_index + 1)
            return datetime.date(*selected_date)
        except TypeError:
            return None

    @date.setter
    def date(self, date):
        invalid_date_msg = f'Dates must be either datetime.date objects or strings of the form YYYY-MM-DD'

        # Check format
        if type(date) not in (datetime.date, datetime.datetime, str):
            raise TypeError(invalid_date_msg)

        if type(date) == str:
            # Check date is of the form YYYY-MM-DD
            if not self._date_pattern.match(date):
                raise ValueError(invalid_date_msg)

            # Get date components
            year, month, day = [int(value) for value in date.split('-')]

            # Validate date
            try:
                datetime.date(year, month, day)
            except ValueError:
                raise ValueError(f'"{date}" is not a valid date')

        else:
            year, month, day = date.year, date.month, date.day

        self.year = year
        self.month = month
        self._update_day_select()
        self.day = day

    @property
    def date_str(self):
        """Get the selected date as a string"""
        return str(self.date) if self.date else None

    @property
    def year(self):
        """Gets or sets the selected year"""
        if self._year_select.selected:
            return int(self._year_select.selected)
        else:
            return None

    @year.setter
    def year(self, year):
        if year is not None:
            # Expand the year selector range if needed
            if year < int(self._year_select.items[0]):
                self._year_select.items = list(range(year, int(self._year_select.items[-1]) + 1))
            if year > int(self._year_select.items[-1]):
                self._year_select.items = list(range(int(self._year_select.items[0]), year + 1))

            self._year_select.selected = str(year)
        else:
            self._year_select.selected = None

        self._update_day_select()

    @property
    def month(self):
        """Gets or sets the selected month as an integer from 1 to 12"""
        if self._month_select.selected:
            return self._month_select.selected_index + 1
        else:
            return None

    @month.setter
    def month(self, month):
        if month is not None:
            if type(month) != int:
                raise TypeError('Month must be an integer from 1 to 12.')
            if not 1 <= month <= 12:
                raise ValueError('Month must be an integer from 1 to 12.')

            self._month_select.selected_index = month - 1
        else:
            self._month_select.selected = None

        self._update_day_select()

    @property
    def month_name(self):
        """Gets or sets the full name of the currently selected month"""
        if self._month_select.selected:
            # Month select could be month numbers or month names
            return self._month_names[self._month_select.selected_index]
        else:
            return None

    @month_name.setter
    def month_name(self, month_name):
        if month_name in self._month_names:
            # Month name could be the complete name
            self._month_select.selected_index = self._month_names.index(month_name)
        elif month_name in self._month_names_short:
            # Month name could be a shortened name
            self._month_select.selected_index = self._month_names_short.index(month_name)
        else:
            raise ValueError(f'"{month_name}" is not a valid month')

    @property
    def day(self):
        """Gets or sets the selected day in the date widget"""
        if self._day_select.selected:
            return int(self._day_select.selected)
        else:
            return None

    @day.setter
    def day(self, day):
        if day is not None:
            # Check if the day is an integer
            if type(day) != int or day < 1:
                raise ValueError('Day must be a positive integer')
            if day > 31:
                raise ValueError(f'{day} is not a valid day')
            if self.month and day > int(self._day_select.items[-1]):
                raise ValueError(f'Day {day} is not valid for this month')

            self._day_select.selected = str(day)
        else:
            self._day_select.selected = None

    def set_selector_order(self, selector_order):
        """Specifies the order of each selector in the date widget

        Args:
            selector_order (str): Must be a string of length 3 consisting of 'D', 'M', 'Y'

        Raises:
            ValeError: if the argument is not of the correct format
            GooeyPieError: if the date widget has already been added to the window
        """
        if self._added:
            raise GooeyPieError('The selector order cannot be changed after the widget has been added to the window')
        if selector_order not in ('DMY', 'DYM', 'MDY', 'MYD', 'YDM', 'YMD'):
            raise ValueError('The selector order must be a string consisting of a single "D", "M" and "Y", specifying'
                             'the order of the date selectors')
        widgets = {'Y': self._year_select, 'M': self._month_select, 'D': self._day_select}
        self._order = [widgets[key] for key in selector_order]

    @property
    def disabled(self):
        """Gets or set the state of the date widget"""
        return self.year_disabled and self.month_disabled and self.day_disabled

    @disabled.setter
    def disabled(self, state):
        self.year_disabled = self.month_disabled = self.day_disabled = bool(state)
        self._separator_1 = self._separator_1 = bool(state)

    @property
    def year_disabled(self):
        """Gets or sets the state of the year select of the date widget. When disabled, the year can still be changed
        programmatically"""
        return self._year_select.disabled

    @year_disabled.setter
    def year_disabled(self, state):
        self._year_select.disabled = bool(state)

    @property
    def month_disabled(self):
        """Gets or sets the state of the month select of the date widget. When disabled, the month can still be changed
        programmatically"""
        return self._month_select.disabled

    @month_disabled.setter
    def month_disabled(self, state):
        self._month_select.disabled = bool(state)

    @property
    def day_disabled(self):
        """Gets or sets the state of the day select of the date widget. When disabled, the day can still be changed
        programmatically"""
        return self._day_select.disabled

    @day_disabled.setter
    def day_disabled(self, state):
        self._day_select.disabled = bool(state)

    def set_separator(self, char):
        """Sets the separator character to use between the individual date selectors. Default is None.

        Args:
            char (str): A string to use as the separator between the individual date selectors

        Raises:
            GooeyPieError: If the method is called after the widget has been added to the window
        """
        if self._added:
            raise GooeyPieError('The date separator cannot be changed or set '
                                'after the widget has been added to the window')
        self._separator = char
        self._separator_1.text = self._separator_2.text = char

    def set_month_display(self, display_mode):
        """Sets how the months will be displayed in the month selector

        Args:
            display_mode: either 'full' (full month names), 'short' (3 letter abbreviations) or 'numeric'
                (integer from 1 to 12)

        Raises:
            GooeyPieError: the date format has already been added to the window
            ValueError: the display_mode is not one of 'full', 'short' or 'numeric'
        """
        if self._added:
            raise GooeyPieError('Month display mode cannot be changed after the widget has been added to the window')
        if display_mode not in ('full', 'short', 'numeric'):
            raise ValueError('Month display must be either "full", "short" or "numeric"')

        month_display = {'full': self._month_names, 'short': self._month_names_short, 'numeric': self._month_numbers}
        self._month_select.items = month_display[display_mode]
        self._month_select.width = max([len(month) for month in self._month_select.items]) + 1

    @property
    def year_range(self):
        """Gets or sets the initial bounds of the year selector

        If the date is later set to a year outside of this range the selector will expand to fit.
        """
        return [int(self._year_select.items[0]), int(self._year_select.items[-1])]

    @year_range.setter
    def year_range(self, year_range):
        current_selection = self.year

        try:
            start_year, end_year = year_range
        except (TypeError, ValueError):
            raise TypeError('year_range must be a list of length 2 (the smallest and largest years to display)')

        if type(start_year) != int or type(end_year) != int:
            raise TypeError('Year range values must be positive integers')
        if start_year <= 0 or end_year <= 0:
            raise ValueError('Year range values must be positive integers')
        if start_year > end_year:
            raise ValueError('Invalid year range - smallest year must be before largest year')

        self._year_select.items = list(range(start_year, end_year + 1))

        # Restore the selection or choose the closest
        if current_selection is not None:
            if current_selection < start_year:
                self.year = start_year
            elif current_selection > end_year:
                self.year = end_year
            else:
                self.year = current_selection

    def set_today(self):
        """Sets the value of the date widget to the current day"""
        self.date = datetime.date.today()

    def add_days(self, days):
        """Adds a given number of days to the current date"""
        if not all((self.year, self.month, self.day)):
            raise GooeyPieError(f'Cannot add or subtract days from {self} because no date has been set')
        self.date += datetime.timedelta(days=days)

    def subtract_days(self, days):
        """Subtracts a given number of days to the current date"""
        self.add_days(-days)

    def add_months(self, months):
        """Adds a given number of months to the current date"""
        if not all((self.year, self.month, self.day)):
            raise GooeyPieError(f'Cannot add or subtract months from {self} because no date has been set')
        years_to_add = int(months / 12)
        months_to_add = months % 12
        if self.month + months_to_add > 12:
            years_to_add += 1
            months_to_add -= 12

        self.year += years_to_add
        self.month += months_to_add
        self._update_day_select()

    def subtract_months(self, months):
        """Subtracts a given number of months to the current date"""
        self.add_months(-months)

    def add_years(self, years):
        """Adds a given number of years to the current date"""
        if not all((self.year, self.month, self.day)):
            raise GooeyPieError(f'Cannot add or subtract years from {self} because no date has been set')
        self.year = int(self._year_select.selected) + years

    def subtract_years(self, years):
        """Subtracts a given number of years to the current date"""
        self.add_years(-years)

    def clear(self):
        """Clears all select elements of the date widget"""
        self.year = None
        self.month = None
        self.day = None
        self._update_day_select()


class Textbox(Container, GooeyPieWidget):
    """Textbox widget"""

    def __init__(self, container, width=20, height=5):
        """Create a new Textbox widget

        Args:
            width (int): The width of the Textbox in characters
            height (int): The height of the Textbox in lines
        """
        Container.__init__(self, container)

        # Set container to fill cell
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Create tk Text widget
        self._tk_text_widget = tk.Text(self, width=width, height=height)
        self._tk_text_widget.configure(borderwidth=1,
                                       relief='flat',
                                       font=font.nametofont('TkDefaultFont'),
                                       wrap='word',
                                       highlightthickness=1,
                                       undo=True)

        # Different border colour names for Windows and Mac
        # https://www.tcl.tk/man/tcl8.6/TkCmd/colors.htm
        if OS == 'Windows':
            self._tk_text_widget.configure(highlightbackground='systemGrayText')
            self._tk_text_widget.configure(highlightcolor='systemHighlight')
        if OS == "Mac":
            self._tk_text_widget.configure(highlightbackground='systemBevelActiveLight')
            self._tk_text_widget.configure(highlightcolor='systemHighlight')

        self._tk_text_widget.bind('<Tab>', self.focus_next_widget)
        self._tk_text_widget.bind('<Shift-Tab>', self.focus_previous_widget)
        self._tk_text_widget.bind('<Control-Tab>', self.insert_tab)

        # Create and configure vertical scrollbar
        self._scrollbar_vertical = tk.Scrollbar(self, orient='vertical')
        self._scrollbar_vertical.config(command=self._tk_text_widget.yview)
        self._tk_text_widget.config(yscrollcommand=self._scrollbar_vertical.set)
        self._scrollbar_visibility = 'auto'
        self._scrollbar_is_hidden = True

        # Add to parent Container
        self._tk_text_widget.grid(row=0, column=0, sticky='nsew')
        self._scrollbar_vertical.grid(row=0, column=1, sticky='nsew')

        # If the textbox changes size, update the scrollbar
        self._tk_text_widget.bind('<Configure>', self._configure)

        # Initialise event handling
        GooeyPieWidget.__init__(self, container)
        self._events['change'] = None

        # Variable used in the change event on the textbox
        self._sentinel = ''

        # Set an event to always fire to update the scrollbar when new text is added
        self._tk_text_widget.bind('<KeyRelease>', self._newtextbox_change_event)

    def __str__(self):
        return f"""<Textbox widget>"""

    def __repr__(self):
        return self.__str__()

    def _configure(self, _event):
        """Called when the <Configure> event fires on the textbox"""
        if self._scrollbar_visibility == 'auto':
            self._update_scrollbar()

    def _update_scrollbar(self):
        """Updates the visibility of the scrollbar in response to resize events, changes to the contents
        of the textbox and changes to the scrollbar setting using the scrollbar property.
        """
        self._set_scrollbar()

        # Additional calls are made here as the scrollbar does not reliably update immediately,
        # meaning that it may not appear or disappear as needed when scrollbar visibility set to 'auto'
        self.after(200, self._set_scrollbar)
        self.after(500, self._set_scrollbar)

    def _set_scrollbar(self):
        """Sets the scrollbar visibility based on the contents of the textbox"""
        scrollbar_value = self._scrollbar_vertical.get()
        if scrollbar_value == (0.0, 1.0) or scrollbar_value == (0.0, 0.0, 0.0, 0.0):
            if not self._scrollbar_is_hidden:
                self._hide_scrollbar()
        else:
            if self._scrollbar_is_hidden:
                self._show_scrollbar()

    def _hide_scrollbar(self):
        """Hides the scrollbar from the Textbox"""
        self._scrollbar_vertical.grid_remove()
        self._tk_text_widget.grid_remove()
        self._tk_text_widget.grid(row=0, column=0, sticky='nsew', columnspan=2)
        self._scrollbar_is_hidden = True

    def _show_scrollbar(self):
        """Shows the scrollbar on the side of the Textbox"""
        self._tk_text_widget.grid_remove()
        self._tk_text_widget.grid(row=0, column=0, sticky='nsew', columnspan=1)
        self._scrollbar_vertical.grid()
        self._scrollbar_is_hidden = False

    @property
    def scrollbar(self):
        """Gets or sets the scrollbar setting. Must be one of either 'auto', 'hidden' or 'visible'"""
        return self._scrollbar_visibility

    @scrollbar.setter
    def scrollbar(self, setting):
        if setting not in ('auto', 'visible', 'hidden'):
            raise ValueError("Invalid scrollbar option - must be set to 'auto', 'hidden' or 'visible'")

        self._scrollbar_visibility = setting
        if setting == 'visible':
            self._show_scrollbar()
        elif setting == 'hidden':
            self._hide_scrollbar()
        else:
            # Auto scrollbar - call the update method to determine if it should be shown or hidden
            self._update_scrollbar()

    @staticmethod
    def focus_next_widget(event):
        """Overrides the default behaviour of inserting a tab character in a textbox instead of
        changing focus to the next widget
        """
        event.widget.tk_focusNext().focus()
        return 'break'

    @staticmethod
    def focus_previous_widget(event):
        """Overrides the default behaviour of inserting a tab character in a textbox instead of
        changing focus to the previous widget
        """
        event.widget.tk_focusPrev().focus()
        return 'break'

    @staticmethod
    def insert_tab(event):
        """Allows the user to insert a tab character into the textbox with ctrl/cmd-tab"""
        event.widget.insert('current', '\t')
        return 'break'

    @property
    def width(self):
        """Gets or sets the width of the Textbox in characters"""
        return self._tk_text_widget.cget('width')

    @width.setter
    def width(self, cols):
        if type(cols) != int or int(cols) < 1:
            raise ValueError('Width must be a positive integer')
        self._tk_text_widget.configure(width=cols)

    @property
    def height(self):
        """Gets or sets the height of the Textbox in lines"""
        return self._tk_text_widget.cget('width')

    @height.setter
    def height(self, rows):
        if type(rows) != int or int(rows) < 1:
            raise ValueError('Height must be a positive integer')
        self._tk_text_widget.configure(height=rows)

    @property
    def selected(self):
        """Gets any selected text"""
        ranges = self._tk_text_widget.tag_ranges('sel')
        if ranges:
            return self._tk_text_widget.get(*ranges)
        else:
            return ''

    @property
    def text(self):
        """Gets or sets the contents of the Textbox"""

        # Strip the trailing newline added by tkinter
        return self._tk_text_widget.get('1.0', 'end')[:-1]

    @text.setter
    def text(self, text):
        self._tk_text_widget.delete('1.0', 'end')
        self._tk_text_widget.insert('1.0', text)

        self._newtextbox_change_event(None)

    def clear(self):
        """Clear the contents of the Textbox"""
        self._tk_text_widget.delete('1.0', 'end')

        # Process the change event
        self._newtextbox_change_event(None)

    def prepend(self, text):
        """Adds text to the beginning of the Textbox

        Args:
            text (str): The text to add to the Textbox
        """
        self.text = f'{text}{self.text}'
        self.scroll_to_start()

    def prepend_line(self, text):
        """Adds text plus a newline character to the beginning of the Textbox

        Args:
            text (str): The text to add to the Textbox
        """
        self.prepend(f'{text}\n')
        self.scroll_to_start()

    def append(self, text):
        """Adds text to the end of the Textbox

        Args:
            text (str): The text to add to the Textbox
        """
        self.text = f'{self.text}{text}'
        self.scroll_to_end()

    def append_line(self, text):
        """Adds to the Textbox on a new line

        Args:
            text (str): The text to add to the Textbox
        """

        # Only add a newline if there is already text there
        if self.text:
            self.append('\n')

        self.append(text)
        self.scroll_to_end()

    def scroll_to_start(self):
        """Scrolls to the top of the Textbox"""
        self._tk_text_widget.yview_moveto(0.0)

    def scroll_to_end(self):
        """Scrolls to the top of the Textbox"""
        self._tk_text_widget.yview_moveto(1.0)
