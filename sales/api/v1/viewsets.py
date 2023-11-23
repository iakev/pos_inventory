"""
Model defining viewsets for Sales API's
"""
from datetime import datetime
from decimal import Decimal, ROUND_HALF_EVEN
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
)
from pos_inventory.utils.decorators import response_schema

from products.models import Product, Stock
from sales.models import (
    PaymentMode,
    ProductSales,
    Sales,
    Customer,
    Supplier,
    Purchase,
    PurchaseProduct,
)
from administration.models import Employee, Business
from .serializers import (
    SalesSerializer,
    SalesResponseSerializer,
    GenerateSaleReceiptSerializer,
    GenerateSalesReportSerializer,
    ProductSalesSerializer,
    ProductSalesResponseSerializer,
    ProductSaleUpdateSerializer,
    GetProductSalesSerializer,
    PaymentModeSerializer,
    PaymentModeResponseSerializer,
    CustomerSerializer,
    PurchaseSerializer,
    PurchaseResponseSerializer,
    PurchaseProductSerializer,
    PurchaseProductResponseSerializer,
)


@response_schema(serializer=SalesResponseSerializer)
class SalesViewSet(ViewSet):
    """
    API endpoint that allows Sales to be viewed or edited.
    """

    serializer_class = SalesSerializer
    lookup_field = "uuid"

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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this sale.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def retrieve(self, request, uuid=None):
        """Retrieve a Sale indentified by uuid"""
        sale = get_object_or_404(self.sales_queryset, uuid=uuid)
        serializer = SalesSerializer(sale)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Create a new Sale"""
        serializer = SalesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this sale.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def update(self, request, uuid=None):
        """Update a Sale"""
        sale = get_object_or_404(self.sales_queryset, uuid=uuid)
        serializer = SalesSerializer(sale, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this sale.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def partial_update(self, request, uuid=None):
        """Update a Sale"""
        sale = get_object_or_404(self.sales_queryset, uuid=uuid)
        serializer = SalesSerializer(sale, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this sale.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
        responses={status.HTTP_204_NO_CONTENT: {}},
    )
    def destroy(self, request, uuid=None):
        """Delete a Sale"""
        sale = get_object_or_404(self.sales_queryset, uuid=uuid)
        sale.delete()
        return Response(status=204)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this sale.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
        request=GetProductSalesSerializer,
        responses={status.HTTP_200_OK: ProductSalesResponseSerializer},
    )
    @action(detail=True, methods=["POST"])
    def get_products_information(self, request, uuid=None):
        """
        Get all products and product_sale_info related
        to a speciic sale
        """
        sale = get_object_or_404(self.sales_queryset, uuid=uuid)
        product_sales = sale.product_sales.all()
        serializer = ProductSalesSerializer(product_sales, many=True)
        return Response(serializer.data, status=200)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this sale.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
        request=GenerateSaleReceiptSerializer,
    )
    @action(detail=True, methods=["POST"])
    def generate_receipt(self, request, uuid=None):
        """
        Complete a Sale by adding the requisite data, setting status and
        and amount_paid and generating a receipt/receipt_data
        """
        payment_mode_mapping = dict((y, x) for x, y in PaymentMode.PaymentMethod.choices)
        payment_mode = request.data.get("payment_mode", None)
        amount_paid = request.data.get("amount_paid", None)
        sale = get_object_or_404(self.sales_queryset, uuid=uuid)
        product_sales = sale.product_sales.all()
        receipt_data = {}
        receipt_data["business_name"] = sale.business.name
        receipt_data["business_address"] = sale.business.address
        receipt_data["business_tax_pin"] = sale.business.tax_pin
        receipt_data["business_phone"] = sale.business.phone_number
        receipt_data["business_email"] = sale.business.email_address
        receipt_data["label"] = sale.receipt_label
        receipt_data["product_info"] = []
        total_amount = sale.sale_amount_with_tax
        total_tax = sale.tax_amount

        for product_sale in product_sales:
            product_info = {
                "name": product_sale.product.name,
                "description": product_sale.product.description,
                "unit_price": product_sale.price_per_unit,
                "quantity": product_sale.quantity_sold,
                "total_amount_without_tax": product_sale.price,
                "tax_designation": dict(Product.TaxType.choices)[product_sale.product.tax_type],
                "tax": product_sale.tax_amount,
            }
            receipt_data["product_info"].append(product_info)

        receipt_data["total_amount_without_tax"] = sale.sale_amount_with_tax - sale.tax_amount
        receipt_data["total_tax"] = total_tax
        receipt_data["total_amount"] = Decimal(total_amount)
        receipt_data["payment_mode"] = payment_mode
        receipt_data["total_amount_paid"] = Decimal(amount_paid)
        receipt_data["sale_status"] = dict(Sales.TransactionProgress.choices)[Sales.TransactionProgress.Approved]

        if payment_mode in payment_mode_mapping:
            mapped_payment_mode = payment_mode_mapping[payment_mode]
            payment_mode_obj, _ = PaymentMode.objects.get_or_create(payment_method=mapped_payment_mode)

            # Check if properties is None before creating the till dictionary
            if not payment_mode_obj.properties:
                reset_dict = {
                    1: 0,
                    5: 0,
                    10: 0,
                    20: 0,
                    50: 0,
                    100: 0,
                    200: 0,
                    500: 0,
                    1000: 0,
                }
                payment_mode_obj.properties = reset_dict
                payment_mode_obj.save()

            sale.payment = payment_mode_obj
            sale.save()

            if (
                mapped_payment_mode == PaymentMode.PaymentMethod.CASH
                or mapped_payment_mode == PaymentMode.PaymentMethod.CASH_CREDIT
            ):
                receipt_data["change"] = sale.generate_change(receipt_data["total_amount"], Decimal(amount_paid))

        # Save the payment mode for the sale
        sale.sale_status = Sales.TransactionProgress.Approved
        sale.amount_paid = Decimal(amount_paid)
        sale.change = sale.amount_paid - sale.sale_amount_with_tax
        sale.save()
        return Response(receipt_data)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this sale.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    @action(detail=True, methods=["POST"])
    def break_down_denomination(self, request, uuid=None):
        """
        Breakdown denomination when there is no change available
        """
        sale = get_object_or_404(self.sales_queryset, uuid=uuid)
        denominations = request.denominations
        sale.break_down_denominiations(denominations)

    @extend_schema(
        request=GenerateSalesReportSerializer,
    )
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
        if start_date <= end_date and end_date <= datetime.date(datetime.now()):
            sales_summary = Sales.objects.filter(created_at__date__range=[start_date, end_date])
        if not sales_summary:
            return Response(
                {"message": "No sales found for the given date range"},
                status=400,
            )
        report = {
            "total_sales": 0,
            "tax_amount": 0,
            "profit": 0,
            "sales": [],
        }
        for sale in sales_summary:
            summary = {
                "cashier_id": sale.employee.uuid if sale.employee else None,
                "payment_id": sale.payment.uuid if sale.payment else None,
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
                    "tax_type": dict(Product.TaxType.choices)[product.tax_type],
                    "product_tax": product_sale.tax_amount,
                    "cost": stock.cost_per_unit * product_sale.quantity_sold,
                    "profit": (product_sale.price_per_unit - stock.cost_per_unit) * product_sale.quantity_sold,
                }

                total_tax += product_sale.tax_amount

                total_profit += product_info["profit"]

                summary["products"].append(product_info)
            total_sales += sale.sale_amount_with_tax
            total_tax = sale.tax_amount
            report["total_sales"] += total_sales
            report["tax_amount"] += total_tax
            report["profit"] += total_profit

            report["sales"].append(summary)

        return Response(
            {"sales_report": report},
            status=200,
        )


@response_schema(serializer=ProductSalesResponseSerializer)
class ProductSalesViewset(ViewSet):
    """
    API endpoint that allows Product to be viewed or edited.
    """

    serializer_class = ProductSalesSerializer
    lookup_field = "uuid"

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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this sale.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def retrieve(self, request, uuid=None):
        """
        Retun a single ProductSale
        """
        product_sale = get_object_or_404(self.product_sales_queryset, uuid=uuid)
        serializer = ProductSalesSerializer(product_sale)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Create a new ProductSale"""
        serializer = ProductSalesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this product_sale.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
        request=ProductSaleUpdateSerializer,
    )
    def update(self, request, uuid=None):
        """Update a ProductSale"""
        product_sale = get_object_or_404(self.product_sales_queryset, uuid=uuid)
        serializer = ProductSaleUpdateSerializer(product_sale, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this product_sale.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
        request=ProductSaleUpdateSerializer,
    )
    def partial_update(self, request, uuid=None):
        """Update a ProductSale"""
        product_sale = get_object_or_404(self.product_sales_queryset, uuid=uuid)
        serializer = ProductSaleUpdateSerializer(product_sale, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this ProductSale.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def destroy(self, request, uuid=None):
        """Delete a ProductSale"""
        product_sale = get_object_or_404(self.product_sales_queryset, uuid=uuid)
        sale = product_sale.sale
        sale.sale_amount_with_tax -= product_sale.price + product_sale.tax_amount
        sale.tax_amount -= product_sale.tax_amount
        sale.save()
        product = product_sale.product
        stock = get_object_or_404(self.stock_queryset, product_id=product.id)
        stock.update_stock_quantity(Stock.StockInOutType.Return_in, product_sale.quantity_sold, "Sale undone")
        product_sale.delete()
        return Response(status=204)


class CustomerViewset(ViewSet):
    """API endpoint that allows customer to be viewed or edited"""

    serializer_class = CustomerSerializer
    lookup_field = "uuid"

    @property
    def queryset(self):
        return Customer.objects.all()

    def list(self, request, *args, **kwargs):
        """Returns a list of Customer"""
        serializer = CustomerSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this Customer.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def retrieve(self, request, uuid=None):
        """Retrieves a Customer given its associated identifier"""
        customer = get_object_or_404(self.queryset, uuid=uuid)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Creates a  new customer"""
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this Customer.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def update(self, request, uuid=None):
        """Updates a Customer given its associated identifier"""
        customer = get_object_or_404(self.queryset, uuid=uuid)
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this Customer.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def partial_update(self, request, uuid=None):
        """updates a customer partially given it's identifier"""
        customer = get_object_or_404(self.queryset, uuid=uuid)
        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this Customer.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def destroy(self, request, uuid=None):
        """deletes an existing Customer"""
        customer = get_object_or_404(self.queryset, uuid=uuid)
        customer.delete()
        return Response(status=204)


@response_schema(serializer=PaymentModeResponseSerializer)
class PaymentModeViewSet(ViewSet):
    """API endpoint that allows payment mode to be viewed or edited"""

    serializer_class = PaymentModeSerializer
    lookup_field = "uuid"

    @property
    def queryset(self):
        return PaymentMode.objects.all()

    def list(self, request, *args, **kwargs):
        """Returns a list of all PaymentModes"""
        serializer = PaymentModeSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this Payment Mode.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def retrieve(self, request, uuid=None):
        """Retrieves a PaymentMode given its associated identifier"""
        payment = get_object_or_404(self.queryset, uuid=uuid)
        serializer = PaymentModeSerializer(payment)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Creates a  new PaymentMode"""
        serializer = PaymentModeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this Payment Mode.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def update(self, request, uuid=None):
        """Updates a PaymentMode given its associated identifier"""
        payment = get_object_or_404(self.queryset, uuid=uuid)
        serializer = PaymentModeSerializer(payment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this Payment Mode.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def partial_update(self, request, uuid=None):
        """updates a PaymentMode partially given it's identifier"""
        payment = get_object_or_404(self.queryset, uuid=uuid)
        serializer = PaymentModeSerializer(payment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this Payment Mode.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def destroy(self, request, uuid=None):
        """deletes an existing PaymentMode"""
        payment = get_object_or_404(self.queryset, uuid=uuid)
        payment.delete()
        return Response(status=204)


@response_schema(serializer=PurchaseResponseSerializer)
class PurchaseViewSet(ViewSet):
    """API endpoint that allows purchases to viewed and edited"""

    serializer_class = PurchaseSerializer
    lookup_field = "uuid"

    @property
    def stock_queryset(self):
        return Stock.objects.all()

    @property
    def supplier_queryset(self):
        return Supplier.objects.all()

    @property
    def employee_queryset(self):
        return Employee.objects.all()

    @property
    def purchase_queryset(self):
        return Purchase.objects.all()

    @property
    def product_queryset(self):
        return Product.objects.all()

    def list(self, request, *args, **kwargs):
        """list all purchases"""
        serializer = PurchaseSerializer(self.purchase_queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this Purchase.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def retrieve(self, request, uuid=None):
        """Return a single purchase"""
        purchase = get_object_or_404(self.purchase_queryset, uuid=uuid)
        serializer = PurchaseSerializer(purchase)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """create a new purchase"""
        serializer = PurchaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this Purchase.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def update(self, request, uuid=None):
        """Update a Purchase"""
        purchase = get_object_or_404(self.purchase_queryset, uuid=uuid)
        serializer = PurchaseSerializer(purchase, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this Purchase.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def partial_update(self, request, uuid=None):
        """Update a Purchase"""
        purchase = get_object_or_404(self.purchase_queryset, uuid=uuid)
        serializer = PurchaseSerializer(purchase, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this Purchase.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def destroy(self, request, uuid=None):
        """Delete a Purchase"""
        purchase = get_object_or_404(self.purchase_queryset, uuid=uuid)
        purchase.delete()
        return Response(status=204)

    # TODO: Maybe make an action that list suppliers an products
    # related to a single purchase in a succint manner


@response_schema(serializer=PurchaseProductResponseSerializer)
class PurchaseProductViewSet(ViewSet):
    """
    API endpoint that allows purchaseStock to viewed and edited
    """

    serializer_class = PurchaseProductSerializer
    lookup_field = "uuid"

    @property
    def purchase_product_queryset(self):
        return PurchaseProduct.objects.all()

    @property
    def purchase_queryset(self):
        return Purchase.objects.all()

    @property
    def product_queryset(self):
        return Product.objects.all()

    def list(self, request, *args, **kwargs):
        """list all PurchaseProducts"""
        serializer = PurchaseProductSerializer(self.purchase_product_queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this PurchaseStock.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def retrieve(self, request, uuid=None):
        """Return a single PurchaseProduct"""
        purchase_product = get_object_or_404(self.purchase_product_queryset, uuid=uuid)
        serializer = PurchaseProductSerializer(purchase_product)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Create a new PurchaseProduct"""
        serializer = PurchaseProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this PurchaseProduct.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def update(self, request, uuid=None):
        """Update a PurchaseProduct"""
        purchase_product = get_object_or_404(self.purchase_product_queryset, uuid=uuid)
        serializer = PurchaseProductSerializer(purchase_product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this PurchaseProduct.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def partial_update(self, request, uuid=None):
        """Update a PurchaseProduct"""
        purchase_product = get_object_or_404(self.purchase_product_queryset, uuid=uuid)
        serializer = PurchaseProductSerializer(purchase_product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this PurchaseProduct.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def destroy(self, request, uuid=None):
        """Delete a PurchaseProduct"""
        purchase_product = get_object_or_404(self.purchase_product_queryset, uuid=uuid)
        purchase_product.purchase.purchase_amount -= purchase_product.total_product_cost
        purchase_product.purchase.save()
        purchase_product.delete()
        return Response(status=204)
