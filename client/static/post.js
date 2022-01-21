function ifSuccess(response) {
    if(response.ok)
    {
    console.log("POST SUCESSFULLY CREATED.");
        let tID = setTimeout(function () {
            alert("Post sucessfully created. You will be redirected to the posts page.")
            window.location.href = "/myprofile";
            window.clearTimeout(tID);
        }, );

    }
    else
    {
        console.log("FAILED TO CREATE POST.")
        alert("Please try again!")
    }
}
function ifError(){
    alert("Problem!")
}

function post(){

    const data = {
        name: document.getElementsByName("name")[0],
        post: document.getElementsByName("post")[0].value
    };
    url = "http://localhost:3002/api/v1/create-post";
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
function back(){
    window.location.href = "/myprofile";
}