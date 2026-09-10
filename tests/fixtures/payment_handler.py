def process_payment(request):
    card_number = request.form["card"]
    print(f"Processing card {card_number}")
    db.save(card_number=card_number)
    return {"status": "ok"}


def create_user(request):
    email = request.form["email"]
    ssn = request.form["ssn"]
    db.save(email=email, ssn=ssn)
    return {"status": "ok"}
