/*
 var oTable;
 var selected = new Array();


 $(function () {
 $(".load").click(function () {
 $("form").submit();
 alert(selected);
 return false;
 });
 });




 $(document).ready(function () {
 oTable= $('#vulns_table').DataTable();

 $(".nRow").click(function () {
 var iPos = oTable.fnGetPosition(".nRow");
 var aData = oTable.fnGetData(iPos);
 var iId = aData[0];
 if (jQuery.inArray(iId, selected) == -1) {
 selected[selected.length++] = iId;
 }
 else {
 selected = jQuery.grep(selected, function (value) {
 return value != iId;
 });
 }

 $(".nRow").toggleClass('row_selected');
 });
 })



 var s
 $(document).ready(function() {selectedIDs
 var table = $('#vulns_table').DataTable();

 $('#vulns_table tbody').on( 'click', 'tr', function () {
 $(this).toggleClass('selected');
 } );

 $('.load').click( function () {
 var selected = table.cell('.selected',0)

 console.log (selected.data())
 s =  selected
 //alert( table.rows('.selected').data().id() );
 } );
 } );

 */

var oTable;
var selectedIDs = new Array();

$(document).ready(function () {
    /* Add a click handler to the rows - this could be used as a callback */
    $("#vulns_table_selection tbody tr").click(function (e) {
        span = $(this).children(".selection_item").first().children("span");
        if ($(this).hasClass('selected')) {
            $(this).removeClass('!important selected ');
            if (span.hasClass('glyphicon-chevron-right')) {
                span.removeClass('glyphicon-chevron-right');
                span.addClass('glyphicon-unchecked');
            }
        }
        else {
            oTable.$('tr.selected')//.removeClass('row_selected');
            $(this).addClass('selected');
            if (span.hasClass('glyphicon-unchecked')) {
                span.removeClass('glyphicon-unchecked');
                span.addClass('glyphicon-chevron-right');
            }
        }
    });


    /* Init the table */
    oTable = $('#vulns_table_selection').dataTable();


    /* Get the rows which are currently selected */
    function fnGetSelected(oTableLocal) {
        return oTableLocal.$('tr.selected');
    }

    /* Add a click handler for the load row */
    $('.load').click(function () {
        var anSelected = fnGetSelected(oTable);
        // console.log (oTable);
        // console.log(anSelected);
        selectedIDs = new Array();
        $(anSelected).each(function () {
            selectedIDs.push($(this).find("td:first").next().find("a").html());
        });
        selectedIDs.join(',')
        //console.log ( selectedIDs);
        $("input[name='ids']").val("");
        $("input[name='ids']").val(selectedIDs);
        $("form").submit();
    });


})

