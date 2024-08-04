# from flask import Flask, request, send_file, render_template
# from PyPDF2 import PdfReader, PdfWriter
# from io import BytesIO
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib.units import inch
# import os

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/merge', methods=['POST'])
# def merge_pdfs():
#     try:
#         sections = {}
#         for key, file in request.files.items():
#             if key.startswith('pdf_files_'):
#                 section_num = key.split('_')[2]
#                 if section_num not in sections:
#                     sections[section_num] = []
#                 sections[section_num].append(file)

#         writer = PdfWriter()
#         for section_num, files in sorted(sections.items(), key=lambda x: int(x[0])):
#             section_title = request.form.get(f'section_title_{section_num}', 'Untitled Section')
            
#             for file in files:
#                 reader = PdfReader(file)
#                 for page_num, page in enumerate(reader.pages):
#                     if page_num == 0:  # Add title only to the first page of each PDF
#                         overlay_title_on_page(writer, page, section_title)
#                     writer.add_page(page)

#         output_stream = BytesIO()
#         writer.write(output_stream)
#         output_stream.seek(0)

#         return send_file(output_stream, as_attachment=True, download_name='merged.pdf')
#     except Exception as e:
#         return f"An error occurred: {e}", 500

# def overlay_title_on_page(writer, page, title):
#     packet = BytesIO()
#     can = canvas.Canvas(packet, pagesize=letter)
    
#     # Define the title style
#     can.setFont("Helvetica-Bold", 18)
#     can.drawString(40, 750, title)  # Adjust the position as needed
    
#     can.save()

#     packet.seek(0)
#     new_pdf = PdfReader(packet)
#     overlay = new_pdf.pages[0]
    
#     # Overlay the title on the existing page
#     page.merge_page(overlay)

# if __name__ == '__main__':
#     app.run(debug=True)


# from flask import Flask, request, send_file, render_template
# from PyPDF2 import PdfReader, PdfWriter
# from io import BytesIO
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from reportlab.lib.colors import black

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/merge', methods=['POST'])
# def merge_pdfs():
#     try:
#         sections = {}
#         for key, file in request.files.items():
#             if key.startswith('pdf_files_'):
#                 section_num = key.split('_')[2]
#                 if section_num not in sections:
#                     sections[section_num] = []
#                 sections[section_num].append(file)

#         writer = PdfWriter()
#         for section_num, files in sorted(sections.items(), key=lambda x: int(x[0])):
#             section_title = request.form.get(f'section_title_{section_num}', 'Untitled Section')
            
#             for file in files:
#                 reader = PdfReader(file)
#                 for page_num, page in enumerate(reader.pages):
#                     if page_num == 0:  # Add title only to the first page of each PDF
#                         page = overlay_title_on_page(page, section_title)
#                     writer.add_page(page)

#         output_stream = BytesIO()
#         writer.write(output_stream)
#         output_stream.seek(0)

#         return send_file(output_stream, as_attachment=True, download_name='merged.pdf')
#     except Exception as e:
#         return f"An error occurred: {e}", 500

# def overlay_title_on_page(page, title):
#     packet = BytesIO()
#     can = canvas.Canvas(packet, pagesize=letter)
    
#     # Title formatting
#     can.setFont("Helvetica-Bold", 24)  # Title size
#     text_width = can.stringWidth(title, "Helvetica-Bold", 24)
#     title_x = (letter[0] - text_width) / 2
#     title_y = letter[1] - 40  # Position just above the content, adjust as needed
    
#     can.drawString(title_x, title_y, title)  # Center align title
    
#     # Draw underline
#     can.setStrokeColor(black)
#     can.setLineWidth(1)
#     can.line(title_x, title_y - 5, title_x + text_width, title_y - 5)
    
#     can.save()

#     packet.seek(0)
#     new_pdf = PdfReader(packet)
#     overlay = new_pdf.pages[0]
    
#     # Overlay the title on the existing page
#     page.merge_page(overlay)
#     return page

# if __name__ == '__main__':
#     app.run(debug=True)

# from flask import Flask, request, send_file, render_template
# from PyPDF2 import PdfReader, PdfWriter
# from io import BytesIO
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from reportlab.lib.colors import black

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/merge', methods=['POST'])
# def merge_pdfs():
#     try:
#         sections = {}
#         for key, file in request.files.items():
#             if key.startswith('pdf_files_'):
#                 section_num = key.split('_')[2]
#                 if section_num not in sections:
#                     sections[section_num] = []
#                 sections[section_num].append(file)

#         writer = PdfWriter()
#         for section_num, files in sorted(sections.items(), key=lambda x: int(x[0])):
#             section_title = request.form.get(f'section_title_{section_num}', 'Untitled Section')
#             added_title = False  # Flag to check if the title has been added

#             for file in files:
#                 reader = PdfReader(file)
#                 for page_num, page in enumerate(reader.pages):
#                     if page_num == 0 and not added_title:  # Add title only on the first page of the section
#                         page = overlay_title_on_page(page, section_title)
#                         added_title = True  # Title added, set flag to True
#                     writer.add_page(page)

#         output_stream = BytesIO()
#         writer.write(output_stream)
#         output_stream.seek(0)

#         return send_file(output_stream, as_attachment=True, download_name='merged.pdf')
#     except Exception as e:
#         return f"An error occurred: {e}", 500

# def overlay_title_on_page(page, title):
#     packet = BytesIO()
#     can = canvas.Canvas(packet, pagesize=letter)
    
#     # Title formatting
#     can.setFont("Helvetica-Bold", 24)  # Title size
#     text_width = can.stringWidth(title, "Helvetica-Bold", 24)
#     title_x = (letter[0] - text_width) / 2
#     title_y = letter[1] - 40  # Position just above the content, adjust as needed
    
#     can.drawString(title_x, title_y, title)  # Center align title
    
#     # Draw underline
#     can.setStrokeColor(black)
#     can.setLineWidth(1)
#     can.line(title_x, title_y - 5, title_x + text_width, title_y - 5)
    
#     can.save()

#     packet.seek(0)
#     new_pdf = PdfReader(packet)
#     overlay = new_pdf.pages[0]
    
#     # Overlay the title on the existing page
#     page.merge_page(overlay)
#     return page

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, send_file, render_template
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/merge', methods=['POST'])
def merge_pdfs():
    try:
        sections = {}
        cover_page = request.files.get('cover_page_pdf')
        for key, file in request.files.items():
            if key.startswith('pdf_files_'):
                section_num = key.split('_')[2]
                if section_num not in sections:
                    sections[section_num] = []
                sections[section_num].append(file)

        writer = PdfWriter()

        # Add cover page first if it exists
        if cover_page:
            cover_pdf = PdfReader(cover_page)
            for page in cover_pdf.pages:
                writer.add_page(page)

        # Add section PDFs
        for section_num, files in sorted(sections.items(), key=lambda x: int(x[0])):
            section_title = request.form.get(f'section_title_{section_num}', 'Untitled Section')
            added_title = False  # Flag to check if the title has been added

            for file in files:
                reader = PdfReader(file)
                for page_num, page in enumerate(reader.pages):
                    if page_num == 0 and not added_title:  # Add title only on the first page of the section
                        page = overlay_title_on_page(page, section_title)
                        added_title = True  # Title added, set flag to True
                    writer.add_page(page)

        output_stream = BytesIO()
        writer.write(output_stream)
        output_stream.seek(0)

        return send_file(output_stream, as_attachment=True, download_name='merged.pdf')
    except Exception as e:
        return f"An error occurred: {e}", 500

def overlay_title_on_page(page, title):
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    
    # Title formatting
    can.setFont("Helvetica-Bold", 24)  # Title size
    text_width = can.stringWidth(title, "Helvetica-Bold", 24)
    title_x = (letter[0] - text_width) / 2
    title_y = letter[1] - 40  # Position just above the content, adjust as needed
    
    can.drawString(title_x, title_y, title)  # Center align title
    
    # Draw underline
    can.setStrokeColor(black)
    can.setLineWidth(1)
    can.line(title_x, title_y - 5, title_x + text_width, title_y - 5)
    
    can.save()

    packet.seek(0)
    new_pdf = PdfReader(packet)
    overlay = new_pdf.pages[0]
    
    # Overlay the title on the existing page
    page.merge_page(overlay)
    return page

if __name__ == '__main__':
    app.run(debug=True)
