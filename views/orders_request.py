import sqlite3
import json
from models import Order
from models.metal import Metal
from models.size import Size
from models.style import Style
ORDERS = [
    {
        "id": 1,
        "metal_id": 3,
        "size_id": 2,
        "style_id": 3,
        "timestamp": 1614659931693
    }

]


def get_all_orders():
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            o.id,
            o.metal_id,
            o.size_id,
            o.style_id,
            o.timestamp,
            m.metal metal_metal,
            m.price metal_price,
            s.carets size_carets,
            s.price size_price,
            t.style style_style,
            t.price style_price
        FROM orders o
        JOIN Metals m ON m.id = o.metal_id
        JOIN Sizes s ON s.id = o.size_id
        JOIN Styles t ON t.id = o.style_id
        """)

        # Initialize an empty list to hold all animal representations
        orders = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            order = Order(row['id'], row['metal_id'],
                          row['size_id'], row['style_id'], row['timestamp'])
            # Create a metal instance from the current row
            metal = Metal(row['metal_id'], row['metal_metal'], row['metal_price'])

            # Create a Style instance from the current row
            style = Style(row['style_id'], row['style_style'], row['style_price'])

            # Create a Size instance from the current row
            size = Size(row['size_id'], row['size_carets'], row['size_price'])

            # Add the dictionary representation of related object to the order instance
            order.metal = metal.__dict__
            order.style = style.__dict__
            order.size = size.__dict__

    # Add the dictionary representation of the order to the list
            orders.append(order.__dict__)

    # Use `json` package to properly serialize list as JSON
    return orders


def get_single_order(id):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            o.id,
            o.metal_id,
            o.size_id,
            o.style_id,
            o.timestamp
        FROM orders o
        WHERE o.id = ?
        """, (id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        order = Order(data['id'], data['metal_id'],
                      data['size_id'], data['style_id'], data['timestamp'])

        return order.__dict__


def create_order(new_order):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Orders
            ( metal_id, size_id, style_id, timestamp)
        VALUES
            ( ?, ?, ?, ?);
        """, (new_order['metal_id'], new_order['size_id'],
              new_order['style_id'], new_order['timestamp'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_order['id'] = id

    return new_order


def delete_order(id):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM orders
        WHERE id = ?
        """, (id, ))


def update_order(id, new_order):
    # Iterate the ORDERS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, order in enumerate(ORDERS):
        if order["id"] == id:
            # Found the order. Update the value.
            ORDERS[index] = new_order
            break
