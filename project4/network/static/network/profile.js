document.addEventListener("DOMContentLoaded", () => {
  document.querySelector("#followButton").addEventListener("click", () => {
    fetch(`/profile/${window.location.href.split("/")[4]}`, {
      method: "POST",
    })
      .then(() => {
        /* if (document.querySelector("#followButton").innerHTML === "Follow") {
          document.querySelector("#followButton").innerHTML = "Unfollow";
          document.querySelector("#followers").innerHTML =
            parseInt(document.querySelector("#followers").innerHTML) + 1;
        } else {
          document.querySelector("#followButton").innerHTML = "Follow";
          document.querySelector("#followers").innerHTML =
            parseInt(document.querySelector("#followers").innerHTML) - 1;
        } */
        window.location.reload();
      })
      .catch((error) => {
        console.log("Error:", error);
      });
  });
});
