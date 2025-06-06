import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

def load_csv() -> pd.DataFrame:
    """
    Load a Azure Usage data file into a pandas DataFrame
    
    Returns:
        pd.DataFrame: dataframe
    """
    df = pd.read_csv("data/AzureUsage.csv")
    return df

def summarize_data(df) -> str:
    """
    Generate a summary of the data
    
    Args:
        pd.DataFrame: dataframe
    Returns:
        str: summary of the data
    """
    summary = f"Rows: {len(df)}\nColumns: {', '.join(df.columns)}\n\n"
    
    # Azure-specific summary
    if 'Cost' in df.columns:
        total_cost = df['Cost'].sum()
        summary += f"Total Cost: ${total_cost:.2f}\n"
        summary += f"Average Cost: ${df['Cost'].mean():.2f}\n"
    
    if 'ServiceName' in df.columns:
        top_services = df.groupby('ServiceName')['Cost'].sum().sort_values(ascending=False).head(5)
        summary += "\nTop 5 Services by Cost:\n"
        for service, cost in top_services.items():
            summary += f"- {service}: ${cost:.2f}\n"
    
    if 'ServiceRegion' in df.columns:
        top_regions = df.groupby('ServiceRegion')['Cost'].sum().sort_values(ascending=False).head(5)
        summary += "\nTop 5 Regions by Cost:\n"
        for region, cost in top_regions.items():
            summary += f"- {region}: ${cost:.2f}\n"
    
    return summary

def generate_chart(x_col:str, y_col:str, output_dir='reports/charts') -> str:
    """
    Generate a chart from the data
    
    Args:
        x_col (str): The column to use for the x-axis.
        y_col (str): The column to use for the y-axis.
        output_dir (str): The directory to save the chart.
        
    Returns:
        str: path and filename to the saved chart.
    """
    
    df = pd.read_csv("data/AzureUsage.csv")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_chart.png"
    path = os.path.join(output_dir, filename)

    # For Azure data, we might want to aggregate data
    if x_col in ['ServiceName', 'ServiceRegion', 'ServiceType']:
        # Group by the x column and sum the y column
        chart_data = df.groupby(x_col)[y_col].sum().sort_values(ascending=False).head(10).reset_index()
        
        # Create a bar chart
        plt.figure(figsize=(10, 6))
        plt.bar(chart_data[x_col], chart_data[y_col])
        plt.xticks(rotation=45, ha='right')
        plt.title(f"{y_col} by {x_col}")
        plt.tight_layout()
        plt.savefig(path)
        plt.close()
    else:
        # Default behavior for other columns
        df.plot(kind='bar', x=x_col, y=y_col, legend=False, figsize=(10, 6))
        plt.tight_layout()
        plt.savefig(path)
        plt.close()
    
    path_str = f"Chart saved at: {path}"
    return path_str

df_table = load_csv()
result = summarize_data(df_table)
print(result)

path_output = generate_chart('ServiceName', 'Cost')
print(path_output) 