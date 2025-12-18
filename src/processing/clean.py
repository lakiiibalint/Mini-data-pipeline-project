from typing import Optional, Dict
import re
import logging

logger = logging.getLogger(__name__)

def to_price(raw_price: Optional[str]) -> Optional[float]:
    if not raw_price:
        return None
    try:
        match = re.search(r"(\d+(?:\.\d+)?)", raw_price)
        if match:
            return float(match.group(1))
        cleaned_price = (
            raw_price.replace("Â", "").replace("£", "").replace("$", "").replace("€", "").strip()
        )
        return float(cleaned_price) if cleaned_price else None
    except ValueError:
        logger.warning(f"Could not parse price: {raw_price}")
        return None


def to_rating(raw_rating: Optional[str]) -> Optional[int]:
    """
    Examples:
        "Five" -> 5
        "3" -> 3
        "4.0" -> 4
        None -> None
    """
    if not raw_rating:
        return None
    
    word_to_num = {
        "zero": 0, "one": 1, "two": 2, "three": 3, 
        "four": 4, "five": 5
    }
    #string
    raw_lower = raw_rating.strip().lower()
    
    if raw_lower in word_to_num:
        return word_to_num[raw_lower]
    #numeric
    try:
        match = re.search(r'(\d+(?:\.\d+)?)', raw_rating) #regex
        if match:
            num = float(match.group(1))
            if 0 <= num <= 5:
                return int(round(num))
    except (ValueError, AttributeError):
        pass
    
    logger.warning(f"Could not parse rating: {raw_rating}")
    return None


def to_availability(raw_availability: Optional[str]) -> Optional[int]:
    """
    Examples:
        "In stock (22 available)" -> 22
        "15 in stock" -> 15
        "Out of Stock" -> None
    """
    if not raw_availability:
        return None

    text = raw_availability.strip().lower()

    if "out of stock" in text or "unavailable" in text:
        return None

    match = re.search(r"(\d+)", text)
    if match:
        try:
            return int(match.group(1))
        except ValueError:
            logger.warning(f"Could not parse availability count: {raw_availability}")
            return None

    if "in stock" in text or "available" in text:
        return 1

    logger.warning(f"Could not parse availability: {raw_availability}")
    return None


#{'title': 'A Light in the Attic', 'price': 'Â£51.77',
#  'availability': 'In stock', 'rating': 3, 
# 'product_page_url': 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'}
def clean_row(row: Dict) -> Optional[Dict]:

    if not row:
        return None

    # Must have
    title = (row.get("title") or "").strip()
    url = (row.get("product_page_url") or "").strip()

    if not title or not url:
        return None

    # Support both scraper-shaped and DB-shaped raw rows
    price_raw = row.get("price_raw") if row.get("price_raw") is not None else row.get("price")
    rating_raw = row.get("rating_raw") if row.get("rating_raw") is not None else row.get("rating")
    availability_raw = row.get("availability_raw") if row.get("availability_raw") is not None else row.get("availability")

    rating_str = None
    if rating_raw is not None:
        rating_str = str(rating_raw)

    return {
        "title": title,
        "price": to_price(price_raw),
        "rating": to_rating(rating_str),
        "availability": to_availability(availability_raw),
        "product_page_url": url,
    }
    