/* Parses the schemas for the json fields from json,
 * then renders the appropriate input text boxes.
 * If editing is true, we are on the application page.
 * If editing is false, we are on the review page.
 */
function parseSchemas(editing) {
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
                    addNewRow(tableBodyRow, $table, editing);
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


function addNewRow(tableBodyRow, $table, editing) {
    // Event handler for clicking on the "Add New" button.
    // Also attaches delete row event handler to "delete row" button.
    var $row = $(tableBodyRow);
    $row.appendTo($table);
    $row.find(".deleteRowButton").click(function() {
        $(this).closest("tr").remove();
    });

    if (!editing) {
        // Don't show buttons on review page.
        $row.find("button").hide();
        $(".addRowButton").hide();
        $row.find(":input").attr("disabled","disabled");
    }

    // Update to track changes, if form already has not changed.
    if (typeof $("form.applicationForm").isChanged === 'function' && !$("form.applicationForm").isChanged()) {
        $("form.applicationForm").trackChanges();
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