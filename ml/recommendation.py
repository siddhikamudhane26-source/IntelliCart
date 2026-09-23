from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend_similar(products, selected_product, limit=8):
    if not products or not selected_product: return products[:limit]
    docs=[f"{p.get('category','')} {p.get('name','')} {p.get('description','')}" for p in products]
    target=f"{selected_product.get('category','')} {selected_product.get('name','')} {selected_product.get('description','')}"
    v=TfidfVectorizer(stop_words='english'); m=v.fit_transform(docs+[target]); scores=cosine_similarity(m[-1],m[:-1]).ravel()
    return [p for p,s in sorted(zip(products,scores),key=lambda x:x[1],reverse=True)[:limit]]

def recommend_for_customer(products, customer_history=None, limit=8):
    if not products: return []
    if not customer_history: return sorted(products,key=lambda p:p.get('rating',0),reverse=True)[:limit]
    docs=[f"{p.get('category','')} {p.get('name','')} {p.get('description','')}" for p in products]
    v=TfidfVectorizer(stop_words='english'); m=v.fit_transform(docs+[' '.join(customer_history)]); scores=cosine_similarity(m[-1],m[:-1]).ravel()
    return [p for p,s in sorted(zip(products,scores),key=lambda x:x[1],reverse=True)[:limit]]
