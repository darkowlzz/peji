from bs4 import BeautifulSoup
from peji.page import PageGenerator


class ShopGenerator(PageGenerator):

    def generate_html(self, data):
        template = '''
<!DOCTYPE html>
<html lang="en">

<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

<!-- Bootstrap CSS -->
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
    integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">

<!-- Handlebars -->
<script type="text/javascript"
    src="https://cdnjs.cloudflare.com/ajax/libs/handlebars.js/4.1.2/handlebars.js"></script>

<title>{{ title }}</title>
</head>

<body>
<div id="jumbo-div"></div>

<!-- The picture fullscreen modal -->
<div id="myModal" class="modal">
    <span class="close">&times;</span>
    <img class="modal-content" id="img01">
    <div id="caption"></div>
</div>

<div id="listing" class="container"></div>

<div id="footer" class="container"></div>


<!-- Handlebars templates -->

<!-- Template for header jumbotron -->
<script id="jumbo-hb" type="text/x-handlebars-template">
    <div id="jumbo" class="jumbotron jumbotron-fluid text-center">
        <div class="container">
        <h1 id="title" class="display-4 text-light">{{title}}</h1>
        <img id="title-logo" class="jumbo-logo" src="{{title-logo}}">
        <p id="title-lead" class="lead text-light">{{title-lead}}</p>
        <hr class="my-4">
        <p id="title-sublead" class="text-light">{{title-sublead}}</p>
        </div>
    </div>
    </script>

<!-- Template for a category and items list -->
<script id="list-category-hb" type="text/x-handlebars-template">
    <hr class="my-4">
    <h2 id="#" class="text-center text-uppercase font-weight-bold text-dark">{{category}}</h2>
    <!-- no-gutters removes the extra space between the children elements. -->
    <div class="row no-gutters justify-content-sm-center justify-content-md-center justify-content-lg-center justify-content-xl-center">
    {{#each items}}
    <div class="col-sm-8 col-md-6 col-lg-4">
        <div class="card bg-dark mb-2 mt-2 ml-2 mr-2">
        <img src="{{image}}" class="card-img-top cover" id="{{id}}">
        <div class="card-body">
            <h5 class="card-title text-light text-center">{{title}}</h5>
            <p class="card-text text-light text-center">{{description}}</p>
            {{#if ../showPrice}}
            <p class="card-text text-light text-center">
                {{../currencySymbol}}
                {{price}}
                {{#if ../currencyName}}
                ({{../currencyName}})
                {{/if}}
            </p>
            {{/if}}
            <div class="text-center">
            {{#if available}}
            {{button}}
            {{else}}
            <p class="text-center"><span class="badge badge-light">Unavailable</span></p>
            {{/if}}
            </div>
        </div>
        <div class="card-footer">
            <small class="text-muted">{{publishDate}}</small>
        </div>
        </div>
    </div>
    {{/each}}
    </div>
    </script>

<!-- Template for site footer -->
<script id="footer-hb" type="text/x-handlebars-template">
    <footer class="pt-4 my-md-5 pt-md-5 border-top">
        <div class="row">
        <div class="col-12 col-md">
            <img class="mb-2" src="{{title-logo}}" alt="" width="24" height="24">
            <small class="d-block mb-3 text-muted">&copy; 2019</small>
        </div>
        {{#each info}}
        <div class="col-6 col-md">
            <h5>{{title}}</h5>
            <ul class="list-unstyled text-small">
            {{#each items}}
            <li><a class="text-muted" href="{{link}}" target="_blank">{{name}}</a></li>
            {{/each}}
            </ul>
        </div>
        {{/each}}
        </div>
    </footer>
    </script>

<!-- Load bootstrap components -->
<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"
    integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo"
    crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"
    integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1"
    crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"
    integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM"
    crossorigin="anonymous"></script>

<link rel="stylesheet" href="style.css">
<script src="index.js"></script>

</body>

</html>
'''
        soup = BeautifulSoup(template, 'html.parser')
        soup.title.string = data['title']
        with open('public/index.html', 'w') as html_file:
            html_file.write(soup.prettify())

    def generate_css(self, data):
        template = '''
.fw-body {
    background: whitesmoke !important;
}

.jumbo-logo {
    width: 170px;
    max-height: 170px;
}

.cover {
  object-fit: cover;
  width: auto;
  height: 225px;
}

/* Image modal */
#myImg {
  border-radius: 5px;
  cursor: pointer;
  transition: 0.3s;
}

#myImg:hover {opacity: 0.7;}

.card {
    overflow: hidden;
}

/* The Modal (background) */
.modal {
  display: none; /* Hidden by default */
  position: fixed; /* Stay in place */
  z-index: 1; /* Sit on top */
  padding-top: 100px; /* Location of the box */
  left: 0;
  top: 0;
  width: 100%; /* Full width */
  height: 100%; /* Full height */
  overflow: auto; /* Enable scroll if needed */
  background-color: rgb(0,0,0); /* Fallback color */
  background-color: rgba(0,0,0,0.9); /* Black w/ opacity */
}

/* Modal Content (image) */
.modal-content {
  margin: auto;
  display: block;
  width: 80%;
  max-width: 700px;
}

/* Caption of Modal Image */
#caption {
  margin: auto;
  display: block;
  width: 80%;
  max-width: 700px;
  text-align: center;
  color: #ccc;
  padding: 10px 0;
  height: 150px;
}

/* Add Animation */
.modal-content, #caption {
  -webkit-animation-name: zoom;
  -webkit-animation-duration: 0.6s;
  animation-name: zoom;
  animation-duration: 0.6s;
}

@-webkit-keyframes zoom {
  from {-webkit-transform:scale(0)}
  to {-webkit-transform:scale(1)}
}

@keyframes zoom {
  from {transform:scale(0)}
  to {transform:scale(1)}
}

/* The Close Button */
.close {
  position: absolute;
  top: 15px;
  right: 35px;
  color: #f1f1f1;
  font-size: 40px;
  font-weight: bold;
  transition: 0.3s;
}

.close:hover,
.close:focus {
  color: #bbb;
  text-decoration: none;
  cursor: pointer;
}

/* 100% Image Width on Smaller Screens */
@media only screen and (max-width: 700px){
  .modal-content {
    width: 100%;
  }
}
'''
        with open('public/style.css', 'w') as css_file:
            css_file.write(template)

    def generate_js(self, data):
        template = '''
$(document).ready(function () {

  var modal = document.getElementById('myModal');
  var configURL = "config.json"

  fetch(configURL)
    .then(function (response) { return response.json(); })
    .then(function (data) {

      // Set page title.
      document.title = data["title"]

      var jumboTemplate = $("#jumbo-hb").html()
      var jumboTemplateScript = Handlebars.compile(jumboTemplate)
      jumboHtml = jumboTemplateScript(data)
      $("#jumbo-div").append(jumboHtml)

      $("#jumbo").css("background", data["primary-background"])
      $("body").css("background", data["secondary-background"])

      // Footer
      var footerTemplate = $("#footer-hb").html()
      var footerTemplateScript = Handlebars.compile(footerTemplate)
      footerHtml = footerTemplateScript(data)
      $("#footer").append(footerHtml)

      // Build the body with catalog data.
      buildCatalog(data)
    });

  // Get the <span> element that closes the modal
  var span = document.getElementsByClassName("close")[0];

  // When the user clicks on <span> (x), close the modal
  span.onclick = function () {
    modal.style.display = "none";
  }
})

function buildCatalog(data) {
  var modal = document.getElementById('myModal');
  var modalImg = document.getElementById("img01");
  var captionText = document.getElementById("caption");

  // Iterate through the catalog and create entries for all the items per
  // category.
  catalog = data["catalog"]
  for (var catIndex = 0; catIndex < catalog.length; catIndex++) {
    category = catalog[catIndex]
    catDataURL = category['dataURL']

    // Fetch category data.
    fetch(catDataURL)
      .then(function (response) { return response.json(); })
      .then(function (categoryData) {
        // Add showPrice from root config to each of the category data so that
        // it can be used in the card template.
        categoryData['showPrice'] = data['showPrice']
        categoryData['currencySymbol'] = data['currencySymbol']
        categoryData['currencyName'] = data['currencyName']

        var categoryTemplate = $("#list-category-hb").html()
        var categoryTemplateScript = Handlebars.compile(categoryTemplate, { noEscape: true })
        categoryHtml = categoryTemplateScript(categoryData)
        $("#listing").append(categoryHtml)
      })
      .then(function () {
        // Add click event on all the images for preview.
        var imgs = $(".card-img-top")
        imgs.each(function () {
          $(this).click(function () {
            modal.style.display = "block"
            modalImg.src = this.src
            captionText.innerHTML = this.alt
          })
        })
      });
  }
}
'''
        with open('public/index.js', 'w') as js_file:
            js_file.write(template)
