"""
Module that describes models (DATABASE tables) related to products, suppliers
and Categories. Forming a basis of inventory control through business logic
"""
from io import BytesIO
from os import name
from PIL import Image
import uuid as uuid_lib

from django.db import models

from django.core.files import File
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from administration.models import Supplier

# Create your models here.
class Category(models.Model):
    """
    Class defining the category that is used to classify products
    contains a slug for easy url constructor
    images and thumbnail also present and a way to get create
    thumbnails if not present
    """
    name = models.CharField(max_length=255)
    uuid = models.UUIDField(editable=False, db_index=True, default=uuid_lib.uuid4)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/{self.uuid}/"
    
    def get_image(self):
        if self.image:
            return "http://127.0.0.1:8000" + self.image.url
        return ""
    
    def get_thumbnail(self):
        if self.thumbnail:
            return "http://127.0.0.1:8000" + self.thumbnail.url
        
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return "http://127.0.0.1:8000" + self.thumbnail.url
            else:
                return ""
            
    def make_thumbnail(self, image, size=(150, 150)):
        img = Image.open(image)
        (width, height) = (300, 200)
        #resize all images to a standard size before generating thumbnails
        img.resize((width,height))
        img.convert('RGB')
        img.thumbnail(size)
        #saving image as file buffer in memory (mimicing a file)
        thumb_io = BytesIO()
        img.save(thumb_io,'JPEG',quality=85)
        #reading converted thumbnail as a file and saving it in variable thumbnail
        thumbnail = File(thumb_io,name=image.name)

        return thumbnail
    
class Product(models.Model):
    """
    Contains the products to be sold by the system and forms the
    basis of the stock
    """
    class UnitOfQuantity(models.TextChoices):
        """
        Enum for Packaging Type of Product and their
        respective codes
        """
        Pair = "PR",_("Pair")
        Cap = "AV", _("Cap")
        Barrel = "BA", _("Barrel")
        bundle = "BE", _("bundle")
        bag = "BG", _("bag")
        block = "BL", _("block")
        BLL_Barrel = "BLL", _("BLL Barrel (petroleum) (158,987 dm3)")
        box = "BX", _("box")
        Can = "CA", _("Can")
        Cell = "CEL", _("Cell")
        centimetre = "CMT", _("centimetre")
        CARAT = "CR", _("CARAT")
        Drum = "DR", _("Drum")
        Dozen = "DZ", _("Dozen")
        Gallon = "GLL", _("Gallon")
        Gram = "GRM", _("GRAM")
        Gross = "GRO", _("Gross")
        Kilogram = "KG", _("Kilogram")
        kilometre = "KTM", _("kilometre")
        kilowatt = "KWT", _("kilowatt")
        Litre = "LTR", _("Litre")
        pound = "LBR", _("pound")
        link = "LK", _("link")
        Metre = "MTR", _("Metre")
        Sqaure_Metre = "M2", _("Square Metre")
        Cubic_Metre = "M3", _("Cubic Metre")
        milligram = "MGM", _("milligram")
        megawatt_hour = "MWT", _("megawatt hour (1000 Kw.h)")
        Number = "NO", _("Number")
        part_per_thousand = "NX", _("part per thousand")
        packet = "PA", _("packet")
        plate = "PG", _("plate")
        reel = "RL", _("reel")
        roll = "RO", _("roll")
        set = "SET", _("set")
        sheet = "ST", _("sheet")
        tonne = "TNE", _("tonne (metric ton)")
        tube = "TU", _("tube")
        Pieces_item_Number = "U", _("Pieces/item[Number]")
        yard = "YRD", _("yard")

    class TaxType(models.TextChoices):
        A = "A", _("A-Exempt")
        B = "B_16", _("B-16%")
        C = "C", _("C-0%")
        D = "D", _("D-Non-VAT")
        E = "E", _("E-8%")

    class ProductType(models.TextChoices):
        """
        Enums for Product Types and thei codes
        """
        Raw_Material = "1", _("Raw Material")
        Finished_Product = "2", _("Finished Product")
        Service = "3", _("Service Without Stock")

    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    uuid = models.UUIDField(editable=False, db_index=True, default=uuid_lib.uuid4)
    code = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)
    product_type = models.CharField(max_length=2, choices=ProductType.choices)
    tax_type = models.CharField(max_length=5, choices=TaxType.choices)
    unit = models.CharField(max_length=5, choices=UnitOfQuantity.choices)
    limited = models.BooleanField(null=True)
    active_for_sale = models.BooleanField(null=True)

    class Meta:
        verbose_name_plural = 'products'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/{self.uuid}/"

class SupplierProduct(models.Model):
    """
    Through table for the many to many relationship of supplier and products
    """
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Stock(models.Model):
    """
    Class with attributes for inventory management
    """
    uuid = models.UUIDField(editable=False, db_index=True, default=uuid_lib.uuid4)
    product_id = models.OneToOneField(Product, primary_key=True, on_delete=models.CASCADE)
    stock_quantity = models.DecimalField(max_digits=10,decimal_places=2,blank=True,default=0.00)
    updated_at = models.DateTimeField(auto_now_add=True)
    cost_per_unit = models.DecimalField(max_digits=6,decimal_places=2)
    price_per_unit_retail = models.DecimalField(max_digits=6,decimal_places=2)
    price_per_unit_wholesale = models.DecimalField(max_digits=6,decimal_places=2)
    reorder_level = models.DecimalField(null=True, max_digits=6, decimal_places=2)
    reorder_quantity = models.DecimalField(null=True, max_digits=6, decimal_places=2)

    class Meta:
        verbose_name_plural ='stocks'
        ordering = ['product_id']
