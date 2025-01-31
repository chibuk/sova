// Клик блока, затемняющего страницу при активной боковой панели меню.
document.querySelector('#cover').addEventListener('click', function(event) {
    document.querySelector('#nav-toggle').checked = false;
});

function modify_menu() {
    /**
     * Перемещает часть пунктов из меню горизонтального в боковую панель,
     * которая открывается по клику по "бургеру" (три горизонтальные полоски)
     * Вид меню: Элемент1 Элемент2 ... ЭлементN Поиск Бургер
     * @param {int} menu_len число пунктов, оставляемых в горизонтальном основном меню, остальные уйдут в боковую панель
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
    /**
     * Перемещает часть пунктов из боковой панели в меню горизонтальное.
     * @param {int} menu_len число пунктов, оставляемых в горизонтальном основном меню,
     * если там меньше, то добираем, перемещая из боковой панели
     */
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
        if (header_width <= 375) return 1; // xmobile
        if (header_width <= 512) return 2; // xLmobile
        if (header_width <= 768) return 3; // xxLmobile
        if (header_width <= 1024) return 4;// tablet и брокк широкие экраны
        return 5;
    }
    const l = _menu_len();
    setmenu_panel(l);
    setmenu_nav(l);
}; 
modify_menu(); // отработать при загрузке

window.addEventListener('resize', modify_menu);

