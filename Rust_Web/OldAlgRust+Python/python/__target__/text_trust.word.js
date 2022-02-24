// Transcrypt'ed from Python, 2020-02-27 10:26:16
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
var __name__ = 'text_trust.word';
export var Word =  __class__ ('Word', [object], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, text, trust) {
		self.text = text;
		self.trust = trust;
	});},
	get __str__ () {return __get__ (this, function (self) {
		return ((('(' + self.text) + ',') + self.trust) + ')';
	});},
	get create_list_words () {return __getcm__ (this, function (cls, text_list, trust_list) {
		if (len (text_list) != len (trust_list)) {
			var __except0__ = ValueError (__mod__ ('Length of text_list does not equal length of trust_list: %d != %d', tuple ([len (text_list), len (trust_list)])));
			__except0__.__cause__ = null;
			throw __except0__;
		}
		var words_list = (function () {
			var __accu0__ = [];
			for (var list_iter = 0; list_iter < len (text_list); list_iter++) {
				__accu0__.append (Word (text_list [list_iter], trust_list [list_iter]));
			}
			return __accu0__;
		}) ();
		return words_list;
	});},
	get clone () {return __get__ (this, function (self) {
		return Word (self.text, self.trust);
	});}
});

//# sourceMappingURL=text_trust.word.map