from crewai import Crew, Process
from tasks import RequirementAnalysis, TaskPlanning, CodeGenerationTask, TestValidationTask, CodeFixTask
from agents import requirement_analysis, task_planner_agent, code_generator_agent, test_validation_agent, code_fix_agent
from datetime import datetime
import os
from fpdf import FPDF





def get_input(prompt):
    user_input = input(prompt).strip()
    while not user_input:
        print("L'entrée ne peut pas être vide. Veuillez réessayer.")
        user_input = input(prompt).strip()
    return user_input


inputs = {
    'topic': get_input('Enter the topic (e.g., Library Management System): ')
}


crew_analysis = Crew(
    agents=[requirement_analysis],
    tasks=[RequirementAnalysis.req(inputs['topic'])],
    process=Process.sequential,
)

print("\n=== Lancement de l'Analyse des Exigences ===\n")
analysis_result = crew_analysis.kickoff(inputs)

print("\n=== Résultats de l'Analyse des Exigences ===\n")
if isinstance(analysis_result, dict):
    for key, value in analysis_result.items():
        print(f"{key}:\n{value}\n{'-' * 50}")
else:
    print(analysis_result)

formatted_analysis_result = RequirementAnalysis.format_requirements_output(analysis_result)
print(formatted_analysis_result)

crew_planning = Crew(
    agents=[task_planner_agent],
    tasks=[TaskPlanning.plan_and_decompose(inputs['topic'],formatted_analysis_result)],  
    process=Process.sequential,
)

print("\n=== Lancement de la Planification et Décomposition des Tâches ===\n")
planning_result = crew_planning.kickoff(formatted_analysis_result)


print("\n=== Résultats de la Planification ===\n")
if isinstance(planning_result, dict):
    for key, value in planning_result.items():
        print(f"{key}:\n{value}\n{'-' * 50}")
else:
    print(planning_result)



crew_generation = Crew(
    agents=[code_generator_agent],
    tasks=[CodeGenerationTask.code_generation(inputs['topic'], planning_result)],
    process=Process.sequential,
)
print("=== lancement de code_generation_agent ===\n")

code_result = crew_generation.kickoff()
print("\n############### Code ###############")
print(code_result)




crew_test_validation = Crew(
    agents=[test_validation_agent],
    tasks=[TestValidationTask.validate_code(inputs['topic'], code_result)],  # Passer le code généré
    process=Process.sequential,
)

print("\n=== Lancement de la Validation des Tests ===\n")
validation_result = crew_test_validation.kickoff()

# Afficher les résultats de la validation des tests
print("\n############### Résultats de la Validation des Tests ###############")
if isinstance(validation_result, dict):
    for key, value in validation_result.items():
        print(f"{key}:\n{value}\n{'-' * 50}")
else:
    print(validation_result)

## validaion
validation_status = TestValidationTask.extract_final_status(validation_result)

if validation_status and validation_status.lower() != 'valid':

    fixed_crew = Crew(
        agents=[code_generator_agent],
        tasks=[CodeFixTask.fix_code(inputs['topic'], code_result, validation_result)],
        process=Process.sequential )

    code_result = fixed_crew.kickoff()
    print("\n=== Lancement de la Fixation des Codes ===\n")
    print(code_result)
####

from agents import documentation_agent


print("\n=== Lancement de la Documentation ===\n")

documentation = documentation_agent.generate_documentation(code_result,inputs['topic'])

# Afficher ou traiter la documentation
print("\n=== Documentation Générée ===\n")
print(documentation)

