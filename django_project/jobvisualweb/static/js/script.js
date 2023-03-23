$(document).ready(function(){
  $('.sub-btn').click(function(){
    $(this).next('.sub-item').slideToggle();
    $(this).find('.dropdown').toggleClass('rotate');

    
  });
  $('#dataTable').DataTable();
});