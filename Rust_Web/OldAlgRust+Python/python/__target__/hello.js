// Transcrypt'ed from Python, 2020-02-27 10:26:15
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import {print_edit_diff, test_greedy, test_tichy} from './chdiff.js';
import {Word} from './text_trust.word.js';
import {Edit} from './text_trust.edit.js';
import {Block} from './text_trust.block.js';
import {Version} from './text_trust.version.js';
var __name__ = '__main__';
export var getTrustExample = function (test_strings) {
	var initial_trust = 1;
	var test_trusts = [10, 7, 10, 20];
	var trust_inheritance_const = 0.5;
	var revision_const = 0.1;
	var edge_effect_const = 2;
	var constants = tuple ([trust_inheritance_const, revision_const, edge_effect_const]);
	print ('Initial String: ' + str (test_strings [0]));
	for (var [string_iter, string] of enumerate (test_strings)) {
		print ((('String ' + str (string_iter)) + ': ') + string);
	}
	print ('Version 1:\n');
	print (('Initial Trust: ' + str (initial_trust)) + '\n');
	var text_list = test_strings [0].py_split ();
	print (text_list [0]);
	var version_list = [];
	var ver = Version.create_initial_version (text_list, initial_trust, constants);
	version_list.append (ver);
	print ('Block List:');
	for (var string_iter = 0; string_iter < len (test_strings) - 1; string_iter++) {
		print ('Version ' + str (string_iter + 2));
		print ('Author Reputation: ' + str (test_trusts [string_iter]));
		var diff_list = test_tichy (test_strings [string_iter], test_strings [string_iter + 1]);
		console.log (diff_list);
		var edit_list = (function () {
			var __accu0__ = [];
			for (var edit of diff_list) {
				__accu0__.append (Edit.edit_tuple_constructor (edit));
			}
			return __accu0__;
		}) ();
		var text_list = test_strings [string_iter + 1].py_split ();
		var ver = Version.create_next_version (ver, text_list, edit_list, test_trusts [string_iter]);
		version_list.append (ver);
		for (var word of ver.word_list) {
			console.log (str (word));
		}
		print ('Block List:\n');
		print (''.join ((function () {
			var __accu0__ = [];
			for (var block of ver.block_list) {
				__accu0__.append (str (block) + '\n');
			}
			return __accu0__;
		}) ()));
		print ('\n');
	}
	var output = [];
	for (var version of version_list) {
		var words = [];
		for (var word of version.word_list) {
			words.append (word);
		}
		output.append (words);
	}
	return output;
};

//# sourceMappingURL=hello.map