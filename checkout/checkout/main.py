import os

import stripe
from flask import Flask, jsonify, render_template

secret_key = os.environ["STRIPE_SECRET_KEY"]
publishable_key = os.environ["STRIPE_PUBLISHABLE_KEY"]

stripe.api_key = secret_key

app = Flask(__name__)


@app.after_request
def after_request(response):
    header = response.headers
    # Don't do this in a production environment, '*' is too broad.
    header['Access-Control-Allow-Origin'] = '*'
    return response


@app.route("/", methods=["GET"])
def home_page():
    return render_template("index.html", stripe_publishable_key=publishable_key)


@app.route("/success", methods=["GET"])
def success():
    return render_template("success.html")


@app.route("/cancelled", methods=["GET"])
def cancelled():
    return render_template("cancelled.html")


@app.route("/payments", methods=["POST"])
def create_session():
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        shipping_address_collection={
            "allowed_countries": ["IE"]
        },
        billing_address_collection="auto",
        line_items=[{
            "price_data": {
                "currency": "eurs",
                "product_data": {
                    "name": "T-Shirt"
                },
                "unit_amount": 2000
            },
            "quantity": 1
        }],
        mode="payment",
        success_url="http://127.0.0.1:4242/success",
        cancel_url="http://127.0.0.1:4242/cancel"
    )
    return jsonify(id=session.id)


if __name__ == "__main__":
    app.run(port=4242)
