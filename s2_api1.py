#!/usr/bin/python3

print ("Content-type: text/html\r\n\r\n");

print('''
<html>

<head>

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prototype Sentinel 2 API client</title>

    <!--[if lt IE 9]>
    <p>This website requires Internet Explorer 9 or later</p>
    <![endif]-->

    <!-- Twitter Bootstrap CSS -->
    <link href="http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.1.1/css/bootstrap.css" rel="stylesheet" media="screen">
    <!-- jQuery library (necessary for Bootstrap) -->
    <script src="http://cdnjs.cloudflare.com/ajax/libs/jquery/2.0.3/jquery.min.js"></script>
    <!-- Twitter Bootstrap JavaScript -->
    <script src="http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.1.1/js/bootstrap.min.js"></script>

    <!--external stylesheet-->
    <link rel="stylesheet" type="text/css" href="/api_client.css">
   
</head>

<body> 
''')

print('''
<!-- Twitter Bootstrap RWD navbar header -->
<header id="navbar" class="navbar navbar-inverse navbar-fixed-top">
  <div class="container">
    <div class="navbar-header">
      <div class="header">
    <div class="title">
    Prototype Sentinel 2 API client
    </div>
    <div class="headerLinks">
    </div>
      </div>
      <!-- used as the toggle for collapsed navbar menu -->
      <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
    <span class="sr-only">Toggle navigation</span>
    <span class="icon-bar"></span>
    <span class="icon-bar"></span>
    <span class="icon-bar"></span>
      </button>
    </div>
    <div class="navbar-collapse collapse">
      <!-- main navbar menu -->
      <nav>
    <ul class="menu nav navbar-nav">
      <li class="first leaf"></li>
      <li class="leaf"></li>
      <li class="leaf"></li>
      <li class="leaf"></li>
      <li class="last leaf"></li>
    </ul>
      </nav>
    </div>
  </div>

</header>

<div class="container-fluid">
  <div class="row-fluid">
    <div class="span12">
      <h3>Search for packages</h3>
      <form method="post" action=""> 
    Search term: <input type="text" name="search" size="30" value="">
    <span class="error">* <?php echo $searchErr;?></span>
    <br/><br/>
    <p><span class="error">* required field</span></p>
    <br/>
    <input type="reset" value="Clear">
    <input type="submit" name="submit" value="Search">  
      </form>
    </div>
  </div>

  <!-- Footer with links to functions and options -->
  <div id="footer">
    <div id="left-footer">
      <div id="right-footer">
      </div>
    </div>
  </div>

</div>

</body>
</html>
''')