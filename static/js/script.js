document.querySelector(".burger").onclick = function() {
	this.classList.toggle("burger-active");
	document.querySelector("nav").classList.toggle("active");
}

$(function() {
  // при нажатии на кнопку top_up
  $('.top_up').click(function() {
    // переместиться в верхнюю часть страницы
    $("html, body").animate({
      scrollTop:0},1000);
  })
})
// при прокрутке окна (window)
$(window).scroll(function() {
  // если пользователь прокрутил страницу более чем на 500px
  if ($(this).scrollTop()>500) {
    // то сделать кнопку top_up видимой
    $('.top_up').fadeIn();
    $('.top_up').css({display:"flex"});
  }
  // иначе скрыть кнопку top_up
  else {
    $('.top_up').fadeOut();
  }
});

