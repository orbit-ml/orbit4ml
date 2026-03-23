from unittest.mock import patch, MagicMock

import torch

from orbit4ml.data.eurosat import EuroSAT


def test_eurosat_is_torch_dataset():
    assert issubclass(EuroSAT, torch.utils.data.Dataset)


@patch("orbit4ml.data.eurosat.torchvision.datasets.EuroSAT")
def test_eurosat_wraps_torchvision(mock_tv_eurosat):
    mock_dataset = MagicMock()
    mock_dataset.__len__ = MagicMock(return_value=27000)
    mock_tv_eurosat.return_value = mock_dataset

    ds = EuroSAT(root="./data")
    mock_tv_eurosat.assert_called_once()
    assert len(ds) == 27000


@patch("orbit4ml.data.eurosat.torchvision.datasets.EuroSAT")
def test_eurosat_getitem_returns_tensor_and_label(mock_tv_eurosat):
    mock_dataset = MagicMock()
    mock_dataset.__getitem__ = MagicMock(return_value=(torch.randn(3, 64, 64), 5))
    mock_dataset.__len__ = MagicMock(return_value=100)
    mock_tv_eurosat.return_value = mock_dataset

    ds = EuroSAT(root="./data")
    img, label = ds[0]
    assert isinstance(img, torch.Tensor)
    assert img.shape == (3, 64, 64)
    assert label == 5


@patch("orbit4ml.data.eurosat.torchvision.datasets.EuroSAT")
def test_eurosat_license_info(mock_tv_eurosat):
    mock_tv_eurosat.return_value = MagicMock()
    ds = EuroSAT(root="./data")
    assert ds.license == "CC-BY-4.0"
