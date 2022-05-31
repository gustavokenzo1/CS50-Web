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
