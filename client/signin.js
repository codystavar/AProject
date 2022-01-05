function ifSuccess(response) {
    if(response.ok)
    {
    console.log("USER LOGGED IN.");
    location.href = 'loginredsuc.html';
    }
    else
    {
        console.log("User did not log in")
        location.href = 'loginredfail.html'
    }

}

function ifError(error) {
    console.log(error);
}

function signin() {
    const data = {
        email: document.getElementsByName("email")[0].value,
        password: document.getElementsByName("password")[0].value
    };
    url = "http://localhost:3002/api/v1/sign-in";
    options = {
        body: JSON.stringify(data),
        method: 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
        }
    };

    fetch(url, options)
    .then(ifSuccess)
    .catch(ifError)
}