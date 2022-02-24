// Transcrypt'ed from Python, 2020-02-27 10:26:16
var math = {};
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import {Word} from './text_trust.word.js';
import {Edit} from './text_trust.edit.js';
import {Block} from './text_trust.block.js';
import * as __module_math__ from './math.js';
__nest__ (math, '', __module_math__);
var __name__ = 'text_trust.version';
export var Version =  __class__ ('Version', [object], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, word_list, edit_list, author_rep, constants) {
		self.word_list = word_list;
		self.edit_list = edit_list;
		self.author_rep = author_rep;
		self.constants = constants;
		self.trust_inheritance_const = constants [0];
		self.revision_const = constants [1];
		self.edge_effect_const = constants [2];
		self.block_list = self.compute_blocks ();
		self.apply_insertion_trust ();
		self.check_block_bound_changes ();
		self.apply_edge_effect ();
		self.apply_revision_effect ();
	});},
	get create_initial_version () {return __getcm__ (this, function (cls, text_list, initial_trust, constants) {
		var word_list = Word.create_list_words (text_list, (function () {
			var __accu0__ = [];
			for (var x = 0; x < len (text_list); x++) {
				__accu0__.append (initial_trust);
			}
			return __accu0__;
		}) ());
		var edit_list = [Edit (Edit.MOVE, 0, 0, len (word_list))];
		return cls (word_list, edit_list, initial_trust, constants);
	});},
	get create_next_version () {return __getcm__ (this, function (cls, prev_version, new_text, new_edits, author_rep) {
		var prev_word_list = prev_version.word_list;
		var new_word_list = Word.create_list_words (new_text, (function () {
			var __accu0__ = [];
			for (var x = 0; x < len (new_text); x++) {
				__accu0__.append (-(1));
			}
			return __accu0__;
		}) ());
		for (var edit of new_edits) {
			if (edit.edit_type == Edit.MOVE) {
				for (var word_iter = 0; word_iter < edit.lengthr; word_iter++) {
					new_word_list [edit.destination + word_iter] = prev_word_list [edit.origin + word_iter].clone ();
				}
			}
		}
		return cls (new_word_list, new_edits, author_rep, prev_version.constants);
	});},
	get compute_blocks () {return __get__ (this, function (self) {
		var present_edits = (function () {
			var __accu0__ = [];
			for (var edit of self.edit_list) {
				if (edit.destination >= 0) {
					__accu0__.append (edit);
				}
			}
			return __accu0__;
		}) ();
		var present_edits = sorted (present_edits, __kwargtrans__ ({key: (function __lambda__ (edit) {
			return edit.destination;
		})}));
		var version_blocks = [];
		for (var edit of present_edits) {
			var start_words = edit.destination;
			var end_words = start_words + edit.lengthr;
			version_blocks.append (Block (self.word_list.__getslice__ (start_words, end_words, 1), edit));
		}
		return version_blocks;
	});},
	get apply_insertion_trust () {return __get__ (this, function (self) {
		for (var block of self.block_list) {
			if (block.edit.edit_type == Edit.INSERT) {
				for (var word of block.words) {
					word.trust = self.author_rep * self.trust_inheritance_const;
				}
			}
		}
	});},
	get check_block_bound_changes () {return __get__ (this, function (self) {
		for (var block of self.block_list) {
			if (block.edit.edit_type == Edit.MOVE) {
				if (block.edit.origin == block.edit.destination && block.edit.destination == 0) {
					block.left_bound_change = false;
				}
				else {
					block.left_bound_change = true;
				}
				if (block.edit.origin == block.edit.destination && block.edit.destination == len (self.word_list) - block.edit.lengthr) {
					block.right_bound_change = false;
				}
				else {
					block.right_bound_change = true;
				}
			}
		}
	});},
	get apply_edge_effect () {return __get__ (this, function (self) {
		for (var block of self.block_list) {
			if (block.left_bound_change) {
				for (var [word_iter, word] of enumerate (block.words)) {
					var k = word_iter;
					var new_word_trust_left = word.trust + (self.trust_inheritance_const * self.author_rep - word.trust) * math.exp (-(self.edge_effect_const) * k);
					word.trust = new_word_trust_left;
				}
			}
			if (block.right_bound_change) {
				for (var [word_iter, word] of enumerate (block.words)) {
					var k_bar = (len (block.words) - word_iter) - 1;
					var new_word_trust_right = word.trust + (self.trust_inheritance_const * self.author_rep - word.trust) * math.exp (-(self.edge_effect_const) * k_bar);
					word.trust = new_word_trust_right;
				}
			}
		}
	});},
	get apply_revision_effect () {return __get__ (this, function (self) {
		for (var word of self.word_list) {
			if (word.trust < self.author_rep) {
				word.trust = word.trust + (self.author_rep - word.trust) * self.revision_const;
			}
		}
	});}
});

//# sourceMappingURL=text_trust.version.map