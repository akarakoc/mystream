
$(function () {
    $('[data-toggle="popover"]').popover();
});


function getImageXYWH(c)
{
    imageXYWH = "xywh=pixel:" + c.x + "," + c.y + "," + c.w + "," + c.h;
};

function getSelected(c){
    imageAnnotationSelected = true;
}

$( document ).ready(function() {

    $('.annotatedImage img').Jcrop({
        onChange:   getImageXYWH,
        onSelect:   getSelected
      });

    $('.annotatedImage').click(function(e) {
         imageXPath = getXpath($(this).find("img")[0]);
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
    imageXPath = "";
    numberOfAnno = 0;


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

            var ab = new AnnotationBuilder().tagging(window.location.href, imageXYWH, imageXPath);

            var json = ab.toJSON();
            console.log(json);

            var imageName = getImageName(imageXPath);

            openAnnotationModal(imageName + " " + imageXYWH , json, annoType);

    }else if ( window.getSelection() != "" ){
        var annoType = "Text";

        var ab = new AnnotationBuilder().highlight();
        ab.result.target.toSelection();
        var json = ab.toJSON();

        openAnnotationModal( ab.result.target.selector[1].exact, json, annoType );

        e.preventDefault();
    }
});

$( document ).on( "click", "div", function(e) {

    if($(this).attr("data-purpose") == "pointedAnnotation"){

        var scrollId = $(this).attr("id").replace("annoBorder","");

        if($("#annoContainer").css("display") == "none")
            $("#annoContainer").toggle('blind',1000);

        $(".annoTitle").removeClass("scrolledBorder");
        document.getElementById("annoContainer").scrollTop = $("#anno-title-" + scrollId).position().top - 100;
        $($("#anno-title-" + scrollId)[0]).addClass("scrolledBorder");

    }
});

$( document ).on( "click", ".highlightedAnnotation", function(e) {

    var scrollId = $(this).data("dataAnnoIndex");

    if($("#annoContainer").css("display") == "none")
        $("#annoContainer").toggle('blind',1000);

    $(".annoTitle").removeClass("scrolledBorder");
    document.getElementById("annoContainer").scrollTop = $("#anno-title-" + scrollId).position().top - 100;
    $($("#anno-title-" + scrollId)[0]).addClass("scrolledBorder");

});



//
// $( document ).contextmenu(function(e) {
//
//     var ab = new AnnotationBuilder().highlight();
//     ab.result.target.toSelection();
//     var json = ab.toJSON();
//
//     openAnnotationModal( ab.result.target.selector[1].exact, json );
//
//     e.preventDefault();
// });

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

    var imageAnnoList  = $("div").find("[data-purpose='pointedAnnotation']");


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


    var imageAnnoList  = $("div").find("[data-purpose='pointedAnnotation']");

    $.each(imageAnnoList, function(index, a) {
        $(a).css("display", "none");
    });
});

// $(document).on('click', ".annotationSelector", function() {
//     //$(".popover").hide();
//     var popId = $(this).attr("id");
//     openPopover(popId);
// });

function openPopover(popId){
    if($("#" + popId).hasClass("highlightedAnnotation")) {
        $("#" + popId).popover('show');
         //setTimeout(closePopover(popId), 3000);
    }
}

function closePopover(popId){
    $("#" + popId).popover('hide');
}


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

          var jsonList = data.response.annoList;
          console.log("Annotations is received successfully ! ");
          console.log(jsonList.length + " annotations are found for this page !");
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
                                         var annotation = new AnnotationBuilder().fromJSON(JSON.stringify(json));
                                         annotation.result.target.toSelection();
                                         surroundSelection(json, index) ;
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
    var numberOfAnno = index + 1;

    if($(".annoContainer").height() < 1000 )
        $(".annoContainer").css("height" , $(".annoContainer").height() + 200 );

    if(numberOfAnno == 1)
        $("#annotationCount").html("There is " + numberOfAnno + " annotation on this page");
    else
        $("#annotationCount").html("There are " + numberOfAnno + " annotations on this page");
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
        var xpath = json.target.selector[1].value;
        annoLabel = getImageName(xpath);
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
    xywh = xywh.split(",")

    var xpath = anno.target.selector[1].value;

    var imageName = getImageName(xpath);

    var left = parseInt(xywh[0]);
    var top = parseInt(xywh[1]);
    var width =  parseInt(xywh[2]);
    var height =  parseInt(xywh[3]);

    var imagePointButton = "<button data-purpose='pointedAnnotation'  id='" + annoUpdateId +
        "' data-body='" + buttonBody +
        "' data-selected='" + imageName + " " + anno.target.selector[0].value +
        "' data-type='" + body.type +
        "' data-currentSrc='" + anno.id +
        "' data-json='" + JSON.stringify(anno) +
        "' type='button' class='btn btn-warning updateImageAnnotation' style=' " +
        " display: block; " +
        " position: absolute; " +
        " z-index : 700;" +
        " height: 1.5em; " +
        " width: 1.5em; " +
        " top : " + top + "px; left :" + left + "px;" +
        "' >" +
            "<svg class='bi bi-chat-square-dots-fill' width='1em' height='1em' viewBox='0.5 0 15 15' fill='currentColor' xmlns='http://www.w3.org/2000/svg'>" +
              "<path fill-rule='evenodd' d='M0 2a2 2 0 012-2h12a2 2 0 012 2v8a2 2 0 01-2 2h-2.5a1 1 0 00-.8.4l-1.9 2.533a1 1 0 01-1.6 0L5.3 12.4a1 1 0 00-.8-.4H2a2 2 0 01-2-2V2zm5 4a1 1 0 11-2 0 1 1 0 012 0zm4 0a1 1 0 11-2 0 1 1 0 012 0zm3 1a1 1 0 100-2 1 1 0 000 2z' clip-rule='evenodd'/>" +
            "</svg>" +
        "</button>";

        var annotationBorderDiv = "<div data-purpose='pointedAnnotation'  id='annoBorder" + index + "' " +
        " name='borderDiv' " +
        " style=' " +
        " cursor : context-menu; " +
        " border-radius : 10%;" +
        " display: block; " +
        " border: #ffc107; " +
        " border-width : 3px; " +
        " border-style : dashed; " +
        " position: absolute; " +
        " opacity: 50%; " +
        " z-index : 650;" +
        " height: " + height + "px; " +
        " width: " + width + "px; " +
        " top : " + top + "px; left :" + left + "px;" +
        "' >" +
        "</div>";


    $(getComponentByXpath(xpath).parentElement).find(".jcrop-holder").append( annotationBorderDiv );
    $(getComponentByXpath(xpath).parentElement).find(".jcrop-holder").append( imagePointButton );

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

        console.log(index);
        $(a).data("dataAnnoIndex", index);

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

    // TODO :  popover is closed
    // $(a).popover({delay: { "show": 100, "hide": 1000 }, trigger: 'click', sanitize:false, content: contentHTMLText});


}






function sendPostRequest(post_data, anno, annoType){
    $.ajax({
        type: "POST",
        url: annotate_remote,
        data: JSON.stringify(post_data),
        contentType: 'application/json',
        success: function (data, status) {
            console.log("Annotation is saved successfully");

            if( annoType == "Image"){
                pointImage(anno, "none")
            }else if ( annoType == "Text"){
                var annotation = new AnnotationBuilder().fromJSON(JSON.stringify(anno));

                annotation.result.target.toSelection();
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
        numberOfAnno += 1;
        addAnnotationToSidebar(textAnno, numberOfAnno , annoType);
    }else{
        showMessage("Error", " Body must be URI to create Image or Video annotation.");
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

function findXpath(element)
{
    if (element && element.id)
        return '//*[@id="' + element.id + '"]';
    else
        return Xpath.getElementTreeXPath(element);
};

function getComponentByXpath(xpath) {
    return document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
}

function getXpath(element)
{
    var paths = [];  // Use nodeName (instead of localName)
    // so namespace prefix is included (if any).
    for (; element && element.nodeType == Node.ELEMENT_NODE;
           element = element.parentNode)
    {
        var index = 0;
        var hasFollowingSiblings = false;
        for (var sibling = element.previousSibling; sibling;
              sibling = sibling.previousSibling)
        {
            // Ignore document type declaration.
            if (sibling.nodeType == Node.DOCUMENT_TYPE_NODE)
                continue;

            if (sibling.nodeName == element.nodeName)
                ++index;
        }

        for (var sibling = element.nextSibling;
            sibling && !hasFollowingSiblings;
            sibling = sibling.nextSibling)
        {
            if (sibling.nodeName == element.nodeName)
                hasFollowingSiblings = true;
        }

        var tagName = (element.prefix ? element.prefix + ":" : "")
                          + element.localName;
        var pathIndex = (index || hasFollowingSiblings ? "["
                   + (index + 1) + "]" : "");
        paths.splice(0, 0, tagName + pathIndex);
    }

    return paths.length ? "/" + paths.join("/") : null;
};

function getImageName(xpath){
    var imageSrc = $(getComponentByXpath(xpath)).prop("currentSrc").split('/');
    if(imageSrc[imageSrc.length-1 ] == ""){
        return imageSrc[imageSrc.length-2 ];
    }
    return imageSrc[imageSrc.length-1 ];
}