 $(document).ready(function(){
	 $('#id_date').datepicker({altFormat: 'yyyy-mm-dd'});
   $("#id_does_repeat").change(function(event) {
		 if(this.checked) {
			$("#frequency").show("blind", {}, 500, function() {
				//$('#id_repeats')
				alert('set the selection');
			});
		 } else {
			$("#frequency").hide("blind")
		 }
   });
	 $('#id_repeats').change(function(event) {
		 alert('selected a frequency');
	 });
 });
