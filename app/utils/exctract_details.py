import re

def extract_details(transcription):
    """
    Extract selling price, cost price, and product name from Hindi transcription.
    :param transcription: Transcribed text in Hindi
    :return: Extracted details
    """
    # Attempt to find selling price with approximate patterns
    selling_price_match = re.search(r'(\d+)', transcription)  # Match any standalone number
    cost_price_match = re.search(r'कहरीद\s*(\d+)', transcription)  # Match cost price with keyword approximation
    product_name_match = re.search(r'का\s*([\u0900-\u097F]+)', transcription)  # Match Hindi words for product name

    # Extract values
    selling_price = int(selling_price_match.group(1)) if selling_price_match else None
    cost_price = int(cost_price_match.group(1)) if cost_price_match else None
    product_name = product_name_match.group(1) if product_name_match else None

    return {
        "selling_price": selling_price,
        "cost_price": cost_price,
        "product_name": product_name
    }
