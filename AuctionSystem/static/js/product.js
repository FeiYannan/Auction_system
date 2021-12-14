
function validateForm() {
  let x = document.forms["myForm"]["new_price"].value;
  let y = document.forms["myForm"]["current_price"].value;
  if (parseInt(x) <= parseInt(y)) {
    alert("Your bid price must be higher than current price.");
    return false;
  }
}
