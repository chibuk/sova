// Клик блока, затемняющего страницу при активной боковой панели меню.
document.querySelector('#cover').addEventListener('click', function(event) {
    document.querySelector('#nav-toggle').checked = false;
});

/**
 * Убирает часть пунктов из меню горизонтального в боковую панель,
 * которая открывается по клику по "бургеру" (три горизонтальные полоски)
 * Вид меню: Элемент1 Элемент2 ... ЭлементN Поиск Бургер
 * @param {*} menu_len число пунктов, оставляемых в горизонтальном основном меню, остальные уйдут в боковую панель
 */
function setmenu_panel (menu_len) {
    const nav_ul_element = document.querySelector('nav > ul.menu'); // основное горизонтальное меню
    const panel_ul_element = document.querySelector('nav.nav > ul'); // боковая панель меню
    const li_elements = nav_ul_element.children;
    if (li_elements.length > (menu_len + 2)) {   // Пять элементов меню оставить (в т.ч. поиск и бургер)
        for (let li of [...li_elements].slice(menu_len, -2)) { // Оставить menu_len первых пунктов и два последних (поиск и бургер)
            if (panel_ul_element.firstChild) {
                panel_ul_element.insertBefore(li, panel_ul_element.firstChild);
            } else {
                panel_ul_element.appendChild(li);
            }
        }
    }
};
function setmenu_nav (menu_len) {
    const nav_ul_element = document.querySelector('nav > ul.menu'); // основное горизонтальное меню
    const panel_ul_element = document.querySelector('nav.nav > ul'); // боковая панель меню
    const nav_li_elements = nav_ul_element.children;
    const panel_li_elements = panel_ul_element.children;
    if (nav_li_elements.length < (menu_len + 2)) {
        for (let li of [...panel_li_elements].slice(0, (menu_len + 2 - nav_li_elements.length))) {
            nav_ul_element.insertBefore(li, nav_ul_element.querySelector('#search'));
        }
    }
};
// Длина меню в зависимости от ширины хедера
function _menu_len () {
    const header_width = document.querySelector('header').clientWidth;
    if (header_width <= 360) return 0; // mobile
    if (header_width <= 768) return 1; // xmobile
    if (header_width <= 1024) return 3;// tablet
    return 4;
}

function resizemenu() {
    const l = _menu_len();
    setmenu_panel(l);
    setmenu_nav(l);
}; 
resizemenu(); // отработка первичная

window.addEventListener('resize', resizemenu);
