import os
import pytest
from typing import Callable
from dunderdecorators import dunder_iter, dunder_getitem, \
	dunder_setitem, dunder_missing, dunder_repr 
from dunderdecorators import DunderDecoratorException 

def test_dunder_iter_no_params_positive(
			dunder_iter_no_params: Callable, 
) -> None:
	dunder_iter_no_params.a = 1
	dunder_iter_no_params.b = 2
	dunder_iter_no_params.c = 3
	attr_values = [i for i in dunder_iter_no_params]
	assert attr_values == [('a', 1), ('b', 2), ('c', 3)]

def test_dunder_iter_no_params_negative1(
			dunder_iter_no_params: Callable, 
) -> None:
	dunder_iter_no_params.a = 1
	dunder_iter_no_params.b = 2
	dunder_iter_no_params.c = 3
	attr_values = [i for i in dunder_iter_no_params]
	assert attr_values != [1, 2, 3]

def test_dunder_iter_no_params_negative2(
			dunder_iter_no_params: Callable, 
) -> None:
	dunder_iter_no_params.a = 1
	dunder_iter_no_params.b = 2
	dunder_iter_no_params.c = 3
	attr_values = [i for i in dunder_iter_no_params]
	assert attr_values != ['a', 'b', 'c']

def test_dunder_iter_no_params_has_iter(
			dunder_iter_no_params: Callable, 
) -> None:
	assert hasattr(dunder_iter_no_params, '__iter__') == True	

def test_dunder_iter_no_params_parent_inherit_iter_negative(
			control: Callable
) -> None:

	@dunder_iter
	class ControlChildWithDunderIter(type(control)):
		pass	
	control_child_with_dunder_iter = (
		ControlChildWithDunderIter()
	)
	assert (
		hasattr(control, '__iter__') == False and
		hasattr(
			control_child_with_dunder_iter, 
			'__iter__'
		) == True 
	)

def test_dunder_iter_slots_no_iter_attrs(
		dunder_iter_slots_no_iterable_attrs: Callable,
) -> None:
	attr_values = [
		i for i in dunder_iter_slots_no_iterable_attrs
	]
	assert attr_values == [
		('a', 1),
		('b', 2.0),
		('c', 3.0)
	]

def test_dunder_iter_slots_no_iter_attrs_negative1(
		dunder_iter_slots_no_iterable_attrs: Callable,
) -> None:
	attr_values = [
		i for i in dunder_iter_slots_no_iterable_attrs
	]
	assert attr_values != ['a', 'b', 'c']	

def test_dunder_iter_slots_no_iter_attrs_negative2(
		dunder_iter_slots_no_iterable_attrs: Callable,
) -> None:
	attr_values = [
		i for i in dunder_iter_slots_no_iterable_attrs
	]
	assert attr_values != [1, 2.0, 3.0]

def test_dunder_iter_no_slots_no_iter_attrs_exception(
		dunder_iter_no_slots_no_iterable_attrs_exception: Callable,
) -> None:
	with pytest.raises(DunderDecoratorException) as exception_info:
		attr_values = [
			i for i in dunder_iter_no_slots_no_iterable_attrs_exception
		]
	assert (
		('slots', 'iter') == exception_info.value.message and  
		('dict', 'iter') != exception_info.value.message and
		'iterable' != exception_info.value.message
	)

def test_dunder_iter_slots_with_iter_attrs_exception(
		dunder_iter_slots_with_iterable_attrs_exception: Callable,
) -> None:
	with pytest.raises(DunderDecoratorException) as exception_info:
		attr_values = [
			i for i in dunder_iter_slots_with_iterable_attrs_exception
		]
	assert (
		('slots', 'iter') != exception_info.value.message and  
		('dict', 'iter') != exception_info.value.message and
		'iterable' == exception_info.value.message
	)

def test_dunder_iter_slots_with_iter_attrs(
		dunder_iter_slots_with_iterable_attrs: Callable,
) -> None:
	attr_values = [
		i for i in dunder_iter_slots_with_iterable_attrs
	]
	assert attr_values == list(range(10))

def test_dunder_iter_with_iter_attrs(
		dunder_iter_with_iterable_attrs: Callable,
) -> None:
	attr_values = [
		i for i in dunder_iter_with_iterable_attrs
	]
	assert attr_values == list(range(10))

def test_dunder_iter_with_no_iter_attrs_exception(
		dunder_iter_with_no_iterable_attrs_exception: Callable,
) -> None:
	with pytest.raises(DunderDecoratorException) as exception_info:
		attr_values = [
			i for i in dunder_iter_with_no_iterable_attrs_exception
		]
	assert (
		('slots', 'iter') != exception_info.value.message and  
		('dict', 'iter') != exception_info.value.message and
		'iterable' == exception_info.value.message
	)

def test_dunder_iter_no_slots(
		dunder_iter_with_no_slots_exception: Callable,
) -> None:
	with pytest.raises(DunderDecoratorException) as exception_info:
		attr_values = [
			i for i in dunder_iter_with_no_slots_exception
		]
	assert (
		('slots', 'iter') != exception_info.value.message and  
		('dict', 'iter') == exception_info.value.message and
		'iterable' != exception_info.value.message
	)
