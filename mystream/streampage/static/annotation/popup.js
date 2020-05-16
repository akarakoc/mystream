
$(function () {
    $('[data-toggle="popover"]').popover();
});




$( document ).ready(function() {


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




$( document ).contextmenu(function(e) {

    var ab = new AnnotationBuilder().highlight();
    ab.result.target.toSelection();
    var json = ab.toJSON();
    // var ab2 = new AnnotationBuilder().fromJSON(json);
    // ab2.result.target.toSelection();

    $( "#target" ).val(ab.result.target.selector[1].exact);

    var obj = JSON.parse(json);
    var pretty = JSON.stringify(obj, undefined, 4);

    $( "#jsonAnnotation" ).val(pretty);

    $("#modalLongTitle").html("Create Annotation");
    $("#submit").html("Create");

    $("#annotation-modal").modal()

    e.preventDefault();
});

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

$(document).on('click', "#slideButton", function() {
    $( "#annoContainer").toggle('blind',1000);
});

$(document).on('click', "#openHighlightButton", function() {
    $( "#closeHighlightButton").css("display", "block");
    $(this).css("display", "none");

    var annoList = $(".annotationSelector");

    $.each(annoList, function(index, a) {
        $(a).addClass("highlightedAnnotation");
    });
});

$(document).on('click', "#closeHighlightButton", function() {
    $( "#openHighlightButton").css("display", "block");
    $(this).css("display", "none");

    var annoList = $(".annotationSelector");

    $.each(annoList, function(index, a) {
        $(a).removeClass("highlightedAnnotation");
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
                                    var ab2 = new AnnotationBuilder().fromJSON(JSON.stringify(json));
                                    ab2.result.target.toSelection();

                                    surroundSelection(json) ;

                                    addAnnotationToSidebar(json, index);

                                }catch(error){
                                    console.log(error);
                                    console.log(json);

                                }

                                });
      }
    });
}

function addAnnotationToSidebar(json, index){

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

    annotationContent = annotationContent.replace(urlRegex, " <a  href='//$1' target='_blank' >$1</a> ");

    var annoDivId = "anno-div-" + index;
    var annoTitleId = "anno-title-" + index;
    var annoContentId = "anno-content-" + index;
    var annoUpdateId = "anno-update-bttn-" + index;

    $('.annoContainer').append(
        "<div id='" + annoDivId + "' class='annoDiv'>  " +
        "<div id='" + annoTitleId + "' class='annoTitle'>" +
            "<label> " + window.getSelection() + "</label>" +
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
            "' data-selected='" + window.getSelection() +
            "' data-json='" + JSON.stringify(json) +
            "'>Update Annotation" +
        "</button>" +
        "</div>"
    );
}



function surroundSelection(json) {

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






function sendPostRequest(post_data, textAnno){
    $.ajax({
        type: "POST",
        url: annotate_remote,
        data: JSON.stringify(post_data),
        contentType: 'application/json',
        success: function (data, status) {
            console.log("ok");

            var ab2 = new AnnotationBuilder().fromJSON(JSON.stringify(textAnno));
            ab2.result.target.toSelection();

            surroundSelection(textAnno);

            if($("#submit").html() == "Update")
                showMessage("Info", "Annotation is updated successfully. ");
            else
                showMessage("Info", "Annotation is created successfully. ");

            $("#annotation-modal").modal('hide');
            //location.reload();

        },
        error: function () {
            showMessage("Error", "Errors occured while creating annoation !");
        }

    });
}

function createAnnotation() {
    var type = $("#type").val();
    var body = $("#body").val();

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
        sendPostRequest(post_data, textAnno);
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


