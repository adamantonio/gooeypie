import os
import tkinter
from tkinter import messagebox
from tkinter import filedialog

from .widgets import *

__version__ = "0.3.0"


class WindowBase(Container):
    """Base class for GooeyPieApp and Window classes
    Provides functions for window options like size, title and menus
    """
    def __init__(self, root, title, *args):
        """Creates the base window object"""

        self._root = root   # for the class GooeyPieApp, this is the tkinter.Tk() instance
        self._root.title(title)  # title of the window

        Container.__init__(self, root)

        self._menubar = tk.Menu(root)
        self._menu = {}  # internal dictionary for menu objects
        self._menu_tkcontrols = {}  # internal dictionary of tk control variables for menu radio buttons and check
        self._preferred_size = [0, 0]  # users preferred size (actual size may be larger to fit in all widgets)

        self._interval_callback = None  # Dictionary for set_interval callback (callback and delay)
        self._timeout = None  # Identifier used when calling set_timeout, used by clear_timeout
        self._icon = None  # Window icon
        self._resizable = [True, True]

        self._on_close_callback = None  # Function called when window is closed
        self._default_close = self._root.destroy  # Default destroy for apps, overridden to hide() for windows
        self._root.protocol("WM_DELETE_WINDOW", self._handle_window_close)

        self.storage = {}  # Global storage variable

    def _init_window(self):
        """Sets up the window with the users size preferences and menus"""

        # Add the menu bar to the window if there is one
        if self._menu:
            self._root.config(menu=self._menubar)

        # Add the main Container to the window
        self.pack(fill='both', expand=True, padx=0, pady=0)

        # Call update() to get width and height info, then set the min size to these values
        # Prevents window resizing covering up the widgets.
        self._root.update_idletasks()
        min_width = self._root.winfo_width()
        min_height = self._root.winfo_height()
        self._root.minsize(min_width, min_height)

        # Make the window larger than the minimum if it has been set by the user AND they haven't made it too small
        width = max(self._preferred_size[0], min_width)
        height = max(self._preferred_size[1], min_height)
        self._root.geometry(f'{width}x{height}')

    def _handle_window_close(self):
        """Called whenever a window is closed with the [X] or associated keyboard shortcut"""
        if self._on_close_callback is None:
            confirm_exit = True
        else:
            confirm_exit = self._on_close_callback()

        if confirm_exit:
            self._default_close()

    @property
    def title(self):
        """Get or set the title of the window"""
        return self._root.title()

    @title.setter
    def title(self, text):
        self._root.title(text)

    def set_size(self, width, height):
        """Sets the size of the window

        Args:
            width (int): The width of the window in pixels
            height (int): The height of the window in pixels

        """
        self._preferred_size = [width, height]

    @property
    def width(self):
        """Gets or sets the preferred width of the window.

        The actual width might be wider than the set value in order to fit all widgets
        """

        return self._root.winfo_width()

    @width.setter
    def width(self, value):
        if value == 'auto':
            value = 0

        self._preferred_size[0] = value

        # Normally width is set before the window is initialised/displayed, and the call to root.geometry() is made
        # during self._init(). If the window is already visible, change the size immediately.
        # Note: size will not change if the window is minimised (iconified)
        if self._root.winfo_ismapped():
            self._root.geometry(f'{value}x{self.height}')

    @property
    def height(self):
        return self._root.winfo_height()

    @height.setter
    def height(self, value):
        """Gets or sets the preferred height of the window. The actual height might be taller than the set value
        in order to fit all widgets
        """
        if value == 'auto':
            value = 0

        self._preferred_size[1] = value

        # Normally height is set before the window is initialised/displayed, and the call to root.geometry() is made
        # during self._init(). If the window is already visible, change the size immediately.
        # Note: size will not change if the window is minimised (iconified)
        if self._root.winfo_ismapped():
            self._root.geometry(f'{self.width}x{value}')

    @property
    def resizable_horizontal(self):
        """Gets or sets whether the window can be resized horizontally"""
        return self._resizable[0]

    @resizable_horizontal.setter
    def resizable_horizontal(self, value):
        self._resizable[0] = bool(value)
        self._root.resizable(bool(value), self._resizable[1])

    @property
    def resizable_vertical(self):
        """Gets or sets whether the window can be resized vertically"""
        return self._resizable[0]

    @resizable_vertical.setter
    def resizable_vertical(self, value):
        self._resizable[1] = bool(value)
        self._root.resizable(self._resizable[0], bool(value))

    def set_resizable(self, resize):
        """Determines whether the user can change the size of the window

        Args:
            resize (bool): Whether the window can be resized or not by the user
        """
        resize = bool(resize)
        self._resizable = [resize, resize]
        self._root.resizable(resize, resize)

    def _create_menu(self, menu_path, parent):
        """Creates a tk menu object if it does not exist and adds it to the internal dictionary of menu objects
        menu_path is either the name of a top level menu (string) or a tuple (top_level_name, sub_menu_name)
        parent is either self._menubar (root menu) or the parent menu for submenus
        """

        # The name of the menu is either the menu_path itself (for top level menus) or if creating
        # a submenu, it is the last element in the tuple for submenus
        menu_name = menu_path if type(menu_path) is str else menu_path[-1]

        if menu_path not in self._menu:
            self._menu[menu_path] = tk.Menu(parent, tearoff=0)
            parent.add_cascade(label=menu_name, menu=self._menu[menu_path])

    def _create_menu_item(self, menu_path, item, callback):
        """Create a normal menu item in the given menu path.

        The path is either a string for the name of the top level menu name (e.g. File)
        or a 2-tuple representing a submenu (e.g. Settings -> Language)
        GooeyPie only supports one level of nesting (menu or sub menu)
        """

        self._menu[menu_path].add_command(label=item)

        # Add callback function to item
        if callback is not None:
            current = self._menu[menu_path].index('end')

            try:
                # Check that the callback accepts a single argument and
                assert callback.__code__.co_argcount == 1
            except AssertionError:
                raise ValueError(f'{callback.__name__}() must accept a single argument')
            except AttributeError:
                raise ValueError(f'A callback function that accepts a single argument must be specified')

            # Construct item path for passing to the callback eg ("File", "Open") or ("Edit", "Copy", "Formatting")
            if type(menu_path) is str:
                item_path = (menu_path, item)
            else:
                item_path = menu_path + (item,)
            # self._menu[menu_path].entryconfigure(current, command=partial(callback, item_path))
            self._menu[menu_path].entryconfigure(current, command=partial(self._menu_select_callback,
                                                                          item_path, callback))

    def _create_menu_radios(self, menu_path, options, callback):
        """Creates a group of radio button menu items in either a top level menu or a submenu"""

        if type(menu_path) == str:
            # Menu radios - a tuple of the form (menu, option1, option2, ...) forms the name of the control variable
            control_var_key = (menu_path,) + tuple(options)
        else:
            # Submenu radios - a tuple of the form (menu, submenu, option1, option2, ...)
            # forms the name of the control variable
            control_var_key = menu_path + tuple(options)

        # Create the associated control variable and set the default value to the first option
        self._menu_tkcontrols[control_var_key] = tk.StringVar(value=options[0])

        if callback is not None:
            assert callback.__code__.co_argcount == 1
            for option in options:
                self._menu[menu_path].add_radiobutton(label=option, variable=self._menu_tkcontrols[control_var_key],
                                                      command=partial(self._menu_radio_select_callback, menu_path,
                                                                      control_var_key, callback))
        else:
            # Add without callback
            for option in options:
                self._menu[menu_path].add_radiobutton(label=option, variable=self._menu_tkcontrols[control_var_key])

    def _menu_select_callback(self, menu_path, callback):
        """Handles callbacks for regular menu items"""
        event = GooeyPieEvent('menu', self, menu=menu_path)
        callback(event)

    def _menu_radio_select_callback(self, menu_path, control_var, callback):
        """Handles callbacks for menu radio items"""
        selected_option = self._menu_tkcontrols[control_var].get()
        if type(menu_path) == str:
            # If the radio item is in a top level menu - e.g. ('Font', 'Bold')
            menu_str = (menu_path, selected_option)
        else:
            # If the radio item is in a submenu - e.g. ('Format', 'Font', 'Bold')
            menu_str = (menu_path[0], menu_path[1], selected_option)

        event = GooeyPieEvent('menu', self, menu=menu_str)
        callback(event)

    def _create_menu_checkbutton(self, menu_path, item, callback, state):
        """Adds a checkbutton menu item"""

        # The item_path, eg ("File", "Open") or ("Edit", "Copy", "Formatting"), used for the callback and control var
        if type(menu_path) is str:
            item_path = (menu_path, item)
        else:
            item_path = menu_path + (item,)

        self._menu_tkcontrols[item_path] = tk.BooleanVar(value=state)
        self._menu[menu_path].add_checkbutton(label=item, variable=self._menu_tkcontrols[item_path])

        if callback is not None:
            assert callback.__code__.co_argcount == 1
            self._menu[menu_path].entryconfigure(self._menu[menu_path].index('end'),
                                                 command=partial(self._menu_select_callback, item_path, callback))

    def _change_menu_state(self, menu_path, item, state):
        """Enables or disables a menu item or submenu"""
        menu = self._menu[menu_path]
        menus = [menu.entrycget(index, 'label') for index in range(menu.index('end') + 1) if
                 menu.type(index) != 'separator']

        if item not in menus:
            raise ValueError(f"'{item}' is not a menu item under the menu {menu_path}")
        self._menu[menu_path].entryconfigure(item, state=state)

    def add_menu_item(self, menu, item, event_function):
        """Adds a menu item to the window to a top level menu

        Args:
            menu (str): The top level menu name
            item (str): The menu item
            event_function (function): The function to call when the menu item is selected (must accept a
                single argument)
        """
        self._create_menu(menu, self._menubar)
        self._create_menu_item(menu, item, event_function)

    def add_submenu_item(self, menu, submenu, item, event_function):
        """Adds a menu item to the window to a submenu

        Args:
            menu (str): The top level menu name
            submenu (str): The name of the submenu under menu
            item (str): menu item under menu -> submenu
            event_function (function): The function to call when the menu item is selected (must accept a
                single argument)
        """
        self._create_menu(menu, self._menubar)
        self._create_menu((menu, submenu), self._menu[menu])
        self._create_menu_item((menu, submenu), item, event_function)

    def add_menu_radios(self, menu, options, event_function):
        """Adds a group of radio menu items to a top level menu

        A menu radio group always has one item checked. If another item in the group is selected, it becomes checked
        and the previously checked item becomes unchecked.

         Args:
            menu (str): The top level menu name
            options (list): A list of the menu items that will act as a group. By default, the first item
                will be checked.
            event_function (function): The event function to call when any of the options are selected (The current
                selection does not have to change for the event function to fire).
        """
        self._create_menu(menu, self._menubar)
        self._create_menu_radios(menu, options, event_function)

    def add_submenu_radios(self, menu, submenu, options, event_function):
        """Add a group of radio menu items to a submenu

        Args:
            menu (str): The top level menu name
            submenu (str): The name of the submenu under menu
            options (list): A list of the menu items that will act as a group. By default, the first item
                will be checked.
            event_function (function): The event function to call when any of the options are selected (The current
                selection does not have to change for the event function to fire).
        """
        self._create_menu(menu, self._menubar)
        self._create_menu((menu, submenu), self._menu[menu])
        self._create_menu_radios((menu, submenu), options, event_function)

    def add_menu_checkbox(self, menu, item, event_function, checked=False):
        """Adds a checkbox menu item to a top level menu

        A checkbox menu item can have a check mark next to it indicating that it is checked. Selecting a checkbox
        menu item toggles its state between checked and unchecked

        Args:
            menu (str): The top level menu name
            item (str): The name of the checkbox menu item
            event_function (function): The event function to call when any of the options are selected (The current
                selection does not have to change for the event function to fire).
            checked (bool): Whether the item is initially checked or not
        """
        self._create_menu(menu, self._menubar)
        self._create_menu_checkbutton(menu, item, event_function, checked)

    def add_submenu_checkbox(self, menu, submenu, item, event_function, checked=False):
        """Adds a checkbox menu item to a submenu

        Args:
            menu (str): The top level menu name
            submenu (str): The name of the submenu under menu
            item (str): The name of menu item
            event_function (function): The event function to call when any of the options are selected (The current
                selection does not have to change for the event function to fire).
            checked (bool): Whether the item is initially checked or not
        """
        self._create_menu(menu, self._menubar)
        self._create_menu((menu, submenu), self._menu[menu])
        self._create_menu_checkbutton((menu, submenu), item, event_function, checked)

    def add_menu_separator(self, menu):
        """Adds a separator to a menu

        Args:
            menu (str): The top level menu name

        Raises:
            ValueError: The top level menu does not exist
        """
        if menu not in self._menu:
            raise ValueError(f"No top level menu '{menu}' found")
        self._menu[menu].add_separator()

    def add_submenu_separator(self, menu, submenu):
        """Adds a separator to a submenu

        Args:
            menu (str): The top level menu name
            submenu (str): The name of the submenu under menu

        Raises:
            ValueError: The menu path (menu -> submenu) does not exist
        """
        if (menu, submenu) not in self._menu:
            raise ValueError(f"No submenu '{submenu}' found under menu '{menu}' found")
        self._menu[(menu, submenu)].add_separator()

    def disable_menu(self, menu):
        """Disables a top level menu

        Args:
            menu (str): The name of the top level menu

        Raises:
            ValueError: menu is not a top level menu
        """
        if menu not in self._menu:
            raise ValueError(f"'{menu}' is not a top level menu")
        self._menubar.entryconfigure(menu, state='disabled')

    def enable_menu(self, menu):
        """Enables a top level menu

        Args:
            menu (str): The name of the top level menu

        Raises:
            ValueError: menu is not a top level menu
        """
        if menu not in self._menu:
            raise ValueError(f"'{menu}' is not a top level menu")
        self._menubar.entryconfigure(menu, state='normal')

    def disable_menu_item(self, menu, item):
        """Disables a menu item

        Args:
            menu (str): The top level menu name
            item (str): The name of the menu item

        Raises:
            ValueError: menu is not a top level menu
        """
        if menu not in self._menu:
            raise ValueError(f"'{menu}' is not a top level menu")
        self._change_menu_state(menu, item, 'disabled')

    def enable_menu_item(self, menu, item):
        """Enables a menu item

        Args:
            menu (str): The top level menu name
            item (str): The name of the menu item

        Raises:
            ValueError: menu is not a top level menu
        """
        if menu not in self._menu:
            raise ValueError(f"'{menu}' is not a top level menu")
        self._change_menu_state(menu, item, 'normal')

    def disable_submenu_item(self, menu, submenu, item):
        """Disables a submenu item

        Args:
            menu (str): The top level menu name
            submenu (str): The name of the submenu under menu
            item (str): The name of the menu item

        Raises:
            ValueError: menu is not a top level menu
            ValueError: submenu is not a menu under menu
        """
        if menu not in self._menu:
            raise ValueError(f"'{menu}' is not a top level menu")
        if (menu, submenu) not in self._menu:
            raise ValueError(f"'{submenu}' is not a submenu under '{menu}'")
        self._change_menu_state((menu, submenu), item, 'disabled')

    def enable_submenu_item(self, menu, submenu, item):
        """Enables a submenu item

        Args:
            menu (str): The top level menu name
            submenu (str): The name of the submenu under menu
            item (str): The name of the menu item

        Raises:
            ValueError: menu is not a top level menu
            ValueError: submenu is not a menu under menu
        """
        if menu not in self._menu:
            raise ValueError(f"'{menu}' is not a top level menu")
        if (menu, submenu) not in self._menu:
            raise ValueError(f"'{submenu}' is not a submenu under '{menu}'")
        self._change_menu_state((menu, submenu), item, 'normal')

    def set_menu_radio(self, menu, options, item):
        """Selects a particular item in a group of radio menu items

        Args:
            menu (str): The top level menu name
            options (list): The list of all the radio menu items
            item (str): The item in options to set as the selected item

        Raises:
            ValueError: The radio menu radio items do not exist
            ValueError: The item is not one of the options
        """
        control_var_key = (menu,) + tuple(options)
        if control_var_key not in self._menu_tkcontrols:
            raise ValueError(f"Could not find radio menu items {options} in '{menu}'")
        if item not in options:
            raise ValueError(f"'{item}' must be one of {options}")

        self._menu_tkcontrols[control_var_key].set(item)

    def set_submenu_radio(self, menu, submenu, options, item):
        """Selects a particular item in a group of radio menu items in a submenu

        Args:
            menu (str): The top level menu name
            submenu (str): The name of the submenu under menu
            options (list): The list of all the radio menu items
            item (str): The item in options to set as the selected item

        Raises:
            ValueError: The radio menu radio items do not exist
            ValueError: The item is not one of the options
        """
        control_var_key = (menu, submenu) + tuple(options)
        if control_var_key not in self._menu_tkcontrols:
            raise ValueError(f"Could not find radio menu items {options} in '{menu}' -> '{submenu}'")
        if item not in options:
            raise ValueError(f"'{item}' must be one of {options}")

        self._menu_tkcontrols[control_var_key].set(item)

    def get_menu_radio(self, menu, options):
        """Returns the selected radio menu item under a top level menu

        Args:
            menu (str): The top level menu name
            options (list): The list of all the radio menu items

        Returns:
            str: The menu item in options that is currently selected

        Raises:
            ValueError: The options do not exist as a radio menu group under menu
        """
        control_var_key = (menu,) + tuple(options)
        if control_var_key not in self._menu_tkcontrols:
            raise ValueError(f"Could not find radio menu items {options} in '{menu}'")

        return self._menu_tkcontrols[control_var_key].get()

    def get_submenu_radio(self, menu, submenu, options):
        """Returns the selected radio menu item under a submenu

        Args:
            menu (str): The top level menu name
            submenu (str): The name of the submenu under menu
            options (list): The list of all the radio menu items

        Returns:
            str: The menu item in options that is currently selected

        Raises:
            ValueError: The options do not exist as a radio menu group under menu -> submenu
        """
        control_var_key = (menu, submenu) + tuple(options)
        if control_var_key not in self._menu_tkcontrols:
            raise ValueError(f"Could not find radio menu items {options} in '{menu}' -> '{submenu}'")

        return self._menu_tkcontrols[control_var_key].get()

    def get_menu_checkbox(self, menu, item):
        """Returns the state of a checkbox menu item under a top level menu

        Args:
            menu (str): The top level menu name
            item (str): The item in menu to

        Returns:
            bool: The state of the checkbox

        Raises:
            ValueError: The item does not exist as a checkbox menu item under menu
        """
        control_var_key = (menu, item)
        if control_var_key not in self._menu_tkcontrols:
            raise ValueError(f"Could not find checkbox item '{item}' in '{menu}'")

        return self._menu_tkcontrols[control_var_key].get()

    def set_menu_checkbox(self, menu, item, state):
        """Set the state of a checkbox menu item under a top level menu

        Args:
            menu (str): The top level menu name
            item (str): The item in menu to
            state (bool): The state of the checkbox

        Raises:
            ValueError: The item does not exist as a checkbox menu item under menu
        """
        control_var_key = (menu, item)
        if control_var_key not in self._menu_tkcontrols:
            raise ValueError(f"Could not find checkbox item '{item}' in '{menu}'")

        self._menu_tkcontrols[control_var_key].set(bool(state))

    def get_submenu_checkbox(self, menu, submenu, item):
        """Returns the state of a checkbox menu item under a submenu

        Args:
            menu (str): The top level menu name
            submenu (str): The name of the submenu under menu
            item (str): The item in menu to

        Returns:
            bool: The state of the checkbox

        Raises:
            ValueError: The item does not exist as a checkbox menu item under menu
        """
        control_var_key = (menu, submenu, item)
        if control_var_key not in self._menu_tkcontrols:
            raise ValueError(f"Could not find checkbox menu item '{item}' in '{menu}' -> '{submenu}'")

        return self._menu_tkcontrols[control_var_key].get()

    def set_submenu_checkbox(self, menu, submenu, item, state):
        """Set the state of a checkbox menu item under a submenu

        Args:
            menu (str): The top level menu name
            submenu (str): The name of the submenu under menu
            item (str): The item in menu to
            state (bool): The state of the checkbox

        Raises:
            ValueError: The item does not exist as a checkbox menu item under menu -> submenu
        """
        control_var_key = (menu, submenu, item)
        if control_var_key not in self._menu_tkcontrols:
            raise ValueError(f"Could not find checkbox menu item '{item}' in '{menu}' -> '{submenu}'")

        self._menu_tkcontrols[control_var_key].set(bool(state))

    def on_close(self, close_function):
        """Registers a function to be called when the window is closed

        Args:
            close_function (function): The function called when the user closes the window. This function must
                return a boolean value to confirm exit. If the function returns False, the window will not close.

        """
        if not callable(close_function):
            raise TypeError('The argument to the on_close method must be a function')
        self._on_close_callback = close_function

    @staticmethod
    def _check_icon(icon):
        if icon not in ('info', 'question', 'warning', 'error'):
            raise ValueError("The icon for the confirm popup must be one of 'info', 'question', 'warning' or 'error'")

    def alert(self, title, message, icon='info'):
        """Launches an alert popup window

        Alert popups display a message with a single 'OK' button. No value is returned when the user dismisses
        the message

        Args:
            title (str): The text on the title bar of the alert window
            message (str): The text on the alert window
            icon (str): The type of alert - one of 'error', 'warning', 'question', 'info'. Depending on the OS,
                an icon corresponding to the type of alert is shown on the alert.
        """
        self._check_icon(icon)
        if icon == 'error':
            messagebox.showerror(title, message, parent=self._root, icon='error')
        elif icon == 'warning':
            messagebox.showwarning(title, message, parent=self._root, icon='warning')
        elif icon == 'question':
            messagebox.showinfo(title, message, parent=self._root, icon='question')
        elif icon == 'info':
            messagebox.showinfo(title, message, parent=self._root, icon='info')

    def confirm_okcancel(self, title, message, icon):
        """Launches a confirm popup with buttons 'OK' and 'Cancel'

        Args:
            title (str): The text on the title bar of the popup window
            message (str): The text on the confirm popup
            icon(str): The icon to show on the confirm popup (OS-dependent). Must be one of 'error', 'warning',
                'question', 'info'

        Returns:
            bool: True if 'OK' was selected, False if 'Cancel' was selected or the window was dismissed with ESC
                or the close button
        """
        self._check_icon(icon)
        return messagebox.askokcancel(title, message, parent=self._root, icon=icon)

    def confirm_yesno(self, title, message, icon):
        """Launches a confirm popup with buttons 'Yes' and 'No'

        Args:
            title (str): The text on the title bar of the popup window
            message (str): The text on the confirm popup
            icon(str): The icon to show on the confirm popup (OS-dependent). Must be one of 'error', 'warning',
                'question', 'info'

        Returns:
            bool: True if 'Yes' was selected, False if 'No' was selected or the window was dismissed with ESC
                or the close button
        """
        self._check_icon(icon)
        return messagebox.askyesno(title, message, parent=self._root, icon=icon)

    def confirm_retrycancel(self, title, message, icon):
        """Launches a confirm popup with buttons 'Retry' and 'Cancel'

        Args:
            title (str): The text on the title bar of the popup window
            message (str): The text on the confirm popup
            icon(str): The icon to show on the confirm popup (OS-dependent). Must be one of 'error', 'warning',
                'question', 'info'

        Returns:
            bool: True if 'Retry' was selected, False if 'Cancel' was selected or the window was dismissed with ESC
                or the close button
        """
        self._check_icon(icon)
        return messagebox.askretrycancel(title, message, parent=self._root, icon=icon)

    def confirm_yesnocancel(self, title, message, icon):
        """Launches a confirm popup with buttons 'Yes', 'No' and 'Cancel'

        Args:
            title (str): The text on the title bar of the popup window
            message (str): The text on the confirm popup
            icon(str): The icon to show on the confirm popup (OS-dependent). Must be one of 'error', 'warning',
                'question', 'info'

        Returns:
            bool: True if 'OK' was selected, False if 'No' was selected, and None if either 'Cancel' was selected
                or the window was dismissed with ESC or the close button
        """
        self._check_icon(icon)
        return messagebox.askyesnocancel(title, message, parent=self._root, icon=icon)

    def _trigger_interval_callback(self):
        """Calls the callback function associated with set_interval and sets up the next call"""
        if self._interval_callback:
            self._interval_callback['function']()
            # Race condition exists here if the interval is cleared during the callback, so another if needed!
            if self._interval_callback:
                self._root.after(self._interval_callback['delay'], self._trigger_interval_callback)

    def set_interval(self, delay, interval_function):
        """Sets a function to repeatedly execute

        Args:
            delay (int): The frequency with which to call the interval function, in milliseconds
            interval_function (function): The function to call every 'delay' milliseconds

        Raises:
            TypeError: If the interval_function is not a callable function
        """
        if not callable(interval_function):
            raise TypeError('The second argument to set_interval must be a function')

        self._interval_callback = {
            'delay': delay,
            'function': interval_function
        }
        self._root.after(delay, self._trigger_interval_callback)

    def clear_interval(self):
        """Clears the set_interval function"""
        self._interval_callback = None

    def set_timeout(self, delay, timeout_function):
        """Sets a function to execute once after a given delay

        Args:
            delay (int): The frequency with which to call the interval function, in milliseconds
            timeout_function (function): The function to call every 'delay' milliseconds

        Raises:
            TypeError: If the interval_function is not a callable function
        """
        if not callable(timeout_function):
            raise TypeError('The second argument to set_timeout must be a function')

        self._timeout = self._root.after(delay, timeout_function)

    def clear_timeout(self):
        """Clears a timeout function if it exists"""
        if self._timeout:
            self._root.after_cancel(self._timeout)


class FileWindow:
    """Abstract base class for opening files and folders

    Inherited by OpenSaveFileWindow
    """
    def __init__(self, parent, title):
        """Creates a new FileWindow with the given parent window and title"""
        self._options = {'master': parent, 'title': title}

    def set_initial_folder(self, folder_name, *paths):
        """Sets an initial named folder that the FileWindow will open to

        The initial folder name is a common name used across operating systems, corresponding to either the location of
        the currently running app, or the user's home directory, documents directory or desktop.

        Args:
            folder_name (str): the named folder where the window will initially open to. Must be one of 'home',
                'documents', 'desktop' or 'app'
            *paths: additional subfolders under the initial folder
        """
        folder_name = folder_name.lower()
        if folder_name not in ('home', 'documents', 'desktop', 'app'):
            raise GooeyPieError("Argument 'folder_name' must be one of 'home', 'documents', 'desktop' or 'app'")

        home = os.path.expanduser('~')
        if folder_name == 'home':
            self._options['initialdir'] = home
        if folder_name == 'documents':
            self._options['initialdir'] = os.path.join(home, 'Documents')
        if folder_name == 'desktop':
            self._options['initialdir'] = os.path.join(home, 'Desktop')
        if folder_name == 'app':
            self._options['initialdir'] = os.path.abspath(os.getcwd())

        self._options['initialdir'] = os.path.join(self._options['initialdir'], *paths)

    @property
    def initial_path(self):
        """Gets or sets the full path of the location that the FileWindow will open to.

        The path will vary by operating system - e.g. Windows fonts could be in 'C:\Windows\Fonts\', but the
        equivalent in macOS is '"'/Library/Fonts'
        """
        return self._options.get('initialdir', None)

    @initial_path.setter
    def initial_path(self, path):
        self._options['initialdir'] = path


class OpenSaveFileWindow(FileWindow):
    """Abstract base class for opening and saving file window

    Inherited by OpenFileWindow and SaveFileWindow
    """
    def __init__(self, parent, title):
        """Create a new Open or Save window with the given parent and title"""
        super().__init__(parent, title)
        self._options['filetypes'] = [('All files', '*.*')]

    def add_file_type(self, description, extension):
        """Adds a new file type to be displayed as a filter when opening or saving files

        Args:
            description (str): A description of the file type(s)
            extension (str): The file pattern(s) to filter, multiple types should be separated with a space
        """
        if self._options['filetypes'] == [('All files', '*.*')]:
            # Replace the default "All files" file type if it is the only one.
            self._options['filetypes'] = [(description, extension)]
        else:
            self._options['filetypes'].append((description, extension))


class OpenFileWindow(OpenSaveFileWindow):
    """Open file dialog"""
    def __init__(self, parent, title):
        """Creates a new Open File Window

        Args:
            parent (WindowBase): The window or app that will initiate the Open File Window
            title (str): The title that appears on the Open File Window title bar
        """
        super().__init__(parent, title)
        self._select_multiple_files = False

    @property
    def allow_multiple(self):
        """Gets or sets whether to allow the user to select multiple files when the Open File Window is initiated"""
        return self._select_multiple_files

    @allow_multiple.setter
    def allow_multiple(self, allow):
        self._select_multiple_files = bool(allow)

    def open(self):
        """Launches the file open dialog and returns the selected and path filename(s),

        Returns:
            The filename as a string including the full path, or if multiple files are selected a list of all
            path-filenames, or None if the user clicks cancel or otherwise dismisses the window
        """
        if self.allow_multiple:
            return filedialog.askopenfilenames(**self._options) or None
        else:
            return filedialog.askopenfilename(**self._options) or None


class SaveFileWindow(OpenSaveFileWindow):
    """Save File window"""
    def __init__(self, parent, title):
        """Creates a new Save File Window

        Args:
            parent (WindowBase): The window or app that will initiate the Open File Window
            title (str): The title that appears on the Save File Window title bar
        """
        super().__init__(parent, title)

    def open(self):
        """Launches the file save window

        Returns:
            The selected/entered filename(s) and its full path, including the extension added with add_file_type
                Returns None if the user clicks cancel or otherwise dismisses the window
        """

        # If the default extension is not specified, no extension is added even when one is selected
        return filedialog.asksaveasfilename(**self._options, defaultextension='') or None


class OpenFolderWindow(FileWindow):
    """Allows a user to select a folder on their local system, returns the full path to the folder"""
    def __init__(self, parent, title):
        """Creates a new Open Folder Window

        Args:
            parent (WindowBase): The window or app that will initiate the Open Folder Window
            title (str): The title that appears on the Open Folder Window title bar
        """
        super().__init__(parent, title)

    def open(self):
        """Launches the Open Folder window

        Returns:
            The complete path to the selected folder as a string, or None if the user selects Cancel or otherwise
                dismisses the window
        """
        return filedialog.askdirectory(**self._options, mustexist=True) or None


class Window(WindowBase):
    """For creating windows in addition to the main window created with the call to GooeyPieApp"""
    def __init__(self, parent, title):
        """Creates a new window

        Args:
            parent (WindowBase): The parent window or application object
            title (str): The text that appears in the title bar of the window
        """
        WindowBase.__init__(self, tk.Toplevel(parent), title)
        self._initialised = False
        self._default_close = self.hide  # By default, additional windows are hidden
        self.hide()

    def __str__(self):
        return f"<Window '{self.title}'>"

    def show(self):
        """Makes the window visible"""
        self._root.deiconify()
        self._root.grab_release()
        if not self._initialised:
            self._initialised = True
            self._init_window()

    def show_on_top(self):
        """Makes the window visible and prevents the user from interacting with the parent window"""
        self._root.deiconify()
        self._root.grab_set()
        if not self._initialised:
            self._initialised = True
            self._init_window()

    def hide(self):
        """Hides the window"""
        self._root.withdraw()
        self._root.grab_release()


class GooeyPieApp(WindowBase):
    """The main application window"""
    def __init__(self, title):
        """Creates the application object and main window

        Args:
            title (str): The text that appears in the title bar of the main window

        """
        WindowBase.__init__(self, tk.Tk(), title)

    def __str__(self):
        return f"<GooeyPieApp '{self.title}'>"

    def __repr__(self):
        return self.__str__()

    def _set_default_icon(self):
        icon_data = """iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAAsSAAALEgHS3X78AAACUklEQVRYhc1XgbGCMA
        wNfwFwAtlAN4ANdANHkA1kA91AN9ANdAPdQDaAP0H+vZ7xQoFCVbz/7nqcQvNekzRpiZn1iJg5Z+aCP4/iYTvSnJo8ZeZqBGIb1YOrJiD9ArE
        NIyKAS4ioIKKQenC73agoCvMUpGlK8/mcoijqm27jl4jiHyLKXORVVVGe5xTHsSHb7XaNd5PJxIg4HA4+AkLD7Uq47XbLYRhykiR8Pp+d/tzv
        9zydTs3o+1ahoK43q9XK11hNNAQNQasAkM9mMy7L0otccL1eB4toCFiv12+R2yL6PFgTIJPw/AQQDoTRtZiagMViwZvN5iPkAiQwhPQKuN/vT
        ERvu97G8Xg0XugVAJXwwBhwhfVHqsLlcjGFZgzArq6eGk8BqGqoZmMAdlHCnQJ8sVwuB89w9gmJxZByq4Fa4cpuG13JXROAjB0KiEVyvbtrni
        FAnJCIQ4HEwsiy7DkDHTMIgkEDXbSWAzB2Op28MgGtGXMkw5EXYRhSWZb2Ua82kiRp5gDwSvdD5UT4+BFnhAX9xAXdqMg2huTyAUghXPIHhrE
        uVNY2YIH6faMbQoBvP5DDiLYhXrEhrV7QEODTyzVAKMJllfaugm38r223HkhEhM8+l20prkVf0V5BqNo803kkgwgY8ClQ+BYu5kd3hSB4Rci1
        QC2g81CKiTCAiVL5IEaKD4zhN7JeDqTa7XpuR0c0h9K8b2UgRNywOqwSccSQEzMEtFVR2SEQ0NGOc6+LyStAl+1oRs+LSYUiNgY5uTvh0nD/l
        8upjO9ez5npDxwrvxk2vF3PAAAAAElFTkSuQmCC"""
        icon = tkinter.PhotoImage(data=icon_data)
        self._root.iconphoto(True, icon)

    def set_icon(self, image_file):
        """Sets the icon for all windows in the application

        Args:
            image_file (str): The filename of the image to use as the window icon

        """
        self._icon = image_file

        if image_file[-3:] == 'ico':
            self._root.iconbitmap(True, image_file)
        else:
            self._root.iconphoto(True, ImageTk.PhotoImage(PILImage.open(image_file)))

    def copy_to_clipboard(self, text):
        """Copies text to the OS clipboard

        Args:
            text (str): Copies text to the clipboard
        """
        self.clipboard_clear()
        self.clipboard_append(text)
        self.update()  # now it stays on the clipboard after the window is closed

    def font_available(self, font_name):
        """Checks whether a particular font is installed on the computer

        Args:
            font_name (str): The font name to check for

        Returns:
            bool: Whether the given font_name exists on the users computer
        """
        return font_name.lower() in [f.lower() for f in self.fonts()]

    def fonts(self):
        """Get all available system fonts

        Returns:
            list: All font names (as strings)

        """
        return list(font.families(self))

    def exit(self):
        """Closes all windows and exits the program"""
        self._root.destroy()

    def run(self):
        """Starts the application"""
        self._init_window()
        if not self._icon:
            self._set_default_icon()
        self.mainloop()
