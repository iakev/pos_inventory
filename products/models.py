"""
Module that describes models (DATABASE tables) related to products, suppliers
and Categories. Forming a basis of inventory control through business logic
"""
from decimal import Decimal
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    class PackagingUnit(models.TextChoices):
        """
        Enum for packaging unit type of product and their associated
        codes
        """
        Ampoule = "AM", _("Ampoule")
        Barrel = "BA", _("Barrel")
        Bottlecrate = "BC", _("Bottlecrate")
        Bundle = "BE", _("Bundle")
        Balloon = "BF", _("Balloon")
        Bag = "BG", _("Bag")
        Bucket = "BJ", _("Bucket")
        Basket = "BK", _("Basket")
        Bale = "BL", _("Bale")
        Bottle_cylindrical = "BQ", _("Bottle protected cylindrical")
        Bar = "BR", _("Bar")
        Bottle_bulbous = "BV", _("Bottle bulbous")
        Can = "CA", _("Can")
        Chest = "CH", _("Chest")
        Coffin = "CJ", _("Coffin")
        Coil = "CL", _("Coil")
        Box_wooden = "CR", _("Wooden Box, Wooden Case")
        Cassette = "CS", _("Cassette")
        Carton = "CT", _("Carton")
        Container = "CTN", _("Container")
        Cylinder = "CY", _("Cylinder")
        Drum = "DR", _("Drum")
        Extra_countable_item = "GT", _("Extra Countable Item")
        Hand_baggage = "HH", _("Hand Baggage")
        Ingots = "IZ", _("Ingots")
        Jar = "JR", _("Jar")
        Jug = "JU", _("Jug")
        Jerry_can_cylindrical = "JY", _("Jerry CAN Cylindrical")
        Canester = "KZ", _("Canester")
        Logs_in_bundle_bunch_truss = "LZ", _("Logs, in bundle/bunch/truss")
        Net = "NT", _("Net")
        Non_exterior_packaging_unit = "OU", _("Non-Exterior Packaging Unit")
        Poddon = "PD" ,  _("Poddon")
        Plate = "PG" ,  _("Plate")
        Pipe = "PI" ,  _("Pipe")
        Pilot = "PO" ,  _("Pilot")
        Traypack = "PU" ,  _("Traypack")
        Reel = "RL" ,  _("Reel")
        Roll = "RO" ,  _("Roll")
        Rods_in_bundle_bunch_truss = "RZ",  _("Rods, in bundle/bunch/truss")
        Skeletoncase = "SK" ,  _("Skeletoncase")
        Tank_cylindrical = "TY" ,  _("Tank, cylindrical")
        Bulk_gas_at_1031_mbar_15_oC = "VG" ,  _("Bulk, gas(at 1031 mbar 15 oC)")
        Bulk_liquid_at_normal_temperature_pressure = "VL" ,  _("Bulk, liquid(at normal temperature/pressure)")
        Bulk_solid_large_particles_nodules = "VO" ,  _("Bulk, solid, large particles(nodules)")
        Bulk_gas_liquefied_at_abnormal_temperature_pressure = "VQ" ,  _("Bulk, gas(liquefied at abnormal temperature/pressure)")
        Bulk_solid_granular_particles_grains = "VR" ,  _("Bulk, solid, granular particles(grains)")
        Extra_bulk_item = "VT" ,  _("Extra Bulk Item")
        Bulk_fine_particles_powder = "VY" ,  _("Bulk, fine particles(\"powder\")")
        Mills = "ML" ,  _("Mills cigarette")
        TAN = "TN" ,  _("TAN 1TAN REFER TO 20BAGS")

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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(editable=False, db_index=True, default=uuid_lib.uuid4)
    code = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)
    product_type = models.CharField(max_length=2, choices=ProductType.choices)
    tax_type = models.CharField(max_length=5, choices=TaxType.choices)
    packaging_unit = models.CharField(max_length=4, choices=PackagingUnit.choices)
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
    class StockInOutType(models.TextChoices):
        """
        Enumeration for stock movement (in/out)
        """
        Import = "01", _("Incoming-Import")
        Purchase = "02", _("Incoming-Purchase")
        Return_in = "03", _("Incoming-Return")
        Stock_movement_in = "04", _("Incoming-Stock Movement")
        Processing_in = "05", _("Incoming-Processing")
        Adjustment_in = "06", _("Incoming-Adjustment")
        Sale = "11", _("Outgoing-Sale")
        Return_out = "12", _("Outgoing-Return")
        Stock_movement_out = "13", _("Outgoing-Stock Movement")
        Processing_out = "14", _("Outgoing-Processing")
        Discarding = "15", _("outgoing-Discarding")
        Adjustment_out = "16", _("outgoing-Adjustment")

    uuid = models.UUIDField(editable=False, db_index=True, default=uuid_lib.uuid4)
    product_id = models.OneToOneField(Product, primary_key=True, on_delete=models.CASCADE)
    stock_quantity = models.DecimalField(max_digits=10,decimal_places=2,blank=True,default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cost_per_unit = models.DecimalField(max_digits=6,decimal_places=2)
    price_per_unit_retail = models.DecimalField(max_digits=6,decimal_places=2)
    price_per_unit_wholesale = models.DecimalField(max_digits=6,decimal_places=2)
    reorder_level = models.DecimalField(null=True, max_digits=6, decimal_places=2)
    reorder_quantity = models.DecimalField(null=True, max_digits=6, decimal_places=2)
    stock_movement_type = models.CharField(null=True, max_length=4, choices=StockInOutType.choices)
    stock_movement_quantity = models.DecimalField(null=True, max_digits=6,decimal_places=2)
    stock_movement_remarks = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural ='stocks'
        ordering = ['product_id']

    def switch_stock_case(self, stock_movement_type, stock_movement_quantity, stock_movement_remarks):
        """
        Encapsulating the stock-movement type and its respective quantity.
        """
        if stock_movement_type in [
            self.StockInOutType.Import,
            self.StockInOutType.Purchase,
            self.StockInOutType.Return_in,
            self.StockInOutType.Stock_movement_in,
            self.StockInOutType.Processing_in,
            self.StockInOutType.Adjustment_in
        ]:
            stock_movement_quantity = Decimal(stock_movement_quantity)
            self.stock_quantity += stock_movement_quantity
            self.stock_movement_remarks = stock_movement_remarks
        elif stock_movement_type in [
            self.StockInOutType.Sale,
            self.StockInOutType.Return_out,
            self.StockInOutType.Stock_movement_out,
            self.StockInOutType.Processing_out,
            self.StockInOutType.Discarding,
            self.StockInOutType.Adjustment_out
        ]:
            stock_movement_quantity = Decimal(stock_movement_quantity)
            self.stock_quantity -= stock_movement_quantity
            self.stock_movement_remarks = stock_movement_remarks

    def update_stock_quantity(self, stock_movement_type, stock_movement_quantity, stock_movement_remarks):
        """
        Update Stock quantity according to the given stock_movement_type
        """
        self.switch_stock_case(stock_movement_type, stock_movement_quantity, stock_movement_remarks)
        self.save()
