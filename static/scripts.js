document.addEventListener("DOMContentLoaded", function() {

    // Get URLs from data attributes
    const prevImageUrl = document.getElementById('prevImage').getAttribute('data-url');
    const nextImageUrl = document.getElementById('nextImage').getAttribute('data-url');

    // Elements for rename functionality
    const renameBtn = document.getElementById("renameBtn");
    const imageName = document.getElementById("imageName");
    const saveName = document.getElementById("saveName");
    const cancelRename = document.getElementById("cancelRename");

    // Rename button click event
    renameBtn.addEventListener("click", function() {
        this.style.display = "none";
        imageName.style.display = "block";
        saveName.style.display = "block";
        cancelRename.style.display = "block";
    });

    // Cancel rename button click event
    cancelRename.addEventListener("click", function() {
        renameBtn.style.display = "block";
        imageName.style.display = "none";
        saveName.style.display = "none";
        this.style.display = "none";
    });

    // Save name button click event
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

    // Keydown event listener for navigation and rename functionality
    document.addEventListener("keydown", function(event) {
        switch (event.keyCode) {
            case 37: // Left arrow key
                window.location.href = prevImageUrl;
                break;
            case 39: // Right arrow key
                window.location.href = nextImageUrl;
                break;
            case 113: // F2 key for Rename
                if (document.activeElement !== imageName) { // Ensure it doesn't trigger when already renaming
                    renameBtn.style.display = "none";
                    imageName.style.display = "block";
                    imageName.value = renameBtn.textContent;
                    saveName.style.display = "block";
                    cancelRename.style.display = "block";
                    imageName.focus();
                }
                break;
            case 13: // 'Enter' key
                if (document.activeElement === imageName) { 
                    saveName.click();
                }
                break;
            case 27: // 'Escape' key
                if (document.activeElement === imageName) {
                    cancelRename.click();
                }
                break;
        }
    });

    // If you have additional code (like the tag functionality) add it below

    // ... [rest of your code]
});
