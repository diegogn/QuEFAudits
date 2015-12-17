function do_ajax(url, data, success_f, error_f, files){
    if(files){
        $.ajax({
            url : url, // the endpoint
            type : 'POST', // http method
            data : data, // data sent with the post request
            cache: false,
            processData: false,
            contentType: false,
            // handle a successful response
            success : success_f,

            // handle a non-successful response
            error : error_f
        });
    }else{
        $.ajax({
            url : url, // the endpoint
            type : 'POST', // http method
            data : data, // data sent with the post request
            // handle a successful response
            success : success_f,

            // handle a non-successful response
            error : error_f
        });
    }
}

function success_answer(json) {
    $("*#answer_errors").remove();
    if(!json.id){
        $('#answer-form').find(':input').each(function(){
            id = $(this).prop("id");
            name = id.substring(3,id.length);
            errors = json[name];
            if(errors){
                error = errors.join();
                $("<div class='clearfix'></div><div class='alert alert-danger' id='answer_errors'><strong>"+error+"</strong></div>").insertAfter($(this).parent());
            }
        });
    }else{
        $('#answer-form')[0].reset(); // remove the value from the form
        $("#myModalFormAnswer").modal('hide');
        $('#answers').append("<div class='col-lg-12 text-center'>"+json.name+": "+json.value+"&nbsp; <a class='normal-link' href='/audits/edit/gestor/answer/"+json.id+"'> <span class='glyphicon glyphicon-pencil'></span></a> &nbsp;<a class='normal-link' href='/audits/delete/gestor/answer/"+json.id+"'> <span class='glyphicon glyphicon-remove'></span></a></div>");
        if(Cookies.get('django_language') == 'es'){
                  alert('Su respuesta ha sido creada correctamente.');
              }else{
                   alert('Your answer has been created succesfully.');
              }
        }
}

function success_doc(json) {
    $("*#document_errors").remove();
    if(!json.id){
        $('#document-form').find(':input').each(function(){
            id = $(this).prop("id");
            name = id.substring(3,id.length);
            errors = json[name];
            if(errors){
                error = errors.join();
                $("<div class='clearfix'></div><div class='alert alert-danger' id='document_errors'><strong>"+error+"</strong></div>").insertAfter($(this).parent());
            }
        });
    }else{
        $('#document-form')[0].reset(); // remove the value from the form
        $("#myModalForm").modal('hide');
        $('#documents').append("<div class='glyphicon glyphicon-book col-lg-12 text-center'>"+json.filename+"&nbsp; <a href='/audits/document/delete/"+json.id+"'>x</a></div>");
        if(Cookies.get('django_language') == 'es'){
                  alert('Su documento ha sido creado correctamente.');
              }else{
                   alert('Your document has been created succesfully.');
              }
        }
}

function error_answer(xhr,errmsg,err) {
    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
}

function load_js(id){
    $('#answer-form').on('submit', function(event){
            event.preventDefault();
            do_ajax('/audits/create/gestor/answer/'+id, {name: $('#id_name').val(), value: $('#id_value').val()}, success_answer, error_answer, false);
        });
    $('#document-form').on('submit', function(event){
        event.preventDefault();
        data = new FormData($('form')[0]);
        do_ajax('/audits/document/create/'+id, data, success_doc, error_answer, true);
    });
}

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