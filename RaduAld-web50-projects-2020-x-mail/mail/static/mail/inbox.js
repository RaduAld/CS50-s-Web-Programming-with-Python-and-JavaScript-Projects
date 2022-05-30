document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views9
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  const email_btn = document.querySelector('#send_email');
  email_btn.addEventListener('click', function() {
    recipients_v = document.querySelector('#compose-recipients').value
    subject_v = document.querySelector('#compose-subject').value
    body_v = document.querySelector('#compose-body').value
    if (recipients_v == null || recipients_v == "", 
        subject_v == null || subject_v == "",
        body_v == null || body_v == "") {
        alert("Please fill in all inputs of the form!");
        document.querySelector('#compose-recipients').value = recipients_v;
        document.querySelector('#compose-subject').value = subject_v;
        document.querySelector('#compose-body').value = body_v;
    } else {
      fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
            recipients: recipients_v,
            subject: subject_v,
            body: body_v,
        })
      })
      .then(response => response.json())
      .then(result => {
          // Print result
          console.log(result);
          load_mailbox('sent')
      });
    }
  })
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#email-view').innerHTML = ``;

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-recipients').disabled = false
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-subject').disabled = false
  document.querySelector('#compose-body').value = '';

  document.querySelector('#compose-title').innerHTML = 'New Email';
  document.querySelector('#compose-title').style.paddingTop = '0px';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#email-view').innerHTML = ``;

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  //Display emails
  fetch('/emails/' + mailbox)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);

      // Show email list
      for (i=0; i < emails.length; i++){
        let preview =  document.createElement('div');
        if (!emails[i].read){ 
          preview.innerHTML = `<div id=${i} class="card email-preview">
            <div class="card-header top-preview">
              ${emails[i].subject}
              <div class="date"> ${emails[i].timestamp} </div>
            </div>
            <div class="card-body" style="background-color: white; color: #A9CBB7">
              <blockquote class="blockquote mb-0">
                <p>${emails[i].body}</p>
                <footer class="blockquote-footer" style="color: #A9CBB7">From ${emails[i].sender} To ${emails[i].recipients}</footer>
              </blockquote>
            </div>
          </div>`;
        } else {
          preview.innerHTML = `<div id=${i} class="card email-preview">
              <div class="card-header top-preview">
                ${emails[i].subject}
                <div class="date"> ${emails[i].timestamp} </div>
              </div>
              <div class="card-body" style="background-color: gray; color: #A9CBB7;">
                <blockquote class="blockquote mb-0 preview">
                  <p>${emails[i].body}</p>
                  <footer class="blockquote-footer" style="color: #A9CBB7">From ${emails[i].sender} To ${emails[i].recipients}</footer>
                </blockquote>
              </div>
            </div>`;
        }
        let id = emails[i].id
        preview.addEventListener('click', () => load_email(id));
        preview.style.cursor = "pointer"
        document.querySelector('#emails-view').append(preview);
      }
  });
}

function load_email(email_id) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#email-view').innerHTML = ``;

  fetch('/emails/' + email_id)
  .then(response => response.json())
  .then(email => {
      // Print email
      console.log(email);

      if (email.read == false){
        fetch('/emails/' + email_id, {
          method: 'PUT',
          body: JSON.stringify({
              read: true
          })
        })
      }
      document.querySelector('#email-view').innerHTML = `
        <div class="card-header top-preview">
          ${email.subject}
          <div class="date"> ${email.timestamp} </div>
        </div>
        <div id="bdy" class="card-body">
          <blockquote class="blockquote mb-0 preview">
            <h5>From: ${email.sender}</h5>
            <h5>To: ${email.recipients}</h5>
          </blockquote>
          <div class="line-breaker">${email.body}</div>
        </div>`;

      var x = email.recipients.includes(document.querySelector('#user_email').value)
      if (x) {
        const but = document.createElement('button')
        but.classList.add('btn', 'email-btn')
        if (email.archived){
          but.innerHTML = 'Unarchive'
        } else {
          but.innerHTML = 'Archive'
        }
        but.addEventListener('click', function () {
          if (email.archived){
            fetch('/emails/' + email.id, {
              method: 'PUT',
              body: JSON.stringify({
                  archived: false
              })
            })
            console.log('Unarchived!')
            location.reload()
          } else {
            fetch('/emails/' + email.id, {
              method: 'PUT',
              body: JSON.stringify({
                  archived: true
              })
            })
            console.log('Archived!')
            location.reload()
          }
        })
        document.querySelector('#bdy').append(but)
        const reply = document.createElement('button');
        reply.innerHTML = 'Reply'
        reply.classList.add('btn', 'email-btn')
        reply.addEventListener('click', function() {
          document.querySelector('#compose-view').style.display = 'block';
          document.querySelector('#compose-title').innerHTML = 'Reply Email';
          document.querySelector('#compose-title').style.paddingTop = '10px';
          document.querySelector('#compose-recipients').value = email.sender;
          document.querySelector('#compose-recipients').disabled = true;
          const n = email.subject
          const m = n.startsWith("Re: ")
          if (m === false){
            document.querySelector('#compose-subject').value = 'Re: ' + email.subject;
          } else {
            document.querySelector('#compose-subject').value = email.subject;
          }
          document.querySelector('#compose-subject').disabled = true;
          document.querySelector('#compose-body').value = 'On ' + email.timestamp + ' ' + email.sender + ' wrote:\n' + email.body + '\n \n';
          window.scrollTo({
            right: 0, 
            top: window.innerHeight,
            behavior: 'smooth'
          })
        })
        document.querySelector('#bdy').append(reply)
      }
  });
}

