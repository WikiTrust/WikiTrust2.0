// Transcrypt'ed from Python, 2020-03-16 11:49:27
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import {edit_diff_greedy, make_index2} from './wikitrust_algorithms.text_diff.chdiff.js';
import {Edit} from './wikitrust_algorithms.text_diff.edit.js';
import {Author} from './wikitrust_algorithms.author_reputation.author.js';
import {Version} from './wikitrust_algorithms.author_reputation.version.js';
import {Callable, Dict, List, Sequence, Tuple} from './typing.js';
var __name__ = 'wikitrust_algorithms.author_reputation.article';
export var Article =  __class__ ('Article', [object], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, max_judgement_dist, scaling_constant, scaling_function) {
		self.versions = [];
		self.max_judgement_dist = max_judgement_dist;
		self.scaling_constant = scaling_constant;
		self.scaling_function = scaling_function;
	});},
	get add_new_version () {return __get__ (this, function (self, new_version) {
		self.versions.append (new_version);
		var reference_version_range = range (max ((len (self.versions) - self.max_judgement_dist) - 1, 0), len (self.versions) - 2);
		for (var reference_version_iter of reference_version_range) {
			var reference_version = self.versions [reference_version_iter];
			var judged_version = self.versions [reference_version_iter + 1];
			if (Author.check_same_author (judged_version.author, new_version.author)) {
				// pass;
			}
			else {
				var reputation_change = ((self.scaling_constant * self.compute_edit_distance (reference_version, judged_version)) * self.compute_edit_quality (reference_version, judged_version, new_version)) * self.scaling_function (new_version.author.get_author_rep ());
				judged_version.author.set_author_rep (judged_version.author.get_author_rep () + reputation_change);
			}
		}
	});},
	get compute_edit_distance () {return __getcm__ (this, function (cls, version_1, version_2) {
		var split_version_1 = version_1.text.py_split ();
		var split_version_2 = version_2.text.py_split ();
		var edit_index = make_index2 (split_version_2);
		var edit_list_tuples = edit_diff_greedy (split_version_1, split_version_2, edit_index);
		var edit_list = (function () {
			var __accu0__ = [];
			for (var edit_tuple of edit_list_tuples) {
				__accu0__.append (Edit.edit_tuple_constructor (edit_tuple));
			}
			return __accu0__;
		}) ();
		var insertion_total = 0;
		var deletion_total = 0;
		for (var edit of edit_list) {
			if (edit.edit_type == Edit.INSERT) {
				insertion_total += edit.length;
			}
			else if (edit.edit_type == Edit.DELETE) {
				deletion_total += edit.length;
			}
		}
		var move_total = 0;
		var move_list = (function () {
			var __accu0__ = [];
			for (var edit of edit_list) {
				if (edit.edit_type == Edit.MOVE) {
					__accu0__.append (edit);
				}
			}
			return __accu0__;
		}) ();
		var moves_origin_list = sorted (move_list, __kwargtrans__ ({key: (function __lambda__ (edit) {
			return edit.origin;
		})}));
		var moves_destination_list = sorted (move_list, __kwargtrans__ ({key: (function __lambda__ (edit) {
			return edit.destination;
		})})).__getslice__ (0, null, -(1));
		var origin_valid_move_list = [];
		for (var [move_a_iter, move_a] of enumerate (moves_origin_list)) {
			for (var move_b of moves_origin_list.__getslice__ (move_a_iter + 1, null, 1)) {
				origin_valid_move_list.append (tuple ([move_a, move_b]));
			}
		}
		var destination_valid_move_list = [];
		for (var [move_a_iter, move_a] of enumerate (moves_destination_list)) {
			for (var move_b of moves_destination_list.__getslice__ (move_a_iter + 1, null, 1)) {
				destination_valid_move_list.append (tuple ([move_a, move_b]));
			}
		}
		var crossed_move_list = [];
		for (var move_pair of origin_valid_move_list) {
			if (__in__ (move_pair, destination_valid_move_list)) {
				crossed_move_list.append (move_pair);
			}
		}
		for (var crossed_move of crossed_move_list) {
			move_total += crossed_move [0].length * crossed_move [1].length;
		}
		var distance = (float (max (insertion_total, deletion_total)) - float (0.5 * max (insertion_total, deletion_total))) + float (move_total);
		return distance;
	});},
	get compute_edit_quality () {return __getcm__ (this, function (cls, version_1, version_2, version_3) {
		if (cls.compute_edit_distance (version_1, version_2) == 0) {
			return float (0);
		}
		var edit_quality = float ((cls.compute_edit_distance (version_1, version_3) - cls.compute_edit_distance (version_2, version_3)) / cls.compute_edit_distance (version_1, version_2));
		return edit_quality;
	});}
});

//# sourceMappingURL=wikitrust_algorithms.author_reputation.article.map