function readURL(input) {
    //  file=document.getElementById("inputFile").files[0];
    //  file_url=document.URL;
    // // file_url=URL.createObjectURL(file);
    //  $('#viewer').attr('src',file_url);
     if (input.files && input.files[0]) {
         var reader = new FileReader();

         reader.onload = function (e) {
             $('#viewer').attr('src', e.target.result);
         }

         reader.readAsDataURL(input.files[0]);
     }
 }

 $("#inputFile").change(function () {
     readURL(this);
 });
