function makeLike(element){
    const csrfToken = document.cookie.match(/csrftoken=([^ ;]+)/)[1];
    // fetch request
    fetch("/like",{
        method:"PUT",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body:JSON.stringify({
            action:"like",
            postId: element.dataset.post_id,
        })
    })
    .then(response => {
        return response.json()
        })
    .then(data=>{
        const isFilled = element.src.includes('suit-heart-fill.svg');
        console.log(data.amount_of_likes);
        if (isFilled) {
            // change to empty heart
            element.src="static/network/images/suit-heart.svg"
        }
        else {element.src="static/network/images/suit-heart-fill.svg"}
        element.nextElementSibling.innerHTML=data.amount_of_likes;
    })    
    
    
}

function editText(main,form,post_id) {
    // console.log(main);console.log(form);console.log(post_id);
    let newText=form.querySelector("textarea").value;
    // console.log(newText);
    // fetch request
    fetch("edit",{
        method:"PUT",
        body:JSON.stringify({
            post_id:post_id,
            new_body:newText,
        })})
    .then(response => {
        if (!response.ok) {return response.json().then(data=>{throw new Error(`Status code:${response.status}\n${data.error}`);})}
        return response.json()
    })
    .then(data=>{
        console.log(data.message);
        main.style.display="block";
        main.querySelector("p").innerHTML=newText;
        form.style.display="none";
    })
    .catch(error=>{console.log(error.message)})    
    
}

document.querySelectorAll(".like").forEach(like=>{like.onclick=(event)=>{
    makeLike(event.target)}});

document.querySelectorAll(".edit_button").forEach(
    edit_button => {
        edit_button.onclick= (event) =>{
            let main=event.target.parentElement;
            let previous_text=main.querySelector("p").innerHTML;
            // console.log(main);
            let post=main.parentElement;
            // console.log(post);
            let form = document.createElement("form");
            form.innerHTML=`<textarea name="edit" cols="88" rows="5">${previous_text}</textarea></br><button type="submit">Confirm</button>`;
            post.appendChild(form);
            main.style.display="none";
            form.addEventListener("submit",function(event){event.preventDefault();editText(main,form,post.dataset.post_id)});
        }
    }
)

document.querySelector(".edit_profile_img").onclick=function(event){
    event.preventDefault();
    let element=event.target;
    let form=element.previousElementSibling;
    form.style.display="block";
}

document.querySelectorAll(".edit_button_profile").forEach(
    edit_button => {
        edit_button.onclick = (event) => {console.log(event.target)
            let main = event.target.parentElement;
            let previous_text = main.querySelector("p").innerHTML;
            let post = main.parentElement;
            let form = document.createElement("form");
            form.innerHTML = `<textarea name="edit" cols="88" rows="5">${previous_text}</textarea></br><button type="submit">Confirm</button>`;
            post.appendChild(form);
            main.style.display = "none";
            form.addEventListener("submit", function (event) {
                event.preventDefault();
                editTextProfile(main, form, post.dataset.post_id);
            });
        }
    }
);

function editTextProfile(main, form, post_id) {
    let newText = form.querySelector("textarea").value;
    fetch("/edit", {
        method: "PUT",
        body: JSON.stringify({
            post_id: post_id,
            new_body: newText,
        })
    })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(`Status code:${response.status}\n${data.error}`);
                });
            }
            return response.json()
        })
        .then(data => {
            console.log(data.message);
            main.style.display = "block";
            main.querySelector("p").innerHTML = newText;
            form.style.display = "none";
        })
        .catch(error => {
            console.log(error.message)
        })
}

