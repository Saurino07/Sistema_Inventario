from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Articulo, Responsiva
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

# VISTA 1: Lista de artículos e inventario
def lista_articulos(request):
    articulos = Articulo.objects.all()
    return render(request, 'inventario/lista_articulos.html', {'articulos': articulos})

# VISTA 2: Registrar Salida (Baja del stock) y Generar Responsiva
def registrar_salida(request, articulo_id):
    articulo = get_object_or_404(Articulo, id=articulo_id)

    if request.method == 'POST':
        recibe_nombre = request.POST.get('recibe_nombre')
        recibe_departamento = request.POST.get('recibe_departamento')
        recibe_puesto = request.POST.get('recibe_puesto')
        motivo = request.POST.get('motivo_salida')

        # 1. Restar 1 al stock si hay disponibles
        if articulo.stock > 0:
            articulo.stock -= 1
            if articulo.stock == 0:
                articulo.estado = 'ASIGNADO'
            articulo.save()

            # 2. Crear el registro de responsiva
            responsiva = Responsiva.objects.create(
                articulo=articulo,
                recibe_nombre=recibe_nombre,
                recibe_departamento=recibe_departamento,
                recibe_puesto=recibe_puesto,
                motivo_salida=motivo,
                registrado_por=request.user if request.user.is_authenticated else None
            )

            # Redireccionar a descargar el PDF de la responsiva recién creada
            return redirect('generar_pdf_responsiva', responsiva_id=responsiva.id)

    return render(request, 'inventario/registrar_salida.html', {'articulo': articulo})

# VISTA 3: Generación de archivo PDF dinámico usando ReportLab
def generar_pdf_responsiva(request, responsiva_id):
    responsiva = get_object_or_404(Responsiva, id=responsiva_id)

    # Crear buffer en memoria para almacenar el PDF
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Título del Documento
    p.setFont("Helvetica-Bold", 16)
    p.drawString(150, 750, "CARTA RESPONSIVA DE EQUIPO DE TI")
    
    p.setFont("Helvetica", 11)
    p.drawString(50, 710, f"Fecha de entrega: {responsiva.fecha_entrega.strftime('%Y-%m-%d %H:%M')}")
    p.drawString(50, 690, f"Folio Responsiva: #{responsiva.id}")
    
    # Sección del Receptor
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, 650, "DATOS DEL RESGUARDANTE:")
    p.setFont("Helvetica", 11)
    p.drawString(70, 630, f"Nombre: {responsiva.recibe_nombre}")
    p.drawString(70, 610, f"Departamento: {responsiva.recibe_departamento}")
    p.drawString(70, 590, f"Puesto: {responsiva.recibe_puesto}")
    
    # Sección del Equipo
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, 550, "DATOS DEL EQUIPO ENTREGADO:")
    p.setFont("Helvetica", 11)
    p.drawString(70, 530, f"Artículo: {responsiva.articulo.nombre}")
    p.drawString(70, 510, f"Código Patrimonial: {responsiva.articulo.codigo_patrimonial}")
    p.drawString(70, 490, f"Marca / Modelo: {responsiva.articulo.marca} - {responsiva.articulo.modelo}")
    p.drawString(70, 470, f"Número de Serie: {responsiva.articulo.numero_serie}")

    p.drawString(50, 430, f"Motivo / Observaciones: {responsiva.motivo_salida}")

    # Firmas
    p.line(50, 250, 250, 250)
    p.drawString(80, 235, "Entrega (TI)")
    
    p.line(320, 250, 520, 250)
    p.drawString(350, 235, "Recibe (Conforme)")

    # Finalizar y guardar PDF
    p.showPage()
    p.save()

    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')

from .forms import ArticuloForm

# VISTA 4: Agregar nuevo artículo
def crear_articulo(request):
    if request.method == 'POST':
        form = ArticuloForm(request.POST)
        if form.is_valid():
            form.save() # Guarda el nuevo artículo en PostgreSQL
            return redirect('lista_articulos')
    else:
        form = ArticuloForm()
    
    return render(request, 'inventario/form_articulo.html', {'form': form, 'titulo': 'Registrar Nuevo Artículo'})

# VISTA 5: Editar artículo existente
def editar_articulo(request, articulo_id):
    articulo = get_object_or_404(Articulo, id=articulo_id)
    if request.method == 'POST':
        form = ArticuloForm(request.POST, instance=articulo)
        if form.is_valid():
            form.save()
            return redirect('lista_articulos')
    else:
        form = ArticuloForm(instance=articulo)
    
    return render(request, 'inventario/form_articulo.html', {'form': form, 'titulo': f'Editar: {articulo.nombre}'})
# VISTA 6: Historial de responsivas / entregas
def historial_responsivas(request):
    responsivas = Responsiva.objects.all().order_by('-fecha_entrega')
    return render(request, 'inventario/historial_responsivas.html', {'responsivas': responsivas})