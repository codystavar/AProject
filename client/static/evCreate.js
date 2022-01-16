function ifSuccess(response) {
    if(response.ok)
    {
    console.log("EVENT SUCCESSFULLY CREATED.");
        let tID = setTimeout(function () {
            alert("Event successfully created. You will be redirected to the sign in page.")
            window.location.href = "/myprofile";
            window.clearTimeout(tID);
        }, 4000);

    }
    else
    {
        console.log("USER FAILED TO CREATE EVENT.")
        alert("Please enter data that does not already exist!")
    }
}
function ifError(error){
        console.log("USER FAILED TO CREATE EVENT.");
}

function testCreateEvent() {
    const data = {
        title: document.getElementsByName("title")[0].value,
        startdate: document.getElementsByName("startdate")[0].value,
        enddate: document.getElementsByName("enddate")[0].value
    };

    url = "http://localhost:3002/api/v1/cevents";
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

function backButton(){
    window.location.href = "/myprofile";
}