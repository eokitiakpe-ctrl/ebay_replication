## Dependency Graph Answers

1. If I edit `code/preprocess.py`, Make will rebuild the figures (`figure_5_2.png` and `figure_5_3.png`) because they depend on that script. Since the figures are inputs to the paper, Make will also rebuild `paper/paper.pdf`. It will skip `did_analysis.py` and `did_table.tex` because those depend on a different script.

2. If I edit `code/did_analysis.py`, Make will rebuild `output/tables/did_table.tex` and then recompile `paper/paper.pdf` because the table is used in the paper. It will skip the preprocessing step and figures because they depend on `preprocess.py`, which did not change.

3. If I edit `paper/paper.tex`, Make will only rebuild `paper/paper.pdf`. It will skip both Python scripts (`preprocess.py` and `did_analysis.py`) because the figures and tables they produce have not changed.

