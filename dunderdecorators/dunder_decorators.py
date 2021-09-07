'''
By Andy Stokely
'''

from collections import namedtuple
from collections.abc import Mapping, Iterable
from typing import Optional, TypeVar, Hashable, \
	Dict, Iterable, Union, Tuple, List, Any, Generator
from .exceptions import DunderDecoratorException 

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
						raise DunderDecoratorException(
							cls, ('dict', 'iter')
						) 
				setattr(cls, '__iter__', __iter__)
			else:
				def __iter__(
						cls: Cls
				) -> Generator:
					if hasattr(cls, '__slots__'):
						for attr in cls.__slots__:
							yield attr, getattr(cls, attr) 
					else:
						raise DunderDecoratorException(
							cls, ('slots', 'iter')
						) 
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
					raise DunderDecoratorException(
						cls, 
						'iterable', 
						attr
					) 
			setattr(cls, '__iter__', __iter__)
		return cls
	if cls is None:
		return wrap 
	return wrap(cls)

def dunder_setitem(
		cls: Optional[Cls] = None, 
		attr: Optional[str] = False, 
		slots: Optional[str] = None,
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
				if hasattr(getattr(cls, attr), '__getitem__'):
					getattr(cls, attr)[key] = value
				else:
					raise DunderDecoratorException(
						cls, 
						'indexable', 
						attr
					) 
				return
			setattr(cls, '__setitem__', __setitem__)
		else:
			if slots is None:
				def __setitem__(
						cls: Cls, 
						key: Hashable, 
						value: Any,
				) -> None:
					if hasattr(cls, '__dict__'):
						cls.__dict__[key] = value
					else:
						raise DunderDecoratorException('dict')
					return
				setattr(
					cls, 
					'__setitem__', 
					__setitem__
				)
			else:
				def __setitem__(
						cls: Cls, 
						key: str, 
						value: Any,
				) -> None:
					if hasattr(cls, '__slots__'):
						if hasattr(cls, key):
							setattr(cls, key, value)
						else:
							raise DunderDecoratorException(
								'slots_immutable'
							)
					else:
						raise DunderDecoratorException('slots')
					return
				setattr(
					cls, 
					'__setitem__', 
					__setitem__
				)
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

