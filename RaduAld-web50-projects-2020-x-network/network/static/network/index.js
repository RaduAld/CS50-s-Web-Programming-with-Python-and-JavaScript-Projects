document.addEventListener('DOMContentLoaded', function() {

    check_posts = document.querySelector("#posts")
    if (check_posts.length === 0){
      check_posts.innerHTML = 'There are no posts on this page.'
    }

    const form = document.querySelector('#new-post-form');
    var height = form.clientHeight;
    form.style.visibility = 'hidden';
    form.style.opacity = '0';
    form.style.height = '0';
    form.style.width = '0';
    form.style.padding = '0';

    document.querySelector('#new_post_btn').onclick = () => {
        document.querySelector('#form-header').innerHTML = 'Create Post'
        if(form.style.visibility == 'hidden'){
            form.style.visibility = 'visible';
            form.style.opacity = '1';
            form.style.height = height + 'px';
            form.style.width = '100%';
            form.style.padding = '20px';
          }
          else{
            form.style.visibility = 'hidden';
            form.style.opacity = '0';
            form.style.height = '0';
            form.style.width = '0';
            form.style.padding = '0';
          }
    };

    document.querySelector('#post-btn').addEventListener('click', function() {
      body_v = document.querySelector('#texta-new').value;
      if (body_v == null || body_v == ""){
        alert('To create a post please enter a body.')
      } else {
        fetch('/posts', {
          method: 'POST',
          body: JSON.stringify({
              body: body_v,
          })
        })
        .then(response => response.json())
        .then(result => {
            // Print result
            console.log(result);
            location.reload();
        });
      }
    });

    const help = document.querySelector("#help").innerHTML
    if (help == 2){
      profile_page()
    }
});

function like(post_id, lk){
  fetch('/posts/' + post_id, {
    method: 'PUT',
    body: JSON.stringify({
        var: lk,
    })
  })
  .then(
    $('#card' + post_id).load(' #card' + post_id)
  )
}

function edit(post_id){
  body = document.querySelector("#body" + post_id);
  texta = document.querySelector("#edit-texta" + post_id);
  texta.value = body.innerHTML;
  body.style.display = "none";
  texta.style.display = "block";
  texta.style.width = "100%";
  const save = document.createElement('button');
  save.innerHTML = "Save"
  save.classList.add('btn', 'btn-primary');
  save.addEventListener('click', function() {
    body_v = texta.value;
    if (body_v == null || body_v == ""){
      alert('To create a post please enter a body.')
    } else {
      fetch('/posts/' + post_id, {
        method: 'PUT',
        body: JSON.stringify({
            var: 'edit',
            text: body_v
        })
      })
      .then(
        $('#card' + post_id).load(' #card' + post_id)
      )
    }
  })
  document.querySelector('#buttons' + post_id).append(save);
  document.querySelector('#edit' + post_id).style.display = "none";
}

function profile_page(){
  usrnm = document.querySelector('#header').innerHTML;
  fetch('/user/' + usrnm)
  .then(response => response.json())
  .then(user => {
      const logged_username = document.querySelector('#logged').innerHTML;
      const old_fllw = document.querySelector('#fllw-btn');
      const fllw = old_fllw.cloneNode(true);
      old_fllw.parentNode.replaceChild(fllw, old_fllw);
      fetch('/user/' + logged_username)
      .then(response => response.json())
      .then(logged => {
        if (logged.username === user.username){
          fllw.style.display = "none";
        } else {
        if (user.followers.includes(logged.username)){
          fllw.innerHTML = 'Unfollow';
          fllw.addEventListener('click', function() {
            fetch('/profile/' + user.username, {
              method: 'PUT',
              body: JSON.stringify({
                  follow: false
              })
            })
            .then(response => response.json())
            .then(json => console.log(json))
            location.reload()
          })
        } else {
          fllw.innerHTML = 'Follow';
          fllw.addEventListener('click', function() {
            fetch('/profile/' + user.username, {
              method: 'PUT',
              body: JSON.stringify({
                  follow: true
              })
            })
            .then(response => response.json())
            .then(json => console.log(json))
            location.reload()
          })
        }
      }
    });
  });
}

{/*  */}