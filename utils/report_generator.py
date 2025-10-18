"""
Report generation utilities for exporting analysis results.
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import pandas as pd
from datetime import datetime
import io


def generate_pdf_report(
    title: str,
    sections: list,
    output_path: str = None
) -> bytes:
    """
    Generate a PDF report with multiple sections.
    
    Args:
        title: Report title
        sections: List of dictionaries with 'title' and 'content' keys
        output_path: Optional path to save PDF
        
    Returns:
        PDF bytes
    """
    # Create buffer
    buffer = io.BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(
        buffer if not output_path else output_path,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
    )
    
    # Container for elements
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Title
    elements.append(Paragraph(title, title_style))
    elements.append(Spacer(1, 0.2 * inch))
    
    # Add timestamp
    timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    elements.append(Paragraph(f"Generated: {timestamp}", styles['Normal']))
    elements.append(Spacer(1, 0.3 * inch))
    
    # Add sections
    for section in sections:
        # Section title
        elements.append(Paragraph(section['title'], heading_style))
        
        # Section content
        if isinstance(section['content'], str):
            # Text content
            for line in section['content'].split('\n'):
                if line.strip():
                    elements.append(Paragraph(line, styles['Normal']))
                    elements.append(Spacer(1, 0.1 * inch))
        
        elif isinstance(section['content'], pd.DataFrame):
            # Table content
            elements.append(Spacer(1, 0.2 * inch))
            table_data = [section['content'].columns.tolist()] + section['content'].values.tolist()
            
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(table)
        
        elements.append(Spacer(1, 0.3 * inch))
    
    # Build PDF
    doc.build(elements)
    
    # Get bytes
    if not output_path:
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
    
    return None


def generate_html_report(
    title: str,
    sections: list,
    charts_html: list = None
) -> str:
    """
    Generate an HTML report with charts.
    
    Args:
        title: Report title
        sections: List of dictionaries with 'title' and 'content' keys
        charts_html: Optional list of Plotly chart HTML strings
        
    Returns:
        HTML string
    """
    timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .container {{
                background-color: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #1f77b4;
                text-align: center;
                border-bottom: 3px solid #1f77b4;
                padding-bottom: 20px;
            }}
            h2 {{
                color: #2c3e50;
                margin-top: 30px;
                border-left: 5px solid #1f77b4;
                padding-left: 15px;
            }}
            .timestamp {{
                text-align: center;
                color: #666;
                font-style: italic;
                margin-bottom: 30px;
            }}
            .content {{
                line-height: 1.6;
                color: #333;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }}
            th {{
                background-color: #1f77b4;
                color: white;
                padding: 12px;
                text-align: left;
            }}
            td {{
                padding: 10px;
                border-bottom: 1px solid #ddd;
            }}
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            .chart-container {{
                margin: 30px 0;
            }}
            pre {{
                background-color: #f4f4f4;
                padding: 15px;
                border-radius: 5px;
                overflow-x: auto;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{title}</h1>
            <p class="timestamp">Generated: {timestamp}</p>
    """
    
    # Add sections
    for section in sections:
        html += f"<h2>{section['title']}</h2>\n"
        html += "<div class='content'>\n"
        
        if isinstance(section['content'], str):
            # Convert newlines to HTML
            content = section['content'].replace('\n', '<br>')
            html += f"<p>{content}</p>\n"
        
        elif isinstance(section['content'], pd.DataFrame):
            # Convert DataFrame to HTML table
            html += section['content'].to_html(index=False, classes='data-table')
        
        html += "</div>\n"
    
    # Add charts
    if charts_html:
        html += "<h2>Visualizations</h2>\n"
        for chart_html in charts_html:
            html += f"<div class='chart-container'>{chart_html}</div>\n"
    
    html += """
        </div>
    </body>
    </html>
    """
    
    return html


def create_summary_report(
    stats: dict,
    top_performers: pd.DataFrame,
    bottom_performers: pd.DataFrame,
    insights: str
) -> list:
    """
    Create standardized summary report sections.
    
    Args:
        stats: Summary statistics dictionary
        top_performers: Top performing countries DataFrame
        bottom_performers: Bottom performing countries DataFrame
        insights: Insights text
        
    Returns:
        List of report sections
    """
    sections = [
        {
            'title': 'Executive Summary',
            'content': f"""
Global GDP Growth Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Dataset Coverage:
• {stats['num_countries']} countries analyzed
• {stats['num_years']} years of data
• {stats['total_observations']:,} total observations

Key Metrics:
• Average global GDP growth: {stats['avg_growth']:.2f}%
• Median growth: {stats['median_growth']:.2f}%
• Growth volatility (std dev): {stats['std_growth']:.2f}%
• Range: {stats['min_growth']:.2f}% to {stats['max_growth']:.2f}%
            """
        },
        {
            'title': 'Top Performing Countries',
            'content': top_performers
        },
        {
            'title': 'Bottom Performing Countries',
            'content': bottom_performers
        },
        {
            'title': 'Key Insights',
            'content': insights
        }
    ]
    
    return sections


def export_data_to_excel(
    dataframes: dict,
    output_path: str
) -> None:
    """
    Export multiple DataFrames to Excel with multiple sheets.
    
    Args:
        dataframes: Dictionary of {sheet_name: DataFrame}
        output_path: Path to save Excel file
    """
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        for sheet_name, df in dataframes.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
