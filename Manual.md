# CSV Data Explorer - Manual

This document provides a detailed guide on how to use the **CSV Data Explorer** CLI tool, including usage examples and sample commands.

---

##  **Commands**

### Show Number of Rows and Columns
```sh
python csv_explorer.py sample.csv --operation rows
python csv_explorer.py sample.csv --operation columns
```
### Show Statistics of the Dataset
```sh
python csv_explorer.py sample.csv --operation stats
```
### Display First N Rows
```sh
python csv_explorer.py sample.csv --operation head
```
## Fill Missing Values
### Fill with a specific value
```sh
python csv_explorer.py sample.csv --operation fill --column "Column1" --value 0
```
### Fill with mean, median, or mode
```sh
python csv_explorer.py sample.csv --operation fill --column "Column1" --average mean
python csv_explorer.py sample.csv --operation fill --column "Column1" --average median
python csv_explorer.py sample.csv --operation fill --column "Column1" --average mode
```
### Export Data to File
```sh
python csv_explorer.py sample.csv --export "output.csv" --format csv
python csv_explorer.py sample.csv --export "output.xlsx" --format excel
python csv_explorer.py sample.csv --export "output.json" --format json
```
## Data Visualization
### Line Plot
```sh
python csv_explorer.py sample.csv --visual line --x "Column1" --y "Column2"
```
### Bar Plot
```sh
python csv_explorer.py sample.csv --visual bar --x "Column1" --y "Column2"
```
### Box Plot
```sh
python csv_explorer.py sample.csv --visual boxplot --y "Column1"
```
### Histogram
```sh
python csv_explorer.py sample.csv --visual hist --x "Column1"
```
### Pie Chart
```sh
python csv_explorer.py sample.csv --visual pie --x "Column1" --y "Column2"
```
### Scatter Plot
```sh
python csv_explorer.py sample.csv --visual scatter --x "Column1" --y "Column2"
```
### Heatmap (Beta)
```sh
python csv_explorer.py sample.csv --visual heatmap --x "Column1,Column2"
```
