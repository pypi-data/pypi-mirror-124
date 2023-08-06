from pathlib import Path

import numpy as np

import fast_overlap

ims = np.load(str(Path(__file__).parent / "test-ims.npy"))
expected = np.load(str(Path(__file__).parent / "expected-overlap.npy"))
shape = (int(np.max(ims[0]) + 1), int(np.max(ims[1]) + 1))


def test_overlap():
    out = fast_overlap.overlap(ims[0].astype(np.int32), ims[1].astype(np.int32), shape)
    assert np.all(out == expected)


def test_parallel_overlap():
    out = fast_overlap.overlap_parallel(
        ims[0].astype(np.int32), ims[1].astype(np.int32), shape
    )
    assert np.all(out == expected)
