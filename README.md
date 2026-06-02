# AI-Assisted Compiler Error Diagnosis System

## Overview

This project is a Machine Learning based compiler error diagnosis system that automatically analyzes GCC/G++ compiler diagnostics and classifies C++ compilation errors into meaningful categories. The system assists beginner programmers by providing human-readable explanations and debugging guidance.

## Problem Statement

Compiler error messages are often difficult for beginners to understand. This project aims to simplify the debugging process by automatically classifying compiler errors and providing structured repair suggestions.

## Features

* Automated compiler error classification
* 8 compiler error categories
* Beginner-friendly explanations
* Fully local execution (no cloud APIs)
* Fast prediction and diagnosis

## Tech Stack

* Python
* scikit-learn
* NumPy
* Pandas

## Machine Learning Pipeline

1. Data Collection
2. Data Cleaning and Preprocessing
3. Feature Engineering
4. Model Training
5. Evaluation and Validation

## Models Evaluated

* Random Forest
* Support Vector Machine (SVM)
* Decision Tree
* Naive Bayes

## Results

| Metric                | Value  |
| --------------------- | ------ |
| Test Accuracy         | 86%    |
| Cross Validation Mean | 87.7%  |
| Validation Pass Rate  | 93.75% |

## Repository Structure

* WEEK1-WEEK14: Project development and implementation phases
* WEEK5/error_collection: Error dataset collection
* WEEK13: Testing and Validation
* WEEK14: Final Report

## Future Improvements

* Larger dataset collection
* Deep learning based classification
* IDE integration
* Real-time debugging assistance
