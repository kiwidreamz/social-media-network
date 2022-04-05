document.addEventListener('DOMContentLoaded', function() {




  });

function like(id) {

    // console.log(post.likes)
    fetch(`/like/${id}`, {
        method: "PUT",
        body: JSON.stringify({ like: true})
    })
    .then((response) => response.json())
    .then(post => {
        document.querySelector(`#like_count${id}`).innerHTML = post.likes;

    });

}

function unlike(id) {

    // console.log(post.likes)
    fetch(`/like/${id}`, {
        method: "PUT",
        body: JSON.stringify({ like: false })
    })
    .then((response) => response.json())
    .then(post => {
        document.querySelector(`#like_count${id}`).innerHTML = post.likes;

    });

}

function editpost(post_id) {

    fetch(`/edit/${post_id}`, {
        method: "PUT",
        body: JSON.stringify({ request: body.textarea })
    })
    console.log(body)
    .then((response) => response.json())
    .then(post => {
        document.querySelector(`#${post.id}post_id`).innerHTML = post;

    });

}


