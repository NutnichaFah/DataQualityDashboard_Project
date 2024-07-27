// Funcion to update data when select Parent
function onChange() {
  var selectedParentValue = document.getElementById("parentList").value;$('#selectedChild option').remove()
  // res:response
  $('#selectedChild').append('<option value="">เลือกหน่วยงานย่อย</option>')
  $.post('/dashboard2', {'selectedParent_id': selectedParentValue}, function(res){
      $.each(res.org_info, function(i, v){
        if(selectedParentValue != '')
          $('#selectedChild').append('<option value="'+v.org_id+'">'+v.org_title+'</option>')
          
      })

    // Update data on score card
      $('#sc_org').text(res.org_child_count)
      $('#sc_package').text(res.package_count)
      $('#sc_resource').text(res.resource_count)
      $('#machine_read').html(res.machine_readable_table)

      // Call the updateChartData_Openness function here
        updateChartData(mychartDoughnut_Openness, res.openness_group);
        updateChartData(mychartDoughnut_Downloadable, res.downloadable_group);
        updateChartData(mychartDoughnut_API, res.api_group);
        updateChartData(mychartBar_Timeliness, res.time_group);

  })
}

// Function to update data
function updateChartData(chart, data) {
  let labels = [];
  let counts = [];

  $.each(data, function(index, item) {
    labels.push(item.label);
    counts.push(item.count);
  });

  chart.data.datasets[0].data = counts;
  chart.data.labels = labels;

  chart.update(); // Redraw the chart
}

// Funcion to update data when select Child
$(document).on('change', '#selectedChild', function(){
  $.post('/dashboard3', {'sub_org_id': $(this).val()}, function(res){
    // Update data on score card
      $('#sc_org').text(res.org_count)
      $('#sc_package').text(res.package_count)
      $('#sc_resource').text(res.resource_count)
      $('#machine_read').html(res.machine_readable_table)

  // Call the updateChartData_Openness function here
    updateChartData(mychartDoughnut_Openness, res.openness_group);
    updateChartData(mychartDoughnut_Downloadable, res.downloadable_group);
    updateChartData(mychartDoughnut_API, res.api_group);
    updateChartData(mychartBar_Timeliness, res.time_group);
  })
})










// function updateChartData(data) {
//   // # 1-Openness Data
//   let openness_label = data.map(data => data.openness_label); // Extract op_score values
//   let openness_count = data.map(data => data.openness_count); // Extract op_score values
//   mychartDoughnut_Openness.data.datasets[0].data = openness_count; // Update chart dataset
//   mychartDoughnut_Openness.data.labels = openness_label; // Update chart dataset

//   mychartDoughnut_Openness.update(); // Redraw the chart
// }


// function updateChartData_Openness(data) {
//   // # 1-Openness Data
//   let openness_label = [];
//   let openness_count = [];

//   $.each(data, function(index, item) {
//     openness_label.push(item.openness_label);
//     openness_count.push(item.openness_count);
//   });

//   mychartDoughnut_Openness.data.datasets[0].data = openness_count; // Update chart dataset
//   mychartDoughnut_Openness.data.labels = openness_label; // Update chart dataset

//   mychartDoughnut_Openness.update(); // Redraw the chart
// }
