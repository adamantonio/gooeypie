from .widgets import *
from .containers import *
from .error import *
from tkinter import messagebox


class WindowBase(Container):
    """
    Base class for GooeyPieApp and Window classes
    Provides functions for window options like size, title and menus
    """
    def __init__(self, root, title, *args):
        self._root = root   # for the class GooeyPieApp, this is the tkinter.Tk() instance
        self._root.title(title)  # title of the window

        Container.__init__(self, root)

        self._menubar = tk.Menu(root)
        self._menu = {}  # internal dictionary for menu objects
        self._menu_tkcontrols = {}  # internal dictionary of tk control variables for menu radio buttons and check
        self._preferred_size = [0, 0]  # users preferred size (may be larger to fit in all apps)

        self._interval_callback = None  # Dictionary for set_interval callback (callback and delay)
        self._timeout = None  # Identifier used when calling set_timeout, used by clear_timeout
        self._icon = None  # Window icon

        self._on_close_callback = None  # Function called when window is closed
        self._default_close = self._root.destroy
        self._root.protocol("WM_DELETE_WINDOW", self._handle_window_close)

        self.storage = {}  # Global storage variable

    def _init_window(self):
        """Sets up the window with the users size preferences and menus"""

        # Add the menu bar to the window if there is one
        if self._menu:
            self._root.config(menu=self._menubar)

        # Add the main Container to the window
        self.pack(fill='both', expand=True, padx=0, pady=0)

        # Call update to get width and height info, then set the min size to these values
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
        return self._root.title()

    @title.setter
    def title(self, text):
        self._root.title(text)

    def set_size(self, width, height):
        self._preferred_size = [width, height]

    def set_icon(self, image_file):
        self._icon = image_file
        self._root.iconbitmap(image_file)

    @property
    def width(self):
        return self._root.winfo_width()

    @width.setter
    def width(self, value):
        """Sets the preferred width of the window. Actual width might be wider to fit in all widgets"""
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
        """Sets the preferred height of the window. Actual height might be wider to fit in all widgets"""
        if value == 'auto':
            value = 0

        self._preferred_size[1] = value

        # Normally height is set before the window is initialised/displayed, and the call to root.geometry() is made
        # during self._init(). If the window is already visible, change the size immediately.
        # Note: size will not change if the window is minimised (iconified)
        if self._root.winfo_ismapped():
            self._root.geometry(f'{self.width}x{value}')

    def resizable(self, resize):
        """Determines whether the user can change the size of the window"""
        pass

    def _create_menu(self, menu_path, parent):
        """Creates a tk menu object if it does not exist and adds it to the internal dictionary of menu objects

        menu_path is either the name of a top level menu or a tuple (top_level_name, sub_menu_name)
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
            self._menu[menu_path].entryconfigure(current, command=partial(self._menu_select_callback, item_path, callback))

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
            # callback((menu_path, selected_option))
        else:
            # If the radio item is in a submenu - e.g. ('Format', 'Font', 'Bold')
            menu_str = (menu_path[0], menu_path[1], selected_option)
            # callback((menu_path[0], menu_path[1], selected_option))

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
            self._menu[menu_path].entryconfigure(self._menu[menu_path].index('end'), command=partial(self._menu_select_callback, item_path, callback))

    def _change_menu_state(self, menu_path, item, state):
        """Change

        menu: string or tuple representing menu or (menu, submenu)
        item: string
        state: string
        """
        try:
            menu = self._menu[menu_path]

            max_index = menu.index('end')
            # find the menu item
            for i in range(max_index + 1):
                if menu.type(i) != 'separator' and menu.entrycget(i, 'label') == item:
                    index = i
            menu.entryconfigure(index, state=state)
        except NameError:
            raise NameError(f"The menu item could not be found")
        except KeyError:
            raise KeyError(f"The menu could not be found")

    def add_menu_item(self, menu, item, callback):
        """Adds a menu command to the window"""
        self._create_menu(menu, self._menubar)
        self._create_menu_item(menu, item, callback)

    def add_submenu_item(self, menu, submenu, item, callback):
        """Create a submenu 'item' with name 'submenu' under 'menu'"""
        self._create_menu(menu, self._menubar)
        self._create_menu((menu, submenu), self._menu[menu])
        self._create_menu_item((menu, submenu), item, callback)

    def add_menu_radios(self, menu, options, callback):
        """Add a group of radio button menu items to a top level menu"""
        self._create_menu(menu, self._menubar)
        self._create_menu_radios(menu, options, callback)

    def add_submenu_radios(self, menu, submenu, options, callback):
        """Add a group of radio button menu items to a submenu"""
        self._create_menu(menu, self._menubar)
        self._create_menu((menu, submenu), self._menu[menu])
        self._create_menu_radios((menu, submenu), options, callback)

    def add_menu_checkbox(self, menu, item, callback, checked=False):
        self._create_menu(menu, self._menubar)
        self._create_menu_checkbutton(menu, item, callback, checked)

    def add_submenu_checkbox(self, menu, submenu, item, callback, checked=False):
        self._create_menu(menu, self._menubar)
        self._create_menu((menu, submenu), self._menu[menu])
        self._create_menu_checkbutton((menu, submenu), item, callback, checked)

    def add_menu_separator(self, *path):
        """Adds a separator to the given path"""
        assert(len(path) == 1 or len(path) == 2)
        menu_path = path[0] if len(path) == 1 else path
        self._menu[menu_path].add_separator()

    # Alias the add_menu_separator for consistency
    add_submenu_separator = add_menu_separator

    def disable_menu_item(self, menu, item):
        """Disable the given item under the specified menu"""
        self._change_menu_state(menu, item, 'disabled')

    def enable_menu_item(self, menu, item):
        """Enables the specified item under menu. Has no effect if the item is already enabled"""
        self._change_menu_state(menu, item, 'normal')

    def disable_submenu_item(self, menu, submenu, item):
        """Disable the item under the specified menu, submenu"""
        self._change_menu_state((menu, submenu), item, 'disabled')

    def enable_submenu_item(self, menu, submenu, item):
        """Enable the item under the specified menu, submenu"""
        self._change_menu_state((menu, submenu), item, 'normal')

    def set_menu_radio(self, menu, options, item):
        """"""
        control_var_key = (menu,) + tuple(options)
        self._menu_tkcontrols[control_var_key].set(item)

    def set_submenu_radio(self, menu, submenu, options, item):
        control_var_key = (menu, submenu) + tuple(options)
        self._menu_tkcontrols[control_var_key].set(item)

    def get_menu_radio(self, menu, options):
        """"""
        control_var_key = (menu,) + tuple(options)
        return self._menu_tkcontrols[control_var_key].get()

    def get_submenu_radio(self, menu, submenu, options):
        """"""
        control_var_key = (menu, submenu) + tuple(options)
        return self._menu_tkcontrols[control_var_key].get()

    def get_menu_checkbox(self, menu, item):
        """Returns the state of the menu checkbutton"""
        return self._menu_tkcontrols[(menu, item)].get()

    def set_menu_checkbox(self, menu, item, state):
        """Sets the state of the menu checkbutton"""
        self._menu_tkcontrols[(menu, item)].set(state)

    def get_submenu_checkbox(self, menu, submenu, item):
        """Returns the state of the menu checkbutton"""
        return self._menu_tkcontrols[(menu, submenu, item)].get()

    def set_submenu_checkbox(self, menu, submenu, item, state):
        """Sets the state of the menu checkbutton"""
        self._menu_tkcontrols[(menu, submenu, item)].set(state)

    def on_close(self, callback):
        """Registers a function to be called when the window is closed"""
        if not callable(callback):
            raise GooeyPieError('The argument to the on_close method must be the name of a function')
        self._on_close_callback = callback

    # Work all this stuff out - https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/tkMessageBox.html
    def ask_ok_cancel(self, title, message):
        return messagebox.askokcancel(title, message, parent=self._root, icon='info', default='cancel')

    # Dialogs that have a single 'OK' button
    def info_dialog(self, title, message):
        messagebox.showinfo(title, message, parent=self._root, icon='info')

    def warning_dialog(self, title, message):
        messagebox.showwarning(title, message, parent=self._root, icon='warning')

    def error_dialog(self, title, message):
        messagebox.showerror(title, message, parent=self._root, icon='error')

    # Dialogs that return a value
    def info_question(self, title, message, buttons='okcancel'):
        """NOT YET IMPLEMENTED"""
        pass

    def question_question(self, title, message, buttons='okcancel'):
        # well this is a silly function name
        """NOT YET IMPLEMENTED"""
        pass

    def warning_question(self, title, message, buttons='okcancel'):
        """NOT YET IMPLEMENTED"""
        pass

    def error_question(self, title, message, buttons='okcancel'):
        """NOT YET IMPLEMENTED"""
        pass

    def _trigger_interval_callback(self):
        """Calls the callback function associated with set_interval and sets up the next call"""
        if self._interval_callback:
            self._interval_callback['function']()
            # Race condition exists here if the interval is cleared during the callback, so another if needed!
            if self._interval_callback:
                self._root.after(self._interval_callback['delay'], self._trigger_interval_callback)

    def set_interval(self, delay, callback):
        """Sets up the callback function to execute every delay milliseconds"""
        self._interval_callback = {
            'delay': delay,
            'function': callback
        }
        self._root.after(delay, self._trigger_interval_callback)

    def clear_interval(self):
        """Stops the set_interval callback"""
        self._interval_callback = None

    def set_timeout(self, delay, callback):
        """Execute the given callback function one time after delay milliseconds"""
        self._timeout = self._root.after(delay, callback)

    def clear_timeout(self):
        """Clears a timeout function if it exists"""
        if self._timeout:
            self._root.after_cancel(self._timeout)


class Window(WindowBase):
    """An additional window"""
    def __init__(self, app, title):
        WindowBase.__init__(self, tk.Toplevel(app), title)
        self._initialised = False
        self._default_close = self.hide
        self.hide()

        ## testing ##
        # When a window is closed with the [X], it is destroyed so cannot be opened again. It might be more intuitive
        # for students to only have the window hidden so it can be reopened.
        # this hides the window rather than closing it.
        # self.on_close(self.hide)
        # But if I set this here when it's instantiated, then it can be overridden, so I need

        # The other problem here is that any on_close method needs to hide the window explicitly so this will need to
        # be carefully documented.

    def __str__(self):
        return f"<Window '{self.title}'>"

    def show(self):
        self._root.deiconify()
        self._root.grab_release()
        if not self._initialised:
            self._initialised = True
            self._init_window()

    def show_on_top(self):
        self._root.deiconify()
        self._root.grab_set()
        if not self._initialised:
            self._initialised = True
            self._init_window()

    def hide(self):
        self._root.withdraw()
        self._root.grab_release()

    # def on_close(self, callback):
    #     """Registers a function to be called when the window is closed"""
    #     self._root.protocol("WM_DELETE_WINDOW", callback)


class GooeyPieApp(WindowBase):
    """The main application window"""
    def __init__(self, title):
        WindowBase.__init__(self, tk.Tk(), title)

    def __str__(self):
        return f"<GooeyPieApp '{self.title}'>"

    def _set_default_icon(self):
        try:
            import os
            icon_path = os.path.join(os.path.dirname(__file__), 'gplogo3.ico')
            self._root.iconbitmap(icon_path)
        except Exception as e:
            print(f'Could not set icon: {e}')

    def copy_to_clipboard(self, text):
        """Copies the provided text to the OS clipboard"""
        self.clipboard_clear()
        self.clipboard_append(text)
        self.update()  # now it stays on the clipboard after the window is closed

    def font_available(self, font_name):
        """Returns true if font_name is installed on the system, case-insensitive"""
        # TODO: check if MacOS cares about case for font names
        return font_name.lower() in [f.lower() for f in self.fonts()]

    def fonts(self):
        """Returns a list of all system fonts"""
        return list(font.families(self))

    def exit(self):
        self._root.destroy()

    def run(self):
        """Starts the application"""
        self._init_window()
        if not self._icon:
            self._set_default_icon()
        self.mainloop()
