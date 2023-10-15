document.addEventListener("DOMContentLoaded", function() {

    // Get URLs from data attributes
    const prevImageUrl = document.getElementById('prevImage').getAttribute('data-url');
    const nextImageUrl = document.getElementById('nextImage').getAttribute('data-url');

    // Keydown listener for navigation
    document.addEventListener("keydown", function(event) {
        switch (event.keyCode) {
            case 37: // Left arrow key
                window.location.href = prevImageUrl;
                break;
            case 39: // Right arrow key
                window.location.href = nextImageUrl;
                break;
        }
    });

    // Rename functionality
    const renameBtn = document.getElementById("renameBtn");
    const imageName = document.getElementById("imageName");
    const saveName = document.getElementById("saveName");
    const cancelRename = document.getElementById("cancelRename");

    renameBtn.addEventListener("click", function() {
        this.style.display = "none";
        imageName.style.display = "block";
        saveName.style.display = "block";
        cancelRename.style.display = "block";
    });

    cancelRename.addEventListener("click", function() {
        renameBtn.style.display = "block";
        imageName.style.display = "none";
        saveName.style.display = "none";
        this.style.display = "none";
    });

    saveName.addEventListener("click", function() {
        let newName = imageName.value;
        fetch("/rename_image", {
            method: "POST",
            body: new URLSearchParams({
                "new_name": newName,
                "old_name": renameBtn.textContent
            }),
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            }
        }).then(response => window.location.reload());
    });

    // If you have additional code (like the tag functionality) add it below

    // ... [rest of your code]

});
