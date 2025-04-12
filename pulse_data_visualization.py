import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_pulse_data(filepath="C:/Users/sethw/Downloads/Exercise_Data.csv"):
    """
    Load and preprocess pulse data from a CSV file
    
    Parameters:
    -----------
    filepath : str
        Path to the CSV file containing pulse data
    
    Returns:
    --------
    pd.DataFrame
        Preprocessed pulse data
    """
    data = pd.read_csv(filepath)
    # Basic preprocessing (handling missing values, etc.)
    data = data.dropna()
    
    # Reshape data from wide to long format for easier plotting
    # Convert the time columns (1 min, 15 min, 30 min) to a single 'pulse' column
    long_data = pd.melt(data, 
                        id_vars=['id', 'diet', 'kind'],
                        value_vars=['1 min', '15 min', '30 min'],
                        var_name='time',
                        value_name='pulse')
    
    # Rename 'kind' to 'exercise' for clarity
    long_data = long_data.rename(columns={'kind': 'exercise'})
    
    return long_data

def generate_pulse_heatmap(data, pulse_col='pulse', x_col='exercise', y_col='diet', 
                          title='Average Pulse Rate by Diet and Exercise Type', figsize=(12, 8)):
    """
    Generate a heatmap visualization of pulse data
    
    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame containing pulse data
    pulse_col : str, default='pulse'
        Column name for pulse values
    x_col : str, default='exercise'
        Column name for x-axis values (e.g., exercise type)
    y_col : str, default='diet'
        Column name for y-axis values (e.g., diet type)
    title : str, default='Average Pulse Rate by Diet and Exercise Type'
        Title for the heatmap
    figsize : tuple, default=(12, 8)
        Size of the figure
    """
    plt.figure(figsize=figsize)
    
    # Create a pivot table for the heatmap
    pivot_data = data.pivot_table(index=y_col, columns=x_col, values=pulse_col, aggfunc='mean')
    
    # Create the heatmap
    ax = sns.heatmap(pivot_data, annot=True, cmap='YlOrRd', fmt='.1f', linewidths=.5)
    
    plt.title(title, fontsize=16)
    plt.xlabel(x_col.capitalize(), fontsize=12)
    plt.ylabel(y_col.capitalize(), fontsize=12)
    
    plt.tight_layout()
    plt.savefig('pulse_heatmap.png')
    plt.show()
    
    # Additional heatmap showing pulse over time for each exercise type
    pivot_time = data.pivot_table(index='time', columns='exercise', values='pulse', aggfunc='mean')
    
    plt.figure(figsize=figsize)
    ax = sns.heatmap(pivot_time, annot=True, cmap='YlGnBu', fmt='.1f', linewidths=.5)
    plt.title('Average Pulse Rate Over Time by Exercise Type', fontsize=16)
    plt.xlabel('Exercise Type', fontsize=12)
    plt.ylabel('Time', fontsize=12)
    
    plt.tight_layout()
    plt.savefig('pulse_time_heatmap.png')
    plt.show()

def generate_categorical_plots(data, figsize=(14, 10)):
    """
    Generate categorical plots of pulse values by diet and exercise type
    
    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame containing pulse data
    figsize : tuple, default=(14, 10)
        Size of the figure
    """
    # Create a figure with subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 10))
    
    # Violin plot for pulse values by diet type
    sns.violinplot(x='diet', y='pulse', data=data, inner=None, palette='pastel', ax=ax1)
    sns.boxplot(x='diet', y='pulse', data=data, width=0.3, palette='Set2', saturation=0.5, ax=ax1)
    sns.stripplot(x='diet', y='pulse', data=data, size=4, color='black', alpha=0.3, ax=ax1)
    ax1.set_title('Pulse Values by Diet Type')
    ax1.set_xlabel('Diet Type')
    ax1.set_ylabel('Pulse Value')
    ax1.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Boxplot with swarmplot overlay for pulse values by exercise type
    sns.boxplot(x='exercise', y='pulse', data=data, palette='Set3', ax=ax2)
    sns.swarmplot(x='exercise', y='pulse', data=data, color='black', alpha=0.5, ax=ax2)
    ax2.set_title('Pulse Values by Exercise Type')
    ax2.set_xlabel('Exercise Type')
    ax2.set_ylabel('Pulse Value')
    ax2.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('pulse_categorical_plots.png')
    plt.show()

def main():
    """
    Example usage of the pulse data visualization functions
    """
    # Sample data - replace with your actual data file
    try:
        data = load_pulse_data()
        
        # Generate visualizations
        generate_pulse_heatmap(data)
        generate_categorical_plots(data)
        
    except FileNotFoundError:
        print("Sample data file not found. Please provide a valid file path.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()