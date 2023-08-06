import numpy as np
from overrides import overrides
from typing import Any, Iterator, Dict, Callable
from nwdata import Reader

class DummyDataset(Reader):
	def __init__(self, N=10):
		super().__init__(
			dataBuckets = {"data" : ["rgb"], "labels" : ["class"]},
			dimGetter = {
				"rgb" : (lambda dataset, index : dataset[index]),
				"class" : (lambda dataset, index : 0)
			},
			dimTransform = {}
		)
		self.isCacheable = True
		self.dataset = np.random.randn(N, 3)

	@overrides
	def getDataset(self) -> Any:
		return self.dataset

	@overrides
	def __len__(self) -> int:
		return len(self.dataset)

class TestReader:
	def test_constructor_1(self):
		reader = DummyDataset()
		print(reader)
		assert not reader is None
		assert reader.datasetFormat.dataBuckets == {"data" : ["rgb"], "labels" : ["class"]}
		assert list(reader.datasetFormat.dimGetter.keys()) == ["rgb", "class"]
		for v in reader.datasetFormat.dimGetter.values():
			assert isinstance(v, Callable)
		assert list(reader.datasetFormat.dimTransform.keys()) == ["data", "labels"]
		assert list(reader.datasetFormat.dimTransform["data"].keys()) == ["rgb"]
		for v in reader.datasetFormat.dimTransform["data"].values():
			assert isinstance(v, Callable)
		assert list(reader.datasetFormat.dimTransform["labels"].keys()) == ["class"]
		for v in reader.datasetFormat.dimTransform["labels"].values():
			assert isinstance(v, Callable)

	def test_getItem_1(self):
		reader = DummyDataset()
		item = reader.iterate()[0]
		rgb = item["data"]["rgb"]
		assert np.abs(reader.dataset[0] - rgb).sum() < 1e-5

	def test_getNumData_1(self):
		reader = DummyDataset()
		numData = len(reader)
		assert numData == len(reader.dataset)

	def test_iterateOneEpoch_1(self):
		reader = DummyDataset()
		generator = reader.iterateOneEpoch()
		for i, item in enumerate(generator):
			rgb = item["data"]["rgb"]
			assert np.abs(rgb - reader.dataset[i]).sum() < 1e-5
		assert i == len(reader.dataset) - 1

	def test_iterateForever_1(self):
		reader = DummyDataset()
		generator = reader.iterateForever()
		for i, item in enumerate(generator):
			rgb = item["data"]["rgb"]
			ix = i % len(reader.dataset)
			assert np.abs(rgb - reader.dataset[ix]).sum() < 1e-5
			if i == len(reader.dataset) * 3:
				break

def main():
	# TestDataset().test_constructor_1()
	TestDataset().test_iterateOneEpoch_1()

if __name__ == "__main__":
	main()