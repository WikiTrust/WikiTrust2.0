// Transcrypt'ed from Python, 2020-03-16 11:49:26
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
var __name__ = 'heapq';
export var __about__ = 'Heap queues\n\n[explanation by François Pinard]\n\nHeaps are arrays for which a[k] <= a[2*k+1] and a[k] <= a[2*k+2] for\nall k, counting elements from 0.  For the sake of comparison,\nnon-existing elements are considered to be infinite.  The interesting\nproperty of a heap is that a[0] is always its smallest element.\n\nThe strange invariant above is meant to be an efficient memory\nrepresentation for a tournament.  The numbers below are `k\', not a[k]:\n\n                                   0\n\n                  1                                 2\n\n          3               4                5               6\n\n      7       8       9       10      11      12      13      14\n\n    15 16   17 18   19 20   21 22   23 24   25 26   27 28   29 30\n\n\nIn the tree above, each cell `k\' is topping `2*k+1\' and `2*k+2\'.  In\na usual binary tournament we see in sports, each cell is the winner\nover the two cells it tops, and we can trace the winner down the tree\nto see all opponents s/he had.  However, in many computer applications\nof such tournaments, we do not need to trace the history of a winner.\nTo be more memory efficient, when a winner is promoted, we try to\nreplace it by something else at a lower level, and the rule becomes\nthat a cell and the two cells it tops contain three different items,\nbut the top cell "wins" over the two topped cells.\n\nIf this heap invariant is protected at all time, index 0 is clearly\nthe overall winner.  The simplest algorithmic way to remove it and\nfind the "next" winner is to move some loser (let\'s say cell 30 in the\ndiagram above) into the 0 position, and then percolate this new 0 down\nthe tree, exchanging values, until the invariant is re-established.\nThis is clearly logarithmic on the total number of items in the tree.\nBy iterating over all items, you get an O(n ln n) sort.\n\nA nice feature of this sort is that you can efficiently insert new\nitems while the sort is going on, provided that the inserted items are\nnot "better" than the last 0\'th element you extracted.  This is\nespecially useful in simulation contexts, where the tree holds all\nincoming events, and the "win" condition means the smallest scheduled\ntime.  When an event schedule other events for execution, they are\nscheduled into the future, so they can easily go into the heap.  So, a\nheap is a good structure for implementing schedulers (this is what I\nused for my MIDI sequencer :-).\n\nVarious structures for implementing schedulers have been extensively\nstudied, and heaps are good for this, as they are reasonably speedy,\nthe speed is almost constant, and the worst case is not much different\nthan the average case.  However, there are other representations which\nare more efficient overall, yet the worst cases might be terrible.\n\nHeaps are also very useful in big disk sorts.  You most probably all\nknow that a big sort implies producing "runs" (which are pre-sorted\nsequences, which size is usually related to the amount of CPU memory),\nfollowed by a merging passes for these runs, which merging is often\nvery cleverly organised[1].  It is very important that the initial\nsort produces the longest runs possible.  Tournaments are a good way\nto that.  If, using all the memory available to hold a tournament, you\nreplace and percolate items that happen to fit the current run, you\'ll\nproduce runs which are twice the size of the memory for random input,\nand much better for input fuzzily ordered.\n\nMoreover, if you output the 0\'th item on disk and get an input which\nmay not fit in the current tournament (because the value "wins" over\nthe last output value), it cannot fit in the heap, so the size of the\nheap decreases.  The freed memory could be cleverly reused immediately\nfor progressively building a second heap, which grows at exactly the\nsame rate the first heap is melting.  When the first heap completely\nvanishes, you switch heaps and start a new run.  Clever and quite\neffective!\n\nIn a word, heaps are useful memory structures to know.  I use them in\na few applications, and I think it is good to keep a `heap\' module\naround. :-)\n\n--------------------\n[1] The disk balancing algorithms which are current, nowadays, are\nmore annoying than clever, and this is a consequence of the seeking\ncapabilities of the disks.  On devices which cannot seek, like big\ntape drives, the story was quite different, and one had to be very\nclever to ensure (far in advance) that each tape movement will be the\nmost effective possible (that is, will best participate at\n"progressing" the merge).  Some tapes were even able to read\nbackwards, and this was also used to avoid the rewinding time.\nBelieve me, real good tape sorts were quite spectacular to watch!\nFrom all times, sorting has always been a Great Art! :-)\n';
export var __all__ = ['heappush', 'heappop', 'heapify', 'heapreplace', 'merge', 'nlargest', 'nsmallest', 'heappushpop'];
export var heappush = function (heap, item) {
	heap.append (item);
	_siftdown (heap, 0, len (heap) - 1);
};
export var heappop = function (heap) {
	var lastelt = heap.py_pop ();
	if (heap) {
		var returnitem = heap [0];
		heap [0] = lastelt;
		_siftup (heap, 0);
		return returnitem;
	}
	return lastelt;
};
export var heapreplace = function (heap, item) {
	var returnitem = heap [0];
	heap [0] = item;
	_siftup (heap, 0);
	return returnitem;
};
export var heappushpop = function (heap, item) {
	if (heap && heap [0] < item) {
		var __left0__ = tuple ([heap [0], item]);
		var item = __left0__ [0];
		heap [0] = __left0__ [1];
		_siftup (heap, 0);
	}
	return item;
};
export var heapify = function (x) {
	var n = len (x);
	for (var i of py_reversed (range (Math.floor (n / 2)))) {
		_siftup (x, i);
	}
};
export var _heappop_max = function (heap) {
	var lastelt = heap.py_pop ();
	if (heap) {
		var returnitem = heap [0];
		heap [0] = lastelt;
		_siftup_max (heap, 0);
		return returnitem;
	}
	return lastelt;
};
export var _heapreplace_max = function (heap, item) {
	var returnitem = heap [0];
	heap [0] = item;
	_siftup_max (heap, 0);
	return returnitem;
};
export var _heapify_max = function (x) {
	var n = len (x);
	for (var i of py_reversed (range (Math.floor (n / 2)))) {
		_siftup_max (x, i);
	}
};
export var _siftdown = function (heap, startpos, pos) {
	var newitem = heap [pos];
	while (pos > startpos) {
		var parentpos = pos - 1 >> 1;
		var parent = heap [parentpos];
		if (newitem < parent) {
			heap [pos] = parent;
			var pos = parentpos;
			continue;
		}
		break;
	}
	heap [pos] = newitem;
};
export var _siftup = function (heap, pos) {
	var endpos = len (heap);
	var startpos = pos;
	var newitem = heap [pos];
	var childpos = 2 * pos + 1;
	while (childpos < endpos) {
		var rightpos = childpos + 1;
		if (rightpos < endpos && !(heap [childpos] < heap [rightpos])) {
			var childpos = rightpos;
		}
		heap [pos] = heap [childpos];
		var pos = childpos;
		var childpos = 2 * pos + 1;
	}
	heap [pos] = newitem;
	_siftdown (heap, startpos, pos);
};
export var _siftdown_max = function (heap, startpos, pos) {
	var newitem = heap [pos];
	while (pos > startpos) {
		var parentpos = pos - 1 >> 1;
		var parent = heap [parentpos];
		if (parent < newitem) {
			heap [pos] = parent;
			var pos = parentpos;
			continue;
		}
		break;
	}
	heap [pos] = newitem;
};
export var _siftup_max = function (heap, pos) {
	var endpos = len (heap);
	var startpos = pos;
	var newitem = heap [pos];
	var childpos = 2 * pos + 1;
	while (childpos < endpos) {
		var rightpos = childpos + 1;
		if (rightpos < endpos && !(heap [rightpos] < heap [childpos])) {
			var childpos = rightpos;
		}
		heap [pos] = heap [childpos];
		var pos = childpos;
		var childpos = 2 * pos + 1;
	}
	heap [pos] = newitem;
	_siftdown_max (heap, startpos, pos);
};
export var merge = function* () {
	var key = null;
	var reverse = false;
	var iterables = tuple ([].slice.apply (arguments).slice (0));
	var h = [];
	var h_append = h.append;
	if (reverse) {
		var _heapify = _heapify_max;
		var _heappop = _heappop_max;
		var _heapreplace = _heapreplace_max;
		var direction = -(1);
	}
	else {
		var _heapify = heapify;
		var _heappop = heappop;
		var _heapreplace = heapreplace;
		var direction = 1;
	}
	if (key === null) {
		for (var [order, it] of enumerate (map (py_iter, iterables))) {
			try {
				var py_next = it.__next__;
				h_append ([py_next (), order * direction, py_next]);
			}
			catch (__except0__) {
				if (isinstance (__except0__, StopIteration)) {
					// pass;
				}
				else {
					throw __except0__;
				}
			}
		}
		_heapify (h);
		while (len (h) > 1) {
			try {
				while (true) {
					var __left0__ = h [0];
					var value = __left0__ [0];
					var order = __left0__ [1];
					var py_next = __left0__ [2];
					var s = __left0__;
					yield value;
					s [0] = py_next ();
					_heapreplace (h, s);
				}
			}
			catch (__except0__) {
				if (isinstance (__except0__, StopIteration)) {
					_heappop (h);
				}
				else {
					throw __except0__;
				}
			}
		}
		if (h) {
			var __left0__ = h [0];
			var value = __left0__ [0];
			var order = __left0__ [1];
			var py_next = __left0__ [2];
			yield value;
			yield* py_next.__self__;
		}
		return ;
	}
	for (var [order, it] of enumerate (map (py_iter, iterables))) {
		try {
			var py_next = it.__next__;
			var value = py_next ();
			h_append ([key (value), order * direction, value, py_next]);
		}
		catch (__except0__) {
			if (isinstance (__except0__, StopIteration)) {
				// pass;
			}
			else {
				throw __except0__;
			}
		}
	}
	_heapify (h);
	while (len (h) > 1) {
		try {
			while (true) {
				var __left0__ = h [0];
				var key_value = __left0__ [0];
				var order = __left0__ [1];
				var value = __left0__ [2];
				var py_next = __left0__ [3];
				var s = __left0__;
				yield value;
				var value = py_next ();
				s [0] = key (value);
				s [2] = value;
				_heapreplace (h, s);
			}
		}
		catch (__except0__) {
			if (isinstance (__except0__, StopIteration)) {
				_heappop (h);
			}
			else {
				throw __except0__;
			}
		}
	}
	if (h) {
		var __left0__ = h [0];
		var key_value = __left0__ [0];
		var order = __left0__ [1];
		var value = __left0__ [2];
		var py_next = __left0__ [3];
		yield value;
		yield* py_next.__self__;
	}
	};
export var nsmallest = function (n, iterable, key) {
	if (typeof key == 'undefined' || (key != null && key.hasOwnProperty ("__kwargtrans__"))) {;
		var key = null;
	};
	if (n == 1) {
		var it = py_iter (iterable);
		var sentinel = object ();
		if (key === null) {
			var result = min (it, __kwargtrans__ ({py_default: sentinel}));
		}
		else {
			var result = min (it, __kwargtrans__ ({py_default: sentinel, key: key}));
		}
		return (result === sentinel ? [] : [result]);
	}
	try {
		var size = len (iterable);
		try {
			if (n >= size) {
				return sorted (iterable, __kwargtrans__ ({key: key})).__getslice__ (0, n, 1);
			}
		}
		catch (__except0__) {
		}
	}
	catch (__except0__) {
		if (isinstance (__except0__, tuple ([py_TypeError, AttributeError]))) {
			// pass;
		}
		else {
			throw __except0__;
		}
	}
	if (key === null) {
		var it = py_iter (iterable);
		var result = (function () {
			var __accu0__ = [];
			for (var [i, elem] of zip (range (n), it)) {
				__accu0__.append (tuple ([elem, i]));
			}
			return __accu0__;
		}) ();
		if (!(result)) {
			return result;
		}
		_heapify_max (result);
		var top = result [0] [0];
		var order = n;
		var _heapreplace = _heapreplace_max;
		for (var elem of it) {
			if (elem < top) {
				_heapreplace (result, tuple ([elem, order]));
				var __left0__ = result [0];
				var top = __left0__ [0];
				var _order = __left0__ [1];
				order++;
			}
		}
		result.py_sort ();
		return (function () {
			var __accu0__ = [];
			for (var [elem, order] of result) {
				__accu0__.append (elem);
			}
			return __accu0__;
		}) ();
	}
	var it = py_iter (iterable);
	var result = (function () {
		var __accu0__ = [];
		for (var [i, elem] of zip (range (n), it)) {
			__accu0__.append (tuple ([key (elem), i, elem]));
		}
		return __accu0__;
	}) ();
	if (!(result)) {
		return result;
	}
	_heapify_max (result);
	var top = result [0] [0];
	var order = n;
	var _heapreplace = _heapreplace_max;
	for (var elem of it) {
		var k = key (elem);
		if (k < top) {
			_heapreplace (result, tuple ([k, order, elem]));
			var __left0__ = result [0];
			var top = __left0__ [0];
			var _order = __left0__ [1];
			var _elem = __left0__ [2];
			order++;
		}
	}
	result.py_sort ();
	return (function () {
		var __accu0__ = [];
		for (var [k, order, elem] of result) {
			__accu0__.append (elem);
		}
		return __accu0__;
	}) ();
};
export var nlargest = function (n, iterable, key) {
	if (typeof key == 'undefined' || (key != null && key.hasOwnProperty ("__kwargtrans__"))) {;
		var key = null;
	};
	if (n == 1) {
		var it = py_iter (iterable);
		var sentinel = object ();
		if (key === null) {
			var result = max (it, __kwargtrans__ ({py_default: sentinel}));
		}
		else {
			var result = max (it, __kwargtrans__ ({py_default: sentinel, key: key}));
		}
		return (result === sentinel ? [] : [result]);
	}
	try {
		var size = len (iterable);
		try {
			if (n >= size) {
				return sorted (iterable, __kwargtrans__ ({key: key, reverse: true})).__getslice__ (0, n, 1);
			}
		}
		catch (__except0__) {
		}
	}
	catch (__except0__) {
		if (isinstance (__except0__, tuple ([py_TypeError, AttributeError]))) {
			// pass;
		}
		else {
			throw __except0__;
		}
	}
	if (key === null) {
		var it = py_iter (iterable);
		var result = (function () {
			var __accu0__ = [];
			for (var [i, elem] of zip (range (0, -(n), -(1)), it)) {
				__accu0__.append (tuple ([elem, i]));
			}
			return __accu0__;
		}) ();
		if (!(result)) {
			return result;
		}
		heapify (result);
		var top = result [0] [0];
		var order = -(n);
		var _heapreplace = heapreplace;
		for (var elem of it) {
			if (top < elem) {
				_heapreplace (result, tuple ([elem, order]));
				var __left0__ = result [0];
				var top = __left0__ [0];
				var _order = __left0__ [1];
				order--;
			}
		}
		result.py_sort (__kwargtrans__ ({reverse: true}));
		return (function () {
			var __accu0__ = [];
			for (var [elem, order] of result) {
				__accu0__.append (elem);
			}
			return __accu0__;
		}) ();
	}
	var it = py_iter (iterable);
	var result = (function () {
		var __accu0__ = [];
		for (var [i, elem] of zip (range (0, -(n), -(1)), it)) {
			__accu0__.append (tuple ([key (elem), i, elem]));
		}
		return __accu0__;
	}) ();
	if (!(result)) {
		return result;
	}
	heapify (result);
	var top = result [0] [0];
	var order = -(n);
	var _heapreplace = heapreplace;
	for (var elem of it) {
		var k = key (elem);
		if (top < k) {
			_heapreplace (result, tuple ([k, order, elem]));
			var __left0__ = result [0];
			var top = __left0__ [0];
			var _order = __left0__ [1];
			var _elem = __left0__ [2];
			order--;
		}
	}
	result.py_sort (__kwargtrans__ ({reverse: true}));
	return (function () {
		var __accu0__ = [];
		for (var [k, order, elem] of result) {
			__accu0__.append (elem);
		}
		return __accu0__;
	}) ();
};

//# sourceMappingURL=heapq.map