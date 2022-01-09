import tkinter
from tkinter import messagebox
from PIL import Image as PILImage, ImageTk

from .widgets import *
from .containers import *
from .error import *

__version__ = "0.2.1"


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
        self._preferred_size = [0, 0]  # users preferred size (actual size may be larger to fit in all widgets)

        self._interval_callback = None  # Dictionary for set_interval callback (callback and delay)
        self._timeout = None  # Identifier used when calling set_timeout, used by clear_timeout
        self._icon = None  # Window icon

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

    def alert(self, title, message, icon):
        """Alerts have a single 'OK' button and do not return a value"""
        if icon == 'error':
            messagebox.showerror(title, message, parent=self._root, icon='error')
        elif icon == 'warning':
            messagebox.showwarning(title, message, parent=self._root, icon='warning')
        elif icon == 'question':
            messagebox.showinfo(title, message, parent=self._root, icon='question')
        else:
            messagebox.showinfo(title, message, parent=self._root, icon='info')

    # Confirmation dialogs return a value
    @staticmethod
    def _check_icon(icon):
        if icon not in ('info', 'question', 'warning', 'error'):
            raise GooeyPieError("The icon for the confirm popup must be one of 'info', 'question', 'warning' or 'error'")

    def confirm_okcancel(self, title, message, icon):
        self._check_icon(icon)
        return messagebox.askokcancel(title, message, parent=self._root, icon=icon)

    def confirm_yesno(self, title, message, icon):
        self._check_icon(icon)
        return messagebox.askyesno(title, message, parent=self._root, icon=icon)

    def confirm_retrycancel(self, title, message, icon):
        self._check_icon(icon)
        return messagebox.askretrycancel(title, message, parent=self._root, icon=icon)

    def confirm_yesnocancel(self, title, message, icon):
        self._check_icon(icon)
        return messagebox.askyesnocancel(title, message, parent=self._root, icon=icon)

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


class FileWindow:
    """Base class for opening files and folders"""
    def __init__(self, parent, title):
        self._options = {'master': parent, 'title': title}

    def set_initial_folder(self, folder_name, *paths):
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
        return self._options.get('initialdir', None)

    @initial_path.setter
    def initial_path(self, path):
        self._options['initialdir'] = path


class OpenSaveFileWindow(FileWindow):
    """Windows for opening and saving files
    Base class for OpenFileWindow and SaveFileWindow
    """
    def __init__(self, parent, title):
        super().__init__(parent, title)
        self._options['filetypes'] = [('All files', '*.*')]

    def add_file_type(self, description, extension):
        if self._options['filetypes'] == [('All files', '*.*')]:
            # Replace the default "All files" file type if it is the only one.
            self._options['filetypes'] = [(description, extension)]
        else:
            self._options['filetypes'].append((description, extension))


class OpenFileWindow(OpenSaveFileWindow):
    """Open file dialog"""
    def __init__(self, parent, title):
        super().__init__(parent, title)
        self._select_multiple_files = False

    @property
    def allow_multiple(self):
        return self._select_multiple_files

    @allow_multiple.setter
    def allow_multiple(self, allow):
        self._select_multiple_files = bool(allow)

    def open(self):
        """Launches the file open dialog and returns the selected and path filename(s),
        Returns None if the user clicks cancel
        """
        if self.allow_multiple:
            return filedialog.askopenfilenames(**self._options) or None
        else:
            return filedialog.askopenfilename(**self._options) or None


class SaveFileWindow(OpenSaveFileWindow):
    def __init__(self, parent, title):
        super().__init__(parent, title)

    def open(self):
        """Launches the file save dialog and returns the selected/entered filename(s),
        The filename will include the extension added with add_file_type
        Returns None if the user clicks cancel
        """

        # If default extension is not specified, no extension is added even when one is selected
        return filedialog.asksaveasfilename(**self._options, defaultextension='') or None


class OpenFolderWindow(FileWindow):
    """Allows a user to select a folder on their local system, returns the full path to the folder"""
    def __init__(self, parent, title):
        super().__init__(parent, title)

    def open(self):
        return filedialog.askdirectory(**self._options, mustexist=True) or None


class Window(WindowBase):
    """An additional window"""
    def __init__(self, app, title):
        WindowBase.__init__(self, tk.Toplevel(app), title)
        self._initialised = False
        self._default_close = self.hide  # By default, additional windows are hidden
        self.hide()

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


class GooeyPieApp(WindowBase):
    """The main application window"""
    def __init__(self, title):
        WindowBase.__init__(self, tk.Tk(), title)

    def __str__(self):
        return f"<GooeyPieApp '{self.title}'>"

    def __repr__(self):
        return self.__str__()

    def _set_default_icon(self):
        icon_data = """iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAAsSAAALEgHS3X78AAACUklEQVRYhc1XgbGCMAwNfwFwAtlAN4ANdANHkA1kA91AN9ANdAPdQDaAP0H+vZ7xQoFCVbz/7nqcQvNekzRpiZn1iJg5Z+aCP4/iYTvSnJo8ZeZqBGIb1YOrJiD9ArENIyKAS4ioIKKQenC73agoCvMUpGlK8/mcoijqm27jl4jiHyLKXORVVVGe5xTHsSHb7XaNd5PJxIg4HA4+AkLD7Uq47XbLYRhykiR8Pp+d/tzv9zydTs3o+1ahoK43q9XK11hNNAQNQasAkM9mMy7L0otccL1eB4toCFiv12+R2yL6PFgTIJPw/AQQDoTRtZiagMViwZvN5iPkAiQwhPQKuN/vTERvu97G8Xg0XugVAJXwwBhwhfVHqsLlcjGFZgzArq6eGk8BqGqoZmMAdlHCnQJ8sVwuB89w9gmJxZByq4Fa4cpuG13JXROAjB0KiEVyvbtrniFAnJCIQ4HEwsiy7DkDHTMIgkEDXbSWAzB2Op28MgGtGXMkw5EXYRhSWZb2Ua82kiRp5gDwSvdD5UT4+BFnhAX9xAXdqMg2huTyAUghXPIHhrEuVNY2YIH6faMbQoBvP5DDiLYhXrEhrV7QEODTyzVAKMJllfaugm38r223HkhEhM8+l20prkVf0V5BqNo803kkgwgY8ClQ+BYu5kd3hSB4Rci1QC2g81CKiTCAiVL5IEaKD4zhN7JeDqTa7XpuR0c0h9K8b2UgRNywOqwSccSQEzMEtFVR2SEQ0NGOc6+LyStAl+1oRs+LSYUiNgY5uTvh0nD/l8upjO9ez5npDxwrvxk2vF3PAAAAAElFTkSuQmCC"""
        icon = tkinter.PhotoImage(data=icon_data)
        self._root.iconphoto(True, icon)

    def set_icon(self, image_file):
        """Sets the icon for all windows in the application"""
        self._icon = image_file

        if image_file[-3:] == 'ico':
            self._root.iconbitmap(True, image_file)
        else:
            self._root.iconphoto(True, ImageTk.PhotoImage(PILImage.open(image_file)))

    def copy_to_clipboard(self, text):
        """Copies the provided text to the OS clipboard"""
        self.clipboard_clear()
        self.clipboard_append(text)
        self.update()  # now it stays on the clipboard after the window is closed

    def font_available(self, font_name):
        """Returns true if font_name is installed on the system, case-insensitive"""
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
