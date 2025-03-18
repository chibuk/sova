// Calendar module
const calCalendar = () => {
  const calcontainer = document.getElementById(`cal-container`),
        getPosition = () => { // позиция прокрутки ленты дней календаря
    return calcontainer.scrollLeft;
  },
        calDayWidth = () => { // ширина элемента .cal-day
    return calcontainer.querySelector(".cal-day").clientWidth;
  },
  // Ширина всей ленты с датами, которая прокручивается
        widthDays = () => {
    let widthall = 0;
    document.querySelectorAll(".cal-month").forEach(_month => {
      widthall += _month.clientWidth;
    });
    return widthall;
  },
        num = () => {   // шаг, сколько прокрутить на клик (в днях). Функция, чтобы обновлялось значение.
    return Math.floor(calcontainer.clientWidth / calDayWidth() / 2) - 1 // прокручиваем почти половину видимого содержания (-1)
  };
  // Показать|убрать стрелки перемотки ленты
  function reDrowArrows() {
    const position = getPosition();
    endposition = widthDays() - calcontainer.clientWidth - position;
    if (position == 0) document.getElementById('cal-start').style.display = 'none' // начало ленты
    else document.getElementById('cal-start').style.display = 'block';
    if (endposition <= 0) document.getElementById('cal-end').style.display = 'none' // конец ленты
    else document.getElementById('cal-end').style.display = 'block';
  }
  document.getElementById("cal-container").addEventListener('scroll', reDrowArrows);
  const resizeObserver = new ResizeObserver((entries, observer) => {
    entries.forEach((entry) => {
      reDrowArrows();
    });
  });
  resizeObserver.observe(calcontainer);
  function scrollDate(num) {  // Прокрутить ленту через num дней;
    let _left = getPosition() + num * calDayWidth();
    const calLsatWidth = document.getElementById('cal-last').clientWidth;
    if (widthDays() - _left - calLsatWidth < calcontainer.clientWidth) 
      _left = widthDays() - calcontainer.clientWidth + calDayWidth(); // прокрутим больше на calDayWidth, чтобы наверняка, оно дальше предела не даст
    calcontainer.scrollTo({top: 0, left: _left, behavior: 'smooth'});
  }
  document.getElementById('cal-start').addEventListener('click', () => scrollDate(-num())); // назад
  document.getElementById('cal-end').addEventListener('click', () => scrollDate(num()));  // вперед
  function setDayHandlers() { // назначить обработчики клика на .cal-day ссылки
    calcontainer.querySelectorAll('.cal-day').forEach(calday => {
      calday.addEventListener("click", function() {
        _setDate(this);
      });
    });
  }; setDayHandlers();
  // Коллекция id объектов EventPages, которые уже отображены (для уменьшения операций с DOM)
  let evensIdSet = new Set();
  /**
   * Объект управляет состоянием диапазона дат. Тут хранится (false|date_object)
   * начальная и конечная дата, начальный и конечный элемент, чтобы атрибутом
   * aria-current управлять его статусом. Здесь логика реакции на клик, когда
   * элемент выделяется или выделяется диапазон. Поле prn выдает результат.
   */
  const dateObject = {
    _start: false,
    _start_element: false,
    _end: false,
    _end_element: false,
    _setDate(calDayElement) { 
      const day = calDayElement.querySelector('time').getAttribute('datetime');
      return new Date(Date.parse(day)) 
    },
    set start(day) {
      if (day) { // YYYY-mm-dd|false
        if (this._start_element && this._start_element != day) this._start_element.setAttribute('aria-current', 'false');
        this._start = this._setDate(day);
        this._start_element = day;
        day.setAttribute('aria-current', 'true');
      }
      else { // Римена выбора дня
        this._start = false;
        this._start_element.setAttribute('aria-current', 'false');
        this._start_element = false;
      }
    },
    get start() {
      return this._start;
    },
    set end(day) {
      const cal_marker = document.getElementById('cal-marker'); // маркер диапазона дат
      if (day) { // YYYY-mm-dd|false
        if (day == this._start_element) { // Отмена выбора даты (повторный клик на элементе)
          this.start = false;
          return;
        }
        if (this._end_element) this._end_element.setAttribute('aria-current', 'false');
        this._end = this._setDate(day);
        this._end_element = day;
        day.setAttribute('aria-current', 'true');
        /**
         * Начальная дата может быть больше кеонечной, тогда на возврат,
         * меняем их местами.
         */
        let start = this.start,
            start_element = this._start_element,
            end = this.end,
            end_element = this._end_element;
        
        if (this.start > this.end) {
          start = this.end;
          start_element = this._end_element;
          end = this.start;
          end_element = this._start_element;
          this._start = start;
          this._start_element = start_element;
          this._end = end;
          this._end_element = end_element;
        }; // Берем координаты элементов start и end и располагаем маркер повех
        const top = start_element.offsetTop,
              left = start_element.offsetLeft,
              height = start_element.offsetHeight,
              width = (end_element.offsetLeft + end_element.offsetWidth) - left;
        cal_marker.style.cssText = `
          top: ${top}px; 
          left: ${left}px; 
          display: block;
          width: ${width}px; 
          height: ${height}px;`;
      }
      else {
        this._end = false;
        this._end_element.setAttribute('aria-current', 'false');
        this._end_element = false;
        cal_marker.style.display = "none";
        // evensIdSet.clear(); // Очисстка коллекции, т.к. начался выбор нового диапазона дат
      }
    },
    get end() {
      return this._end;
    },
    get prn() {
      if (!this.start) return; // Отмена выбора даты (повторный клик на то же число календаря)
      loadContent(this.start, this.end);  // отображение квадратов событий за этот диапазон дат
    }
  }
  function sleep(ms) {  // Для пауз await sleep(1000)
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  /**
   * Получение строки даты ISO формата, такие даты можно сравнивать как строки
   * @param {DateObject} date 
   * @returns "YYYY-mm-dd"
   */
  const dateToISO = (date) => {return date ? date.toISOString().split("T")[0] : ""};
  /**
   * Формирование строки даты
   * @param {'YYYY-mm-dd'} datestr 
   * @returns String(Сегодня | Завтра | dd.mm.YYYY)
   */
  const dts = (datestr) => {
    if (!datestr) return '';
    const now = (new Date());
    if (datestr <= dateToISO(now)) return "Сегодня"; // Даже если событие началось вчера, вернём "Сегодня"
    now.setDate(now.getDate() + 1);
    if (datestr == dateToISO(now)) return "Завтра";
    const _s = datestr.split("-");
    return `${_s[2]}.${_s[1]}.${_s[0]}`
  }
  /**
   * Получение строки интервала для вывода (Сегодня | Завтра | Завтра - dd-mm-YYYY)
   * @param {DateISOStr} date_on 
   * @param {DateISOStr} date_end 
   * @returns String
   */
  function d_interval_str(date_on, date_end) {
    if (!date_end || date_on == date_end) return dts(date_on);
    let d1 = dts(date_on);
    let d2 = dts(date_end);
    // После приведения dts (обраезает прошлый период, выдает "Сегодня" или "Завтра"), 
    // значения d1, d2 могут совпасть
    if (d1 == d2) return d1; 
    else return d1 + ' ‒ ' + d2;
  }
  /**
   * Заполняет ленту квадратиками обытий за указанный диапазон дат
   * @param {date} start 
   * @param {date} end 
   */
  async function loadContent (start, end) {
    const container = document.getElementById("cal__content");
    // Занружаем объекты EventPage
    const events = await fetchEvents(dateToISO(start), dateToISO(end));
    if (events) {
      // Соберём коллекцию id от всех полученных events для сравнения с имеющимися
      const newEventsId = new Set(events.items.map(item => item.id));
      // Вычитаем из существующих, коллекцию id полученных
      const difference = evensIdSet.difference(newEventsId) // получили Set элементов, которые надо удалить
      let elements_for_remove = [];
      // сначала присвоим им класс для эффекта исчезновения, потом разом удалим
      for (let _i of difference) {
        const element = container.querySelector(`[data-id='${_i}']`); // мученник
        element.classList.add('hideing'); // исчезает
        evensIdSet.delete(_i); // стираем о нём память
        elements_for_remove.push(element);
      }
      if (difference.size > 0) await sleep(1000); // время на исчезание удаляемых
      for (let _i of elements_for_remove) { // удаление
        _i.remove();
      }
      for (let event of events.items) {
        if (evensIdSet.has(event.id)) continue; // уже есть, пропускаем
        // Создание квадратиков событий (картинка с подписью снизу, датой и местом проведения)
        const div = createTag("a", {
          class: "event", 
          href: event.meta.html_url, 
          'data-id': event.id,
          'data-date': event.date_on, // для сортировки будем, сранвнивать строки дат YYYY-mm-dd
        }, '');
        div.appendChild(createTag("img", {
          src: event.image_thumbnail.url,
          class: "event__img"
        }, ''));
        const div_txt = createTag("div", {class: "event__text"}, ''); // блок с текстами под картинкой
        div.appendChild(div_txt);
        div_txt.appendChild(createTag("div",{class: 'event__text__h1'}, event.h1))
        const footer = createTag('div', {class: 'event__text__footer'}, ''); // блок для даты и места проведения
        div_txt.appendChild(footer);
        footer.appendChild(createTag("div",{class: 'event__text__footer__date nowrap'}, d_interval_str(event.date_on, event.date_end)));
        if (event.location ) footer.appendChild(createTag("div",{class: 'event__text__footer__location'}, event.location));
        /**
         * Из коллекции детей container'а проверять, начиная с последнего, сравнивать data-date,
         * если дата имеющегося больше, то пропустить и перейти к предыдущему элементу, если
         * равна или меньше, то вернуть текущий элемент, для вставки после него. Короче сортировка.
         * @param {'YYYY-mm-dd'} _dateString // такие даты можно сравнивать :) 
         */
        function findPosition(_dateString) {
          let _rez = false;
          if (container.hasChildNodes()){
            const children = container.children;
            const childrenReverse = ([...children]).reverse();
            for (let child of childrenReverse) {
              if (child.dataset.date > _dateString) _rez = child;
            };
          };
          return _rez; // false | positionElement
        };
        const beforeElement = findPosition(event.date_on);
        div.classList.add('showing'); // клвсс появления 400мсек
        if (beforeElement) {
          container.insertBefore(div, beforeElement);
        } else {
          container.appendChild(div);
        }
        evensIdSet.add(event.id); // Собираем id коллекцию имеющихся событий (EvenPage)
        setTimeout(() => { // пусть появление успеет сработать, потом убираем .showing
          div.classList.remove('showing'); // иначе потом .hideing не сработает
        }, 500);
      }
    }
    /**
     * Создание HTML тега
     * @param {string} tag 
     * @param {атрибут: "значение",} attrs 
     * @param {string} innerText 
     * @returns тег для встраивания в дерево dom
     */
    function createTag (tag, attrs={}, innerText) {
      const elem = document.createElement(tag);
      elem.innerText = innerText;
      for (let key in attrs) {
          elem.setAttribute(key, attrs[key])
      }
      return elem;
    }
  }
  /**
   * Загружает объекты EventPage, пересекающиеся с диапазоном запрошеных дат
   * @param {string} date_on 
   * @param {string} date_end 
   * @returns data (JSON с объектами внутри), 
   * data.meta.total_count содержит общее количество
   * обектов data.items
   */
  async function fetchEvents(date_on, date_end) {
    const delimiter = (date_on && date_end) ? "," : "",
          dateString = (date_on ? date_on + delimiter : '') + (date_end ? date_end : ''),
          url = `/jsonapi/v2/events/?dates=${dateString}&fields=date_on,date_end,h1,image_thumbnail,location&order=date_on`;
    return await fetchData(url);
  }
  /**
   * Запрос данных с сервера Fetch
   * @param {URIString} url 
   * @returns false|JSONDataObject
   */
  async function fetchData(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Ошибка:', error);
        return false; // в случае ошибки
    }
  }
  /**
   * Обработчик кликка по ленте с датами, инициирует загрузку данных с сервера
   * @param {HTMLTagElement} calDayElement 
   */
  async function _setDate(calDayElement) {
    if (!dateObject.start) dateObject.start = calDayElement;
    else if (!dateObject.end) dateObject.end = calDayElement;
    else {
      dateObject.end = false;
      dateObject.start = calDayElement;
    }
    dateObject.prn;
  };
  const _now = new Date(),
        _end = new Date();
  _end.setDate(_end.getDate() + 7); // 7 дней событий сразу покажет при загрузке
  calcontainer.querySelector(`[datetime="${dateToISO(_now)}"]`).parentNode.click();
  calcontainer.querySelector(`[datetime="${dateToISO(_end)}"]`).parentNode.click();
}; 
calCalendar();

const cal_settings = {
  mode: "range",
  dateFormat: "d-m-Y",
  minDate: "today",
  position: "auto right",
  clickOpens: false,
  positionElement: document.getElementById('cal-last'),
  defaultDate: ["19-03-2025", "22-03-2025"]
};
flatpickr.localize(flatpickr.l10ns.ru);
const fp = flatpickr('#cal-last-fp', cal_settings);

let toggle = false;
document.querySelector('#cal-last').addEventListener('click', (event) => {
  if (toggle) {
    toggle = false;
    fp.close();
  }
  else {
    toggle = true;
    fp.open();
  }
});
