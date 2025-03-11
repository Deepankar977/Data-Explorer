import argparse
import pandas as pd
from matplotlib import pyplot as plt, style
import seaborn as sns

parser = argparse.ArgumentParser()
parser.add_argument("CSV_File", help="Path to the CSV file for analysis")
parser.add_argument("--Operation", help="Operation to perform, number of rows and columns, and head to see top rows",
                    choices=["rows", "columns", "head", "stats", "fill"])
parser.add_argument("--column", help="Column name to fill missing values.")
parser.add_argument("--value", help="Value to fill the missing cells")
parser.add_argument("--average", choices=["mean", "median", "mode"],
                    help="Type of average to fill missing values instead of a fixed value.")
parser.add_argument("--visual", help="A visual representation of given data",
                    choices=["hist","bar","line","pie", "boxplot", "scatter", "heatmap"])
parser.add_argument("--x",help="choosing column as x-axis for visualisation")
parser.add_argument("--y",help="choosing column as y-axis for visualisation")
parser.add_argument("--export", help="File name to export the modified data")
parser.add_argument("--format", choices=["csv", "excel", "json"], help="Format to export the data")

args = parser.parse_args()

if args.CSV_File:
    df = pd.read_csv(args.CSV_File)
else:
    raise FileNotFoundError

def fill_dec():
    column = df[args.column]
    if args.average == "mode":
        return column.mode().iloc[0]  # Mode returns multiple values, select the first one
    elif args.average == "mean":
        return column.mean()
    elif args.average == "median":
        return column.median()

def data_ops():
    if args.Operation == "rows":
        num_rows = len(df)
        return f"Number of rows is {num_rows}"
    elif args.Operation == "columns":
        num_rows, num_col = df.shape
        return f"Number of columns is {num_col}"
    elif args.Operation == "head":
        how_many = input("How many rows you want to see?: ")
        return df.head(int(how_many))
    elif args.Operation == "stats":
        return df.describe()
    elif args.Operation == "fill":
        if not args.column:
            print("Error: --column argument is required for fill operation.")
            exit()
        if args.column not in df.columns:
            print(f"Error: Column '{args.column}' not found in the dataset.")
            exit()
        if args.value and args.average:
            print("Error: Please provide either --value OR --average, not both.")
            exit()
        if args.value:
            try:
                args.value = float(args.value)  # Convert only if it's a number
            except ValueError:
                pass  # Keep as string if conversion fails
        # Decide fill value
        fill_value = args.value if args.value else fill_dec()
        # Apply filling
        new_table = df.fillna({args.column: fill_value})
        return f"""Here is the new table with missing values filled:\n
----------------------------------------------------------------------------------------------------\n{new_table}"""

def export():
    if args.export or args.format:
        try:
            if args.format == 'csv':
                df.to_csv(args.export, index=False)
            elif args.format == 'excel':
                df.to_excel(args.export, index=False)
            elif args.format == 'json':
                df.to_json(args.export, orient='records', lines=True)
            print(f"Data exported to {args.export} in {args.format} format.")
        except Exception as e:
            print(f"Error exporting data {e}")


def line():
    a = df[args.x]
    b = df[args.y]
    style.use('ggplot')
    plt.plot(a,b,"g",label=args.y, linewidth=4)
    plt.title(f"{args.x} vs {args.y}")
    plt.ylabel(args.y)
    plt.xlabel(args.x)
    plt.legend()
    plt.show(block=True)

def bar():
    a = df[args.x]
    b = df[args.y]
    plt.bar(a,b)
    plt.xlabel(args.x)
    plt.ylabel(args.y)
    plt.title(f"Graph of {args.y}")
    plt.show(block=True)

def boxplot():
    if args.y not in df.columns:
        print(f"Error: Column '{args.y}' not found in the dataset.")
        return
    if not pd.api.types.is_numeric_dtype(df[args.y]):
        print(f"Error: Column '{args.y}' must contain numeric values for a boxplot.")
        return
    if df[args.y].nunique() == 1:
        print(f"Warning: Column '{args.y}' contains only one unique value, boxplot may not be meaningful.")
    plt.boxplot(df[args.y].dropna())
    plt.title(f"Boxplot of {args.y}")
    plt.ylabel(args.y)
    plt.show()

def histogram():
    if args.x not in df.columns:
        print(f"Error: Column {args.x} not found in the dataset.")
        return
    if not pd.api.types.is_numeric_dtype(df[args.x]):
        print(f"Error: Column '{args.x}' must contain numeric values for a histogram.")
        return
    plt.hist(df[args.x], bins=20, color='blue', edgecolor='black', alpha=0.7)
    plt.title(f"Histogram of {args.x}")
    plt.xlabel(args.x)
    plt.ylabel("Frequency")
    plt.show()

def pie():
    plt.style.use("ggplot")
    # Check if columns exist
    if args.x not in df.columns or args.y not in df.columns:
        print(f"Error: One or both of the columns '{args.x}' and '{args.y}' not found in dataset.")
        return
    # Ensure y-axis data is numeric
    if not pd.api.types.is_numeric_dtype(df[args.y]):
        print(f"Error: Column '{args.y}' must contain numeric values for a pie chart.")
        return
    # Group by args.x to sum up args.y
    grouped_data = df.groupby(args.x)[args.y].sum()
    labels = grouped_data.index.tolist()
    values = grouped_data.values.tolist()
    #plt.figure(figsize=(8, 6))
    plt.pie(values, labels=labels, wedgeprops={'edgecolor': 'black'})
    plt.title(f"Pie Chart of {args.y}")
    plt.show()

def scatter():
    plt.style.use('seaborn-v0_8-dark-palette')
    a = df[args.x].dropna().tolist()
    b = df[args.y].dropna().tolist()
    plt.scatter(a,b)
    plt.xlabel(args.x)
    plt.ylabel(args.y)
    plt.title(f"Scatter graph of {args.x} vs {args.y}")
    plt.show()

def heatmap(): #beta
    plt.style.use('seaborn-v0_8-dark-palette')
    # Ask user for column names (optional)
    selected_columns = args.x.split(",") if args.x else df.select_dtypes(include=["number"]).columns.tolist()
    for col in selected_columns:
        if col not in df.columns:
            print(f"Error: Column '{col}' not found in the dataset.")
            return
    plt.figure(figsize=(10, 6))
    sns.heatmap(df[selected_columns].corr(), annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title(f"Heatmap of Selected Columns: {', '.join(selected_columns)}")
    plt.show()

def visualise():
    if args.visual == "line":
        line()
    elif args.visual == "bar":
        bar()
    elif args.visual == "boxplot":
        boxplot()
    elif args.visual == "hist":
        histogram()
    elif args.visual == "pie":
        pie()
    elif args.visual == "scatter":
        scatter()
    elif args.visual == "heatmap":
        heatmap()

if args.Operation:
    print(data_ops())

if args.visual:
    visualise()

export()
