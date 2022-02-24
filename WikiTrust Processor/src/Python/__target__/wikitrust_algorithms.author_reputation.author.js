// Transcrypt'ed from Python, 2020-03-16 11:49:26
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
var __name__ = 'wikitrust_algorithms.author_reputation.author';
export var Author =  __class__ ('Author', [object], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, author_id, starting_reputation, maximum_reputation) {
		self.author_id = author_id;
		self.reputation = starting_reputation;
		self.maximum_reputation = maximum_reputation;
	});},
	get __str__ () {return __get__ (this, function (self) {
		return (('Author ID: ' + str (self.author_id)) + '    Reputation:') + str (self.reputation);
	});},
	get get_author_rep () {return __get__ (this, function (self) {
		return self.reputation;
	});},
	get set_author_rep () {return __get__ (this, function (self, new_author_rep) {
		self.reputation = min (max (new_author_rep, 0), self.maximum_reputation);
	});},
	get check_same_author () {return __getcm__ (this, function (cls, author_1, author_2) {
		if (author_1.author_id == author_2.author_id) {
			return true;
		}
		return false;
	});}
});

//# sourceMappingURL=wikitrust_algorithms.author_reputation.author.map