// sidebar
sidebar = document.querySelector('.sidebar')
sidebarBtn = document.querySelector('.sidebar-btn')
console.log(sidebar)
console.log(sidebarBtn)
content = '<'

sidebarBtn.addEventListener('click', sidebarToggleActive)

function sidebarToggleActive() {
    sidebar.classList.toggle('active')
    c = sidebarBtn.innerHTML
    sidebarBtn.innerHTML = content
    content = c
}

// sidebar link 
sidebarLinkList = document.querySelectorAll('.cat-menu_item')
sidebarLinkList.forEach(item => {
    item.addEventListener('click', () => {
        sidebar.classList.remove('active')
    })
})

// header_menu 
burger = document.querySelector('.burger')
closeHeaderMenu = document.querySelector('.close-header-menu')
headerMenu = document.querySelector('.header_menu')
burger.addEventListener('click', () => {
    headerMenu.classList.add('active')
})
closeHeaderMenu.addEventListener('click', () => {
    headerMenu.classList.remove('active')
})
