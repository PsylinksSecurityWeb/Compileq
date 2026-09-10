def create_user(request):
    email = request.form["email"]
    date_of_birth = request.form["date_of_birth"]
    db.save(email=email, date_of_birth=date_of_birth)
    return {"status": "ok"}
