     function register_teacher() {
         var passcode = prompt("Please enter teacher passcode:");
         if (passcode == 123) {
             window.open("http://127.0.0.1:5000/register_teacher", "_self")

         } else {
             alert("Passcode invalid!");
             window.open("http://127.0.0.1:5000/", "_self");
         }
     }
