function ifSuccess(response) {
    if(response.ok)
    {
    console.log("POST SUCESSFULLY LIKED/DISLIKED.");
    let tID = setTimeout(function () {
        window.location.href = "/get_posts";
        window.clearTimeout(tID);
    }, 4000);

    }
    else
    {
        console.log("FAILED TO LIKE/DISLIKE THE POST.")
        alert("Please try again!")
    }
}
function ifError(){
    alert("Problem!")
}
function like(id_post){
    console.log(id_post);
    url = "http://localhost:3002/api/v1/like";
    options = {
        body: JSON.stringify(id_post),
        method: 'UPDATE',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
        }
    };
    fetch(url, options)
    .then(ifSuccess)
    .catch(ifError)
}
function dislike(id_post){
    console.log(id_post);
    url = "http://localhost:3002/api/v1/dislike";
    options = {
        body: JSON.stringify(id_post),
        method: 'UPDATE',
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


