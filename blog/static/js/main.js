document.getElementById('pic1').addEventListener('change', function() {
    var fileName = this.files.length ? this.files[0].name : 'No file chosen';
    document.getElementById('file-name1').textContent = fileName;
});

document.getElementById('pic2').addEventListener('change', function() {
    var fileName = this.files.length ? this.files[0].name : 'No file chosen';
    document.getElementById('file-name2').textContent = fileName;
});
// -------------------------
$(window).on('load', function (){
    $('.loader-wrapper').fadeOut('slow');
});

// ----------------------- menu section ---------------------------

