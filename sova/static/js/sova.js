// Клик блока, затемняющего страницу при активной боковой панели меню.
document.querySelector('#cover').addEventListener('click', function(event) {
    document.querySelector('#nav-toggle').checked = false;
});

/**
 * Перемещение пунктов оризонтального меню в меню вертикальной панели и иобратно в завиисмомти от ширины
 */
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
    /**
     * Приводим в соответствие высоту видимой области для мобильных устройств,
     * т.к. есть проблемы с height: 100vh;
     */
    function adjustViewportHeight() {
        document.documentElement.style.setProperty('--viewport-height', `${window.innerHeight}px`);
        document.documentElement.style.setProperty('--viewport-width', `${window.innerWidth}px`); // для других целей (для галереи)
    }
    const l = _menu_len();
    setmenu_panel(l);
    setmenu_nav(l);
    adjustViewportHeight();
};
modify_menu(); // отработать при загрузке
window.addEventListener('resize', modify_menu);
window.addEventListener('orientationchange', modify_menu);


// Gallery module
document.querySelectorAll('.gallery__photo').forEach(element => {
    element.addEventListener('click', (event) => {
        const element = event.currentTarget;
        setTimeout(function(element) {
            element.scrollIntoView(
                {behavior: "smooth", block: "nearest", inline: "center"}
            );
        }, 500, element);

    });
});
