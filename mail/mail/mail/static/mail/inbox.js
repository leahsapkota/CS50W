document.addEventListener('DOMContentLoaded', function () {
  // Attach event listeners for mailbox navigation
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archive').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('#compose-form').onsubmit = send_email;

  // Load the inbox by default
  load_mailbox('inbox');
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-detail-view').style.display = 'none';

  // Clear previous selections
  document.querySelectorAll('button').forEach(button => button.classList.remove("selected"));
  document.querySelector('#compose').classList.add("selected");

  // Clear form fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function send_email(event) {
  event.preventDefault(); // Prevent page reload

  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  fetch('/emails', {
    method: 'POST',
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ recipients, subject, body })
  })
    .then(response => response.json())
    .then(result => {
      if (result.message) {
        load_mailbox('sent');
      } else if (result.error) {
        document.querySelector('#to-text-error-message').innerText = result.error;
      }
    })
    .catch(error => console.log("Error:", error));
}

function load_mailbox(mailbox) {
  // Show mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-detail-view').style.display = 'none';

  // Highlight selected button
  document.querySelectorAll('button').forEach(button => button.classList.remove("selected"));
  document.querySelector(`#${mailbox}`).classList.add("selected");

  // Show mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Fetch emails for the selected mailbox
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      emails.forEach(email => {
        const emailDiv = document.createElement('div');
        emailDiv.classList.add("email-entry", email.read ? "read" : "unread");
        emailDiv.innerHTML = `
          <strong>${email.sender}</strong> - ${email.subject}
          <span class="timestamp">${email.timestamp}</span>
        `;
        emailDiv.addEventListener('click', () => load_email(email.id, mailbox));
        document.querySelector('#emails-view').append(emailDiv);
      });
    })
    .catch(error => console.log("Error fetching emails:", error));
}

function load_email(email_id, mailbox) {
  // Hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-detail-view').style.display = 'block';

  // Fetch email details
  fetch(`/emails/${email_id}`)
    .then(response => response.json())
    .then(email => {
      document.querySelector('#email-detail-view').innerHTML = `
        <h4>${email.subject}</h4>
        <p><strong>From:</strong> ${email.sender}</p>
        <p><strong>To:</strong> ${email.recipients.join(', ')}</p>
        <p><strong>Sent:</strong> ${email.timestamp}</p>
        <hr>
        <p>${email.body}</p>
      `;

      // Add archive/unarchive button if not in "Sent" mailbox
      if (mailbox !== 'sent') {
        const archiveButton = document.createElement('button');
        archiveButton.innerText = email.archived ? "Unarchive" : "Archive";
        archiveButton.addEventListener('click', () => toggle_archive(email_id, !email.archived));
        document.querySelector('#email-detail-view').append(archiveButton);
      }

      // Add reply button
      const replyButton = document.createElement('button');
      replyButton.innerText = "Reply";
      replyButton.addEventListener('click', () => reply_email(email));
      document.querySelector('#email-detail-view').append(replyButton);
    });

  // Mark email as read
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({ read: true })
  });
}

function toggle_archive(email_id, archive_status) {
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({ archived: archive_status })
  }).then(() => load_mailbox('inbox'));
}

function reply_email(email) {
  compose_email();
  document.querySelector('#compose-recipients').value = email.sender;
  document.querySelector('#compose-subject').value = email.subject.startsWith("Re: ") ? email.subject : "Re: " + email.subject;
  document.querySelector('#compose-body').value = `\n\n\n---- On ${email.timestamp} ${email.sender} wrote:\n${email.body}`;
}
