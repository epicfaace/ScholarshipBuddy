/* Creates an array of objects from the json entry fields,
 * then serializes it and sets the value of the associated textarea to this string.
 */
function serializeJSONFields() {
    $("form.applicationForm").find("textarea.JSONFieldValue").each(function() {
        var $textarea = $(this);
        var $table = $textarea.siblings("table.JSONFieldTable[data-name='" + $textarea.attr("name") + "']").first();
        var array = [];
        $table.find("tr").not(':first').each(function() {
            var entry = {};
            $(this).find("td").each(function() {
                var $input = $(this).find(":input:visible");
                if (!$input.length) {
                    // if it's a button td.
                    return;
                }
                var $inputVal = $input.val();
                // handle number-inputs:
                if ($input.attr('type') == 'number' && !isNaN($inputVal)) {
                    $inputVal = parseInt($inputVal);
                }
                entry[$input.attr("name")] = $inputVal;
            });
            array.push(entry);
        });
        $textarea.val(JSON.stringify(array));
    });
}

$(function() {
    // Form change script.
    $.fn.extend({
        trackChanges: function() {
          $(this).find(":input").off("change.form keyup.form")
          .on("change.form keyup.form", function() {
             $(this.form).data("changed", true);
          });
        }
        ,
        isChanged: function() { 
          return this.data("changed"); 
        }
        ,
        setChangesSaved: function() {
            $(this.form).data("changed", false);
        }
    });
    parseSchemas(true);

    $("form.applicationForm").trackChanges();

    // When all links (including button save, etc. clicked, submit the form by ajax and then redirect to appropriate url.
    $("a.pageLink, a#save").click(function(e) {
        // Disable "are you sure..." dialog
        window.onbeforeunload = function() {};

        var url = $(this).attr("href");
        var $form = $("form.applicationForm");
        $(".overlay").show();
        if (!$form.isChanged() && $(this).attr("id") != "save") {
            // If data has not changed, don't submit the form (UNLESS you're clicking the "save" button.)
            $(".overlay").removeClass("saving");
            return true;
        }
        e.preventDefault();
        serializeJSONFields();

        $form.find("input[name=redirect]").val($(this).attr("href"));
        $form.submit();
    });
    /* Confirmation before leaving.
     * Only show the dialog if data has changed.
    */
    window.onbeforeunload = function (evt) {
        if (!$("form.applicationForm").isChanged()) {
            return;
        }
        var message = 'There are unsaved changes. Are you sure you want to leave without saving?';
        if (typeof evt == 'undefined') {
            evt = window.event;
        }
        if (evt) {
            evt.returnValue = message;
        }
        return message;
    }
});