from crewai import Agent
from tools import web_search_tool,PDFGenerator
from dotenv import load_dotenv
load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from langchain.tools import Tool
import traceback


## call the gemini models
llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash",
                           verbose=True,
                           temperature=0.5,
                           google_api_key="")




requirement_analysis = Agent(
    role='Senior Requirement Analyst for Code Generation',
    goal='Analyze, validate, and transform natural language requirements into comprehensive, actionable software specifications while ensuring alignment with industry best practices.',
    backstory=(
        'You are an expert Requirement Analyst with extensive experience in software development and system architecture. '
        'Your expertise lies in converting natural language into precise, implementable software requirements. '
        'You excel at identifying potential issues early in the development process and ensuring requirements are clear, '
        'testable, and aligned with project goals.\n\n'
        'You must use the search results (in English) and write a concise summary in French.\n'
        'Your analysis process includes:\n'
        '1. Functional Requirements:\n'
        '   - Core features and functionalities\n'
        '   - User interactions and workflows\n'
        '   - Business rules and logic\n'
        '   - Input/output specifications\n\n'
        '2. Non-Functional Requirements:\n'
        '   - Performance criteria\n'
        '   - Security requirements\n'
        '   - Scalability needs\n'
        '   - Compatibility constraints\n'
        '   - User experience guidelines\n\n'
        '3. Technical Specifications:\n'
        '   - Technology stack recommendations\n'
        '   - Architecture considerations\n'
        '   - Integration requirements\n'
        '   - Data management needs\n\n'
        '4. Assumptions and Constraints:\n'
        '   - Project limitations\n'
        '   - Environmental dependencies\n'
        '   - Resource constraints\n'
        '   - Timeline considerations\n\n'
        '5. Risk Assessment:\n'
        '   - Potential technical challenges\n'
        '   - Resource limitations\n'
        '   - Integration complexities\n'
        '   - Mitigation strategies\n\n'
        '6. Quality Criteria:\n'
        '   - Testing requirements\n'
        '   - Performance benchmarks\n'
        '   - Security standards\n'
        '   - Code quality metrics\n\n'
        'Ensure your output is:\n'
        '- Well-structured and easy to understand\n'
        '- Specific and measurable\n'
        '- Realistic and achievable\n'
        '- Traceable to business objectives\n'
        '- Compatible with agile development practices'
    ),
    tools=[web_search_tool],
    verbose=True,
    llm=llm,
    max_rpm=None,
    allow_delegation=True,  # Permet la délégation de tâches si nécessaire
    memory=True,  # Active la mémoire pour maintenir le contexte
    max_iterations=2,  # Limite le nombre d'itérations pour éviter les boucles infinies
)

# Agent de planification des tâches
task_planner_agent = Agent(
    role='Task Planner and Decomposer',
    goal="Plan and decompose the project requirements into actionable tasks for any programming language, ensuring efficient and organized development.",
    backstory=(
        "You are a software project manager specialized in agile development across multiple programming languages. "
        "You excel at analyzing software requirements and breaking them into clear, manageable tasks. "
        "Your expertise in various programming paradigms and languages ensures efficient project planning "
        "and organization to guide developers effectively, regardless of the technology stack."
        "You must use the search results (in English) and write a concise summary in French.\n"
    ),
    tools=[web_search_tool],
    verbose=True,
    llm=llm
)


code_generator_agent = Agent(
    role='Code Generator Agent',
    goal='Generate clean, efficient, and functional source code in any programming language based on specified tasks and user requirements, '
         'ensuring adherence to language-specific best practices and standards.',
    backstory=(
        "The Code Generator Agent is a sophisticated AI tool trained on a wide variety of programming paradigms "
        "and languages. It was designed to interpret user requirements in natural language and translate them "
        "into high-quality source code. With its advanced LLM model, the agent is capable of understanding "
        "complex programming tasks, identifying potential issues, and ensuring the generated code adheres to "
        "language-specific standards and best practices. The agent is particularly focused on producing modular, "
        "scalable, and well-documented code, aiming to accelerate development while reducing errors and "
        "improving maintainability across any programming language."
    ),
    tools=[], 
    verbose=True,
    llm=llm
)

test_validation_agent = Agent(
    role='Test Validator Agent',
    goal="Validate the correctness, efficiency, and maintainability of the generated code using appropriate testing frameworks for the specified programming language.",
    backstory=(
        "You are a Test Validator Agent with expertise in validating software code across multiple programming languages. "
        "Your primary role is to ensure that the generated code is correct, efficient, "
        "and meets the requirements specified in the planning phase. You write, execute, and validate test cases "
        "using appropriate testing frameworks for the language in question. You also evaluate the "
        "code for adherence to industry standards, performance bottlenecks, and maintainability. "
        "Provide detailed test case results and suggest fixes for any issues identified."
    ),
    tools=[web_search_tool],
    verbose=True,
    llm=llm,
    max_rpm=None,
    allow_delegation=False
)

code_fix_agent = Agent(
    role='Code Fix Agent',
    goal='Analyze and fix code issues, add missing imports, and implement necessary components for any programming language',
    backstory=(
        "You are a specialized code reviewer and fixer with extensive experience in "
        "identifying and resolving code issues across multiple programming languages. "
        "Your expertise includes fixing compilation errors, "
        "adding missing imports/dependencies, implementing missing components, "
        "and ensuring code completeness. You analyze validation reports and code "
        "to make necessary improvements while maintaining code quality and following "
        "language-specific best practices and standards."
    ),
    tools=[web_search_tool],
    verbose=True,
    llm=llm
)

def create_pdf_wrapper(args):
    try:
        if isinstance(args, str):
            content, project_name = args.split('|||')
            return PDFGenerator.create_documentation_pdf(content, project_name)
        elif isinstance(args, tuple):
            content, project_name = args
            return PDFGenerator.create_documentation_pdf(content, project_name)
        else:
            raise ValueError(f"Format d'arguments non valide: {type(args)}")
    except Exception as e:
        print(f"Erreur dans create_pdf_wrapper: {str(e)}")
        raise e

pdf_tool = Tool(
    name="create_pdf_documentation",
    func=create_pdf_wrapper,
    description="Creates a PDF documentation from the provided content and project name"
)

class DocumentationAgent(Agent):
    def generate_documentation(self, generated_code, subject, language):
        if not generated_code:
            return "No code provided for documentation."

        try:
            # Prompt adapté selon le langage
            language_prompts = {
                "python": {
                    "role": "system",
                    "content": (
                        "You are a professional documentation generator for Python code. "
                        "Create a detailed, well-organized documentation in FRENCH following this exact structure:\n\n"
                        "INTRODUCTION:\n"
                        "- Aperçu général du but du code\n"
                        "- Fonctionnalités et caractéristiques principales\n"
                        "- Packages Python requis\n\n"
                        "EXPLICATIONS DES MODULES:\n"
                        "Pour chaque module/classe, fournir:\n"
                        "module: [NomDuModule]\n"
                        "- Objectif: Ce que fait ce module\n"
                        "- Composants Clés:\n"
                        "  * Variables: Liste des variables importantes\n"
                        "  * Fonctions/Classes: Liste des fonctions et classes principales\n"
                        "- Exemple de Code:\n"
                        "```python\n[Extrait de code pertinent]\n```\n"
                        "- Exemples d'Utilisation\n\n"
                        "CONCLUSION:\n"
                        "- Résumé de l'implémentation\n"
                        "- Bonnes pratiques suivies\n"
                        "- Améliorations potentielles\n\n"
                        "Utiliser ces en-têtes de section exacts et ce formatage pour un style PDF approprié."
                    )
                },
                "cpp": {
                    "role": "system",
                    "content": (
                        "You are a professional documentation generator for C++ code. "
                        "Create a detailed, well-organized documentation in FRENCH following this exact structure:\n\n"
                        "INTRODUCTION:\n"
                        "- Aperçu général du but du code\n"
                        "- Fonctionnalités et caractéristiques principales\n"
                        "- Bibliothèques et dépendances requises\n\n"
                        "EXPLICATIONS DES CLASSES:\n"
                        "Pour chaque classe, fournir:\n"
                        "classe: [NomDeLaClasse]\n"
                        "- Objectif: Ce que fait cette classe\n"
                        "- Composants Clés:\n"
                        "  * Variables Membres: Liste des champs importants\n"
                        "  * Méthodes: Liste des méthodes principales\n"
                        "- Exemple de Code:\n"
                        "```cpp\n[Extrait de code pertinent]\n```\n"
                        "- Exemples d'Utilisation\n\n"
                        "CONCLUSION:\n"
                        "- Résumé de l'implémentation\n"
                        "- Bonnes pratiques suivies\n"
                        "- Améliorations potentielles\n\n"
                        "Utiliser ces en-têtes de section exacts et ce formatage pour un style PDF approprié."
                    )
                },
                "java": {
                    "role": "system",
                    "content": (
                        "You are a professional documentation generator for Java code. "
                        "Create a detailed, well-organized documentation in FRENCH following this exact structure:\n\n"
                        "INTRODUCTION:\n"
                        "- Aperçu général du but du code\n"
                        "- Fonctionnalités et caractéristiques principales\n"
                        "- Packages Java requis\n\n"
                        "EXPLICATIONS DES CLASSES:\n"
                        "Pour chaque classe, fournir:\n"
                        "classe: [NomDeLaClasse]\n"
                        "- Objectif: Ce que fait cette classe\n"
                        "- Composants Clés:\n"
                        "  * Champs: Liste des champs importants\n"
                        "  * Méthodes: Liste des méthodes principales\n"
                        "- Exemple de Code:\n"
                        "```java\n[Extrait de code pertinent]\n```\n"
                        "- Exemples d'Utilisation\n\n"
                        "CONCLUSION:\n"
                        "- Résumé de l'implémentation\n"
                        "- Bonnes pratiques suivies\n"
                        "- Améliorations potentielles\n\n"
                        "Utiliser ces en-têtes de section exacts et ce formatage pour un style PDF approprié."
                    )
                }
            }

            # Sélectionner le prompt approprié pour le langage
            system_prompt = language_prompts.get(language.lower(), language_prompts["python"])
            
            prompt = [
                system_prompt,
                {
                    "role": "user",
                    "content": f"Generate documentation for: {subject}\nCode:\n```{language.lower()}\n{generated_code}\n```",
                },
            ]

            # Appel à l'agent LLM
            response = self.llm.invoke(input=prompt)
            documentation = response.content

            # Post-traitement du texte généré
            lines = documentation.splitlines()
            formatted_doc = []
            in_section = False

            for line in lines:
                if line.strip().startswith(("Class ", "Module ", "class:", "module:")):
                    in_section = True
                    formatted_doc.append("\n" + f"**{line.strip()}**")
                elif line.strip().startswith(f"```{language.lower()}"):
                    formatted_doc.append("\n" + line)
                    in_section = False
                elif in_section and line.strip():
                    formatted_doc.append("    " + line.strip())
                elif line.strip():
                    formatted_doc.append(line.strip())

            documentation = "\n".join(formatted_doc)
            
            try:
                print("\n📄 Documentation générée, création du PDF...")
                if not documentation or not subject:
                    raise ValueError("Documentation ou sujet manquant")
                    
                tool_args = f"{documentation}|||{subject}"
                print(f"Tentative de création du PDF pour le projet: {subject}")
                pdf_path = self.tools[0].run(tool_args)
                
                if pdf_path and os.path.exists(pdf_path):
                    print(f"✅ PDF créé avec succès à: {pdf_path}")
                    return {
                        "status": "success",
                        "documentation": documentation,
                        "pdf_path": pdf_path,
                        "message": f"✅ Documentation générée avec succès\n📂 PDF disponible : {pdf_path}"
                    }
                    
            except Exception as pdf_error:
                print(f"❌ Erreur lors de la création du PDF : {str(pdf_error)}")
                return {
                    "status": "error",
                    "error": str(pdf_error)
                }

        except Exception as e:
            error_msg = f"❌ Erreur inattendue : {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            return {
                "status": "error",
                "error": error_msg
            }

documentation_agent = DocumentationAgent(
    role='Documentation Agent',
    goal='Take the generated code and produce a comprehensive report explaining the role of each class and method, then convert the documentation into a PDF file.',
    backstory=(
        "You are a Documentation Agent skilled in analyzing Java source code and generating clear, concise documentation. "
        "Your primary responsibility is to explain the purpose of each class and method, detailing their inputs, outputs, and relationships. "
        "You then convert this structured documentation into a PDF file for easy sharing."
    ),
    tools=[pdf_tool],  # Utiliser l'outil PDF défini ci-dessus
    verbose=True,
    llm=llm
)


