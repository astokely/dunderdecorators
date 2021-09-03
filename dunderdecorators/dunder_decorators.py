'''
By Andy Stokely
'''
from collections import namedtuple
import numpy as np
from typing import Optional, TypeVar, Hashable, \
	Dict, Iterable, Union, Tuple, List, Any, Generator

Cls = TypeVar('User Defined Class')

class TypeList(list):

    def __init__(self, iterable, exclude_type):
        self.exclude_type = exclude_type
        super().__init__([
            i for i in iterable
            if not isinstance(i, exclude_type
        )])

    def append(self, val):
        if self.exclude_type == int:
            if isinstance(bool):
                super().append(value)
        if isinstance(self.exclude_type):
            return
        super().append(value)

    def __setitem__(self, index, val):
        if self.exclude_type == int:
            if isinstance(key, bool):
                super().__setitem__(key, value)
        if isinstance(key, self.exclude_type):
            return
        super().__setitem__(key, value)

def dunder_iter(
		cls: Optional[Cls] = None, 
		iter_return: Optional[str] = (
			'attr_or_field_and_value'
		),
		iter_attr: Optional[Iterable] = False,
		iter_field: Optional[Iterable] = False,
) -> Cls:
	def wrap(
			cls: Cls,
	) -> Cls:
		iterate_over_field_or_attr = TypeList(
			[iter_attr, iter_field], 
			bool
		)
		if iterate_over_field_or_attr:
			def __iter__(
						cls: Cls
				) -> Generator:
				iter_ = iterate_over_field_or_attr[0]
				iter_ = getattr(cls, iter_)
				if isinstance(iter_, dict):
					for k, v in iter_.items():
						yield k, v
				else:
					for i in iter_:
						yield i
			setattr(cls, '__iter__', __iter__)
		else:
			if iter_return == 'attr_or_field_and_value':
				def __iter__(
						cls: Cls
				) -> Generator:
					for k, v in cls.__dict__.items():
						yield k, v
				setattr(cls, '__iter__', __iter__)
			elif iter_return == 'attr':
				def __iter__(
						cls: Cls
				) -> Generator:
					for field in cls.__dict__.keys():
						yield field
				setattr(cls, '__iter__', __iter__)
			elif iter_return == 'field':
				def __iter__(
						cls: Cls
				) -> Generator:
					for field in cls.__dict__.keys():
						yield field
				setattr(cls, '__iter__', __iter__)
			elif iter_return == 'value':
				def __iter__(
						cls: Cls
				) -> Generator:
					for value in cls.__dict__.values():
						yield value

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

