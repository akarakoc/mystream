
$(function () {
    $('[data-toggle="popover"]').popover();
});


function getImageXYWH(c)
{
    console.log('x='+ c.x +' y='+ c.y +' x2='+ c.x2 +' y2='+ c.y2)
    console.log('w='+c.w +' h='+ c.h)
    imageXYWH = "xywh=pixel:" + c.x + "," + c.y + "," + c.w + "," + c.h;
};

function getImageTarget(c){
    imageAnnotationSelected = true;
    imageTarget = $('.jcrop-holder img').prop("currentSrc");
}

$( document ).ready(function() {

// $( "*", document.body ).click(function( event ) {
//     console.log("this : " + this );
//   var offset = $( this ).offset();
//   event.stopPropagation();
//   console.log( "deneme : " + " coords ( " + offset.left + ", " + offset.top + " )" );
// });


    // jQuery(function($){
    //
    //   $('img').Jcrop({
    //     onChange:   getImageXYWH,
    //     onSelect:   getImageTarget
    //   });
    //
    // });

    $('img').Jcrop({
        onChange:   getImageXYWH,
        onSelect:   getImageTarget
      });
/*******************************************/
/*  Define Variables
/*******************************************/

    // From http://www.whatwg.org/specs/web-apps/current-work/multipage/states-of-the-type-attribute.html#e-mail-state-%28type=email%29
    uriRegex = /^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/,
    urlRegex = /((([A-Za-z]{3,9}:(?:\/\/)?)(?:[\-;:&=\+\$,\w]+@)?[A-Za-z0-9\.\-]+|(?:www\.|[\-;:&=\+\$,\w]+@)[A-Za-z0-9\.\-]+)((?:\/[\+~%\/\.\w\-_]*)?\??(?:[\-\+=&;%@\.\w_]*)#?(?:[\.\!\/\\\w]*))?)/;
    target = $( "#target" ),
    body = $( "#body" ),
    allFields = $( [] ).add( target ).add( body ),
    tips = $( ".validateTips" );

    imageAnnotationSelected = false;
    imageXYWH = "";
    imageTarget = "";

/*******************************************/
/*  Rest API Endpoints
/*******************************************/
    search_remote ="https://mystream-anno.herokuapp.com/searchAnnotation";
    search_local ="http://localhost:8080/searchAnnotation";

    annotate_remote = "https://mystream-anno.herokuapp.com/annoateText";
    annotate_local = "http://localhost:8080/annoateText";

    visualizeAnnotations();

/*******************************************/
/*  Annotation Submit
/*******************************************/


});

$( document ).on( "click", "#createAnnotationButton", function(e) {

    if(window.getSelection() == "" && !imageAnnotationSelected ){
        showMessage("Warning", "Please, select a part of text or image to annotate.");
    }else if(imageAnnotationSelected){
            var annoType = "Image";

            var ab = new AnnotationBuilder().tagging(imageTarget, imageXYWH);
            // ab.result.target.toSelection();
            var json = ab.toJSON();
            console.log(json);

            openAnnotationModal( imageTarget + " " + imageXYWH , json, annoType);

    }else if ( window.getSelection() != "" ){
        var annoType = "Text";

        var ab = new AnnotationBuilder().highlight();
        ab.result.target.toSelection();
        var json = ab.toJSON();

        openAnnotationModal( ab.result.target.selector[1].exact, json, annoType );

        e.preventDefault();
    }
});


$( document ).contextmenu(function(e) {

    var ab = new AnnotationBuilder().highlight();
    ab.result.target.toSelection();
    var json = ab.toJSON();

    openAnnotationModal( ab.result.target.selector[1].exact, json );

    e.preventDefault();
});

function openAnnotationModal( targetVal, json, annoType ){
    $( "#target" ).val(targetVal);
    $( "#body" ).val("");

    var obj = JSON.parse(json);
    var pretty = JSON.stringify(obj, undefined, 4);

    $( "#jsonAnnotation" ).val(pretty);
    $( "#annoType" ).val(annoType);

    $("#modalLongTitle").html("Create Annotation");
    $("#submit").html("Create");

    $("#annotation-modal").modal();
}

$(document).on('submit', "#annotation-modal-form", function(event) {
    event.preventDefault();
    createAnnotation();
    return false;
});


$(document).on('keyup', "#searchAnnotation", function() {
    var annoIndex;
    var searchKey = $("#searchAnnotation").val();

    if( searchKey == '' || searchKey == undefined || searchKey == null || searchKey == "*")
        $(".annoDiv").css("display", "block");

    var btnList = $(".updateAnnotation");

    $.each(btnList, function(index, btn) {
        var json = JSON.stringify($(btn).data("json"));
        annoIndex = $(btn).attr("id").split("anno-update-bttn-")[1];
        if(json.toLowerCase().includes(searchKey.toLowerCase()))
            $("#anno-div-" + annoIndex).css("display","block");
        else
            $("#anno-div-" + annoIndex).css("display","none");
    });
});

$(document).on('click', ".updateAnnotation", function() {
    $(".popover").hide();
    $("#target").val($(this).data("selected"));
    $("#body").val($(this).data("body"));
    $("#type").val($(this).data("type"));
    $("#jsonAnnotation").val(JSON.stringify($(this).data("json")));

    // changes for update
    $("#modalLongTitle").html("Update Annotation");
    $("#submit").html("Update");

    $("#annotation-modal").modal();
  });


$(document).on('click', ".updateImageAnnotation", function() {
    $(".popover").hide();
    $("#target").val($(this).data("selected"));
    $("#body").val($(this).data("body"));
    $("#type").val($(this).data("type"));
    $("#jsonAnnotation").val(JSON.stringify($(this).data("json")));

    // changes for update
    $("#modalLongTitle").html("Update Annotation");
    $("#submit").html("Update");

    $("#annotation-modal").modal();
  });

$(document).on('click', "#slideButton", function() {
    $( "#annoContainer").toggle('blind',1000);
});

$(document).on('click', "#openHighlightButton", function() {
    $( "#closeHighlightButton").css("display", "block");
    $(this).css("display", "none");

    var textAnnoList = $(".annotationSelector");

    $.each(textAnnoList, function(index, a) {
        $(a).addClass("highlightedAnnotation");
    });

    var imageAnnoList = $(".pointedAnnotation");

    $.each(imageAnnoList, function(index, a) {
        $(a).css("display", "block");
    });

});

$(document).on('click', "#closeHighlightButton", function() {
    $( "#openHighlightButton").css("display", "block");
    $(this).css("display", "none");

    var annoList = $(".annotationSelector");

    $.each(annoList, function(index, a) {
        $(a).removeClass("highlightedAnnotation");
    });


    var imageAnnoList = $(".pointedAnnotation");

    $.each(imageAnnoList, function(index, a) {
        $(a).css("display", "none");
    });
});

$(document).on('click', ".annotationSelector", function() {

    $(".popover").hide();

    var popId = $(this).attr("id");


    if($(this).hasClass("highlightedAnnotation")) {
        $(this).popover('show');
         setTimeout(function() {
            $("#" + popId).popover('hide');
        }, 3000);
    }else{
        $(this).popover('hide');
    }
});






function showMessage(title, message){
    $('.toast-title').html(title);
    $('.toast-body').html(message);
    $('.toast').toast({ delay: 3000 });
    $('.toast').toast('show');
}

/*******************************************/
/*  Annotation Functions
/*******************************************/
function visualizeAnnotations(){
    $.ajax({
      url: search_remote,
      data: { source : window.location.href },
      contentType: 'application/json',
      success: function(data, status){
          console.log("okk");
          var jsonList = data.response.annoList;

          $.each(jsonList, function(index, json) {
                                try {
                                     var annoType = "Text";
                                     var selectorList = json.target.selector;
                                     $.each(selectorList, function(index, selector) {
                                         if(selector.type == "FragmentSelector"){
                                             annoType = "Image"
                                         }
                                     });
                                     if( annoType == "Text"){
                                         var ab2 = new AnnotationBuilder().fromJSON(JSON.stringify(json));
                                         ab2.result.target.toSelection();
                                         surroundSelection(json) ;
                                     }else if( annoType == "Image"){
                                         pointImage(json, index);
                                     }

                                     addAnnotationToSidebar(json, index, annoType);

                                }catch(error){
                                    console.log(error);
                                    console.log(json);

                                }

                                });
      }
    });
}

function addAnnotationToSidebar(json, index, annoType){

    // Update Size Firstly
    var count = index + 1;

    // if($(".annoContainer").height() < 1000 )
        $(".annoContainer").css("height" , $(".annoContainer").height() + 200 );

    if(count == 1)
        $("#annotationCount").html("There is " + count + " annotation on this page");
    else
        $("#annotationCount").html("There are " + count + " annotations on this page");
    var body = json.body[0];
    var buttonBody;

    var annotationContent = "";
    if (body.type == 'TextualBody') {
        annotationContent = body.value;
        buttonBody = body.value;
    }else{
         annotationContent = body.related;
         buttonBody = body.related;
    }

    if(annotationContent.includes("http"))
        annotationContent = annotationContent.replace(urlRegex, " <a  href='$1' target='_blank' >$1</a> ");
    else
        annotationContent = annotationContent.replace(urlRegex, " <a  href='//$1' target='_blank' >$1</a> ");

    var annoDivId = "anno-div-" + index;
    var annoTitleId = "anno-title-" + index;
    var annoContentId = "anno-content-" + index;
    var annoUpdateId = "anno-update-bttn-" + index;
    var annoLabel = "";

    if( annoType == "Text" ){
        annoLabel = window.getSelection();
    }else{
        annoLabel = "Image on the page";
    }

    $('.annoContainer #content').append(
        "<div id='" + annoDivId + "' class='annoDiv'>  " +
        "<div id='" + annoTitleId + "' class='annoTitle'>" +
            "<label> " + annoLabel + "</label>" +
        "</div>" +
        "<div>" +
            "<label> <i> Type </i>:" + body.type + " </label>" +
        "</div>" +
        "<div>" +
            "<label> <i> Content </i> : </label>" +
            "<label id='" + annoContentId + "'>" + annotationContent + " </label>" +
        "</div>" +
        "<div>" +
            // "<label>Json : </label>" +
            // "<label> " + JSON.stringify(json) + "</label>" +
        "</div>" +
        "<button id='" + annoUpdateId + "' type='button' class='btn btn-warning updateAnnotation'" +
            " data-body='" + buttonBody +
            "' data-type='" + body.type +
            "' data-selected='" + annoLabel +
            "' data-json='" + JSON.stringify(json) +
            "'>Update Annotation" +
        "</button>" +
        "</div>"
    );
}

function pointImage(anno, index){

    var annoUpdateId = "anno-image-update-bttn-" + index;
    var body = anno.body[0];

    var buttonBody;
    if (body.type == 'TextualBody') {
        buttonBody = body.value;
    }else{
         buttonBody = body.related;
    }

    /* ---------------------------------------- */
    /*  Resolve Image Location from Annotation  */
    /* ---------------------------------------- */
    var xywh = anno.target.selector[0].value;
    xywh = xywh.replace("xywh=pixel:","");
    xywh = xywh.split(",");

    var imageTarget = anno.target.source.split("/");
    var imageSrc = imageTarget[imageTarget.length-1 ];
    var position = $("div img[src$='" + imageSrc + "']").parent().offset();
    var top = parseInt(position.top) + parseInt(xywh[0]);
    var left = parseInt(position.left) + parseInt(xywh[1]);

    var imagePointButton = "<div class='pointedAnnotation' >" +
        "<button id='" + annoUpdateId +
        "' data-body='" + buttonBody +
        "' data-selected='" + imageSrc + " " + anno.target.selector[0].value +
        "' data-type='" + body.type +
        "' data-currentSrc='" + anno.id +
        "' data-json='" + JSON.stringify(anno) +
        "' type='button' class='btn btn-warning updateImageAnnotation' style=' " +
        " display: block; " +
        " position: fixed; " +
        " height: 1.5em; " +
        " width: 1.5em; " +
        " top : " + top + "px; left :" + left + "px;" +
        "' >" +
            "<svg class='bi bi-chat-square-dots-fill' width='1em' height='1em' viewBox='0.5 0 15 15' fill='currentColor' xmlns='http://www.w3.org/2000/svg'>" +
              "<path fill-rule='evenodd' d='M0 2a2 2 0 012-2h12a2 2 0 012 2v8a2 2 0 01-2 2h-2.5a1 1 0 00-.8.4l-1.9 2.533a1 1 0 01-1.6 0L5.3 12.4a1 1 0 00-.8-.4H2a2 2 0 01-2-2V2zm5 4a1 1 0 11-2 0 1 1 0 012 0zm4 0a1 1 0 11-2 0 1 1 0 012 0zm3 1a1 1 0 100-2 1 1 0 000 2z' clip-rule='evenodd'/>" +
            "</svg>" +
        "</button>" +
     "</div>";

    $('.image').append( imagePointButton );



}


function surroundSelection(json, index) {

    var body = json.body[0];
    var canonical = json.canonical;

    var isUpdate = $("#submit").html() == "Update";

     if( !isUpdate ){
        var span = document.createElement("span");
        span.class="surroundSpan";
        span.style.fontWeight = "bold";
        span.style.color = "black";

        var a = document.createElement('a');
        a.target = "_blank";
        var id = json.canonical;
        id = id.replace("urn:uuid:","");
        // a.style.background = "#ffd969";
        $(a).addClass("highlightedAnnotation");
        $(a).addClass("annotationSelector");
        $(a).attr("id", id);


        $(a).data("title", "Annotation");
        $(a).data("html", true);
        $(a).data("placement", "bottom");
        $(a).data("container", "body");

        $(a).data("template", $("#popover-template").textContent);

        span.appendChild(a);

        if (window.getSelection) {
            var sel = window.getSelection();
            if (sel.rangeCount) {
                var range = sel.getRangeAt(0).cloneRange();
                range.surroundContents(a);
                sel.removeAllRanges();
                sel.addRange(range);
            }
        }
     }
    var buttonBody;
    var annotationContent = "";
    var addGoToButton = false;
    var addTextualContent = false;

     if(body.type == 'TextualBody'){
         annotationContent = body.value;
         addTextualContent = true;
         buttonBody = body.value
     }else{
         annotationContent = body.related;
         addGoToButton = true;
         buttonBody = body.related;
     }
      annotationContent = annotationContent.replace( urlRegex,  " <a  href='//$1' target='_blank' >$1</a> ");


    var contentHTMLText  =  "<div>" +
                            "The word " + window.getSelection() + " is linked with a " + body.type;
    if(addGoToButton)
        contentHTMLText +=  " <a href='" + body.related + "' target='_blank' > Go to Annotation </a> ";

    if(addTextualContent)
        contentHTMLText +=  "<div>" + " <strong> Annotation Content </strong> " +
                            " <span>" +  annotationContent + "</span>" + "</div>";

    contentHTMLText     +=  " <button type='button' class='btn btn-warning updateAnnotation'" +
                                " data-body='" + buttonBody +
                                "' data-type='" + body.type +
                                "' data-selected='" + window.getSelection() +
                                "' data-json='" + JSON.stringify(json) +
                                "'>Update Annotation</button>\n"
                            "</div>";

    $(a).popover({delay: { "show": 100, "hide": 1000 }, trigger: 'click', sanitize:false, content: contentHTMLText});


}






function sendPostRequest(post_data, anno, annoType){
    $.ajax({
        type: "POST",
        url: annotate_remote,
        data: JSON.stringify(post_data),
        contentType: 'application/json',
        success: function (data, status) {
            console.log("Annotation is saved successfully");

            var ab2 = new AnnotationBuilder().fromJSON(JSON.stringify(anno));

            if( annoType == "Image"){
                pointImage(anno, "none")
            }else if ( annoType == "Text"){
                ab2.result.target.toSelection();
                surroundSelection(anno);
            }

            if($("#submit").html() == "Update")
                showMessage("Info", "Annotation is updated successfully. ");
            else
                showMessage("Info", "Annotation is created successfully. ");

            $("#annotation-modal").modal('hide');
            //location.reload();

        },
        error: function (error) {
            console.log("Annotation cannot be saved.");
            console.log(error);

            showMessage("Error", "Errors occured while creating annoation !");
        }

    });
}

function createAnnotation() {
    var type = $("#type").val();
    var body = $("#body").val();
    var annoType = $("#annoType").val();

    var jsonAnnotation = $("#jsonAnnotation").val();

    var valid = true;
    allFields.removeClass("ui-state-error");

    if( type == "Image" || type == "Video" )
        valid = valid && checkRegexp($("#body"), urlRegex, "failed");

    if (valid) {
        var content = {};
        if( type == "TextualBody" ){
            content = { "type": "TextualBody", "format": "text/plain", "value": body };
        }else if(  type == "Image" ){
            content = { "id" : body, "type": "Image", "format":"image/jpeg", "related": body };
        }else if(  type == "Video" ){
            content = { "id" : body, "type": "Video", "format":"audio/mpeg", "related": body };
        }

        var textAnno = JSON.parse(jsonAnnotation);
        textAnno.body = [ content ];

        var post_data = { textAnno };
        sendPostRequest(post_data, textAnno, annoType);
    }
}

function isNotEmpty(param){
    return param != undefined && param != '' && param != null;
}

/*******************************************/
/*  Validation Functions
/*******************************************/

function updateTips( t ) {
  tips
    .text( t )
    .addClass( "ui-state-highlight" );
  setTimeout(function() {
    tips.removeClass( "ui-state-highlight", 1500 );
  }, 500 );
}

function checkLength( o, n, min, max ) {
  if ( o.val().length > max || o.val().length < min ) {
    o.addClass( "ui-state-error" );
    updateTips( "Length of " + n + " must be between " +
      min + " and " + max + "." );
    return false;
  } else {
    return true;
  }
}

function checkRegexp( o, regexp, n ) {
  if ( !( regexp.test( o.val() ) ) ) {
    o.addClass( "ui-state-error" );
    updateTips( n );
    return false;
  } else {
    return true;
  }
}


