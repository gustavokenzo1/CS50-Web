document.addEventListener("DOMContentLoaded", () => {
  document.querySelector("#followButton").addEventListener("click", () => {
    fetch(`/profile/${window.location.href.split("/")[4]}`, {
      method: "POST",
    })
      .then(() => {
        window.location.reload();
      })
      .catch((error) => {
        console.log("Error:", error);
      });
  });
});

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("#profileLikeIcon").forEach((icon) => {
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
