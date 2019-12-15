from bs4 import BeautifulSoup
from peji.page import PageGenerator


class CalendarGenerator(PageGenerator):

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
    <div class="container" id="cal">
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

    <div class="container" id="footer">
    </div>
    <!-- Handlebars templates -->

    <!-- Template for head banner -->
    <script id="head-hb" type="text/x-handlebars-template">
    <div class="starter-template">
            <h1>{{title}}</h1>
            <img id="title-logo" class="head-logo" src="{{title-logo}}">
            <br><br>
            <p class="lead">{{title-lead}}</p>
    </div>
    </script>

    <!-- Template for calendar -->
    <script id="calendar-hb" type="text/x-handlebars-template">
        <div class="container col-xs-12 text-center">
            {{#if code}}
                {{{code}}}
            {{else}}
            <iframe
                src="https://calendar.google.com/calendar/embed?src={{id}}&amp;height=600&amp;wkst=1&amp;bgcolor=%23ffffff&amp;ctz={{timezone}}&amp;showTitle=1&amp;showNav=1&amp;title=Schedule"
                style="border:solid 1px #777" width="800" height="600" frameborder="0" scrolling="no"></iframe>
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

.head-logo {
    width: 170px;
    max-height: 170px;
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

      // Calendar
      var calTemplate = $("#calendar-hb").html()
      var calTemplateScript = Handlebars.compile(calTemplate)
      calHtml = calTemplateScript(data["calendar"])
      $("#cal").append(calHtml)

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
