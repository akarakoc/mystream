
$(function () {
  $('[data-toggle="popover"]').popover()
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

    highlightCurrentAnnotations();

/*******************************************/
/*  Annotation Submit
/*******************************************/
   $("#annotation-modal-form").submit(function(event){
        event.preventDefault();
		createAnnotation();
		return false;
	});


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

/*******************************************/
/*  Annotation Functions
/*******************************************/
function highlightCurrentAnnotations(){
    $.ajax({
      url: search_remote,
      data: { source : window.location.href },
      contentType: 'application/json',
      success: function(data, status){
          console.log("okk");
          var jsonList = data.response.annoList;
          jsonList.forEach(function (json, index){
                                   var ab2 = new AnnotationBuilder().fromJSON(JSON.stringify(json));
                                   ab2.result.target.toSelection();
                                   surroundSelection(json) ;
                                });
      }
    });
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
        span.style.background = "#FFFF00";

        var a = document.createElement('a');
        a.target = "_blank";
        a.style.background = "yellow";

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


    var contentHTMLText =   "<div>" +
                            "The word " + window.getSelection() + " is linked with a " + body.type +
                            " <a href='" + body.related + "' target='_blank' > Go to Annotation </a> " +
                            " <a class='updateAnnotation' data-body='" + body.related + "' data-type='" + body.type + "'   href='#'  > </a> " +
                            " <button type='button' class='btn btn-warning updateAnnotation'" +
                                "data-body='" + body.related +
                                "' data-type='" + body.type +
                                "' data-selected='" + window.getSelection() +
                                "' data-json='" + JSON.stringify(json) +
                                "'>Update Annotation</button>\n"
                            "</div>";

    $(a).popover({delay: { "show": 100, "hide": 1000 }, trigger: 'hover', sanitize:false, content: contentHTMLText});
    $(document).on('click', ".updateAnnotation", function() {
        $("#target").val($(this).data("selected"));
        $("#body").val($(this).data("body"));
        $("#type").val($(this).data("type"));
        $("#jsonAnnotation").val(JSON.stringify($(this).data("json")));

        // changes for update
        $("#modalLongTitle").html("Update Annotation");
        $("#submit").html("Update");

        $("#annotation-modal").modal();
      });



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
            location.reload();

            surroundSelection(textAnno);
            alert("completed");
        },
        error: function () {
            alert("Error");
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
        if( type == "Text" ){
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

