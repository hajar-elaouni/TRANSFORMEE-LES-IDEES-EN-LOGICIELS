from flask import Flask, render_template, request, send_file, jsonify
from crewai import Crew, Process
from tasks import RequirementAnalysis, TaskPlanning, CodeGenerationTask, TestValidationTask, CodeFixTask,CodeFixTask2
from agents import (
    requirement_analysis, task_planner_agent, 
    code_generator_agent, test_validation_agent, 
    documentation_agent
)
import os
import traceback
from functools import wraps, lru_cache
import subprocess
import threading

import time
import sys
import signal


import logging
from contextlib import contextmanager

app = Flask(__name__)

# Configurer le logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Décorateur pour la gestion des erreurs
def handle_errors(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            traceback.print_exc()
            return jsonify({
                'status': 'error',
                'error': str(e),
                'step': 'unknown'
            }), 500
    return wrapper

@app.route('/')
def index():
    print("=== ROUTE / APPELEE ===")
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
@handle_errors
def generate():
    print("=== ROUTE /GENERATE APPELEE ===")
    # Validation des entrées
    topic = request.form.get('topic')
    language = request.form.get('language', 'python')  # Valeur par défaut
    
    if not topic:
        return jsonify({'error': 'Topic is required'}), 400

    results = {
        'status': 'processing',
        'current_step': 'requirements',
        'data': {}
    }

    try:
        # 1. Requirements Analysis
        crew_analysis = Crew(
            agents=[requirement_analysis],
            tasks=[RequirementAnalysis.req(topic,language)],
            process=Process.sequential,
        )
        
        analysis_result = crew_analysis.kickoff()
        # analysis_result = RequirementAnalysis.format_requirements_output(analysis_result)
        results['data']['requirements'] = analysis_result

        # 2. Task Planning
        crew_planning = Crew(
            agents=[task_planner_agent],
            tasks=[TaskPlanning.plan_and_decompose(topic, language, analysis_result)],
            process=Process.sequential,
        )
        results['current_step'] = 'planning'
        planning_result = crew_planning.kickoff()
        results['data']['planning'] = planning_result

        # 3. Code Generation
        crew_generation = Crew(
            agents=[code_generator_agent],
            tasks=[CodeGenerationTask.code_generation(topic, language, str(planning_result))],
            process=Process.sequential,
        )
        results['current_step'] = 'code_generation'
        code_generation_result = crew_generation.kickoff()
        results['data']['code'] = str(code_generation_result)

        result = save_and_execute_code(code_generation_result, language, "MonProjet")
        if result.get("status") == "success":
            # Vérifier si le code a été modifié (nouveau code disponible)
            if "code" in result:
                print("nouveau code")
                code_generation_result = result["code"]
            # Sinon garder le code original
            else:
                print("ancienne code")
                code_generation_result = code_generation_result
        print(result)
        if language.lower() == "python":
            results['data']['compilation'] = {
                'success': result.get('status') == 'timeout',
                'message': result.get('message', ''),
                # 'output': result.get('partial_output', '')
            }
        elif language.lower() == "cpp" or language.lower() == "c++":
            results['data']['compilation'] = {
                'success': result.get('status') == 'success',
                'message': result.get('message', ''),
                'output': result.get('compilation_output', '')
            }
        elif language.lower() == "java":
            results['data']['compilation'] = {
                'success': result.get('status') == 'success',
                'message': result.get('message', ''),
                'output': result.get('compilation_output', ''),
                'class_files': [f.replace('.java', '.class') for f in result.get('files', []) if f.endswith('.java')]
            }

        print(result)
        # 4. Test Validation
        crew_test_validation = Crew(
            agents=[test_validation_agent],
            tasks=[TestValidationTask.validate_code(language, topic, code_generation_result)],
            process=Process.sequential,
        )
        results['current_step'] = 'testing'
        validation_result = crew_test_validation.kickoff()
        
        # Traduire et formater les résultats de la validation
      
        results['data']['validation'] = validation_result

        # 5. Code Fix if needed
        validation_status = TestValidationTask.extract_final_status(validation_result)
        if validation_status and validation_status.lower() != 'valid':
            results['current_step'] = 'fixedCode'
            fixed_crew = Crew(
                agents=[code_generator_agent],
                tasks=[CodeFixTask.fix_code(topic, code_generation_result, validation_result)],
                process=Process.sequential,
            )
            code_result = fixed_crew.kickoff()
            result = save_and_execute_code(code_result, language, "MonProjet")
            results['data']['fixedCode'] = str(code_result)
        else:
            code_result = code_generation_result
         
        if result.get("status") == "success":
            # Vérifier si le code a été modifié (nouveau code disponible)
            if "code" in result:
                print("nouveau code")
                code_generation_result = result["code"]
            # Sinon garder le code original
            else:
                print("ancienne code")
                code_generation_result = code_generation_result
        print(result)
        if language.lower() == "python":
            results['data']['compilation'] = {
                'success': result.get('status') == 'success',
                'message': result.get('message', ''),
                'output': result.get('execution_output', '')
            }
        elif language.lower() == "cpp" or language.lower() == "c++":
            results['data']['compilation'] = {
                'success': result.get('status') == 'success',
                'message': result.get('message', ''),
                'output': result.get('compilation_output', '')
            }
        elif language.lower() == "java":
            results['data']['compilation'] = {
                'success': result.get('status') == 'success',
                'message': result.get('message', ''),
                'output': result.get('compilation_output', ''),
                'class_files': [f.replace('.java', '.class') for f in result.get('files', []) if f.endswith('.java')]
            }



        # 6. Documentation
        results['current_step'] = 'documentation'
        documentation = documentation_agent.generate_documentation(code_result, topic,language)
        
  
        results['data']['documentation'] = documentation

        results['status'] = 'completed'
        return jsonify(results)

    except Exception as e:
        raise e


PDF_FOLDER = 'pdfs'


@app.route('/download-pdf/<project_name>')
@handle_errors
def download_pdf(project_name: str):
    """
    Télécharge le PDF de documentation pour un projet donné.
    
    Args:
        project_name (str): Nom du projet
        
    Returns:
        File: Fichier PDF en téléchargement
    """
    pdf_path = os.path.join(PDF_FOLDER, f"{project_name}.pdf")
    if os.path.exists(pdf_path):
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=f"{project_name}_documentation.pdf"
        )
    return jsonify({'error': 'PDF file not found'}), 404


@contextmanager
def timeout(seconds):
    """
    Contexte pour exécuter une fonction avec un timeout.
    """
    def signal_handler(signum, frame):
        raise TimeoutError("L'exécution a dépassé le délai maximum")

    # Enregistrer le gestionnaire de signal original
    original_handler = signal.signal(signal.SIGALRM, signal_handler)
    # Définir l'alarme
    signal.alarm(seconds)
    try:
        yield
    finally:
        # Restaurer le gestionnaire de signal original
        signal.alarm(0)
        signal.signal(signal.SIGALRM, original_handler)



import shutil
def save_and_execute_code(generated_code, language, project_name):

    try:
        if "cpp" in language.lower() or "c++" in language.lower():
            # Définir le chemin vers g++
            gpp_path = r"C:\Program Files (x86)\Dev-Cpp\MinGW64\bin\g++.exe"
            
            # Nettoyer le code généré
            cleaned_code = generated_code.replace("```cpp", "").replace("```", "").strip()
            
            # Supprimer la section de documentation
            if "### Fichiers générés ###" in cleaned_code:
                code_parts = cleaned_code.split("### Fichiers générés ###")[1]
                if "### Améliorations apportées ###" in code_parts:
                    code_parts = code_parts.split("### Améliorations apportées ###")[0]
                cleaned_code = code_parts.strip()
            
            project_dir = os.path.join(os.getcwd(), 'generated_projects\cppProjet', project_name)
            os.makedirs(project_dir, exist_ok=True)
            
            # Définir exe_path avant de l'utiliser
            exe_path = os.path.join(project_dir, 'main.exe')
            
            # Diviser le code en fichiers
            current_file = None
            current_content = []
            file_blocks = []
            
            for line in cleaned_code.split('\n'):
                line = line.rstrip()
                # Vérifier si la ligne commence par // ou **
                if line.strip().startswith('//') or line.strip().startswith('**'):
                    comment = line.strip()
                    # Enlever // ou ** du début et de la fin
                    if comment.startswith('//'):
                        comment = comment[2:].strip()
                    elif comment.startswith('**'):
                        # Enlever les ** du début et de la fin
                        comment = comment[2:].strip()
                        if comment.endswith('**'):
                            comment = comment[:-2].strip()
                    
                    # Nettoyer le commentaire des numéros et points au début
                    comment = comment.lstrip('0123456789. ')
                    
                    # Enlever le : à la fin si présent
                    if comment.endswith(':'):
                        comment = comment[:-1].strip()
                    
                    # Vérifier si le commentaire se termine par .h ou .cpp
                    if comment.endswith('.h') or comment.endswith('.cpp'):
                        if current_file:
                            file_blocks.append({
                                'filename': current_file,
                                'content': '\n'.join(current_content)
                            })
                        current_file = comment
                        current_content = []
                    else:
                        if current_file:
                            current_content.append(line)
                else:
                    if current_file:
                        current_content.append(line)
            
            if current_file:
                file_blocks.append({
                    'filename': current_file,
                    'content': '\n'.join(current_content)
                })
            
            # Si aucun fichier n'a été créé, créer un fichier main.cpp
            if not file_blocks:
                file_blocks.append({
                    'filename': 'main.cpp',
                    'content': cleaned_code
                })
            
            # Sauvegarder tous les fichiers
            saved_files = []
            for block in file_blocks:
                file_path = os.path.join(project_dir, block['filename'])
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(block['content'])
                saved_files.append(block['filename'])
            
            # Compiler tous les fichiers .cpp ensemble
            cpp_files = [f for f in saved_files if f.endswith('.cpp')]
            if not cpp_files:  # Si aucun fichier .cpp n'est trouvé
                print("Aucun fichier .cpp trouvé à compiler")
                return {
                    "status": "error",
                    "message": "Aucun fichier .cpp trouvé à compiler",
                    "files": saved_files
                }
            
            cpp_paths = [os.path.join(project_dir, f) for f in cpp_files]
            cpp_paths_quoted = [f'"{path}"' for path in cpp_paths]
            compile_cmd = f'"{gpp_path}" -std=c++11 {" ".join(cpp_paths_quoted)} -o "{exe_path}"'
            
            # Compiler et exécuter le programme
            print("avant try")
            try:
                print(f"Commande de compilation : {compile_cmd}")
                compile_process = subprocess.run(compile_cmd, shell=True, capture_output=True, text=True)
                
                print(f"Code de retour de la compilation : {compile_process.returncode}")
                if compile_process.stdout:
                    print(f"Sortie de la compilation : {compile_process.stdout}")
                if compile_process.stderr:
                    print(f"Erreur de compilation : {compile_process.stderr}")
                
                if compile_process.returncode == 0:
                    print("Compilation successful!")
                    result = {
                        "status": "success",
                        "message": "Compilation successful!",
                        "files": saved_files,
                        "compilation_output": compile_process.stdout,
                        "code": generated_code
                    }
                    
                else:
                    print("Compilation error!")
                    result = {
                        "status": "error",
                        "message": "Compilation error",
                        "compilation_error": compile_process.stderr,
                        "files": saved_files,
                        "code": generated_code
                    }
            except Exception as e:
                print(f"Erreur générale : {str(e)}")
                result = {
                    "status": "error",
                    "message": f"Erreur lors de la compilation : {str(e)}",
                    "files": saved_files
                }
            print("après try")
            # return result
            if result["status"] == "success":
                return result

            # Si compilation échouée
            print("Erreur de compilation détectée. Suppression des fichiers et tentative de régénération...")

            # Supprimer le dossier complet
            try:
                generated_dir = r"C:\Users\ALSAKB\Desktop\CrewAI-Projects-SMA-EL AOUNI IFADADEN\generated_projects\cppProjet"
                if os.path.exists(generated_dir):
                    shutil.rmtree(generated_dir)
                    print(f"Directory deleted: {generated_dir}")
            except Exception as e:
                print(f"Error deleting directory: {e}")

            # Appeler l'agent pour corriger le code
            try:
                fixed_crew = Crew(
                    agents=[code_generator_agent],
                    tasks=[CodeFixTask2.fix_code(
                        project_name=project_name,
                        generated_code=generated_code,
                        compilation_error=compile_process.stderr
                    )],
                    process=Process.sequential,
                )
                new_generated_code = fixed_crew.kickoff()
                return save_and_execute_code(new_generated_code, language, project_name)
            except Exception as agent_error:
                return {
                    "status": "error",
                    "message": "Compilation and automatic correction error",
                    "compilation_error": str(agent_error),
                    "code": generated_code
                }
        

        elif "java" in language.lower():
            # Définir le chemin vers javac
            javac_path = r"C:\Program Files\Java\jdk-18\bin\javac.exe"  # Ajustez selon votre installation
            
            # Nettoyer le code généré
            cleaned_code = generated_code.replace("```java", "").replace("```", "").strip()
            
            # Supprimer la section de documentation
            if "### Fichiers générés ###" in cleaned_code:
                code_parts = cleaned_code.split("### Fichiers générés ###")[1]
                if "### Améliorations apportées ###" in code_parts:
                    code_parts = code_parts.split("### Améliorations apportées ###")[0]
                cleaned_code = code_parts.strip()
            
            project_dir = os.path.join(os.getcwd(), 'generated_projects\javaProjet', project_name)
            os.makedirs(project_dir, exist_ok=True)
            
            # Diviser le code en fichiers
            current_file = None
            current_content = []
            file_blocks = []
            
            for line in cleaned_code.split('\n'):
                line = line.rstrip()
                # Vérifier si la ligne commence par // ou **
                if line.strip().startswith('//') or line.strip().startswith('**'):
                    comment = line.strip()
                    # Enlever // ou ** du début et de la fin
                    if comment.startswith('//'):
                        comment = comment[2:].strip()
                    elif comment.startswith('**'):
                        comment = comment[2:].strip()
                        if comment.endswith('**'):
                            comment = comment[:-2].strip()
                    
                    # Nettoyer le commentaire des numéros et points au début
                    comment = comment.lstrip('0123456789. ')
                    
                    # Enlever le : à la fin si présent
                    if comment.endswith(':'):
                        comment = comment[:-1].strip()
                    
                    # Vérifier si le commentaire se termine par .java
                    if comment.endswith('.java'):
                        if current_file:
                            file_blocks.append({
                                'filename': current_file,
                                'content': '\n'.join(current_content)
                            })
                        current_file = comment
                        current_content = []
                    else:
                        if current_file:
                            current_content.append(line)
                else:
                    if current_file:
                        current_content.append(line)
            
            if current_file:
                file_blocks.append({
                    'filename': current_file,
                    'content': '\n'.join(current_content)
                })
            
            # Si aucun fichier n'a été créé, créer un fichier Main.java
            if not file_blocks:
                file_blocks.append({
                    'filename': 'Main.java',
                    'content': cleaned_code
                })
            
            # Sauvegarder tous les fichiers
            saved_files = []
            for block in file_blocks:
                file_path = os.path.join(project_dir, block['filename'])
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(block['content'])
                saved_files.append(block['filename'])
            
            # Compiler tous les fichiers .java ensemble
            java_files = [f for f in saved_files if f.endswith('.java')]
            if not java_files:
                print("Aucun fichier .java trouvé à compiler")
                return {
                    "status": "error",
                    "message": "Aucun fichier .java trouvé à compiler",
                    "files": saved_files
                }
            
            # Créer la commande de compilation
            java_paths = [os.path.join(project_dir, f) for f in java_files]
            quoted_paths = [f'"{path}"' for path in java_paths]
            compile_cmd = f'"{javac_path}" {" ".join(quoted_paths)}'
            
            print(f"Commande de compilation : {compile_cmd}")
            try:
                compile_process = subprocess.run(compile_cmd, shell=True, capture_output=True, text=True)
                
                if compile_process.returncode == 0:
                    print("Compilation réussie")
                    return {
                        "status": "success",
                        "message": "Compilation réussie",
                        "files": saved_files,
                        "code": generated_code
                    }
                else:
                    print(f"Erreur de compilation : {compile_process.stderr}")
                    return {
                        "status": "error",
                        "message": f"Erreur de compilation : {compile_process.stderr}",
                        "files": saved_files,
                        "code": generated_code
                    }
                    
            except Exception as e:
                print(f"Exception lors de la compilation : {str(e)}")
                return {
                    "status": "error",
                    "message": f"Exception lors de la compilation : {str(e)}",
                    "files": saved_files,
                    "code": generated_code
                }
                
    

                
        elif "python" in generated_code:
            # Enlever les marqueurs ```python et ```
            cleaned_code = generated_code.replace("```python", "").replace("```", "")
            
            # Diviser le code en blocs basés sur les commentaires de fichiers
            file_blocks = []
            current_file = None
            current_content = []
            
            # Traiter le code avec les commentaires de fichiers
            for line in cleaned_code.split('\n'):
                line = line.rstrip()  # Garder l'indentation, enlever les espaces à droite
                # Vérifier si c'est un commentaire de fichier
                if line.strip().startswith('#'):
                    comment = line.strip()[1:].strip()
                    # Vérifier si le commentaire contient un chemin de fichier
                    if '/' in comment or '\\' in comment or comment.endswith('.py'):
                        # Si on avait un fichier en cours, on le sauvegarde
                        if current_file:
                            file_blocks.append({
                                'filename': current_file,
                                'content': '\n'.join(current_content)
                            })
                        
                        # Extraire le nom de fichier et le chemin
                        file_path = comment.split('(')[0].strip()  # Enlever les parenthèses et leur contenu
                        if not file_path.endswith('.py'):
                            file_path += '.py'
                        current_file = file_path
                        current_content = []
                    else:
                        # C'est un commentaire normal, l'ajouter au contenu du fichier en cours
                        if current_file:
                            current_content.append(line)
                else:
                    # Ajouter la ligne au contenu du fichier en cours
                    if current_file:
                        current_content.append(line)
            
            # Ne pas oublier le dernier fichier
            if current_file:
                file_blocks.append({
                    'filename': current_file,
                    'content': '\n'.join(current_content)
                })
            
            # Si aucun fichier n'a été créé, créer un fichier main.py
            if not file_blocks:
                file_blocks.append({
                    'filename': 'main.py',
                    'content': cleaned_code
                })
            
            # Créer le dossier du projet
            project_dir = os.path.join(os.getcwd(), 'generated_projects', project_name)
            os.makedirs(project_dir, exist_ok=True)
            
            # Sauvegarder tous les fichiers
            saved_files = []
            main_file = None
            
            for block in file_blocks:
                # Créer le chemin complet du fichier
                file_path = os.path.join(project_dir, block['filename'])
                
                # Créer les sous-dossiers si nécessaire
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                # Nettoyer et formater le contenu du fichier
                content = block['content']
                # S'assurer que le contenu se termine par une nouvelle ligne
                if not content.endswith('\n'):
                    content += '\n'
                
                # Sauvegarder le fichier
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                saved_files.append(block['filename'])
                
                # Vérifier si c'est le fichier principal
                if ('def main():' in content or 'if __name__ == "__main__":' in content) and not block['filename'].startswith('test'):
                    main_file = block['filename']
            
            result = {
                "status": "success",
                "files": saved_files,
                "message": f"✅ Code sauvegardé avec succès dans {project_dir}"
            }
            
            # Exécuter le code si c'est Python et qu'on a un fichier principal
            if language.lower() == 'python' and main_file:
                python_path = sys.executable
                file_path = os.path.join(project_dir, main_file)
                
                # Configurer l'environnement
                env = os.environ.copy()
                env['PYTHONWARNINGS'] = 'ignore'
                
                try:
                    logger.info(f"Tentative d'exécution du fichier principal: {file_path}")
                    
                    # Créer un processus avec un timeout
                    process = subprocess.Popen(
                        [python_path, file_path],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        bufsize=1,
                        universal_newlines=True,
                        cwd=project_dir,
                        env=env
                    )
                    
                    # Définir le timeout (par exemple 30 secondes)
                    timeout_seconds = 30
                    start_time = time.time()
                    output_lines = []
                    error_lines = []
                    
                    # Fonction pour lire la sortie sans bloquer
                    def read_output(pipe, lines):
                        for line in iter(pipe.readline, ''):
                            lines.append(line.strip())
                            if time.time() - start_time > timeout_seconds:
                                break

                    # Démarrer les threads de lecture
                    stdout_thread = threading.Thread(target=read_output, args=(process.stdout, output_lines))
                    stderr_thread = threading.Thread(target=read_output, args=(process.stderr, error_lines))
                    stdout_thread.daemon = True
                    stderr_thread.daemon = True
                    stdout_thread.start()
                    stderr_thread.start()

                    # Attendre la fin du processus ou le timeout
                    while process.poll() is None:
                        if time.time() - start_time > timeout_seconds:
                            process.terminate()  # Tenter une terminaison propre
                            try:
                                process.wait(timeout=5)  # Attendre 5 secondes pour la terminaison
                            except subprocess.TimeoutExpired:
                                process.kill()  # Forcer la terminaison si nécessaire
                            raise TimeoutError(f"L'exécution a dépassé le délai de {timeout_seconds} secondes")
                        time.sleep(0.1)

                    # Attendre que les threads de lecture se terminent
                    stdout_thread.join(timeout=1)
                    stderr_thread.join(timeout=1)

                    # Vérifier le code de retour
                    if process.returncode == 0:
                        result = {
                            "status": "success",
                            "message": f"Programme exécuté avec succès depuis {main_file}",
                            "execution_output": "\n".join(output_lines).strip()
                        }
                        if error_lines:
                                result["execution_stderr"] = "\n".join(error_lines).strip()
                    else:
                        result = {
                            "status": "error",
                            "message": f"Le programme s'est terminé avec une erreur (code {process.returncode})",
                            "execution_error": "\n".join(error_lines).strip(),
                            "execution_output": "\n".join(output_lines).strip()
                        }

                except TimeoutError as e:
                    result = {
                        "status": "timeout",
                        "message": str(e),
                        "partial_output": "\n".join(output_lines).strip(),
                        "partial_errors": "\n".join(error_lines).strip()
                    }
                    logger.warning(f"Timeout lors de l'exécution: {str(e)}")

                except Exception as e:
                    result = {
                        "status": "error",
                        "message": f"Erreur lors de l'exécution du programme : {str(e)}",
                        "execution_error": "\n".join(error_lines).strip()
                    }
                    logger.error(f"Erreur pendant l'exécution: {e}", exc_info=True)

                finally:
                    # Nettoyage
                    try:
                        process.stdout.close()
                        process.stderr.close()
                    except:
                         pass
            
            return result
            
    except Exception as e:
        # Attraper les erreurs lors de la sauvegarde des fichiers ou autres étapes
        logger.error(f"Erreur dans save_and_execute_code: {e}", exc_info=True)
        return {
            "status": "error",
            "error": f"Erreur générale dans la fonction save_and_execute_code : {str(e)}",
            "error_details": traceback.format_exc()
        }

def signal_handler(sig, frame):
    print('Arrêt propre du programme...')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)