from flask import Flask, jsonify, request
import psycopg2
import os

app = Flask(__name__)


# Root / Welcome Endpoint
@app.route("/")
def root():
    return jsonify({
        "message": "Ecommerce Backend is Running",
        "status": "healthy"
    }), 200


# Kubernetes Health Check Endpoint
@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    }), 200


# Database Connection
def get_db_connection():
    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    return connection


# Backend Welcome API
@app.route("/api")
def home():
    return jsonify({
        "message": "Welcome to E-Commerce Backend"
    }), 200


# Get All Products
@app.route("/products", methods=["GET"])
def get_products():

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, name, price FROM products ORDER BY id"
    )

    products = cursor.fetchall()

    cursor.close()
    connection.close()

    result = []

    for product in products:
        result.append({
            "id": product[0],
            "name": product[1],
            "price": float(product[2])
        })

    return jsonify(result), 200


# Create New Product
@app.route("/products", methods=["POST"])
def create_product():

    data = request.get_json()

    name = data["name"]
    price = data["price"]

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO products (name, price) VALUES (%s, %s) RETURNING id",
        (name, price)
    )

    product_id = cursor.fetchone()[0]

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Product created successfully",
        "id": product_id
    }), 201


# Start Flask Application
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )