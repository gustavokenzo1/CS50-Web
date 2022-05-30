document.addEventListener("DOMContentLoaded", () => {
  getPosts();

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

function getPosts() {
  fetch("/post")
    .then((response) => response.json())
    .then((data) => {
      data.forEach((post) => {
        const element = document.createElement("div");
        element.innerHTML += `
          <div class="postContainer">
            <div class="postText">
              ${post.text}
            </div>
            <div class="postInfo>
              <div class="postLikes">
                <i id="likeIcon" class="fa fa-solid fa-heart-o" style="margin-right: 5px;"></i> 0
              </div>
              <div class="postUser">
                <strong>Posted by:</strong>
                  <a href="/profile/${post.user.username}">
                    ${post.user.username}
                  </a>
              </div>
              <div class="postTimestamp">
                <small>
                  ${post.timestamp}
                </small>
              </div>
            </div>
          </div>
        `;

        document.querySelector(".latestPosts").append(element);
      });
    })
    .catch((error) => console.log("Error:", error));
}
