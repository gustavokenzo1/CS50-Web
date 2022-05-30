document.addEventListener("DOMContentLoaded", () => {
  // Create post
  document.querySelector("#submit-form").onsubmit = () => {
    const text = document.querySelector("#submit-post-text").value;

    fetch("/post", {
      method: "POST",
      body: JSON.stringify({
        message: text,
      }),
    })
      .then(() => {
        window.location.reload();
      })
      .catch((error) => console.log("Error: ", error));
  };
});
