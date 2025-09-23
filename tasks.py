from crewai import Task
from agents import requirement_analysis, task_planner_agent, code_generator_agent, test_validation_agent



class RequirementAnalysis(Task):
    @staticmethod
    def req(application, language):
        """
        Crée une tâche pour analyser les exigences utilisateur et générer des spécifications organisées.
        """
        return Task(
            description=(
                f"Project: {application}\n"
                f"Programming Language: {language}\n"
                "Objective: Analyze user-provided requirements to identify and define key functional and non-functional requirements.\n"
                "Tasks to perform:\n"
                "- Break down ambiguous or complex requirements into clear and actionable specifications.\n"
                "- Clearly define the expected components, functions, and functionalities based on the chosen programming language.\n"
                "- Document any assumptions made during the analysis.\n"
                "- Highlight areas requiring further clarification.\n"
                "- Consider language-specific best practices and patterns."
            ),
            expected_output=(
                "A well-organized document containing:\n"
                "1. A summary of functional requirements.\n"
                "2. A summary of non-functional requirements.\n"
                "3. Assumptions and identified ambiguities.\n"
                "4. Language-specific considerations and recommendations.\n"
                "All output must be written in French."
            ),

            agent=requirement_analysis,
        )

    @staticmethod
    def format_requirements_output(raw_output):
            """
            Organise dynamiquement la sortie brute de l'agent en sections structurées.
            Fonctionne quelle que soit la structure ou les titres utilisés dans le texte.
            """
            if not isinstance(raw_output, str):
                print("Erreur : la sortie brute n'est pas une chaîne de caractères.")
                return {}

            formatted_output = {}
            current_section = None

            lines = raw_output.split("\n")

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Détecter un titre de section (ex: "1. Titre", "* Titre", ou "Titre:")
                is_section_title = re.match(r"^(\*+|\d+\.)?\s*[\w\s\-éèêàçÉÈÊÀÇ]+(:|\*)?$", line)
                if is_section_title and not line.startswith("* "):  # éviter les puces normales
                    # Nettoyer le titre
                    clean_title = re.sub(r"^\*+", "", line)
                    clean_title = re.sub(r"^\d+\.\s*", "", clean_title)
                    clean_title = clean_title.strip(" :*")
                    current_section = clean_title
                    if current_section not in formatted_output:
                        formatted_output[current_section] = []
                elif current_section:
                    formatted_output[current_section].append(line)

            # Convertir les listes en texte structuré
            for key in formatted_output:
                formatted_output[key] = "\n".join(formatted_output[key]) if formatted_output[key] else "Aucune information identifiée."

            return formatted_output


# Classe pour la planification des tâches


class TaskPlanning(Task):
    @staticmethod
    def plan_and_decompose(application, language, requirements_summary):
        if isinstance(requirements_summary, dict):
            requirements_summary = "\n".join(
                f"{key}: {value}" for key, value in requirements_summary.items()
            )

        return Task(
            description=(
                f"Project: {application}\n"
                f"Programming Language: {language}\n"
                "Objective: Decompose the requirements into specific coding tasks.\n"
                "Requirements Summary:\n"
                f"{requirements_summary}\n"
                "Tasks to perform:\n"
                "1. Research and identify the best practices and patterns for the specified programming language.\n"
                "2. Based on the research, plan the implementation including:\n"
                "   - Required components/modules/classes structure\n"
                "   - Functions/methods and their purposes\n"
                "   - Dependencies and relationships between components\n"
                "   - Language-specific considerations\n"
                "3. Ensure the plan follows the language's conventions and best practices.\n"
                "4. Make the tasks actionable for direct code generation."
            ),
           expected_output=(
                f"A well-organized plan for {language} implementation including:\n"
                "1. Language-specific best practices and patterns identified\n"
                "2. Detailed component structure and organization\n"
                "3. Function/method specifications and purposes\n"
                "4. Dependencies and relationships between components\n"
                "5. Language-specific considerations and recommendations\n"
                "All output must be written in French."
            ),
            agent=task_planner_agent
        )

    @staticmethod
    def format_task_output(raw_output):
        """
        Format the task planning output into a structured format that adapts to different programming languages.
        """
        formatted_output = {
            "Components": [],  # Pour les classes, modules, ou autres structures selon le langage
            "Functions": {},   # Pour les méthodes, fonctions, ou autres routines
            "Dependencies": [], # Pour les relations, imports, ou autres dépendances
            "BestPractices": [], # Pour les pratiques spécifiques au langage
            "ActionableTasks": [] # Pour les tâches concrètes à implémenter
        }

        if not isinstance(raw_output, str):
            print("Error: Raw output is not a string.")
            return formatted_output

        # Parse the output
        lines = raw_output.split("\n")
        current_section = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Détection des sections
            if "Components:" in line or "Classes:" in line or "Modules:" in line:
                current_section = "Components"
            elif "Functions:" in line or "Methods:" in line:
                current_section = "Functions"
            elif "Dependencies:" in line or "Relationships:" in line or "Imports:" in line:
                current_section = "Dependencies"
            elif "Best Practices:" in line or "Language Specific:" in line:
                current_section = "BestPractices"
            elif "Actionable Tasks:" in line or "Implementation Tasks:" in line:
                current_section = "ActionableTasks"
            elif current_section:
                # Traitement des lignes selon la section
                if current_section == "Functions":
                    # Gestion des fonctions/méthodes avec leur description
                    if ":" in line or "-" in line:
                        try:
                            # Supporte différents formats de séparation
                            if ":" in line:
                                func_name, func_desc = line.split(":", 1)
                            else:
                                func_name, func_desc = line.split("-", 1)
                            
                            component_name = func_name.strip()
                            description = func_desc.strip()
                            
                            if component_name not in formatted_output[current_section]:
                                formatted_output[current_section][component_name] = []
                            formatted_output[current_section][component_name].append(description)
                        except ValueError:
                            # Si le format n'est pas standard, ajouter comme une entrée simple
                            formatted_output[current_section].setdefault("General", []).append(line)
                else:
                    # Pour les autres sections, ajouter simplement la ligne
                    if line and not line.startswith(("-", "*", "•")):
                        formatted_output[current_section].append(line)

        # Nettoyage des listes vides
        for key in formatted_output:
            if isinstance(formatted_output[key], list) and not formatted_output[key]:
                formatted_output[key] = []
            elif isinstance(formatted_output[key], dict) and not formatted_output[key]:
                formatted_output[key] = {}

        return formatted_output


class CodeGenerationTask(Task):
    @staticmethod
    def code_generation(application, language, planing_summary):
        global requirements_summary
        if isinstance(planing_summary, dict):
            requirements_summary = "\n".join(
                f"{key}: {value}" for key, value in planing_summary.items()
            )

        return Task(
            description=(
                f"Code Generation Task for {application} Development in {language}\n\n"
                "The task involves generating high-quality source code "
                "to meet the following business and technical requirements:\n\n"
                f"{planing_summary}\n\n"
                "Before generating the code:\n"
                "1. Research and identify the best practices and coding standards for the specified programming language\n"
                "2. Understand the language-specific patterns and conventions\n"
                "3. Identify appropriate documentation standards for the language\n\n"
                "The generated code should:\n"
                "- Follow the language's best practices and conventions\n"
                "- Be properly structured and organized\n"
                "- Include appropriate error handling\n"
                "- Be well-documented according to language standards\n"
                "- Be modular, scalable, and maintainable\n"
                "- Follow the planned architecture\n\n"
                "IMPORTANT: For each code file, you MUST include a comment indicating the filename before the code.\n"
                "For C++ files, use this format:\n"
                "// filename.h\n"
                "or\n"
                "** filename.h **\n"
                "For Python files, use this format:\n"
                "# filename.py\n"
                "For Java files, use this format:\n"
                "// filename.java\n"
                "or\n"
                "** filename.java **\n\n"
                "Example for C++:\n"
                "// task.h\n"
                "class Task { ... };\n\n"
                "// task.cpp\n"
                "void Task::method() { ... }\n\n"
                "Example for Python:\n"
                "# task.py\n"
                "class Task:\n    def __init__(self):\n        pass\n\n"
                "Example for Java:\n"
                "// Task.java\n"
                "public class Task {\n    public void method() { ... }\n}"
            ),
            expected_output=(
                f"Expected Output: A fully functional set of {language} source code files, "
                "which meet the specified business and technical requirements outlined in the planning summary. "
                "The generated code should be:\n"
                "1. Clean, modular, and well-documented\n"
                "2. Following language-specific best practices\n"
                "3. Properly structured according to the language's conventions\n"
                "4. Ready for testing and integration\n"
                "5. Efficient and reusable\n"
                "6. Aligned with the project's long-term goals\n\n"
                "The output must include:\n"
                "- All required components/modules/classes\n"
                "- Proper error handling\n"
                "- Comprehensive documentation\n"
                "- Necessary dependencies and imports\n"
                "- Unit tests or test cases\n\n"
                "IMPORTANT: Each code file must be preceded by a comment indicating its filename:\n"
                "- For C++: // filename.h or ** filename.h ** or // filename.cpp or ** filename.cpp **\n"
                "- For Python: # filename.py\n"
                "- For Java: // filename.java or ** filename.java **"
            ),
            agent=code_generator_agent
        )




class CodeFixTask(Task):
    @staticmethod
    def fix_code(application, code_result, validation_result):
        """
        Creates a task to fix code issues and add necessary components.
        """
        return Task(
            description=(
                f"Code Fix Task for {application}\n\n"
                "Objective: Analyze the code and validation results to fix issues and add missing components.\n\n"
                "Input Code:\n"
                f"{code_result}\n\n"
                "Validation Results:\n"
                f"{validation_result}\n\n"
                "Tasks to perform:\n"
                "1. Fix any syntax errors identified\n"
                "2. Add missing module/package imports\n"
                "3. Implement any missing functions or classes\n"
                "4. Ensure all dependencies are properly handled\n"
                "5. Maintain code quality and best practices\n"
                "6. Follow language-specific conventions and patterns\n"
            ),
            expected_output=(
                "Expected Output: The corrected and complete code with the following attributes:\n"
                "1. All necessary module/package imports\n"
                "2. All required functions and classes implemented\n"
                "3. Proper error handling\n"
                "4. Resolved syntax issues\n"
                "5. Summary of fixes made\n"
                "### Corrected Code: ###\n"
                "{corrected_code_here}\n"
            ),
            agent=code_generator_agent
        )

    @staticmethod
    def format_fix_output(raw_output):
        """
        Format the code fix output into a structured format.
        """
        formatted_output = {
            "Fixed Code": "",
            "Changes Made": [],
            "Added Imports": [],
            "Added Classes": [],
            "Remaining Issues": []
        }

        if not isinstance(raw_output, str):
            print("Error: Raw output is not a string.")
            return formatted_output

        current_section = None
        lines = raw_output.split("\n")

        for line in lines:
            if "FIXED CODE:" in line.upper():
                current_section = "Fixed Code"
            elif "CHANGES MADE:" in line.upper():
                current_section = "Changes Made"
            elif "ADDED IMPORTS:" in line.upper():
                current_section = "Added Imports"
            elif "ADDED CLASSES:" in line.upper():
                current_section = "Added Classes"
            elif "REMAINING ISSUES:" in line.upper():
                current_section = "Remaining Issues"
            elif current_section:
                if current_section == "Fixed Code":
                    formatted_output[current_section] += line + "\n"
                else:
                    formatted_output[current_section].append(line.strip())

        return formatted_output


class TestValidationTask(Task):
    @staticmethod
    def validate_code(language, application, generated_code):
        # Vérification des paramètres
        if not language:
            language = "python"  # ou une autre valeur par défaut
        if not application:
            application = "Unknown Application"
        if not generated_code:
            generated_code = "No code provided"

        if language.lower() == "python":
            test_tool = "pytest or unittest"
            quality_guidelines = "PEP8, modularity, readability"
        elif language.lower() == "java":
            test_tool = "JUnit"
            quality_guidelines = "code reusability, SOLID principles, documentation"
        elif language.lower() == "javascript":
            test_tool = "Jest or Mocha"
            quality_guidelines = "modularity, ES6 conventions, comments"
        else:
            test_tool = "appropriate testing framework"
            quality_guidelines = "standard practices for the language"

        return Task(
            description=(
                f"Test Validation Task for {application} Development in {language}\n\n"
                f"Objective: Validate the generated {language} code using {test_tool}.\n\n"
                f"Code to validate:\n{generated_code}\n\n"
                "Tasks to perform:\n"
                f"- Write and run test cases using {test_tool}.\n"
                "- Check that all required functionalities work correctly.\n"
                "- Report test results (pass/fail).\n"
                f"- Check code quality: {quality_guidelines}.\n"
                "- Suggest improvements if needed.\n"
            ),
            expected_output=(
                "Expected Output: A validation report that includes:\n"
                "1. Test summary (pass/fail).\n"
                "2. Performance issues (if any).\n"
                "3. Code quality analysis.\n"
                "4. Suggested improvements.\n"
                "5. Final approval or rejection.\n"
                "Final Status: Must be exactly '**Final Status: Valid**' or '**Final Status: Not_Valid**'."
            ),
            agent=test_validation_agent
        )

    @staticmethod
    def format_validation_output(raw_output):
        """
        Format the validation output into a structured format for easy review.
        """
        formatted_output = {
            "Test Cases": [],
            "Performance Issues": [],
            "Code Quality Issues": [],
            "Improvement Suggestions": [],
            "Final Status": ""
        }

        if not isinstance(raw_output, str):
            print("Error: Raw output is not a string.")
            return formatted_output

        # Split the raw output into lines for processing
        lines = raw_output.split("\n")
        current_section = None

        for line in lines:
            if "Test Cases:" in line:
                current_section = "Test Cases"
            elif "Performance Issues:" in line:
                current_section = "Performance Issues"
            elif "Code Quality Issues:" in line:
                current_section = "Code Quality Issues"
            elif "Improvement Suggestions:" in line:
                current_section = "Improvement Suggestions"
            elif "Final Status:" in line:
                current_section = "Final Status"
            elif current_section:
                formatted_output[current_section].append(line.strip())

        # Convert lists into formatted strings for readability
        for key in formatted_output:
            formatted_output[key] = "\n".join(formatted_output[key])

        return formatted_output

    @staticmethod
    def extract_final_status(text):
        match = re.search(r"Final Status:\s*(\w+)", text, re.IGNORECASE)
        if match:
            return match.group(1)
        else:
            return None



class CodeFixTask2(Task):
    @staticmethod
    def fix_code(project_name, generated_code, compilation_error):
        return Task(
            description=(
                f"""
You are a skilled software engineer responsible for fixing code that failed to compile or run.

Project Name: {project_name}

Here is the original generated code:
------------------------
{generated_code}
------------------------

Here is the error message (compilation or runtime):
------------------------
{compilation_error}
------------------------

Your task:
1. Analyze the provided code and understand its structure and purpose.
2. Examine the error message to identify the cause of the failure.
3. Modify the code to eliminate the specific issue reported in the error.
4. Ensure that the same error does not occur again.
5. Maintain the original logic and style as much as possible.
6. Avoid introducing new bugs or syntax issues.

IMPORTANT CONSTRAINTS:
1. DO NOT include any test files or test dependencies (like gtest, catch2, etc.)
2. DO NOT use any external libraries unless explicitly required
3. If testing is needed, use simple assertions in the main file
4. All code should be self-contained
5. Focus only on the core functionality

⚠️ Do not include any explanations — just return the new, corrected version of the code as a single complete file.
"""
            ),
            expected_output=(""""
            A complete, working solution with:
            1. All necessary source files
            2. No external dependencies
            3. Clear documentation
            4. Proper error handling"""),
            agent=code_generator_agent
        )


import re

def extract_final_status(text):
    match = re.search(r"Final Status:\s*(\w+)", text, re.IGNORECASE)
    if match:
        return match.group(1)
    else:
        return None  # Or raise an exception, depending on your needs
