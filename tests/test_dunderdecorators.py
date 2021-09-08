from dunderdecorators import dunder_iter, dunder_setitem, \
	dunder_getitem, dunder_missing, dunder_repr, \
	DunderDecoratorException
import pytest
from typing import List, Dict

def test_dunder_iter():
	@dunder_iter
	class Test(object):

		def __init__(
				self,
				a: int,
				b: int,
				c: int,
		) -> None:
			self.a = a
			self.b = b
			self.c = c

	test = Test(1, 2, 3)
	test_values = [i for i in test]
	assert test_values == [
		('a', 1), 
		('b', 2), 
		('c', 3)
	]

def test_dunder_iter_with_non_mapping_attr():
	@dunder_iter(attr='a')
	class Test(object):

		def __init__(
				self,
				a: List,
		) -> None:
			self.a = a

	test = Test([1, 2, 3])
	test_values = [i for i in test]
	assert test_values == [1, 2, 3]

def test_dunder_iter_with_mapping_attr():
	@dunder_iter(attr='a')
	class Test(object):

		def __init__(
				self,
				a: Dict,
		) -> None:
			self.a = a

	test = Test({
		'a' : 1, 
		'b' : 2, 
		'c' : 3
	})
	test_values = {k : v for k, v in test}
	assert test_values == {
		'a' : 1, 
		'b' : 2, 
		'c' : 3
	}

def test_dunder_iter_slots_exception():
	@dunder_iter(slots=True)
	class Test(object):

		def __init__(
				self,
				a: int,
				b: int,
				c: int,
		) -> None:
			self.a = a
			self.b = b
			self.c = c

	test = Test(1, 2, 3)
	with pytest.raises(DunderDecoratorException) as exception_info:
		test_values = [i for i in test]
	assert exception_info.value.message == ('slots', 'iter')

def test_dunder_iter_iterable_attr_exception():
	@dunder_iter(attr='a')
	class Test(object):

		def __init__(
				self,
				a: int,
				b: int,
				c: int,
		) -> None:
			self.a = a
			self.b = b
			self.c = c

	test = Test(1, 2, 3)
	with pytest.raises(DunderDecoratorException) as exception_info:
		test_values = [i for i in test]
	assert exception_info.value.message == ('iterable')

def test_dunder_iter_with_slots():
	@dunder_iter(slots=True)
	class Test(object):
		__slots__ = ('a', 'b', 'c')
		def __init__(
				self,
				a: int,
				b: int,
				c: int,
		) -> None:
			self.a = a
			self.b = b
			self.c = c

	test = Test(1, 2, 3)
	test_values = [i for i in test]
	assert test_values == [
		('a', 1), 
		('b', 2), 
		('c', 3)
	]

def test_dunder_iter_with_slots_and_attr():
	@dunder_iter(attr='a')
	class Test(object):
		__slots__ = ('a',)
		def __init__(
				self,
				a: List,
		) -> None:
			self.a = a

	test = Test([1, 2, 3])
	test_values = [i for i in test]
	assert test_values == [1, 2, 3]

def test_dunder_iter_with_slots_dict_exception():
	@dunder_iter
	class Test(object):
		__slots__ = ('a', 'b', 'c')
		def __init__(
				self,
				a: int,
				b: int,
				c: int,
		) -> None:
			self.a = a
			self.b = b
			self.c = c

	test = Test(1, 2, 3)
	with pytest.raises(DunderDecoratorException) as exception_info:
		test_values = [i for i in test]
	assert exception_info.value.message == ('dict', 'iter')

def test_dunder_iter_with_slots_iterable_attr_exception():
	@dunder_iter(slots=True, attr='a')
	class Test(object):
		__slots__ = ('a', 'b', 'c')
		def __init__(
				self,
				a: int,
				b: int,
				c: int,
		) -> None:
			self.a = a
			self.b = b
			self.c = c

def test_dunder_iter_with_slots_and_iter_slots_declaration():
	@dunder_iter(attr='a')
	class Test(object):
		__slots__ = ('a',)
		def __init__(
				self,
				a: List,
		) -> None:
			self.a = a

	test = Test([1, 2, 3])
	test_values = [i for i in test]
	assert test_values == [1, 2, 3]

def test_dunder_setitem():
	@dunder_setitem
	class Test(object):

		def __init__(
				self,
				a: int,
				b: int,
				c: int,
		) -> None:
			self.a = a
			self.b = b
			self.c = c

	test = Test(1, 2, 3)
	test['a'] = 3
	test['b'] = 2
	test['c'] = 1
	assert (
		[test.a, test.b, test.c] == 
		[3, 2, 1]
	)

def test_dunder_setitem_with_non_mapping_attr():
	@dunder_setitem(attr='a')
	class Test(object):

		def __init__(
				self,
				a: List,
		) -> None:
			self.a = a

	test = Test([1, 2, 3])
	test[0] = 3
	test[1] = 2
	test[2] = 1
	assert (
		test.a == 
		[3, 2, 1]
	)

def test_dunder_iter_with_mapping_attr():
	@dunder_setitem(attr='a')
	class Test(object):

		def __init__(
				self,
				a: Dict,
		) -> None:
			self.a = a

	test = Test({
		'a' : 1, 
		'b' : 2, 
		'c' : 3
	})
	test['a'] = 3
	test['b'] = 2
	test['c'] = 1
	assert test.a == {
		'a' : 3, 
		'b' : 2, 
		'c' : 1
	}

def test_dunder_setitem_with_slots():
	@dunder_setitem(slots=True)
	class Test(object):
		__slots__ = ('a', 'b', 'c')
		def __init__(
				self,
				a: int,
				b: int,
				c: int,
		) -> None:
			self.a = a
			self.b = b
			self.c = c

	test = Test(1, 2, 3)
	test['a'] = 3
	test['b'] = 2
	test['c'] = 1
	assert (
		[test.a, test.b, test.c] == 
		[3, 2, 1]
	)

def test_dunder_setitem_with_slots_and_non_mapping_attr():
	@dunder_setitem(attr='a', slots=True)
	class Test(object):

		def __init__(
				self,
				a: List,
		) -> None:
			self.a = a

	test = Test([1, 2, 3])
	test[0] = 3
	test[1] = 2
	test[2] = 1
	assert (
		test.a == 
		[3, 2, 1]
	)

def test_dunder_setitem_with_slots_and_mapping_attr():
	@dunder_setitem(attr='a', slots=True)
	class Test(object):

		def __init__(
				self,
				a: Dict,
		) -> None:
			self.a = a

	test = Test({
		'a' : 1, 
		'b' : 2, 
		'c' : 3
	})
	test['a'] = 3
	test['b'] = 2
	test['c'] = 1
	assert test.a == {
		'a' : 3, 
		'b' : 2, 
		'c' : 1
	}

def test_dunder_setitem_indexing_exception():
	@dunder_setitem(attr='a')
	class Test(object):

		def __init__(
				self,
				a: int,
		) -> None:
			self.a = a
	test = Test(1)
	exception_key_words = [
		'Attribute',
		'belonging',
		'indexable',
		'attr',
		'name',
		'owned',
		'without',
		'parameters',
		'__dict__',
	]
	exception_null_key_words = [
		'list',
		'provided',	
		'slots',	
	]
	with pytest.raises(DunderDecoratorException) as exception_info:
		test[0] = 3
	assert exception_info.value.message == 'indexable'
	for key_word in exception_key_words:
		assert key_word in str(exception_info.value)
	for key_word in exception_null_key_words:
		assert key_word not in str(exception_info.value)

def test_dunder_setitem_indexing_has_iterable_attr_exception():
	@dunder_setitem(attr='a')
	class Test(object):

		def __init__(
				self,
				a: int,
				b: List,
		) -> None:
			self.a = a
			self.b = b
	test = Test(1, [1, 2, 3])
	exception_key_words = [
		'Attribute',
		'belonging',
		'indexable',
		'attr',
		'name',
		'owned',
		'without',
		'parameters',
		'__dict__',
		'list',
		'provided',
	]
	exception_null_key_words = [
		'slots',	
	]
	with pytest.raises(DunderDecoratorException) as exception_info:
		test[0] = 3
	assert exception_info.value.message == 'indexable'
	for key_word in exception_key_words:
		assert key_word in str(exception_info.value)
	
def test_dunder_setitem_indexing_with_slots_exception():
	@dunder_setitem(attr='a')
	class Test(object):
		__slots__ = ('a',)

		def __init__(
				self,
				a: int,
		) -> None:
			self.a = a
	test = Test(1)
	exception_key_words = [
		'Attribute',
		'belonging',
		'indexable',
		'attr',
		'name',
		'owned',
		'slots',	
		'True',
	]
	exception_null_key_words = [
		'without',
		'parameters',
		'__dict__',
		'list',
		'provided',	
	]
	with pytest.raises(DunderDecoratorException) as exception_info:
		test[0] = 3
	assert exception_info.value.message == 'indexable'
	for key_word in exception_key_words:
		assert key_word in str(exception_info.value)
	for key_word in exception_null_key_words:
		assert key_word not in str(exception_info.value)

def test_dunder_setitem_indexing_with_slots_and_iterable_attr_exception():
	@dunder_setitem(attr='a')
	class Test(object):
		__slots__ = ('a', 'b', 'c',)

		def __init__(
				self,
				a: int,
				b: List,
				c: List,
		) -> None:
			self.a = a
			self.b = b
			self.c = c
	test = Test(1, [1, 2, 3], [4, 5, 6])
	exception_key_words = [
		'Attribute',
		'belonging',
		'indexable',
		'attr',
		'name',
		'owned',
		'slots',
		'list',
		'provided',
		'[\'b\', \'c\']',
	]
	exception_null_key_words = [
		'parameters',
		'__dict__',	
		'without',
	]
	with pytest.raises(DunderDecoratorException) as exception_info:
		test[0] = 3
	assert exception_info.value.message == 'indexable'
	for key_word in exception_key_words:
		assert key_word in str(exception_info.value)
	for key_word in exception_null_key_words:
		assert key_word not in str(exception_info.value)

def test_dunder_key_not_hashable_exception():
	@dunder_setitem(attr='a')
	class Test(object):

		def __init__(
				self,
				a: Dict,
		) -> None:
			self.a = a
	test = Test({'a' : 1})
	exception_key_words = [
		'Provided',
		'is',
		'of',
		'type',
		'not',
		'hashable',
	]
	with pytest.raises(DunderDecoratorException) as exception_info:
		test[[1, 2, 3]] = 3
	assert exception_info.value.message == 'key_not_hashable'
	for key_word in exception_key_words:
		assert key_word in str(exception_info.value)

def test_dunder_setitem_dict_exception():
	@dunder_setitem
	class Test(object):
		__slots__ = ('a',)
		def __init__(
				self,
				a: Dict,
		) -> None:
			self.a = a
	test = Test({'a' : 1})
	exception_key_words = [
		'has',
		'no',
		'attribute',
		'__dict__',
		'Consider',
		'slots',
		'True',
	]
	with pytest.raises(DunderDecoratorException) as exception_info:
		test['a'] = [1, 2, 3]
	assert exception_info.value.message == ('dict', 'setitem')
	for key_word in exception_key_words:
		assert key_word in str(exception_info.value)

def test_dunder_setitem_slots_exception():
	@dunder_setitem(slots=True)
	class Test(object):
		def __init__(
				self,
				a: Dict,
		) -> None:
			self.a = a
	test = Test({'a' : 1})
	exception_key_words = [
		'parameters',
		'Consider',
		'__slots__',
	]
	with pytest.raises(DunderDecoratorException) as exception_info:
		test['a'] = [1, 2, 3]
	assert exception_info.value.message == ('slots', 'setitem')
	for key_word in exception_key_words:
		assert key_word in str(exception_info.value)

def test_dunder_getitem_dict_exception():
	@dunder_getitem
	class Test(object):
		__slots__ = ('a',)
		def __init__(
				self,
				a: Dict,
		) -> None:
			self.a = a
	test = Test({'a' : 1})
	exception_key_words = [
		'has',
		'no',
		'attribute',
		'Consider',
		'__dict__',
	]
	with pytest.raises(DunderDecoratorException) as exception_info:
		x = test['a']
	assert exception_info.value.message == ('dict', 'getitem')
	for key_word in exception_key_words:
		assert key_word in str(exception_info.value)

def test_dunder_getitem():
	@dunder_getitem
	class Test(object):
		def __init__(
				self,
				a: int,
				b: int,
				c: int,
		) -> None:
			self.a = a
			self.b = b
			self.c = c
	test = Test(1, 2, 3)
	assert (
		[test['a'], test['b'], test['c']] ==
		[1, 2, 3]
	)

def test_dunder_getitem_slots():
	@dunder_getitem(slots=True)
	class Test(object):
		__slots__ = ('a', 'b', 'c')
		def __init__(
				self,
				a: int,
				b: int,
				c: int,
		) -> None:
			self.a = a
			self.b = b
			self.c = c
	test = Test(1, 2, 3)
	assert (
		[test['a'], test['b'], test['c']] ==
		[1, 2, 3]
	)

def test_dunder_getitem_with_attr():
	@dunder_getitem(attr='a')
	class Test(object):
		def __init__(
				self,
				a: List,
		) -> None:
			self.a = a
	test = Test([1, 2, 3])
	assert (
		[test[0], test[1], test[2]] ==
		[1, 2, 3]
	)

def test_dunder_getitem_slots():
	@dunder_getitem(slots=True)
	class Test(object):
		__slots__ = ('a', 'b', 'c')
		def __init__(
				self,
				a: int,
				b: int,
				c: int,
		) -> None:
			self.a = a
			self.b = b
			self.c = c
	test = Test(1, 2, 3)
	assert (
		[test['a'], test['b'], test['c']] ==
		[1, 2, 3]
	)
		
def test_dunder_missing():
	@dunder_getitem
	@dunder_missing(default_value=1.0)
	class Test(object):
		def __init__(
				self,
				a: int,
				b: int,
				c: int,
		) -> None:
			self.a = a
			self.b = b
			self.c = c
	test = Test(1, 2, 3)
	test['d']
	assert test.d == 1.0 





























