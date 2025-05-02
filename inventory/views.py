from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def inventory_report_pdf(request, month, year):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM monthly_inventory_report(%s, %s)", [month, year])
        report_data = cursor.fetchall()

    template_path = 'reports/inventory_report_pdf.html'
    context = {'report_data': report_data, 'month': month, 'year': year}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="inventory_report_{month}_{year}.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)
    return response

