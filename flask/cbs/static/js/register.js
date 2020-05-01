function billingInfo() {
  var checkBox = document.getElementById("billing");
  var middle = document.getElementById("middle");
  var right = document.getElementById("right");
  var middleInputs = middle.getElementsByTagName("input");
  var rightInputs = right.getElementsByTagName("input");
  if (checkBox.checked == true) {
    middle.style.display = "block";
    right.style.display = "block";
    for (var i = 0; i < rightInputs.length; i++) {
      rightInputs[i].required = true;
    }
    for (var i = 0; i < middleInputs.length; i++) {
      middleInputs[i].required = true;
    }
  } else {
    middle.style.display = "none";
    right.style.display = "none";
    for (var i = 0; i < rightInputs.length; i++) {
      rightInputs[i].required = false;
    }
    for (var i = 0; i < middleInputs.length; i++) {
      middleInputs[i].required = false;
    }
  }
}
