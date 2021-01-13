

# TODO: finish register check and userID and error message
def valid_register(request):
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    rpassword = request.form['rpassword']
    error = ''
    userID = 0
    # other information?
    # checking...
    error = 'test'
    
    return userID, error

# TODO: finish login check and return userID and error message
def valid_login(username, password):
    userID = 0
    error = 'test'
    return userID, error