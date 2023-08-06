
def normalize_customer_info(customer=None):
    if customer is None:
        customer = {}

    return {
        'accountAge': customer.get('accountAge', None),
        'emailAddress': customer.get('emailAddress', None) or customer.get('email', None),
        'firstName': customer.get('firstName', None),
        'lastName': customer.get('lastName', None),
        'firstNameKana': customer.get('firstNameKana', None),
        'lastNameKana': customer.get('lastNameKana', None),
        'address': customer.get('address', None),
        'phoneNumber': customer.get('phoneNumber', customer.get('phone', None)),
        'dateOfBirth': customer.get('dateOfBirth', None),
        'legalGender': customer.get('legalGender', customer.get('gender', None)),
        'reference': customer.get('reference', None),
    }


def normalize_product_data(product=None):
    if product is None:
        product = {}

    return {
        'name': product.get('name', None),
        'brand': product.get('brand', None),
        'categories': product.get('categories', None),
        'description': product.get('description', None),
        'gtin': product.get('gtin', None),
        'images': product.get('images', None),
        'reference': product.get('reference', None),
        'url': product.get('url', None),
        'metadata': product.get('metadata', None),
    }


def normalize_price_data(price=None):
    if price is None:
        price = {}

    return {
        'productData': normalize_product_data(price.get('productData', None) or {}),
        'amount': price.get('amount', None),
        'currency': price.get('currency', None),
        'metadata': price.get('metadata', None),
    }


def normalize_line_item_data(line_item=None):
    if line_item is None:
        line_item = {}

    amount = line_item.get('amount', None)
    price = line_item.get('price', None)

    return {
        'price': price if type(price) is str else None,
        'priceData': normalize_price_data(line_item.get('priceData', None) or {
            'productData': {
                'name': line_item.get('name', None),
                'brand': line_item.get('brand', None),
                'categories': line_item.get('categories', None),
                'gtin': line_item.get('gtin', None),
                'images': line_item.get('images', None),
                'reference': line_item.get('reference', None),
                'url': line_item.get('url', None),
                'description': line_item.get('productDescription', None),
                'metadata': line_item.get('productMetadata', None),
            },
            'amount': amount if amount else price if type(price) is int or type(price) is float else None,
            'currency': line_item.get('currency', None),
            'label': line_item.get('label', None),
            'description': line_item.get('priceDescription', None),
            'metadata': line_item.get('priceMetadata', None),
        }),
        'quantity': line_item.get('quantity', None),
        'description': line_item.get('description', None),
        'metadata': line_item.get('metadata', None),
    }


def normalize_line_item_data_list(items=None):
    if items is None:
        items = []

    return list(map(normalize_line_item_data, items)) if type(items) is list else []


def normalize_order_data(order):
    if order is None:
        order = {}

    return {
        'amount': order.get('amount', None),
        'currency': order.get('currency', None),
        'captureMethod': order.get('captureMethod', None),
        'confirmationMethod': order.get('confirmationMethod', None),
        'coupons': order.get('coupons', None),
        'shippingInfo': order.get('shippingInfo', None),
        'lineItemData': normalize_line_item_data_list(order.get('lineItemData', None) or order.get('items', None)),
    }


def normalize_shipping(shipping):
    if shipping is None:
        shipping = {}

    return {
        'address': shipping.get('address', None) or {
            'line1': shipping.get('line1', None),
            'line2': shipping.get('line2', None),
            'line3': shipping.get('line3', None),
            'line4': shipping.get('line4', None),
            'line5': shipping.get('line5', None),
            'subLocality': shipping.get('subLocality', None),
            'locality': shipping.get('locality', None),
            'administrativeArea': shipping.get('administrativeArea', None),
            'postalCode': shipping.get('postalCode', None),
            'country': shipping.get('country', None),
        },
        'addressType': shipping.get('addressType', None),
    }


def normalize_checkout_session_payload(payload):
    if payload is None:
        payload = {}

    return {
        'customerInfo': normalize_customer_info(payload.get('customerInfo', None) or payload.get('customer', None)),
        'orderData': normalize_order_data(payload.get('orderData', None) or {
            'amount': payload.get('amount', None),
            'currency': payload.get('currency', None),
            'captureMethod': payload.get('captureMethod', None),
            'confirmationMethod': payload.get('confirmationMethod', None),
            'coupons': payload.get('coupons', None),
            'shippingInfo': payload.get('shippingInfo', normalize_shipping(payload.get('shipping', None))),
            'items': payload.get('items', None),
            'lineItemData': payload.get('lineItemData', None),
            'description': payload.get('orderDescription', None),
            'metadata': payload.get('orderMetadata', None),
        }),
        'reference': payload.get('reference', None),
        'metadata': payload.get('metadata', None),
        'successUrl': payload.get('successURL', None),  # Temp prop
        'cancelUrl': payload.get('cancelURL', None),  # Temp prop
        'test': payload.get('test', None),  # Temp prop
    }
