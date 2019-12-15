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

    <div id="personal" class="container" >
    </div>

    <div id="social" class="container">
    </div>

<!-- Snow effect - temporary -->
<div class="snowflakes" aria-hidden="true">
    <div class="snowflake">
        ❅
    </div>
    <div class="snowflake">
        ❅
    </div>
    <div class="snowflake">
        ❆
    </div>
    <div class="snowflake">
        ❄
    </div>
    <div class="snowflake">
        ❅
    </div>
    <div class="snowflake">
        ❆
    </div>
    <div class="snowflake">
        ❄
    </div>
    <div class="snowflake">
        ❅
    </div>
    <div class="snowflake">
        ❆
    </div>
    <div class="snowflake">
        ❄
    </div>
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

    <!-- Template for personal links -->
    <script id="personal-hb" type="text/x-handlebars-template">
        <div class="container social">
            {{#if items.length}}
            <h4>{{title}}</h4>
            <div class="row justify-content-center">
                {{#each items}}
                <div class="col-sm-6 col-md col-lg-4">
                    <a href="{{link}}" style="color:inherit;">
                        <!-- Insert image is provided, else use the item name -->
                        {{#if image}}
                        <img src="{{image}}" class="social-logo" width="140" height="140" preserveAspectRatio="xMidYMid slice" focusable="false">
                        <p>{{name}}</p>
                        {{else}}
                        <p>{{name}}</p>
                        {{/if}}
                    </a>
                </div>
                {{/each}}
            </div>
            <hr/>
            <br>
            {{/if}}
        </div>
    </script>


    <!-- Template for social links -->
    <script id="social-hb" type="text/x-handlebars-template">
        <div class="container social">
            {{#if items.length}}
            <h4>{{title}}</h4>
            <div class="row justify-content-center">
                {{#each items}}
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
            <hr/>
            <br>
            {{/if}}
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
                    <h5 style="color:{{../footerTextHeadColor}}">{{title}}</h5>
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

.social {
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

/* Snow effect - temporary */

/* customizable snowflake styling */
.snowflake {
  color: #fff;
  font-size: 1em;
  font-family: Arial;
  text-shadow: 0 0 1px #000;
}

@-webkit-keyframes snowflakes-fall{0%{top:-10%}100%{top:100%}}@-webkit-keyframes snowflakes-shake{0%{-webkit-transform:translateX(0px);transform:translateX(0px)}50%{-webkit-transform:translateX(80px);transform:translateX(80px)}100%{-webkit-transform:translateX(0px);transform:translateX(0px)}}@keyframes snowflakes-fall{0%{top:-10%}100%{top:100%}}@keyframes snowflakes-shake{0%{transform:translateX(0px)}50%{transform:translateX(80px)}100%{transform:translateX(0px)}}.snowflake{position:fixed;top:-10%;z-index:9999;-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none;cursor:default;-webkit-animation-name:snowflakes-fall,snowflakes-shake;-webkit-animation-duration:10s,3s;-webkit-animation-timing-function:linear,ease-in-out;-webkit-animation-iteration-count:infinite,infinite;-webkit-animation-play-state:running,running;animation-name:snowflakes-fall,snowflakes-shake;animation-duration:10s,3s;animation-timing-function:linear,ease-in-out;animation-iteration-count:infinite,infinite;animation-play-state:running,running}.snowflake:nth-of-type(0){left:1%;-webkit-animation-delay:0s,0s;animation-delay:0s,0s}.snowflake:nth-of-type(1){left:10%;-webkit-animation-delay:1s,1s;animation-delay:1s,1s}.snowflake:nth-of-type(2){left:20%;-webkit-animation-delay:6s,.5s;animation-delay:6s,.5s}.snowflake:nth-of-type(3){left:30%;-webkit-animation-delay:4s,2s;animation-delay:4s,2s}.snowflake:nth-of-type(4){left:40%;-webkit-animation-delay:2s,2s;animation-delay:2s,2s}.snowflake:nth-of-type(5){left:50%;-webkit-animation-delay:8s,3s;animation-delay:8s,3s}.snowflake:nth-of-type(6){left:60%;-webkit-animation-delay:6s,2s;animation-delay:6s,2s}.snowflake:nth-of-type(7){left:70%;-webkit-animation-delay:2.5s,1s;animation-delay:2.5s,1s}.snowflake:nth-of-type(8){left:80%;-webkit-animation-delay:1s,0s;animation-delay:1s,0s}.snowflake:nth-of-type(9){left:90%;-webkit-animation-delay:3s,1.5s;animation-delay:3s,1.5s}

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

      // Personal
      var personals = data["personal"] || []
      if (personals.items.length > 0) {
        var personalTemplate = $("#personal-hb").html()
        var personalTemplateScript = Handlebars.compile(personalTemplate)
        personalHTML = personalTemplateScript(personals)
        $("#personal").append(personalHTML)
      }

      // Socials
      var socials = data["social"] || []
      if (socials.items.length > 0) {
        var socialTemplate = $("#social-hb").html()
        var socialTemplateScript = Handlebars.compile(socialTemplate)
        socialHtml = socialTemplateScript(socials)
        $("#social").append(socialHtml)
      }

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
