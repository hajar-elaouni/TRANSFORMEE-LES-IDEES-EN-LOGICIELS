## https://serper.dev/

from dotenv import load_dotenv
load_dotenv()
import traceback
import requests
from fpdf import FPDF
from datetime import datetime
import json

from langchain.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field



def clean_text_for_pdf(content):
    # Remplacer les caractères non supportés
    replacements = {
        "•": "-",
        "’": "'",
        "“": '"',
        "”": '"',
    }
    for old, new in replacements.items():
        content = content.replace(old, new)
    return content
class PDFGenerator:
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 12)
            self.set_text_color(0, 0, 0)
            self.cell(0, 10, 'Compte rendu', 0, 1, 'C')
            self.ln(10)

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    @staticmethod
    def create_documentation_pdf(content, project_name):
        try:
            content = clean_text_for_pdf(content)
            pdf = PDFGenerator.PDF()
            
            # Page de titre
            pdf.add_page()
            pdf.set_font('Arial', 'B', 24)
            pdf.ln(60)
            pdf.cell(0, 20, project_name, 0, 1, 'C')
            pdf.set_font('Arial', 'I', 14)
            pdf.cell(0, 10, f'Documentation générée le {datetime.now().strftime("%d/%m/%Y")}', 0, 1, 'C')
            
            # Contenu
            pdf.add_page()
            
            # Séparation du contenu en paragraphes
            paragraphs = content.split('\n')
            in_code_block = False
            
            for paragraph in paragraphs:
                if paragraph.strip():
                    # Gestion des blocs de code
                    if paragraph.strip().startswith('```'):
                        in_code_block = not in_code_block
                        continue
                    
                                    # Grands titres (INTRODUCTION, CLASS EXPLANATIONS, CONCLUSION)
                    cleaned_paragraph = paragraph.strip().replace("#", "").replace("**", "").replace("##", "").strip().upper()

                    if cleaned_paragraph in ["INTRODUCTION:", "CLASS EXPLANATIONS:", "CONCLUSION:"]:
                        pdf.set_font('Arial', 'B', 16)
                        pdf.set_text_color(0, 51, 102)  # Bleu foncé
                        pdf.multi_cell(0, 10, cleaned_paragraph)
                        pdf.ln(5)
                    

                    elif paragraph.strip().startswith("**") and paragraph.strip().endswith("**"):
                        # Nettoyer le texte en enlevant les ** et ##
                        clean_text = paragraph.strip().replace("**", "").replace("##", "").strip().upper()
                        pdf.set_font('Arial', 'B', 14)
                        pdf.set_text_color(51, 102, 0)  # Vert foncé
                        pdf.multi_cell(0, 10, clean_text)
                        pdf.ln(5)
                    
                    elif paragraph.strip().startswith("- **") and paragraph.strip().endswith("**"):
                        # Nettoyer le texte en enlevant les **
                        clean_text = paragraph.strip().replace("**", "").strip()
                        pdf.set_font('Arial', 'B', 14)
                        pdf.set_text_color(0, 0, 0)  # Noir
                        pdf.multi_cell(0, 10, clean_text)
                        pdf.ln(5)

                    elif paragraph.strip().startswith("* **") and paragraph.strip().endswith("**"):
                        # Nettoyer le texte en enlevant les **
                        clean_text = paragraph.strip().replace("**", "").strip()
                        pdf.set_font('Arial', 'BU', 10)  # B pour Bold, U pour Underline
                        pdf.set_text_color(0, 0, 0)  # Noir
                        pdf.multi_cell(0, 10, clean_text)
                        pdf.ln(5)
                    
                    # Sous-titres (class: [ClassName])
                    elif paragraph.strip().startswith("class:"):
                        pdf.set_font('Arial', 'B', 14)
                        pdf.set_text_color(51, 102, 0)  # Vert foncé
                        pdf.multi_cell(0, 10, paragraph)
                        pdf.ln(5)

                    
                    
                    # Sections (Purpose, Key Components, etc.)
                    elif paragraph.strip().endswith(":"):
                        pdf.set_font('Arial', 'B', 12)
                        pdf.set_text_color(0, 0, 0)  # Noir
                        pdf.multi_cell(0, 10, paragraph)
                    
                    # Blocs de code
                    elif in_code_block:
                        pdf.set_font('Courier', '', 10)  # Police monospace pour le code
                        pdf.set_text_color(51, 51, 51)  # Gris foncé
                        pdf.set_fill_color(245, 245, 245)  # Fond gris clair
                        pdf.multi_cell(0, 10, paragraph, fill=True)
                    
                    # Texte normal
                    else:
                        pdf.set_font('Arial', '', 12)
                        pdf.set_text_color(0, 0, 0)
                        pdf.multi_cell(0, 10, paragraph)
                        
                    if not in_code_block:
                        pdf.ln(5)

            output_file = fr"\pdfs\{project_name}.pdf"
            pdf.output(output_file, "F")
            print(f"PDF généré avec succès : {output_file}")
            return output_file
            
        except Exception as e:
            print(f"Erreur lors de la génération du PDF : {e}")
            traceback.print_exc()
            return None

class WebSearchInput(BaseModel):
    query: str = Field(description="La requête de recherche")
    num_results: int = Field(default=3, description="Nombre de résultats à retourner")

class WebSearchTool(BaseTool):
    name = "web_search"
    description = "Effectue une recherche web et retourne les résultats pertinents. Prend en paramètre la requête de recherche et optionnellement le nombre de résultats souhaités."
    args_schema: Type[BaseModel] = WebSearchInput

    def _run(self, query: str, num_results: int = 3, run_manager=None) -> str:
        try:
            # Utiliser l'API Serper.dev
            url = "https://google.serper.dev/search"
            
            payload = json.dumps({
                "q": query,
                "num": num_results,
                "gl": "us",       # Pays = États-Unis
                "hl": "en"   
            })
            
            headers = {
                'X-API-KEY': "",  # Obtenir la clé depuis les variables d'environnement
                'Content-Type': 'application/json'
            }
            
            response = requests.post(url, headers=headers, data=payload)
            results = response.json()
            
            if "organic" not in results:
                return "Aucun résultat trouvé. Veuillez reformuler votre recherche."
            
            formatted_results = []
            for result in results["organic"][:num_results]:
                formatted_results.append({
                    "title": result.get("title", ""),
                    "link": result.get("link", ""),
                    "snippet": result.get("snippet", "")
                })
            
            return json.dumps(formatted_results, indent=2, ensure_ascii=False)
            
        except Exception as e:
            return f"Erreur lors de la recherche: {str(e)}"

    async def _arun(self, query: str, num_results: int = 3, run_manager=None) -> str:
        """Méthode asynchrone (non implémentée)"""
        raise NotImplementedError("La recherche web ne supporte pas encore les appels asynchrones")

# Création de l'outil

web_search_tool = WebSearchTool()
