// Transcrypt'ed from Python, 2020-03-16 11:49:26
var math = {};
var sys = {};
var time = {};
var wikitrust_algorithms = {};
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as __module_time__ from './time.js';
__nest__ (time, '', __module_time__);
import * as __module_sys__ from './sys.js';
__nest__ (sys, '', __module_sys__);
import * as __module_math__ from './math.js';
__nest__ (math, '', __module_math__);
import {Version as TextTrustVersion} from './wikitrust_algorithms.text_trust.version.js';
import {Edit} from './wikitrust_algorithms.text_diff.edit.js';
import {test_tichy} from './wikitrust_algorithms.text_diff.chdiff.js';
import {Version as AuthorRepVersion} from './wikitrust_algorithms.author_reputation.version.js';
import {Article} from './wikitrust_algorithms.author_reputation.article.js';
import {Author} from './wikitrust_algorithms.author_reputation.author.js';
import * as __module_wikitrust_algorithms__ from './wikitrust_algorithms.js';
__nest__ (wikitrust_algorithms, '', __module_wikitrust_algorithms__);
var __name__ = '__main__';
export var __MAXREP__ = 100000;
export var __TRUSTCONST__ = 1;
export var __REVISIONCONST_ = 0.1;
export var __EDGECONST__ = 2;
export var __VERSIONCONST__ = tuple ([__TRUSTCONST__, __REVISIONCONST_, __EDGECONST__]);
export var __MAXJUDGEDIST__ = 4;
export var __SCALINGCONST__ = 0.01;
export var __SCALINGFUNC__ = (function __lambda__ (x) {
	return math.log (1.1 + x);
});
export var compute_demo = function (file_name) {
	var revision_list = create_revision_list (file_name).__getslice__ (0, null, -(1));
	var author_table = create_author_table (revision_list);
	var version_list = [];
	var initial_text = revision_list [0] [2];
	var initial_version = TextTrustVersion.create_initial_version (initial_text.py_split (), 0, __VERSIONCONST__);
	version_list.append (initial_version);
	var initial_version_author_id = revision_list [0] [1];
	var initial_version_author = author_table [initial_version_author_id];
	print ('Rev#' + str (0));
	print (revision_list [0] [0]);
	print (revision_list [0] [1]);
	print ();
	var article = Article (__MAXJUDGEDIST__, __SCALINGCONST__, __SCALINGFUNC__);
	article.add_new_version (AuthorRepVersion (initial_version_author, revision_list [0] [2]));
	for (var version_iter = 1; version_iter < len (revision_list); version_iter++) {
		print ('Rev #' + str (version_iter));
		print ('Revision ID: ' + str (revision_list [version_iter] [0]));
		print ('User ID: ' + str (revision_list [version_iter] [1]));
		print ();
		var old_text = revision_list [version_iter - 1] [2];
		var new_text = revision_list [version_iter] [2];
		var version_author_id = revision_list [version_iter] [1];
		var version_author = author_table [version_author_id];
		var version_author_rep = version_author.reputation;
		var diff_list = test_tichy (old_text, new_text);
		var edit_list = (function () {
			var __accu0__ = [];
			for (var edit of diff_list) {
				__accu0__.append (Edit.edit_tuple_constructor (edit));
			}
			return __accu0__;
		}) ();
		var text_list = new_text.py_split ();
		var prev_version = version_list.__getslice__ (-(1), null, 1) [0];
		article.add_new_version (AuthorRepVersion (version_author, new_text));
		var new_version = TextTrustVersion.create_next_version (prev_version, text_list, edit_list, version_author_rep);
		version_list.append (new_version);
	}
	for (var author_id of author_table.py_keys ()) {
		print (author_table [author_id]);
	}
	return version_list;
};
export var create_author_table = function (revision_list) {
	var author_id_list = (function () {
		var __accu0__ = [];
		for (var revision of revision_list) {
			__accu0__.append (revision [1]);
		}
		return __accu0__;
	}) ();
	var author_id_list = sorted (list (dict.fromkeys (author_id_list)));
	var author_table = dict ({});
	for (var author_id of author_id_list) {
		author_table [author_id] = Author (author_id, 0, __MAXREP__);
	}
	author_table [0].maximum_reputation = 0;
	return author_table;
};
export var create_revision_list = function (json_data) {
	var revision_list = [];
	for (var rev_num = 0; rev_num < json_data ['size']; rev_num++) {
		var __left0__ = json_data ['revisions'] [rev_num] ['revisionId'];
		var revision_id = __left0__;
		var revision_text = __left0__;
		var __left0__ = json_data ['revisions'] [rev_num] ['userId'];
		var user_id = __left0__;
		var revision_text = __left0__;
		var text = json_data ['revisions'] [rev_num] ['text'];
		revision_list.append (tuple ([revision_id, user_id, text]));
	}
	return revision_list;
};

//# sourceMappingURL=demo.map