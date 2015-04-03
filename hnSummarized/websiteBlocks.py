"""
Author: Nicholas Rutherford
"""

HEADER = """
<!DOCTYPE html>
<html lang="en">

<head>
  <title>HN Summarized</title>
  <meta name="keywords" content="Hacker News Summarized, HN-sum">
  <meta name="description" content="A summarized version of Hacker News">
  <meta name="author" content="Nicholas Rutherford">
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
  <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>
  <link rel="stylesheet" type="text/css" href="custom.css">
</head>

<body>
<div class="container-fluid">
<span id="forkongithub"><a href="https://github.com/nicholasRutherford/HN-sum">Fork me on GitHub</a></span>
<div class="jumbotron">
    <h1 class="text-center">HN Summarized</h1>
</div>
</div>
<div class="container">
"""

ROW = '<div class="row">'
ROW_END = "</div>\n"

ELEMENT = """
    <div class="col-sm-6">
        <div class="container-fluid">
            <h3 class="text-center">{0}</h3>
            <h3 class="text-center"><small>{1}</small></h3>
            <blockquote>
                <p>
                    {2}
                </p>
                <footer>
                    <a href ="{3}">Article</a> | <a href="{4}">HN Comments</a>
                </footer>
            </blockquote>
        </div>
    </div>
"""

DATE = """
<div class="=container-fluid">
    <div class="text-center">
        <h2>{0}</h2>
    </div>
</div>
"""

PAGER = """
<ul class="pager">
  <li><a href="{0}">Newer</a></li>
  <li><a href="{1}">Older</a></li>
</ul>
"""
PAGER_INDEX = """
<ul class="pager">
  <li><a href="{0}">Older</a></li>
</ul>
"""

PAGER_END = """
<ul class="pager">
  <li><a href="{0}">Newer</a></li>
</ul>
"""

FOOTER = """
<div class="jumbotron">
    <p class="text-center"><a href="about.html">About this website.</a></p>
</div>

</div>
</body>
</html>
"""
