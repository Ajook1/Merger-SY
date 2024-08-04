from flask import Flask, request, send_file, render_template_string
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black

app = Flask(__name__)

@app.route('/')
def index():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Annual Audit Generator</title>
        <style>
            body {
                font-family: 'Roboto', sans-serif;
                background: linear-gradient(to right, #6a11cb, #2575fc);
                color: #fff;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: flex-start;
                min-height: 100vh;
            }
            .container {
                background: rgba(255, 255, 255, 0.9);
                border-radius: 10px;
                box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
                padding: 30px;
                width: 100%;
                max-width: 800px;
                color: #333;
                margin-top: 100px;
            }
            nav {
                position: fixed;
                top: 0;
                width: 100%;
                background-color: #343a40;
                color: white;
                padding: 10px 0;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                z-index: 1000;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            nav .navbar-content {
                display: flex;
                align-items: center;
                max-width: 1200px;
                width: 100%;
                padding: 0 20px;
            }
            nav img {
                height: 40px;
                margin-right: 15px;
            }
            nav h1 {
                font-size: 24px;
                margin: 0;
                padding: 0;
                text-align: center;
                flex-grow: 1;
            }
            h1 {
                text-align: center;
                color: #ffffff;
                margin-bottom: 30px;
            }
            label {
                display: block;
                margin: 10px 0 5px;
                color: #333;
            }
            input[type="file"],
            input[type="text"],
            button {
                width: calc(100% - 22px);
                padding: 10px;
                margin: 5px 0 15px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            input[type="file"] {
                padding: 3px;
            }
            button {
                background-color: #007BFF;
                color: white;
                border: none;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }
            button:hover {
                background-color: #0056b3;
            }
            .section {
                padding: 20px;
                background: #f9f9f9;
                border: 1px solid #ddd;
                border-radius: 8px;
                margin-bottom: 20px;
                position: relative;
                display: flex;
                flex-direction: column;
                gap: 15px;
            }
            .section h2 {
                margin-top: 0;
            }
            .section-content {
                flex-grow: 1;
            }
            .add-button,
            .remove-section-button,
            .remove-pdf-button {
                display: inline-block;
                width: auto;
                padding: 10px 20px;
                margin-top: 10px;
                border-radius: 4px;
            }
            .add-button {
                background-color: #28a745;
            }
            .add-button:hover {
                background-color: #218838;
            }
            .remove-section-button {
                background-color: #dc3545;
                color: white;
                position: absolute;
                top: 15px;
                right: 15px;
            }
            .remove-section-button:hover {
                background-color: #c82333;
            }
            .pdf-input-container {
                display: flex;
                align-items: center;
                position: relative;
                gap: 10px;
            }
            .pdf-input-container input[type="file"] {
                flex-grow: 1;
            }
            .remove-pdf-button {
                background-color: #ffc107;
                color: white;
            }
            .remove-pdf-button:hover {
                background-color: #e0a800;
            }
            #addSectionButton {
                background-color: #17a2b8;
                margin-top: 20px;
            }
            #addSectionButton:hover {
                background-color: #138496;
            }
            #pdfForm button[type="submit"] {
                width: 100%;
                background-color: #007BFF;
                padding: 15px;
                margin-top: 20px;
                border-radius: 4px;
                border: none;
                font-size: 16px;
            }
            #pdfForm button[type="submit"]:hover {
                background-color: #0056b3;
            }
            .cover-page {
                padding: 20px;
                background: #e9ecef;
                border: 1px solid #ddd;
                border-radius: 8px;
                margin-bottom: 20px;
            }
            .cover-page h2 {
                margin-top: 0;
            }
        </style>
    </head>
    <body>
        <nav>
            <div class="navbar-content">
                <img src="logo.png" alt="Logo">
                <h1>Annual Audit Academic Report Generator</h1>
            </div>
        </nav>
        <div class="container">
            <form id="pdfForm" enctype="multipart/form-data" action="/merge" method="post">
                <div id="sectionsContainer">
                    <div class="cover-page">
                        <h2>Cover Page</h2>
                        <label for="cover_page_pdf">Upload Cover Page PDF:</label>
                        <input type="file" id="cover_page_pdf" name="cover_page_pdf" accept="application/pdf">
                    </div>
                    <div class="section" id="fileInputsContainer1">
                        <button type="button" class="remove-section-button" onclick="removeSection(this)">Remove Section</button>
                        <div class="section-content">
                            <h2>Upload PDF Files</h2>
                            <div>
                                <label for="section_title_1">Section Name:</label>
                                <input type="text" id="section_title_1" name="section_title_1" value="Department Profile" placeholder="Like Department Profile" required>
                            </div>
                            <div class="pdf-input-container">
                                <label for="pdf_files_1_1">Select PDF file:</label>
                                <input type="file" id="pdf_files_1_1" name="pdf_files_1_1" accept="application/pdf" required>
                                <button type="button" class="remove-pdf-button" onclick="removeInput(this)">Remove PDF</button>
                            </div>
                        </div>
                        <button type="button" class="add-button" onclick="addFileInput('fileInputsContainer1')">Add Another PDF</button>
                    </div>
                    <div class="section" id="fileInputsContainer2">
                        <button type="button" class="remove-section-button" onclick="removeSection(this)">Remove Section</button>
                        <div class="section-content">
                            <h2>Upload PDF Files</h2>
                            <div>
                                <label for="section_title_2">Section Name:</label>
                                <input type="text" id="section_title_2" name="section_title_2" value="Curricular Aspects" placeholder="Like Curricular Aspects" required>
                            </div>
                            <div class="pdf-input-container">
                                <label for="pdf_files_2_1">Select PDF file:</label>
                                <input type="file" id="pdf_files_2_1" name="pdf_files_2_1" accept="application/pdf" required>
                                <button type="button" class="remove-pdf-button" onclick="removeInput(this)">Remove PDF</button>
                            </div>
                        </div>
                        <button type="button" class="add-button" onclick="addFileInput('fileInputsContainer2')">Add Another PDF</button>
                    </div>
                </div>
                <button type="button" id="addSectionButton" class="add-button">Add New Section</button>
                <button type="submit">Merge PDFs</button>
            </form>
        </div>
        <script>
            let sectionCounter = 2;

            function removeInput(button) {
                button.closest('.pdf-input-container').remove();
            }

            function addFileInput(containerId) {
                const container = document.getElementById(containerId);
                const sectionNumber = containerId.replace('fileInputsContainer', '');
                const inputCount = container.querySelectorAll('.pdf-input-container').length + 1;

                const newInput = document.createElement('div');
                newInput.classList.add('pdf-input-container');
                newInput.innerHTML = `
                    <label for="pdf_files_${sectionNumber}_${inputCount}">Select PDF file:</label>
                    <input type="file" id="pdf_files_${sectionNumber}_${inputCount}" name="pdf_files_${sectionNumber}_${inputCount}" accept="application/pdf" required>
                    <button type="button" class="remove-pdf-button" onclick="removeInput(this)">Remove PDF</button>
                `;
                container.querySelector('.section-content').appendChild(newInput);
            }

            function addSection() {
                sectionCounter++;
                const sectionsContainer = document.getElementById('sectionsContainer');

                const newSection = document.createElement('div');
                newSection.classList.add('section');
                newSection.id = `fileInputsContainer${sectionCounter}`;
                newSection.innerHTML = `
                    <button type="button" class="remove-section-button" onclick="removeSection(this)">Remove Section</button>
                    <div class="section-content">
                        <h2>Upload PDF Files</h2>
                        <div>
                            <label for="section_title_${sectionCounter}">Section Name:</label>
                            <input type="text" id="section_title_${sectionCounter}" name="section_title_${sectionCounter}" placeholder="Section Title" required>
                        </div>
                        <div class="pdf-input-container">
                            <label for="pdf_files_${sectionCounter}_1">Select PDF file:</label>
                            <input type="file" id="pdf_files_${sectionCounter}_1" name="pdf_files_${sectionCounter}_1" accept="application/pdf" required>
                            <button type="button" class="remove-pdf-button" onclick="removeInput(this)">Remove PDF</button>
                        </div>
                    </div>
                    <button type="button" class="add-button" onclick="addFileInput('fileInputsContainer${sectionCounter}')">Add Another PDF</button>
                `;
                sectionsContainer.appendChild(newSection);
            }

            function removeSection(button) {
                button.closest('.section').remove();
            }

            document.getElementById('addSectionButton').addEventListener('click', addSection);
        </script>
    </body>
    </html>
    """
    return render_template_string(html_content)

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
