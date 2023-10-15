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
        }).then(response => {
            if (response.ok) {
                renameBtn.textContent = newName;
                cancelRename.click();
            } else {
                console.error("Error renaming image.");
            }
        });
        
    });

    // Keydown event listener for navigation and rename functionality
    document.addEventListener("keydown", function(event) {
        switch (event.keyCode) {
            case 37: // Left arrow key
                if (document.activeElement !== imageName) { 
                    window.location.href = prevImageUrl;
                }
                break;
            case 39: // Right arrow key
                if (document.activeElement !== imageName) {
                    window.location.href = nextImageUrl;
                }
                break;
            case 113: // F2 key for Rename
                if (document.activeElement !== imageName) { 
                    renameBtn.style.display = "none";
                    imageName.style.display = "block";
                    imageName.value = renameBtn.textContent;
                    saveName.style.display = "block";
                    cancelRename.style.display = "block";
                    imageName.focus();
                }
                break;
                case 13: // 'Enter' key
                event.preventDefault(); // Prevent any default action
                const debouncedSave = debounce(() => {
                    if (document.activeElement === imageName) {
                        saveName.click();
                    } else {
                        renameBtn.style.display = "none";
                        imageName.style.display = "block";
                        imageName.value = renameBtn.textContent;
                        saveName.style.display = "block";
                        cancelRename.style.display = "block";
                        imageName.focus();
                    }
                }, 300);  // 300 milliseconds debounce time
                debouncedSave();
                break;            
            case 27: // 'Escape' key
                if (document.activeElement === imageName) {
                    cancelRename.click();
                }
                break;
        }
    });

    // If you have additional code (like the tag functionality) add it below
    function debounce(func, wait) {
        let timeout;
        return function(...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }
    
    // ... [rest of your code]
});
