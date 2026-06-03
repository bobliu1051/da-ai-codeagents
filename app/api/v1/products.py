"""
Products API v1.

Mid-generation: uses repositories but doesn't go through a service layer.
Also doesn't require authentication for reads (intentional - product catalog
is public).
"""
from flask import Blueprint, request, jsonify
from app.repositories.product_repo import ProductRepository
from app.utils.cache import get_cache

bp = Blueprint("products_v1", __name__)


@bp.route("/", methods=["GET"])
def list_products():
    cache = get_cache()
    # Cache key includes pagination
    limit = int(request.args.get("limit", 100))
    offset = int(request.args.get("offset", 0))
    cache_key = f"products:list:{limit}:{offset}"
    cached = cache.get(cache_key)
    if cached is not None:
        return jsonify(cached)

    products = ProductRepository().list_active(limit=limit, offset=offset)
    data = [p.to_dict() for p in products]
    cache.set(cache_key, data, ttl=300)
    return jsonify(data)


@bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = ProductRepository().find_by_id(product_id)
    if not product:
        return jsonify({"error": "not found"}), 404
    return jsonify(product.to_dict())


@bp.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "")
    if not query:
        return jsonify([])
    # Note: this is not cached. TODO.
    products = ProductRepository().search(query)
    return jsonify([p.to_dict() for p in products])
