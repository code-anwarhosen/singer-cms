document.addEventListener('DOMContentLoaded', function() {
    const avatarInput = document.getElementById('id_avatar');
    const avatarPreview = document.getElementById('avatar-preview');
    const removeBtn = document.getElementById('remove-avatar');
    
    // Handle avatar change
    if (avatarInput) {
        avatarInput.addEventListener('change', function(e) {
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    // Convert div to img if needed
                    if (avatarPreview.tagName === 'DIV') {
                        const newImg = document.createElement('img');
                        newImg.id = 'avatar-preview';
                        newImg.className = 'avatar-preview';
                        newImg.src = e.target.result;
                        avatarPreview.parentNode.replaceChild(newImg, avatarPreview);
                    } else {
                        avatarPreview.src = e.target.result;
                    }
                    
                    // Show remove button if not already visible
                    if (!removeBtn) {
                        const newRemoveBtn = document.createElement('button');
                        newRemoveBtn.id = 'remove-avatar';
                        newRemoveBtn.type = 'button';
                        newRemoveBtn.className = 'avatar-btn';
                        newRemoveBtn.textContent = 'Remove';
                        newRemoveBtn.addEventListener('click', removeAvatar);
                        document.querySelector('.avatar-actions').appendChild(newRemoveBtn);
                    }
                };
                reader.readAsDataURL(this.files[0]);
            }
        });
    }
    
    // Handle remove button
    if (removeBtn) {
        removeBtn.addEventListener('click', removeAvatar);
    }
    
    function removeAvatar() {
        // Clear the file input
        if (avatarInput) {
            avatarInput.value = '';
        }
        
        // Replace img with div if needed
        if (avatarPreview.tagName === 'IMG') {
            const newDiv = document.createElement('div');
            newDiv.id = 'avatar-preview';
            newDiv.className = 'avatar-preview';
            avatarPreview.parentNode.replaceChild(newDiv, avatarPreview);
        }
        
        // Remove the remove button
        const btn = document.getElementById('remove-avatar');
        if (btn) {
            btn.remove();
        }
    }
});
