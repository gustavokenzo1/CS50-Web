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

  document.querySelectorAll("#editButton").forEach((button) => {
    button.addEventListener("click", () => {
      const id = button.getAttribute("data-id");

      document.querySelectorAll(".postContainer").forEach((post) => {
        if (
          post.getAttribute("id") === id &&
          post.querySelector("button").innerHTML === "Edit"
        ) {
          post.querySelector(".text").style.display = "none";
          post.querySelector(".editForm").style.display = "block";
          post.querySelector("button").innerHTML = "Save";

          post.querySelector("button").onclick = () => {
            const text = post.querySelector(".editForm").value;
            post.querySelector(".text").innerHTML = text;

            fetch(`/edit/${id}`, {
              method: "PATCH",
              body: JSON.stringify({
                message: text,
              }),
            }).catch((error) => console.log("Error: ", error));
          };
        } else {
          post.querySelector(".text").style.display = "block";
          post.querySelector(".editForm").style.display = "none";
          post.querySelector("button").innerHTML = "Edit";
        }
      });
    });
  });
});
