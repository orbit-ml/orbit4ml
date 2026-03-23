# orbit4ml.data

Space ML datasets and loaders. All datasets are download-on-demand wrappers —
orbit4ml does not redistribute third-party data. Each wrapper documents its
upstream license.

## Quick Example

```python
import torch
from orbit4ml.data import EuroSAT

dataset = EuroSAT(root="./data")
loader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=True)

for images, labels in loader:
    print(images.shape)  # torch.Size([32, 3, 64, 64])
    print(labels.shape)  # torch.Size([32])
    break
```

---

## EuroSAT

::: orbit4ml.data.eurosat.EuroSAT
    options:
      show_root_heading: true
      show_source: true
      members_order: source
