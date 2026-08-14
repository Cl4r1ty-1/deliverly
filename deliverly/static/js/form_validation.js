// bootstrap custom style form validation
// source + credit: https://getbootstrap.com/docs/5.0/forms/validation/#custom-styles

// Code licenced under: https://github.com/twbs/bootstrap/blob/main/LICENSE
// Docs licenced under: https://creativecommons.org/licenses/by/3.0/

// Example starter JavaScript for disabling form submissions if there are invalid fields
(function () {
  'use strict'

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  var forms = document.querySelectorAll('.needs-validation')

  // Loop over them and prevent submission
  Array.prototype.slice.call(forms)
    .forEach(function (form) {
      form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }

        form.classList.add('was-validated')
      }, false)
    })
})()