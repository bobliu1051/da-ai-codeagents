from app.models import BaseModel


class Order(BaseModel):
    table_name = "orders"

    VALID_STATUSES = ["pending", "paid", "shipped", "delivered", "cancelled", "refunded"]

    def is_complete(self):
        return self.status in ("delivered", "refunded")


class OrderItem(BaseModel):
    table_name = "order_items"


class Product(BaseModel):
    table_name = "products"

    def is_in_stock(self):
        return getattr(self, "stock", 0) > 0
