from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
import csv
import json
from django.urls import path
from django.template.loader import get_template
from xhtml2pdf import pisa
from core.models import Heading, Paragraph
def home(request):
    return render(request, 'scraper/home1.html')

def scrape(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        # get the required data from soup object
        title = soup.title.string
        headings = []
        for heading_type in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            for heading in soup.find_all(heading_type):
                Heading.objects.create(type=heading_type, text=heading.text.strip())
                headings.append((heading_type,heading.text.strip()))
        paragraphs = []
        print('heading',headings)
        for paragraph in soup.find_all('p'):
            paragraphs.append(paragraph.text.strip())
            Paragraph.objects.create(text=paragraph.text.strip())


        headings_count = {}
        for heading_type_display, heading_type_value in Heading.TYPE_CHOICES:
            headings_count[heading_type_display] = Heading.objects.filter(type=heading_type_display).count()
        
            print('heading_count',headings_count)
        paragraphs_count = Paragraph.objects.count()
        context = {
            'title': title,

            'headings': headings,

            'paragraphs': paragraphs,
            'headings_count_h1': headings_count['h1'],
            'headings_count_h2': headings_count['h2'],
            'headings_count_h3': headings_count['h3'],
            'headings_count_h4': headings_count['h4'],
            'headings_count_h5': headings_count['h6'],
            'headings_count_h6': headings_count['h6'],
            'paragraphs_count': paragraphs_count,
        }
        request.session['scraped_data'] = context
        return render(request, 'scraper/result.html', context)
    else:
        return render(request, 'scaper/home.html')

def download_file(request):
    if 'scraped_data' in request.session:
        context = request.session['scraped_data']
        response = HttpResponse(content_type='')
        if request.POST['download_type'] == 'pdf':
            template_path = 'result.html'
            template = get_template(template_path)
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            filename = f"{context['title']}.pdf"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            buffer = BytesIO()
            pisa_status = pisa.CreatePDF(html, dest=response, encoding='utf-8')
            if pisa_status.err:
                return HttpResponse('PDF generation failed')
        elif request.POST['download_type'] == 'csv':
            response = HttpResponse(content_type='text/csv')
            filename = f"{context['title']}.csv"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            writer = csv.writer(response)
            writer.writerow(['Title', 'Headings', 'Paragraphs'])
            rows = zip([context['title']], context['headings'], context['paragraphs'])
            for row in rows:
                writer.writerow(row)
        elif request.POST['download_type'] == 'json':
            response = HttpResponse(content_type='application/json')
            filename = f"{context['title']}.json"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            json.dump(context, response, indent=4)
        return response
    else:
        return render(request, 'scaper/home.html')