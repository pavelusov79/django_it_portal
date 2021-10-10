$('.bi-sliders').on('click', function() {
    $('.extend').css('display', 'block');
    $('label[for=search]').css('display', 'inline-block');
    $('label[for=search_vacancy]').css('display', 'inline-block');
    $(this).css('opacity', 0);
    $('.button-search').css('margin-left', '1.3rem');

})

$('.share').on('click', function() {
    $('.share-icons').toggleClass("active");
    return false;
});

$('.experience-button').formset({
    addText: 'Добавить опыт работы',
    deleteText: 'Удалить',
    prefix: '2',
    formCssClass: 'dynamic-experience_form'
});

$('.education-button').formset({
    addText: 'Добавить образование',
    deleteText: 'Удалить',
    prefix: '1',
    formCssClass: 'dynamic-education_form'
});

$('svg').click(function() {
    var my_var = $(this).attr('class');
    var data_id = $(this).attr('id');
    var url = $(this).attr('data-url');
    $.ajax({
        type: 'GET',
        url: url,
        data: {class: my_var, data_id: data_id},
        success: function(data) {
            console.log('----' + $('#' + data_id).attr('class'));
            if($('#' + data_id).attr('class') == 'bi bi-star') {
                $('#' + data_id).removeClass('bi-star').addClass('bi-star-fill');
                $('#' + data_id).children('path').attr('d', "M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z");
            }else if($('#' + data_id).attr('class') == 'bi bi-star-fill') {
                $('#' + data_id).removeClass('bi-star-fill').addClass('bi-star');
                $('#' + data_id).children('path').attr('d', "M2.866 14.85c-.078.444.36.791.746.593l4.39-2.256 4.389 2.256c.386.198.824-.149.746-.592l-.83-4.73 3.522-3.356c.33-.314.16-.888-.282-.95l-4.898-.696L8.465.792a.513.513 0 0 0-.927 0L5.354 5.12l-4.898.696c-.441.062-.612.636-.283.95l3.523 3.356-.83 4.73zm4.905-2.767-3.686 1.894.694-3.957a.565.565 0 0 0-.163-.505L1.71 6.745l4.052-.576a.525.525 0 0 0 .393-.288L8 2.223l1.847 3.658a.525.525 0 0 0 .393.288l4.052.575-2.906 2.77a.565.565 0 0 0-.163.506l.694 3.957-3.686-1.894a.503.503 0 0 0-.461 0z");
            }
        }
    });
});

$('.see_vacancy').click(function() {
    var vacancy_id = $(this).attr('id');
    var id = $('#status' + vacancy_id).html();
    var url = $(this).attr('data-url');
    $.ajax({
        type: 'GET',
        url: url,
        data: {vacancy_id: vacancy_id, status_id: id},
        success: function(data) {
            console.log('success');
        }
    });
});

$('.see_resume').click(function() {
    var resume_id = $(this).attr('id');
    var id = $('#status' + resume_id).html();
    var url = $(this).attr('data-url');
    $.ajax({
        type: 'GET',
        url: url,
        data: {resume_id: resume_id, status_id: id},
        success: function(data) {
            console.log('success');
        }
    });
});



