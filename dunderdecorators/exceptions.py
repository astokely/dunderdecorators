
from collections import namedtuple
from collections.abc import Mapping, Iterable
from typing import Optional, TypeVar, Hashable, \
	Dict, Iterable, Union, Tuple, List, Any, Generator

Cls = TypeVar('User Defined Class')

class DunderDecoratorException(Exception):

	def __init__(
			self,
			cls_obj: Cls,
			message: str,
			attr: Optional[str] = '',
	) -> None:
		self.cls_obj = cls_obj
		self.attr = attr
		self.message = message
		self.cls_obj_name_and_addr = (
			f'<{cls_obj.__module__}'
			+ f'.{cls_obj.__class__.__name__}'
			+ f' object at {hex(id(cls_obj))}>'
		)
		super().__init__(message)

	def __str__(self):
		if self.message == 'iterable':
			attr_type = getattr(
					self.cls_obj, self.attr
			).__class__.__name__ 
			iterable_attrs = []
			message = ''
			message = (
				f'\n\nAttribute "{self.attr}" belonging to '
				+ f'{self.cls_obj_name_and_addr} is\n'
				+ f'of type {attr_type}, which is not iterable. attr' 
				+ f' must be the name of an attribute\n'
				+ f'owned by {self.cls_obj_name_and_addr} '
				+ f'that is {self.message}.'
			)
			if hasattr(self.cls_obj, '__slots__'):
				message += (
					f'\nConsider setting slots to True.'
				)
				for attr in self.cls_obj.__slots__:
					value = getattr(self.cls_obj, attr)
					if isinstance(value, Iterable):
						iterable_attrs.append(attr)
			elif hasattr(self.cls_obj, '__dict__'):
				message += (
					f'\n\nConsider using dunder_iter without '
					+ f'any parameters, which will define __iter__\n'
					+ f'with repsect to {self.cls_obj_name_and_addr}\'s __dict__.'
				)
				for attr, value in self.cls_obj.__dict__.items():
					if isinstance(value, Iterable):
						iterable_attrs.append(attr)
			if iterable_attrs:
				message = (
					f'{message[:-1]}, \nor setting attr equal to the name of one\n'
					+ f'of {self.cls_obj_name_and_addr}\'s iterable attributes.\n'
					+ f'A list of {self.cls_obj_name_and_addr}\'s '
					+ f'iterable \nattributes is provided below.\n'
					+ f'{iterable_attrs}'
				)

		if self.message == 'indexable':
			attr_type = getattr(
					self.cls_obj, self.attr
			).__class__.__name__ 
			indexable_attrs = []
			message = ''
			message = (
				f'\n\nAttribute "{self.attr}" belonging to '
				+ f'{self.cls_obj_name_and_addr} is\n'
				+ f'of type {attr_type}, which is not indexable. attr' 
				+ f' must be the name of an attribute\n'
				+ f'owned by {self.cls_obj_name_and_addr} '
				+ f'that is {self.message}.'
			)
			if hasattr(self.cls_obj, '__slots__'):
				message += (
					f'\nConsider setting slots to True.'
				)
				for attr in self.cls_obj.__slots__:
					value = getattr(self.cls_obj, attr)
					if hasattr(value, '__getitem__'):
						indexable_attrs.append(attr)
			elif hasattr(self.cls_obj, '__dict__'):
				message += (
					f'\n\nConsider using dunder_iter without '
					+ f'any parameters, which will define __iter__\n'
					+ f'with repsect to {self.cls_obj_name_and_addr}\'s __dict__.'
				)
				for attr, value in self.cls_obj.__dict__.items():
					if hasattr(value, '__getitem__'):
						indexable_attrs.append(attr)
			if indexable_attrs:
				message = (
					f'{message[:-1]}, \nor setting attr equal to the name of one\n'
					+ f'of {self.cls_obj_name_and_addr}\'s indexable attributes.\n'
					+ f'A list of {self.cls_obj_name_and_addr}\'s '
					+ f'indexable \nattributes is provided below.\n'
					+ f'{indexable_attrs}'
				)

		elif self.message == ('dict', 'iter'):
			message = (
				f'\n{self.cls_obj_name_and_addr} '
				+ f' has no attribute  "__dict__".\n'
			)
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
						f'{message[:-1]}, or setting attr to the name of an iterable '
						+ f'attribute owned\nby {self.cls_obj_name_and_addr}. '
						+ f'A list of {self.cls_obj_name_and_addr}\'s '
						+ f'iterable \nattributes is provided below.\n'
						+ f'{iterable_attrs}'
					)
		elif self.message == ('slots', 'iter'):
			message = (
				f'\n{self.cls_obj_name_and_addr} '
				+ f' has no attribute  "__slots__".\n'
			)
			if hasattr(self.cls_obj, '__dict__'):
				message += (
					f'\nConsider using dunder_iter without '
					+ f'any parameters, which will define __iter__\n'
					+ f'with repsect to {self.cls_obj_name_and_addr}\'s __dict__.'
				)
				iterable_attrs = [] 
				for attr, value in self.cls_obj.__dict__.items():
					if isinstance(value, Iterable):
						iterable_attrs.append(attr)
				if iterable_attrs:
					message = (
						f'{message[:-1]}, or setting attr to the name of an iterable '
						+ f'attribute owned\nby {self.cls_obj_name_and_addr}. '
						+ f'A list of {self.cls_obj_name_and_addr}\'s '
						+ f'iterable \nattributes is provided below.\n'
						+ f'{iterable_attrs}'
					)
		elif self.message == 'slots_immutable':
			message = (
				f'\n{self.cls_obj_name_and_addr} '
				+ f'uses __slots__ instead of __dict__ '
				+ f'to store it\'s attributes, which '
				+ f'means you cannot\n'
				+ f'add new attributes to '
				+ f'{self.cls_obj_name_and_addr} '
				+ f'post object creation.'
			)
		return message 

