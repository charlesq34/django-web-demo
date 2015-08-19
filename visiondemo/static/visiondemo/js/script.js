// check for selected crop region
function checkForm() {
    if (parseInt($('#x1').val())) return true;
    $('.error').html('Please select a crop region and then press Upload').show();
    return false;
};

// update info by cropping (onChange and onSelect events handler)
function updateInfo(e) {
    $('#x1').val(e.x);
    $('#y1').val(e.y);
    $('#x2').val(e.x2);
    $('#y2').val(e.y2);
};

// Create variables (in this scope) to hold the Jcrop API and image size
var jcrop_api, boundx, boundy;

//document.getElementById('preview').onload = 
function start_crop() { // onload event handler
    // display step 2
    $('.step2').fadeIn(500);
    var oImage = document.getElementById('preview');

    // destroy Jcrop if it is existed
    if (typeof jcrop_api != 'undefined') {
        jcrop_api.destroy();
        jcrop_api = null;
        $('#preview').width(oImage.naturalWidth);
        $('#preview').height(oImage.naturalHeight);
    }

    setTimeout(function(){
        // initialize Jcrop
        $('#preview').Jcrop({
            minSize: [32, 32], // min crop size
            //aspectRatio : 1, // keep aspect ratio 1:1
            bgFade: true, // use fade effect
            bgOpacity: .3, // fade opacity
            onChange: updateInfo,
            onSelect: updateInfo,
        }, function(){

            // use the Jcrop API to get the real image size
            var bounds = this.getBounds();
            boundx = bounds[0];
            boundy = bounds[1];

            // Store the Jcrop API in the jcrop_api variable
            jcrop_api = this;
        });
    },3000);
};

function urlHandler() {
    document.getElementById('preview').src = document.getElementById('url').value;
    start_crop();
    //TODO: support different submit method for URLs
};


function fileSelectHandler() {

    // get selected file
    var oFile = $('#image_file')[0].files[0];

    // hide all errors
    $('.error').hide();

    // check for image type (jpg and png are allowed)
    var rFilter = /^(image\/jpeg|image\/png)$/i;
    if (! rFilter.test(oFile.type)) {
        $('.error').html('Please select a valid image file (jpg and png are allowed)').show();
        return;
    }

    // check for file size
    if (oFile.size > 2048 * 2048) {
        $('.error').html('You have selected too big file, please select a one smaller image file').show();
        return;
    }

    // preview element
    var oImage = document.getElementById('preview');

    // prepare HTML5 FileReader
    var oReader = new FileReader();
        oReader.onload = function(e) {

        // e.target.result contains the DataURL which we can use as a source of the image
        oImage.src = e.target.result; 
        start_crop();
    };

    // read selected file as DataURL
    oReader.readAsDataURL(oFile);
}
