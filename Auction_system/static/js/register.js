// To check a password between 7 to 16 characters which contain only characters, numeric digits, underscore and first character must be a letter

// function checkPassword(password,confirm){
//   var requirement= /^[A-Za-z]\w{7,14}$/;
//   if (password.value.match(requirement)){
//     if (password.value==confirm.value){
//       alert("OK")
//     }else{
//       alert("Two passwords not matched")
//     }
//   }else{
//     alert("Requirement not met")
//   }
// }

$('#pwdId, #cPwdId').on('keyup', function () {
       if ($('#pwdId').val() != '' && $('#cPwdId').val() != '' && $('#pwdId').val() == $('#cPwdId').val()) {
         $("#submitBtn").attr("disabled",false);
         $('#cPwdValid').show();
         $('#cPwdInvalid').hide();
         $('#cPwdValid').html('Valid').css('color', 'green');
         $('.pwds').removeClass('is-invalid')
       } else {
         $("#submitBtn").attr("disabled",true);
         $('#cPwdValid').hide();
         $('#cPwdInvalid').show();
         $('#cPwdInvalid').html('Not Matching').css('color', 'red');
         $('.pwds').addClass('is-invalid')
       }
});
