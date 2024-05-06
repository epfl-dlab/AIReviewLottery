[![Python 3.12.1](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-312/)
[![MIT License](https://img.shields.io/github/license/m43/focal-loss-against-heuristics)](LICENSE)
[![arXiv](https://img.shields.io/badge/arXiv-2303.04132-b31b1b.svg)](https://arxiv.org/abs/2405.02150)

# The AI Review Lottery: Widespread AI-Assisted Peer Reviews Boost Paper Scores and Acceptance Rates

This repository contains the implementation for the models' data labeling and experiments in [The AI Review Lottery: Widespread AI-Assisted Peer Reviews Boost Paper Scores and Acceptance Rates](https://arxiv.org/abs/2405.02150).

```
@misc{latona2024ai,
      title={The AI Review Lottery: Widespread AI-Assisted Peer Reviews Boost Paper Scores and Acceptance Rates}, 
      author={Giuseppe Russo Latona and Manoel Horta Ribeiro and Tim R. Davidson and Veniamin Veselovsky and Robert West},
      year={2024},
      eprint={2405.02150},
      archivePrefix={arXiv},
      primaryClass={cs.CY}
}
```
**Please consider citing our work, if you found the provided resources useful.**<br>

---
## 1. The Idea and the Repository in a Nutshell


Journals and conferences worry that peer reviews assisted by artificial intelligence (AI), particularly large language models (LLMs), may negatively influence the validity and fairness of the peer-review system, a cornerstone of modern science. In this work, we address this concern with a quasi-experimental study of the prevalence and impact of AI-assisted peer reviews in the context of the 2024 International Conference on Learning Representations (ICLR), a large and prestigious machine-learning conference. In this study, we conducted three analyses:

1. Prevalence of AI-assisted reviews: We quantify the number of reviews labeled as AI-assisted (according to GPTZero LLM detector).
2. Effect of AI-assisted reviews on scores: We quantify the difference between AI-assisted and human review scores on submissions submitted to ICLR2024.
3. Effect of AI-assisted reviews on paper acceptance: We study whether receiving an AI-assisted review boosts the likelihood of acceptance.

These three analysis and the results we obtained are illustrated in 

<div align="center">
<img src="analyses/fig1.png" style="width:80%">
</div>

