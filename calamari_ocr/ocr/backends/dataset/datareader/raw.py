from typing import Generator, Tuple, Union
import numpy as np

from calamari_ocr.ocr.datasets.datasetype import DataSetMode
from calamari_ocr.ocr.backends.dataset.data_types import SampleMeta, InputSample
from calamari_ocr.ocr.backends.dataset.datareader.base import DataReader


class RawDataReader(DataReader):
    def __init__(self, mode: DataSetMode, images=None, texts=None, meta=None):
        """ Create a dataset from memory

        Since this dataset already contains all data in the memory, this dataset may not be loaded

        Parameters
        ----------
        images : list of images
            the images of the dataset
        texts : list of str
            the texts of this dataset
        """
        super().__init__(mode, skip_invalid=False, remove_invalid=False)

        if images is None and texts is None:
            raise Exception("Empty data set is not allowed. Both images and text files are None")

        if images is not None and texts is not None and len(images) == 0 and len(texts) == 0:
            raise Exception("Empty data set provided.")

        if texts is None or len(texts) == 0:
            if images is None:
                raise Exception("Empty data set.")

            # No gt provided, probably prediction
            texts = [None] * len(images)

        if images is None or len(images) == 0:
            if len(texts) is None:
                raise Exception("Empty data set.")

            # No images provided, probably evaluation
            images = [None] * len(texts)

        if not meta:
            meta = [SampleMeta(str(i), None) for i in range(len(images))]

        for image, text, meta in zip(images, texts, meta):
            self.add_sample({
                "image": image,
                "text": text,
                "id": meta.id,
                "meta": meta,
            })

        self.loaded = True

    def _load_sample(self, sample, text_only) -> Generator[InputSample, None, None]:
        if text_only:
            yield InputSample(None, sample['text'], sample['meta'])
        yield InputSample(sample['image'], sample['text'], sample['meta'])
