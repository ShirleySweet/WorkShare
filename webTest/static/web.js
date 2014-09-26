var n = 0;

function newSub(id){
    $("#id_mission_id").val(id)
    show("submission")
};

function editPerson(id){
    $("input#id_id").val(id)
    $("input#id_name").val($("#"+id+"_name").text());
    $("input#id_department").val($("#"+id+"_department").text());
    $("input#id_title").val($("#"+id+"_title").text());
    $("input#id_remark").val($("#"+id+"_remark").text());
    var op = $("#"+id+"_position").text();
    $("#id_status option").each(function (){
        if($(this).text()==op){
            $(this).attr('selected',true);
        }
    });
    id = "person-update";
    document.getElementById(id).style.display = "";
};

function editSub(id,order){
    $("input#id_mission_id").val(id);
    $("input#id_name").val($("#"+id+"_name").text());
    $("input#id_mremark").val($("#"+id+"_remark").text());
    $("input#id_order").val(order);
    $("input#id_content").val($("#"+id+"_"+order+"_content").text());
    $("input#id_sremark").val($("#"+id+"_"+order+"_subremark").text());
    var op = $("#"+id+"_"+order+"_status").text();
    $("#id_status option").each(function (){
        if($(this).text()==op){
            $(this).attr('selected',true);
        }
    });
    id = "submission-update";
    document.getElementById(id).style.display = "";
};

function onSuccess(){
    alert("OK")
};

function onFail(){
    alert("Fail")
};

function show(table){
    id = table+"-hide";
    document.getElementById(id).style.display = "";
};

function hide(table){
    id = table+"-hide";
    document.getElementById(id).style.display = "none";
};

function Uhide(table){
    id = table+"-update";
    document.getElementById(id).style.display = "none";
};

function newReport(){
    ++n;
    $("#ordern").val(n);
    var ele =document.getElementById("sub_report");
    var p = document.createElement("p");
    p.className = "subre";
    var text = document.createElement("textarea");
    text.name = "text_"+n;
    var textNode = document.createTextNode('report id: '+ n+'');
    var sle = document.createElement("select");
    sle.id = "sel_"+n;
    sle.name = "mission_"+n;
    var pid = $("#name_select").val();
    getOption(pid,sle.id);
    ele.appendChild(p);
    p.appendChild(textNode);
    p.appendChild(text);
    p.appendChild(sle);
};

function deleteReport(){
    if(n==0) return;
    n--;
    var arrP = document.getElementsByClassName("subre");
    var div = document.getElementById("sub_report");
    div.removeChild(arrP[arrP.length-1]);
};

function getOption(pid,sid){
    $.ajax("/load/",{
        dateType:"json",
        type:"get",
        data:{
            "id":pid
        },
    success:function(data) {
            var myobj = eval(data);
            for(var i=0;i<myobj.length;i++){
                var op = document.createElement("option");
                op.value = myobj[i].m_id+"_"+myobj[i].m_order;
                op.text = myobj[i].content;
                document.getElementById(sid).appendChild(op);
            }
        }
    });
};

$(function() {
    $( "#datepicker" ).datepicker({ dateFormat: "yy-mm-dd" });
  });
