function hide(fields){
    $.each(fields, function(val,e){
        a = $("#id_"+e).parent().parent();
        a.val("");
        a.css("display",'none');
        a.insertBefore($("div.col-lg-12").last());
    });
}

function show(fields, bool){
    $.each(fields,function(cont,val){
                   a = $("#id_"+val);
                   if(bool == true){a.val("");}
                   a.parent().parent().css("display",'block');
               });
}


$(document).ready(function(){
    fields = ["freq","interval","count","byday","bymonth","bymonthday","wkst","byyearday","bysetpos"];

    $.each(fields, function(val,e){
        $("#id_"+e).parent().parent().insertBefore($("div.col-lg-12").last());
    });

    if($("#id_period").val() == '4'){
        show(fields, false);
    }else{
        hide(fields);
    }
   $('#id_period').on("change", function(){
       switch($('#id_period').val()){
           case "0":
               hide(fields);
           case "1":
               hide(fields);
               $("#id_freq").val("WEAKLY");
               $("#id_interval").val("");
               $("#id_count").val("");
               $("#id_byday").val("");
               $("#id_bymonth").val("");
               $("#id_bymonthday").val("");
               $("#id_wkst").val("");
               $("#id_byyearday").val("");
               $("#id_bysetpos").val("");
               break;

           case "2":
               hide(fields);
               $("#id_freq").val("MONTHLY");
               $("#id_interval").val("");
               $("#id_count").val("");
               $("#id_byday").val("");
               $("#id_bymonth").val("");
               $("#id_bymonthday").val("");
               $("#id_wkst").val("");
               $("#id_byyearday").val("");
               $("#id_bysetpos").val("");
               break;

           case "3":
               hide(fields);
               $("#id_freq").val("YEARLY");
               $("#id_interval").val("");
               $("#id_count").val("");
               $("#id_byday").val("");
               $("#id_bymonth").val("");
               $("#id_bymonthday").val("");
               $("#id_wkst").val("");
               $("#id_byyearday").val("");
               $("#id_bysetpos").val("");
               break;

           case "4":
               show(fields, true);
               break;
       }
   });
});