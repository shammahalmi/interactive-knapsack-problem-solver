# Knapsack Problem Solver and Algorithm Analysis

## Project Overview

This project provides both an interactive application and a comprehensive experimental analysis of the Knapsack Problem.

The repository contains:

* A Streamlit-based web application for solving knapsack problems interactively.
* A detailed Jupyter Notebook that analyzes and compares different knapsack algorithms using multiple performance metrics.

The project demonstrates the implementation, evaluation, and comparison of three classical variants of the Knapsack Problem.

---

## Algorithms Implemented

### 0/1 Knapsack

A Dynamic Programming approach where each item can be selected at most once.

**Time Complexity:** O(n × W)

### Unbounded Knapsack

A Dynamic Programming approach where items can be selected multiple times.

**Time Complexity:** O(n × W)

### Fractional Knapsack

A Greedy algorithm that selects items according to their value-to-weight ratio and allows fractional item selection.

**Time Complexity:** O(n log n)

---

## Repository Structure

```text
knapsack-problem-solver/
│
├── app.py
├── knapsack_algorithm_analysis.ipynb
├── README.md
```

### app.py

Interactive Streamlit application that allows users to:

* Enter custom weights and values
* Define knapsack capacity
* Compare algorithm performance
* Visualize selected items
* Analyze execution times
* View capacity utilization statistics

### knapsack_algorithm_analysis.ipynb

Research-oriented notebook containing:

* Performance Analysis
* Solution Quality Comparison
* Runtime Analysis
* Scalability Analysis
* Convergence Analysis
* Diversity Analysis
* Function Evaluation Analysis
* Sensitivity Analysis
* Statistical Evaluation
* Final Comparative Discussion

---

## Features

### Interactive Application

* Streamlit-based user interface
* Custom problem inputs
* Real-time algorithm comparison
* Visualization dashboard
* Best algorithm identification

### Experimental Analysis

* Comparative algorithm evaluation
* Performance benchmarking
* Complexity analysis
* Statistical testing
* Scalability experiments

---

## Technologies Used

* Python
* Streamlit
* Pandas
* NumPy
* Matplotlib
* SciPy
* Jupyter Notebook

---

## Visualizations

The project includes:

* Maximum Value Comparison
* Runtime Comparison
* Capacity Usage Analysis
* Convergence Curves
* Diversity Curves
* Scalability Analysis Charts
* Statistical Evaluation Results

---

## Learning Outcomes

This project demonstrates practical experience in:

* Dynamic Programming
* Greedy Algorithms
* Algorithm Design
* Performance Evaluation
* Statistical Analysis
* Data Visualization
* Interactive Application Development
* Streamlit Deployment

---

## Future Improvements

* Branch and Bound Implementation
* Multi-Objective Knapsack Optimization
* Additional Benchmark Datasets
* Export Results to CSV/PDF
* Advanced Visualization Dashboard

---
