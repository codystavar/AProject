function ifSuccess(response) {
    if(response.ok)
    {
    console.log("USER SUCESSFULLY CREATED.");
        let tID = setTimeout(function () {
            alert("User sucessfully created. You will be redirected to the sign in page.")
            window.location.href = "/";
            window.clearTimeout(tID);
        }, 4000);
    
    }
    else
    {
        console.log("USER FAILED TO CREATE ACCOUNT.")
        alert("Please enter data that does not already exist!")
    }
}

function createAccount() {
    const data = {
        username: document.getElementsByName("username")[0].value,
        firstName: document.getElementsByName("firstName")[0].value,
        secondName: document.getElementsByName("secondName")[0].value,
        email: document.getElementsByName("email")[0].value,
        password: document.getElementsByName("password")[0].value
    };
    url = "http://localhost:3002/api/v1/users";
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