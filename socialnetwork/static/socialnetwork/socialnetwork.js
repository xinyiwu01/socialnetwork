"use strict"


// Sends a new request to update the to-do list
function getGlobal() {
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return
        updatePage(xhr)
    }

    xhr.open("GET", "/socialnetwork/get-global", true)
    xhr.send()
}

function getFollower() {
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return
        updatePageFollower(xhr)
    }

    xhr.open("GET", "/socialnetwork/get-follower", true)
    xhr.send()
}

function updatePage(xhr) {
    if (xhr.status == 200) {
        let response = JSON.parse(xhr.responseText)
        updateList(response)
        return
    }

    if (xhr.status == 0) {
        displayError("Cannot connect to server")
        return
    }

    if (!xhr.getResponseHeader('content-type') == 'application/json') {
        displayError("Received status=" + xhr.status)
        return
    }

    let response = JSON.parse(xhr.responseText)
    if (response.hasOwnProperty('error')) {
        displayError(response.error)
        return
    }

    displayError(response)
}

function updatePageFollower(xhr) {
    if (xhr.status == 200) {
        let response = JSON.parse(xhr.responseText)
        updateListFollower(response)
        return
    }

    if (xhr.status == 0) {
        displayError("Cannot connect to server")
        return
    }

    if (!xhr.getResponseHeader('content-type') == 'application/json') {
        displayError("Received status=" + xhr.status)
        return
    }

    let response = JSON.parse(xhr.responseText)
    if (response.hasOwnProperty('error')) {
        displayError(response.error)
        return
    }

    displayError(response)
}

function displayError(message) {
    let errorElement = document.getElementById("error")
    errorElement.innerHTML = message
}

function updateList(items) {
    // Removes the old to-do list items
    let list = document.getElementById("my_posts_go_here")
    let posts = items['posts']

    for (let i = 0; i < posts.length; i++) {
        let post = posts[i]
        // Builds a new HTML list item for the posts
        if (document.getElementById("id_post_div_"+post.id) == null) {
            let element = document.createElement("div")
            element.setAttribute("id", "id_post_div_"+post.id)


            let create_time = new Date(Date.parse(post.creation_time,"MM/dd/yyyy hh:mm AM/PM"));

            let post_content =  '<span class="font1" id="id_post_profile_'+post.id+'">' +
                "Post by " +
                '<a href ='+ otherURL(post.user_id) + '>' +post.first_name+" "+post.last_name+ '</a>'  +
                '</span>' +
                '<span id="id_post_text_'+post.id+'" class="font2">' +
                post.text  +
                '</span>' +
                '<span id="id_post_date_time_'+post.id+'" class="font3">' +
                create_time.toLocaleString('en-US', { year:'numeric', month:'numeric', day:'numeric',hour: 'numeric', minute: 'numeric', hour12: true }).replace(","," ") +
                '</span>'

            let button = '<div class="comment">'+'<label>'+"Comment:"+ '</label>'+
                '<input type="text" id="id_comment_input_text_'+post.id+'" name="comment_text">'+
                '<button id="id_comment_button_'+post.id+'" onclick="addComment('+post.id+')">'+"Submit"+'</button>'+
                '<span className="error">'+'</span>'+'</div>'

            let comment_div ='<div id="posts_'+post.id+'_comments_go_here" class="comment">' + '</div>'

            element.innerHTML = post_content + comment_div + button

            // Adds the item to the HTML list
            list.prepend(element)
        }

    }

    let comments = items['comments']

    for (let i = 0; i < comments.length; i++) {
        let comment = comments[i]
        let comment_list = document.getElementById("posts_"+comment.post_id+"_comments_go_here")
        // Builds a new HTML list item for the comments
        if (document.getElementById("id_comment_div_"+comment.id) == null) {
            let element = document.createElement("div")
            element.setAttribute("id", "id_comment_div_"+comment.id)

            let create_time = new Date(comment.creation_time)
            let comment_content =  '<span class="font1" id="id_comment_profile_'+comment.id+'">' +
                "Comment by " +
                '<a href ='+ otherURL(comment.user_id) + '>' +comment.first_name+" "+comment.last_name+ '</a>'  +
                '</span>' +
                '<span id="id_comment_text_'+comment.id+'" class="font2">' +
                comment.comment_text +
                '</span>' +
                '<span id="id_comment_date_time_'+comment.id+'" class="font3">' +
                create_time.toLocaleString('en-US', { year:'numeric', month:'numeric', day:'numeric',hour: 'numeric', minute: 'numeric', hour12: true }).replace(","," ") +
                '</span>'

            element.innerHTML = comment_content

            // Adds the item to the HTML list
            comment_list.appendChild(element)
        }

    }
}

function updateListFollower(items) {
    // Removes the old to-do list items
    let list = document.getElementById("my_posts_go_here")
    let posts = items['posts']

    for (let i = 0; i < posts.length; i++) {
        let post = posts[i]
        // Builds a new HTML list item for the posts
        if (document.getElementById("id_post_div_"+post.id) == null) {
            let element = document.createElement("div")
            element.setAttribute("id", "id_post_div_"+post.id)


            let create_time = new Date(Date.parse(post.creation_time,"MM/dd/yyyy hh:mm AM/PM"));

            let post_content =  '<span class="font1" id="id_post_profile_'+post.id+'">' +
                "Post by " +
                '<a href ='+ otherURL(post.user_id) + '>' +post.first_name+" "+post.last_name+ '</a>'  +
                '</span>' +
                '<span id="id_post_text_'+post.id+'" class="font2">' +
                post.text  +
                '</span>' +
                '<span id="id_post_date_time_'+post.id+'" class="font3">' +
                create_time.toLocaleString('en-US', { year:'numeric', month:'numeric', day:'numeric',hour: 'numeric', minute: 'numeric', hour12: true }).replace(","," ") +
                '</span>'

            let button = '<div class="comment">'+'<label>'+"Comment:"+ '</label>'+
                '<input type="text" id="id_comment_input_text_'+post.id+'" name="comment_text">'+
                '<button id="id_comment_button_'+post.id+'" onclick="addCommentFollower('+post.id+')">'+"Submit"+'</button>'+
                '<span className="error">'+'</span>'+'</div>'

            let comment_div ='<div id="posts_'+post.id+'_comments_go_here" class="comment">' + '</div>'

            element.innerHTML = post_content + comment_div + button

            // Adds the item to the HTML list
            list.prepend(element)
        }

    }

    let comments = items['comments']

    for (let i = 0; i < comments.length; i++) {
        let comment = comments[i]
        let comment_list = document.getElementById("posts_"+comment.post_id+"_comments_go_here")
        // Builds a new HTML list item for the comments
        if (document.getElementById("id_comment_div_"+comment.id) == null) {
            let element = document.createElement("div")
            element.setAttribute("id", "id_comment_div_"+comment.id)

            let create_time = new Date(comment.creation_time)
            let comment_content =  '<span class="font1" id="id_comment_profile_'+comment.id+'">' +
                "Comment by " +
                '<a href ='+ otherURL(comment.user_id) + '>' +comment.first_name+" "+comment.last_name+ '</a>'  +
                '</span>' +
                '<span id="id_comment_text_'+comment.id+'" class="font2">' +
                comment.comment_text +
                '</span>' +
                '<span id="id_comment_date_time_'+comment.id+'" class="font3">' +
                create_time.toLocaleString('en-US', { year:'numeric', month:'numeric', day:'numeric',hour: 'numeric', minute: 'numeric', hour12: true }).replace(","," ") +
                '</span>'

            element.innerHTML = comment_content

            // Adds the item to the HTML list
            comment_list.appendChild(element)
        }

    }
}


function addComment(post_id) {
    let itemTextElement = document.getElementById("id_comment_input_text_"+post_id)
    let itemTextValue   = itemTextElement.value
    // Clear input box and old error message (if any)
    itemTextElement.value = ''
    displayError('')

    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return
        updatePage(xhr)
    }

    xhr.open("POST", addCommentURL, true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send("comment_text="+itemTextValue+"&post_id="+post_id+"&csrfmiddlewaretoken="+getCSRFToken());
}

function addCommentFollower(post_id) {
    let itemTextElement = document.getElementById("id_comment_input_text_"+post_id)
    let itemTextValue   = itemTextElement.value
    // Clear input box and old error message (if any)
    itemTextElement.value = ''
    displayError('')

    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return
        updatePage(xhr)
    }

    xhr.open("POST", addCommentFollowerURL, true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send("comment_text="+itemTextValue+"&post_id="+post_id+"&csrfmiddlewaretoken="+getCSRFToken());
}


function getCSRFToken() {
    let cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
        let c = cookies[i].trim()
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length)
        }
    }
    return "unknown"
}




