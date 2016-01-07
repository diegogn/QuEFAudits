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
        $("#answer_empty_text").remove();
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
        $("#file_empty_text").remove();
        $('#documents').append("<div class='glyphicon glyphicon-book col-lg-12 text-center'>"+json.filename+"&nbsp; <a href='/audits/document/delete/"+json.id+"'>x</a></div>");
        if(Cookies.get('django_language') == 'es'){
                  alert('Su documento ha sido creado correctamente.');
              }else{
                   alert('Your document has been created succesfully.');
              }
        }
}

function success_audit_delete(json) {
    if(json.delete == 'ok'){
        if(Cookies.get('django_language') == 'es'){
            alert('Su auditor\u00EDa ha sido eliminada correctamente. Seras dirigido a la lista de auditor\u00EDas');
        }else{
            alert('Your audit has been deleted succesfully. You are redirecting to list of audits');
        }
        location.href = '/audits/list/gestor/audits/';
    }else{
        if(Cookies.get('django_language') == 'es'){
            alert('No se ha podido eliminar la auditoría, su estado no es correcto.');
        }else{
            alert("Audit could not be deleted, its state is not correct.");
        }
    }
}

function success_item_delete(json) {
    if (json.message == 'ok') {
        if (Cookies.get('django_language') == 'es') {
            alert('Su \u00EDtem ha sido eliminado correctamente. Seras dirigido a la lista de items');
        } else {
            alert('Your item has been deleted succesfully. You are redirecting to list of items');
        }
        location.href = '/audits/list/gestor/items/' + json.tag;
    }
}

function success_tag_delete(json) {
    if (json.message == 'ok') {
        parent_element = $("a[name='"+json.id+"']").parent().parent();
        if(parent_element.parent().prop('class') == 'father' & parent_element.children('li').length == 1){
            parent_element.parent().prop('class','children');
        }

        $("a[name='"+json.id+"']").parent().remove();

        if (Cookies.get('django_language') == 'es') {
            alert('Su etiqueta ha sido eliminada correctamente.');
        } else {
            alert('Your tag has been deleted succesfully.');
        }
    }
}

function success_item_evaluate(json){
        if (Cookies.get('django_language') == 'es') {
            alert('Respuesta guardada correctamente.');
        } else {
            alert('Answer save correctly.');
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
    $('#delete-audit').on('click', function(event){
        event.preventDefault();
        do_ajax('/audits/delete/gestor/audit/'+id, null, success_audit_delete, error_answer, false);
    });
    $('#delete-item').on('click', function(event){
       event.preventDefault();
        do_ajax('/audits/delete/gestor/item/'+id, null, success_item_delete, error_answer, false);
    });

    $("form#result-form").each(function(){
        $(this).on("submit", function(e){
            e.preventDefault();
            data = {answer: $("input:radio:checked", this).val(), result: $(this).prop('name')};
            do_ajax('/audits/evaluate/item/', data, success_item_evaluate, error_answer, false);
        });
    });
}

function form_js(){
    $('#id_parent').on('change', function(event){
        selected = $('#id_parent').val();
        if(selected == ""){
            $('#id_public').prop('disabled', false);
        }else{
            $('#id_public').prop('checked',false);
            $('#id_public').prop('disabled', true);
        }
    });

    $('#id_parent').hover(function(event){
        if(Cookies.get('django_language') == 'en'){
            $(this).after("<p id='notice_text'>If you set a parent tag the public attribute will be the father's public attribute.</p>");
        }else{
            $(this).after("<p id='notice_text'>Si determinas una etiqueta padre el atributo p\u00FAblico ser\u00E1 el del padre.</p>");
        }
        $('#notice_text').css('color', 'red')
    }, function(){
        $('#notice_text').remove();
    });
}


function tree_js(){
    $("ul").on("click","li.father",function(e){
        e.stopPropagation();
        var style = $(this).children("ul.children").css("display");
        if(style == 'none'){
               $(this).children("ul.children").css("display",'block');
        }else{
                $(this).children("ul.children").css("display",'none');
        }
    });

    $("li.children").on("click",function(e){
        e.stopPropagation();
    });

    $("a.normal-link").on("click",function(e){
        e.stopPropagation();
    });

    $("a#stop").on("click", function(e){
        e.stopPropagation();
    });

    $("a.delete-link").each(function(){

        $(this).on("click", function(e){
            e.preventDefault();
            do_ajax('/audits/delete/gestor/tag/'+$(this).prop('name'), null, success_tag_delete, error_answer, false);
        });
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