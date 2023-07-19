"""
Model defining viewsets for Sales API's
"""
from datetime import datetime
from decimal import Decimal, ROUND_HALF_EVEN
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from decimal import Decimal, ROUND_HALF_EVEN
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from products.models import Product, Stock
from sales.models import PaymentMode, ProductSales, Sales, Customer
from administration.models import Employee, Business
from .serializers import (
    PaymentModeSerializer,
    ProductSalesSerializer,
    SalesSerializer,
    CustomerSerializer,
)


class SalesViewSet(ViewSet):
    """
    API endpoint that allows Sales to be viewed or edited.
    """

    @property
    def sales_queryset(self):
        return Sales.objects.all()

    @property
    def customer_queryset(self):
        return Customer.objects.all()

    @property
    def business_queryset(self):
        return Business.objects.all()

    @property
    def payment_queryset(self):
        return PaymentMode.objects.all()

    @property
    def cashier_queryset(self):
        return Employee.objects.all()

    @property
    def product_queryset(self):
        return Product.objects.all()

    def list(self, request, *args, **kwargs):
        """
        List all Sales.
        """
        serializer = SalesSerializer(self.sales_queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Retrieve a Sale indentified by uuid"""
        sale = get_object_or_404(self.sales_queryset, uuid=pk)
        serializer = SalesSerializer(sale)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Create a new Sale"""
        data = request.data
        customer_uuid = data.pop("customer_id", None)
        business_uuid = data.pop("business_id", None)
        cashier_uuid = data.pop("cashier_id", None)
        receipt_type = data.get("receipt_type", None)
        transaction_type = data.get("transaction_type", None)
        if customer_uuid and business_uuid and cashier_uuid:
            customer = get_object_or_404(self.customer_queryset, uuid=customer_uuid)
            business = get_object_or_404(self.business_queryset, uuid=business_uuid)
            cashier = get_object_or_404(self.cashier_queryset, uuid=cashier_uuid)
            data["customer_id"] = customer.id
            data["business_id"] = business.id
            data["cashier_id"] = cashier.id
            data["receipt_label"] = transaction_type + receipt_type
        serializer = SalesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        """Update a Sale"""
        sale = get_object_or_404(self.sales_queryset, uuid=pk)
        serializer = SalesSerializer(sale, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def partial_update(self, request, pk=None):
        """Update a Sale"""
        sale = get_object_or_404(self.sales_queryset, uuid=pk)
        serializer = SalesSerializer(sale, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        """Delete a Sale"""
        sale = get_object_or_404(self.sales_queryset, uuid=pk)
        sale.delete()
        return Response(status=204)

    @action(detail=True, methods=["post"])
    def generate_receipt(self, request, pk=None):
        """
        Complete a Sale by adding the requisite data and creating the related
        product sale object
        """
        payment_mode = request.data.get("payment_mode")
        amount_paid = request.data.get("amount_paid")
        sale = get_object_or_404(self.sales_queryset, uuid=pk)
        business = get_object_or_404(Business, id=sale.business)
        product_sales = sale.product_sales.all()
        receipt_data = {}
        receipt_data["business_name"] = business.name
        receipt_data["business_address"] = business.address
        receipt_data["business_tax_pin"] = business.tax_pin
        receipt_data["business_phone"] = business.phone_number
        receipt_data["business_email"] = business.email_address
        receipt_data["label"] = sale.receipt_label
        receipt_data["product_info"] = {}
        for product_sale in product_sales:
            receipt_data["product_info"]["name"] = product_sale.product.name
            receipt_data["product_info"][
                "description"
            ] = product_sale.product.description
            receipt_data["product_info"]["unit_price"] = product_sale.price_per_unit
            receipt_data["product_info"]["quantity"] = product_sale.quantity_sold
            receipt_data["product_info"][
                "total_amount_without_tax"
            ] = product_sale.price
            receipt_data["product_info"][
                "tax-designation"
            ] = product_sale.product.tax_type
            receipt_data["product_info"]["Total Tax"] = product_sale.sale.tax_amount
            receipt_data["product_info"][
                "Sale Amount with Tax"
            ] = product_sale.sale.sale_amount_with_tax
            receipt_data["Total amount paid"] = amount_paid

        if (
            payment_mode == PaymentMode.PaymentMethod.CASH
            or payment_mode == PaymentMode.PaymentMethod.CASH_CREDIT
        ):
            receipt_data["change"] = sale.generate_change(
                receipt_data["Sale Amount with tax"], amount_paid
            )
        return Response(receipt_data)

    @action(detail=True, methods=["POST"])
    def break_down_denomination(self, request, pk=None):
        """
        Breakdown denomination when there is no change available
        """
        sale = get_object_or_404(self.sales_queryset, uuid=pk)
        denominations = request.denominations
        sale.break_down_denominiations(denominations)

    @action(detail=False, methods=["POST"])
    def generate_sales_report(self, request, *args, **kwargs):
        """
        Generate sales report based on date given
        """
        data = request.data
        start_date = data.get("start_date", None)
        end_date = data.get("end_date", None)
        if start_date and end_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        else:
            return Response(
                {"message": "Please provide a start date and end date"},
                status=400,
            )
        sales_summary = Sales.objects.filter(
            created_at__date__range=[start_date, end_date]
        )
        if not sales_summary:
            return Response(
                {"message": "No sales found for the given date range"},
                status=400,
            )
        report = {
            "total_sales": 0,
            "tax_amount": 0,
            "profit": 0,
            "sales_report": [],
        }
        for sale in sales_summary:
            summary = {
                "cashier_id": sale.cashier_id.id if sale.cashier_id else None,
                "payment_id": sale.payment_id.id if sale.payment_id else None,
                "receipt_label": sale.receipt_label,
                "sale_amount": sale.sale_amount_with_tax,
                "products": [],
            }
            total_tax = 0
            total_sales = 0
            total_profit = 0

            product_sales = sale.product_sales.all()
            for product_sale in product_sales:
                product = product_sale.product
                stock = get_object_or_404(Stock, pk=product_sale.product.id)
                product_info = {
                    "product_name": product.name,
                    "product_description": product.description,
                    "product_unit_price": product_sale.price_per_unit,
                    "product_quantity": product_sale.quantity_sold,
                    "product_price": product_sale.price,
                    "tax_type": product.tax_type,
                    "product_tax": product_sale.tax_amount,
                    "cost": stock.cost_per_unit * product_sale.quantity_sold,
                    "profit": (product_sale.price_per_unit - stock.cost_per_unit)
                    * product_sale.quantity_sold,
                }

                total_tax += product_sale.tax_amount
                total_sales += product_sale.price
                total_profit += product_info["profit"]

                summary["products"].append(product_info)

            report["total_sales"] += total_sales
            report["tax_amount"] += total_tax
            report["profit"] += total_profit

            report["sales_report"].append(summary)

        return Response(
            {"sales_report": report},
            status=200,
        )


class ProductSalesViewset(ViewSet):
    """
    API endpoint that allows Product to be viewed or edited.
    """

    @property
    def product_sales_queryset(self):
        return ProductSales.objects.all()

    @property
    def sales_queryset(self):
        return Sales.objects.all()

    @property
    def product_queryset(self):
        return Product.objects.all()

    @property
    def stock_queryset(self):
        return Stock.objects.all()

    def list(self, request, *args, **kwargs):
        """
        List all ProductSales.
        """
        serializer = ProductSalesSerializer(self.product_sales_queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Retun a single ProductSale
        """
        product_sale = get_object_or_404(self.product_sales_queryset, uuid=pk)
        serializer = ProductSalesSerializer(product_sale)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Create a new ProductSale"""
        data = request.data
        product_uuid = data.pop("product", None)
        sale_uuid = data.pop("sale", None)
        quantity_sold = data.get("quantity_sold", "0")
        product = get_object_or_404(self.product_queryset, uuid=product_uuid)
        sale = get_object_or_404(self.sales_queryset, uuid=sale_uuid)
        data["product"] = product.id
        data["sale"] = sale.id
        stock = get_object_or_404(self.stock_queryset, product_id=product.id)
        if data["is_wholesale"]:
            data["price_per_unit"] = stock.price_per_unit_wholesale
        else:
            data["price_per_unit"] = stock.price_per_unit_retail
        data["price"] = Decimal(quantity_sold) * Decimal(data["price_per_unit"])
        data["tax_rate"] = product.tax_type
        data["tax_amount"] = (
            product.get_total_amount(Decimal(data["price"]), product.tax_type)
            - Decimal(data["price"])
        ).quantize(Decimal("0.00"), rounding=ROUND_HALF_EVEN)
        serializer = ProductSalesSerializer(data=data)
        if serializer.is_valid():
            sale.sale_amount_with_tax += product.get_total_amount(
                Decimal(data["price"]), product.tax_type
            )
            sale.tax_amount += data["tax_amount"]
            stock.update_stock_quantity(
                Stock.StockInOutType.Sale, quantity_sold, "Sale made"
            )
            sale.save()
            stock.save()
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        """Update a ProductSale"""
        product_sale = get_object_or_404(self.product_sales_queryset, uuid=pk)
        serializer = ProductSalesSerializer(product_sale, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def partial_update(self, request, pk=None):
        """Update a ProductSale"""
        product_sale = get_object_or_404(self.product_sales_queryset, uuid=pk)
        serializer = ProductSalesSerializer(
            product_sale, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        """Delete a ProductSale"""
        product_sale = get_object_or_404(self.product_sales_queryset, uuid=pk)
        sale = product_sale.sale
        sale.sale_amount_with_tax -= product_sale.price + product_sale.tax_amount
        sale.tax_amount -= product_sale.tax_amount
        sale.save()
        product = product_sale.product
        stock = get_object_or_404(self.stock_queryset, product_id=product.id)
        stock.update_stock_quantity(
            Stock.StockInOutType.Return_in, product_sale.quantity_sold, "Sale undone"
        )
        stock.save()
        product_sale.delete()
        return Response(status=204)


class CustomerViewset(ViewSet):
    """API endpoint that allows customer to be viewed or edited"""

    @property
    def queryset(self):
        return Customer.objects.all()

    def list(self, request, *args, **kwargs):
        """Returns a list of Customer"""
        serializer = CustomerSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Retrieves a Customer given its associated identifier"""
        customer = get_object_or_404(self.queryset, uuid=pk)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Creates a  new customer"""
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        """Updates a Customer given its associated identifier"""
        customer = get_object_or_404(self.queryset, uuid=pk)
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def partial_update(self, request, pk=None):
        """updates a customer partially given it's identifier"""
        customer = get_object_or_404(self.queryset, uuid=pk)
        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        """deletes an existing Customer"""
        customer = get_object_or_404(self.queryset, uuid=pk)
        customer.delete()
        return Response(status=204)


class PaymentModeViewSet(ViewSet):
    """API endpoint that allows payment mode to be viewed or edited"""

    @property
    def queryset(self):
        return PaymentMode.objects.all()

    def list(self, request, *args, **kwargs):
        """Returns a list of Customer"""
        serializer = PaymentModeSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Retrieves a Customer given its associated identifier"""
        payment = get_object_or_404(self.queryset, uuid=pk)
        serializer = PaymentModeSerializer(payment)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Creates a  new customer"""
        serializer = PaymentModeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        """Updates a Customer given its associated identifier"""
        payment = get_object_or_404(self.queryset, uuid=pk)
        serializer = PaymentModeSerializer(payment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def partial_update(self, request, pk=None):
        """updates a customer partially given it's identifier"""
        payment = get_object_or_404(self.queryset, uuid=pk)
        serializer = PaymentModeSerializer(payment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        """deletes an existing Customer"""
        payment = get_object_or_404(self.queryset, uuid=pk)
        payment.delete()
        return Response(status=204)
