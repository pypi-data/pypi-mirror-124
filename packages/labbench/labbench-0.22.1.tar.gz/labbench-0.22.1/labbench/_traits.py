# This software was developed by employees of the National Institute of
# Standards and Technology (NIST), an agency of the Federal Government.
# Pursuant to title 17 United States Code Section 105, works of NIST employees
# are not subject to copyright protection in the United States and are
# considered to be in the public domain. Permission to freely use, copy,
# modify, and distribute this software and its documentation without fee is
# hereby granted, provided that this notice and disclaimer of warranty appears
# in all copies.
#
# THE SOFTWARE IS PROVIDED 'AS IS' WITHOUT ANY WARRANTY OF ANY KIND, EITHER
# EXPRESSED, IMPLIED, OR STATUTORY, INCLUDING, BUT NOT LIMITED TO, ANY WARRANTY
# THAT THE SOFTWARE WILL CONFORM TO SPECIFICATIONS, ANY IMPLIED WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND FREEDOM FROM
# INFRINGEMENT, AND ANY WARRANTY THAT THE DOCUMENTATION WILL CONFORM TO THE
# SOFTWARE, OR ANY WARRANTY THAT THE SOFTWARE WILL BE ERROR FREE. IN NO EVENT
# SHALL NIST BE LIABLE FOR ANY DAMAGES, INCLUDING, BUT NOT LIMITED TO, DIRECT,
# INDIRECT, SPECIAL OR CONSEQUENTIAL DAMAGES, ARISING OUT OF, RESULTING FROM,
# OR IN ANY WAY CONNECTED WITH THIS SOFTWARE, WHETHER OR NOT BASED UPON
# WARRANTY, CONTRACT, TORT, OR OTHERWISE, WHETHER OR NOT INJURY WAS SUSTAINED
# BY PERSONS OR PROPERTY OR OTHERWISE, AND WHETHER OR NOT LOSS WAS SUSTAINED
# FROM, OR AROSE OUT OF THE RESULTS OF, OR USE OF, THE SOFTWARE OR SERVICES
# PROVIDED HEREUNDER. Distributions of NIST software should also include
# copyright and licensing statements of any third-party software that are
# legally bundled with the code in compliance with the conditions of those
# licenses.
"""
This implementation is deeply intertwined obscure details of the python object
model. Consider starting with a close read of the documentation and exploring
the objects in an interpreter instead of reverse-engineering this code.
"""

from . import util

import typing
from warnings import warn
from functools import wraps
import validators as _val
from contextlib import contextmanager

from inspect import isclass
import inspect
import numbers
import re

# for common types
from pathlib import Path
import numpy as np
import pandas as pd

Undefined = inspect.Parameter.empty

T = typing.TypeVar("T")


class ThisType(typing.Generic[T]):
    pass


class HasTraitsMeta(type):
    __cls_namespace__ = []

    @classmethod
    def __prepare__(cls, names, bases, **kws):
        """Prepare copies of cls._traits, to ensure that any traits defined
        in the definition don't clobber parents' traits.
        """
        ns = dict()
        if len(bases) >= 1:
            if hasattr(bases, "__children__"):
                ns["__children__"] = {}
            traits = {k: v.copy() for k, v in bases[0]._traits.items()}
            ns.update(traits)
            ns["_traits"] = traits
            HasTraitsMeta.__cls_namespace__.append(traits)
            return ns
        else:
            HasTraitsMeta.__cls_namespace__.append({})
            return dict(_traits=HasTraitsMeta.__cls_namespace__[-1])


class Trait:
    """implement typing checking, casting, decorators, and callback
    features in Device classes. These help reduce code errors that
    result from "copy and paste" boilerplate, and help to clarify
    the intent of the code.

    A Device instance supports two types of Traits:

    * A _value trait_ acts as an attribute variable in instantiated
      classes

    * A _property trait_ exposes set and get operations for a
      parameter in the API wrapped by the owning Device class.

    The trait behavior is determined by whether its owner is a Device or HasSettings
    instance.

    Arguments:
        default: the default value of the trait (value traits only)
        key: some types of Device take this input to determine automation behavior

        help: the Trait docstring
        label: a label for the quantity, such as units

    Arguments:
        sets: True if the trait supports writes
        gets: True if the trait supports reads

        cache: if True, interact with the device only once, then return copies (state traits only)
        only: value allowlist; others raise ValueError

    Arguments:
        allow_none: permit None values in addition to the specified type
        remap: a lookup table that maps the python type (keys) to a potentially different backend values (values) ,
                  in places of the to_pythonic and from_pythonic methods (property traits only)

    """

    ROLE_VALUE = "value"
    ROLE_PROPERTY = "property"
    ROLE_DATARETURN = "return"
    ROLE_UNSET = "unset"

    type = None
    role = ROLE_UNSET

    # keyword argument types and default values
    default: ThisType = Undefined
    key: Undefined = Undefined
    func: typing.Callable = None
    # role: str = ROLE_UNSET
    help: str = ""
    label: str = ""
    sets: bool = True
    gets: bool = True
    cache: bool = False
    only: tuple = tuple()
    allow_none: bool = False
    remap: dict = {}

    # If the trait is used for a state, it can operate as a decorator to
    # implement communication with a device
    _setter = None
    _getter = None
    _returner = None
    _decorated_funcs = []

    # __decorator_action__ = None

    def __init__(self, *args, **kws):
        if len(args) >= 1:
            if len(args) == 1 and self.role == self.ROLE_VALUE:
                if "default" in kws:
                    raise ValueError(f"duplicate 'default' argument in {self}")
                kws["default"] = args[0]
            elif len(args) == 1 and self.role == self.ROLE_DATARETURN:
                if "func" in kws:
                    raise ValueError("duplicate 'func' argument")
                kws["func"] = args[0]
            else:
                raise ValueError(f"no positional arguments supported")

        self.kws = dict(kws)
        self.metadata = {}
        self._decorated_funcs = []

        cls_defaults = {k: getattr(self, k) for k in self.__annotations__.keys()}

        if "default" in cls_defaults:
            cls_defaults["default"] = Undefined

        kws = dict(cls_defaults, **kws)

        # check role and related parameter dependencies
        if self.role == self.ROLE_VALUE:
            invalid_args = ("remap", "key", "func")
        elif self.role == self.ROLE_PROPERTY:
            invalid_args = ("default", "func")
        elif self.role == self.ROLE_DATARETURN:
            invalid_args = "default", "key", "sets", "gets"
        else:
            clsname = self.__class__.__qualname__
            raise ValueError(
                f"{clsname}.role must be one of {(self.ROLE_PROPERTY, self.ROLE_DATARETURN, self.ROLE_VALUE)}, not {repr(self.role)}"
            )

        for k in invalid_args:
            if k in cls_defaults and cls_defaults[k] != kws[k]:
                raise AttributeError(
                    f"keyword argument '{k}' is not allowed with {self.role}"
                )

        if self.role == self.ROLE_VALUE and kws["default"] is Undefined:
            # always go with None when this value is allowed, fallback to self.default
            kws["default"] = self.type()

        if self.role == self.ROLE_DATARETURN:
            if kws["func"] is not None:
                # apply a decorator
                self(kws["func"])

        if self.role in (self.ROLE_DATARETURN, self.ROLE_PROPERTY):
            # default Undefined so that cache will fill them in
            self.default = Undefined

        # Replace self.from_pythonic and self.to_pythonic with lookups in self.remap (if defined)
        if len(kws["remap"]) > 0:
            self.remap_inbound = {v: k for k, v in kws["remap"].items()}
        else:
            self.remap_inbound = {}

        if len(kws["remap"]) != len(self.remap_inbound):
            raise ValueError(f"'remap' has duplicate values")

        # set value traits
        for k, v in kws.items():
            setattr(self, k, v)

    @classmethod
    def __init_subclass__(cls, type=Undefined):
        """python triggers this call immediately after a Trait subclass
            is defined, allowing us to automatically customize its implementation.

        Arguments:
            type: the python type represented by the trait
        """
        if type is not Undefined:
            cls.type = type

        # complete the annotation dictionary with the parent
        annots = dict(
            getattr(cls.__mro__[1], "__annotations__", {}),
            **getattr(cls, "__annotations__", {}),
        )

        cls.__annotations__ = dict(annots)

        # # apply an explicit signature to cls.__init__
        # annots = {k: cls.type if v is ThisType else (k, v) \
        #           for k, v in annots.items()}

        # cls._arg_defaults = {k: getattr(cls, k)
        #                     for k in annots if hasattr(cls, k)}

        # if 'default' in cls._arg_defaults:
        #     cls._arg_defaults['default'] = Undefined

        # TODO: remove this
        # util.wrap_attribute(cls, '__init__', __init__, tuple(annots.keys()), cls._arg_defaults, 1, annots)

        # Help to reduce memory use by __slots__ definition (instead of __dict__)
        cls.__slots__ = [n for n in dir(cls) if not n.startswith("_")] + [
            "metadata",
            "kind",
            "name",
        ]

    def copy(self, new_type=None, **update_kws):
        if new_type is None:
            new_type = type(self)
        obj = new_type(**dict(self.kws, **update_kws))
        obj._getter = self._getter
        obj._setter = self._setter
        obj._returner = self._returner
        return obj

    ### Descriptor methods (called automatically by the owning class or instance)
    def __set_name__(self, owner_cls, name):
        """Immediately after an owner class is instantiated, it calls this
        method for each of its attributes that implements this method.

        Trait takes advantage of this to remember the owning class for debug
        messages and to register with the owner class.
        """
        if not issubclass(owner_cls, HasTraits):
            # otherwise, other objects that house this Trait may unintentionally become owners
            return

        # inspect module expects this name - don't play with it
        self.__objclass__ = owner_cls

        # Take the given name, unless we've bene tagged with a different
        self.name = name

        if issubclass(owner_cls, HasTraits):
            owner_cls._traits[name] = self

    def __init_owner_subclass__(self, owner_cls):
        """The owner calls this in each of its traits at the end of defining the subclass
        (near the end of __init_subclass__).
        has been called. Now it is time to ensure properties are compatible with the owner class.
        This is here --- not in __set_name__ --- because python
        obfuscates exceptions raised in __set_name__.

        This is also where we finalize selecting decorator behavior; is it a property or a method?
        """

        if self.role == self.ROLE_VALUE and len(self._decorated_funcs) > 0:
            raise AttributeError(
                f"tried to combine a default value and a decorator implementation in {self}"
            )
        elif self.role == self.ROLE_DATARETURN and len(self._decorated_funcs) == 0:
            raise AttributeError(f"decorate a method to tag its return data")
        elif len(self._decorated_funcs) == 0:
            return

        positional_argcounts = [
            f.__code__.co_argcount - len(f.__defaults__ or tuple())
            for f in self._decorated_funcs
        ]

        if self.role == self.ROLE_DATARETURN:
            for func, argcount in zip(self._decorated_funcs, positional_argcounts):
                if len(self.help.rstrip().strip()) == 0:
                    # take func docstring as default self.help
                    self.help = (func.__doc__ or "").rstrip().strip()

                self._returner = func

        elif self.role == self.ROLE_PROPERTY:
            if set(positional_argcounts) not in ({1}, {1, 2}, {2}):
                raise AttributeError(
                    f"a decorator implementation with @{self} must apply to a getter "
                    f"(above `def func(self)`) and/or setter (above `def func(self, value):`)"
                )
            for func, argcount in zip(self._decorated_funcs, positional_argcounts):
                doc = (func.__doc__ or "").strip().rstrip()
                if len(doc) > 0:
                    # take func docstring as default self.help
                    self.help = self.kws["help"] = doc

                if argcount == 1:
                    self._getter = func
                else:
                    self._setter = func

    def __init_owner_instance__(self, owner):
        # called by owner.__init__
        pass

    @util.hide_in_traceback
    def __set__(self, owner, value):
        # First, validate the pythonic types
        if not self.sets:
            raise AttributeError(f"{self.__str__()} cannot be set")

        # Validate the pythonic value
        if value is not None:
            # cast to self.type and validate
            value = Trait.to_pythonic(self, value)
            value = self.validate(value, owner)

            if len(self.only) > 0 and not self.contains(self.only, value):
                raise ValueError(
                    f"value '{value}' is not among the allowed values {repr(self.only)}"
                )
        elif self.allow_none:
            value = None
        else:
            raise ValueError(f"None value not allowed for trait '{repr(self)}'")

        try:
            value = self.from_pythonic(value)
        except BaseException as e:
            name = owner.__class__.__qualname__ + "." + self.name
            e.args = (e.args[0] + f" in attempt to set '{name}'",) + e.args[1:]
            raise e

        if self.role == self.ROLE_VALUE:
            # apply as a value trait
            owner.__set_value__(self.name, value)

        elif self.role == self.ROLE_PROPERTY:
            # convert to the outbound representation
            if len(self.remap) > 0:
                value = self.remap.get(value, value)

            # send to the device
            if self._setter is not None:
                # from the function decorated by this trait
                self._setter(owner, value)

            elif self.key is not None:
                # otherwise, use the owner's set_key
                owner.set_key(self.key, value, self.name)

            else:
                objname = owner.__class__.__qualname__ + "." + self.name
                raise AttributeError(
                    f"cannot set {objname}: no @{self.__repr__(owner_inst=owner)}."
                    f"setter and no key argument"
                )

        else:
            raise AttributeError(f"data return traits cannot be set")

        owner.__notify__(self.name, value, "set", cache=self.cache)

    @util.hide_in_traceback
    def __get__(self, owner, owner_cls=None):
        """Called by the class instance that owns this attribute to
        retreive its value. This, in turn, decides whether to call a wrapped
        decorator function or the owner's get_key method to retrieve
        the result.

        Returns:
            retreived value
        """

        # only continue to get the value if the __get__ was called for an owning
        # instance, and owning class is a match for what we were told in __set_name__.
        # otherwise, someone else is trying to access `self` and we
        # shouldn't get in their way.
        if owner is None or owner_cls.__dict__.get(
            self.name, None
        ) is not self.__objclass__.__dict__.get(self.name):
            # the .__dict__.get acrobatics avoids a recursive __get__ loop
            return self

        elif self.role == self.ROLE_DATARETURN:
            # inject the labbench Trait hooks into the return value
            @wraps(self._returner)
            def method(*args, **kws):
                value = self._returner(owner, *args, **kws)
                return self.__cast_get__(owner, value)

            return method

        elif not self.gets:
            # stop now if this is not a gets Trait
            raise AttributeError(f"{self.__repr__(owner_inst=owner)} is not gets")

        elif self.role == self.ROLE_VALUE:
            return owner.__get_value__(self.name)

        # from here on, operate as a property getter
        if self.cache and self.name in owner.__cache__:
            # return the cached value if applicable
            return owner.__cache__[self.name]

        elif self._getter is not None:
            # get value with the decorator implementation, if available
            value = self._getter(owner)

        else:
            # otherwise, get with owner.get_key, if available
            if self.key is None:
                # otherwise, 'get'
                objname = owner.__class__.__qualname__
                ownername = self.__repr__(owner_inst=owner)
                raise AttributeError(
                    f"to set the property {self.name}, decorate a method in {objname} or use the function key argument"
                )
            value = owner.get_key(self.key, self.name)

        # apply remapping as appropriate for the trait
        if len(self.remap_inbound) > 0:
            value = self.remap_inbound.get(value, value)

        return self.__cast_get__(owner, value, strict=False)

    @util.hide_in_traceback
    def __cast_get__(self, owner, value, strict=False):
        """Examine value and either return a valid pythonic value or raise an exception if it cannot be cast.

        Arguments:
            owner: the class that owns the trait
            value: the value we need to validate and notify
        :return:
        """
        if self.allow_none and value is None:
            pass
        else:
            # skip validation if None and None values are allowed
            try:
                value = self.to_pythonic(value)
            except BaseException as e:
                # name = owner.__class__.__qualname__ + '.' + self.name
                e.args = (
                    e.args[0]
                    + f" in attempt to get '{self.__repr__(owner_inst=owner)}'",
                ) + e.args[1:]
                raise e

            # Once we have a python value, give warnings (not errors) if the device value fails further validation
            if hasattr(owner, "_logger"):
                log = owner._logger.warning
            else:
                log = warn

            # TODO: This broke array-like data. Was it ever necessary?
            # if value != self.validate(value, owner):
            #     raise ValueError
            # except ValueError:
            #     log(f"'{self.__repr__(owner_inst=owner)}' {self.role} received the value {repr(value)}, " \
            #         f"which fails {repr(self)}.validate()")
            if value is None and not self.allow_none:
                log(
                    f"'{self.__repr__(owner_inst=owner)}' {self.role} received value None, which"
                    f"is not allowed for {repr(self)}"
                )
            if len(self.only) > 0 and not self.contains(self.only, value):
                log(
                    f"'{self.__repr__(owner_inst=owner)}' {self.role} received {repr(value)}, which"
                    f"is not in the valid value list {repr(self.only)}"
                )

        owner.__notify__(
            self.name, value, "get", cache=self.cache or (self.role == self.ROLE_VALUE)
        )

        return value

    @util.hide_in_traceback
    def to_pythonic(self, value):
        """Convert a value from an unknown type to self.type."""
        return self.type(value)

    @util.hide_in_traceback
    def from_pythonic(self, value):
        """convert from a python type representation to the format needed to communicate with the device"""
        return value

    @util.hide_in_traceback
    def validate(self, value, owner=None):
        """This is the default validator, which requires that trait values have the same type as self.type.
            A ValueError is raised for other types.
            value: value to check
        Returns:
            a valid value
        """
        if not isinstance(value, self.type):
            typename = self.type.__qualname__
            valuetypename = type(value).__qualname__
            raise ValueError(
                f"{repr(self)} type must be '{typename}', not '{valuetypename}'"
            )
        return value

    def contains(self, iterable, value):
        return value in iterable

    ### Decorator methods
    @util.hide_in_traceback
    def __call__(self, func):
        """use the Trait as a decorator, which ties this Trait instance to evaluate a property or method in the
        owning class. you can specify
        """
        # only decorate functions.
        if not callable(func):
            raise Exception(
                f"object of type '{func.__class__.__qualname__}' must be callable"
            )

        self._decorated_funcs.append(func)

        # Register in the list of decorators, in case we are overwritten by an
        # overloading function
        if getattr(self, "name", None) is None:
            self.name = func.__name__
        if len(HasTraitsMeta.__cls_namespace__) > 0:
            HasTraitsMeta.__cls_namespace__[-1][func.__name__] = self

        # return self to ensure `self` is the value assigned in the class definition
        return self

    ### introspection
    ###
    def doc(self):
        params = self.doc_params(omit=["help", "default"])
        typename = "Any" if self.type is None else self.type.__qualname__

        doc = f"{self.name} ({typename}): {self.help}"
        if len(params) > 0:
            doc += f" ({params})"

        return doc

    def doc_params(self, omit=["help"]):
        pairs = []

        for name in self.__annotations__.keys():
            default = getattr(type(self), name)
            v = getattr(self, name)

            # skip uninformative debug info
            if name.startswith("_") or name in omit:
                continue

            # only show non-defaults
            v = getattr(self, name)
            if v == default:
                continue

            pairs.append(f"{name}={repr(v)}")

        return ",".join(pairs)

    def __repr__(self, omit=["help"], owner_inst=None):
        declaration = f"{self.role}.{type(self).__qualname__}({self.doc_params(omit)})"

        if owner_inst is None:
            return declaration
        else:
            return f"<{declaration} as {owner_inst}.{self.name}>"

    __str__ = __repr__

    def _owned_name(self, owner):
        if owner._owned_name is None:
            return type(owner).__qualname__ + "." + self.name
        else:
            return owner._owned_name + "." + self.name


Trait.__init_subclass__()


class HasTraits(metaclass=HasTraitsMeta):
    __notify_list__ = {}
    __cls_namespace__ = {}

    def __init__(self, **values):
        # who is informed on new get or set values
        self.__notify_list__ = {}

        # for cached properties and values in this instance
        self.__cache__ = {}
        self._calibrations = {}

        for name, trait in self._traits.items():
            trait.__init_owner_instance__(self)

            if trait.default is not Undefined:
                self.__cache__[name] = trait.default

    @util.hide_in_traceback
    def __init_subclass__(cls):
        cls._traits = dict(getattr(cls, "_traits", {}))
        cls._property_attrs = []
        cls._value_attrs = []
        cls._datareturn_attrs = []
        parent_traits = getattr(cls.__mro__[1], "_traits", {})

        # annotations = getattr(cls, '__annotations__', {})

        for name, trait in dict(cls._traits).items():
            # Apply the trait decorator to the object if it is "part 2" of a decorator
            obj = getattr(cls, name)

            if not isinstance(obj, Trait):
                if (
                    trait.role
                    in (
                        Trait.ROLE_PROPERTY,
                        Trait.ROLE_DATARETURN,
                    )
                    and callable(obj)
                ):
                    # if it's a method, decorate it
                    cls._traits[name] = trait(obj)
                else:
                    # if not decorating, clear from the traits dict, and emit a warning at runtime
                    thisclsname = cls.__qualname__
                    parentclsname = cls.__mro__[1].__qualname__
                    warn(
                        f"'{name}' in {thisclsname} is not a trait, but replaces one in parent class {parentclsname}"
                    )
                    del cls._traits[name]

                    continue

            setattr(cls, name, cls._traits[name])

        if cls._traits in HasTraitsMeta.__cls_namespace__:
            HasTraitsMeta.__cls_namespace__.remove(cls._traits)

        # finalize trait setup
        for name, trait in dict(cls._traits).items():
            if not hasattr(trait, "__objclass__"):
                trait.__set_name__(cls, name)
            trait.__init_owner_subclass__(cls)

            if trait.role == Trait.ROLE_VALUE:
                cls._value_attrs.append(name)
            elif trait.role == Trait.ROLE_DATARETURN:
                cls._datareturn_attrs.append(name)
            elif trait.role == Trait.ROLE_PROPERTY:
                cls._property_attrs.append(name)

    # @contextmanager
    # def _hold_notifications(self, names=Undefined):
    #     """ pause notifications for the specified traits
    #         inside this context. names is a list of trait
    #         names, or Undefined (default) to pause all traits.
    #     """
    #     if names is Undefined:
    #         names = list(self._traits.keys())
    #     elif isinstance(names, str):
    #         names = [names]

    #     pre,self._holds=self._holds, names
    #     yield
    #     self._holds=pre

    @util.hide_in_traceback
    def __notify__(self, name, value, type, cache):
        old = self.__cache__.setdefault(name, Undefined)

        msg = dict(new=value, old=old, owner=self, name=name, type=type, cache=cache)

        for handler in self.__notify_list__.values():
            handler(dict(msg))

        self.__cache__[name] = value

    def set_key(self, key, value, name=None):
        """implement this in subclasses to use `key` to set a parameter value from the
        Device with self.backend.

        property traits defined with "key=" call this to set values
        in the backend.
        """

        clsname = self.__class__.__qualname__
        raise NotImplementedError(
            f"implement {clsname}.get_key for access to key/value parameters on the device"
        )

    def get_key(self, key, name=None):
        """implement this in subclasses to use `key` to retreive a parameter value from the
        Device with self.backend.

        property traits defined with "key=" call this to retrieve values
        from the backend.
        """
        clsname = self.__class__.__qualname__
        raise NotImplementedError(
            f"implement {clsname}.get_key for access key/value parameters on the device"
        )

    @util.hide_in_traceback
    def __get_value__(self, name):
        """Get value of a trait for this value traits instance

        Arguments:
            name: Name of the trait
        Returns:
            cached value, or the trait default if it has not yet been set
        """
        return self.__cache__[name]

    @util.hide_in_traceback
    def __set_value__(self, name, value):
        """Set value of a trait for this value traits instance

        Arguments:
            name: Name of the trait
            value: value to assign
        Returns:
            None
        """
        # assignment to to self.__cache__ here would corrupt 'old' message key in __notify__
        pass


class Any(Trait, type=None):
    """allows any value"""

    @util.hide_in_traceback
    def validate(self, value, owner=None):
        return value

    @util.hide_in_traceback
    def to_pythonic(self, value):
        return value


Trait.__annotations__["key"] = Any


def observe(obj, handler, name=Any, type_=("get", "set")):
    """Register a handler function to be called whenever a trait changes.

    The handler function takes a single message argument. This
    dictionary message has the keys

    * `new`: the updated value
    * `old`: the previous value
    * `owner`: the object that owns the trait
    * `name`: the name of the trait
    * 'event': 'set' or 'get'

    Arguments:
        handler: the handler function to call when the value changes
        names: notify only changes to these trait names (None to disable filtering)
    """

    if not callable(handler):
        raise ValueError(
            f"argument 'handler' is {repr(handler)}, which is not a callable"
        )

    if isinstance(name, str):
        name = (name,)

    if isinstance(type, str):
        type_ = (type_,)

    def wrapped(msg):
        # filter according to name and type
        if name is not Any and msg["name"] not in name:
            return
        elif msg["type"] not in type_:
            return
        handler(msg)

    if isinstance(obj, HasTraits):
        obj.__notify_list__[handler] = wrapped
    else:
        raise TypeError("object to observe must be an instance of Device")


def unobserve(obj, handler):
    """Unregister a handler function from notifications in obj."""
    if isinstance(obj, HasTraits):
        try:
            del obj.__notify_list__[handler]
        except KeyError as e:
            ex = e
        else:
            ex = None
        if ex:
            raise ValueError(f"{handler} was not registered to observe {obj}")
    else:
        raise TypeError("object to unobserve must be an instance of Device")


class LookupCorrectionMixIn(Trait):
    """act as another BoundedNumber trait calibrated with a lookup table"""

    table: Any = None  # really a pandas Series

    def _min(self, owner):
        by_cal, by_uncal = owner._calibrations.get(self.name, (None, None))
        if by_uncal is None:
            return None
        else:
            return by_uncal.min()

    def _max(self, owner):
        by_cal, by_uncal = owner._calibrations.get(self.name, (None, None))
        if by_uncal is None:
            return None
        else:
            return by_uncal.max()

    def __init_owner_instance__(self, owner):
        observe(owner, self.__owner_event__, name=self._other.name)

    def __owner_event__(self, msg):
        owner = msg["owner"]
        owner.__notify__(
            self.name,
            self.lookup_cal(msg["new"], owner),
            msg["type"],
            cache=msg["cache"],
        )

    def lookup_cal(self, uncal, owner):
        """return the index value that gives the attenuation level nearest to `proposal`"""
        by_cal, by_uncal = owner._calibrations.get(self.name, (None, None))
        if by_uncal is None:
            return None

        try:
            return by_uncal.loc[uncal]
        except KeyError:
            pass

        # this odd try-except...raise oddness spares us internal
        # pandas details in the traceback
        util.logger.warning(
            f"{self.__repr__(owner_inst=owner)} has no entry at {repr(uncal)} {self.label}"
        )
        return None

    def find_uncal(self, cal, owner):
        """look up the calibrated value for the given uncalibrated value. In the event of a lookup
        error, then if `self.allow_none` evaluates as True, triggers return of None, or if
         `self.allow_none` evaluates False, ValueError is raised.
        """
        by_cal, by_uncal = owner._calibrations.get(self.name, (None, None))
        if by_uncal is None:
            return None

        i = by_cal.index.get_loc(cal, method="nearest")
        return by_cal.iloc[i]

    def set_table(self, series_or_uncal, cal=None, owner=None):
        """set the lookup table as `set_table(series)`, where `series` is a pandas Series (uncalibrated
        values in the index), or `set_table(cal_vector, uncal_vector)`, where both vectors have 1
        dimension of the same length.
        """

        if owner is None:
            raise ValueError(f"must pass owner to set_table")

        import pandas as pd

        if isinstance(series_or_uncal, pd.Series):
            by_uncal = pd.Series(series_or_uncal).copy()
        elif cal is not None:
            by_uncal = pd.Series(cal, index=series_or_uncal)
        elif series_or_uncal is None:
            return
        else:
            raise ValueError(
                f"must call set_table with None, a Series, or a pair of vector "
                f"arguments, not {series_or_uncal}"
            )
        by_uncal = by_uncal.sort_index()
        by_uncal.index.name = "uncal"
        by_uncal.name = "cal"

        by_cal = pd.Series(by_uncal.index, index=by_uncal.values, name="uncal")
        by_cal = by_cal.sort_index()
        by_cal.index.name = "cal"

        owner._calibrations[self.name] = by_cal, by_uncal

    def __get__(self, owner, owner_cls=None):
        if owner is None or owner_cls is not self.__objclass__:
            return self

        by_cal, by_uncal = owner._calibrations.get(self.name, (None, None))
        if by_uncal is None:
            raise KeyError(
                f"load a correction table to use the corrected '{self.name}' {self.role}, "
                f"or use the uncorrected '{self._other.name}' {self._other.role}"
            )

        uncal = self._other.__get__(owner, owner_cls)
        cal = self.lookup_cal(uncal, owner)

        if cal is None:
            return uncal
        else:
            return cal

    def __set__(self, owner, cal):
        by_cal, by_uncal = owner._calibrations.get(self.name, (None, None))
        if by_uncal is None:
            raise KeyError(
                f"load a correction table to use the corrected '{self.name}' {self.role}, "
                f"or use the uncorrected '{self._other.name}' {self._other.role}"
            )

        # start with type conversion and validation on the requested calibrated value
        cal = self._other.to_pythonic(cal)

        # lookup the uncalibrated value that results in the nearest calibrated result
        uncal = self.find_uncal(cal, owner)

        if uncal is None:
            self._other.__set__(owner, cal)
        elif uncal != type(self._other).validate(self, uncal, owner):
            # raise an exception if the calibration table contains invalid
            # values, instead
            raise ValueError(
                f"calibration lookup in {self.__repr__(owner_inst=owner)} produced invalid value {repr(uncal)}"
            )
        else:
            # execute the set
            self._other.__set__(owner, uncal)


class OffsetCorrectionMixIn(Trait):
    """act as another BoundedNumber trait, calibrated with an additive offset"""

    offset_name: str = (
        None  # the name of a trait in owner that contains the offset value
    )

    def _min(self, owner):
        if None in (self._other._min(owner), owner._calibrations[self.name]):
            return None
        return self._other._min(owner) + owner._calibrations[self.name]

    def _max(self, owner):
        if None in (self._other._max(owner), owner._calibrations[self.name]):
            return None
        return self._other._max(owner) + owner._calibrations[self.name]

    def __init_owner_instance__(self, owner):
        self._last_value = None

        observe(owner, self.__other_update__, self._other.name)
        observe(owner, self.__offset_update__, name=self.offset_name)
        owner._calibrations[self.name] = getattr(owner, self.offset_name)

        # # get the current offset, and observe changes to the value to keep it
        # # up to date
        # if self.role == self.ROLE_PROPERTY:
        #     observe(owner., self.__offset_update__, name=self.offset_name)
        #     owner._calibrations[self.name] = getattr(owner., self.offset_name)
        # elif self.role == self.ROLE_VALUE:
        #     observe(owner, self.__offset_update__, name=self.offset_name)
        #     owner._calibrations[self.name] = getattr(owner, self.offset_name)
        # elif self.role == self.ROLE_UNSET:
        #     raise ValueError(f"{self.__repr__(owner_inst=owner)} is not attached to a device")
        # else:
        #     raise ValueError(f"unrecognized trait type '{self.role}'")

    def __offset_update__(self, msg):
        owner = msg["owner"]
        owner._calibrations[self.name] = msg["new"]

        if None in (self._last_value, owner._calibrations[self.name]):
            value = None
        else:
            value = self._last_value + owner._calibrations[self.name]

        owner.__notify__(self.name, value, msg["type"], cache=msg["cache"])

    def __other_update__(self, msg):
        owner = msg["owner"]
        value = self._last_value = msg["new"]

        if None in (value, owner._calibrations[self.name]):
            value = None
        else:
            value = value + owner._calibrations[self.name]

        owner.__notify__(self.name, value, msg["type"], cache=msg["cache"])

    def _offset_trait(self, owner):
        return owner._traits[self.offset_name]
        # if self.role == self.ROLE_PROPERTY:
        #     return owner.[self.offset_name]
        # else:
        #     return owner[self.offset_name]

    def __get__(self, owner, owner_cls=None):
        if owner is None or owner_cls is not self.__objclass__:
            return self

        if owner._calibrations[self.name] is None:
            offset_trait = self._offset_trait(owner)
            raise AttributeError(
                f"use the uncalibrated {self._other.__repr__(owner_inst=owner)}, or calibrate "
                f"{self.__repr__(owner_inst=owner)} first by setting {offset_trait}"
            )

        return self._other.__get__(owner, owner_cls) + owner._calibrations[self.name]

    def __set__(self, owner, value):
        if owner._calibrations[self.name] is None:
            offset_trait = self._offset_trait(owner)
            raise AttributeError(
                f"use the uncalibrated {self._other.__repr__(owner_inst=owner)}, or calibrate "
                f"{self.__repr__(owner_inst=owner)} first by setting {offset_trait}"
            )

        # use the other to the value into the proper format and validate it
        value = self._other.to_pythonic(value)
        type(self._other).validate(self, value, owner)

        self._other.__set__(owner, value - owner._calibrations[self.name])


class TransformMixIn(Trait):
    """act as an arbitrarily-defined (but reversible) transformation of another BoundedNumber trait"""

    _forward: Any = lambda x: x
    _reverse: Any = lambda x: x

    def __init_owner_instance__(self, owner):
        observe(owner, self.__owner_event__)

    def __owner_event__(self, msg):
        # pass on a corresponding notification when self._other changes
        if msg["name"] != self._other.name:
            return

        owner = msg["owner"]
        owner.__notify__(
            self.name, self._forward(msg["new"]), msg["type"], cache=msg["cache"]
        )

    def _min(self, owner):
        # TODO: ensure this works properly for any reversible self._forward()?
        if self._other._min(owner) is None:
            return None
        return min(
            self._forward(self._other._max(owner)),
            self._forward(self._other._min(owner)),
        )

    def _max(self, owner):
        # TODO: does this actually work for any reversible self._forward()?
        if self._other._max(owner) is None:
            return None
        return max(
            self._forward(self._other._max(owner)),
            self._forward(self._other._min(owner)),
        )

    def __get__(self, owner, owner_cls=None):
        if owner is None or owner_cls is not self.__objclass__:
            return self

        return self._forward(self._other.__get__(owner, owner_cls))

    def __set__(self, owner, value):
        # use the other to the value into the proper format and validate it
        value = self._other.to_pythonic(value)
        type(self._other).validate(self, value, owner)
        self._other.__set__(owner, self._reverse(value))


class BoundedNumber(Trait):
    """accepts numerical, str, or bytes values, following normal python casting procedures (with bounds checking)"""

    default: ThisType = None
    allow_none: bool = True
    min: ThisType = None
    max: ThisType = None

    @util.hide_in_traceback
    def validate(self, value, owner=None):
        if not isinstance(value, (bytes, str, bool, numbers.Number)):
            raise ValueError(
                f"a '{type(self).__qualname__}' trait value must be a numerical, str, or bytes instance"
            )

        # Check bounds once it's a numerical type
        min = self._min(owner)
        max = self._max(owner)

        if max is not None and value > max:
            raise ValueError(
                f"{value} is greater than the max limit {max} of {self._owned_name(owner)}"
            )
        if min is not None and value < min:
            raise ValueError(
                f"{value} is less than the min limit {min} of {self._owned_name(owner)}"
            )

        return value

    def _max(self, owner):
        """overload this to dynamically compute max"""
        return self.max

    def _min(self, owner):
        """overload this to dynamically compute max"""
        return self.min

    def calibrate(
        self,
        offset_name=Undefined,
        lookup=Undefined,
        help="",
        label=Undefined,
        allow_none=False,
    ):
        """generate a new Trait subclass that calibrates values given by
        another trait. their configuration comes from a trait in the owner.

        Arguments:
            offset_name: the name of a value trait in the owner containing a numerical offset
            lookup: a table containing calibration data, or None to configure later
        """

        params = {}
        if lookup is not Undefined:
            mixin = LookupCorrectionMixIn
            params["table"] = lookup

        elif offset_name is not Undefined:
            mixin = OffsetCorrectionMixIn
            params["offset_name"] = offset_name

        if label is Undefined:
            label = self.label

        if len(params) != 1:
            raise ValueError(f"must set exactly one of `offset` and `table`")

        name = self.__class__.__name__
        name = ("" if name.startswith("Dependent") else "Dependent") + name
        ttype = type(name, (mixin, type(self)), dict(_other=self))

        return ttype(
            help=help,
            label=self.label,
            sets=self.sets,
            gets=self.gets,
            allow_none=allow_none,
            **params,
        )

    def transform(self, forward, reverse, help="", allow_none=False):
        """generate a new Trait subclass that calibrates values given by
        another trait.

        Arguments:
            forward: a function that returns the transformed numerical value
        given the untransformed value
            reverse: a function that returns the untransformed numerical value
        given the transformed value.
        """

        name = self.__class__.__name__
        name = ("" if name.startswith("Dependent") else "Dependent") + name
        ttype = type(name, (TransformMixIn, type(self)), dict(_other=self))

        return ttype(
            help=help,
            label=self.label,
            sets=self.sets,
            gets=self.gets,
            allow_none=allow_none,
            _forward=forward,
            _reverse=reverse,
        )

    def __neg__(self):
        def neg(x):
            return None if x is None else -x

        return self.transform(
            neg, neg, allow_none=self.allow_none, help=f"-1*({self.help})"
        )

    def __add__(self, other):
        def add(x):
            return None if x is None else x + other

        def sub(x):
            return None if x is None else x - other

        return self.transform(
            add, sub, allow_none=self.allow_none, help=f"({self.help}) + {other}"
        )

    __radd__ = __add__

    def __sub__(self, other):
        def add(x):
            return None if x is None else x + other

        def sub(x):
            return None if x is None else x - other

        return self.transform(
            sub, add, allow_none=self.allow_none, help=f"({self.help}) + {other}"
        )

    def __rsub__(self, other):
        def add(x):
            return None if x is None else other + x

        def sub(x):
            return None if x is None else other - x

        return self.transform(
            sub, add, allow_none=self.allow_none, help=f"({self.help}) + {other}"
        )

    def __mul__(self, other):
        def mul(x):
            return None if x is None else x * other

        def div(x):
            return None if x is None else x / other

        return self.transform(
            mul, div, allow_none=self.allow_none, help=f"({self.help}) + {other}"
        )

    __rmul__ = __mul__

    def __truediv__(self, other):
        def mul(x):
            return None if x is None else x * other

        def div(x):
            return None if x is None else x / other

        return self.transform(
            div, mul, allow_none=self.allow_none, help=f"({self.help}) + {other}"
        )

    def __rdiv__(self, other):
        def mul(x):
            return None if x is None else other * x

        def div(x):
            return None if x is None else other / x

        return self.transform(
            div, mul, allow_none=self.allow_none, help=f"({self.help}) + {other}"
        )


class NonScalar(Any):
    """generically non-scalar data, such as a list, array, but not including a string or bytes"""

    @util.hide_in_traceback
    def validate(self, value, owner=None):
        if isinstance(value, (bytes, str)):
            raise ValueError(f"given text data but expected a non-scalar data")
        if not hasattr(value, "__iter__") and not hasattr(value, "__len__"):
            raise ValueError(f"expected non-scalar data but given a non-iterable")
        return value


class Int(BoundedNumber, type=int):
    """accepts numerical, str, or bytes values, following normal python casting procedures (with bounds checking)"""


class Float(BoundedNumber, type=float):
    """accepts numerical, str, or bytes values, following normal python casting procedures (with bounds checking)"""

    step: ThisType = None

    @util.hide_in_traceback
    def validate(self, value, owner=None):
        value = super().validate(value, owner)
        if self.step is not None:
            mod = value % self.step
            if mod < self.step / 2:
                return value - mod
            else:
                return value - (mod - self.step)
        return value


class Complex(Trait, type=complex):
    """accepts numerical or str values, following normal python casting procedures (with bounds checking)"""

    allow_none: bool = False


class Bool(Trait, type=bool):
    """accepts boolean or numeric values, or a case-insensitive match to one of ('true',b'true','false',b'false')"""

    allow_none: bool = False

    @util.hide_in_traceback
    def validate(self, value, owner=None):
        if isinstance(value, (bool, numbers.Number)):
            return value
        elif isinstance(value, (str, bytes)):
            lvalue = value.lower()
            if lvalue in ("true", b"true"):
                return True
            elif lvalue in ("false", b"false"):
                return False
        raise ValueError(
            f"'{self.__repr__(owner_inst=owner)}' accepts only boolean, numerical values,"
            "or one of ('true',b'true','false',b'false'), case-insensitive"
        )


class String(Trait):
    """base class for string types, which adds support for case sensitivity arguments"""

    case: bool = True
    # allow_none: bool = True # let's not override this default

    @util.hide_in_traceback
    def contains(self, iterable, value):
        if not self.case:
            iterable = [v.lower() for v in iterable]
            value = value.lower()
        return value in iterable


class Unicode(String, type=str):
    """accepts strings or numeric values only; convert others explicitly before assignment"""

    default: ThisType = ""

    @util.hide_in_traceback
    def validate(self, value, owner=None):
        if not isinstance(value, (str, numbers.Number)):
            raise ValueError(
                f"'{type(self).__qualname__}' traits accept values of str or numerical type, not {type(value).__name__}"
            )
        return value


class Bytes(String, type=bytes):
    """accepts bytes objects only - encode str (unicode) explicitly before assignment"""

    default: ThisType = b""


class Iterable(Trait):
    """accepts any iterable"""

    @util.hide_in_traceback
    def validate(self, value, owner=None):
        if not hasattr(value, "__iter__"):
            raise ValueError(
                f"'{type(self).__qualname__}' traits accept only iterable values"
            )
        return value


class Dict(Iterable, type=dict):
    """accepts any type of iterable value accepted by python `dict()`"""


class List(Iterable, type=list):
    """accepts any type of iterable value accepted by python `list()`"""


class Tuple(Iterable, type=tuple):
    """accepts any type of iterable value accepted by python `tuple()`"""

    sets: bool = False


class Path(Trait, type=Path):
    must_exist: bool = False
    """ does the path need to exist when set? """

    @util.hide_in_traceback
    def validate(self, value, owner=None):
        path = self.type(value)

        if self.must_exist and not path.exists():
            raise IOError()

        return path


class PandasDataFrame(NonScalar, type=pd.DataFrame):
    pass


class PandasSeries(NonScalar, type=pd.Series):
    pass


class NumpyArray(NonScalar, type=np.ndarray):
    pass


class NetworkAddress(Unicode):
    """a IDN-compatible network address string, such as an IP address or DNS hostname"""

    accept_port: bool = True

    @util.hide_in_traceback
    def validate(self, value, owner=None):
        """Rough IDN compatible domain validator"""

        host, *extra = value.split(":", 1)

        if len(extra) > 0:
            port = extra[0]
            try:
                int(port)
            except ValueError:
                raise ValueError(f'port {port} in "{value}" is invalid')

            if not self.accept_port:
                raise ValueError(
                    f"{self} does not accept a port number (accept_port=False)"
                )

        for validate in _val.ipv4, _val.ipv6, _val.domain, _val.slug:
            if validate(host):
                break
        else:
            raise ValueError("invalid host address")

        return value


VALID_TRAIT_ROLES = Trait.ROLE_VALUE, Trait.ROLE_PROPERTY, Trait.ROLE_DATARETURN


def subclass_namespace_traits(namespace_dict, role, omit_trait_attrs):
    for name, attr in dict(namespace_dict).items():
        if isclass(attr) and issubclass(attr, Trait):
            # subclass our traits with the given role
            new_trait = type(name, (attr,), dict(role=role))
            new_trait.role = role

            # clean out annotations for stub generation
            new_trait.__annotations__ = dict(new_trait.__annotations__)
            for drop_attr in omit_trait_attrs:
                new_trait.__annotations__.pop(drop_attr)
            new_trait.__module__ = namespace_dict["__name__"]

            namespace_dict[name] = new_trait
