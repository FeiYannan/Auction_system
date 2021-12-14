let customer = document.getElementById('customer');
let admin = document.getElementById('admin');
let register = document.getElementById('formFooter');
let cus_login = document.getElementById('cus_login');
let admin_login = document.getElementById('admin_login');

admin.addEventListener("input",()=>{
if (admin.checked)
  register.style.visibility="hidden";
  admin_login.style.display="block";
  cus_login.style.display="none";
})
customer.addEventListener("input",()=>{
if (customer.checked)
  register.style.visibility="visible";
  cus_login.style.display="block";
  admin_login.style.display="none";
})
