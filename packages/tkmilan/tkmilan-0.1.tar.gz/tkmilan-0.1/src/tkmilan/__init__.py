#!/usr/bin/env python
"""
`tkinter`'s evil twin.
"""
import typing
import logging
import warnings
import math
from contextlib import contextmanager

import tkinter as tk
from tkinter import ttk
import tkinter.simpledialog  # Implemented in newer typshed versions

from . import model
from . import var
from . import mixin
from . import exception
from . import spec
from . import parser
from . import fn


# TypeChecking
class varTree(var.ObjectList[model.TreeElement]):
    '''Type-Checking variable type for `Tree`.'''
    pass


# Useful models
Binding = model.Binding

# Layouts
# TODO: Transform into a Enum
AUTO = mixin.AUTO
'''Automatic Layout.
'''
HORIZONTAL = mixin.HORIZONTAL
'''Horizontal (1 row) Layout.
'''
VERTICAL = mixin.VERTICAL
'''Vertical (1 column) Layout.
'''

logger = logging.getLogger(__name__)


# Usable Widgets


class RootWindow(tk.Tk, mixin.ContainerWidget):
    '''A root window, the toplevel widget for the entire application.

    Usually there's only one of this in a single application. Multiple root
    windows are unsupported.

    See `tkinter.Tk`.

    Args:
        theme: Theme to use. Default to choosing a tasteful choice depending on
            the OS.

    Note:
        Technically, it should be OK to use multiple root windows per-process,
        but this hasn't been tested, there are no test cases where this makes
        sense.
    '''
    isNoneable: bool = False  # Always present, no matter what

    def __init__(self, *args, theme: str = None, **kwargs):
        self._bindings_global: typing.MutableMapping[str, model.BindingGlobal] = {}
        super().__init__()  # tk.Tk
        kwargs['expand'] = False  # `Toplevel` has no parent grid to expand
        self.init_container(*args, **kwargs)
        self.style = self.setup_style(theme)

    def setup_style(self, theme):
        style = ttk.Style(self)
        if theme is None:
            # Good for Linux
            # On Windows, check: 'winnative', 'vista'
            theme = 'alt'
        style.theme_use(theme)
        return style

    def instate(self, statespec, callback=None):
        ''''''  # Do not document
        # Not applicable to the root window
        return None

    def state(self, statespec):
        ''''''  # Do not document
        # Not applicable to root window
        raise NotImplementedError


class FrameUnlabelled(ttk.Frame, mixin.ContainerWidget):
    '''A simple frame to hold other widgets, visually invisible.

    This is the simplest form of `mixin.ContainerWidget`, just a bunch of
    widgets. There's no separation between the outside and the inside of the
    frame.

    There is no Python documentation, see ``Tk`` `ttk.Frame <https://www.tcl.tk/man/tcl/TkCmd/ttk_frame.html>`_ documentation.

    Args:
        parent: The parent widget. Can be a `RootWindow` or another `mixin.ContainerWidget`.

    See Also:
        `FrameLabelled`: Visible version, with a label.
    '''
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        self.init_container(*args, **kwargs)


class FrameLabelled(ttk.LabelFrame, mixin.ContainerWidget):
    '''A frame to hold other widgets surrounded by a line, including a label.

    This is a frame with a label. It is visually separated from the other
    widgets. You can control the label position.

    There is no Python documentation, see ``Tk`` `ttk.LabelFrame <https://www.tcl.tk/man/tcl/TkCmd/ttk_labelframe.html>`_ documentation.

    Args:
        label: The label to include on the frame separator. Can be given as a class variable.
        labelAnchor: The position of the label on the frame separator.
            Given as one of the cardinal points.
            Defaults to a OS-specific location (`model.CP.default`).

    See Also:
        `FrameUnlabelled`: Invisible version, without a label.

        `FrameStateful`: Support for an embedded `Checkbox` as label.
    '''
    label: typing.Optional[str] = None

    def __init__(self, parent, *args, label: typing.Optional[str] = None, labelAnchor: model.CP = model.CP.default, labelwidget=None, **kwargs):
        chosen_label = self.label or label
        if chosen_label is None:
            raise ValueError('{self!r}: Missing required label')
        super().__init__(parent, text=chosen_label, labelanchor=labelAnchor.value)
        self.init_container(*args, **kwargs)


class Label(ttk.Label, mixin.SingleWidget):
    '''A label, can be text, image, or both.

    This is a label, a static-ish widget without interaction.

    This must include at least some text or an image, even though both are optional.

    No state is included.

    There is no Python documentation, see ``Tk`` `ttk.Label <https://www.tcl.tk/man/tcl/TkCmd/ttk_label.html>`_ documentation.

    Args:
        image: The image to show. Optional.
            See ``Tk`` `tk.Image <https://www.tcl.tk/man/tcl/TkCmd/image.html>`_ documentation.

        onClick: Override the `onClick` method.

        parent: The parent widget. Can be a `RootWindow` or another `mixin.ContainerWidget`.
        label: The text to show. Optional.
    '''
    state_type = var.nothing

    def __init__(self, parent, *, label: str = None, onClick: typing.Callable = None, image: tk.Image = None, **kwargs):
        if label is None and image is None:
            raise exception.InvalidWidgetDefinition(Label)
        self.init_single()
        if onClick:
            self.onClick = onClick  # type: ignore  # Assinging to a method
        kwargs['text'] = label
        super().__init__(parent, **kwargs)  # ttk.Label
        if image:
            self.set_image(image)
        self.binding('<Button-1>', self.invoke_onClick)

    def invoke_onClick(self, event=None):
        ''''''  # Internal, do not document
        self.onClick()

    def set_image(self, image: tk.Image):
        '''Change the label image.
        '''
        self._image = image  # Save a reference to avoid garbage collection
        self['image'] = self._image

    # TODO: Pass the event object?
    # TODO: Not needed on labels
    def onClick(self):
        """Callback to be executed when clicking this widget.

        Defaults to doing nothing.

        Available for subclass redefinition.
        """
        pass


class Button(ttk.Button, mixin.SingleWidget):
    '''A button with a label.

    This is a button, with a label. The main interaction is being clicked on.

    No state is included.

    There is no Python documentation, see ``Tk`` `ttk.Button <https://www.tcl.tk/man/tcl/TkCmd/ttk_button.html>`_ documentation.

    Args:
        width: The button width, in pixels. Defaults to an ad-hoc calculation
            based on the length of the label.
        onClick: Override the `onClick` method.

        parent: The parent widget. Can be a `RootWindow` or another `mixin.ContainerWidget`.
        label: The label to include inside the button
    '''
    state_type = var.nothing

    def __init__(self, parent, *, label: str, onClick: typing.Callable = None, width: int = None, **kwargs):
        self.init_single(variable=None)  # No state here
        if onClick:
            self.onClick = onClick  # type: ignore  # Assinging to a method
        kwargs.update({
            'text': label,
            'width': width or Button.__width(len(label or 'M')),
            'command': self.invoke_onClick,
        })
        super().__init__(parent, **kwargs)  # ttk.Button

    def invoke_onClick(self):
        ''''''  # Internal, do not document
        self.onClick()

    def onClick(self):
        """Callback to be called when clicking this widget.

        Defaults to doing nothing.

        Available for subclass redefinition.
        """
        pass

    @staticmethod
    def __width(chars: int):
        # TODO: Measure the font size: https://stackoverflow.com/a/30952406
        return math.ceil(-4 + 6 * math.pow(chars, 0.41))


class Checkbox(ttk.Checkbutton, mixin.SingleWidget):
    '''A checkbox, simple boolean choice.

    This is a checkbox with a label. The main interaction is being clicked on,
    which toggle its value.

    The state is a single `bool` value.

    There is no Python documentation, see ``Tk`` `ttk.Checkbutton <https://www.tcl.tk/man/tcl/TkCmd/ttk_checkbutton.htm>`_ documentation.

    Args:

        parent: The parent widget. Can be a `RootWindow` or another `mixin.ContainerWidget`.
        label: The label to include besides the checkbox. It is included on the right side (``tk.E``).
        readonly: Should the widget allow interaction to toggle its value.
        variable: Use an externally defined variable, instead of creating a new one specific for this widget.
    '''
    state_type = var.Boolean

    def __init__(self, parent, *, label: str, readonly: bool = False, variable: var.Boolean = None, **kwargs):
        self.init_single(variable, gkeys=['readonly'])
        kwargs.update({
            'text': label,
            'onvalue': True,
            'offvalue': False,
            'variable': self.variable,
        })
        super().__init__(parent, **kwargs)  # ttk.Checkbutton
        if readonly:
            # Read-only checkboxen are editable, for some reason
            self.gstate = model.GuiState(enabled=False, readonly=True)

    def toggle(self) -> None:
        '''Switch the variable state to its opposite (`not <not>`).'''
        self.wstate = not self.wstate


class Entry(ttk.Entry, mixin.SingleWidget):
    '''An entry widget, single-line text editor.

    This is an entry box, a single-line editor for strings. The main
    interaction is editing the text contained within.

    The state is a single `str` value.

    There is no Python documentation, see ``Tk`` `ttk.Entry <https://www.tcl.tk/man/tcl/TkCmd/ttk_entry.htm>`_ documentation.

    Args:
        parent: The parent widget. Can be a `RootWindow` or another `mixin.ContainerWidget`.
        label: The label to include besides the entry. **Not implemented yet**.
        variable: Use an externally defined variable, instead of creating a new one specific for this widget.
    '''
    state_type = var.String

    def __init__(self, parent, *, label: str, variable: typing.Optional[var.String] = None, **kwargs):
        self.init_single(variable)
        self.label = label  # TODO: Show label somehow
        kwargs.update({
            'textvariable': self.variable,
        })
        super().__init__(parent, **kwargs)  # ttk.Entry


class Combobox(ttk.Combobox, mixin.SingleWidget):
    '''A combobox widget, combining an `Entry` with a `Listbox`.

    This is a combobox, an `Entry` with a button that shows a pop-up `Listbox`
    with some predefined ``values``.

    The entry can be ``readonly``, in which case the only possible values are
    the ones shown on the value list, otherwise the entry is editable with
    arbitrary values, just like any `Entry`.

    The ``immediate`` parameter can be used to control when is the default
    value setup. Defaults to being set only when the GUI stabilizes, but it can
    be set as soon as possible.

    There is no Python documentation, see ``Tk`` `ttk.Combobox <https://www.tcl.tk/man/tcl/TkCmd/ttk_combobox.html>`_ documentation.

    Args:
        values: A list of values to show on the pop-up listbox.

        parent: The parent widget. Can be a `RootWindow` or another `mixin.ContainerWidget`.
        label: The label to include besides the combobox. **Not implemented yet**.
        readonly: Should the widget allow interaction to toggle its value.
        immediate: Set the default value ASAP (`True`), or delay it after the
            GUI is stable (`False`). Defaults to `False`.
    '''
    state_type = var.String

    def __init__(self, parent, values: spec.SpecCountable, *, label: str, readonly: bool = True, variable: var.String = None, immediate: bool = False, **kwargs):
        self.init_single(variable, gkeys=['readonly'])
        self.label = label  # TODO: Show label somehow
        self.specValues = values
        kwargs.update({
            'textvariable': self.variable,
            'values': list(self.specValues.all()),
        })
        super().__init__(parent, **kwargs)  # ttk.Combobox
        if immediate:
            self.setDefault()
        else:
            self.after_idle(self.setDefault)
        if readonly:
            self.gstate = model.GuiState(readonly=True)
        if __debug__:
            if type(self) == Combobox and isinstance(self.specValues, spec.StaticMap):
                warnings.warn('See `ComboboxMap` for using the values correctly', stacklevel=2)

    # TODO: This could be a common `mixin.SingleWidget` method?
    def setDefault(self):
        '''Set the current state to the default label.'''
        self.wstate = self.specValues.default

    def eSet(self, label: str) -> typing.Callable:
        '''Return an event function to set the state a certain label.'''
        if label not in self.specValues:
            raise exception.InvalidCallbackDefinition(f'Setting an invalid label: {label}')

        def eSet():
            self.wstate = label
        return eSet


class ComboboxMap(Combobox):
    '''A combobox widget, prepared to use `spec.StaticMap`.

    This is just a normal `Combobox`, but the ``values`` object must be a
    `spec.StaticMap`, and the widget value will be returned as its value, not
    the label.

    Note:
        This is still WIP, seems like a very big hack for now.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert isinstance(self.specValues, spec.StaticMap), f'{self}: values must be a `spec.StaticMap`'

    def state_get(self, *args, **kwargs):
        ''''''  # Do not document
        label = super().state_get(*args, **kwargs)
        value = self.specValues.value(label)
        # if __debug__:
        #     logger.debug('L[%s] => %r', label, value)
        return model.VState(value, label=label)

    def state_set(self, state, *args, **kwargs):
        ''''''  # Do not document
        # Support setting labels and VState
        if isinstance(state, model.VState):
            label = self.specValues.label(state.value)
            if __debug__:
                if state.label:
                    assert state.label == label
                # logger.debug('%r => %s', state, label)
        else:  # Setting a simple label
            label = state
            if __debug__:
                pass  # logger.debug('L[%s]', label)
        return super().state_set(label, *args, **kwargs)

    def eSetValue(self, value):
        '''Wraper for `Combobox.eSet`, prepared to use `spec.StaticMap`.'''
        assert isinstance(self.specValues, spec.StaticMap)
        return self.eSet(self.specValues.label(value))

    if __debug__:
        # Warn about trace usage
        def trace(self, *args, **kwargs):
            if self.specValues not in kwargs.values():
                warnings.warn('Make sure to send `self.specValues` to get the "real" values', stacklevel=2)
            return super().trace(*args, **kwargs)


class Listbox(ttk.Treeview, mixin.SingleWidget):
    '''A listbox widget, a list of strings.

    This is a modern variation of the listbox, a way to display several rows of
    content (simple strings, in this case), and be able to select one at a
    time.

    The ``width`` must be fixed to a certain value, there's no support to
    automatically stretch if to the grid location.

    The ``height`` can be hardcoded to a value, or it can vary with the
    contents. Note that the ``maxHeight`` is smaller than the amount of rows to
    display, no scrollbar is shown, but the list can be
    scrolled with the mouse wheel.

    The state is a `list` of `str` values, `var.StringList`.

    See `Python ttk.Treeview <tkinter.ttk.Treeview>` and ``Tk``
    `ttk.Treeview <https://tcl.tk/man/tcl8.6/TkCmd/ttk_treeview.htm>`_
    documentation.

    Args:
        parent: The parent widget. Can be a `RootWindow` or another `mixin.ContainerWidget`.
        label: The label to include besides the listbox. **Not implemented yet**.
        width: The maximum width of the widget, in pixels. This is the width of
            the only column. If the widget itself grows larger than this value, the
            column does not scale.
        minWidth: The minimum width of the widget, in pixels. This is the
            minimum width of the only column.
        height: If given, always show this quantity of rows. If it is `None`,
            the number of permanently shown rows will vary between ``minHeight``
            and ``maxHeight``.
        minHeight: If ``height`` is `None`, make sure this number of rows is
            always visible.
        maxHeight: If ``height`` is `None`, make sure there are no more
            visible rows than this number. Optional, when `None`, there's no
            upport limit on the visible number of rows.
        columnConfig: Override configuration for all columns. Advanced usage only.

        variable: Use an externally defined variable, instead of creating a new one specific for this widget.
    '''
    state_type = var.StringList

    def __init__(self, parent, *, label: str = None, variable: var.StringList = None,
                 columnConfig: typing.Mapping[str, typing.Any] = None,
                 width: int = 200, minWidth: int = 20,
                 height: int = None, minHeight: int = 1, maxHeight: int = None,
                 **kwargs):
        kwargs.update({
            'columns': ('text',),  # Single Column
            'show': [],  # Hide tree chars and headings
            'selectmode': tk.BROWSE,  # Select single element
        })
        self.heightRange: typing.Optional[typing.Tuple[int, typing.Optional[int]]]
        if height is None:
            self.heightRange = minHeight, maxHeight
        else:
            kwargs['height'] = height  # Hardcode the height value
            self.heightRange = None
        # Configure (single) column
        cConfig = {
            'width': width,
            'minwidth': minWidth,
            'anchor': tk.CENTER,
            'stretch': True,
        }
        if columnConfig:
            cConfig.update(columnConfig)
        # Apply setup variables
        self.init_single(variable)
        super().__init__(parent, **kwargs)  # ttk.Treeview
        for c in self['columns']:
            self.column(c, **cConfig)
        # Trace variable state
        self.trace(self.__listbox_set, trace_name=f'__:{__name__}')

    def get_selection_mode(self) -> str:
        '''Get the selection mode.

        Thiw widget supports only a single selection mode, ``tk.BROWSE``, so
        this always return that value.
        '''
        return str(self.cget('selectmode'))

    def selection(self):
        '''Get the selected value.

        Returns:
            Since this supports only a single selection, return the selected
            value, or ``None`` if none is selected.
        '''
        value = super().selection()
        if self.get_selection_mode() == tk.BROWSE:
            if len(value) == 1:
                return value[0]
            else:
                return None
        else:
            return value

    def __listbox_set(self, *args, **kwargs):
        # This function is called when the value changes
        # It's the implementation that binds the variable and the widget,
        #  so this should be idempotent
        value = self.variable.get()
        # TODO: Be smart about changing the current state? Measure this.
        # Delete the current children
        self.delete(*self.get_children())
        # Add everything from the value
        for element in value:
            self.insert('', 'end', element, values=[element])
        if self.heightRange is not None:
            minHeight, maxHeight = self.heightRange
            wsize = max(minHeight, len(value))
            if maxHeight:
                wsize = min(maxHeight, wsize)
            if __debug__:
                logger.debug(f'{self}: Auto Height: {wsize}')
            self.configure(height=wsize)


class FrameStateful(ttk.LabelFrame, mixin.ContainerWidget):
    '''A frame to hold other widgets, with a checkbox.

    This is a frame with an embedded checkbox `cstate_widget` as "label". This
    label controls the enabled state of the child widgets. You can control the
    checkbox position.

    There is no Python documentation, see ``Tk`` `ttk.LabelFrame <https://www.tcl.tk/man/tcl/TkCmd/ttk_labelframe.html>`_ documentation.
    Note the ``labelwidget`` option.

    Args:
        label: The label to include on the frame separator. Can be given as a class variable.
        labelAnchor: The position of the label on the frame separator.
            Given as one of the cardinal points.
            Defaults to a OS-specific location (`model.CP.default`).
        defaultCstate: The default value for `cstate`. Defaults to starting
            enabled.

    See Also:
        `FrameLabelled`: A simpler version of this, without the embedded checkbox.
    '''
    label: typing.Optional[str] = None

    class __w_cstate(Checkbox):
        isHelper = True

    cstate_widget: __w_cstate
    '''The widget for the embedded `Checkbox`.

    Uses the `cstate` variable.

    Note:
        The widget type is a local `Checkbox` subclass, specific for this widget.
    '''
    cstate: var.Boolean
    '''The variable holding the embedded `Checkbox` state.

    Used on the `cstate_widget`
    '''

    def __init__(self, parent, *args, label: typing.Optional[str] = None, labelAnchor: model.CP = model.CP.default, defaultCstate: bool = True, **kwargs):
        # Create the checkbox widget
        chosen_label = self.label or label
        if chosen_label is None:
            raise ValueError('{self!r}: Missing required label')
        cstate_widget = self.__class__.__w_cstate(parent, label=chosen_label, readonly=False)
        assert isinstance(cstate_widget.variable, var.Boolean), f'{self!r} checkbox widget is not a simple boolean'
        self.cstate = cstate_widget.variable
        # Usual Initialization
        super().__init__(parent, labelwidget=cstate_widget, labelanchor=labelAnchor.value)
        self.init_container(*args, **kwargs)
        # Configure the checkbox widget
        self.cstate_widget = cstate_widget
        self.cstate_widget.trace(self.onChanged_cstate)
        self.cstate.set(defaultCstate)

    def state_get(self, *args, **kwargs) -> model.WState[bool, typing.Any]:
        ''''''  # Do not document
        return model.WState(
            self.cstate.get(),
            super().state_get(*args, **kwargs),
        )

    def state_set(self, state: model.WState, *args, **kwargs):
        ''''''  # Do not document
        assert isinstance(state.state, bool), f'Invalid WState: {state!r}'
        self.cstate.set(state.state)
        super().state_set(state.substate, *args, **kwargs)

    def set_gui_state(self, state: typing.Optional[model.GuiState] = None, **kwargs) -> None:
        # "Trace" the frame enabled status
        frame_enabled = kwargs.get('enabled', None) if state is None else state.enabled
        super().set_gui_state(state, **kwargs)
        if isinstance(frame_enabled, bool):
            state_enabled = self.cstate.get()
            if __debug__:
                logger.debug(f'S| {self}: F={frame_enabled} S={state_enabled}')
            # TODO: unsetOnDisable
            # TODO: setOnEnable
            # self.cstate.set(frame_enabled)
            self.cstate_widget.gstate = model.GuiState(enabled=frame_enabled)
            self.set_gui_substate(enabled=frame_enabled and state_enabled)

    def onChanged_cstate(self, cstate, etype):
        status = cstate.get()
        assert etype == 'write'
        if __debug__:
            logger.debug(f'{self}: {status}')
        self.set_gui_substate(model.GuiState(enabled=status))


# TODO: Use `tk.scrolledtext.ScrolledText`?
class EntryMultiline(tk.Text, mixin.SingleWidget):
    '''A multiline text widget, supporting `LTML` contents.

    This is a multiline version of the `Entry` widget, with rich text
    capabilities.
    Supports only the readonly state, that is, the widget contents can only be
    edited programatically.

    The state is a single `str` value, internally parsed to `parser.LTML
    <LTML>`.

    There is no Python documentation, see ``Tk`` `tk.Text <https://www.tcl.tk/man/tcl/TkCmd/text.htm>`_ documentation.

    Args:
        parent: The parent widget. Can be a `RootWindow` or another `mixin.ContainerWidget`.
        variable: Use an externally defined variable, instead of creating a new
            one specific for this widget.

    .. note::

        The underlying widget is not part of `ttk <tkinter.ttk>` like most others. All
        efforts are expended to make this an implementation detail, without
        practical effects.
    '''
    state_type = var.String

    def __init__(self, parent, *, variable: var.String = None, **kwargs):
        self.init_single(variable)
        kwargs.pop('state', None)  # Support only readonly state
        super().__init__(parent, **kwargs)  # tk.Entry
        readonly = True  # Support only readonly state, for now...
        # GUI State Tracker
        # - Since this is not a `ttk.Widget`, this need to be emulated
        self.__gstate = model.GuiState(enabled=True, readonly=readonly)
        # State Tracker
        self.trace(self._varChanged, trace_name=f'__:{__name__}')

        # Bindings
        # TODO: Support `BindingTag`(`self.binding_tag`)?
        self.tag_bind('a', '<Button-1>', self._onClickTag, add=True)
        if readonly:
            self.binding('<Double-Button-1>', lambda e: 'break')  # Disable double click

    def _varChanged(self, var, etype):
        vs = var.get()
        with self.as_editable():
            # Delete the entire state
            # From: First line, first character
            #   To: End
            self.delete('1.0', 'end')
            # Reset styles
            self.style_reset()
            # Add the current state
            # TODO: Save the TextElement somewhere in this object, with `data`?
            for te in parser.parse_LTML(vs):
                assert isinstance(te, model.TextElement)
                self.insert(tk.END, te.text, te.atags)

    def get_gui_state(self) -> model.GuiState:
        ''''''  # Do not document
        if __debug__:
            logger.debug('State > %r', self.__gstate)
        # return a copy of the object
        return model.GuiState(**dict(self.__gstate.items()))

    def set_gui_state(self, state: typing.Optional[model.GuiState] = None, *, _internal: bool = False, **kwargs) -> None:
        ''''''  # Do not document
        if state is None:
            state = model.GuiState(**kwargs)
        if __debug__:
            logger.debug('State < %r', state)
        # Adjust current state
        for sname, svalue in state.items():
            assert sname != '_internal'  # Should be impossible...
            if svalue is not None:
                if sname == 'readonly' and _internal is False:
                    raise ValueError(f'{self}: No support for external readonly state manipulation')
                setattr(self.__gstate, sname, svalue)
        # Adjust widget state
        cfg = {}
        if self.__gstate.enabled is True:
            if self.__gstate.readonly is not None:
                cfg['state'] = tk.NORMAL if not self.__gstate.readonly else tk.DISABLED
            cfg['background'] = 'white'
        elif self.__gstate.enabled is False:
            cfg['state'] = tk.DISABLED
            cfg['background'] = 'lightgrey'
            self.style_reset()
        # if __debug__:
        #     logger.debug('C %s', self.__gstate)
        #     logger.debug('| %s', cfg)
        self.configure(**cfg)
        # Valid: TBD

    @contextmanager
    def as_editable(self):
        '''Temporarily mark the widget as editable.

        A context manager, used to change the contents of the widget while keep
        it "readonly".
        Technically, this should only be used internally, using the state
        tracker functions, but it might be useful externally.

        This is to be used like this:

        .. code:: python

            # `widget` is readonly
            with widget.as_editable():
                pass  # `widget` is editable
            # `widget` is readonly
        '''
        assert self.__gstate.readonly is True
        self.set_gui_state(readonly=False, _internal=True)
        try:
            yield
        finally:
            self.set_gui_state(readonly=True, _internal=True)

    def _style_a(self, tag: str = 'a', *, visited: bool) -> None:
        # TODO: Configure using "style"
        fg = 'purple' if visited else 'blue'
        self.tag_configure(tag, foreground=fg, underline=True)

    def style_reset(self, event=None, *, a: bool = True) -> None:
        '''Reset the style to the original.'''
        for tag in self.tag_names():
            # a
            if a and tag == 'a' or tag.startswith('a::'):
                self._style_a(tag=tag, visited=False)

    def _onClickTag(self, event, *, tag_name: str = 'a'):
        if not self.__gstate.enabled:
            return  # Do nothing when disabled
        dobj = self.dump(f'@{event.x},{event.y}', text=True, tag=True)
        if __debug__:
            logger.debug('D: %r', dobj)
        dwhat = [dinner[0] for dinner in dobj]
        tags_cl = []  # Ignore the "sel" tag
        if 'tagon' in dwhat:
            # Click in the start of the tag
            tags_cl = [lst[1] for lst in dobj if lst[0] == 'tagon' and lst[1] != tk.SEL]
            # For nested tags, this might not be the same as the text method
        if len(tags_cl) == 0 and 'text' in dwhat:
            # Click in the middle of the tag
            click_location = [lst[2] for lst in dobj if lst[0] == 'text'][0]
            tp = self.tag_prevrange(tag_name, click_location)
            if __debug__:
                logger.debug(' | Text @ <%s', tp)
            tags_cl = [lst[1] for lst in self.dump(*tp, tag=True) if lst[1] != tk.SEL]
        if len(tags_cl) == 0:
            raise NotImplementedError
        if __debug__:
            logger.debug(' | Tags %s', tags_cl)
        assert len(tags_cl) == 2
        tagi, tag = tags_cl
        assert tag_name == tag, f'Wrong onClickTag: Requested[{tag_name}] != Found[{tag}]'
        assert tagi.startswith(tag), f'Wrong tag_index: {tag}[{tagi}]'
        if __debug__:
            logger.debug(f' = {tag}[{tagi}]')
        self._style_a(tag=tagi, visited=True)
        self.onClickTag(tag, tagi)

    def onClickTag(self, tag: str, tag_index: str) -> None:
        """Callback to be called when clicking ``a`` tags in this widget.

        Defaults to doing nothing.

        Available for subclass redefinition.
        """
        pass


class Notebook(ttk.Notebook, mixin.ContainerWidget):
    '''A tabbed interface to hold other containers.

    This is a tabbed interface to show several containers in the same space.

    The individual tabs must all be containers, there's no support for single
    widgets. Use a holder `FrameUnlabelled` to show a single widget for each
    tab.

    There is no Python documentation, see ``Tk`` `ttk.Notebook <https://www.tcl.tk/man/tcl/TkCmd/ttk_notebook.html>`_ documentation.

    Args:
        layout: Ignored, it is hardcoded to `None` always.
        traversal: Setup tab traversal with special keyboard shortcuts, and
            also with mouse wheel scrolling. See the Tk documentation for the
            keyboard part. Enabled by default.
        traversalWraparound: When ``traversal`` is setup, configure wraparound.
            That is, scrolling to the next tab from the last one should "scroll"
            into the first tab, and vice-versa for the first tab.
            This only matters for the mouse wheel traversal.
            Disabled by default.

    See Also:
        `NotebookUniform`: A simpler version of this, when each individual tab is the same type
    '''
    Tab = model.NotebookTab  # Alias the notebook tab information  # TODO: Move NotebookTab class here?
    '''Alias for `model.NotebookTab` class.'''
    wtabs: typing.Mapping[str, model.NotebookTab]
    '''Mapping of tab identifiers, and `model.NotebookTab` objects.'''

    def __init__(self, parent, *args, layout=None, traversal: bool = True, traversalWraparound: bool = False, **kwargs):
        super().__init__(parent)
        # No `layout` is used, force it to `None`
        self.init_container(*args, layout=None, **kwargs)
        # Tab Traversal
        self.tWraparound = traversalWraparound
        if traversal:
            self.enable_traversal()
            # Bind mouse wheel: Digital Scrolling
            self._traversal = fn.bind_mousewheel(self, up=self._tabScrollUp, down=self._tabScrollDown, immediate=True)

    def setup_widgets(self, *args, **kwargs):
        '''Define the sub widgets based on the tabs.

        Do not overwrite this unless you know what you are doing.

        To edit the tabs, see `setup_tabs`.
        '''
        self.wtabs = self.setup_tabs(*args, **kwargs)
        if __debug__:
            logger.debug(f'{self}: {len(self.wtabs)} Tabs')
        widgets = {}
        for identifier, ti in self.wtabs.items():
            if __debug__:
                logger.debug('> %s: %r', ti.name, ti.widget)
            assert isinstance(ti.widget, mixin.ContainerWidget), f'{self!r}: Tab Widget [{ti.identifier or identifier}]"{ti.name}" must be a container'
            extra = {
                **ti.extra,
                'image': ti.image or '',
                'compound': ti.imageCompound,
            }
            self.add(ti.widget, text=ti.name, **extra)
            ti.identifier = identifier
            widgets[identifier] = ti.widget
        return widgets

    def setup_tabs(self, *args, **kwargs) -> typing.Mapping[str, model.NotebookTab]:
        '''Define the tabs here.

        Similar to `setup_widgets <mixin.ContainerWidget.setup_widgets>`, but
        defines `model.NotebookTab`, extra information about each widget.
        '''
        raise NotImplementedError

    def selection(self) -> typing.Optional[str]:
        '''Search for the current selected tab.

        This functions searches for the currently selected tab, and returns its
        identifier (the key on the `wtabs` dictionary).
        '''
        # TODO: Optimise this?
        selected_id = self.select()
        if __debug__:
            logger.debug('S: %r', selected_id)
            tabs_id = [str(w) for w in self.tabs()]
            logger.debug(' | %s', ' '.join(tabs_id))
        for idx, wtab in self.wtabs.items():
            if str(wtab.widget) == selected_id:
                return idx
        return None

    def selection_set(self, idx: str):
        '''Select a tab by identifier.'''
        wtab = self.wtabs.get(idx, None)
        assert wtab is not None, f'Invalid Selection: {idx}'
        return self.select(tab_id=str(wtab.widget))

    def _tabScrollUp(self, event=None):
        keys = list(self.wtabs.keys())
        selected = self.selection()
        if selected == keys[0]:
            # First Tab
            if self.tWraparound:
                new_selected = keys[-1]
            else:
                new_selected = None
        else:
            selected_idx = keys.index(selected)
            new_selected = keys[selected_idx - 1]
        if new_selected:
            self.selection_set(new_selected)

    def _tabScrollDown(self, event=None):
        keys = list(self.wtabs.keys())
        selected = self.selection()
        if selected == keys[-1]:
            # Last Tab
            if self.tWraparound:
                new_selected = keys[0]
            else:
                new_selected = None
        else:
            selected_idx = keys.index(selected)
            new_selected = keys[selected_idx + 1]
        if new_selected:
            self.selection_set(new_selected)


class NotebookUniform(Notebook):
    '''A tabbed interface to hold a series of uniform containers.

    This is a variant of the regular `Notebook` specially created to simplify
    the usual case where all the tabs are very similar (usually, they are the
    same underlying class).

    Args:
        tabids: A mapping of tab identifiers and tab titles.

    See Also:
        `Notebook`: A fully generic version of this. Don't try to make the
        `setup_tab` function too complex, move to this widget instead.
    '''
    tabids: typing.Optional[typing.Mapping[str, str]] = None

    def __init__(self, *args, tabids: typing.Optional[typing.Mapping[str, str]] = None, **kwargs):
        self.tabids = self.tabids or tabids
        if self.tabids is None:
            raise ValueError('{self!r}: Missing required tabids')
        super().__init__(*args, **kwargs)

    def setup_tabs(self, *args, **kwargs) -> typing.Mapping[str, model.NotebookTab]:
        '''Define the sub tabs, based on the common tab.

        Do not overwrite this unless you know what you are doing.

        To edit the common tab, see `setup_tab`.
        '''
        assert self.tabids is not None
        tabs = {}
        for tid, tname in self.tabids.items():
            tabs[tid] = Notebook.Tab(tname,
                                     self.setup_tab(tid, tname),
                                     *args, **kwargs)
        return tabs

    def setup_tab(self, identifier: str, name: str) -> mixin.ContainerWidget:
        '''Define the common tab `ContainerWidget` here.

        Similar to `setup_tabs <Notebook.setup_tabs>`, but for a single tab widget.
        '''
        raise NotImplementedError


class Tree(ttk.Treeview, mixin.SingleWidget):
    '''A hierarchical multicolumn data display widget.

    This widget is capable of showing a hierarchy of data records (one per
    row). Each record can have multiple columns of data.

    See `Python ttk.Treeview <tkinter.ttk.Treeview>` and ``Tk``
    `ttk.Treeview <https://tcl.tk/man/tcl8.6/TkCmd/ttk_treeview.htm>`_
    documentation.

    Args:
        parent: The parent widget. Can be a `RootWindow` or another `mixin.ContainerWidget`.
        variable: Use an externally defined variable, instead of creating a new
            one specific for this widget.

        label: The heading text for the first column, which includes the labels.
        columns: Mapping between column identifiers and its titles. Supports
            also a direct map between identifier and `model.TreeColumn`.
        expand: Grow the widget to match the container grid size. This is
            usually supported for containers, but it is included here.
        style_altbg: Configure a primitive version of alternating colors for
            the record background. Uses a single color for odd records, the others
            remain with the default colors. It's not ready for prime time, defaults
            to disabled.

    See Also:
        `Listbox`: Simplified version of this
    '''
    Element = model.TreeElement  # Alias the tree element information  # TODO: Move TreeElement class here?
    state_type = varTree

    wcolumns: typing.Mapping[str, model.TreeColumn]

    def __init__(self, parent, *, variable: typing.Optional[varTree] = None,
                 label: typing.Optional[str],
                 columns: typing.Mapping[str, typing.Union[model.TreeColumn, str]],
                 expand: bool = True, style_altbg: bool = False,
                 **kwargs):
        # Setup widget columns
        wcolumns = {}
        for cid, cobj in columns.items():
            if isinstance(cobj, model.TreeColumn):
                ccol = cobj
            elif isinstance(cobj, str):
                ccol = model.TreeColumn(cid, name=cobj)
            else:
                raise ValueError(f'{self!r}: Invalid column "{cid}": {cobj!r}')
            wcolumns[cid] = ccol
        self.wcolumns = wcolumns
        # Initialise Variable
        self.init_single(variable)
        kwargs.update({
            'selectmode': tk.NONE,  # No selection
            'columns': list(self.wcolumns.keys()),
        })
        super().__init__(parent, **kwargs)
        # Appearance
        if expand:
            self.grid(sticky=tk.NSEW)
        self._style_altbg = style_altbg
        # # Headers
        if label is not None:
            self.heading('#0', text=label)
        for wcol in self.wcolumns.values():
            self.heading(wcol.identifier, text=wcol.name)
        # # Alternate Backgrounds
        # TODO: Support recalculation when something is open/closed
        if self._style_altbg:  # TODO: Configure using "style", default to True
            self.tag_configure('__:lines-alt', background='lightgray')
        # Trace variable state
        self.trace(self.__tree_set, trace_name=f'__:{__name__}')

    def __tree_ls(self, parent: typing.Optional[str] = None, *, _lst: typing.Optional[typing.MutableSequence[model.TreeElement]] = None):
        '''List all widget ids, in linear order.'''
        # TODO: Convert to generator
        _lst = _lst or []
        assert _lst is not None
        for wtop in self.get_children(item=parent):
            _lst.append(wtop)
            self.__tree_ls(parent=wtop, _lst=_lst)
        return _lst

    def __tree_clean(self, parent=None) -> None:
        lst: typing.Sequence[model.TreeElement] = self.__tree_ls(parent=parent)
        self.delete(*lst)

    def __tree_put(self, elements: typing.Sequence[model.TreeElement], *,
                   parent: typing.Optional[str] = None,
                   openlevel: int = 1, _level: int = 0):
        parent_loc = tk.END if parent is None else self.index(parent)
        for eid, element in enumerate(elements):
            if __debug__:
                tpl_text = f'{parent or "__top__"}::#{eid}'
                logger.debug(f'{">" * (_level + 1)} {tpl_text}: L:"{element.label}" C:|{" ".join(element.columns)}|')
            assert len(element.columns) == len(self.wcolumns), f'Invalid Columns Size: E{len(element.columns)} W{len(self.wcolumns)}'
            cid = self.insert(parent or '', parent_loc,
                              text=element.label, values=element.columns,
                              open=_level < openlevel,
                              )
            if __debug__:
                logger.debug(f'{"|" * (_level + 1)} ID: {cid}')
            if element.children:
                if __debug__:
                    logger.debug(f'{"|" * (_level + 1)} Children: {len(element.children)}')
                self.__tree_put(element.children,
                                parent=cid,
                                openlevel=openlevel, _level=_level + 1)

    def __tree_set(self, *args, **kwargs):
        value = self.variable.get()
        self.__tree_clean()
        self.__tree_put(value)
        if self._style_altbg:
            # TODO: Support tracking the open/closed states
            for cnt, rid in enumerate(self.__tree_ls()):
                if cnt % 2 == 0:
                    tags = set(self.item(rid, option='tags'))
                    tags.add('__:lines-alt')
                    self.item(rid, tags=list(tags))
