import numpy as np
from overrides import overrides
from typing import Dict
from .metric import Metric

accObj = None

class GlobalAccuracy(Metric):
	def __init__(self):
		super().__init__(direction="max")
		self.reset()

	def fReturn(self):
		return self.globalCorrect / (self.globalAll + np.spacing(1))

	def reset(self):
		self.globalCorrect = 0
		self.globalAll = 0

	def onEpochStart(self, **kwargs):
		self.reset()

	def epochReduceFunction(self, results):
		res = self.fReturn()
		self.reset()
		return res

	def __call__(self, y, t, **k):
		t = t.astype(bool)
		y = (y == y.max(axis=-1, keepdims=True))
		y = y[t]
		self.globalCorrect += y.sum()
		self.globalAll += t.sum()
		return self.fReturn()

class LocalAccuracy(Metric):
	def __init__(self):
		super().__init__(direction="max")

	def __call__(self, results:np.ndarray, labels:np.ndarray, **kwargs) -> float: #type: ignore[override]
		Shape, NC = results.shape[0: -1], results.shape[-1]
		# If labels are not one-hot, but a list of indices, convert ot one-hot
		if not len(np.unique(labels)) in (1, 2):
			assert labels.dtype == np.uint8
			labels = np.eye(NC)[labels]

		labels = labels.astype(bool)
		assert results.shape == labels.shape

		# Flatten to 2D
		results = results.reshape(-1, NC)
		labels = labels.reshape(-1, NC)

		# Keep only max value
		labelsArgMax = labels[range(len(results)), results.argmax(axis=-1)]
		return labelsArgMax.mean()

# Based on https://towardsdatascience.com/multi-class-metrics-made-simple-part-i-f1Score-and-f1Score-9250280bddc2
class Accuracy(Metric):
	def __init__(self, mode="local"):
		super().__init__("max")
		assert mode in ("local", "global")
		self.mode = mode
		self.obj = {
			"local" : LocalAccuracy,
			"global" : GlobalAccuracy
		}[mode]()

	@overrides
	def getExtremes(self) -> Dict[str, float]:
		return {"min" : 0, "max" : 1}

	def iterationReduceFunction(self, results):
		return self.obj.iterationReduceFunction(results)

	def epochReduceFunction(self, results):
		results = self.obj.epochReduceFunction(results)
		return results

	def __call__(self, y, t, **k):
		return self.obj(y, t, **k)

# Simple wrapper for the Accuracy class
# @param[in] y Predictions (After softmax). Shape: MBx(Shape)xNC
# @param[in] t Class labels. Shape: MBx(Shape) and values of 0 and 1.
def accuracy(y:np.ndarray, t:np.ndarray, **kwargs):
	global accObj
	if accObj is None:
		accObj = Accuracy(mode="local")
	return accObj(y, t)
