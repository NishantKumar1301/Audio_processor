from app.models import Transaction


class TransactionAccessor:
    @staticmethod
    def create_or_update_transaction(openai_request, product_name=None, selling_price=None, cost_price=None):

        transaction, created = Transaction.objects.update_or_create(
            openai_request=openai_request,
            defaults={
                "product_name": product_name,
                "selling_price": selling_price,
                "cost_price": cost_price,
            }
        )
        if transaction.selling_price and transaction.cost_price:
            transaction.calculate_profit()
        return transaction

