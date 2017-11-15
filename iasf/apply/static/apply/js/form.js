/* Parses the schemas for the json fields from json,
 * then renders the appropriate input text boxes.
 */
function parseSchemas() {
    try {
        var schemas = JSON.parse(document.getElementById("JSONListFieldSchemas").innerHTML.trim());
        for (var inputName in schemas) {
            $("form.applicationForm").find("textarea[name='"+inputName+"']").each(function() {
                var $textarea = $(this).hide().addClass("JSONFieldValue");
                var properties = schemas[inputName].items.properties;
                var propertyOrder = schemas[inputName].items.order; // this is the list of keys in properties that should be enumerated through.
                var tableHeadRow = "<tr>";
                var tableBodyRow = "<tr>";
                console.log(propertyOrder);
                for (var i in propertyOrder) {
                    var property = propertyOrder[i];
                    console.log(property);
                    var propertyTitle = (properties[property].title ? properties[property].title: property); // If "title" attribute of object is defined, let the title be this.
                    tableHeadRow += "<th>" + propertyTitle + "</th>";
                    var input = createInput(properties[property].type, properties[property].format, property);
                    tableBodyRow += "<td>" + input + "</td>";
                }
                tableBodyRow += '<td><button type="button" class="btn btn-sm btn-danger deleteRowButton" aria-label="Left Align"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></button></td>';
                tableHeadRow += "</tr>";
                tableBodyRow += "</tr>";
                addRowButton = '<button type="button" class="btn btn-sm btn-default addRowButton" aria-label="Left Align"><span class="glyphicon glyphicon-plus" aria-hidden="true"></span> Add another</button>';
                var $table = $("<table class=JSONFieldTable data-name='"+inputName+"'>" + tableHeadRow + "</table>");
                $table.insertAfter($textarea);
                $addRowButton = $(addRowButton);
                $addRowButton.insertAfter($table).click(function() {
                    addNewRow(tableBodyRow, $table);
                });

                // Loads current data into the table.
                try {
                    var currentData = JSON.parse($textarea.val());
                    if (!currentData) throw "no data";
                    var $tableHeadRow = $table.find("tr").first();
                    for (var i in currentData) {
                        $addRowButton.click();
                        var $finalRow = $table.find("tr").last();
                        for (var key in currentData[i]) {
                            var value = currentData[i][key];
                            $finalRow.find(":input:visible[name='" + key + "']").val(value);
                        }
                    }
                }
                catch (e) {
                    // No data should be loaded, so just add an empty row for now.
                    $addRowButton.click();
                }
            }); // end of each
        }
    }
    catch (e) {
        console.error(e);
        alert("An error occurred loading the form. Please contact us about the issue and/or try again later.");
    }
}
/* Gets input type; i.e., "text" for type "string" in schema,
 * "number" for type "integer".
 */
function getInputTypeFromSchema(inputType) {
    console.log(inputType);
    switch (inputType) {
        case "integer":
            return "number";
        case "string":
            return "text";
    }
    return "text";
}
/* Creates input HTML based on input format and name.
 */
function createInput(type, format, name) {
    if (format) type = format; // if format is there, override the type.
    switch (type) {
        case "textarea":
            return "<textarea class='form-control form-control-sm' name='"+ name +"'></textarea>";
        case "integer":
            return "<input type=number class='form-control form-control-sm' name='"+ name +"'>";
        case "string":
        default:
            return "<input type=text class='form-control form-control-sm' name='"+ name +"'>";
    }
    
}


function addNewRow(tableBodyRow, $table) {
    // Event handler for clicking on the "Add New" button.
    // Also attaches delete row event handler to "delete row" button.
    var $row = $(tableBodyRow);
    $row.appendTo($table);
    $row.find(".deleteRowButton").click(function() {
        $(this).closest("tr").remove();
    });
}
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
          $(":input",this).change(function() {
             $(this.form).data("changed", true);
          });
        }
        ,
        isChanged: function() { 
          return this.data("changed"); 
        }
    });
    $("form.applicationForm").trackChanges();

    parseSchemas();

    // When all links (including button save, etc. clicked, submit the form by ajax and then redirect to appropriate url.
    $("a.pageLink, a").click(function(e) {
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
        if ($form.attr("data-shouldSubmitAjax") == "false") {
            // For file upload fields -- can't submit files over ajax, so just submit normally.
            $form.submit();
            return;
        }

        $.post("", $form.serialize()).success(function(data) {
            window.location.href = url;
        }).fail(function(xhr) {
            var errorDialogText = "There was an error saving your data. Please fix the errors and try again.";
            errorDialogText += "<br><br>";
            try {
                var errors = JSON.parse(xhr.responseText);
                console.log(errors);
                $addRowButton.find(":input").popover('hide');
                for (var inputName in errors) {
                    var message = errors[inputName].join(", ");
                    errorDialogText += "<span class=errorTextDialog>" + inputName + ": </span>";
                    errorDialogText += "<span class=errorMessageDialog>" + message + "</span>";
                    errorDialogText += "<br>";
                    $form.find(":input:visible[name='" + inputName + "'], table:visible[data-name='" + inputName + "']").popover({title: "Error", content: message}).popover('show');
                }
            }
            catch (e) {
                // JSON error not parsed successfully.
                console.error(e);
                errorDialogText += "Error could not be parsed.<br>" + xhr.responseText;
            }

            var $modal = $(".modalError");
            $modal.find(".modal-body").html(errorDialogText);
            $modal.modal();
            $(".overlay").hide();
        });
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