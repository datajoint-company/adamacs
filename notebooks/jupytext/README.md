
The DataJoint team has started using Jupytext internally to facilitate code review
the involves Jupyter notebooks. This package auto-generates py scripts that sync with 
notebooks. We keep these in a subdirectory of `notebooks/` to be ignored by most users,
while still highlighting differences on code review. If installed as a package within
Jupyter, these will autosync on save.

```bash
pip install jupytext
jupytext --set-formats ipynb,py notebooks/*ipynb
jupytext --sync notebooks/*ipynb # optional precautionary sync
mv notebooks/*py notebooks/jupytext/
```
