# Language Models: *n*-grams and PCFGs
*Derek Andersen and Joanne Chau*  

Final project for LIN 538: Statistics for Linguists at Stony Brook University (Fall 2020).

## Overview

This project's objective is to train, evaluate, and compare the results of two different statistical language models: a **trigram model** and a **PCFG**. In both cases, **perplexity** is used as a metric for evaluation. Both models were trained on the same data, the Wall Street Journal corpus containing 2,499 stories from a three-year period resulting in 38,785 English sentences. In both cases, the corpus was split 80/20 into train/test datasets.

## Contents

This repository contains code files, a comprehensive walkthrough of the project's code in the form of a Jupyter notebook, and the project report. Specifically,

- `trigram_model.py`: a Python implementation of a trigram language model,
- `pcfg_model.py`: a Python implementation of a PCFG language model,
- `LIN538_final.ipynb`: a Jupyer notebook file containing a walkthrough of both language models and their output,
- `LIN538_final_report.pdf`: the project report PDF, and
- `LIN538_final_report.tex`: the LaTeX source file for the project report.
