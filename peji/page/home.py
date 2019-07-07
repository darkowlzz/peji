from bs4 import BeautifulSoup
from peji.page import PageGenerator


class HomeGenerator(PageGenerator):

    def generate_html(self, data):
        template = '''
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8" />
    <meta content="width=device-width, initial-scale=1, shrink-to-fit=no" name="viewport" />
    <!-- Bootstrap CSS -->
    <link crossorigin="anonymous" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
        integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" rel="stylesheet" />
    <!-- Handlebars -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/handlebars.js/4.1.2/handlebars.js" type="text/javascript">
    </script>
    <title>{{ title }}</title>
</head>

<body>
    <div id="head-div">
    </div>

    <div id="social" class="container">
    </div>

    <div id="footer" class="container">
    </div>

    <!-- Handlebars templates -->
    <!-- Template for head banner -->
    <script id="head-hb" type="text/x-handlebars-template">
        <div class="starter-template">
            <h1>{{title}}</h1>
            <img id="title-logo" class="head-logo" src="{{title-logo}}">
            <br><br>
            <p class="lead">{{title-lead}}</p>
            <!-- Embed periscope on-air widget only if on-air-id is set -->
            {{#if on-air-id}}
            <br><br>
            <scr{{!}}ipt>window.twttr = function (t, e, r) { var n, i = t.getElementsByTagName(e)[0], w = window.twttr || {}; return t.getElementById(r) ? w : (n = t.createElement(e), n.id = r, n.src = "https://platform.twitter.com/widgets.js", i.parentNode.insertBefore(n, i), w._e = [], w.ready = function (t) { w._e.push(t) }, w) }(document, "script", "twitter-wjs")</scr{{!}}ipt>
            <a href="https://www.periscope.tv/{{on-air-id}}" class="periscope-on-air" data-size="large">@{{on-air-id}}</a>
            <br>
            {{/if}}
        </div>
    </script>

    <!-- Template for social links -->
    <script id="social-hb" type="text/x-handlebars-template">
        <div class="container social">
            <div class="row justify-content-center">
                {{#each this}}
                <div class="col-sm-6 col-md col-lg-4">
                    <a href="{{link}}" target="_blank">
                        <!-- Insert image is provided, else use the item name -->
                        {{#if image}}
                        <img src="{{image}}" class="social-logo" width="140" height="140" preserveAspectRatio="xMidYMid slice" focusable="false">
                        {{else}}
                        <p>{{name}}</p>
                        {{/if}}
                    </a>
                </div>
                {{/each}}
            </div>
        </div>
    </script>

    <!-- Template for footer -->
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
            </div>
        </footer>
    </script>

    <!-- Load bootstrap components -->
    <script crossorigin="anonymous" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo"
        src="https://code.jquery.com/jquery-3.3.1.slim.min.js">
        </script>
    <script crossorigin="anonymous" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1"
        src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js">
        </script>
    <script crossorigin="anonymous" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM"
        src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js">
        </script>
    <link href="style.css" rel="stylesheet" />
    <script src="index.js">
    </script>
</body>

</html>
'''
        soup = BeautifulSoup(template, 'html.parser')
        soup.title.string = data['title']
        with open('public/index.html', 'w') as html_file:
            html_file.write(soup.prettify())

    def generate_css(self, data):
        template = '''
.starter-template {
  padding: 3rem 1.5rem;
  text-align: center;
}

.social .col-lg-4 {
  margin-bottom: 1.5rem;
  text-align: center;
}

.head-logo {
    width: 170px;
    max-height: 170px;
}

.social-logo {
  width: auto;
  max-height: 150px;
  margin-top: 2rem;
  margin-bottom: 2rem;
}
'''
        with open('public/style.css', 'w') as css_file:
            css_file.write(template)

    def generate_js(self, data):
        template = '''
$(document).ready(function () {

  var configURL = "config.json"

  fetch(configURL)
    .then(function (response) { return response.json(); })
    .then(function (data) {

      // Set page title.
      document.title = data["title"]

      var headTemplate = $("#head-hb").html()
      var headTemplateScript = Handlebars.compile(headTemplate)
      headHtml = headTemplateScript(data)
      $("#head-div").append(headHtml)

      $("body").css("background", data["primary-background"])
      // Set global text color.
      $("body").css("color", data["textColor"])

      // Info
      var socialTemplate = $("#social-hb").html()
      var socialTemplateScript = Handlebars.compile(socialTemplate)
      socialHtml = socialTemplateScript(data["social"])
      $("#social").append(socialHtml)

      // Footer
      var footerTemplate = $("#footer-hb").html()
      var footerTemplateScript = Handlebars.compile(footerTemplate)
      footerHtml = footerTemplateScript(data)
      $("#footer").append(footerHtml)
    });
})
'''
        with open('public/index.js', 'w') as js_file:
            js_file.write(template)
