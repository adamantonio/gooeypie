import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import font
from functools import partial
from gooeypie.error import GooeyPieError
from gooeypie.containers import *   # Used for the ScrolledListbox & Radiogroup widgets

import platform

if platform.system() == 'Windows':
    OS = 'Windows'
if platform.system() == 'Darwin':
    OS = 'Mac'

try:
    from PIL import Image as PILImage, ImageTk
    PILLOW = True
except ImportError:
    PILImage = ImageTk = None
    PILLOW = False


class GooeyPieEvent:
    """Event objects are passed to callback functions"""
    def __init__(self, event_name, gooeypie_widget, tk_event=None):
        """Creates a GooeyPie event object, passed to all callback functions"""
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
            if tk_event.char == '??':
                self.key = None
            else:
                self.key = {
                    'char': tk_event.char,
                    'keysym': tk_event.keysym,
                    'keycode': tk_event.keycode
                }
        else:
            self.mouse = None
            self.key = None


class GooeyPieWidget:
    """Base class for other GooeyPie widget classes, mostly for event handling"""

    # Event names in GooeyPie matched with their corresponding tk events
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
        # Check that the container is valid
        # if not isinstance(container, ContainerBase)
        if not isinstance(container, (ttk.Frame, ttk.LabelFrame)):
            raise GooeyPieError(f'A widget can only be added to a GooeyPieApp, Window or container')

        self._container = container

        # All events initially set to None
        self._events = {event_name: None for event_name in self._tk_event_mappings.keys()}

        self._disabled = False
        self.margins = ['auto', 'auto', 'auto', 'auto']  # top, right, bottom, left

    def _event(self, event_name, tk_event=None):
        """Constructs a GooeyPie Event object and calls the registered callback"""
        try:
            gooeypie_event = GooeyPieEvent(event_name, self, tk_event)
            self._events[event_name](gooeypie_event)
        except KeyError:
            raise AttributeError(f"'{event_name}' listener not associated with this widget")

    def _slider_change_event(self, event_name, slider_value):
        """In tkinter, slider change events send the new value of the slider, so this is a special callback"""

        # The slider's change event will be called whenever a movement is detected on the widget, even if the
        # movement does not actually change the value. This checks whether or not a change has actually been made.
        if self._value.get() != self._previous_value:
            self._previous_value = self._value.get()  # Update the previous value
            self._event(event_name)

    def _number_change_event(self, event_name, tkinter_event_object):
        """For implementing a change event on change in the Number ttk.Spinbox widget"""
        self._event(event_name)

    def _text_change_event(self, event_name, a, b, c):
        """To implement the change event for the Input/Textbox widget, a trace must be
        added to the variable associated with the Input. The trace command sends
        3 arguments to the callback"""
        self._event(event_name)

    def add_event_listener(self, event_name, callback):
        """Registers callback to respond to certain events"""

        # Check that the event is valid for the given widget
        if event_name not in self._events:
            raise GooeyPieError(f"The event '{event_name}' is not valid for widget {self}")

        # Check that the callback is a function
        if not callable(callback):
            raise GooeyPieError(f"The second argument does not appear to be the name of a function. "
                                f"Remember, no brackets - you don't want to *call* the function")

        # Check that the event function specified accepts a single argument
        if callback.__code__.co_argcount != 1:
            raise GooeyPieError(f"Your event function '{callback.__name__}' must accept a single argument")

        # Hyperlinks have default events for mouse_down (activating the link)
        # and mouse_over (showing a hand icon)
        if isinstance(self, Hyperlink):
            if event_name in ('mouse_down', 'mouse_over'):
                raise GooeyPieError(f"The '{event_name}' event cannot be associated with a Hyperlink")

        # Store the callback function in the widgets events dictionary
        self._events[event_name] = callback

        if event_name in self._tk_event_mappings:
            self.bind(self._tk_event_mappings[event_name], partial(self._event, event_name))

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

            if isinstance(self, Textbox):
                # TODO: change event for the textbox is complicated - will need to add a 'sentinel' to the Textbox widget
                # http://webcache.googleusercontent.com/search?q=cache:KpbCmAzvn_cJ:code.activestate.com/recipes/464635-call-a-callback-when-a-tkintertext-is-modified/+&cd=2&hl=en&ct=clnk&gl=au
                self.bind('<<Modified>>', partial(self._event, event_name))

        if event_name == 'press':
            # press event only on buttons (for now perhaps...)
            self.configure(command=partial(self._event, event_name))

        if event_name == 'select':
            # Select event associated at the moment with listboxes and dropdowns
            if isinstance(self, Listbox):
                self.bind('<<ListboxSelect>>', partial(self._event, event_name))
            elif isinstance(self, ScrolledListbox):
                self._listbox.bind('<<ListboxSelect>>', partial(self._event, event_name))
            elif isinstance(self, Dropdown):
                self.bind('<<ComboboxSelected>>', partial(self._event, event_name))

    def remove_event_listener(self, event_name):
        """
        Removes an event listener from a widget. Raises a GooeyPieError if the event is no associated with that widget,
        but does not raise an error if there is no event to remove.
        """
        if event_name not in self._events:
            raise GooeyPieError(f"Event '{event_name}' is not valid for {self}")

        if event_name in self._tk_event_mappings:
            # Unbind standard events like mouse_down, right_click etc
            if not (isinstance(self, Hyperlink) and event_name in ('mouse_down', 'mouse_over')):
                # Go ahead and unbind unless they we're trying to break the hyperlink
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
                # If there is a change event, then
                if self._observer:
                    self._value.trace_vdelete('w', self._observer)
                    self._observer = None

            if isinstance(self, Textbox):
                # TODO: add_event_listener not implemented
                self.unbind('<<Modified>>')

        if event_name == 'press':
            # press event on buttons
            self.configure(command='')

        if event_name == 'select':
            # Select event associated at the moment with listboxes and dropdowns
            if isinstance(self, Listbox):
                self.unbind('<<ListboxSelect>>')
            elif isinstance(self, ScrolledListbox):
                self._listbox.unbind('<<ListboxSelect>>')
            elif isinstance(self, Dropdown):
                self.unbind('<<ComboboxSelected>>')

    # All widgets can be enabled and disabled
    @property
    def disabled(self):
        return self._disabled

    @disabled.setter
    def disabled(self, value):
        self._disabled = bool(value)

        # Different widgets are disabled in different ways
        if isinstance(self, (Listbox, Textbox)):
            # tk widgets disabled with config
            state = 'disabled' if self._disabled else 'normal'
            self.config(state=state)

        elif isinstance(self, ScrolledListbox):
            # The listbox is a member of the ScrolledListbox object
            state = 'disabled' if self._disabled else 'normal'
            self._listbox.disabled = True

        elif isinstance(self, RadiogroupBase):
            # Both the container and each radiobutton are disabled
            state = ['disabled'] if self._disabled else ['!disabled']
            self.state(state)  # disable the container
            for radio in self.winfo_children():
                radio.state(state)  # disable each radiobutton

        else:
            # most other widgets are ttk widgets disabled with the state() method
            state = ['disabled'] if self._disabled else ['!disabled']
            self.state(state)


    # TODO: grid (layout) options? Can these be set prior to gridding, or only after they've been added?
    # Easy to implement by calling grid() on the widget - previously set options are not overridden unless specified
    # In fact, can call grid() at any time with options set - row/column will be set automatically though.

    # This allows for code like:
    #       button = gl.Button(app, 'Click me', callback)
    #       button.stretch/fill = True  <-- need words to describe fill_x and fill_y (haven't used x and y, so am wary...)
    #       button.align = 'right'    <-- could feasibly see this line being something that would be useful to a user
    #       button.valign = 'bottom'
    #       button.location = (2, 3)   <-- this feels counter to the general philosophy of gl.
    #           Why would a widget be moved to a different location after it has been added?
    #           Even still, maybe this should be a function, like button.move_to(2, 1)

    # Also users should be able to override the default padding set by add(). This should be possible either
    # before or after gridding. This means I definitely need a dictionary of these options)
    #       button.margin = 4               <-- all sides
    #       label.margin = (2, 4, 5, 1)     <-- top, right, bottom, left
    #       image.margin = (4, 6)           <-- top/bottom, left/right


    # TESTING: Retrieve all grid settings
    def get_info(self):
        return self.grid_info()
        # Sample output: Grid info: {'in': <guilite.GuiLiteApp object .!guiliteapp>, 'column': 1, 'row': 1, 'columnspan': 1, 'rowspan': 1, 'ipadx': 0, 'ipady': 0, 'padx': (0, 10), 'pady': (0, 10), 'sticky': 'nw'}

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

    def set_focus(self):
        """Sets the focus to the widget"""

        # If tkinter's focus() method is called during an event, it is ignored. This hackiness fixes that.
        self.winfo_toplevel().after(0, self.focus)


class Label(ttk.Label, GooeyPieWidget):
    def __init__(self, container, text):
        GooeyPieWidget.__init__(self, container)
        ttk.Label.__init__(self, container, text=text)

        # mapping for alignment options
        self._tk_settings = {
            'left': 'w',
            'center': 'center',
            'right': 'e'
        }

    def __str__(self):
        return f"<Label '{self.text}'>"

    @property
    def text(self):
        return self.cget('text')

    @text.setter
    def text(self, content):
        self.configure(text=content)

    @property
    def align(self):
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
        return self.cget('justify')

    @justify.setter
    def justify(self, value):
        """If the label contains newline characters, set to 'left', 'center' or 'right to justify the text."""
        self.configure(justify=value)


class Button(ttk.Button, GooeyPieWidget):
    def __init__(self, container, text, callback, min_size=10):
        GooeyPieWidget.__init__(self, container)
        ttk.Button.__init__(self, container, text=text)
        size = max(min_size, len(text) + 2)
        self.configure(width=size)
        self._events['press'] = None
        if callback:
            self.add_event_listener('press', callback)

    def __str__(self):
        return f"<Button '{self.text}'>"

    @property
    def width(self):
        return self.cget('width')

    @width.setter
    def width(self, value):
        self.configure(width=value)

    @property
    def text(self):
        return self.cget('text')

    @text.setter
    def text(self, text):
        self.configure(text=text)

    # TESTING #
    def info(self):
        return self.grid_info()


class Slider(ttk.Scale, GooeyPieWidget):
    def __init__(self, container, low, high, orientation='horizontal'):
        GooeyPieWidget.__init__(self, container)
        self._events['change'] = None

        # The slider's value will be a float or int depending on the low/high parameter data type
        if isinstance(low, float) or isinstance(high, float):
            self._value = tk.DoubleVar()
        else:
            self._value = tk.IntVar()

        # The previous value is stored so that the change event is called only when the actual value changes
        self._previous_value = self._value.get()

        # Swap low and high for vertical orientation to change the weird default behaviour
        if orientation == 'vertical':
            low, high = high, low

        ttk.Scale.__init__(self, container, from_=low, to=high, orient=orientation, variable=self._value)

    def __str__(self):
        return f'<Slider from {self.cget("from")} to {self.cget("to")}>'

    @property
    def value(self):
        return self._value.get()

    @value.setter
    def value(self, val):
        self.set(val)

    @property
    def orientation(self):
        return self.cget('orient')

    @orientation.setter
    def orientation(self, direction):
        self.configure(orient=direction)


class StyleLabel(Label):
    """A StyleLabel can be customised with colours (foreground and background), fonts and size

    Two helper functions exist in the main application object:
      fonts() returns all fonts
      font_available(name) returns True if name is installed on the current system
    """

    def __init__(self, container, text):
        super().__init__(container, text)
        self._style = ttk.Style()
        self._style_id = f'{str(id(self))}.TLabel'  # Need a custom id for each instance
        self.configure(style=self._style_id)

    def __str__(self):
        return f"<StyleLabel '{self.text}'>"

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

    def clear_styles(self):
        self._style.configure(self._style_id, font=font.nametofont('TkDefaultFont'))
        self.colour = 'default'
        self.background_color = 'default'

    @property
    def font_name(self):
        return self._get_current_font()['family']

    @font_name.setter
    def font_name(self, value):
        if value == 'default':
            self._set_font_property('family', font.nametofont('TkDefaultFont').actual()['family'])
        else:
            self._set_font_property('family', value)

    @property
    def font_size(self):
        return self._get_current_font()['size']

    @font_size.setter
    def font_size(self, value):
        if value == 'default':
            self._set_font_property('size', font.nametofont('TkDefaultFont').actual()['size'])
        else:
            try:
                self._set_font_property('size', int(value))
            except ValueError:
                raise ValueError(f"Font size must be an integer or the string 'default' "
                                 f"(value specified was {value})")

    @property
    def font_weight(self):
        return self._get_current_font()['weight']

    @font_weight.setter
    def font_weight(self, value):
        try:
            ('bold', 'normal').index(value)
            self._set_font_property('weight', value)
        except ValueError:
            raise ValueError(f"Font weight must be either 'bold' or 'normal' (value specified was '{value}')")

    @property
    def font_style(self):
        if self._get_current_font()['slant'] == 'roman':
            return 'normal'
        else:
            return 'italic'

    @font_style.setter
    def font_style(self, value):
        try:
            ('italic', 'normal').index(value)
            self._set_font_property('slant', value)
        except ValueError:
            raise ValueError(f"Font style must be either 'italic' or 'normal' (value specified was '{value}')")

    @property
    def underline(self):
        current_font = self._style.lookup(self._style_id, 'font')
        if font.Font(font=current_font).actual()['underline'] == 0:
            return 'normal'
        else:
            return 'underline'

    @underline.setter
    def underline(self, value):
        try:
            # 0 for normal, 1 for underline
            self._set_font_property('underline', ('normal', 'underline').index(value))
        except ValueError:
            raise ValueError(f"Underline must be either 'underline' or 'normal' (value specified was '{value}')")

    @property
    def strikethrough(self):
        current_font = self._style.lookup(self._style_id, 'font')
        if font.Font(font=current_font).actual()['overstrike'] == 0:
            return 'normal'
        else:
            return 'strikethrough'

    @strikethrough.setter
    def strikethrough(self, value):
        try:
            # 0 for normal, 1 for strikethrough (overstrike in tk-land)
            self._set_font_property('overstrike', ('normal', 'strikethrough').index(value))
        except ValueError:
            raise ValueError(f"Strikethrough style must be either 'strikethrough' or 'normal' "
                             f"(value specified was '{value}')")

    @property
    def colour(self):
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
                for y in layout[n+2:]:
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
        StyleLabel.__init__(self, container, text)
        self.url = url
        self.colour = 'blue'
        self.underline = 'underline'
        self.bind('<Enter>', lambda e: self.configure(cursor='hand2'))
        self.bind('<Button-1>', self._open_link)
        self.configure(takefocus=True)  # Labels don't normally take focus when tabbing

    def __str__(self):
        return f"<Hyperlink '{self.text}'>"

    def _open_link(self, e):
        if not self.disabled:
            import webbrowser
            webbrowser.open(self.url)


class Image(Label):
    def __init__(self, container, image):
        Label.__init__(self, container, None)
        self.image = image

    def __str__(self):
        return f"""<Image '{self.image}'>"""

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, image):
        image_extension = image[-3:]
        if not PILLOW and image_extension != 'gif':
            raise ValueError('Only gif images can be used at this time.')

        self._image = image

        if not PILLOW:
            self._tk_image = tk.PhotoImage(file=image)
        else:
            self._tk_image = ImageTk.PhotoImage(PILImage.open(image))

        self.configure(image=self._tk_image)

    # TODO: Overwrite the text setter to raise an error?


class Input(ttk.Entry, GooeyPieWidget):
    def __init__(self, container):
        GooeyPieWidget.__init__(self, container)
        self._value = tk.StringVar()
        ttk.Entry.__init__(self, container, textvariable=self._value)
        self._events['change'] = None
        self._observer = None  # Used in tkinter's trace method, for the 'change' event

    def __str__(self):
        return f"""<Input widget>"""

    @property
    def width(self):
        return self.cget('width')

    @width.setter
    def width(self, value):
        if type(value) != int or int(value) < 1:
            raise ValueError('Width must be a positive integer')
        self.configure(width=value)

    @property
    def text(self):
        return self._value.get()

    @text.setter
    def text(self, value):
        self._value.set(value)

    @property
    def secret(self):
        # 'show' will be the empty string if secret is not set
        return self.cget('show')

    @secret.setter
    def secret(self, value):
        if value:
            self.configure(show='●')
        else:
            self.configure(show='')

    @property
    def justify(self):
        return self.cget('justify')

    @justify.setter
    def justify(self, value):
        self.configure(justify=value)

    def select(self):
        self.focus()
        self.select_range(0, tk.END)


class Secret(Input):
    def __init__(self, container):
        Input.__init__(self, container)
        self.configure(show='●')

    def __str__(self):
        return f"""<Secret widget>"""

    def unmask(self):
        self.configure(show='')

    def mask(self):
        self.configure(show='●')

    def toggle(self):
        if self.cget('show'):
            self.unmask()
        else:
            self.mask()


class Listbox(tk.Listbox, GooeyPieWidget):
    def __init__(self, container, items=()):
        GooeyPieWidget.__init__(self, container)
        tk.Listbox.__init__(self, container)

        # Configuration options to make the listbox look more like a ttk widget
        self.configure(borderwidth=1, relief='flat', font=font.nametofont('TkDefaultFont'), activestyle='none',
                       highlightcolor='systemHighlight', highlightthickness=1, exportselection=0)

        # Different border colour names for Windows and Mac https://www.tcl.tk/man/tcl8.6/TkCmd/colors.htm
        if OS == 'Windows':
            self.configure(highlightbackground='systemGrayText')
        if OS == "Mac":
            self.configure(highlightbackground='systemBlackText')

        self.insert('end', *items)
        self._events['select'] = None

    def __str__(self):
        return f'<Listbox {tuple(self.items)}>'

    @property
    def height(self):
        """Returns the number of lines in the listbox"""
        return self.cget('height')

    @height.setter
    def height(self, lines):
        """Sets the *minimum* number of lines in the listbox. The number of visible lines may be different
        """
        self.configure(height=lines)

    @property
    def width(self):
        """Returns the number of lines in the listbox"""
        return self.cget('width')

    @width.setter
    def width(self, chars):
        """Sets the width of the listbox, in characters. Default is 20."""
        self.configure(width=chars)

    @property
    def items(self):
        """Returns a COPY of the items in the listbox"""
        return list(self.get(0, 'end'))

    @items.setter
    def items(self, items_):
        """Sets the contents of the listbox"""
        self.delete(0, 'end')
        self.insert(0, *items_)

    @property
    def multiple_selection(self):
        """Returns a Boolean indicating whether the listbox allows multiple items to be selected or not"""
        return self.cget('selectmode') == 'extended'

    @multiple_selection.setter
    def multiple_selection(self, multiple):
        """Sets if the listbox allows multiple items to be selected or not"""
        self.select_none()
        mode = 'extended' if multiple else 'browse'
        self.configure(selectmode=mode)

    @property
    def selected_index(self):
        """Returns the index(es), starting from 0, of the selected line.
        Returns None if nothing is selected.
        Returns a list of indexes if multiple selections are enabled.
        """
        select = self.curselection()
        if len(select) == 0:
            return None
        if self.multiple_selection:
            return list(select)
        else:
            return select[0]

    @selected_index.setter
    def selected_index(self, index):
        """Selects the line at the given index, counting from 0
        This will add to the current selection if multiple selection is set
        """
        # Clear the current selection if single selection only
        if not self.multiple_selection:
            self.select_none()

        self.selection_set(index)
        self.see(index)  # Show the selected line (in case it is not be in view)

    @property
    def selected(self):
        """Returns the item(s), starting from 0, of the currently selected line.
        Returns None if nothing is selected.
        Returns a list of items if multiple selections are enabled.
        """
        select = self.curselection()
        if len(select) == 0:
            return None
        if self.multiple_selection:
            return [self.get(0, 'end')[index] for index in select]
        else:
            return self.get(0, 'end')[select[0]]

    def select_none(self):
        """Deselects any items that may be selected in the listbox"""
        self.selection_clear(0, 'end')

    def select_all(self):
        """Selects (highlights) all items in the listbox. Multiple selection must be enabled"""
        if self.multiple_selection:
            self.selection_set(0, 'end')

    def add_item(self, item):
        """Adds an item to the end of the listbox"""
        self.insert('end', item)

    def add_item_to_start(self, item):
        """Adds an item to the top of the listbox"""
        self.insert(0, item)

    def remove_item(self, index):
        """Removes and returns the item at the given index"""
        if type(index) != int:
            raise ValueError('Cannot remove item from listbox - the index must be an integer')
        if index < 0:
            raise ValueError('Cannot remove item from listbox - the index cannot be negative')
        if index >= len(self.items):
            raise ValueError('Cannot remove item from listbox - index too large')

        # Get item, remove and return
        item = self.items[index]
        self.delete(index)
        return item

    def remove_selected(self):
        """Removes all items from the selected index(es) and returns"""
        if self.selected_index is not None:
            if self.multiple_selection:
                # Return a list of items if multiple selection enabled
                removed_items = []
                # traverse the selected indexes in reverse order to avoid
                # index repetition issues
                for index in reversed(self.selected_index):
                    # self.remove_item returns each removed item, append it to a list
                    removed_items.append(self.remove_item(index))
                # items were added to removed_items in reversed order, so return the reverse
                # to get the correct order back
                return list(reversed(removed_items))
            else:
                # Return single value
                index = self.selected_index
                removed_item = self.remove_item(index)
                self.selected_index = index   # Keep the existing selection
                return removed_item


class ScrolledListbox(Container, GooeyPieWidget):
    def __init__(self, container, items=()):
        Container.__init__(self, container)

        # Set container to fill cell
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Create listbox and scrollbar
        self._listbox = Listbox(self, items)
        self._scrollbar = tk.Scrollbar(self, orient='vertical')

        # Configure behaviour of scrollbar
        self._scrollbar.config(command=self._listbox.yview)
        self._listbox.config(yscrollcommand=self._scrollbar.set)

        # Add to parent Container
        self._listbox.grid(row=0, column=0, sticky='nsew')
        self._scrollbar.grid(row=0, column=1, sticky='nsew')

        # Default scrollbar settings
        self._scrollbar_visible = 'auto'
        self.bind('<Configure>', self._update_scrollbar)  # Update scrollbar visibility when listbox changes size

        # Alias Listbox methods for this class that don't affect its contents
        # (methods that affect the contents need to take the additional step of checking
        # for the scrollbar visibility if scrollbar visibility is set to 'auto')
        self.select_all = self._listbox.select_all
        self.select_none = self._listbox.select_none

        GooeyPieWidget.__init__(self, container)
        self._events['select'] = None

    def _visible_lines(self):
        """Returns the number of lines that the listbox can currently display by dividing the height of the listbox
        by the height of the font (in pixels). This may be different to the height property set on the listbox if
        it has been stretched to fill in the vertical direction.
        Used to determine whether or not to show the scrollbar when set it is set to 'auto'
        """
        self._listbox.update()
        font_height = font.Font(font='TkDefaultFont').metrics('linespace')
        font_height *= 1.05  # fudge to account for line spacing, presumably
        listbox_height = self._listbox.winfo_height()
        return int(listbox_height / font_height)

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
            if len(self._listbox.items) > self._visible_lines():
                self._show_scrollbar()
            else:
                self._hide_scrollbar()

    def _hide_scrollbar(self):
        """Hides the scrollbar from the listbox"""
        self._listbox.grid_remove()
        self._listbox.grid(row=0, column=0, sticky='nsew', columnspan=2)
        self._scrollbar.grid_remove()

    def _show_scrollbar(self):
        """Shows the scrollbar on the side of the listbox"""
        self._listbox.grid_remove()
        self._listbox.grid(row=0, column=0, sticky='nsew', columnspan=1)
        self._scrollbar.grid()

    @property
    def height(self):
        return self._listbox.cget('height')

    @height.setter
    def height(self, lines):
        self._listbox.configure(height=lines)

    @property
    def width(self):
        return self._listbox.width

    @width.setter
    def width(self, chars):
        self._listbox.width = chars

    @property
    def scrollbar(self):
        return self._scrollbar_visible

    @scrollbar.setter
    def scrollbar(self, setting):
        if setting not in ('auto', 'visible', 'hidden'):
            raise GooeyPieError("Invalid scrollbar option - must be set to 'auto', 'hidden' or 'visible'")
        self._scrollbar_visible = setting
        self._update_scrollbar()

    @property
    def items(self):
        """Returns a COPY of the items in the listbox"""
        return self._listbox.items

    @items.setter
    def items(self, items_):
        """Sets the contents of the listbox"""
        self._listbox.items = items_
        self._update_scrollbar()

    @property
    def multiple_selection(self):
        """Returns a Boolean indicating whether the listbox allows multiple items to be selected or not"""
        return self._listbox.multiple_selection

    @multiple_selection.setter
    def multiple_selection(self, multiple):
        """Sets if the listbox allows multiple items to be selected or not"""
        self._listbox.multiple_selection = multiple

    @property
    def selected(self):
        """Returns the item(s), starting from 0, of the currently selected line.
        Returns None if nothing is selected.
        Returns a list of items if multiple selections are enabled.
        """
        return self._listbox.selected

    @property
    def selected_index(self):
        """Returns the index(es), starting from 0, of the selected line.
        Returns None if nothing is selected.
        Returns a list of indexes if multiple selections are enabled.
        """
        return self._listbox.selected_index

    @selected_index.setter
    def selected_index(self, index):
        """Selects the line at the given index, counting from 0
        This will add to the current selection if multiple selection is set
        """
        self._listbox.selected_index = index

    def add_item(self, item):
        """Adds an item to the end of the listbox"""
        self._listbox.add_item(item)
        self._update_scrollbar()

    def add_item_to_start(self, item):
        """Adds an item to the top of the listbox"""
        self._listbox.add_item_to_start(item)
        self._update_scrollbar()

    def remove_item(self, index):
        """Removes and returns the item at the given index"""
        removed = self._listbox.remove_item(index)
        self._update_scrollbar()
        return removed

    def remove_selected(self):
        """Removes all items from the selected index(es) and returns"""
        removed = self._listbox.remove_selected()
        self._update_scrollbar()
        return removed


class Textbox(scrolledtext.ScrolledText, GooeyPieWidget):
    def __init__(self, container, width=20, height=5):
        GooeyPieWidget.__init__(self, container)
        scrolledtext.ScrolledText.__init__(self, container, width=width, height=height)

        self.configure(borderwidth=1, relief='flat', font=font.nametofont('TkDefaultFont'),
                       wrap='word', highlightcolor='systemHighlight', highlightthickness=1)

        # Different border colour names for Windows and Mac
        # https://www.tcl.tk/man/tcl8.6/TkCmd/colors.htm
        if OS == 'Windows':
            self.configure(highlightbackground='systemGrayText')
        if OS == "Mac":
            self.configure(highlightbackground='systemBlackText')

        self.bind('<Tab>', self.focus_next_widget)
        self.bind('<Shift-Tab>', self.focus_previous_widget)
        self.bind('<Control-Tab>', self.insert_tab)
        # self._events['change'] = None

    # TODO: readonly option
    # https://stackoverflow.com/questions/3842155/is-there-a-way-to-make-the-tkinter-text-widget-read-only

    def __str__(self):
        return f"""<Textbox object>"""

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
        """Allows the user to insert a tab character into the textbox with ctrl"""
        event.widget.insert('current', '\t')
        return 'break'

    @property
    def width(self):
        return self.cget('width')

    @width.setter
    def width(self, cols):
        self.configure(width=cols)

    @property
    def height(self):
        return self.cget('width')

    @height.setter
    def height(self, rows):
        self.configure(height=rows)

    @property
    def text(self):
        """Get all text. Strip the trailing newline added by tkinter"""
        return self.get('1.0', 'end')[:-1]

    @text.setter
    def text(self, text):
        """Replaces the contents of the textbox"""
        self.clear()
        self.insert('1.0', text)

    def clear(self):
        """Clear the contents of the textbox"""
        self.delete('1.0', 'end')

    def prepend(self, text):
        """Adds the given text to the beginning of the textbox"""
        self.text = f'{text}{self.text}'

    def prepend_line(self, text):
        """Adds the given text to the beginning of the textbox including a newline"""
        self.prepend(f'{text}\n')

    def append(self, text):
        """Adds the given text to the end of the textbox"""
        self.text = f'{self.text}{text}'

    def append_line(self, text):
        """Adds the given text to the end of the textbox including a newline"""
        self.append(f'{text}\n')


class ImageButton(Button):
    def __init__(self, container, image, callback, text=''):
        super().__init__(container, text, callback, 0)
        image_extension = image[-3:]
        if not PILLOW and image_extension != 'gif':
            raise ValueError('Only gif images can be used at this time.')

        self._image = image

        if not PILLOW:
            self._tk_image = tk.PhotoImage(file=image)
        else:
            self._tk_image = ImageTk.PhotoImage(PILImage.open(image))

        self._tk_image = ImageTk.PhotoImage(PILImage.open(image))
        self.configure(image=self._tk_image, compound='left' if text else 'image')

    def __str__(self):
        return f"""<ImageButton '{self.image}'>"""

    @property
    def image_position(self):
        return self.cget('compound')

    @image_position.setter
    def image_position(self, position):
        """If an image button includes text, set where the image should appear relative to that text"""
        self.configure(compound=position)


class Checkbox(ttk.Checkbutton, GooeyPieWidget):
    def __init__(self, container, text):
        GooeyPieWidget.__init__(self, container)
        self._checked = tk.BooleanVar(value=False)
        ttk.Checkbutton.__init__(self, container, text=text, variable=self._checked)
        self.state(['!alternate'])
        self._events['change'] = None   # Checkboxes support the 'change' event

    def __str__(self):
        return f'''<Checkbox '{self.cget("text")}'>'''

    @property
    def checked(self):
        return self._checked.get()

    @checked.setter
    def checked(self, state):
        self._checked.set(state)


class RadiogroupBase(GooeyPieWidget):
    """Base class used by Radiogroup and LabelledRadiogroup"""
    def __init__(self, container, choices, orient, override_spacing=False):
        GooeyPieWidget.__init__(self, container)
        self._events['change'] = None   # Radiobuttons support the 'change' event
        self._selected = tk.StringVar()

        # If images are used (to be implemented, need to support passing a list of 2-tuples,
        # where first item is the image, second is the value returned

        length = len(choices)
        # Set the appropriate grid based on the orientation. Create associated lists used when calling add()
        if orient == 'vertical':
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
                    if orient == 'vertical':
                        margins[2] = pady[1]
                    else:
                        # Bit more spacing between horizontal items
                        margins[1] = padx[1] * 2

            if isinstance(self, LabelRadiogroup):
                margins = ['auto'] * 4
                # For vertically aligned radiogroups, reduce the vertical spacing between items.

                if orient == 'vertical':
                    if pos != length - 1:
                        margins[2] = 0

            self.add(radiobutton, rows[pos], columns[pos], align='left', margins=margins)

    @property
    def options(self):
        return tuple(widget.cget('text') for widget in self.winfo_children())

    @property
    def selected(self):
        if self._selected.get():
            return self._selected.get()
        else:
            return None

    @selected.setter
    def selected(self, value):
        self._selected.set(value)

    def deselect(self):
        """Deselects all options"""
        self._selected.set(None)

    def disable(self, index):
        """Disables the radiobutton at the given index"""
        self.winfo_children()[index].configure(state='disabled')

    def enable(self, index):
        """Disables the radiobutton at the given index"""
        self.winfo_children()[index].configure(state='enabled')


class Radiogroup(Container, RadiogroupBase):
    """A set of radio buttons"""
    def __init__(self, container, choices, orient='vertical'):
        Container.__init__(self, container)
        RadiogroupBase.__init__(self, container, choices, orient, True)

    def __str__(self):
        return f'<Radiogroup {tuple(self.options)}>'


class LabelRadiogroup(LabelContainer, RadiogroupBase):
    """A set of radio buttons in a label frame"""
    def __init__(self, container, title, choices, orient='vertical'):
        LabelContainer.__init__(self, container, title)
        RadiogroupBase.__init__(self, container, choices, orient)

    def __str__(self):
        return f'<LabelRadiogroup {tuple(self.options)}>'



class OldRadiogroupBase(GooeyPieWidget):
    """Base class used by Radiogroup and LabelledRadiogroup"""
    def __init__(self, container, choices, orient):
        GooeyPieWidget.__init__(self, container)
        self._events['change'] = None   # Radiobuttons support the 'change' event
        self._selected = tk.StringVar()

        # If images are used (to be implemented, need to support passing a list of 2-tuples,
        # where first item is the image, second is the value returned

        if isinstance(choices, (list, tuple)):
            side = 'left' if orient == 'horizontal' else 'top'
            for choice in choices:
                radiobutton = ttk.Radiobutton(self, text=choice, variable=self._selected, value=choice)
                radiobutton.pack(expand=True, fill='x', padx=8, pady=8, side=side)

    @property
    def options(self):
        return tuple(widget.cget('text') for widget in self.winfo_children())

    @property
    def selected(self):
        if self._selected.get():
            return self._selected.get()
        else:
            return None

    @selected.setter
    def selected(self, value):
        self._selected.set(value)


class OldRadiogroup(ttk.Frame, RadiogroupBase):
    """A set of radio buttons"""
    def __init__(self, container, choices, orient='vertical'):
        ttk.Frame.__init__(self, container)
        RadiogroupBase.__init__(self, container, choices, orient)

    def __str__(self):
        return f'<Radiogroup {tuple(self.options)}>'


class OldLabelRadiogroup(ttk.LabelFrame, RadiogroupBase):
    """A set of radio buttons in a label frame"""
    def __init__(self, container, title, choices, orient='vertical'):
        ttk.LabelFrame.__init__(self, container, text=title)
        RadiogroupBase.__init__(self, container, choices, orient)

    def __str__(self):
        return f'<LabelRadiogroup {tuple(self.options)}>'


class Dropdown(ttk.Combobox, GooeyPieWidget):
    def __init__(self, container, choices):
        GooeyPieWidget.__init__(self, container)
        ttk.Combobox.__init__(self, container, values=choices, exportselection=0)
        self.state(['readonly'])
        self._events['select'] = None
        self.choices = choices

    def __str__(self):
        return f'<Dropdown {tuple(self.choices)}>'

    @property
    def selected(self):
        index = self.current()
        if index == -1:
            return None
        else:
            return self.cget('values')[index]

    @selected.setter
    def selected(self, value):
        """Sets the given item """
        try:
            self.cget('values').index(value)
            self.set(value)
        except ValueError:
            raise ValueError(f"Cannot set Dropdown to '{value}' as it is not one of the options")

    @property
    def selected_index(self):
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

    def deselect(self):
        """Sets the selected item in the dropdown to a blank"""
        self.set('')


class Number(ttk.Spinbox, GooeyPieWidget):
    def __init__(self, container, low, high, increment=1):
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

    @property
    def value(self):
        """Returns the value of the Number widget according to the type of increment
        Note: The ttk.Spinbox widget get() method always returns a string
        """
        val = self.get()
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
        # Typesafe setter not being used:
        # if type(value) not in (int, float):
        #     raise ValueError(f'Invalid number {repr(value)} specified for {self}')
        # if value < self.cget('from'):
        #     raise ValueError(f'{value} is below the minimum value for {self}')
        # if value > self.cget('to'):
        #     raise ValueError(f'{value} is above the maximum value for {self}')

    @property
    def width(self):
        return self.cget('width')

    @width.setter
    def width(self, value):
        """Sets the width of the spinbox in characters (includes the control buttons)"""
        self.configure(width=value)

    # The underlying ttk widget (Spinbox) has 3 states: normal, disabled and readonly, so the read_only getter/setter
    # and disabled getter/setter is overridden to deal with GooeyPie supporting both properties 'separately'. In short,
    # a disabled widget cannot have its read_only property altered, but no error is raised if that happens
    @property
    def read_only(self):
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
        return bool(self.cget('wrap'))

    @wrap.setter
    def wrap(self, state):
        self.configure(wrap=bool(state))


class Table(ttk.Treeview, GooeyPieWidget):
    """For displaying tabular data"""
    def columns(self, cols):
        """Sets the column names of the table"""
        pass

    def add_data(self, data):
        """Adds a row of data to the table"""
        pass

