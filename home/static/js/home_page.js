/* document.addEventListener('DOMContentLoaded', function () { }
  */

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