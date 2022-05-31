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
        } else if (
          post.getAttribute("id") === id &&
          post.querySelector("button").innerHTML === "Save"
        ) {
          post.querySelector(".text").style.display = "block";
          post.querySelector(".editForm").style.display = "none";
          post.querySelector("button").innerHTML = "Edit";
        }
      });
    });
  });

  document.querySelectorAll("#likeIcon").forEach((icon) => {
    fetch(`/like/${icon.getAttribute("data-id")}`, {
      method: "GET",
    }).then((response) => {
      response.json().then((data) => {
        if (data.message === "liked") {
          icon.classList.remove("fa-heart-o");
          icon.classList.add("fa-heart");
          icon.style.color = "red";
        }
      });
    });

    icon.addEventListener("click", () => {
      const id = icon.getAttribute("data-id");

      fetch(`/like/${id}`, {
        method: "POST",
      }).catch((error) => console.log("Error: ", error));

      if (icon.classList.contains("fa-heart-o")) {
        icon.classList.remove("fa-heart-o");
        icon.classList.add("fa-heart");
        icon.style.color = "red";

        document.querySelectorAll("#likes").forEach((like) => {
          if (like.getAttribute("data-id") === id) {
            like.innerHTML = parseInt(like.innerHTML) + 1;
          }
        });
      } else {
        icon.classList.remove("fa-heart");
        icon.classList.add("fa-heart-o");
        icon.style.color = "black";

        document.querySelectorAll("#likes").forEach((like) => {
          if (like.getAttribute("data-id") === id) {
            like.innerHTML = parseInt(like.innerHTML) - 1;
          }
        });
      }
    });
  });
});
