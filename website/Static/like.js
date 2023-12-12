function like(eventId) {
    const likeCount = document.getElementById(`likes-count-${eventId}`);
    const likeButton = document.getElementById(`like-button-${eventId}`);

    fetch(`/like-event/${eventId}`, {method: "POST"})
        .then((res) => res.json())
        .then((data) => {
            likeCount.innerHTML = data["likes"];
            if(data["liked"] === true) {
                likeButton.className = "fa-solid fa-heart";
            } else {
                likeButton.className = "fa-regular fa-heart";
            }
        }).catch((e) => alert("Could not like post."));
}