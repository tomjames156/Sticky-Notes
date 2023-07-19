const colour_theme = document.querySelector('body').classList;

const hideMenu = () => {
    menu.classList.remove('active');
    contentContainer.classList.remove('menu-shown');
}

if(colour_theme == 'light-mode yellow-theme'){
    themeText('black', '#8a7c02', 'white', '#ffffcc')
}else if(colour_theme == 'light-mode green-theme'){
    themeText('black', 'rgba(0, 100, 0, 0.7176470588)', 'white', '#e6f8e2')
}else if(colour_theme == 'light-mode pink-theme'){
    themeText('black', 'rgba(161, 4, 90, 0.662745098)', 'white', '#ffeaf0')
}else if(colour_theme == 'light-mode purple-theme'){
    themeText('black', 'rgba(117, 1, 152, 0.6784313725)', 'white', '#f7ebfe')
}else if(colour_theme == 'light-mode blue-theme'){
    themeText('black', '#00689d', '#f1f1f1', '#dff4ff',)
}else if(colour_theme == 'light-mode gray-theme'){
    themeText('black', '#606060', 'white', '#f1f1f1')
}else if(colour_theme == 'light-mode charcoal-theme'){
    themeText('white', '#8d8d8d', 'white', 'gray', 'white')
}else if(colour_theme == "dark-mode yellow-theme"){
    themeText('white', '#8a7c02', 'white', "#333333", '#777777', '#999999' )
}else if(colour_theme == "dark-mode green-theme"){
    themeText('white', 'rgba(0, 100, 0, 0.7176470588)', 'white', "#333333", '#777777', '#999999' )
}else if(colour_theme == "dark-mode pink-theme"){
    themeText('white', 'rgba(161, 4, 90, 0.662745098)', 'white', "#333333", '#777777', '#999999' )
}else if(colour_theme == "dark-mode purple-theme"){
    themeText('white', 'rgba(117, 1, 152, 0.6784313725)', 'white', "#333333", '#777777', '#999999' )
}else if(colour_theme == "dark-mode blue-theme"){
    themeText('white', '#00689d', '#f1f1f1', "#333333", '#777777', '#999999' )
}else if(colour_theme == "dark-mode gray-theme"){
    themeText('white', '#606060', 'white', "#333333", '#777777', '#999999' )
}else if(colour_theme == "dark-mode charcoal-theme"){
    themeText('white', '#8d8d8d', 'white', "#333333", '#777777', '#999999' )
}

function themeText (text_color='black', highlight, text_color_highlight, scroll_bg, scroll_thumb_bg='gray', scroll_bar="#d3d3d3"){
    let styling = `p, span, li, strong, em, ul, s{ color: ${text_color}; text-align: left;} ul { padding: 0 0 0 1rem; margin: 0; list-style: outside!important; } p::selection, span::selection, li::selection, strong::selection, em::selection, ul::selection, s::selection{ color: ${text_color_highlight}; background: ${highlight};} p::-moz-selection, span::-moz-selection, li::-moz-selection, strong::-moz-selection, em::-moz-selection, ul::-moz-selection, s::-moz-selection { color: ${text_color_highlight}; background: ${highlight};} ::-webkit-scrollbar {
    width: 0.5rem;} ::-webkit-scrollbar-thumb { background-color: ${scroll_bar}; margin-block: 0.2rem; border-radius: 0.25rem;} ::-webkit-scrollbar-thumb:hover { background-color: ${scroll_thumb_bg}; width: 15px;} ::-webkit-scrollbar-track{ background: ${scroll_bg}}`

    return tinymce.init({
        selector: 'textarea#note',
        plugins: 'image lists',
        toolbar: 'bold italic underline strikethrough bullist mybutton',
        toolbar_location: 'bottom',
        menubar: false,
        statusbar: false,
        branding: false,
        content_style: styling,
        content_css: "../../css/notes.css",
        content: 'writer',
        max_height: 350,
        setup: function (editor) {
            editor.on('mousedown', function (e) {
                hideMenu()
                resetMenus()
            });
            editor.on('input', () => {
                modifyText()
                submit()
            })
            editor.on('change', () => {
                modifyText()
                submit()
            })
            editor.on('submit', () => {
                setTimeout(savedText, 2000)
            })
            editor.ui.registry.addButton('mybutton', {
                icon: 'image',
                tooltip: 'Add Image',
                onAction: function() {
                    selectImage()
                }
            });
        },       
    });
}