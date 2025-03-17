from fpdf import FPDF, XPos, YPos
import markdown
from bs4 import BeautifulSoup
import os

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font('DejaVu', '', '/System/Library/Fonts/Supplemental/Arial Unicode.ttf')

def read_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def convert_markdown_to_html(markdown_content):
    return markdown.markdown(markdown_content)

def create_pdf(html_content, output_path):
    pdf = PDF()
    pdf.add_page()
    
    # Set font
    pdf.set_font('DejaVu', size=12)
    
    # Parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Process each element
    for element in soup.find_all(['h1', 'h2', 'h3', 'p', 'li', 'code', 'pre']):
        if element.name in ['h1', 'h2', 'h3']:
            # Handle headers
            pdf.set_font('DejaVu', size=16 if element.name == 'h1' else 14 if element.name == 'h2' else 12)
            pdf.ln(10)
            pdf.multi_cell(0, 10, element.get_text().strip())
        elif element.name == 'p':
            # Handle paragraphs
            pdf.set_font('DejaVu', size=12)
            pdf.ln(5)
            pdf.multi_cell(0, 10, element.get_text().strip())
        elif element.name == 'li':
            # Handle list items
            pdf.set_font('DejaVu', size=12)
            pdf.ln(2)
            pdf.cell(5, 10, "•", new_x=XPos.RIGHT, new_y=YPos.TOP)
            pdf.multi_cell(0, 10, element.get_text().strip())
        elif element.name in ['code', 'pre']:
            # Handle code blocks
            pdf.set_font('DejaVu', size=10)
            pdf.ln(5)
            pdf.multi_cell(0, 8, element.get_text().strip())
    
    # Save PDF
    pdf.output(output_path)

def main():
    # Input and output paths
    input_file = "Project_Description.txt"
    output_file = "project_description.pdf"
    
    # Read markdown content
    markdown_content = read_markdown_file(input_file)
    
    # Convert to HTML
    html_content = convert_markdown_to_html(markdown_content)
    
    # Create PDF
    create_pdf(html_content, output_file)
    print(f"PDF generated successfully: {output_file}")

if __name__ == "__main__":
    main() 