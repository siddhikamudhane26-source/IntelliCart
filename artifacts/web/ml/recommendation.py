import math
import re
from collections import Counter, defaultdict


TOKEN_PATTERN = re.compile(r"[a-z0-9]+")


def _tokens(text):
    return TOKEN_PATTERN.findall((text or "").lower())


def _product_text(product):
    return " ".join(
        [
            product["name"] or "",
            product["description"] or "",
            product["category_name"] or "",
        ]
    )


def _tfidf_vectors(products):
    documents = [_tokens(_product_text(product)) for product in products]
    document_frequency = Counter()
    for document in documents:
        document_frequency.update(set(document))
    count = max(len(documents), 1)
    vectors = []
    for document in documents:
        term_count = Counter(document)
        vector = {}
        for term, frequency in term_count.items():
            inverse_frequency = math.log((1 + count) / (1 + document_frequency[term])) + 1
            vector[term] = (frequency / len(document)) * inverse_frequency
        vectors.append(vector)
    return vectors


def _cosine_similarity(left, right):
    shared_terms = set(left) & set(right)
    numerator = sum(left[term] * right[term] for term in shared_terms)
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    if not left_norm or not right_norm:
        return 0
    return numerator / (left_norm * right_norm)


def recommend_similar(db, product_id, limit=4):
    products = db.execute(
        """
        SELECT p.*, c.name AS category_name
        FROM products p JOIN categories c ON c.id = p.category_id
        ORDER BY p.id
        """
    ).fetchall()
    target_index = next((index for index, item in enumerate(products) if item["id"] == product_id), None)
    if target_index is None:
        return []
    vectors = _tfidf_vectors(products)
    scored = [
        (index, _cosine_similarity(vectors[target_index], vector))
        for index, vector in enumerate(vectors)
        if index != target_index
    ]
    scored.sort(key=lambda item: (item[1], products[item[0]]["rating"]), reverse=True)
    return [products[index] for index, _score in scored[:limit]]


def recommend_for_customer(db, customer_id, limit=8):
    interacted = db.execute(
        """
        SELECT DISTINCT product_id FROM interactions
        WHERE customer_id = ? ORDER BY created_at DESC LIMIT 8
        """,
        (customer_id,),
    ).fetchall()
    interacted_ids = {row["product_id"] for row in interacted}
    if not interacted_ids:
        return db.execute(
            """
            SELECT p.*, c.name AS category_name FROM products p
            JOIN categories c ON c.id = p.category_id
            ORDER BY p.rating DESC, p.review_count DESC LIMIT ?
            """,
            (limit,),
        ).fetchall()
    candidates = []
    for product_id in interacted_ids:
        candidates.extend(recommend_similar(db, product_id, limit=limit))
    unique = {}
    for product in candidates:
        if product["id"] not in interacted_ids:
            unique[product["id"]] = product
    result = list(unique.values())
    result.sort(key=lambda product: (product["rating"], product["review_count"]), reverse=True)
    return result[:limit]