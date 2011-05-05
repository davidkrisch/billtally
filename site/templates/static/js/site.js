$(document).ready(function(){
	function hideAllVisible(blind) {
		var visible = blind? ':visible': '';
		$('#ul-daily' + visible).hide("blind");
		$('#ul-weekly' + visible).hide("blind");
		$('#ul-monthly' + visible).hide("blind");
		$('#ul-yearly' + visible).hide("blind");
	}
  // Hide the Recurrence parts of the form
  $('#ul-freq').hide();
	hideAllVisible(false);
	
  $("#id_does_repeat").change(function() {
 	 if(this.checked) {
 		$("#ul-freq").show("blind");
 	 } else {
 		$("#ul-freq").hide("blind")
		hideAllVisible(true);
 	 }
  });
  $('#id_repeats').change(function() {
		hideAllVisible(true);
		var selected = $('#id_repeats').val();
		$('#ul-' + selected).show('blind');
  });

	// Create the date picker
  $('#id_date').datepicker({altFormat: 'yyyy-mm-dd'});
});
