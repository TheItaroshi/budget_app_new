console.log("register is working")
const  usernameField=document.querySelector('#usernameField')
const  emailField=document.querySelector('#emailField')

usernameField.addEventListener('keyup', (event)=> {
    const usernameVal = event.target.value;
    console.log('UsernameVal', usernameVal)

    if(usernameVal.length > 0)
    fetch('/authentication/validate-username', {
        body: JSON.stringify({ username: usernameVal }),
        method: "POST",
    }).then(res => res.json()).then(data => {
        console.log('data', data)
        if(data.username_error){
            usernameField.classList.remove('is-valid')
            usernameField.classList.add('is-invalid')
        }
        else {
            usernameField.classList.remove('is-invalid')
            usernameField.classList.add('is-valid')
        }
    })
})

emailField.addEventListener('keyup', (event)=> {
    const emailVal = event.target.value;
    console.log('EmailVal', emailVal)

    if(emailVal.length > 0)
    fetch('/authentication/validate-email', {
        body: JSON.stringify({ email: emailVal }),
        method: "POST",
    }).then(res => res.json()).then(data => {
        console.log('data', data)
        if(data.email_error){
            emailField.classList.remove('is-valid')
            emailField.classList.add('is-invalid')
        }
        else {
            emailField.classList.remove('is-invalid')
            emailField.classList.add('is-valid')
        }
    })
})