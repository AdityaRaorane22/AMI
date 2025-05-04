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
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px

# Risk and category mappings
access_risk_weights = {
    1: 1, 2: 2, 3: 5, 4: 2, 5: 7, 6: 7, 7: 3, 8: 4, 9: 8, 10: 4, 11: 5, 12: 6,
    13: 4, 14: 4, 15: 6, 16: 7, 17: 5, 18: 4, 19: 4, 20: 6, 21: 7, 22: 7, 23: 3,
    24: 3, 25: 2, 26: 5, 27: 4, 28: 10
}

access_categories = {
    'external_comm': [3, 5, 6],  # External communication channels
    'sensitive_data': [9, 15, 16, 21, 22],  # Highly sensitive data
    'analytics': [8, 10, 11, 13, 14],  # Analytics and reporting tools
    'operational': [12, 17, 19, 20],  # Operational systems
    'design_research': [23, 24, 25, 27],  # Design and research tools
    'project_specific': [7, 18, 26],  # Project-specific tools
    'super_access': [28]  # Full access
}

# Risk level definitions
def risk_level(score):
    if score >= 20:
        return "Critical", "red"
    elif score >= 15:
        return "High", "orange"
    elif score >= 10:
        return "Medium", "yellow"
    else:
        return "Low", "green"

# Streamlit UI
st.set_page_config(layout="wide")
st.title("🔐 Data Leak Path Analyzer")
st.markdown("### Identify and visualize potential data breach pathways")

# File upload
col1, col2, col3 = st.columns(3)
with col1:
    dept_file = st.file_uploader("Upload Department.csv", type="csv")
with col2:
    emp_file = st.file_uploader("Upload Employees_table.csv", type="csv")
with col3:
    access_file = st.file_uploader("Upload Accessibility.csv", type="csv")

if dept_file and emp_file and access_file:
    departments = pd.read_csv(dept_file)
    employees = pd.read_csv(emp_file)
    accessibility = pd.read_csv(access_file)
    employees['Access_ID'] = employees['Access_ID'].apply(ast.literal_eval)
    
    # Create a mapping of Access_ID to Access name
    access_name_map = {row['Access_ID']: row['Access'] for _, row in accessibility.iterrows()}
    
    # Direct leak paths
    leak_paths = []
    
    for _, emp in employees.iterrows():
        emp_name = emp['Emp_name']
        dept_id = emp['Dept_ID']
        dept_name = departments[departments['Dept_ID'] == dept_id]['Dept_Name'].values[0]
        access_ids = emp['Access_ID']
        
        external = set(access_ids).intersection(access_categories['external_comm'])
        sensitive = set(access_ids).intersection(access_categories['sensitive_data'])
        
        if external and sensitive:
            external_names = [access_name_map[aid] for aid in external]
            sensitive_names = [access_name_map[aid] for aid in sensitive]
            risk_score = sum([access_risk_weights[aid] for aid in external.union(sensitive)])
            level, color = risk_level(risk_score)
            
            justification = f"Employee has both external communication ({', '.join(external_names)}) and sensitive data access ({', '.join(sensitive_names)})"
            
            leak_paths.append({
                'employee': emp_name,
                'department': dept_name,
                'external_names': external_names,
                'sensitive_names': sensitive_names,
                'risk_score': risk_score,
                'risk_level': level,
                'color': color,
                'justification': justification
            })
    
    # Build network graph
    G = nx.Graph()
    for _, emp in employees.iterrows():
        dept_name = departments[departments['Dept_ID'] == emp['Dept_ID']]['Dept_Name'].values[0]
        has_sensitive = bool(set(emp['Access_ID']).intersection(access_categories['sensitive_data']))
        has_external = bool(set(emp['Access_ID']).intersection(access_categories['external_comm']))
        has_super = bool(set(emp['Access_ID']).intersection(access_categories['super_access']))
        
        G.add_node(emp['Emp_name'],
                   dept=emp['Dept_ID'],
                   dept_name=dept_name,
                   access=emp['Access_ID'],
                   has_sensitive=has_sensitive,
                   has_external=has_external,
                   has_super=has_super)
    
    # Cross-department paths
    for i, emp1 in employees.iterrows():
        for j, emp2 in employees.iterrows():
            if i < j:
                common = set(emp1['Access_ID']).intersection(emp2['Access_ID'])
                if common:
                    G.add_edge(emp1['Emp_name'], emp2['Emp_name'], 
                              weight=len(common), 
                              common_access=list(common))
                    
                    s1, s2 = emp1['Emp_name'], emp2['Emp_name']
                    d1 = departments[departments['Dept_ID'] == emp1['Dept_ID']]['Dept_Name'].values[0]
                    d2 = departments[departments['Dept_ID'] == emp2['Dept_ID']]['Dept_Name'].values[0]
                    
                    common_access_names = [access_name_map[aid] for aid in common]
                    
                    if G.nodes[s1]['has_sensitive'] and G.nodes[s2]['has_external']:
                        risk = sum([access_risk_weights[aid] for aid in common])
                        level, color = risk_level(risk)
                        
                        justification = f"Employee {s1} has sensitive data access and can share with {s2} who has external comm channels via shared access: {', '.join(common_access_names)}"
                        
                        leak_paths.append({
                            'type': 'cross_department',
                            'source': s1,
                            'source_dept': d1,
                            'target': s2,
                            'target_dept': d2,
                            'common_access': list(common),
                            'common_access_names': common_access_names,
                            'risk_score': risk,
                            'risk_level': level,
                            'color': color,
                            'justification': justification
                        })
    
    leak_paths.sort(key=lambda x: x.get('risk_score', 0), reverse=True)
    
    # Dashboard layout
    st.markdown("## 📊 Risk Dashboard")
    
    # Key metrics
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    direct_leaks = [p for p in leak_paths if 'type' not in p]
    cross_dept_leaks = [p for p in leak_paths if p.get('type') == 'cross_department']
    
    with metric_col1:
        st.metric("Direct Leak Paths", len(direct_leaks))
    
    with metric_col2:
        st.metric("Cross-Department Paths", len(cross_dept_leaks))
    
    # Identify high-risk departments
    dept_risks = {}
    for path in leak_paths:
        if 'type' not in path:
            dept = path['department']
            if dept not in dept_risks:
                dept_risks[dept] = 0
            dept_risks[dept] += path['risk_score']
        else:
            for dept in [path['source_dept'], path['target_dept']]:
                if dept not in dept_risks:
                    dept_risks[dept] = 0
                dept_risks[dept] += path['risk_score'] / 2  # Split risk between departments
    
    riskiest_dept = max(dept_risks.items(), key=lambda x: x[1])[0] if dept_risks else "N/A"
    
    with metric_col3:
        st.metric("Highest Risk Department", riskiest_dept)
    
    with metric_col4:
        avg_risk = sum(p['risk_score'] for p in leak_paths) / len(leak_paths) if leak_paths else 0
        st.metric("Average Risk Score", f"{avg_risk:.1f}")
    
    # Tab layout for different views
    tab1, tab2 = st.tabs(["Risk Matrix", "Leak Paths"])
    
    with tab1:
        st.subheader("Risk Distribution Matrix")
        
        # Create risk matrix data
        departments_list = sorted(list(departments['Dept_Name']))
        risk_matrix = pd.DataFrame(0, index=departments_list, columns=departments_list)
        
        for path in cross_dept_leaks:
            src_dept = path['source_dept']
            tgt_dept = path['target_dept']
            risk_matrix.loc[src_dept, tgt_dept] += path['risk_score']
            risk_matrix.loc[tgt_dept, src_dept] += path['risk_score']  # symmetric
        
        # Visualize risk matrix
        fig, ax = plt.subplots(figsize=(10, 8))
        mask = np.triu(np.ones_like(risk_matrix, dtype=bool))
        cmap = sns.diverging_palette(230, 20, as_cmap=True)
        sns.heatmap(risk_matrix, mask=mask, cmap=cmap, vmax=risk_matrix.max().max(),
                   square=True, linewidths=.5, cbar_kws={"shrink": .5}, ax=ax)
        
        plt.title('Cross-Department Risk Matrix')
        st.pyplot(fig)
        
        # Risk justification
        st.subheader("Matrix Interpretation")
        st.markdown("""
        The risk matrix shows potential data leak paths between departments:
        - **Higher values (darker colors)** indicate greater risk of sensitive data leakage between departments
        - **Lower values (lighter colors)** represent lower risk connections
        
        This visualization helps identify which department pairs need stricter access controls and monitoring.
        """)
        
        # Department risk bar chart
        st.subheader("Department Risk Levels")
        dept_risk_df = pd.DataFrame(list(dept_risks.items()), columns=['Department', 'Risk Score'])
        dept_risk_df = dept_risk_df.sort_values('Risk Score', ascending=False)
        
        fig = px.bar(dept_risk_df, x='Department', y='Risk Score', 
                    color='Risk Score', color_continuous_scale='Reds')
        st.plotly_chart(fig, use_container_width=True)
        
    with tab2:
        # Direct leak paths
        st.subheader("📍 Direct Leak Paths")
        st.markdown("Employees with both sensitive data access and external communication channels")
        
        if direct_leaks:
            for i, path in enumerate(direct_leaks):
                with st.expander(f"🚨 {path['employee']} - {path['department']} (Risk: {path['risk_score']}, Level: {path['risk_level']})"):
                    st.markdown(f"**Risk Justification:** {path['justification']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**External Communication Access:**")
                        for access in path['external_names']:
                            st.markdown(f"- {access}")
                    
                    with col2:
                        st.markdown("**Sensitive Data Access:**")
                        for access in path['sensitive_names']:
                            st.markdown(f"- {access}")
        else:
            st.info("No direct leak paths found.")
        
        # Cross-department leak paths
        st.subheader("🌐 Cross-Department Leak Paths")
        st.markdown("Data leak paths that cross department boundaries")
        
        if cross_dept_leaks:
            for i, path in enumerate(cross_dept_leaks):
                with st.expander(f"🔄 {path['source']} ({path['source_dept']}) ➝ {path['target']} ({path['target_dept']}) - Risk: {path['risk_score']}, Level: {path['risk_level']}"):
                    st.markdown(f"**Risk Justification:** {path['justification']}")
                    
                    st.markdown("**Shared Access Points:**")
                    for access in path['common_access_names']:
                        st.markdown(f"- {access}")
        else:
            st.info("No cross-department leak paths found.")
    

    
    # Export risk report button
    st.markdown("## 📊 Matrix Visualization")
    
    # Additional matrix view - Access type by department
    employees_by_dept = {}
    for _, emp in employees.iterrows():
        dept_id = emp['Dept_ID']
        dept_name = departments[departments['Dept_ID'] == dept_id]['Dept_Name'].values[0]
        
        if dept_name not in employees_by_dept:
            employees_by_dept[dept_name] = []
        
        access_ids = emp['Access_ID']
        has_sensitive = bool(set(access_ids).intersection(access_categories['sensitive_data']))
        has_external = bool(set(access_ids).intersection(access_categories['external_comm']))
        has_super = bool(set(access_ids).intersection(access_categories['super_access']))
        
        risk_type = "Standard"
        if has_sensitive and has_external:
            risk_type = "Critical"
        elif has_sensitive:
            risk_type = "Sensitive"
        elif has_external:
            risk_type = "External"
        
        if has_super:
            risk_type = "Super"
            
        employees_by_dept[dept_name].append({
            'name': emp['Emp_name'],
            'risk_type': risk_type
        })
    
    # Create risk type distribution matrix
    dept_names = sorted(list(employees_by_dept.keys()))
    risk_types = ["Critical", "Sensitive", "External", "Super", "Standard"]
    
    # Initialize the matrix with zeros
    risk_matrix_data = np.zeros((len(dept_names), len(risk_types)))
    
    # Fill the matrix
    for i, dept in enumerate(dept_names):
        for emp in employees_by_dept[dept]:
            j = risk_types.index(emp['risk_type'])
            risk_matrix_data[i, j] += 1
    
    # Create a DataFrame for the heatmap
    risk_matrix_df = pd.DataFrame(risk_matrix_data, 
                                 index=dept_names,
                                 columns=risk_types)
    
    # Plot the heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(risk_matrix_df, cmap="YlOrRd", annot=True, fmt=".0f", linewidths=.5, ax=ax)
    plt.title('Department Access Type Distribution Matrix')
    plt.xlabel('Access Risk Type')
    plt.ylabel('Department')
    st.pyplot(fig)
    
    st.markdown("### Access Type Matrix Interpretation")
    st.markdown("""
    This matrix shows the distribution of employee access types across departments:
    - **Critical**: Employees who have both sensitive data access AND external communication channels
    - **Sensitive**: Employees who only have sensitive data access
    - **External**: Employees who only have external communication access  
    - **Super**: Employees with super-user level access
    - **Standard**: Employees with standard access (no sensitive/external/super)
    
    Higher numbers in the 'Critical' column indicate departments with more potential direct leak points.
    """)
    
    if st.button("📄 Generate Risk Report"):
        st.subheader("Risk Assessment Report")
        
        total_employees = len(employees)
        total_risk_paths = len(leak_paths)
        
        # Create risk summary table
        risk_summary = pd.DataFrame({
            'Risk Level': ['Critical', 'High', 'Medium', 'Low'],
            'Direct Leaks': [
                len([p for p in direct_leaks if p['risk_level'] == 'Critical']),
                len([p for p in direct_leaks if p['risk_level'] == 'High']),
                len([p for p in direct_leaks if p['risk_level'] == 'Medium']),
                len([p for p in direct_leaks if p['risk_level'] == 'Low'])
            ],
            'Cross-Dept Leaks': [
                len([p for p in cross_dept_leaks if p['risk_level'] == 'Critical']),
                len([p for p in cross_dept_leaks if p['risk_level'] == 'High']),
                len([p for p in cross_dept_leaks if p['risk_level'] == 'Medium']),
                len([p for p in cross_dept_leaks if p['risk_level'] == 'Low'])
            ]
        })
        
        st.dataframe(risk_summary, use_container_width=True)
        
        report = f"""
        ## Data Leak Risk Assessment Report
        
        ### Executive Summary
        
        This report identifies potential data leak risks within the organization based on employee access patterns.
        
        **Key Findings:**
        - Total Employees Analyzed: {total_employees}
        - Total Risk Paths Identified: {total_risk_paths}
        - Highest Risk Department: {riskiest_dept}
        - Average Risk Score: {avg_risk:.1f}
        
        ### Top Risk Paths
        
        The following employees have direct access to both sensitive data and external communication channels:
        """
        
        for i, path in enumerate(direct_leaks[:5]):
            report += f"""
            {i+1}. **{path['employee']}** ({path['department']}) - Risk Score: {path['risk_score']}
               - External: {', '.join(path['external_names'])}
               - Sensitive: {', '.join(path['sensitive_names'])}
            """
        
        report += """
        ### Cross-Department Risks
        
        The following cross-department connections represent potential data leak paths:
        """
        
        for i, path in enumerate(cross_dept_leaks[:5]):
            report += f"""
            {i+1}. **{path['source']}** ({path['source_dept']}) → **{path['target']}** ({path['target_dept']}) - Risk Score: {path['risk_score']}
               - Shared Access: {', '.join(path['common_access_names'])}
            """
        
        report += """
        ### Recommendations
        
        1. Review access permissions for employees with both sensitive data and external communication access
        2. Implement stronger controls between high-risk department pairs
        3. Monitor activities of employees that bridge multiple departments
        4. Consider implementing the principle of least privilege across the organization
        5. Conduct regular access reviews to identify and mitigate new risks
        """
        
        st.markdown(report)
else:
    st.info("Please upload all three CSV files to begin analysis.")