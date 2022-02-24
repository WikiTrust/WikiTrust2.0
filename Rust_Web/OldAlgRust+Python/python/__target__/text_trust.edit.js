// Transcrypt'ed from Python, 2020-02-27 10:26:16
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
var __name__ = 'text_trust.edit';
export var Edit =  __class__ ('Edit', [object], {
	__module__: __name__,
	MOVE: 0,
	INSERT: 1,
	DELETE: 2,
	get __init__ () {return __get__ (this, function (self, edit_typey, origin, destination, lengthry) {
		self.edit_type = edit_typey;
		self.origin = origin;
		self.destination = destination;
		self.lengthr = lengthry;
	});},
	get __str__ () {return __get__ (this, function (self) {
		if (self.edit_type == self.MOVE) {
			return __mod__ ('MOVE   : %d -> %d, L= %d', tuple ([self.origin, self.destination, self.lengthr]));
		}
		if (self.edit_type == self.DELETE) {
			return __mod__ ('DELETE : %d, L: %d', tuple ([self.origin, self.lengthr]));
		}
		if (self.edit_type == self.INSERT) {
			return __mod__ ('INSERT : %d, L: %d', tuple ([self.destination, self.lengthr]));
		}
		var __except0__ = RuntimeError (__mod__ ('Invalid Edit type: "%s"', self.edit_type));
		__except0__.__cause__ = null;
		throw __except0__;
	});},
	get edit_tuple_constructor () {return __getcm__ (this, function (cls, edit_info) {
		if (edit_info [0] == cls.MOVE) {
			return cls (edit_info [0], edit_info [1], edit_info [2], edit_info [3]);
		}
		if (edit_info [0] == cls.INSERT) {
			return cls (edit_info [0], -(1), edit_info [2], edit_info [3]);
		}
		if (edit_info [0] == cls.DELETE) {
			return cls (edit_info [0], edit_info [1], -(1), edit_info [3]);
		}
		var __except0__ = ValueError (__mod__ ('Invalid Edit type: "%s"', edit_info [0]));
		__except0__.__cause__ = null;
		throw __except0__;
	});}
});

//# sourceMappingURL=text_trust.edit.map