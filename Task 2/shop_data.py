from datetime import datetime, timedelta
import json
import csv
import itertools as it


def export_expiring_products(json_data, filename, days):
    product_data = json_data["products"]
    today = datetime.today()
    new_date = today + timedelta(days)

    with open(filename, "w", newline="") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            ["id", "name", "category", "expires", "days_left"]
        )
        writer.writeheader()
        for el in product_data:
            product_expires_date = datetime.strptime(el["expires"], "%Y-%m-%d")
            if (
                new_date > product_expires_date
                and today < product_expires_date
            ):
                writer.writerow({
                    "id": el["id"],
                    "name": el["name"],
                    "category": el["category"],
                    "expires": el["expires"],
                    "days_left": (
                        product_expires_date.date() - today.date()
                    ).days
                    })


def export_expired_products(json_data, filename):
    product_data = json_data["products"]
    today = datetime.today()

    with open(filename, "w", newline="") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            ["id", "name", "category", "expires", "expired_days_ago"]
        )
        writer.writeheader()
        for el in product_data:
            product_expires_date = datetime.strptime(el["expires"], "%Y-%m-%d")
            if today > product_expires_date:
                writer.writerow({
                    "id": el["id"],
                    "name": el["name"],
                    "category": el["category"],
                    "expires": el["expires"],
                    "expired_days_ago": (
                        today.date() - product_expires_date.date()
                    ).days
                    })


def export_sales_report(json_data, filename):
    product_data = json_data["products"]

    with open("Task 2/sales.json", "r") as json_file:
        sales_data = json.load(json_file)

    data = {}
    products = {}
    sales_report = []

    for el in sales_data["sales"]:
        if el["product_id"] in data:
            data[el["product_id"]] += el["quantity"]
        else:
            data[el["product_id"]] = el["quantity"]

    for el in product_data:
        products[el["id"]] = el

    for key, value in data.items():
        el = products[key]
        sales_report.append({
            "product_name": el["name"],
            "quantity_sold": value,
            "total_revenue": round((el["price"] * value), 2),
        })

    with open(filename, "w", newline="") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            ["product_name", "quantity_sold", "total_revenue"]
        )
        writer.writeheader()
        writer.writerows(sales_report)


def export_category_summary(json_data, filename):
    product_data = json_data["products"]
    product_data.sort(key=lambda el: el["category"])

    with open(filename, "w", newline="") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            ["category", "products_count", "average_price"]
        )
        writer.writeheader()
        for key, data in it.groupby(
            product_data,
            key=lambda el: el["category"]
        ):
            res = list(data)
            total_sum = sum(map(lambda value: value["price"], res))
            writer.writerow({
                "category": key,
                "products_count": len(res),
                "average_price": round(total_sum / len(res), 2)
            })
