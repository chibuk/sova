/**
 * Перемещение пунктов горизонтального меню в меню 
 * вертикальной панели и иобратно в завиисмомти от ширины
 * Данное меню выплывает при клике на "бургер"
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
// Клик блока, затемняющего страницу при активной боковой панели меню
document.querySelector('.cover').addEventListener('click', function(event) {
    document.querySelector('#nav-toggle').checked = false;
});


/**
 * Gallery module
 * Галерея в виде ряда миниатюр фотографий, которые при клике переходят в режим просмотра,
 * это затемненный экран и фото в центре в полном размере. Можно листать стрелочками-кнопками,
 * стрелками на клавиатуре, свайпами, выход по ESC или кликом в любом месте экрана.
 */
function galleryModule() {
    document.querySelectorAll('.gallery__photo').forEach(element => {
        element.addEventListener('click', (event) => {
            const element = event.currentTarget;
            setTimeout(function(element) {
                element.scrollIntoView( // В режиме просмотра двигаем элемент в центр экрана
                    {behavior: "smooth", block: "nearest", inline: "center"}
                );
            }, 500, element);
        });
    });
    document.getElementById('gallery-toggle').addEventListener('change', function() {
        function EscapeHandler(event) { // Выход из раежима просмотра по ESC
            const checkbox = document.getElementById('gallery-toggle');
            if(event.key === 'Escape') {
                checkbox.checked = false;   // выходим, отработало и
                document.removeEventListener('keydown', EscapeHandler); // сразу убираем обработчик
            }
        };
        if (this.checked) {
            document.addEventListener('keydown', EscapeHandler);
        }
    });
    document.getElementById('gallery__control_backward').addEventListener('click', function(){
        const position = document.querySelector(".gallery__photos").scrollLeft;
        const current = Math.round(position / window.innerWidth);
        photos = document.querySelectorAll('.gallery__photo');
        photos[(current - 1 + photos.length) % photos.length].scrollIntoView(
            {behavior: "smooth", block: "nearest", inline: "center"}
        );
    })
    document.getElementById('gallery__control_forward').addEventListener('click', function(){
        const position = document.querySelector(".gallery__photos").scrollLeft;
        const current = Math.round(position / window.innerWidth);
        photos = document.querySelectorAll('.gallery__photo');
        photos[(current + 1) % photos.length].scrollIntoView(
            {behavior: "smooth", block: "nearest", inline: "center"}
        );
    });
}; 
if (document.querySelectorAll('.gallery__photos').length > 0) galleryModule();


/**
 * Модуль поиска
 */
function searchActivate () {
    const searchElment = document.querySelector('.search'); //блок появится поверх символа поиска
    const cover = document.querySelector('.cover'); //затемнение остальной части страницы (кроме гориз.меню)
    const output = searchElment.querySelector('.search__output');
    // флаг того, чо поиск был уже произведён для исключения дублирующих запросов
    let done = false; // false | "query"
    document.querySelector('#search-button').addEventListener('click', () => {
        searchElment.style.display = 'block';
        done = false;
        const interval = setTimeout(()=>{
            searchElment.classList.add('search__active');
            document.getElementById('SearchInput').focus();
            cover.classList.add('cover_on');
            cover.addEventListener('click', searchOff)
        }, 500);
    });
    function searchOff () {
        searchElment.classList.remove('search__active');
        output.classList.remove('search__output_on');
        const interval = setTimeout(()=>{
            searchElment.style.display = 'none';
            cover.classList.remove('cover_on');
        }, 500);
        cover.removeEventListener('click', searchOff);
    };
    document.querySelector('.search__icon').addEventListener('click', searchOff);
    
   /**
     * Выполняет поиск через API с возможностью добавления параметров
     * @param {string} query - Поисковый запрос
     * @param {Object} [params={}] - Дополнительные параметры запроса
     * @returns {Promise<Object>} - Обещание с данными JSON от сервера
     */
    async function fetchSearchResults(query, params = {}) {
        try {
        // Создаем параметры URL, включая поисковый запрос и дополнительные параметры
        const urlParams = new URLSearchParams({
            // search: encodeURIComponent(query), - кодирует так, что сервер не находит ничего на кириллице
            search: query,
            ...params
        });
        
        const apiUrl = `/jsonapi/v2/pages/?${urlParams.toString()}`;
        
        // Выполняем GET-запрос
        const response = await fetch(apiUrl, {
            method: 'GET',
            headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
            }
        });
    
        // Проверяем статус ответа
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
    
        // Парсим JSON и возвращаем данные
        return await response.json();
        
        } catch (error) {
        console.error('Ошибка при выполнении запроса:', error);
        throw error;
        }
    }
    
    // Функция debounce: минимизирует число вызовов функции 
    // (пропуская несколько, в один финальный)
    function debounce(callee, timeoutMs) {
        return function perform(...args) {
          let previousCall = this.lastCall;
          this.lastCall = Date.now();
          if (previousCall && this.lastCall - previousCall <= timeoutMs) {
            clearTimeout(this.lastCallTimer);
          }
          this.lastCallTimer = setTimeout(() => callee(...args), timeoutMs);
        }
    }

    function createTag (tag, attrs={}, innerText) {
        const elem = document.createElement(tag);
        elem.innerText = innerText;
        for (let key in attrs) {
            elem.setAttribute(key, attrs[key])
        }
        return elem;
    }

    async function search(event) {
        const search_text = event.value;
        if (done === search_text) return;
        if (search_text.length > 2) {
            output.classList.add('search__output_on');
            const response = await fetchSearchResults(search_text);
            output.innerHTML = '';
            output.appendChild(createTag('div', {
                style: "padding: .5em; text-indent: .5em;",
            }, `Всего совпадений ${response.items.length}`));
            const output_links = createTag('div', {}, '')
            output.appendChild(output_links)
            for (const item of response.items) {
                output_links.appendChild(createTag('a', {
                    href: item.meta.html_url,
                    class: 'search__response_link',
                }, item.title));
            }
            done = search_text;
        };
    };
    const searchDebounse = debounce(search, 1000);
    document.getElementById('SearchInput').addEventListener('input', function() {searchDebounse(this)});
    document.getElementById('SearchInput').addEventListener('keydown', function(event) {
        const active = output.querySelector('.search__response_link_active');
        switch (event.key) {
            case 'Enter':
                if (active) {
                    window.location.assign(active.getAttribute('href')); // переход с сохранением истории
                    break;
                };
                search(event.currentTarget);
                event.preventDefault();
                break;
            case 'Escape':
                if (active) {
                    active.classList.remove('search__response_link_active');
                    event.preventDefault();
                    break;
                };
                output.innerHTML = '';
                output.classList.remove('search__output_on')
                break;
            case 'ArrowDown':
                searchResponseArrowHandler(true);            
                break;
            case 'ArrowUp':
                searchResponseArrowHandler(false);
                break;
        }
    });
    /**
     * Ищем в DOM результаты поиска, a.search__response_link
     * если находим элемент a.search__response_link.search__response_link_active,
     * то двигаемся в зависимости от direction - (true) вниз или (false) вверх.
     */
    function searchResponseArrowHandler(direction=true) {
        const seach_total_elements = output.querySelectorAll('a.search__response_link'); //все элементы
        if (seach_total_elements.length == 0) return;
        //ищем активный, если его нет, то "выбираем первый"
        let active = output.querySelector('.search__response_link_active');
        if (direction) { // вниз
            if (active) active = active.nextSibling ? active.nextSibling : active;
            else active = seach_total_elements[0]; // выбираем первый
        } else { // вверх
            if (active) active = active.previousSibling ? active.previousSibling : active;
            else active = seach_total_elements[seach_total_elements.length - 1] // выбираем последний
        } // очищаем все элементы от .search__response_link_active
        for (let element of seach_total_elements) element.classList.remove('search__response_link_active');
        active.classList.add('search__response_link_active');
    }
}; searchActivate();
