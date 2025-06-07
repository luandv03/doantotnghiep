import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from datetime import datetime, timedelta
import os

def load_data():
    """Load the necessary data files."""
    # Paths to data files
    schedule_path = "./out/schedule.json"
    input_path = "./data/input18thieumay2.json"
    
    # Load schedule data
    try:
        with open(schedule_path, 'r', encoding='utf-8') as f:
            schedule_data = json.load(f)
    except Exception as e:
        print(f"Error loading schedule data: {e}")
        schedule_data = []
        
    # Load input data (for machine information)
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            input_data = json.load(f)
    except Exception as e:
        print(f"Error loading input data: {e}")
        input_data = {"workers": [], "operations": []}
        
    return schedule_data, input_data

def extract_employee_positions(input_data):
    """Extract all machine positions from input data."""
    employee_positions = set()
    for employee in input_data.get("assets", []):
        if "position" in employee:
            employee_positions.add(employee["position"])
    return employee_positions

def extract_employee_position_to_employees(input_data):
    """Create a mapping from employee position to list of employees."""
    employee_position_to_employees = {}
    for employee in input_data.get("workers", []):
        employee_position = employee.get("position")
        if employee_position:
            if employee_position not in employee_position_to_employees:
                employee_position_to_employees[employee_position] = []
            employee_position_to_employees[employee_position].append(employee.get("id"))
    return employee_position_to_employees

def extract_operation_to_employee_position(input_data):
    """Create a mapping from operation ID to required employee position."""
    operation_to_employee_position = {}
    for op in input_data.get("operations", []):
        op_id = op.get("id")
        employee_position = op.get("requiredPosition")
        if op_id and employee_position:
            operation_to_employee_position[op_id] = employee_position
    return operation_to_employee_position

def extract_detailed_schedules(schedule_data):
    """Extract all detailed schedule entries from the schedule data."""
    detailed_schedules = []
    
    # Handle different formats of schedule_data
    if isinstance(schedule_data, list):
        for item in schedule_data:
            if isinstance(item, dict) and "detailed_schedule" in item:
                for entry in item.get("detailed_schedule", []):
                    detailed_schedules.append({
                        "operation_id": item.get("id"),
                        "day": entry.get("day"),
                        "shift": entry.get("shift"),
                        "asset_id": entry.get("asset_id"),
                        "worker_id": entry.get("worker_id"),
                    })
    elif isinstance(schedule_data, dict):
        for op_id, op_data in schedule_data.items():
            if isinstance(op_data, dict) and "detailed_schedule" in op_data:
                for entry in op_data.get("detailed_schedule", []):
                    detailed_schedules.append({
                        "operation_id": op_id,
                        "day": entry.get("day"),
                        "shift": entry.get("shift"),
                        "asset_id": entry.get("asset_id"),
                        "worker_id": entry.get("worker_id"),
                    })
    
    return detailed_schedules

def calculate_employee_idle_percentages(detailed_schedules, employee_position_to_employees, operation_to_employee_position):
    """Calculate machine idle percentages for each shift and machine position."""
    # Create a DataFrame from detailed schedules
    if not detailed_schedules:
        print("No detailed schedules found.")
        return pd.DataFrame()
    
    df = pd.DataFrame(detailed_schedules)
    
    # Make sure required columns exist
    required_columns = ["day", "shift", "operation_id", "worker_id"]
    for col in required_columns:
        if col not in df.columns:
            print(f"Required column '{col}' not found in schedule data.")
            return pd.DataFrame()
            
    # Add machine type column based on operation_id
    df["employee_position"] = df["operation_id"].map(operation_to_employee_position)
    
    # Create a unique key for each day-shift combination
    df["day_shift"] = df["day"] + "-" + df["shift"].astype(str)
    
    # Group by day, shift, machine type and count unique machines used
    used_employees = df.groupby(["day", "shift", "employee_position"])["worker_id"].nunique().reset_index()
    used_employees.rename(columns={"worker_id": "used_count"}, inplace=True)
    
    # Create a list of all day-shift-employee_position combinations
    all_combinations = []
    day_shifts = df[["day", "shift"]].drop_duplicates().values.tolist()
    
    for day, shift in day_shifts:
        # Find all employee types used in this day-shift
        employee_positions_used = df[(df["day"] == day) & (df["shift"] == shift)]["employee_position"].unique()
        
        for employee_position in employee_positions_used:
            all_combinations.append({
                "day": day,
                "shift": shift,
                "employee_position": employee_position
            })
            
    # Create a new DataFrame with all combinations
    all_df = pd.DataFrame(all_combinations)
    
    # Merge with used employees count
    result_df = pd.merge(
        all_df,
        used_employees,
        on=["day", "shift", "employee_position"],
        how="left"
    )
    
    # Fill NA values with 0
    result_df["used_count"].fillna(0, inplace=True)
    
    # Add total count of machines for each type
    result_df["total_count"] = result_df["employee_position"].apply(
        lambda x: len(employee_position_to_employees.get(x, []))
    )
    
    # Calculate idle count and percentage
    result_df["idle_count"] = result_df["total_count"] - result_df["used_count"]
    result_df["idle_percentage"] = (result_df["idle_count"] / result_df["total_count"]) * 10
    
    # Create a datetime column for sorting
    result_df["datetime"] = result_df.apply(
        lambda row: datetime.strptime(row["day"], "%Y-%m-%d") + 
                   timedelta(hours=6*(int(row["shift"])-1)),
        axis=1
    )
    
    # Sort by datetime
    result_df = result_df.sort_values(by="datetime")
    
    return result_df

def plot_idle_employee_percentages(result_df, output_dir=None):
    """Plot the idle machine percentages."""
    if result_df.empty:
        print("No data available for plotting.")
        return

    # Create output directory if it doesn't exist
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # Set up a larger plot with a colorful style
    plt.figure(figsize=(15, 10))
    sns.set_style("whitegrid")
    
    # Create labels for x-axis
    result_df["shift_label"] = result_df.apply(
        lambda row: f"{row['day']} (Ca {row['shift']})", 
        axis=1
    )
    
    # Get unique machine types
    employee_positions = result_df["employee_position"].unique()
    
    # Create a grouped bar chart
    ax = plt.subplot(111)
    
    # Color palette
    colors = sns.color_palette("viridis", len(employee_positions))
    
    # Plot for each machine type
    for i, employee_position in enumerate(employee_positions):
        data = result_df[result_df["employee_position"] == employee_position]
        ax.scatter(
            data["shift_label"],
            data["idle_percentage"],
            color=colors[i],
            s=60,
            label=employee_position
        )

    
    # Customize the plot
    plt.title("Tỷ lệ phần trăm nhân viên rảnh theo loại máy và ca làm việc", fontsize=16, fontweight='bold')
    plt.xlabel("Ngày và ca làm việc", fontsize=12)
    plt.ylabel("Tỷ lệ % nhân viên rảnh", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Add legend outside of the plot
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
    
    # Annotate with exact percentages
    for employee_position in employee_positions:
        data = result_df[result_df["employee_position"] == employee_position]
        for i, row in data.iterrows():
            ax.annotate(
                f"{row['idle_percentage']:.1f}%",
                xy=(row["shift_label"], row["idle_percentage"]),
                xytext=(0, 10),
                textcoords="offset points",
                ha='center',
                fontsize=8,
                bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.7)
            )
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the figure
    if output_dir:
        plt.savefig(os.path.join(output_dir, "employee_idle_percentages.png"), dpi=300, bbox_inches='tight')
        print(f"Figure saved to {os.path.join(output_dir, 'employee_idle_percentages.png')}")
    
    # Show the plot
    plt.show()

def plot_employee_position_idle_rates(result_df, output_dir=None):
    """Plot a separate line chart for each employee type."""
    if result_df.empty:
        print("No data available for plotting.")
        return
        
    # Create output directory if it doesn't exist
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    # Get unique employee types
    employee_positions = sorted(result_df["employee_position"].unique())
    
    # Calculate number of rows and columns for subplots
    n_types = len(employee_positions)
    n_cols = min(3, n_types)
    n_rows = (n_types + n_cols - 1) // n_cols  # Ceiling division
    
    # Create figure and subplots
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 4*n_rows))
    
    # Make axes iterable even when there's only one subplot
    if n_rows == 1 and n_cols == 1:
        axes = np.array([axes])
    axes = axes.flatten()
    
    # Plot each employee type
    for i, employee_position in enumerate(employee_positions):
        ax = axes[i]
        
        # Filter data for this employee type
        data = result_df[result_df["employee_position"] == employee_position]
        
        # Create labels for x-axis
        data["shift_label"] = data.apply(
            lambda row: f"{row['day']} (Ca {row['shift']})", 
            axis=1
        )
        
        # Plot the line
        ax.scatter(
            data["shift_label"],
            data["idle_percentage"],
            color=sns.color_palette("viridis")[i % 10],
            s=50
        )

        
        # Add data points with percentages
        for j, row in data.iterrows():
            ax.annotate(
                f"{row['idle_percentage']:.1f}%",
                xy=(row["shift_label"], row["idle_percentage"]),
                xytext=(0, 5),
                textcoords="offset points",
                ha='center',
                fontsize=8,
                bbox=dict(boxstyle='round,pad=0.2', fc='white', alpha=0.7)
            )
        
        # Customize the plot
        ax.set_title(f"{employee_position}", fontsize=12)
        ax.set_ylim(0, 100)  # Set y-axis from 0-100%
        ax.set_ylabel("Tỷ lệ % nhân viên rảnh")
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.set_xticklabels(data["shift_label"], rotation=45, ha='right', fontsize=8)
        
        # Add a horizontal line at 0%
        ax.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
        
    # Hide any unused subplots
    for i in range(len(employee_positions), len(axes)):
        axes[i].set_visible(False)
    
    # Adjust layout
    plt.tight_layout()
    plt.suptitle("Tỷ lệ phần trăm nhân viên rảnh theo loại máy và ca làm việc", fontsize=16, y=1.02)
    
    # Save the figure
    if output_dir:
        plt.savefig(os.path.join(output_dir, "employee_idle_percentages_by_position.png"), dpi=300, bbox_inches='tight')
        print(f"Figure saved to {os.path.join(output_dir, 'employee_idle_percentages_by_position.png')}")
    
    # Show the plot
    plt.show()

def create_heatmap_visualization(result_df, output_dir=None):
    """Create a heatmap visualization of idle employee percentages."""
    if result_df.empty:
        print("No data available for heatmap visualization.")
        return
        
    # Create output directory if it doesn't exist
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    # Create labels for x-axis
    result_df["shift_label"] = result_df.apply(
        lambda row: f"{row['day']} (Ca {row['shift']})", 
        axis=1
    )
    
    # Pivot the data to create a matrix suitable for a heatmap
    heatmap_data = result_df.pivot(
        index="employee_position",
        columns="shift_label",
        values="idle_percentage"
    )
    
    # Create the figure
    plt.figure(figsize=(16, 8))
    
    # Create the heatmap
    sns.heatmap(
        heatmap_data,
        annot=True,
        fmt=".1f",
        cmap="YlGnBu_r",  # Reversed so darker blue means more idle machines
        cbar_kws={'label': '% nhan vien'},
        linewidths=0.5
    )
    
    # Customize the plot
    plt.title("Tỷ lệ phần trăm nhan vien theo vi tri và ca làm việc", fontsize=16)
    plt.xlabel("Ngày và ca làm việc", fontsize=12)
    plt.ylabel("Loại vi tri", fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the figure
    if output_dir:
        plt.savefig(os.path.join(output_dir, "employee_idle_percentage_heatmap.png"), dpi=300, bbox_inches='tight')
        print(f"Heatmap saved to {os.path.join(output_dir, 'employee_idle_percentage_heatmap.png')}")
    
    # Show the plot
    plt.show()

def write_summary_to_csv(result_df, output_dir=None):
    """Write summary information to a CSV file."""
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        
        # Create a more detailed DataFrame for the CSV
        csv_data = result_df.copy()
        csv_data["shift_label"] = csv_data.apply(
            lambda row: f"{row['day']} (Ca {row['shift']})", 
            axis=1
        )
        
        # Reorder columns for better readability
        csv_data = csv_data[[
            "day", "shift", "shift_label", "employee_position",
            "total_count", "used_count", "idle_count", "idle_percentage"
        ]]
        
        # Save to CSV
        csv_path = os.path.join(output_dir, "position_idle_percentages.csv")
        csv_data.to_csv(csv_path, index=False)
        print(f"Data saved to {csv_path}")

def main():
    # Create output directory
    output_dir = "e:/WorkSpace/kpi_2/thuat_toan/KPI/visualization/outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    # Load data
    print("Loading data...")
    schedule_data, input_data = load_data()
    
    # Extract machine types
    print("Extracting machine types...")
    employee_positions = extract_employee_positions(input_data)
    print(f"Found {len(employee_positions)} machine types")
    
    # Create mappings
    print("Creating mappings...")
    employee_position_to_employees = extract_employee_position_to_employees(input_data)
    operation_to_employee_position = extract_operation_to_employee_position(input_data)
    
    # Extract detailed schedules
    print("Extracting detailed schedules...")
    detailed_schedules = extract_detailed_schedules(schedule_data)
    print(f"Found {len(detailed_schedules)} detailed schedule entries")
    
    # Calculate idle percentages
    print("Calculating idle percentages...")
    result_df = calculate_employee_idle_percentages(
        detailed_schedules, employee_position_to_employees, operation_to_employee_position
    )
    
    if result_df.empty:
        print("No valid data available for visualization.")
        return
    
    print(f"Analysis completed with {len(result_df)} data points across {len(result_df['employee_position'].unique())} employee types")
    
    # Plot the results
    print("Creating visualizations...")
    plot_idle_employee_percentages(result_df, output_dir)
    plot_employee_position_idle_rates(result_df, output_dir)
    create_heatmap_visualization(result_df, output_dir)
    
    # Write summary to CSV
    write_summary_to_csv(result_df, output_dir)
    
    print("All visualizations have been created and saved to the outputs directory.")

if __name__ == "__main__":
    main()