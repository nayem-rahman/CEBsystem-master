function active(string) {
  var seat = document.getElementById(string);
  seat.classList.toggle("activeSeat");
  var ticketArea = document.getElementById("tickets");
  var seatClass = seat.classList;
  var div = document.createElement("DIV");
  var remove = document.createElement("BUTTON");
  var adult = document.createElement("BUTTON");
  var child = document.createElement("BUTTON");
  var senior = document.createElement("BUTTON");
  var span = document.createElement("SPAN");
  var icon = document.createElement("I");

  if (seatClass.contains("activeSeat") == true) {
    div.classList.add("ticket");
    div.classList.add("row");
    div.classList.add("mb-3");
    div.id = "ticket " + string;

    icon.classList.add("fas");
    icon.classList.add("fa-minus");
    remove.appendChild(icon);

    remove.classList.add("removeButton");
    remove.classList.add("col-1");
    remove.classList.add("pt-1");
    remove.setAttribute("type", "button");
    remove.setAttribute("name", string);
    remove.setAttribute("onClick", "removeB(this)");
    div.appendChild(remove);

    span.classList.add("col-4");
    span.classList.add("pt-1");
    span.innerHTML = string;
    div.appendChild(span);

    adult.classList.add("ticketType");
    adult.classList.add("col-2");
    adult.setAttribute("type", "button");
    adult.setAttribute("name", "adult");
    adult.setAttribute("id", "adult");
    adult.setAttribute("onClick", "chooseType(this)");
    adult.innerHTML = "Adult";
    div.appendChild(adult);

    child.classList.add("ticketType");
    child.classList.add("col-2");
    child.setAttribute("type", "button");
    child.setAttribute("name", "child");
    child.setAttribute("id", "child");
    child.setAttribute("onClick", "chooseType(this)");
    child.innerHTML = "Child";
    div.appendChild(child);

    senior.classList.add("ticketType");
    senior.classList.add("col-2");
    senior.setAttribute("type", "button");
    senior.setAttribute("name", "senior");
    senior.setAttribute("id", "senior");
    senior.setAttribute("onClick", "chooseType(this)");
    senior.innerHTML = "Senior";
    div.appendChild(senior);

    ticketArea.appendChild(div);
  } else {
    ticketArea.removeChild(document.getElementById("ticket " + string));
  }
}

function chooseType(x) {
  var type = x.id;
  var parent = x.parentNode;
  var parentID = parent.id;
  var adult = parent.querySelector("#adult");
  var child = parent.querySelector("#child");
  var senior = parent.querySelector("#senior");

  if (type == adult.id) {
    adult.classList.add("activePrice");
    child.classList.remove("activePrice");
    senior.classList.remove("activePrice");
  } else if (type == child.id) {
    adult.classList.remove("activePrice");
    child.classList.add("activePrice");
    senior.classList.remove("activePrice");
  } else if (type == senior.id) {
    adult.classList.remove("activePrice");
    child.classList.remove("activePrice");
    senior.classList.add("activePrice");
  }
}


function removeB(y) {
  var id = y.name;
  var ticketArea = document.getElementById("tickets");
  ticketArea.removeChild(document.getElementById("ticket " + id));
  seat = document.getElementById(id);
  seat.classList.toggle("activeSeat");

}
