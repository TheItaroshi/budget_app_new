console.log("register is working")
const  usernameField=document.querySelector('#usernameField')
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