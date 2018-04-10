API_LINK = '/api';

const imageProcessor = {
    img: document.getElementById('image'),
    imgUrl: '/static/img/tmp.jpg',
    imgFolder: '/static/img/',
    video : '/video'
};

imageProcessor.takePicture  = () => {
    $.get(API_LINK + '/picture', (data) => {
        data = JSON.parse(data);
        if(data) {
            imageProcessor.processPicture();
        }
    })
};

imageProcessor.processPicture = () => {
    $.get(API_LINK + '/process', (data) => {
        console.log(data);
        if(data){
            imageProcessor.refreshView(data);
            imageProcessor.refreshPicture()
        }else {
            let alertBox = document.getElementById('alert-box');
            alertBox.style.display = 'block';
            setTimeout( () => {
                alertBox.style.display = 'None';
            }, 3000);
        }
    })
};

imageProcessor.refreshPicture = () => {
    imageProcessor.img.setAttribute('src', imageProcessor.imgUrl + '?' + Math.random())
};

imageProcessor.resetVideo = () => {
    imageProcessor.img.setAttribute('src', imageProcessor.video)
     let fullname = document.getElementById('name'),
        birthday = document.getElementById('birthday'),
        picture = document.getElementById('profile_pic'),
        company = document.getElementById('company'),
        email = document.getElementById('email');
    fullname.innerHTML = 'Jhon Due';
    birthday.innerHTML = '10/08/1987';
    email.innerHTML = 'Any Company';
    company.innerHTML = 'Jhon.due@gmail.com';
    picture.setAttribute('src', '/static/img/default.png');

};

imageProcessor.savePicture = () => {
    $.ajaxSetup({
        type: 'POST',
        timeout: 0,
        error: function(xhr) {
            console.log('Error: ' + xhr.status + ' ' + xhr.statusText)
        }
    });
    let firstName = document.getElementById('firstName').value,
        lastName = document.getElementById('lastName').value ,
        birthday = document.getElementById('birthday').value ,
        company = document.getElementById('company').value ,
        email = document.getElementById('email').value;
    console.log(firstName, lastName, birthday, company, email);
    //document.getElementById('image-form').submit();
    $.post(API_LINK + '/save', {firstName, lastName, birthday, company, email}, (data) => {
        setTimeout(() => {
            console.log('timedout')
         }, 10000);
        if(data) document.location.href = '/';
    })
};

imageProcessor.refreshView = (person) => {
    let fullname = document.getElementById('name'),
        birthday = document.getElementById('birthday'),
        picture = document.getElementById('profile_pic'),
        company = document.getElementById('company'),
        email = document.getElementById('email');
    fullname.innerHTML = person[1] + ' ' + person[2];
    birthday.innerHTML = person[3];
    email.innerHTML = person[4];
    company.innerHTML = person[5];
    picture.setAttribute('src', imageProcessor.imgFolder + person[0] + '.jpg');
};


var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the crurrent tab

function showTab(n) {
  // This function will display the specified tab of the form...
  var x = document.getElementsByClassName("tab");
  x[n].style.display = "block";
  //... and fix the Previous/Next buttons:
  if (n == 0) {
    document.getElementById("prevBtn").style.display = "none";
  } else {
    document.getElementById("prevBtn").style.display = "inline";
  }
  if (n == (x.length - 1)) {
    document.getElementById("nextBtn").innerHTML = "Submit";
  } else {
    document.getElementById("nextBtn").innerHTML = "Next";
  }
  //... and run a function that will display the correct step indicator:
  fixStepIndicator(n)
}


function nextPrev(n) {

  // This function will figure out which tab to display
  var x = document.getElementsByClassName("tab");
  // Exit the function if any field in the current tab is invalid:
  if (n == 1 && !validateForm()) return false;
  // Hide the current tab:
  x[currentTab].style.display = "none";
  // Increase or decrease the current tab by 1:
  currentTab = currentTab + n;
  // if you have reached the end of the form...
  if (currentTab >= x.length) {
    // ... the form gets submitted:
    //document.getElementById("regForm").submit();
      currentTab = currentTab - n;
      document.getElementById('register-box').style.visibility = 'visible';
    imageProcessor.savePicture();
  }
  showTab(currentTab);
  // Otherwise, display the correct tab:
}

function validateForm() {
  // This function deals with validation of the form fields
  var x, y, i, valid = true;
  x = document.getElementsByClassName("tab");
  y = x[currentTab].getElementsByTagName("input");
  // A loop that checks every input field in the current tab:
  for (i = 0; i < y.length; i++) {
    // If a field is empty...
    if (y[i].value == "") {
      // add an "invalid" class to the field:
      y[i].className += " invalid";
      // and set the current valid status to false
      valid = false;
    }
  }
  // If the valid status is true, mark the step as finished and valid:
  if (valid) {
    document.getElementsByClassName("step")[currentTab].className += " finish";
  }
  return valid; // return the valid status
}

function fixStepIndicator(n) {
  // This function removes the "active" class of all steps...
  var i, x = document.getElementsByClassName("step");
  for (i = 0; i < x.length; i++) {
    x[i].className = x[i].className.replace(" active", "");
  }
  //... and adds the "active" class on the current step:
  x[n].className += " active";
}