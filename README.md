# Knapsack Problem Solver

## Project Overview

This project is an interactive application for solving and comparing different variants of the Knapsack Problem.

The system allows users to enter custom item weights, values, and knapsack capacity, then compares the solutions produced by multiple optimization approaches.

The application was developed using Streamlit and provides visual comparisons of solution quality and execution time.


## Algorithms Implemented

### 0/1 Knapsack

A Dynamic Programming approach where each item can be selected at most once.

Time Complexity:

O(n × W)



### Unbounded Knapsack

A Dynamic Programming approach where items can be selected multiple times.

Time Complexity:

O(n × W)



### Fractional Knapsack

A Greedy algorithm that selects items according to their value-to-weight ratio and allows fractional item selection.

Time Complexity:

O(n log n)



## Features

* Interactive user interface
* Custom weight and value inputs
* Adjustable knapsack capacity
* Algorithm performance comparison
* Execution time measurement
* Selected item analysis
* Capacity utilization statistics
* Automatic best algorithm identification
* Visual result dashboards



## Technologies Used

* Python
* Streamlit
* Pandas
* Matplotlib
* Jupyter Notebook



## Visualizations

The application provides:

* Maximum Value Comparison
* Execution Time Comparison
* Selected Item Tables
* Capacity Usage Statistics
* Algorithm Performance Dashboard


## Learning Outcomes

This project demonstrates:

* Dynamic Programming
* Greedy Algorithms
* Algorithm Analysis
* Complexity Comparison
* Interactive Data Applications
* Streamlit Development



## Future Improvements

* Add Genetic Algorithm solutions
* Add Branch and Bound implementation
* Support large-scale benchmark datasets
* Export results to CSV or PDF
* Add advanced performance analytics

