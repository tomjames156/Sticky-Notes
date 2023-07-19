const closeBtn = document.querySelector('[data-close]');
const describeBtn = document.querySelector('[data-describe]');
const menuBtn = document.querySelector('[data-image-menu-btn]')
const imageMenu = document.querySelector('[data-image-menu]');
const descriptionForm = document.querySelector('[data-description]')
const deleteAction = document.querySelector('[data-delete-action]')
const deleteDialog = document.querySelector('[data-delete-dialog]')

closeBtn.addEventListener('click', () => {
    window.close();
})

describeBtn.addEventListener('click', () => {
    descriptionForm.classList.add('active')
})

menuBtn.addEventListener('click', () => {
    imageMenu.classList.toggle('active');
})

deleteAction.addEventListener('click', () => {
    deleteDialog.classList.add('active')
})

const closeImageMenu = () => {
    imageMenu.classList.remove('active')
}

const resetAllMenus = () => {
    deleteDialog.classList.remove('active')
    imageMenu.classList.remove('active');
    descriptionForm.classList.remove('active')
}

for(let option of imageMenu.children){
    option.addEventListener('click', () => {
        closeImageMenu()
    })
}

document.addEventListener('click', (e) => {
    if(!e.target.closest('[data-image-menu]') && !e.target.matches('[data-image-menu-btn]') && !e.target.closest('.controls') && !e.target.closest('[data-description]')){
        resetAllMenus()
    }
    // add another to stop other dialogs from closing
})

// make menuBtn toggle the active class
// add the previous and next to context
// make delete view