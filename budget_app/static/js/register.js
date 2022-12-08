console.log("register is working")

const  usernameField=document.querySelector('#usernameField')
const  emailField=document.querySelector('#emailField')
const  passwordField=document.querySelector('#passwordField')
const  showPasswordToggle=document.querySelector('.showPasswordToggle')
const  submitBtn=document.querySelector('.submit-btn')

submitBtn.disabled = true;

usernameField.addEventListener('keyup', (e)=> {
    const usernameVal = e.target.value;
    console.log('UsernameVal', usernameVal);

    if(usernameVal.length > 0)
    fetch('/authentication/validate-username', {
        body: JSON.stringify({ username: usernameVal }),
        method: "POST",
    }).then(res => res.json()).then(data => {
        console.log('data', data)
        if(data.username_error){
            submitBtn.disabled = true;
            usernameField.classList.remove('is-valid');
            usernameField.classList.add('is-invalid');
        }
        else {
            submitBtn.removeAttribute('disabled')
            usernameField.classList.remove('is-invalid');
            usernameField.classList.add('is-valid');
        }
    })
})

emailField.addEventListener('keyup', (e)=> {
    const emailVal = e.target.value;
    console.log('EmailVal', emailVal)

    if(emailVal.length > 0)
    fetch('/authentication/validate-email', {
        body: JSON.stringify({ email: emailVal }),
        method: "POST",
    }).then(res => res.json()).then(data => {
        console.log('data', data)
        if(data.email_error){
            submitBtn.disabled = true;
            emailField.classList.remove('is-valid');
            emailField.classList.add('is-invalid');
        }
        else {
            submitBtn.removeAttribute('disabled');
            emailField.classList.remove('is-invalid');
            emailField.classList.add('is-valid');
        }
    })
})

handleToggleInput = (e) => {
    if(showPasswordToggle.textContent === "SHOW"){
        showPasswordToggle.textContent = "HIDE";
        passwordField.setAttribute("type", "text")
    }
    else {
        showPasswordToggle.textContent = "SHOW";
        passwordField.setAttribute("type", "password")
    }
}
showPasswordToggle.addEventListener('click', handleToggleInput)
