'''
By Andy Stokely
'''

from collections import namedtuple
from collections.abc import Mapping, Iterable
import numpy as np
from typing import Optional, TypeVar, Hashable, \
	Dict, Iterable, Union, Tuple, List, Any, Generator
from .exceptions import DunderIterError
Cls = TypeVar('User Defined Class')


def dunder_iter(
		cls: Optional[Cls] = None, 
		attr: Optional[str] = None,
		slots: Optional[str] = None,
) -> Cls:
	def wrap(
			cls: Cls,
	) -> Cls:
		if attr is None:
			if slots is None:
				def __iter__(
						cls: Cls
				) -> Generator:
					if hasattr(cls, '__dict__'):
						for attr, value in cls.__dict__.items():
							yield attr, value
					else:
						raise DunderIterError(cls, 'dict') 
				setattr(cls, '__iter__', __iter__)
			else:
				def __iter__(
						cls: Cls
				) -> Generator:
					if hasattr(cls, '__slots__'):
						for attr in cls.__slots__:
							yield attr, getattr(cls, attr) 
					else:
						raise DunderIterError(cls, 'slots') 
				setattr(cls, '__iter__', __iter__)
		else:
			def __iter__(
					cls: Cls
			) -> Generator:
				iter_attr = getattr(cls, attr)
				if isinstance(iter_attr, Mapping):
					for key, value in iter_attr.items():
						yield key, value
				elif isinstance(iter_attr, Iterable):
					for i in iter_attr:
						yield i 
				else:
					raise DunderIterError(cls, 'iterable', attr) 
			setattr(cls, '__iter__', __iter__)
		return cls
	if cls is None:
		return wrap 
	return wrap(cls)

def dunder_setitem(
		cls: Optional[Cls] = None, 
		attr: Optional[str] = False 
) -> Cls:
	def wrap(
			cls: Cls,
	) -> Cls:
		if attr:
			def __setitem__(
					cls: Cls, 
					key: Hashable, 
					value: Any,
			) -> None:
				getattr(cls, attr)[key] = value
				return
		else:
			def __setitem__(
					cls: Cls, 
					key: Hashable, 
					value: Any,
			) -> None:
				cls.__dict__[key] = value
				return
		setattr(cls, '__setitem__', __setitem__)
		return cls
	if cls is None:
		return wrap 
	return wrap(cls)

def dunder_getitem(
		cls: Optional[Cls] = None, 
		attr: Optional[str] = False 
) -> Cls:
	def wrap(
			cls: Cls,
	) -> Cls:
		if attr:
			if hasattr(cls, '__missing__'):
				def __getitem__(
						cls: Cls, 
						key: Hashable
				) -> Any:
					if key in getattr(cls, attr).keys():
						return getattr(cls, attr)[key]
					cls.__missing__(key)
					return getattr(cls, attr)[key]
				setattr(cls, '__getitem__', __getitem__)
			else:
				def __getitem__(
						cls: Cls, 
						key: Hashable
				) -> Any:
					return getattr(cls, attr)[key]
				setattr(cls, '__getitem__', __getitem__)
		else:
			if hasattr(cls, '__missing__'):
				def __getitem__(
						cls: Cls, 
						key: Hashable
				) -> Any:
					if key in cls.__dict__.keys():
						return cls.__dict__[key]
					cls.__missing__(key)
					return cls.__dict__[key]
				setattr(cls, '__getitem__', __getitem__)
			else:
				def __getitem__(cls, key):
					return cls.__dict__[key]
				setattr(cls, '__getitem__', __getitem__)
		return cls
	if cls is None:
		return wrap 
	return wrap(cls)

def dunder_missing(
		cls: Optional[Cls] = None, 
		attr: Optional[str] = False,
		default_value: Optional[Any] = None,	
) -> Any:
	def wrap(
			cls: Cls,
	) -> Cls:
		setattr(
			cls, 
			'__default_value', 
			default_value 
		)
		if attr:
			def __missing__(
					cls: Cls, 
					key: Hashable,
			) ->None:
				getattr(cls, attr)[key] = cls.__default_value
				return
			setattr(cls, '__missing__', __missing__)
		else:
			def __missing__(
					cls: Cls, 
					key: Hashable,
			) ->None:
				cls.__dict__[key] = cls.__default_value
				return
			setattr(cls, '__missing__', __missing__)
		return cls
	if cls is None:
		return wrap 
	return wrap(cls)

def dunder_repr(
		cls: Optional[Cls] = None, 
) -> Any:
	def wrap(
			cls: Cls,
	) -> Cls:
		def __repr__(cls) -> Dict:
			repr_cls_dict = {
				(
					attr if not str(attr)[0].isdigit() 
					else f'{attr.__class__.__name__}_{attr}'
				) : value for attr, value 
				in cls.__dict__.items()
			}
			ReprNamedTuple = namedtuple(
				cls.__class__.__name__, 
				repr_cls_dict
			)
			repr_namedtuple = ReprNamedTuple(
				**repr_cls_dict
			)
			return str(repr_namedtuple)
		setattr(cls, '__repr__', __repr__)
		return cls
	if cls is None:
		return wrap 
	return wrap(cls)

