# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# import ast
# import networkx as nx
# from collections import defaultdict

# # 1. Import and prepare datasets
# # ==============================

# # Import access types data
# access_data = pd.read_csv('Accessibility.csv')
# print("Access data loaded:", access_data.shape)

# # Import employee data
# employee_data = pd.read_csv('Employees_table.csv')
# # Convert string representation of lists to actual lists
# employee_data['Access_ID'] = employee_data['Access_ID'].apply(ast.literal_eval)
# print("Employee data loaded:", employee_data.shape)

# # Import department data
# department_data = pd.read_csv('Department.csv')
# print("Department data loaded:", department_data.shape)

# # Merge department names into employee data
# employee_data = employee_data.merge(department_data, on='Dept_ID', how='left')
# print("\nEmployees with department names:")
# print(employee_data.head())

# # 2. Define risk weights for access types
# # ======================================
# # Higher weights for more sensitive access
# access_risk_weights = {
#     1: 1,  # Teams - low risk
#     2: 2,  # Outlook_Internal
#     3: 5,  # Outlook_External - higher risk (external communication)
#     4: 2,  # Outlook_Internal_Dept
#     5: 7,  # Gmail - high risk (external personal email)
#     6: 7,  # Whatsapp - high risk (external messaging)
#     7: 3,  # Survey_Genius
#     8: 4,  # SD_IT_Analytics
#     9: 8,  # SD_Cyberdata - very high risk (security data)
#     10: 4,  # SD_Quality_Daily_Reports
#     11: 5,  # SD_Data_Analytics
#     12: 6,  # SD_Mahindra
#     13: 4,  # SD_Daily_Lat_long
#     14: 4,  # SD_Daily_Reports
#     15: 6,  # SD_HR_Common - sensitive HR data
#     16: 7,  # SD_Accounts_HO - sensitive financial data
#     17: 5,  # SD_Operations
#     18: 4,  # SD_Training_L&D
#     19: 4,  # SD_Quality
#     20: 6,  # SD_CRIS
#     21: 7,  # SD_Govt_Projects - sensitive government data
#     22: 7,  # SD_CMI_Partnership
#     23: 3,  # SD_Designer
#     24: 3,  # SD_Researcher
#     25: 2,  # DTP
#     26: 5,  # AMI Projects
#     27: 4,  # SD_Marketing
#     28: 10  # Full_access - highest risk
# }

# # Group access types into functional categories for better scenario identification
# access_categories = {
#     'external_comm': [3, 5, 6],  # External communication channels
#     'sensitive_data': [9, 15, 16, 21, 22],  # Highly sensitive data
#     'analytics': [8, 10, 11, 13, 14],  # Analytics and reporting tools
#     'operational': [12, 17, 19, 20],  # Operational systems
#     'design_research': [23, 24, 25, 27],  # Design and research tools
#     'project_specific': [7, 18, 26],  # Project-specific tools
#     'super_access': [28]  # Full access
# }

# # 3. Calculate risk scores for each employee
# # =========================================
# def calculate_risk_score(access_list):
#     base_score = sum(access_risk_weights.get(access_id, 0) for access_id in access_list)
    
#     # Extra risk for dangerous combinations
#     # Example: External communication tools + sensitive data access
#     has_external_comm = any(access_id in access_categories['external_comm'] for access_id in access_list)
#     has_sensitive_data = any(access_id in access_categories['sensitive_data'] for access_id in access_list)
#     has_analytics = any(access_id in access_categories['analytics'] for access_id in access_list)
#     has_full_access = any(access_id in access_categories['super_access'] for access_id in access_list)
    
#     combo_risk = 0
#     if has_external_comm and has_sensitive_data:
#         combo_risk += 15  # High risk combo: external comm + sensitive data
#     if has_full_access and has_external_comm:
#         combo_risk += 25  # Very high risk: full access + external communication
#     if has_sensitive_data and has_analytics:
#         combo_risk += 10  # Risky: Can analyze sensitive data and potentially extract insights
#     if has_external_comm and has_analytics and has_sensitive_data:
#         combo_risk += 20  # Very high risk: Can analyze, access sensitive data and send externally
        
#     return base_score + combo_risk

# # Calculate risk score for each employee
# employee_data['Risk_Score'] = employee_data['Access_ID'].apply(calculate_risk_score)

# # 4. Calculate department averages and identify outliers
# # ====================================================
# dept_avg_risk = employee_data.groupby('Dept_Name')['Risk_Score'].mean().reset_index()
# dept_avg_risk = dept_avg_risk.rename(columns={'Risk_Score': 'Avg_Dept_Risk'})

# # Merge department average risk back to employee data
# employee_data = employee_data.merge(dept_avg_risk, on='Dept_Name', how='left')

# # Calculate how much each employee deviates from their department average
# employee_data['Risk_Deviation'] = employee_data['Risk_Score'] - employee_data['Avg_Dept_Risk']

# # 5. Identify potential data breach pathways and scenarios
# # ======================================================
# def identify_breach_pathways(employee):
#     """Identify specific data breach scenarios based on access combinations"""
#     pathways = []
#     scenarios = []
#     access_ids = employee['Access_ID']
    
#     # Check employee's access against our defined categories
#     has_access = {}
#     for category, id_list in access_categories.items():
#         has_access[category] = any(id in access_ids for id in id_list)
    
#     # PATHWAY ANALYSIS
#     # ----------------
    
#     # Pathway 1: External email + sensitive data
#     if has_access['external_comm'] and has_access['sensitive_data']:
#         pathways.append("External Email → Sensitive Data")
        
#         # Add specific breach scenarios based on which sensitive systems they can access
#         if 9 in access_ids:  # SD_Cyberdata
#             scenarios.append("Could exfiltrate security data via external email")
#         if 16 in access_ids:  # SD_Accounts_HO
#             scenarios.append("Could leak financial data through personal communication channels")
#         if 21 in access_ids:  # SD_Govt_Projects
#             scenarios.append("Government project data at risk of external exposure")
    
#     # Pathway 2: Full access + external communication
#     if has_access['super_access'] and has_access['external_comm']:
#         pathways.append("Full System Access → External Communication")
#         scenarios.append("Has unrestricted data access with external communication channels")
        
#         # Check for specific high-risk external channels
#         if 5 in access_ids:  # Gmail
#             scenarios.append("Could send company data to personal Gmail account")
#         if 6 in access_ids:  # WhatsApp
#             scenarios.append("WhatsApp presents unmonitored communication channel for sensitive data")
    
#     # Pathway 3: Access to multiple departments' data
#     dept_specific = [access for access in access_ids if access >= 10 and access < 28]
#     if len(dept_specific) >= 3:
#         pathways.append("Cross-Department Data Access")
#         scenarios.append(f"Has access to {len(dept_specific)} department-specific systems")
        
#         # High risk: Cross-department access + external comm
#         if has_access['external_comm']:
#             scenarios.append("Can correlate data across departments and send externally")
    
#     # Pathway 4: Financial data + external communication
#     if 16 in access_ids and has_access['external_comm']:
#         pathways.append("Financial Data → External Communication")
#         scenarios.append("Financial data could be exfiltrated through external channels")
    
#     # NEW PATHWAY 5: Analytics tools + sensitive data + external comm
#     if has_access['analytics'] and has_access['sensitive_data'] and has_access['external_comm']:
#         pathways.append("Analytics → Sensitive Data → External Communication")
#         scenarios.append("Could analyze sensitive data and exfiltrate insights")
        
#         # Specific high-risk analytics scenarios
#         if 11 in access_ids:  # SD_Data_Analytics
#             scenarios.append("Data analytics tools could be used to identify high-value information")
    
#     # NEW PATHWAY 6: Cross-function access (IT + Finance)
#     if 8 in access_ids and 16 in access_ids:  # IT Analytics + Financial data
#         pathways.append("IT Analytics → Financial Data")
#         scenarios.append("Technical skills combined with financial data access creates fraud risk")
    
#     # NEW PATHWAY 7: HR data exposure
#     if 15 in access_ids and has_access['external_comm']:
#         pathways.append("HR Data → External Communication")
#         scenarios.append("Employee personal data could be leaked externally")
    
#     # NEW PATHWAY 8: Competitor intelligence risk
#     if has_access['design_research'] and has_access['external_comm'] and has_access['project_specific']:
#         pathways.append("Research & Design → External Communication")
#         scenarios.append("Intellectual property/design research could leak to competitors")
    
#     # NEW PATHWAY 9: Multi-platform external communication risk
#     external_channels = [id for id in access_ids if id in [3, 5, 6]]
#     if len(external_channels) >= 2:
#         pathways.append("Multiple External Communication Channels")
#         scenarios.append(f"Uses {len(external_channels)} different external communication methods, complicating monitoring")
    
#     # NEW PATHWAY 10: Supply chain risk
#     if 12 in access_ids and has_access['external_comm']:  # SD_Mahindra + external comm
#         pathways.append("Supply Chain Data → External Communication")
#         scenarios.append("Vendor/supply chain data could be leaked to competitors")
    
#     return pathways, scenarios

# # Apply the function to identify breach pathways and scenarios
# breach_analysis = employee_data.apply(
#     lambda emp: pd.Series(identify_breach_pathways(emp), index=['Breach_Pathways', 'Breach_Scenarios']), 
#     axis=1
# )
# employee_data = pd.concat([employee_data, breach_analysis], axis=1)
# employee_data['Num_Pathways'] = employee_data['Breach_Pathways'].apply(len)
# employee_data['Num_Scenarios'] = employee_data['Breach_Scenarios'].apply(len)

# # 6. Generate a comprehensive security report
# # =========================================
# print("\n=== ENHANCED SECURITY RISK ANALYSIS REPORT ===")

# # Top 5 highest risk employees
# print("\nTop 5 Highest Risk Employees:")
# high_risk_employees = employee_data.sort_values('Risk_Score', ascending=False).head(5)
# for _, row in high_risk_employees.iterrows():
#     print(f"{row['Emp_name']} (Dept: {row['Dept_Name']}) - Risk Score: {row['Risk_Score']}")
#     print(f"  Access Count: {len(row['Access_ID'])}")
#     print(f"  Potential Breach Pathways:")
#     for pathway in row['Breach_Pathways']:
#         print(f"    - {pathway}")
#     print(f"  Breach Scenarios:")
#     for scenario in row['Breach_Scenarios']:
#         print(f"    - {scenario}")
#     print()

# # Department risk summary
# print("\nDepartment Risk Summary:")
# dept_risk = employee_data.groupby('Dept_Name').agg({
#     'Risk_Score': ['mean', 'max', 'count'],
#     'Num_Pathways': 'sum',
#     'Num_Scenarios': 'sum'
# }).reset_index()
# dept_risk.columns = ['Department', 'Avg_Risk', 'Max_Risk', 'Employee_Count', 'Total_Breach_Pathways', 'Total_Breach_Scenarios']
# print(dept_risk.sort_values('Avg_Risk', ascending=False))

# # 7. Detailed Breach Scenario Analysis
# # ===================================
# print("\n=== DETAILED BREACH SCENARIO ANALYSIS ===")

# # Count occurrences of each breach pathway
# pathway_counts = defaultdict(int)
# for pathways in employee_data['Breach_Pathways']:
#     for path in pathways:
#         pathway_counts[path] += 1

# # Sort and display most common breach pathways
# print("\nMost Common Breach Pathways:")
# for pathway, count in sorted(pathway_counts.items(), key=lambda x: x[1], reverse=True):
#     print(f"{pathway}: {count} employees")

# # Count occurrences of each breach scenario
# scenario_counts = defaultdict(int)
# for scenarios in employee_data['Breach_Scenarios']:
#     for scenario in scenarios:
#         scenario_counts[scenario] += 1

# # Sort and display most common breach scenarios
# print("\nMost Common Breach Scenarios:")
# for scenario, count in sorted(scenario_counts.items(), key=lambda x: x[1], reverse=True):
#     print(f"{scenario}: {count} employees")

# # 8. Cross-departmental Risk Analysis
# # =================================
# print("\n=== CROSS-DEPARTMENTAL RISK ANALYSIS ===")

# # Employees with access across multiple departments
# cross_dept_employees = employee_data[employee_data['Breach_Pathways'].apply(
#     lambda paths: "Cross-Department Data Access" in paths if paths else False
# )]

# if not cross_dept_employees.empty:
#     print(f"\nFound {len(cross_dept_employees)} employees with cross-department access:")
#     for _, emp in cross_dept_employees.iterrows():
#         dept_systems = [id for id in emp['Access_ID'] if id >= 10 and id < 28]
#         print(f"{emp['Emp_name']} ({emp['Dept_Name']}) - Access to {len(dept_systems)} department systems")
#         # Show which department systems they access
#         dept_access = []
#         for access_id in dept_systems:
#             access_name = next((row['Access'] for _, row in access_data.iterrows() 
#                                if row['Access_ID'] == access_id), f"Access_{access_id}")
#             dept_access.append(access_name)
#         print(f"  Department systems: {', '.join(dept_access)}")
# else:
#     print("No employees with significant cross-departmental access found.")

# # 9. Data Exfiltration Path Analysis
# # ================================
# print("\n=== DATA EXFILTRATION PATH ANALYSIS ===")

# # Focus on employees with both sensitive data access and external communication channels
# exfil_risk = employee_data[employee_data['Breach_Pathways'].apply(
#     lambda paths: any("External" in path for path in paths) if paths else False
# )]

# if not exfil_risk.empty:
#     print(f"\nFound {len(exfil_risk)} employees with data exfiltration risk:")
    
#     # Categorize by exfiltration risk level
#     exfil_risk['Exfil_Risk'] = exfil_risk.apply(
#         lambda emp: "CRITICAL" if "Full System Access → External Communication" in emp['Breach_Pathways'] 
#                    else "HIGH" if "Analytics → Sensitive Data → External Communication" in emp['Breach_Pathways']
#                    else "MEDIUM" if "Financial Data → External Communication" in emp['Breach_Pathways']
#                    else "LOW",
#         axis=1
#     )
    
#     # Display by risk category
#     for risk_level in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
#         risk_group = exfil_risk[exfil_risk['Exfil_Risk'] == risk_level]
#         if not risk_group.empty:
#             print(f"\n{risk_level} Exfiltration Risk ({len(risk_group)} employees):")
#             for _, emp in risk_group.iterrows():
#                 print(f"  {emp['Emp_name']} ({emp['Dept_Name']}) - Risk Score: {emp['Risk_Score']}")
#                 # Show external channels they have access to
#                 ext_channels = []
#                 for access_id in emp['Access_ID']:
#                     if access_id in [3, 5, 6]:  # External communication channels
#                         access_name = next((row['Access'] for _, row in access_data.iterrows() 
#                                         if row['Access_ID'] == access_id), f"Access_{access_id}")
#                         ext_channels.append(access_name)
#                 print(f"    External channels: {', '.join(ext_channels)}")
# else:
#     print("No employees with significant data exfiltration risk found.")

# # 10. Visualize the results
# # =======================
# # Plot risk scores by department
# plt.figure(figsize=(12, 6))
# sns.boxplot(x='Dept_Name', y='Risk_Score', data=employee_data)
# plt.xticks(rotation=45, ha='right')
# plt.title('Risk Score Distribution by Department')
# plt.tight_layout()
# plt.savefig('risk_by_department.png')

# # Plot employees with highest risk deviation
# top_deviations = employee_data.sort_values('Risk_Deviation', ascending=False).head(10)
# plt.figure(figsize=(12, 6))
# sns.barplot(x='Emp_name', y='Risk_Deviation', data=top_deviations)
# plt.xticks(rotation=45, ha='right')
# plt.title('Top 10 Employees with Highest Risk Deviation from Department Average')
# plt.tight_layout()
# plt.savefig('risk_deviation.png')

# # Plot breach pathway distribution
# pathway_df = pd.DataFrame([(path, count) for path, count in pathway_counts.items()], 
#                          columns=['Pathway', 'Count'])
# pathway_df = pathway_df.sort_values('Count', ascending=False)

# plt.figure(figsize=(14, 8))
# sns.barplot(x='Count', y='Pathway', data=pathway_df)
# plt.title('Distribution of Potential Data Breach Pathways')
# plt.tight_layout()
# plt.savefig('breach_pathways.png')

# # 11. Save detailed risk report
# # ===========================
# with open('enhanced_security_risk_report.txt', 'w') as f:
#     f.write("ENHANCED SECURITY RISK REPORT\n")
#     f.write("=============================\n\n")
    
#     # Summary statistics
#     f.write("SUMMARY STATISTICS\n")
#     f.write("-----------------\n")
#     f.write(f"Total employees analyzed: {len(employee_data)}\n")
#     f.write(f"Employees with at least one breach pathway: {len(employee_data[employee_data['Num_Pathways'] > 0])}\n")
#     f.write(f"Employees with critical exfiltration risk: {len(exfil_risk[exfil_risk['Exfil_Risk'] == 'CRITICAL']) if 'exfil_risk' in locals() else 'N/A'}\n")
#     f.write(f"Total potential breach scenarios identified: {sum(employee_data['Num_Scenarios'])}\n\n")
    
#     # Department risk ranking
#     f.write("DEPARTMENT RISK RANKING\n")
#     f.write("----------------------\n")
#     for _, dept in dept_risk.sort_values('Avg_Risk', ascending=False).iterrows():
#         f.write(f"{dept['Department']}: Avg Risk = {dept['Avg_Risk']:.2f}, Max Risk = {dept['Max_Risk']}, "
#                 f"Breach Pathways = {dept['Total_Breach_Pathways']}, Scenarios = {dept['Total_Breach_Scenarios']}\n")
#     f.write("\n")
    
#     # Top 10 highest risk employees
#     f.write("TOP 10 HIGHEST RISK EMPLOYEES\n")
#     f.write("--------------------------\n")
#     top_risk = employee_data.sort_values('Risk_Score', ascending=False).head(10)
#     for _, emp in top_risk.iterrows():
#         f.write(f"Employee: {emp['Emp_name']} (Department: {emp['Dept_Name']})\n")
#         f.write(f"Risk Score: {emp['Risk_Score']} (Department Avg: {emp['Avg_Dept_Risk']:.2f})\n")
#         f.write(f"Access IDs: {emp['Access_ID']}\n")
#         f.write("Potential Breach Pathways:\n")
#         for pathway in emp['Breach_Pathways']:
#             f.write(f"  - {pathway}\n")
#         f.write("Breach Scenarios:\n")
#         for scenario in emp['Breach_Scenarios']:
#             f.write(f"  - {scenario}\n")
#         f.write("\n")
    
#     # Most common breach scenarios
#     f.write("MOST COMMON BREACH SCENARIOS\n")
#     f.write("---------------------------\n")
#     for scenario, count in sorted(scenario_counts.items(), key=lambda x: x[1], reverse=True):
#         f.write(f"{scenario}: {count} employees\n")
#     f.write("\n")
    
#     # Detailed employee breach profiles
#     f.write("DETAILED EMPLOYEE BREACH PROFILES\n")
#     f.write("-------------------------------\n")
#     high_risk_emps = employee_data[employee_data['Num_Pathways'] > 0].sort_values('Risk_Score', ascending=False)
    
#     for _, emp in high_risk_emps.iterrows():
#         f.write(f"Employee: {emp['Emp_name']} (Department: {emp['Dept_Name']})\n")
#         f.write(f"Risk Score: {emp['Risk_Score']} (Department Avg: {emp['Avg_Dept_Risk']:.2f})\n")
        
#         # List all access rights with names
#         f.write("Access Rights:\n")
#         for access_id in emp['Access_ID']:
#             access_name = next((row['Access'] for _, row in access_data.iterrows() 
#                               if row['Access_ID'] == access_id), f"Access_{access_id}")
#             f.write(f"  - {access_id}: {access_name}\n")
        
#         f.write("Potential Breach Pathways:\n")
#         for pathway in emp['Breach_Pathways']:
#             f.write(f"  - {pathway}\n")
            
#         f.write("Breach Scenarios:\n")
#         for scenario in emp['Breach_Scenarios']:
#             f.write(f"  - {scenario}\n")
#         f.write("\n")

# print("\nEnhanced Analysis complete. Results saved to:")
# print("- risk_by_department.png")
# print("- risk_deviation.png")
# print("- breach_pathways.png")
# print("- enhanced_security_risk_report.txt")

# # 12. Recommendations based on findings
# # ==================================
# print("\n=== SECURITY RECOMMENDATIONS ===")
# print("1. Review access rights for employees with high risk scores, especially those with multiple breach pathways")
# print("2. Implement additional monitoring for external communications from high-risk employees")
# print("3. Consider department-specific access policies where average risk scores are high")
# print("4. Audit all employees with 'Full_access' rights to ensure necessity")
# print("5. Implement separation of duties for employees with access to both sensitive data and external communication channels")
# print("6. Implement data loss prevention (DLP) solutions focused on external communication channels")
# print("7. Create role-based access control aligned with department needs")
# print("8. Develop an incident response plan specific to data exfiltration scenarios")
# print("9. Conduct regular security awareness training focused on data handling procedures")
# print("10. Implement just-in-time access for sensitive systems instead of permanent access")

# import streamlit as st
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# import ast
# import networkx as nx
# import io

# # Display title
# st.title("Employee Access Risk Analysis")

# # Upload CSV files
# st.sidebar.header("Upload your data files")
# access_file = st.sidebar.file_uploader("Upload Accessibility.csv", type=["csv"])
# employee_file = st.sidebar.file_uploader("Upload Employees_table.csv", type=["csv"])
# department_file = st.sidebar.file_uploader("Upload Department.csv", type=["csv"])

# # Process only if all files are uploaded
# if access_file and employee_file and department_file:
#     # Load data
#     access_data = pd.read_csv(access_file)
#     employee_data = pd.read_csv(employee_file)
#     department_data = pd.read_csv(department_file)

#     # Convert Access_ID strings to lists
#     employee_data['Access_ID'] = employee_data['Access_ID'].apply(ast.literal_eval)

#     # Merge department names
#     employee_data = employee_data.merge(department_data, on='Dept_ID', how='left')

#     # Define risk weights
#     access_risk_weights = {
#         1: 1, 2: 2, 3: 5, 4: 2, 5: 7, 6: 7, 7: 3, 8: 4, 9: 8, 10: 4,
#         11: 5, 12: 6, 13: 4, 14: 4, 15: 6, 16: 7, 17: 5, 18: 4, 19: 4,
#         20: 6, 21: 7, 22: 7, 23: 3, 24: 3, 25: 2, 26: 5, 27: 4, 28: 10
#     }

#     access_categories = {
#         'external_comm': [3, 5, 6],
#         'sensitive_data': [9, 15, 16, 21, 22],
#         'analytics': [8, 10, 11, 13, 14],
#         'operational': [12, 17, 19, 20],
#         'design_research': [23, 24, 25, 27],
#         'project_specific': [7, 18, 26],
#         'super_access': [28]
#     }

#     def calculate_risk_score(access_list):
#         base_score = sum(access_risk_weights.get(access_id, 0) for access_id in access_list)
#         has_external_comm = any(access_id in access_categories['external_comm'] for access_id in access_list)
#         has_sensitive_data = any(access_id in access_categories['sensitive_data'] for access_id in access_list)
#         has_analytics = any(access_id in access_categories['analytics'] for access_id in access_list)
#         has_full_access = any(access_id in access_categories['super_access'] for access_id in access_list)

#         combo_risk = 0
#         if has_external_comm and has_sensitive_data:
#             combo_risk += 15
#         if has_full_access and has_external_comm:
#             combo_risk += 25
#         if has_sensitive_data and has_analytics:
#             combo_risk += 10
#         if has_external_comm and has_analytics and has_sensitive_data:
#             combo_risk += 20
#         return base_score + combo_risk

#     employee_data['Risk_Score'] = employee_data['Access_ID'].apply(calculate_risk_score)

#     dept_avg_risk = employee_data.groupby('Dept_Name')['Risk_Score'].mean().reset_index()
#     dept_avg_risk = dept_avg_risk.rename(columns={'Risk_Score': 'Avg_Dept_Risk'})
#     employee_data = employee_data.merge(dept_avg_risk, on='Dept_Name', how='left')
#     employee_data['Risk_Deviation'] = employee_data['Risk_Score'] - employee_data['Avg_Dept_Risk']

#     def identify_breach_pathways(employee):
#         pathways = []
#         scenarios = []
#         access_ids = employee['Access_ID']
#         has_access = {}
#         for category, id_list in access_categories.items():
#             has_access[category] = any(id in access_ids for id in id_list)

#         if has_access['external_comm'] and has_access['sensitive_data']:
#             pathways.append("External Email → Sensitive Data")
#             if 9 in access_ids:
#                 scenarios.append("Could exfiltrate security data via external email")
#             if 16 in access_ids:
#                 scenarios.append("Could leak financial data through personal communication channels")
#             if 21 in access_ids:
#                 scenarios.append("Government project data at risk of external exposure")

#         if has_access['super_access'] and has_access['external_comm']:
#             pathways.append("Full System Access → External Communication")
#             scenarios.append("Has unrestricted data access with external communication channels")
#             if 5 in access_ids:
#                 scenarios.append("Could send company data to personal Gmail account")
#             if 6 in access_ids:
#                 scenarios.append("WhatsApp presents unmonitored communication channel for sensitive data")

#         dept_specific = [access for access in access_ids if 10 <= access < 28]
#         if len(dept_specific) >= 3:
#             pathways.append("Cross-Department Data Access")
#             scenarios.append(f"Has access to {len(dept_specific)} department-specific systems")
#             if has_access['external_comm']:
#                 scenarios.append("Can correlate data across departments and send externally")

#         if 16 in access_ids and has_access['external_comm']:
#             pathways.append("Financial Data → External Communication")
#             scenarios.append("Financial data could be exfiltrated through external channels")

#         if has_access['analytics'] and has_access['sensitive_data'] and has_access['external_comm']:
#             pathways.append("Analytics → Sensitive Data → External Communication")
#             scenarios.append("Could analyze sensitive data and exfiltrate insights")
#             if 11 in access_ids:
#                 scenarios.append("Data analytics tools could be used to identify high-value information")

#         if 8 in access_ids and 16 in access_ids:
#             pathways.append("IT Analytics → Financial Data")
#             scenarios.append("Technical skills combined with financial data access creates fraud risk")

#         if 15 in access_ids and has_access['external_comm']:
#             pathways.append("HR Data → External Communication")
#             scenarios.append("Employee personal data could be leaked externally")

#         if has_access['design_research'] and has_access['external_comm'] and has_access['project_specific']:
#             pathways.append("Research & Design → External Communication")
#             scenarios.append("Intellectual property/design research could leak to competitors")

#         external_channels = [id for id in access_ids if id in [3, 5, 6]]
#         if len(external_channels) >= 2:
#             pathways.append("Multiple External Communication Channels")
#             scenarios.append(f"Uses {len(external_channels)} different external communication methods")

#         if 12 in access_ids and has_access['external_comm']:
#             pathways.append("Supply Chain Data → External Communication")
#             scenarios.append("Vendor/supply chain data could be leaked to competitors")

#         return pathways, scenarios

#     breach_analysis = employee_data.apply(
#         lambda emp: pd.Series(identify_breach_pathways(emp), index=['Breach_Pathways', 'Breach_Scenarios']), 
#         axis=1
#     )
#     employee_data = pd.concat([employee_data, breach_analysis], axis=1)
#     employee_data['Num_Pathways'] = employee_data['Breach_Pathways'].apply(len)
#     employee_data['Num_Scenarios'] = employee_data['Breach_Scenarios'].apply(len)

#     # Display results
#     st.subheader("Sample Employee Data with Risk Scores")
#     st.dataframe(employee_data.head(10))

#     st.subheader("Department Average Risk Scores")
#     st.dataframe(dept_avg_risk)

#     st.subheader("Distribution of Risk Scores")
#     fig, ax = plt.subplots()
#     sns.histplot(employee_data['Risk_Score'], kde=True, ax=ax)
#     st.pyplot(fig)

#     st.subheader("Top Risk Employees")
#     top_risk = employee_data.sort_values(by='Risk_Score', ascending=False).head(10)
#     st.dataframe(top_risk[['Emp_ID', 'Dept_Name', 'Risk_Score', 'Num_Pathways', 'Num_Scenarios']])

# else:
#     st.warning("Please upload all three CSV files to begin analysis.")

import streamlit as st
import pandas as pd
import ast
import networkx as nx
from itertools import product

# Risk and category mappings
access_risk_weights = {
    1: 1, 2: 2, 3: 5, 4: 2, 5: 7, 6: 7, 7: 3, 8: 4, 9: 8, 10: 4, 11: 5, 12: 6,
    13: 4, 14: 4, 15: 6, 16: 7, 17: 5, 18: 4, 19: 4, 20: 6, 21: 7, 22: 7, 23: 3,
    24: 3, 25: 2, 26: 5, 27: 4, 28: 10
}
access_categories = {
    'external_comm': [3, 5, 6],
    'sensitive_data': [9, 15, 16, 21, 22],
    'super_access': [28]
}

# Streamlit UI
st.title("🔐 Data Leak Path Analyzer")

# File upload
dept_file = st.file_uploader("Upload Department.csv", type="csv")
emp_file = st.file_uploader("Upload Employees_table.csv", type="csv")
access_file = st.file_uploader("Upload Accessibility.csv", type="csv")

if dept_file and emp_file and access_file:
    departments = pd.read_csv(dept_file)
    employees = pd.read_csv(emp_file)
    accessibility = pd.read_csv(access_file)
    employees['Access_ID'] = employees['Access_ID'].apply(ast.literal_eval)

    leak_paths = []

    # Direct leaks
    for _, emp in employees.iterrows():
        emp_name = emp['Emp_name']
        dept_id = emp['Dept_ID']
        dept_name = departments[departments['Dept_ID'] == dept_id]['Dept_Name'].values[0]
        access_ids = emp['Access_ID']

        external = set(access_ids).intersection(access_categories['external_comm'])
        sensitive = set(access_ids).intersection(access_categories['sensitive_data'])

        if external and sensitive:
            external_names = [accessibility[accessibility['Access_ID'] == aid]['Access'].values[0] for aid in external]
            sensitive_names = [accessibility[accessibility['Access_ID'] == aid]['Access'].values[0] for aid in sensitive]
            risk_score = sum([access_risk_weights[aid] for aid in external.union(sensitive)])
            leak_paths.append({
                'employee': emp_name,
                'department': dept_name,
                'external_names': external_names,
                'sensitive_names': sensitive_names,
                'risk_score': risk_score
            })

    G = nx.Graph()
    for _, emp in employees.iterrows():
        G.add_node(emp['Emp_name'],
                   dept=emp['Dept_ID'],
                   access=emp['Access_ID'],
                   has_sensitive=bool(set(emp['Access_ID']).intersection(access_categories['sensitive_data'])),
                   has_external=bool(set(emp['Access_ID']).intersection(access_categories['external_comm'])),
                   has_super=bool(set(emp['Access_ID']).intersection(access_categories['super_access'])))

    # Cross-department
    for i, emp1 in employees.iterrows():
        for j, emp2 in employees.iterrows():
            if i < j:
                common = set(emp1['Access_ID']).intersection(emp2['Access_ID'])
                if common:
                    G.add_edge(emp1['Emp_name'], emp2['Emp_name'], weight=len(common))
                    s1, s2 = emp1['Emp_name'], emp2['Emp_name']
                    d1 = departments[departments['Dept_ID'] == emp1['Dept_ID']]['Dept_Name'].values[0]
                    d2 = departments[departments['Dept_ID'] == emp2['Dept_ID']]['Dept_Name'].values[0]

                    if G.nodes[s1]['has_sensitive'] and G.nodes[s2]['has_external']:
                        risk = sum([access_risk_weights[aid] for aid in common])
                        leak_paths.append({
                            'type': 'cross_department',
                            'source': s1,
                            'source_dept': d1,
                            'target': s2,
                            'target_dept': d2,
                            'common_access': list(common),
                            'risk_score': risk
                        })

    leak_paths.sort(key=lambda x: x.get('risk_score', 0), reverse=True)

    st.subheader("📍 Direct Leak Paths")
    for path in [p for p in leak_paths if 'type' not in p]:
        st.markdown(f"*Risk {path['risk_score']}*: {path['employee']} ({path['department']})")
        st.write(f"External: {path['external_names']}, Sensitive: {path['sensitive_names']}")

    st.subheader("🌐 Cross-Department Leak Paths")
    for path in [p for p in leak_paths if p.get('type') == 'cross_department']:
        st.markdown(f"*Risk {path['risk_score']}*: {path['source']} ➝ {path['target']}")
        st.write(f"Shared Access IDs: {path['common_access']}")

    st.subheader("🔄 Bridge Employees")
    bridges = []
    for node in G.nodes():
        neighbors = list(G.neighbors(node))
        if len(neighbors) > 1:
            dept_set = set(G.nodes[n]['dept'] for n in neighbors)
            if len(dept_set) > 1:
                bridges.append({'employee': node, 'connects_departments': len(dept_set), 'connections': len(neighbors)})

    for b in sorted(bridges, key=lambda x: x['connects_departments'], reverse=True)[:5]:
        st.write(f"{b['employee']} connects {b['connects_departments']} depts, {b['connections']} connections")

    st.subheader("⚠ High-Risk Leak Chains (Risk > 98)")
    sources, targets = [], []

    for _, emp in employees.iterrows():
        a_ids = set(emp['Access_ID'])
        if a_ids.intersection(access_categories['sensitive_data']) or a_ids.intersection(access_categories['super_access']):
            sources.append(emp['Emp_name'])
        if a_ids.intersection(access_categories['external_comm']):
            targets.append(emp['Emp_name'])

    count = 0
    for s, t in product(sources, targets):
        if s != t:
            try:
                paths = list(nx.all_simple_paths(G, s, t, cutoff=3))
            except:
                continue
            for path in paths:
                a_ids = set()
                for p in path:
                    a_ids.update(G.nodes[p]['access'])
                score = sum([access_risk_weights.get(a, 0) for a in a_ids])
                if score > 98:
                    count += 1
                    st.markdown(f"*Chain {count}:* {' ➝ '.join(path)} (Score: {score})")
                    for idx, person in enumerate(path):
                        labels = []
                        p_ids = set(employees[employees['Emp_name'] == person].iloc[0]['Access_ID'])
                        if p_ids.intersection(access_categories['sensitive_data']):
                            labels.append("sensitive")
                        if p_ids.intersection(access_categories['external_comm']):
                            labels.append("external")
                        if p_ids.intersection(access_categories['super_access']):
                            labels.append("super")
                        st.write(f"{idx+1}. {person} [{', '.join(labels)}]")
    if count == 0:
        st.info("No high-risk leak chains found.")