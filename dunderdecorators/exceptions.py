
from collections import namedtuple
from collections.abc import Mapping, Iterable
import numpy as np
from typing import Optional, TypeVar, Hashable, \
	Dict, Iterable, Union, Tuple, List, Any, Generator

Cls = TypeVar('User Defined Class')

class DunderDecoratorException(Exception):

	def __init__(
			self,
			message: Optional[str] = '',
	) -> None:
		self.message = message 
		super().__init__(message)

	def __str__(self):
		return f'{self.message}'

class AttributeException(DunderDecoratorException):

	def __init__(
			self,
			cls_obj: Cls,
			attr: str,
			message: Optional[str] = '',
	) -> None:
		self.cls_obj = cls_obj
		self.attr = attr
		self.message = message
		super().__init__(message)

	def __str__(self):
		attr_type = getattr(
				self.cls_obj, self.attr
		).__class__.__name__ 
		return (
			f'\n\nAttribute "{self.attr}" belonging to {self.cls_obj} is\n'
			+ f'of type {attr_type}, which is not iterable. attr' 
			+ f' must be the name of an attribute\n'
 			+ f'owned by {self.cls_obj} that is {self.message}.'
		)

class ClassObjectException(DunderDecoratorException):

	def __init__(
			self,
			cls_obj: Cls,
			message,
	) -> None:
		self.cls_obj = cls_obj
		self.message = message
		super().__init__(message)

	def __str__(self):
		message = (
			f'\n\n{self.cls_obj} does not'
			+ f' have a __dict__ attribute.'
		)
		if self.message == 'dict':
			if hasattr(self.cls_obj, '__slots__'):
				message += (
					f'\nConsider setting slots to True.'
				)
				iterable_attrs = [] 
				for attr in self.cls_obj.__slots__:
					value = getattr(self.cls_obj, attr)
					if isinstance(value, Iterable):
						iterable_attrs.append(attr)
				if iterable_attrs:
					message = (
						f'{message[:-1]}, or attr to the name of an iterable '
						+ f'attribute owned\nby {self.cls_obj}. A list of '
						+ f'{self.cls_obj}\'s iterable \nattributes is provided below.\n'
						+ f'{iterable_attrs}'
					)
		elif self.message == 'slots':
			if hasattr(self.cls_obj, '__dict__'):
				message += (
					f'\nConsider setting slots to False.'
				)
				iterable_attrs = [] 
				for attr in self.cls_obj.__slots__:
					value = getattr(self.cls_obj, attr)
					if isinstance(value, Iterable):
						iterable_attrs.append(attr)
				if iterable_attrs:
					message = (
						f'{message[:-1]}, or attr to the name of an iterable '
						+ f'attribute owned\nby {self.cls_obj}. A list of '
						+ f'{self.cls_obj}\'s iterable \nattributes is provided below.\n'
						+ f'{iterable_attrs}'
					)
		return f'{message}'
