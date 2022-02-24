// Transcrypt'ed from Python, 2020-02-27 10:26:16
var heapq = {};
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as __module_heapq__ from './heapq.js';
__nest__ (heapq, '', __module_heapq__);
var __name__ = 'chdiff';
export var MOVE = 0;
export var INSERT = 1;
export var DELETE = 2;
export var max_matches = 30;
export var max_del_chunks = 80;
export var min_del_chunk_len = 8;
export var greedy_hash_words = 2;
export var compute_edit_list = function (s1, s2) {
	var idx = make_index_tichy (s2);
	return edit_diff_tichy (s1, s2, idx);
};
export var fast_compute_edit_list = function (s1, s2) {
	var __left0__ = tuple ([len (s1), len (s2)]);
	var l1 = __left0__ [0];
	var l2 = __left0__ [1];
	var m = min (l1, l2);
	var j = 0;
	while (j < m && s1 [j] == s2 [j]) {
		j++;
	}
	var initial_move = (j == 0 ? null : tuple ([MOVE, 0, 0, j]));
	var k = 0;
	while (k < m - j && s1 [(l1 - k) - 1] == s2 [(l2 - k) - 1]) {
		k++;
	}
	var final_move = (k == 0 ? null : tuple ([MOVE, l1 - k, l2 - k, k]));
	var idx = make_index_tichy (s2.__getslice__ (j, l2 - k, 1));
	var intermediate = edit_diff_tichy (s1.__getslice__ (j, l1 - k, 1), s2.__getslice__ (j, l2 - k, 1), idx);
	var new_intermediate = (function () {
		var __accu0__ = [];
		for (var [m, i1, i2, l] of intermediate) {
			__accu0__.append (tuple ([m, i1 + j, i2 + j, l]));
		}
		return __accu0__;
	}) ();
	return tuple ([initial_move, new_intermediate, final_move]);
};
export var quality = function (l, i1, len1, i2, len2) {
	return (1.0 * l) / min (len1, len2) - 0.3 * abs (i1 / (1.0 * len1) - i2 / (1.0 * len2));
};
export var make_index2 = function (words) {
	var index = dict ({});
	for (var i = 0; i < len (words) - 1; i++) {
		if (__in__ (tuple ([words [i], words [i + 1]]), index)) {
			index.__getitem__ ([words [i], words [i + 1]]).append (i);
		}
		else {
			index.__setitem__ ([words [i], words [i + 1]], [i]);
		}
	}
	var todel = [];
	for (var [wp, l] of index.py_items ()) {
		if (len (l) > max_matches) {
			todel.append (wp);
		}
	}
	for (var wp of todel) {
		delete index [wp];
	}
	return index;
};
export var make_index3 = function (words) {
	var index = dict ({});
	for (var i = 0; i < len (words) - 2; i++) {
		if (__in__ (tuple ([words [i], words [i + 1], words [i + 2]]), index)) {
			index.__getitem__ ([words [i], words [i + 1], words [i + 2]]).append (i);
		}
		else {
			index.__setitem__ ([words [i], words [i + 1], words [i + 2]], [i]);
		}
	}
	var todel = [];
	for (var [wp, l] of index.py_items ()) {
		if (len (l) > max_matches) {
			todel.append (wp);
		}
	}
	for (var wp of todel) {
		delete index [wp];
	}
	return index;
};
export var make_index4 = function (words) {
	var index = dict ({});
	for (var i = 0; i < len (words) - 3; i++) {
		if (__in__ (tuple ([words [i], words [i + 1], words [i + 2], words [i + 3]]), index)) {
			index.__getitem__ ([words [i], words [i + 1], words [i + 2], words [i + 3]]).append (i);
		}
		else {
			index.__setitem__ ([words [i], words [i + 1], words [i + 2], words [i + 3]], [i]);
		}
	}
	var todel = [];
	for (var [wp, l] of index.py_items ()) {
		if (len (l) > max_matches) {
			todel.append (wp);
		}
	}
	for (var wp of todel) {
		delete index [wp];
	}
	return index;
};
export var make_index = function (words) {
	if (greedy_hash_words == 2) {
		return make_index2 (words);
	}
	else if (greedy_hash_words == 3) {
		return make_index3 (words);
	}
	else {
		return make_index4 (words);
	}
};
export var make_index_tichy = function (words) {
	return make_index2 (words);
};
export var edit_diff_greedy = function (words1, words2, index2) {
	var matches = [];
	var len1 = len (words1);
	var len2 = len (words2);
	var prev_matches = [];
	for (var i1 = 0; i1 < (len1 - greedy_hash_words) + 1; i1++) {
		if (greedy_hash_words == 2) {
			var ws = tuple ([words1 [i1], words1 [i1 + 1]]);
		}
		else if (greedy_hash_words == 3) {
			var ws = tuple ([words1 [i1], words1 [i1 + 1], words1 [i1 + 2]]);
		}
		else {
			var ws = tuple ([words1 [i1], words1 [i1 + 1], words1 [i1 + 2], words1 [i1 + 3]]);
		}
		if (__in__ (ws, index2)) {
			var new_matches = index2 [ws];
			for (var i2 of new_matches) {
				if (!__in__ (i2 - 1, prev_matches)) {
					var l = 2;
					while (i1 + l < len1 && i2 + l < len2 && words1 [i1 + l] == words2 [i2 + l]) {
						l++;
					}
					var q = quality (l, i1, len1, i2, len2);
					matches.append (tuple ([10.0 - q, tuple ([l, i1, i2])]));
				}
			}
			var prev_matches = new_matches;
		}
		else {
			var prev_matches = [];
		}
	}
	var matched1 = [0] * len (words1);
	var matched2 = [0] * len (words2);
	var match_id = 0;
	var diff = [];
	heapq.heapify (matches);
	while (matches != []) {
		var __left0__ = heapq.heappop (matches);
		var q = __left0__ [0];
		var l = __left0__ [1][0];
		var i1 = __left0__ [1][1];
		var i2 = __left0__ [1][2];
		if (!(matched1 [i1] || matched2 [i2])) {
			if (!(matched1 [(i1 + l) - 1] || matched2 [(i2 + l) - 1])) {
				diff.append (tuple ([MOVE, i1, i2, l]));
				match_id++;
				for (var j = 0; j < l; j++) {
					matched1 [i1 + j] = match_id;
					matched2 [i2 + j] = match_id;
				}
			}
			else {
				var j = l - 2;
				while (matched1 [i1 + j] || matched2 [i2 + j]) {
					j--;
				}
				var l = j + 1;
				if (l >= greedy_hash_words) {
					var q = quality (l, i1, len1, i2, len2);
					heapq.heappush (matches, tuple ([10.0 - q, tuple ([l, i1, i2])]));
				}
			}
		}
		else if (!(matched1 [(i1 + l) - 1] || matched2 [(i2 + l) - 1])) {
			var j = 1;
			while (matched1 [i1 + j] || matched2 [i2 + j]) {
				j++;
			}
			var l = l - j;
			if (l >= greedy_hash_words) {
				var q = quality (l, i1 + j, len1, i2 + j, len2);
				heapq.heappush (matches, tuple ([10.0 - q, tuple ([l, i1 + j, i2 + j])]));
			}
		}
		else if (matched1 [i1] != matched1 [(i1 + l) - 1] && matched2 [i2] != matched2 [(i2 + l) - 1]) {
			var j = 1;
			while (j < l - 1 && (matched1 [i1 + j] || matched2 [i2 + j])) {
				j++;
			}
			if (j < l - 1) {
				var k = j + 1;
				while (k < l - 1 && !(matched1 [i1 + k] || matched2 [i2 + k])) {
					k++;
				}
				var l = k - j;
				if (l >= greedy_hash_words) {
					var q = quality (l, i1 + j, len1, i2 + j, len2);
					heapq.heappush (matches, tuple ([10.0 - q, tuple ([l, i1 + j, i2 + j])]));
				}
			}
		}
	}
	var in_string = false;
	for (var [i1, m1] of enumerate (matched1)) {
		if (!(m1) && !(in_string)) {
			var unm_start = i1;
			var in_string = true;
		}
		if (m1 && in_string) {
			if (i1 > unm_start) {
				diff.append (tuple ([DELETE, unm_start, unm_start, i1 - unm_start]));
			}
			var in_string = false;
		}
	}
	if (in_string && len1 > unm_start) {
		diff.append (tuple ([DELETE, unm_start, unm_start, len1 - unm_start]));
	}
	var in_string = false;
	for (var [i2, m2] of enumerate (matched2)) {
		if (!(m2) && !(in_string)) {
			var unm_start = i2;
			var in_string = true;
		}
		if (m2 && in_string) {
			if (i2 > unm_start) {
				diff.append (tuple ([INSERT, unm_start, unm_start, i2 - unm_start]));
			}
			var in_string = false;
		}
	}
	if (in_string && len2 > unm_start) {
		diff.append (tuple ([INSERT, unm_start, unm_start, len2 - unm_start]));
	}
	return diff;
};
export var text_to_chunk = function (label_data, text) {
	var chunk = text.py_split ();
	var chunk_label = tuple ([0, len (chunk), label_data]);
	return tuple ([chunk, [chunk_label], [], []]);
};
export var revision_prepare = function (text) {
	return text.py_split ();
};
export var edit_diff_tichy = function (w1, w2, idx2) {
	var words1 = w2;
	var words2 = w1;
	var index1 = idx2;
	var len1 = len (words1);
	var len2 = len (words2);
	var matched1 = [];
	for (var val = 0; val < len (words1); val++) {
		matched1.append (false);
	}
	var diff = [];
	var i2 = 0;
	var first_unmatched_2 = 0;
	while (i2 < len2 - 1) {
		var max_quality = null;
		var ws = tuple ([words2 [i2], words2 [i2 + 1]]);
		if (__in__ (ws, index1)) {
			for (var i1 of index1 [ws]) {
				if (!(matched1 [i1] || matched1 [i1 + 1])) {
					var l = 2;
					while (i1 + l < len1 && i2 + l < len2 && !(matched1 [i1 + l]) && words1 [i1 + l] == words2 [i2 + l]) {
						l++;
					}
					var q = quality (l, i1, len1, i2, len2);
					if (max_quality == null || q > max_quality) {
						var max_quality = q;
						var best_match = tuple ([l, i1]);
					}
				}
			}
			if (max_quality != null) {
				if (i2 > first_unmatched_2) {
					diff.append (tuple ([DELETE, first_unmatched_2, first_unmatched_2, i2 - first_unmatched_2]));
				}
				var __left0__ = best_match;
				var l_m = __left0__ [0];
				var i1_m = __left0__ [1];
				diff.append (tuple ([MOVE, i2, i1_m, l_m]));
				for (var j = 0; j < l_m; j++) {
					matched1 [i1_m + j] = true;
				}
				i2 += l_m;
				var first_unmatched_2 = i2;
			}
			else {
				i2++;
			}
		}
		else {
			i2++;
		}
	}
	if (len2 > first_unmatched_2) {
		diff.append (tuple ([DELETE, first_unmatched_2, first_unmatched_2, len2 - first_unmatched_2]));
	}
	var in_string = false;
	for (var [i1, m1] of enumerate (matched1)) {
		if (!(m1) && !(in_string)) {
			var unm_start = i1;
			var in_string = true;
		}
		if (m1 && in_string) {
			diff.append (tuple ([INSERT, unm_start, unm_start, i1 - unm_start]));
			var in_string = false;
		}
	}
	if (in_string) {
		diff.append (tuple ([INSERT, unm_start, unm_start, len1 - unm_start]));
	}
	return diff;
};
export var print_edit_diff = function (diff_cmds) {
	for (var [cmd, i1, i2, l] of diff_cmds) {
		if (cmd == MOVE) {
			print ((((('MOVE   : ' + str (i1)) + ' -> ') + str (i2)) + ', L= ') + str (l));
		}
		if (cmd == DELETE) {
			print ((('DELETE : ' + str (i1)) + ', L: ') + str (l));
		}
		if (cmd == INSERT) {
			print ((('INSERT : ' + str (i1)) + ', L: ') + str (l));
		}
	}
};
export var test_tichy = function (s1, s2) {
	var l1 = s1.py_split ();
	var l2 = s2.py_split ();
	var idx = make_index_tichy (l2);
	return edit_diff_tichy (l1, l2, idx);
};
export var test_greedy = function (s1, s2) {
	var l1 = s1.py_split ();
	var l2 = s2.py_split ();
	var idx = make_index2 (l2);
	return edit_diff_greedy (l1, l2, idx);
};

//# sourceMappingURL=chdiff.map