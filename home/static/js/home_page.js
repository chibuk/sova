/* document.addEventListener('DOMContentLoaded', function () { }
  */

// Slider module
const slSlider = () => {
  // Функция debounce: минимизирует число вызовов функции (включая несколько в один финальный)
  function debounce(callee, timeoutMs) {
    return function perform(...args) {
      let previousCall = this.lastCall
      this.lastCall = Date.now()
      if (previousCall && this.lastCall - previousCall <= timeoutMs) {
        clearTimeout(this.lastCallTimer)
      }
      this.lastCallTimer = setTimeout(() => callee(...args), timeoutMs)
    }
  }
  
  let current = 1; // текущий слайд
  let runtimer = 0; // для ссылки на таймер, чтобы его перезапускать
  
  function setSlideControls() {
    const slider = document.querySelector('#sl-slides');
    const slides = slider.querySelectorAll('a');

    function setCurrentRadio(num) {
      document.querySelectorAll('#sl .button.button-radio').forEach(radio => {
        if (radio.getAttribute('aria-label') == `Показать ${num} из ${slides.length}`) radio.setAttribute('aria-current', true)
        else radio.setAttribute('aria-current', false);
      });
    }
    
    if (current <= slides.length) { // значит листаем следующий
      document.querySelector('.button-prev').setAttribute('aria-disabled', false);
      // а теперь проверим, что это не последний слайд
      if (current == slides.length) document.querySelector('.button-next').setAttribute('aria-disabled', true)
      else {
        document.querySelector('.button-next').setAttribute('aria-disabled', false);
        if (current == 1) document.querySelector('.button-prev').setAttribute('aria-disabled', true);
      }
    } else {   // листаем сначала
      current = 1;
      document.querySelector('.button-prev').setAttribute('aria-disabled', true);
      document.querySelector('.button-next').setAttribute('aria-disabled', false);
    }
    setCurrentRadio(current);
    resetRunTimer();
  }

  const getPosition = () => {
    const slide = document.querySelector(`#carousel-item-${current}`);
    return slide.offsetWidth * (current - 1);
  }
  
  // step - это шаг куда смещаемся (1 | -1)
  function slide(step) {
    const slider = document.querySelector('#sl-slides');
    current += step;
    setSlideControls();
    slider.scrollTo({top: 0, left: getPosition(), behavior: 'smooth'});
  };
  document.querySelector('.button-next').addEventListener('click', () => slide(1));
  document.querySelector('.button-prev').addEventListener('click', () => slide(-1));
  function radioAction() {
    document.querySelectorAll('.button.button-radio').forEach(radio => {
      radio.addEventListener('click', function() {
        current = parseInt(this.getAttribute('slide-num')); 
        slide(0);
      });
    });
  };
  radioAction();
  // обновляет позиции на событие скролл
  function onScrollEnd(event) {
    const position = event.scrollLeft;
    const elementWidth = event.offsetWidth;
    current = parseInt((elementWidth - 5 + position) / elementWidth) + 1; // начинаем счет с единицы
    setSlideControls();
  };
  const onScrollEndDebounce = debounce(onScrollEnd, 200);
  document.querySelector('#sl-slides').addEventListener('scroll', function() {onScrollEndDebounce(this)});

  runtimer = setInterval(slide, 6000, 1);
  function resetRunTimer() {
    clearInterval(runtimer);
    runtimer = setInterval(slide, 6000, 1);
  }

};  
slSlider();


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

  // Прокрутить ленту через num дней;
  function scrollDate(num) {
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
  /**
   * Объект управляет состоянием диапазона дат. Тут хранится (false|date_object)
   * начальная и конечная дата, начальный и конечный элемент, чтобы атрибутом
   * aria-current управлять его статусом. Здесь логика реакции на клик, когда
   * элемент выделяется или выделяется диапазон. Поле prn выдает результат.
   */
  const dateOject = {
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
      else {
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
        let start = this.start,
          start_element = this._start_element,
          end = this.end,
          end_element = this._end_element;
        if (this.start > this.end) {
          start = this.end;
          start_element = this._end_element;
          end = this.start;
          end_element = this._start_element;
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
      }
    },
    get end() {
      return this._end;
    },
    get prn() {
      /**
       * Начальная дата может быть больше кеонечной, тогда на возврат,
       * меняем их местами.
       */
      if (!this.start) return; // Отмена выбора даты (повторный клик на элементе)
      let start = this.start,
          start_element = this._start_element,
          end = this.end,
          end_element = this._end_element;
      if (this.start > this.end) {
        start = this.end;
        start_element = this._end_element;
        end = this.start;
        end_element = this._start_element;
      };
      loadContent(start, end);  // отображение квадратов событий за этот диапазон дат
    }
  }
  /**
   * Заполняет ленту квадратиками обытий за указанный диапазон дат
   * @param {date} start 
   * @param {date} end 
   */
  async function loadContent (start, end) {
    // dateToStr из объекта даты возвращает строку, формата YYYY-dd-mm
    const dateToStr = (date) => {return date ? date.toISOString().split("T")[0] : ""};
    const container = document.getElementById("cal__content");
    container.innerHTML = "";
    const events = await fetchEvents(dateToStr(start), dateToStr(end));
    if (events) {
      for (let event of events.items) {
        // Создание квадратиков событий (картинка с подписью снизу, датой и местом проведения)
        const div = createTag("a", {class: "event", href: event.meta.html_url}, '');
        container.appendChild(div);
        div.appendChild(createTag("img", {
          src: event.image_thumbnail.url,
          class: "event__img"
        }, ''));
        const div_txt = createTag("div", {class: "event__text"}, '')
        div.appendChild(div_txt);
        div_txt.appendChild(createTag("div",{class: 'event__text__h1'}, event.h1))
        
        const dts = (datestr) => {
          const now = new Date();
          if (datestr == now.toISOString().split("T")[0]) return "Сегодня";
          // let tomorrow = new Date();
          now.setDate(now.getDate() + 1);
          // alert(tomorrow.toISOString().split("T")[0]);
          if (datestr == now.toISOString().split("T")[0]) return "Завтра";
          const date = new Date(Date.parse(datestr));
          return date.toLocaleDateString();
          // return date.toLocaleDateString('ru-RU', {weekday: "long", day: '2-digit', month: '2-digit', year: "numeric"});
        }
        
        div_txt.appendChild(createTag("span",{class: 'event__text__date'}, (dts(event.date_on) + (event.date_end ? ' - ' + dts(event.date_end) : ''))))
        if (event.location ) div_txt.appendChild(createTag("span",{class: 'event__text__location'}, event.location));
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
      return elem
    }
  }
  // function datesToStrArray(start, end) {
  //   let dates = [];
  //   if (!start) {
  //     dates = [end.toISOString().split("T")[0]];
  //     return dates;
  //   }
  //   let _start = new Date(Date.parse(start));
  //   let _end = new Date(Date.parse(end))
  //   let i = 0;
  //   do {
  //     i += 1;
  //     dates.push(_start.toISOString().split("T")[0]);
  //     _start.setDate(_start.getDate() + 1);
  //   } while (_start < _end);
  //   dates.push(_end.toISOString().split("T")[0]);
  //   return dates;
  // };
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
    if (!dateOject.start) dateOject.start = calDayElement;
    else if (!dateOject.end) dateOject.end = calDayElement;
    else {
      dateOject.end = false;
      dateOject.start = calDayElement;
    }
    dateOject.prn;
  };
  loadContent(new Date());
}; 
calCalendar();


// Countdown Timer
class CountdownTimer {
  constructor(deadline, onUpdate, onComplete) {
    if (!(deadline instanceof Date)) {
      throw new Error('`deadline` должен быть объектом Date.');
    }

    this.deadline = deadline;
    this.onUpdate = onUpdate;
    this.onComplete = onComplete;
    this.timerId = null;

    this.start();
  }

  // Склонение числительных для отображения корректной формы слова
  static declensionNum(num, words) {
    return words[num % 100 > 4 && num % 100 < 20 ? 2 : [2, 0, 1, 1, 1, 2][(num % 10 < 5) ? num % 10 : 5]];
  }

  // Запуск таймера
  start = () => {
    this.update();
    this.timerId = setInterval(this.update, 1000);
  };

  // Остановка таймера
  stop = () => {
    if (this.timerId) {
      clearInterval(this.timerId);
      this.timerId = null;
    }
  };

  // Вычисление оставшегося времени
  calculateTime = () => {
    const now = new Date();
    const diff = Math.max(0, this.deadline - now);

    return {
      days: Math.floor(diff / (1000 * 60 * 60 * 24)),
      hours: Math.floor((diff / (1000 * 60 * 60)) % 24),
      minutes: Math.floor((diff / (1000 * 60)) % 60),
      seconds: Math.floor((diff / 1000) % 60),
      diff,
    };
  };

  // Форматирование чисел с ведущим нулём
  formatTime = (value) => String(value).padStart(2, '0');

  // Обновление данных таймера
  update = () => {
    const { days, hours, minutes, seconds, diff } = this.calculateTime();

    const formattedTime = {
      days: this.formatTime(days),
      hours: this.formatTime(hours),
      minutes: this.formatTime(minutes),
      seconds: this.formatTime(seconds),
      daysTitle: CountdownTimer.declensionNum(days, ['день', 'дня', 'дней']),
      hoursTitle: CountdownTimer.declensionNum(hours, ['час', 'часа', 'часов']),
      minutesTitle: CountdownTimer.declensionNum(minutes, ['минута', 'минуты', 'минут']),
      secondsTitle: CountdownTimer.declensionNum(seconds, ['секунда', 'секунды', 'секунд']),
    };

    // Callback при обновлении
    this.onUpdate?.(formattedTime);

    // Остановка таймера по завершении
    if (diff === 0) {
      this.stop();
      this.onComplete?.();
    }
  };
}

document.addEventListener('DOMContentLoaded', function () {
  const elDays = document.querySelector('.timer__days');
  const elHours = document.querySelector('.timer__hours');
  const elMinutes = document.querySelector('.timer__minutes');
  const elSeconds = document.querySelector('.timer__seconds');

  // Конечная дата
  const now = new Date();
  const deadline = new Date(`${now.getFullYear()}-01-31T23:59:59`);

  // Создание нового таймера
  const timer = new CountdownTimer(
    deadline,
    (time) => {
      elDays.textContent = time.days;
      elHours.textContent = time.hours;
      elMinutes.textContent = time.minutes;
      elSeconds.textContent = time.seconds;
      elDays.dataset.title = time.daysTitle;
      elHours.dataset.title = time.hoursTitle;
      elMinutes.dataset.title = time.minutesTitle;
      elSeconds.dataset.title = time.secondsTitle;
    },
    () => {
      document.querySelector('.timer').textContent = 'С Новым Годом!';
    }
  );
});
