const startdate = document.getElementById("startdate");
const enddate = document.getElementById("enddate");
const range = document.getElementById("range");

     $(document).ready(function(){
         $('#startdate').datepicker({
             format: "dd/mm/yyyy",
                 language: "th",
                 todayBtn: "linked",
                 autoclose: true,
                 clearBtn:true,
                 todayHighlight:true
         })
         .on("changeDate", function (e) {
             var minDate = new Date(e.date.valueOf());
             $('#end').datepicker("setStartDate", minDate);
         });

         $('#enddate').datepicker({
             format: "dd/mm/yyyy",
             language: "th",
             autoclose: true,
             clearBtn:true,
         });
         $('#range').click(function(){
             var startdate = $('#startdate').val();
             var enddate = $('#enddate').val();
             alert("วันที่เริ่มต้น: " + startdate + ", วันที่สิ้นสุด: " + enddate);
             page = location.pathname.split('/')[2]
            //   console.log(typeof page)
             if(startdate != '' && enddate != '')
             {
                 $.ajax({
                     url:'/range/'+page,
                     method:'POST',
                     data:{startdate:startdate, enddate:enddate},
                     success:function(data)
                     {
                         $('#result_data').html(data);
                         // $('#table_data').append(data.htmlresponse);
                     }
                 });
             }
             else
             {
                 alert("Please Select the Date");
             }
             // alert(enddate);
         });
     });


