document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views
  document
    .querySelector("#inbox")
    .addEventListener("click", () => load_mailbox("inbox"));
  document
    .querySelector("#sent")
    .addEventListener("click", () => load_mailbox("sent"));
  document
    .querySelector("#archived")
    .addEventListener("click", () => load_mailbox("archive"));
  document.querySelector("#compose").addEventListener("click", compose_email);

  // By default, load the inbox
  load_mailbox("inbox");
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#email-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";

  // Clear out composition fields
  document.querySelector("#compose-recipients").value = "";
  document.querySelector("#compose-subject").value = "";
  document.querySelector("#compose-body").value = "";

  document.querySelector("#compose-form").onsubmit = (event) => {
    event.preventDefault();

    const recipients = document.querySelector("#compose-recipients").value;
    const subject = document.querySelector("#compose-subject").value;
    const body = document.querySelector("#compose-body").value;

    fetch("/emails", {
      method: "POST",
      body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body,
      }),
    })
      .then(() => {
        load_mailbox("sent");
      })
      .catch((error) => console.error("Error:", error));
  };
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector("#emails-view").style.display = "block";
  document.querySelector("#email-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "none";

  // Show the mailbox name
  document.querySelector("#emails-view").innerHTML = `<h3>${
    mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
  }</h3>`;

  if (mailbox === "inbox" || mailbox === "sent" || mailbox === "archive") {
    fetch(`emails/${mailbox}`)
      .then((response) => response.json())
      .then((data) =>
        data.forEach((email) => {
          const element = document.createElement("div");

          element.innerHTML += `
            <div value=${email.id} class="email">
              <div class="email-sender">
                <strong>
                  ${email.sender}
                </strong>
              </div>
              <div class="email-subject">
                <strong>
                  ${email.subject}
                </strong>
              </div>
              <div class="email-timestamp">
                <strong>            
                  ${email.timestamp}
                </strong>  
              </div>
            </div>
          `;

          element.addEventListener("click", () => load_mail(email.id));

          if (email.read) element.style.backgroundColor = "#eee";
          else element.style.backgroundColor = "#fff";

          document.querySelector("#emails-view").append(element);

          if (mailbox === "inbox" || mailbox === "archive") {
            const archiveButton = document.createElement("div");

            if (!email.archived) {
              archiveButton.innerHTML += `
                <div class="email-archive">
                  <button class="btn btn-sm btn-outline-primary archiveButton">Archive</button>
                </div>
              `;
            } else {
              archiveButton.innerHTML += `
                <div class="email-archive">
                  <button class="btn btn-sm btn-outline-primary archiveButton">Unarchive</button>
                </div>
              `;
            }

            archiveButton.addEventListener("click", () => {
              fetch(`emails/${email.id}`, {
                method: "PUT",
                body: JSON.stringify({
                  archived: !email.archived,
                }),
              }).catch((error) => console.error("Error:", error));
              window.location.reload();
            });

            document.querySelector("#emails-view").append(archiveButton);
          }
        })
      )
      .catch((error) => console.error("Error:", error));
  }
}

function load_mail(id) {
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#email-view").style.display = "block";
  document.querySelector("#compose-view").style.display = "none";

  fetch(`emails/${id}`, {
    method: "PUT",
    body: JSON.stringify({
      read: true,
    }),
  }).catch((error) => console.error("Error:", error));

  document.querySelector("#email-view").innerHTML = "";

  fetch(`/emails/${id}`)
    .then((response) => response.json())
    .then((email) => {
      const element = document.createElement("div");
      element.innerHTML += `
        <div class="insideEmail">
          <div class="email-header">
            <div class="email-sender">
              <strong>
                Sender:
              </strong>
              ${email.sender}
            </div>
            <div class="email-recipients">
              <strong>
                Recipients:
              </strong>
              ${email.recipients}
            </div>
            <div class="email-subject">
              <strong>
                Subject:
              </strong>
              ${email.subject}
            </div>
            <div class="email-timestamp">
              <strong>
                Date:
              </strong>
              ${email.timestamp}
            </div>
          </div>
          <div class="email-body">
            ${email.body}
          </div>      
          <div class="email-reply">
            <button class="btn btn-sm btn-outline-primary mt-4">Reply</button>
          </div>        
        </div>
      `;
      element.querySelector(".email-reply").addEventListener("click", () => {
        reply_email(email.sender, email.subject, email.body, email.timestamp);
      });
      document.querySelector("#email-view").append(element);
    })
    .catch((error) => console.error("Error:", error));
}

function reply_email(sender, subject, body, timestamp) {
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#email-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";

  document.querySelector("#compose-recipients").value = sender;
  document.querySelector("#compose-subject").value = `${
    subject.startsWith("Re: ") ? subject : "Re: " + subject
  }`;
  document.querySelector(
    "#compose-body"
  ).value = `On ${timestamp} ${sender} wrote:

  ${body}`;

  document.querySelector("#compose-form").onsubmit = (event) => {
    event.preventDefault();

    const recipients = document.querySelector("#compose-recipients").value;
    const subject = document.querySelector("#compose-subject").value;
    const body = document.querySelector("#compose-body").value;

    fetch("/emails", {
      method: "POST",
      body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: `${body}`,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        load_mailbox("sent");
      })
      .catch((error) => console.error("Error:", error));
  };
}
