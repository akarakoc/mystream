
$(  createDialog =  function() {

    var dialog, form,

      // From http://www.whatwg.org/specs/web-apps/current-work/multipage/states-of-the-type-attribute.html#e-mail-state-%28type=email%29
      uriRegex = /^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/,
      urlRegex = /((([A-Za-z]{3,9}:(?:\/\/)?)(?:[\-;:&=\+\$,\w]+@)?[A-Za-z0-9\.\-]+|(?:www\.|[\-;:&=\+\$,\w]+@)[A-Za-z0-9\.\-]+)((?:\/[\+~%\/\.\w\-_]*)?\??(?:[\-\+=&;%@\.\w_]*)#?(?:[\.\!\/\\\w]*))?)/;
      target = $( "#target" ),
      body = $( "#body" ),
      allFields = $( [] ).add( target ).add( body ),
      tips = $( ".validateTips" );

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

    function createAnnotation() {
      var valid = true;
      allFields.removeClass( "ui-state-error" );
      valid = valid && checkRegexp( body, urlRegex, "failed" );

      if ( valid ) {

         var remote ="https://mystream-anno.herokuapp.com/annoateText";
         var local = window.location.href;
         var textAnno = JSON.parse($( "#output" ).val());

         textAnno.body = [
             {
                 "type": "Text",
                 "related": $("#body").val()
             }
         ]

          var post_data = {
             textAnno
          }
          console.log(JSON.stringify(post_data));

          $.ajax({
              type: "POST",
              url: remote,
              data: JSON.stringify(post_data),
              contentType: 'application/json',
              success: function(data, status){
                  console.log("ok");

                  var ab2 = new AnnotationBuilder().fromJSON(JSON.stringify(textAnno));
                  ab2.result.target.toSelection();
                  surroundSelection(textAnno.body[0].related) ;

              }

            });


        dialog.dialog( "close" );
      }
      return valid;
    }

    dialog = $( "#dialog-form" ).dialog({
      autoOpen: false,
      height: 400,
      width: 350,
      modal: true,
      buttons: {
        "Create Annotation": createAnnotation,
        Cancel: function() {
          dialog.dialog( "close" );
        }
      },
      close: function() {
        form[ 0 ].reset();
        allFields.removeClass( "ui-state-error" );
      }
    });

    form = dialog.find( "form" ).on( "submit", function( event ) {
      event.preventDefault();
      createAnnotation();



    });

    return dialog;

  }
);

$( document ).ready(function() {

    var remote ="https://mystream-anno.herokuapp.com/searchAnnotation";

    $.ajax({
      url: remote,
	  data: {source : window.location.href},
      success: function(data, status){
          console.log("okk");
          var jsonList = data.response.annoList;
          jsonList.forEach(function (json, index){
                                   var ab2 = new AnnotationBuilder().fromJSON(JSON.stringify(json));
                                   ab2.result.target.toSelection();
                                   surroundSelection(json.body[0].related) ;
                                });

      }

    });
});

function surroundSelection(source) {
        var span = document.createElement("span");
        span.style.fontWeight = "bold";
        span.style.color = "black";
        span.style.background = "#FFFF00";
        span.title = "This is annotation for : " + source;

        var a = document.createElement('a');
        a.href = source;
        a.target = "_blank";
        a.style.background = "yellow";
        a.title = "This is annotation for : " + source;
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


$( document ).contextmenu(function(e) {
      var ab = new AnnotationBuilder().highlight();
    ab.result.target.toSelection();
    var json = ab.toJSON();
    // var ab2 = new AnnotationBuilder().fromJSON(json);
    // ab2.result.target.toSelection();

    $( "#target" ).val(ab.result.target.selector[1].exact);

    var obj = JSON.parse(json);
    var pretty = JSON.stringify(obj, undefined, 4);

    $( "#output" ).val(pretty);


    dialog = createDialog();
    dialog.dialog( "open" );

    e.preventDefault();
});


$(document).ready(function(){
$( "span" ).hover(
  function() {
   var title = $(this).attr("title");  // extracts the title using the data-title attr applied to the 'a' tag
    $('<div/>', { // creates a dynamic div element on the fly
        text: title,
        class: 'box'
    }).appendTo(this);  // append to 'a' element
  }, function() {
    $(document).find("div.box").remove(); // on hover out, finds the dynamic element and removes it.
  }
);
  });