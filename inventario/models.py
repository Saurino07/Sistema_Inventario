from django.db import models
from django.contrib.auth.models import User

# MODELO 1: Categoría de Artículos (ej: Laptops, Monitores, Periféricos)
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

# MODELO 2: Artículo (Inventario del departamento de TI)
class Articulo(models.Model):
    # Opciones fijas para el estado del artículo
    ESTADOS = [
        ('DISPONIBLE', 'Disponible'),
        ('ASIGNADO', 'Asignado (En uso)'),
        ('BAJA', 'Dado de baja / Inoperativo'),
    ]

    codigo_patrimonial = models.CharField(max_length=50, unique=True, help_text="Número de serie o código interno")
    nombre = models.CharField(max_length=150)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='articulos')
    marca = models.CharField(max_length=50, blank=True)
    modelo = models.CharField(max_length=50, blank=True)
    numero_serie = models.CharField(max_length=100, blank=True)
    
    # Control de existencias/estado
    stock = models.PositiveIntegerField(default=1, help_text="Cantidad física disponible")
    estado = models.CharField(max_length=20, choices=ESTADOS, default='DISPONIBLE')
    fecha_ingreso = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - ({self.codigo_patrimonial})"

# MODELO 3: Responsiva / Asignación (Evidencia de baja/entrega de artículo)
class Responsiva(models.Model):
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    
    # Datos de la persona a la que se le entrega/asigna el producto
    recibe_nombre = models.CharField(max_length=150, help_text="Nombre de quien recibe el artículo")
    recibe_departamento = models.CharField(max_length=100, help_text="Área o departamento del empleado")
    recibe_puesto = models.CharField(max_length=100, blank=True)
    
    # Datos del movimiento
    fecha_entrega = models.DateTimeField(auto_now_add=True)
    motivo_salida = models.TextField(help_text="Razón por la cual se entrega el artículo (Asignación, reemplazo, etc.)")
    
    # Usuario del sistema TI que realizó el registro
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Responsiva #{self.id} - {self.articulo.nombre} a {self.recibe_nombre}"