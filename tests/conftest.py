import pytest
import shutil
import os
from typing import List, Dict, Optional, Set, Tuple
from dunderdecorators import dunder_iter, dunder_getitem, \
    dunder_setitem, dunder_missing, dunder_repr

@pytest.fixture(scope='session')
def dunder_iter_no_params():

	@dunder_iter
	class DunderIterNoParams(object):
		pass
	
	dunder_iter_no_params_obj = DunderIterNoParams()
	return dunder_iter_no_params_obj

@pytest.fixture(scope='session')
def dunder_iter_with_no_slots_exception():

	@dunder_iter
	class DunderIterNoSlotsError(object):

		__slots__ = ('a', 'b', 'c',)

		def __init__(
				self,
				a: int,
				b: float,
				c: float,
		) -> None:
			self.a = a
			self.b = b
			self.c = c
	
	dunder_iter_no_slots_exception = (
		DunderIterNoSlotsError(
			1, 2.0, 3.0
		)
	)
	return dunder_iter_no_slots_exception

@pytest.fixture(scope='session')
def dunder_iter_slots_no_iterable_attrs():

	@dunder_iter(slots=True)
	class DunderIterSlotsNoIterableAttrs(object):

		__slots__ = ('a', 'b', 'c',)

		def __init__(
				self,
				a: int,
				b: float,
				c: float,
		) -> None:
			self.a = a
			self.b = b
			self.c = c
	
	dunder_iter_slots_no_iter_attrs = (
		DunderIterSlotsNoIterableAttrs(
			1, 2.0, 3.0
		)
	)
	return dunder_iter_slots_no_iter_attrs

@pytest.fixture(scope='session')
def dunder_iter_no_slots_no_iterable_attrs_exception():

	@dunder_iter(slots=True)
	class DunderIterNoSlotsNoIterableAttrs(object):
		def __init__(
				self,
				a: int,
				b: float,
				c: float,
		) -> None:
			self.a = a
			self.b = b
			self.c = c
	
	dunder_iter_no_slots_no_iter_attrs = (
		DunderIterNoSlotsNoIterableAttrs(
			1, 2.0, 3.0
		)
	)
	return dunder_iter_no_slots_no_iter_attrs

@pytest.fixture(scope='session')
def dunder_iter_slots_with_iterable_attrs_exception():

	@dunder_iter(attr='a')
	class DunderIterSlotsIterableAttrs(object):
		__slots__ = ('a', 'b', 'c', 'd', 'e',)
		def __init__(
				self,
				a: int,
				b: float,
				c: List,
				d: List,
				e: List,
		) -> None:
			self.a = a
			self.b = b
			self.c = c
			self.d = d
			self.e = e
	
	dunder_iter_slots_with_iter_attrs = (
		DunderIterSlotsIterableAttrs(
			1, 2.0,
			list(range(10)),
			list(range(100)),
			list(range(1000)),
		)
	)
	return dunder_iter_slots_with_iter_attrs

@pytest.fixture(scope='session')
def dunder_iter_slots_with_iterable_attrs():

	@dunder_iter(attr='c')
	class DunderIterSlotsIterableAttrs(object):
		__slots__ = ('a', 'b', 'c', 'd', 'e',)
		def __init__(
				self,
				a: int,
				b: float,
				c: List,
				d: List,
				e: List,
		) -> None:
			self.a = a
			self.b = b
			self.c = c
			self.d = d
			self.e = e
	
	dunder_iter_slots_with_iter_attrs = (
		DunderIterSlotsIterableAttrs(
			1, 2.0,
			list(range(10)),
			list(range(100)),
			list(range(1000)),
		)
	)
	return dunder_iter_slots_with_iter_attrs

@pytest.fixture(scope='session')
def dunder_iter_with_iterable_attrs():

	@dunder_iter(attr='c')
	class DunderIterIterableAttrs(object):
		def __init__(
				self,
				a: int,
				b: float,
				c: List,
				d: List,
				e: List,
		) -> None:
			self.a = a
			self.b = b
			self.c = c
			self.d = d
			self.e = e
	
	dunder_iter_with_iter_attrs = (
		DunderIterIterableAttrs(
			1, 2.0,
			list(range(10)),
			list(range(100)),
			list(range(1000)),
		)
	)
	return dunder_iter_with_iter_attrs

@pytest.fixture(scope='session')
def dunder_iter_with_no_iterable_attrs_exception():

	@dunder_iter(attr='a')
	class DunderIterNoIterableAttrsError(object):
		def __init__(
				self,
				a: int,
		) -> None:
			self.a = a
	
	dunder_iter_with_no_iter_attrs = (
		DunderIterNoIterableAttrsError(1)
	)
	return dunder_iter_with_no_iter_attrs

@pytest.fixture(scope='session')
def control():

	class Control(object):
		pass
	
	control_obj = Control()
	return control_obj
	

