import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import ast
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patches as mpatches

# Load the data
accessibility_df = pd.read_csv('Accessibility.csv')
department_df = pd.read_csv('Department.csv')
employee_df = pd.read_csv('Employees_table.csv')

# Clean and preprocess the data
employee_df['Access_ID'] = employee_df['Access_ID'].apply(ast.literal_eval)

# Merge dataframes to get department names
employee_with_dept = pd.merge(employee_df, department_df, on='Dept_ID')

# Create a lookup dictionary for access names
access_dict = dict(zip(accessibility_df['Access_ID'], accessibility_df['Access']))

# Print the data summary
print("Data Summary:")
print(f"Total employees: {len(employee_df)}")
print(f"Total departments: {len(department_df)}")
print(f"Total access types: {len(accessibility_df)}")
print("\n")

# Function to calculate risk score based on access patterns
def calculate_risk_score(access_list):
    """Calculate risk score based on access combinations and privileges"""
    # Base risk
    risk = len(access_list) * 5
    
    # Check for high-risk combinations
    if 28 in access_list:  # Full access is high risk
        risk += 50
    
    # External access combined with sensitive data access is risky
    if 3 in access_list and any(x in access_list for x in [8, 9, 10, 11, 12, 13, 14]):
        risk += 30
    
    # External communication tools with internal data
    if any(x in access_list for x in [5, 6]) and any(y in access_list for y in [8, 9, 10, 11, 12, 13, 14]):
        risk += 25
        
    # Multiple department access
    dept_access = sum(1 for x in access_list if x >= 8 and x <= 24)
    if dept_access > 3:
        risk += 15 * (dept_access - 3)
    
    return min(risk, 100)  # Cap at 100

# Calculate risk score for each employee
employee_with_dept['Risk_Score'] = employee_with_dept['Access_ID'].apply(calculate_risk_score)

# Identify high-risk employees (risk score > 60)
high_risk_employees = employee_with_dept[employee_with_dept['Risk_Score'] > 60].sort_values(by='Risk_Score', ascending=False)

print("High Risk Employees:")
for _, row in high_risk_employees.iterrows():
    print(f"{row['Emp_name']} (Dept: {row['Dept_Name']}) - Risk Score: {row['Risk_Score']}")
    access_names = [access_dict[access_id] for access_id in row['Access_ID']]
    print(f"  Access: {', '.join(access_names)}")
    
    # Identify critical path for data breach
    critical_paths = []
    
    # Path 1: External communication with sensitive data
    if any(x in row['Access_ID'] for x in [3, 5, 6]):
        if any(y in row['Access_ID'] for y in [8, 9, 10, 11, 12, 13, 14]):
            critical_paths.append("External communication → Sensitive data exfiltration")
    
    # Path 2: Full access privilege escalation
    if 28 in row['Access_ID']:
        critical_paths.append("Full access → Unrestricted data access and potential privilege escalation")
    
    # Path 3: Cross-departmental data movement
    dept_systems = [x for x in row['Access_ID'] if x >= 8 and x <= 24]
    if len(dept_systems) > 2:
        critical_paths.append(f"Cross-departmental access → Data movement across {len(dept_systems)} departments")
    
    if critical_paths:
        print("  Critical Breach Paths:")
        for path in critical_paths:
            print(f"    - {path}")
    print("\n")

# Create data structure for analyzing access patterns
# Transform the data into a binary format for association rule mining
access_matrix = []

for _, row in employee_with_dept.iterrows():
    employee_access = {}
    for access_id in range(1, 29):  # For all possible access IDs (1-28)
        access_name = f"{access_dict.get(access_id, f'Unknown_{access_id}')}"
        employee_access[access_name] = 1 if access_id in row['Access_ID'] else 0
    access_matrix.append(employee_access)

access_df = pd.DataFrame(access_matrix)

# Apply Apriori algorithm for frequent itemsets
min_support = 0.58  # 58% support
frequent_itemsets = apriori(access_df, min_support=min_support, use_colnames=True)

# Generate association rules with minimum confidence of 70%
min_confidence = 0.7  # 70% confidence
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)

if len(rules) > 0:
    print("\nAssociation Rules for Potential Data Breach Pathways:")
    for idx, rule in rules.iterrows():
        antecedents = ', '.join(list(rule['antecedents']))
        consequents = ', '.join(list(rule['consequents']))
        print(f"Rule {idx+1}: {antecedents} → {consequents}")
        print(f"  Support: {rule['support']:.2f}, Confidence: {rule['confidence']:.2f}, Lift: {rule['lift']:.2f}")
        
        # Assess risk implication
        risk_level = "LOW"
        risk_explanation = ""
        
        # Check for external access leading to sensitive data
        if any(ext in antecedents for ext in ['Outlook_External', 'Gmail', 'Whatsapp']):
            if any(sens in consequents for sens in ['SD_IT_Analytics', 'SD_Cyberdata', 'SD_Quality_Daily_Reports']):
                risk_level = "HIGH"
                risk_explanation = "External communication tool access implies access to sensitive data systems"
        
        # Check for cross-departmental access
        sd_systems_ant = sum(1 for x in list(rule['antecedents']) if 'SD_' in x)
        sd_systems_cons = sum(1 for x in list(rule['consequents']) if 'SD_' in x)
        if sd_systems_ant > 0 and sd_systems_cons > 0:
            risk_level = "MEDIUM" if risk_level != "HIGH" else risk_level
            risk_explanation += " Cross-departmental data access pattern detected."
            
        # Full access implications
        if 'Full_access' in consequents:
            risk_level = "HIGH"
            risk_explanation += " Pattern leads to full system access."
        
        print(f"  Risk Assessment: {risk_level} - {risk_explanation}")
        print()
else:
    print("No significant association rules found with the given support and confidence thresholds.")

# Visualization 1: Network Graph of Access Patterns
print("\nGenerating network visualization of access patterns...")

# Create a graph
G = nx.Graph()

# Add employee nodes
for _, row in employee_with_dept.iterrows():
    G.add_node(row['Emp_name'], node_type='employee', department=row['Dept_Name'], 
               risk_score=row['Risk_Score'])

# Add access system nodes
for _, row in accessibility_df.iterrows():
    G.add_node(row['Access'], node_type='access')

# Add edges between employees and their access systems
for _, row in employee_with_dept.iterrows():
    for access_id in row['Access_ID']:
        if access_id in access_dict:
            G.add_edge(row['Emp_name'], access_dict[access_id])

# Draw the graph
plt.figure(figsize=(16, 12))
pos = nx.spring_layout(G, k=0.5, iterations=50)

# Draw employee nodes with risk-based coloring
employee_nodes = [node for node, data in G.nodes(data=True) if data.get('node_type') == 'employee']
risk_scores = [G.nodes[node]['risk_score'] for node in employee_nodes]
cmap = plt.cm.YlOrRd
employee_colors = [cmap(score/100) for score in risk_scores]

nx.draw_networkx_nodes(G, pos, nodelist=employee_nodes, node_color=employee_colors, 
                       node_size=300, alpha=0.8)

# Draw access system nodes
access_nodes = [node for node, data in G.nodes(data=True) if data.get('node_type') == 'access']
nx.draw_networkx_nodes(G, pos, nodelist=access_nodes, node_color='lightblue', 
                       node_shape='s', node_size=200, alpha=0.8)

# Draw edges
nx.draw_networkx_edges(G, pos, width=0.5, alpha=0.5)

# Add labels
nx.draw_networkx_labels(G, pos, font_size=8)

# Create legend
risk_levels = ['Low Risk (0-30)', 'Medium Risk (30-60)', 'High Risk (60-100)']
risk_colors = [cmap(0.2), cmap(0.5), cmap(0.8)]
risk_patches = [mpatches.Patch(color=color, label=label) for color, label in zip(risk_colors, risk_levels)]
access_patch = mpatches.Patch(color='lightblue', label='Access System')
plt.legend(handles=risk_patches + [access_patch], loc='upper right')

plt.title('Employee Access Network with Risk Assessment', fontsize=16)
plt.tight_layout()
plt.savefig('access_network.png', dpi=300)
plt.close()

# Visualization 2: Heatmap of employee access patterns
print("Generating heatmap of employee access patterns...")

# Create a matrix of employee vs access types
heat_data = []
emp_names = []

    # Create unique identifiers for employees (using index to ensure uniqueness)
for idx, row in employee_with_dept.iterrows():
    # Use row index as unique identifier since Emp_ID column doesn't exist
    emp_id = f"{row['Emp_name']}_{idx}"
    emp_names.append(emp_id)
    emp_access = [1 if access_id in row['Access_ID'] else 0 for access_id in range(1, 29)]
    heat_data.append(emp_access)

heat_df = pd.DataFrame(heat_data, columns=[access_dict.get(i, f'Unknown_{i}') for i in range(1, 29)])
heat_df.index = emp_names

# Sort employees by department and risk score
sorted_indices = []
for idx, row in employee_with_dept.sort_values(by=['Dept_ID', 'Risk_Score'], ascending=[True, False]).iterrows():
    sorted_indices.append(f"{row['Emp_name']}_{idx}")

# Safely reindex the dataframe
heat_df = heat_df.reindex(sorted_indices)

# Create department labels for y-axis (shortened for readability)
dept_labels = []
for name in heat_df.index:
    # Extract employee name (remove the ID part)
    emp_name = name.split('_')[0]
    # Find department name
    dept_row = employee_with_dept[employee_with_dept['Emp_name'] == emp_name]
    if not dept_row.empty:
        dept_name = dept_row.iloc[0]['Dept_Name']
        dept_labels.append(f"{emp_name} ({dept_name})")
    else:
        dept_labels.append(name)  # Fallback

# Create a custom colormap that transitions from white to red
colors = [(1, 1, 1), (1, 0.8, 0.8), (1, 0.5, 0.5), (1, 0, 0)]
cmap_name = 'white_to_red'
cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=100)

plt.figure(figsize=(18, 12))
sns.heatmap(heat_df, cmap=cm, cbar_kws={'label': 'Access Granted'})
plt.yticks(np.arange(len(dept_labels)) + 0.5, dept_labels, fontsize=8)
plt.xticks(rotation=90, fontsize=8)
plt.title('Employee Access Patterns by Department', fontsize=16)
plt.tight_layout()
plt.savefig('access_heatmap.png', dpi=300)
plt.close()

# Visualization 3: Critical path graph
print("Generating critical path visualization...")

# Create directed graph for critical paths
CP = nx.DiGraph()

# Add department nodes
for _, row in department_df.iterrows():
    CP.add_node(row['Dept_Name'], node_type='department')

# Add access system nodes
for _, row in accessibility_df.iterrows():
    CP.add_node(row['Access'], node_type='access')

# Add critical high-risk edges based on identified patterns
critical_edges = []

# From association rules
if len(rules) > 0:
    for _, rule in rules.iterrows():
        for antecedent in rule['antecedents']:
            for consequent in rule['consequents']:
                if rule['lift'] > 1.5 and rule['confidence'] > 0.7:
                    CP.add_edge(antecedent, consequent, weight=rule['lift'], 
                                confidence=rule['confidence'], edge_type='rule')
                    critical_edges.append((antecedent, consequent))

# Add edges from high risk employees
for _, row in high_risk_employees.iterrows():
    access_list = [access_dict[access_id] for access_id in row['Access_ID']]
    
    # Connect external communication to sensitive data systems
    ext_comms = ['Outlook_External', 'Gmail', 'Whatsapp']
    sensitive_systems = ['SD_IT_Analytics', 'SD_Cyberdata', 'SD_Quality_Daily_Reports', 
                         'SD_Data_Analytics', 'SD_Daily_Reports']
    
    ext_access = [access for access in access_list if access in ext_comms]
    sensitive_access = [access for access in access_list if access in sensitive_systems]
    
    for ext in ext_access:
        for sens in sensitive_access:
            CP.add_edge(ext, sens, weight=2.0, employee=row['Emp_name'], 
                        department=row['Dept_Name'], edge_type='critical')
            critical_edges.append((ext, sens))
    
    # Connect department to sensitive data access
    if ext_access or access_list:
        CP.add_edge(row['Dept_Name'], ext_access[0] if ext_access else access_list[0], 
                    weight=1.0, employee=row['Emp_name'], edge_type='dept')

# Draw the critical path graph
plt.figure(figsize=(16, 12))
pos = nx.spring_layout(CP, k=0.3, iterations=50)

# Draw nodes with different colors by type
dept_nodes = [node for node, data in CP.nodes(data=True) if data.get('node_type') == 'department']
access_nodes = [node for node, data in CP.nodes(data=True) if data.get('node_type') == 'access']

nx.draw_networkx_nodes(CP, pos, nodelist=dept_nodes, node_color='green', 
                       node_size=300, alpha=0.8)
nx.draw_networkx_nodes(CP, pos, nodelist=access_nodes, node_color='skyblue', 
                       node_size=200, alpha=0.8)

# Draw edges with colors by type
rule_edges = [(u, v) for u, v, d in CP.edges(data=True) if d.get('edge_type') == 'rule']
critical_edges = [(u, v) for u, v, d in CP.edges(data=True) if d.get('edge_type') == 'critical']
dept_edges = [(u, v) for u, v, d in CP.edges(data=True) if d.get('edge_type') == 'dept']

nx.draw_networkx_edges(CP, pos, edgelist=rule_edges, edge_color='orange', width=1.5, alpha=0.7)
nx.draw_networkx_edges(CP, pos, edgelist=critical_edges, edge_color='red', width=2.5, alpha=0.9)
nx.draw_networkx_edges(CP, pos, edgelist=dept_edges, edge_color='green', width=1.0, alpha=0.5)

# Add labels
nx.draw_networkx_labels(CP, pos, font_size=8)

# Create legend
dept_patch = mpatches.Patch(color='green', label='Department')
access_patch = mpatches.Patch(color='skyblue', label='Access System')
rule_line = mpatches.Patch(color='orange', label='Association Rule Path')
critical_line = mpatches.Patch(color='red', label='Critical Breach Path')
dept_line = mpatches.Patch(color='green', label='Department Access Path')

plt.legend(handles=[dept_patch, access_patch, rule_line, critical_line, dept_line], loc='upper right')

plt.title('Critical Data Breach Pathways', fontsize=16)
plt.tight_layout()
plt.savefig('critical_paths.png', dpi=300)
plt.close()

print("\nAnalysis complete. Visualizations saved as PNG files.")
print("Summary of findings:")
print(f"1. Identified {len(high_risk_employees)} high-risk employees with potential for data breaches")
print(f"2. Generated {len(rules) if 'rules' in locals() else 0} association rules with {min_confidence*100}% confidence and {min_support*100}% support")
print("3. Created network visualizations showing access patterns and critical breach paths")
print("\nRecommendations:")
print("1. Review and limit external communication access for employees with sensitive data access")
print("2. Implement department-based access controls to prevent cross-departmental data movement")
print("3. Regularly audit access patterns, especially for high-risk employees")
print("4. Consider implementing least-privilege access model by removing unnecessary access rights")