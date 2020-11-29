from gooeypie.widgets import *
from gooeypie.containers import *
from gooeypie.error import *
from tkinter import messagebox


class WindowBase(Container):
    """
    Base class for GooeyPieApp and Window classes
    Provides functions for window options like size, title and menus
    """
    def __init__(self, root, title, *args):
        self._root = root   # for the class GooeyPieApp, this is the tk.Tk() instance
        self._root.title(title)  # title of the window

        Container.__init__(self, self._root)

        self._menubar = tk.Menu(root)
        self._menu = {}  # internal dictionary for menu objects
        self._menu_tkcontrols = {}  # internal dictionary of tk control variables for menu radio buttons and check
        self._preferred_size = [0, 0]  # users preferred size (may be larger to fit in all apps)

        self._interval_callback = None  # Callback function for set interval

    def _init_window(self):
        """Sets up the window with the users """

        # Add the menu bar to the window if there is one
        if self._menu:
            self._root.config(menu=self._menubar)

        # Add the main Container to the window
        # self.grid(padx=(16, 0), pady=(16, 0), sticky='nsew')
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

        # Maximise the space occupied by the main frame - row/column configure needs to be called on
        # the root window and the main frame
        # self._root.columnconfigure(0, weight=1)
        # self._root.rowconfigure(0, weight=1)
        # self.columnconfigure(0, weight=1)
        # self.rowconfigure(0, weight=1)

    def set_title(self, title):
        self._root.title(title)

    def set_size(self, width, height):
        self._preferred_size = [width, height]

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

    def font_available(self, font_name):
        return font_name in font.families(self)

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

        # Refactor - first arg is menu 'type', this means we can call this fct from add menu radios
        self._menu[menu_path].add_command(label=item)

        # TODO: this could go out to another fct for the radio group option - _set_menu_callback
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
            self._menu[menu_path].entryconfigure(current, command=partial(callback, item_path))

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

    def _menu_radio_select_callback(self, menu_path, control_var, callback):
        """Intermediary callback for menu radio items"""
        selected_option = self._menu_tkcontrols[control_var].get()
        if type(menu_path) == str:
            # If the radio item is in a top level menu - e.g. ('Font', 'Bold')
            callback((menu_path, selected_option))
        else:
            # If the radio item is in a submenu - e.g. ('Format', 'Font', 'Bold')
            callback((menu_path[0], menu_path[1], selected_option))

    def _create_menu_checkbutton(self, menu_path, item, callback, state=True):
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
            self._menu[menu_path].entryconfigure(self._menu[menu_path].index('end'), command=partial(callback, item_path))

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

    def add_menu_checkbutton(self, menu, item, callback):
        self._create_menu(menu, self._menubar)
        self._create_menu_checkbutton(menu, item, callback)

    def add_submenu_checkbutton(self, menu, submenu, item, callback):
        self._create_menu(menu, self._menubar)
        self._create_menu((menu, submenu), self._menu[menu])
        self._create_menu_checkbutton((menu, submenu), item, callback)

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

    def get_menu_checkbutton(self, menu, item):
        """Returns the state of the menu checkbutton"""
        return self._menu_tkcontrols[(menu, item)].get()

    def set_menu_checkbutton(self, menu, item, state):
        """Sets the state of the menu checkbutton"""
        self._menu_tkcontrols[(menu, item)].set(state)

    def get_submenu_checkbutton(self, menu, submenu, item):
        """Returns the state of the menu checkbutton"""
        return self._menu_tkcontrols[(menu, submenu, item)].get()

    def set_submenu_checkbutton(self, menu, submenu, item, state):
        """Sets the state of the menu checkbutton"""
        self._menu_tkcontrols[(menu, submenu, item)].set(state)

    def on_close(self, callback):
        """Registers a function to be called when the window is closed"""
        # TODO: test this, add an exit() or destroy() fct
        self._root.protocol("WM_DELETE_WINDOW", callback)

    # Work all this stuff out - https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/tkMessageBox.html
    def ask_ok_cancel(self, title, message):
        return messagebox.askokcancel(title, message, parent=self, icon='info', default='cancel')

    # Dialogs that have a single 'OK' button
    def info_dialog(self, title, message):
        messagebox.showinfo(title, message, parent=self, icon='info')

    def warning_dialog(self, title, message):
        messagebox.showwarning(title, message, parent=self, icon='warning')

    def error_dialog(self, title, message):
        messagebox.showerror(title, message, parent=self, icon='error')

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

    def set_timeout(self, delay, callback):
        """Execute the given callback function one time after delay milliseonds"""
        self._root.after(delay, callback)

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


class Window(WindowBase):
    """An additional window"""
    def __init__(self, app, title):
        WindowBase.__init__(self, tk.Toplevel(app), title)
        Container.__init__(self, self._root)
        self.grid(padx=10, pady=10)
        self.hide()

    def show(self):
        self._root.deiconify()
        self._root.grab_release()

    def show_on_top(self):
        self._root.deiconify()
        self._root.grab_set()

    def hide(self):
        self._root.withdraw()
        self._root.grab_release()


class GooeyPieApp(WindowBase):
    """The main application window"""
    def __init__(self, title):
        WindowBase.__init__(self, tk.Tk(), title)
        if DEBUG:
            self._root.configure(background='black')

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

    # @staticmethod
    # def ask_yes_no(self, title, message):
    #     return messagebox.askyesno(title, message)
    #
    # @staticmethod
    # def ask_retry_cancel(self, title, message):
    #     return messagebox.askretrycancel(title, message)
    #
    # @staticmethod
    # def alert_error(self, title, message):

    def exit(self):
        self._root.destroy()

    def run(self):
        """Starts the application"""
        self._init_window()
        self._set_default_icon()
        self.mainloop()
