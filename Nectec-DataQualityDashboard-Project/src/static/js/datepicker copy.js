/*{ <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.10.0/css/bootstrap-datepicker.min.css" 
integrity="sha512-34s5cpvaNG3BknEWSuOncX28vz97bRI59UnVtEEpFX536A7BtZSJHsDyFoCl8S7Dt2TPzcrCEoHBGeM4SUBDBw==" crossorigin="anonymous" referrerpolicy="no-referrer" />
<link href= 'https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/themes/ui-lightness/jquery-ui.css'rel='stylesheet'>
<link rel="stylesheet" href= "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.9.0/css/bootstrap-datepicker.min.css">

// <script src="https://code.jquery.com/jquery-3.6.1.min.js" 
// integrity= 
// "sha256-o88AwQnZB+VDvE9tvIXrMQaPlFFSUTR+nldQm1LuPXQ=" 
// crossorigin="anonymous"> 
// </script> 
// <script>
//     $(document).ready(function(){
//         $('#startdate').datepicker({
//             format: "dd/mm/yyyy",
//                 language: "th",
//                 todayBtn: "linked",
//                 autoclose: true,
//                 clearBtn:true,
//                 todayHighlight:true
//         })
//         .on("changeDate", function (e) {
//             var minDate = new Date(e.date.valueOf());
//             $('#end').datepicker("setStartDate", minDate);
//         });

//         $('#enddate').datepicker({
//             format: "dd/mm/yyyy",
//             language: "th",
//             autoclose: true,
//             clearBtn:true,
//         });
//         $('#range').click(function(){
//             var startdate = $('#startdate').val();
//             var enddate = $('#enddate').val();
//             alert("วันที่เริ่มต้น: " + startdate + ", วันที่สิ้นสุด: " + enddate);
//             page = location.pathname.split('/')[2]
//             // console.log(typeof page)
//             if(startdate != '' && enddate != '')
//             {
//                 $.ajax({
//                     url:'/range/'+page,
//                     method:'POST',
//                     data:{startdate:startdate, enddate:enddate},
//                     success:function(data)
//                     {
//                         $('#result_data').html(data);
//                         // $('#table_data').append(data.htmlresponse);
//                     }
//                 });
//             }
//             else
//             {
//                 alert("Please Select the Date");
//             }
//             // alert(enddate);
//         });
//     });
// </script>
//     <script src= 
//     "https://cdn.jsdelivr.net/npm/popper.js@1.12.9/dist/umd/popper.min.js" 
//             integrity= 
//     "sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" 
//             crossorigin="anonymous"> 
//         </script> 
//         <script src= 
//     "https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/js/bootstrap.min.js" 
//             integrity= 
//     "sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" 
//             crossorigin="anonymous"> 
//         </script> 
//         <script src= 
//     "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.9.0/js/bootstrap-datepicker.min.js"> 
//         </script> 
//         <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.10.0/locales/bootstrap-datepicker.th.min.js" 
//         integrity="sha512-cp+S0Bkyv7xKBSbmjJR0K7va0cor7vHYhETzm2Jy//ZTQDUvugH/byC4eWuTii9o5HN9msulx2zqhEXWau20Dg==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
        

// <script>
//     $(document).ready(function(){
//         $("#startdate").datepicker({
//             format: "dd/mm/yyyy",
//                 language: "th",
//                 todayBtn: "linked",
//                 autoclose: true,
//                 clearBtn:true,
//                 todayHighlight:true
//         })
//         .on("changeDate", function (e) {
//             var minDate = new Date(e.date.valueOf());
//             $('#end').datepicker("setStartDate", minDate);
//         });

//         $('#enddate')
//         .datepicker({
//             format: "dd/mm/yyyy",
//             language: "th",
//             autoclose: true,
//             clearBtn:true,
//         })
//         .on("changeDate", function (e) {
//             var maxDate = new Date(e.date.valueOf());
//             $('#start').datepicker("setEndDate", maxDate);
//         });

//         // $('#range').click(function(){
//         //     var startdate = $('#startdate').val();
//         //     var enddate = $('#enddate').val();
//         //     // if(startdate != '' && enddate != '')
//         //     // {
//         //     //     $.ajax({
//         //     //         url:'/range',
//         //     //         method:'POST',
//         //     //         data:{startdate:startdate, enddate:enddate},
//         //     //         success:function(data)
//         //     //         {
//         //     //             $('#table_data').html(data);
//         //     //             // $('#table_data').append(data.htmlresponse);
//         //     //         }
//         //     //     });
//         //     // }
//         //     // else
//         //     // {
//         //     //     alert("Please Select the Date")
//         //     // }
//         // });
//     });
// </script> -->

// <!-- PickaDate -->

// < id="date">
//     <input type="text" class="datepicker" id="datepicker" placeholder="Date">

//     <script>
//         $(document).ready(function(){
//             $('#datepicker').pickadate({
//                 max: true, //ไม่สามารถเลือกวันเดือนปี เกินวันที่ปัจจุบันได้
//                 monthsFull: ['มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน', 'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม'],
//                 monthsShort: ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.'],
//                 weekdaysFull: ['อาทิตย์', 'จันทร์', 'อังคาร', 'พุธ', 'พฤหัสบดี', 'ศุกร์', 'เสาร์'],
//                 weekdaysShort: ['อา.', 'จ.', 'อ.', 'พ.', 'พฤ.', 'ศ.', 'ส.'],
//                 today: 'วันนี้',
//                 clear: 'ลบ',
//                 format: 'dd-mm-yyyy',
//                 formatSubmit: 'dd-mm-yyyy',
//                 selectMonths: true, //เลือกเดือนได้
//                 selectYears: 5, //เลือกปีได้ 5ปี (true, ค่าเริ่มต้น 10ปี )
//                 onRender: function () {
//                     var yearDropdown = this.$root.find('.picker__select--year');
//                     if (yearDropdown.length > 0) {
//                         yearDropdown.find('option').each(function () {
//                             var westernYear = parseInt($(this).text());
//                             var buddhistYear = westernYear + 543; // แปลงเป็น พ.ศ.
//                             $(this).text(buddhistYear);
//                         });
//                     }
//                 },
//                 onClose: function () {
//                     // จัดรูปแบบค่าฟิลด์อินพุตหลังจากที่ตัวเลือกปิด
//                     var selectedDate = this.get('select', 'dd-mm-yyyy'); // รับวันที่เลือก
//                     var parts = selectedDate.split('-'); // แยกส่วนวันที่
//                     var buddhistYear = parseInt(parts[2]) + 543; // แปลงเป็น พ.ศ. (เนื่องจากค่าใน input จะยังเป็น ค.ศ. จึงต้องแปลงอีกรอบ)
//                     var formattedDate = parts[0] + '-' + parts[1] + '-' + buddhistYear; // จัดวันที่ใหม่
//                     this.$node.val(formattedDate); // อัปเดตค่าอินพุต
//                 }
//             });
//         });
//     </script> }*/
