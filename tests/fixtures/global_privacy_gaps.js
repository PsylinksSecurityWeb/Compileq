function initTracking() {
  gtag('config', 'UA-XXXXX-Y');
}

function create_user(request) {
  var dateOfBirth = request.body.dateOfBirth;
  db.save({ dateOfBirth: dateOfBirth });
}
