import numpy as np
from copy import deepcopy
from typing import Dict, Any
from .numpy import npGetInfo

# @brief Return the value of a nested dictionary key
# @param[in] d The potentially nested dictionary
# @param[in] k The potentially nested lookup key
# @return The value of the potentially nested key
def deepDictGet(d:Dict, k:Any):
	if isinstance(k, (tuple, list)):
		if len(k) == 1:
			return d[k]
		else:
			return deepDictGet(d[k[0]], k[1 :])
	else:
		return d[k]

def prettyPrintDict(d:Dict, depth:int=0):
	dphStr = " "  * depth
	for k in d:
		if isinstance(d[k], dict):
			print("%s- %s:" % (dphStr, k))
			prettyPrintDict(d[k], depth+1)
		elif isinstance(d[k], (tuple, list)):
			Len = len(d[k])
			Type = "n/a" if Len == 0 else type(d[k][0])
			print("%s- %s: Len: %s. Type: %s" % (dphStr, k, Len, Type))
		elif isinstance(d[k], np.ndarray):
			print("%s- %s: %s" % (dphStr, k, npGetInfo(d[k])))
		else:
			print("%s- %s. Type: %s"% (dphStr, k, type(d[k])))

# @brief Merges two dictionaries if and only if their keys are completely disjoin
#   TODO: Perhaps in future we can allow key clashes whose subkeys don't interact.
#   So: {"a":{"b":1}} {"a":{"c":2}} => {"a":{"b":1,"c":2}}, but {"a":{"b":1}} and {"a":{"b":2}} clashes.
#    Same, {"a":{"b":1}} and {"a":[5]} (or any other dtype besides a subdict) clashes.
# @param[in] d1 First dictionary
# @param[in] d2 Second dictionary
# @param[in] createNew If true, will create a new dictionary, othrerwise, it will update the first one. Default: true.
# @return Them merged dictionary
def mergeDict(d1:Dict, d2:Dict, createNew:bool=True) -> Dict:
	res = deepcopy(d1) if createNew else d1
	for k in d2:
		assert (not k in d1) or (k in d1 and not deepCheckEqual(d1[k], d2[k])), \
			f"Key clash '{k}'.\n -Present: {d1[k]}\n -New: {d2[k]}"
		res[k] = d2[k]
	return res
