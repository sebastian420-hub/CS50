document.addEventListener('DOMContentLoaded', function() {

  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', function(event) {
    event.preventDefault();
    send_email();
    load_mailbox('sent');
  });

  load_mailbox('inbox');
  
  

  function view_sent() {

    document.querySelector('#email-view').style.display = 'none';
  
    fetch('/emails/sent')
    .then(response => response.json())
    .then(emails => {
      const element = document.createElement('div');
      element.id = 'sent-emails';
     
      emails.forEach(email => {
        console.log(email);
        const item = document.createElement('div');
        item.class = 'container';
        item_id = `${email.id}`;

        item.innerHTML = `
        <button class="button-class" id="${item_id}">
        <span>${email.recipients}</span> 
        <span>${email.subject}</li></span> 
        <span>${email.timestamp}</li></span>
        </button>`;
        element.append(item);
        document.querySelector('#emails-view').append(element);
        console.log( document.getElementById(item_id));
        
        
      });
      
      
      emails.forEach(email => {
        document.getElementById(email.id).addEventListener('click', () => view_email(email.id));
      });


     
    });
    
  }

  

  function view_inbox() {

    document.querySelector('#email-view').style.display = 'none';
    fetch('/emails/inbox')
    .then(response => response.json())
    .then(emails => {
      console.log(emails)
      
      emails.forEach(email => {
        const element = document.createElement('div');
        element.id = `email-${email.id}`;
        console.log(element);
        const item = document.createElement('div');
        item.id = `${email.id}`;
        item.className = 'email-item';
        item.innerHTML = `
        <button class="button-class">
        <span>${email.sender}</span>
        <span>${email.subject}</span> 
        <span>${email.timestamp}</span>
        </button>`;
        element.append(item);
        document.querySelector('#emails-view').append(element);
      });

      emails.forEach(email => {
        document.getElementById(email.id).addEventListener('click', () => view_email(email.id));
        const archiveButton = document.createElement('button');
        archiveButton.id = `archive-${email.id}`;
        archiveButton.className = 'email-item';
        archiveButton.innerHTML = 'Archive';
        const box = document.getElementById(`email-${email.id}`);
        box.append(archiveButton);
        archiveButton.addEventListener('click', () => archive_email(email.id));

      });
    });
  }


  function view_archive() {
    document.querySelector('#email-view').style.display = 'none';
    fetch('/emails/archive')
    .then(response => response.json())
    .then(emails => {
      emails.forEach(email => {
        const element = document.createElement('div');
        element.id = `email-${email.id}`;
        const item = document.createElement('div');
        item.id = `${email.id}`;
        item.className = 'email-item';
        item.innerHTML = `
        <button class="button-class">
        <span>${email.sender}</span>
        <span>${email.subject}</span>
        <span>${email.timestamp}</span>
        </button>`;
        element.append(item);
        document.querySelector('#emails-view').append(element);
      })

      emails.forEach(email => {
        document.getElementById(email.id).addEventListener('click', () => view_email(email.id));
        const archiveButton = document.createElement('button');
        archiveButton.id = `unarchive-${email.id}`;
        archiveButton.className = 'email-item';
        archiveButton.innerHTML = 'Unarchive';
        const box = document.getElementById(`email-${email.id}`);
        box.append(archiveButton);
        archiveButton.addEventListener('click', () => unarchive_email(email.id));
      });
    })
  }


  function archive_email(emailId) {
    fetch(`/emails/${emailId}`, {
      method: 'PUT',
      body: JSON.stringify({
        archived: true
      })
    })
    .then(() => {
      load_mailbox('inbox');

    });
  }


  function unarchive_email(emailId) {
    fetch(`/emails/${emailId}`, {
      method: 'PUT',
      body: JSON.stringify({
        archived: false
      })
    })
    .then(() => {
      load_mailbox('inbox');
    });

  
  }

  function view_email(emailId) {

    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'block';
    fetch(`/emails/${emailId}`)
      .then(response => response.json())
      .then(email => {
        document.querySelector('#email-view').innerHTML = '';
        const emailView = document.createElement('div');
        emailView.innerHTML = `
          <h3>${email.subject}</h3>
          <p>From: ${email.sender}</p>
          <p>To: ${email.recipients}</p>
          <p>Timestamp: ${email.timestamp}</p>
          <div>${email.body}</div>
          <button class="btn btn-sm btn-outline-primary" id="reply">Reply</button>
        `;
        document.querySelector('#email-view').append(emailView);

        document.querySelector('#reply').addEventListener('click', () => reply_email(emailId));
      });
  }



  function send_email() {
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  
    if (recipients && subject && body) {
      fetch('/emails', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body
        })
      })
      .then(response => response.json())
      .then(result => {
        console.log(result);
        document.querySelector('#compose-form').reset();
      });
    } else {
      alert('Please fill all the fields');
    }}


    function reply_email(emailId) {
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#email-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'block';

      fetch(`/emails/${emailId}`)
      .then(response => {
        if(!response.ok) {
          throw new Error('Error: Network response was not ok');
        } else {
          return response.json();
        }
      })
      .then(email => {
        compose_email();
        let subject = email.subject.startsWith('Re:') ? email.subject : `Re: ${email.subject}`;
        let body = email.body.startsWith(`
        On ${email.timestamp} ${email.sender} wrote: ${email.body}
        Reply to: ${email.sender}`) ? email.body : `
        On ${email.timestamp} ${email.sender} wrote: ${email.body}
        Reply to: ${email.sender}`;
        document.getElementById('compose-recipients').value = email.sender;
        document.querySelector('#compose-recipients').disabled = true;
        document.querySelector('#compose-subject').value = subject;
        document.querySelector('#compose-body').value = body;

      }).catch(error => {
        console.log(error);
      });
    }



    function compose_email() {
      document.querySelector('#email-view').style.display = 'none';
      document.querySelector('#compose-recipients').disabled = false;

      // Show compose view and hide other views
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'block';
    
      // Clear out composition fields
      document.querySelector('#compose-recipients').value = '';
      document.querySelector('#compose-subject').value = '';
      document.querySelector('#compose-body').value = '';
    }
    
    
    
    
    
    
    function load_mailbox(mailbox) {
      
      // Show the mailbox and hide other views
      document.querySelector('#emails-view').style.display = 'block';
      document.querySelector('#compose-view').style.display = 'none';
    
      // Show the mailbox name
      document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
      if (mailbox === "sent") {
        view_sent();
        
      }
      else if (mailbox === "inbox") {
        view_inbox();
        document.querySelector('#email-view').style.display = 'none';
      }
      else {
        view_archive();
      }
    }
    
    
    
    


    
 
 

  
});






