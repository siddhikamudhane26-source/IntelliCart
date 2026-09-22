import math


def _distance(left, right):
    return math.sqrt(sum((left[index] - right[index]) ** 2 for index in range(len(left))))


def _kmeans(points, k=4, iterations=12):
    if not points:
        return [], []
    k = min(k, len(points))
    centroids = [points[index] for index in [0, len(points) // 3, (len(points) * 2) // 3, len(points) - 1][:k]]
    assignments = [0] * len(points)
    for _ in range(iterations):
        for index, point in enumerate(points):
            assignments[index] = min(
                range(len(centroids)),
                key=lambda centroid_index: _distance(point, centroids[centroid_index]),
            )
        for centroid_index in range(len(centroids)):
            cluster = [
                point for point, assignment in zip(points, assignments)
                if assignment == centroid_index
            ]
            if cluster:
                centroids[centroid_index] = [
                    sum(point[dimension] for point in cluster) / len(cluster)
                    for dimension in range(len(cluster[0]))
                ]
    return assignments, centroids


def _segment_name(features, centroids, assignment):
    centroid = centroids[assignment]
    recency, frequency, monetary = features
    if centroid[2] > 1.25 and centroid[1] > 1.25:
        return "VIP customers"
    if centroid[0] < 0.9 and centroid[1] > 0.8:
        return "Loyal customers"
    if centroid[0] > 1.4:
        return "At-risk customers"
    return "Growing customers"


def segment_customers(db):
    rows = db.execute(
        """
        SELECT c.id, c.name, c.city,
          COALESCE(julianday('now') - julianday(MAX(o.created_at)), 120) AS recency,
          COUNT(o.id) AS frequency,
          COALESCE(SUM(o.total_amount), 0) AS monetary
        FROM customers c
        LEFT JOIN orders o ON o.customer_id = c.id
        WHERE c.role = 'customer'
        GROUP BY c.id
        ORDER BY monetary DESC
        """
    ).fetchall()
    if not rows:
        return []
    raw_features = [[float(row["recency"]), float(row["frequency"]), float(row["monetary"])] for row in rows]
    maximums = [max(feature[index] for feature in raw_features) or 1 for index in range(3)]
    features = [[feature[index] / maximums[index] for index in range(3)] for feature in raw_features]
    assignments, centroids = _kmeans(features)
    result = []
    for row, feature, assignment in zip(rows, features, assignments):
        result.append(
            {
                "id": row["id"],
                "name": row["name"],
                "city": row["city"],
                "recency": round(row["recency"]),
                "frequency": row["frequency"],
                "monetary": round(row["monetary"], 2),
                "segment": _segment_name(feature, centroids, assignment),
            }
        )
    return result