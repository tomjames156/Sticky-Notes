const menuBtn = document.getElementById('menu-btn');
const menu = document.getElementById('menu');
const mainContent = document.querySelector('div.main-content');
const contentContainer = document.querySelector("div.container");
const body = document.querySelector('body');
const note = document.getElementById('note');
const noteForm = document.querySelector('form#note_form')
const closeBtn = document.getElementById('close_btn');
const themeBtns = document.querySelectorAll(".theme");
const deleteBtn = document.getElementById('delete-note');
const saved = document.querySelector('[data-saved]')
const saving = document.querySelector('[data-saving]')
const submitBtn = document.getElementById('submit');
const noteImagesDivs = document.querySelectorAll('[data-image-parent]');
const imageInput = document.querySelector('#new_image');
const addImageBtn = document.getElementById('add_image')

menuBtn.addEventListener('click', () => {
    menu.classList.add('active');
    contentContainer.classList.add('menu-shown');
});

mainContent.addEventListener('click', () => {
    menu.classList.remove('active')
    contentContainer.classList.remove('menu-shown');
});

note.addEventListener('click', () => {
    menu.classList.remove('active');
    contentContainer.classList.remove('menu-shown');
});

for(let theme of themeBtns){
    theme.addEventListener("click", ()=>{
        body.classList = theme.id;
    })
};

closeBtn.addEventListener('click', () => {
    window.close();
})

deleteBtn.addEventListener('click', () => {
    window.close()
})

const modifyText = () =>  {
    saved.classList.add('hidden')
    saving.classList.remove('hidden')
}

const savedText = () => {
    saved.classList.remove('hidden')
    saving.classList.add('hidden')
}

const submit = () => {
    submitBtn.click()
}

document.addEventListener('mousedown', (e) => {
    if((!e.target.closest('[data-image]') && !e.target.closest('.extra')) || e.button != 2){
        setTimeout(resetMenus, 500)
    }
    if(e.target.matches('[data-image]')){
        console.log('yuhh')
        console.log(e.target)
    }
})

const images = document.querySelectorAll('[data-image]')
const imageMenus = document.querySelectorAll('[data-image-menu]')

const resetMenus = () => {
    for(let menu of imageMenus){
        menu.classList.remove('active')
    }
}

for(let i = 0; i < noteImagesDivs.length; i++){
    noteImagesDivs[i].addEventListener('mousedown', (e) => {
        if(e.button == 2){
            resetMenus()
            console.log(imageMenus[i])
            imageMenus[i].classList.add('active')
        }
    })
}

const selectImage = () => {
    imageInput.click();
}

imageInput.addEventListener('input', (e) => {
    addImageBtn.click();
})