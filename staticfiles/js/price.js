
function calculatePrice() {
  var service = document.getElementById("service").value;
  var pages = document.getElementById("pages").value;
  var level = document.getElementById("level").value;
  var price = 0;
  
  if (service == "high") {
    price = 10.99 * pages;
  } else if (service == "freshman") {
    price = 10.99 * pages;
  } else if (service == "sophomore") {
    price = 12.99 * pages;
  } else if (service == "junior") {
    price = 12.99 * pages;
  } else if (service == "senior") {
    price = 13.99 * pages;
  } else if (service == "masters") {
    price = 13.99 * pages;
  } else if (service == "doctoral") {
    price = 15.99 * pages;
  }

  if (level == "standard") {
    price = 2 + price;
  } else if (level == "premium") {
    price = 5 + price;
  } else if (level == "platinum") {
    price = 7 + price;
  }
  document.getElementById("price").innerHTML = price.toFixed(2);
}