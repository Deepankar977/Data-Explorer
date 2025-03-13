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

# Function to handle zeros by converting them to NaN where needed
def handle_zeros():
    global df
    # Convert zeros to NaN for numeric columns only
    df.replace(0, pd.NA, inplace=True)

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
        handle_zeros()
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
                args.value = float(args.value)
            except ValueError:
                pass
        fill_value = args.value if args.value else fill_dec()
        df[args.column].fillna(fill_value, inplace=True)
        return f"Missing values in column '{args.column}' filled with '{fill_value}'"

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
    handle_zeros()
    try:
        plot_data = df[[args.x, args.y]].dropna().sort_values(by=args.x)
        style.use('ggplot')
        plt.plot(plot_data[args.x], plot_data[args.y], "g", label=args.y, linewidth=2)
        plt.title(f"{args.x} vs {args.y}")
        plt.ylabel(args.y)
        plt.xlabel(args.x)
        plt.legend()
        plt.show()
    except Exception as e:
        print(f"An error occurred: {e}")

def bar():
    handle_zeros()
    try:
        a = df[args.x].dropna()
        b = df[args.y].dropna()
        plt.bar(a, b)
        plt.xlabel(args.x)
        plt.ylabel(args.y)
        plt.title(f"Graph of {args.y}")
        plt.show()
    except Exception as e:
        print(f"An error occurred: {e}")

def boxplot():
    handle_zeros()
    try:
        plt.boxplot(df[args.y].dropna())
        plt.title(f"Boxplot of {args.y}")
        plt.ylabel(args.y)
        plt.show()
    except Exception as e:
        print(f"An error occurred: {e}")

def histogram():
    handle_zeros()
    try:
        plt.hist(df[args.x].dropna(), bins=20, color='blue', edgecolor='black', alpha=0.7)
        plt.title(f"Histogram of {args.x}")
        plt.xlabel(args.x)
        plt.ylabel("Frequency")
        plt.show()
    except Exception as e:
        print(f"An error occurred: {e}")

def pie():
    handle_zeros()
    try:
        grouped_data = df.groupby(args.x)[args.y].sum()
        plt.pie(grouped_data.values, labels=grouped_data.index, wedgeprops={'edgecolor': 'black'})
        plt.title(f"Pie Chart of {args.y}")
        plt.show()
    except Exception as e:
        print(f"An error occurred: {e}")

def scatter():
    handle_zeros()
    try:
        a = df[args.x].dropna()
        b = df[args.y].dropna()
        plt.scatter(a, b)
        plt.xlabel(args.x)
        plt.ylabel(args.y)
        plt.title(f"Scatter plot of {args.x} vs {args.y}")
        plt.show()
    except Exception as e:
        print(f"An error occurred: {e}")

def heatmap():
    handle_zeros()
    try:
        plt.figure(figsize=(10, 6))
        sns.heatmap(df.corr(), annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
        plt.title("Heatmap of Correlation")
        plt.show()
    except Exception as e:
        print(f"An error occurred: {e}")

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
