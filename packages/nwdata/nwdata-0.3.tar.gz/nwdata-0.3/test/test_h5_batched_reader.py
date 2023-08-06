import numpy as np
import os
import h5py
import tempfile
from overrides import overrides
from typing import Tuple, List, Any
from nwdata import H5BatchedReader
from nwutils.batched import getBatchLens

def createDatasetIfNotExist():
	tempFileName = "%s/dataset.h5" % tempfile.gettempdir()
	if not os.path.exists(tempFileName):
		file = h5py.File(tempFileName, "w")
		file["rgb"] = np.random.randn(10, 3)
		file["class"] = np.random.randint(0, 2, size=(10, ))
		file.create_dataset("batches", (4, ), dtype=h5py.special_dtype(vlen=np.dtype("int32")))
		file["batches"][:] = [[0, 1, 2, 3], [4], [5, 6], [7, 8, 9]]
		file.flush()
		file.close()
	return tempFileName

class H5BatchedDataset(H5BatchedReader):
	def __init__(self):
		datasetPath = createDatasetIfNotExist()
		super().__init__(
			datasetPath,
			dataBuckets = {"data" : ["rgb"], "labels" : ["class"]},
			dimTransform = {}
		)

	def getBatches(self):
		if self.batches is None:
			self.setBatches(self.dataset["batches"][()])
		return self.batches

class TestH5BatchedReader:
	def test_constructor_1(self):
		reader = H5BatchedDataset()
		assert not reader is None
		assert not reader.getDataset() is None

	def test_getBatchItem_1(self):
		reader = H5BatchedDataset()
		g = reader.iterate()
		b = reader.batches
		index = b[0]
		item = g[0]
		rgb = item["data"]["rgb"]
		assert rgb.shape[0] == 4
		assert np.abs(rgb - reader.dataset["rgb"][0:4]).sum() < 1e-5

	def test_getBatchItem_2(self):
		reader = H5BatchedDataset()
		g = reader.iterate()
		n = len(g)
		for j in range(100):
			index = reader.batches[j % n]
			batchItem = g[j % n]
			rgb = batchItem["data"]["rgb"]
			print(index)
			Range = np.arange(index[0], index[-1] + 1)
			assert np.abs(rgb - reader.dataset["rgb"][Range]).sum() < 1e-5

	def test_iterateForever_1(self):
		reader = H5BatchedDataset()
		batches = reader.getBatches()
		batchLens = getBatchLens(batches)
		n = len(batches)
		g = reader.iterateForever()
		for j, batchItem in enumerate(g):
			rgb = batchItem["data"]["rgb"]
			try:
				assert len(rgb) == batchLens[j % n]
			except Exception:
				breakpoint()
			index = batches[j % n]
			assert np.abs(rgb - reader.dataset["rgb"][index]).sum() < 1e-5

			if j == 100:
				break

def main():
	TestH5BatchedDataset().test_iterateForever_1()

if __name__ == "__main__":
	main()