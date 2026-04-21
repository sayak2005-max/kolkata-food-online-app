def add_to_cart(session, item):

    cart = session.get("cart", [])

    cart.append(item)

    session["cart"] = cart