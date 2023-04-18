async function updateHeaderImageOnServer(imageUrl) {
  const response = await fetch("/users/profile", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      "X-Requested-With": "XMLHttpRequest", // Add this header to indicate it's an AJAX request
    },
    body: new URLSearchParams({ header_image_url: imageUrl }),
  });

  return response.json();
}

function changeHeaderImage(event) {
  const file = event.target;
  const reader = new FileReader();
  reader.onload = async function () {
    const image = document.getElementById("header-image");
    const dataURL = reader.result;
    image.src = dataURL;

    const response = await updateHeaderImageOnServer(dataURL);
    if (response.status !== "success") {
      console.error("Error updating header image on the server");
    }
  };
  reader.readAsDataURL(file.files[0]);
}
