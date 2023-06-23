from fpdf import FPDF
from selectolax.parser import HTMLParser


class PDF(FPDF):
    def html_table(self, html):
        parser = HTMLParser(html)
        table = parser.css_first("table")
        rows = table.css("thead > tr")

        # Process table header data and draw table header
        self.process_table_header(rows)

    def process_table_header(self, rows):

        # get max rows
        for i, row in enumerate(rows):
            cells = row.css('th')
            colspans = []
            for cell in cells:
                colspan = int(cell.attributes.get("colspan", 1))
                colspans.append(colspan)
            count_of_col = 0
            for x in colspans:
                count_of_col += 1
            if i == 0:
                for cell in cells:
                    colspan = int(cell.attributes.get("colspan", 1))
                    rowspan = int(cell.attributes.get("rowspan", 1))
                    content = cell.text().strip()

                    # Calculate cell width and height based on colspan and rowspan
                    line_height = self.font_size
                    cell_width = self.epw / count_of_col
                    cell_height = line_height

                    if colspan == 2:
                        merged_cell_pos = self.x - self.l_margin
                        merged_cell_width = self.epw / count_of_col

                    if rowspan == 2:
                        cell_height = line_height * 2

                    # set font
                    self.set_font(family='EpocaPro', style='', size=10)

                    # Header
                    self.set_font(family='EpocaPro', style='B', size=10)
                    self.multi_cell(w=cell_width, max_line_height=cell_height, txt=content, border=1, align='L', new_x="RIGHT", new_y="TOP")
                self.ln(line_height)
            else:
                self.cell(merged_cell_pos)
                for cell in cells:
                    colspan = int(cell.attributes.get("colspan", 1))
                    rowspan = int(cell.attributes.get("rowspan", 1))
                    content = cell.text().strip()

                    if colspan == 2:
                        merged_cell_pos = self.x - self.l_margin
                        merged_cell_width = self.epw / count_of_col

                    if rowspan == 2:
                        cell_height = line_height * 2

                    # set font
                    self.set_font(family='EpocaPro', style='', size=10)

                    # Calculate cell width and height based on colspan and rowspan
                    line_height = self.font_size
                    cell_width = merged_cell_width / (colspan * 2)
                    # cell_height = line_height * rowspan

                    # Header
                    self.set_font(style='B')
                    self.multi_cell(w=cell_width, max_line_height=cell_height, txt=content, border=1, align='L', new_x="RIGHT", new_y="TOP")
                self.ln(line_height)

# Create a new PDF object
pdf = PDF(orientation='P', unit='pt', format='A4')
pdf.add_font('EpocaPro', style='', fname='fonts/EpocaPro-Regular.ttf')
pdf.add_font('EpocaPro', style='B', fname='fonts/EpocaPro-Bold.ttf')
pdf.add_font('EpocaPro', style='I', fname='fonts/EpocaPro-Italic.ttf')
pdf.add_page()

# HTML table content
html_table = """
<table>
<thead>
<tr>
<th colspan="1" rowspan="2" scope="row"><span class="leitwort"><span class="api" data-type="anker" id="Zf986b50503189d52299b2795dd3f83be">Auskultationsbefunde nach Lokalisation des Herzgeräusches</span></span></th>
<th colspan="2" rowspan="1" scope="col"><span class="leitwort">Befund</span></th>
<th colspan="1" rowspan="2" scope="col"><span class="leitwort">Mögliche Ursachen</span></th>
</tr>
<tr>
<th scope="col"><span class="leitwort">Betroffene Struktur</span></th>
<th scope="col"><span class="leitwort">Geräusch</span></th>
</tr>
</thead>
<table>
"""

# Convert HTML table header to PDF table header
pdf.html_table(html_table)

# Output the PDF
pdf.output("output.pdf")
