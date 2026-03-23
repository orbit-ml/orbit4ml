"""EuroSAT dataset wrapper for orbit4ml.data.

Wraps torchvision's EuroSAT dataset with on-demand download.
orbit4ml does not redistribute data — users download directly
from the source.

License: CC-BY-4.0 (upstream)
Source: https://github.com/phelber/EuroSAT
"""

from typing import Any

import torch
import torchvision
import torchvision.transforms as T


class EuroSAT(torch.utils.data.Dataset):
    """EuroSAT satellite imagery dataset.

    10-class land use/land cover classification from Sentinel-2.
    Images are 64x64 RGB. Downloads automatically on first use.

    Args:
        root: Root directory for dataset storage.
        transform: Optional transform applied to images.
        download: Whether to download if not found. Defaults to True.
    """

    license = "CC-BY-4.0"

    def __init__(
        self,
        root: str,
        transform: Any = None,
        download: bool = True,
    ) -> None:
        if transform is None:
            transform = T.Compose([T.ToTensor()])

        self._dataset = torchvision.datasets.EuroSAT(
            root=root,
            transform=transform,
            download=download,
        )

    def __len__(self) -> int:
        return len(self._dataset)

    def __getitem__(self, index: int) -> tuple[torch.Tensor, int]:
        return self._dataset[index]
