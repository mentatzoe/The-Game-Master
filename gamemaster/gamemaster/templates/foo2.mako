<!DOCTYPE html>
<html lang="${request.locale_name}">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="pyramid web application">
    <meta name="author" content="Pylons Project">
    <link rel="shortcut icon" href="${request.static_url('gamemaster:static/pyramid-16x16.png')}">

    <title>The Game Master</title>

    <!-- Bootstrap core CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap-theme.min.css">
    <!-- Custom styles for this scaffold -->
    <link href="${request.static_url('gamemaster:static/theme.css')}" rel="stylesheet">



    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="//oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="//oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>
    <![endif]-->
    <style>
        th {
            padding: 10px;
        }
        tr {padding: 10 px 20px;}
    </style>
  </head>

  <body>

     <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">The Game Master</a>
        </div>
        <div id="navbar" class="collapse navbar-collapse">
          <ul class="nav navbar-nav">
            <li class="active"><a href="#">Home</a></li>
            <li><a href="#about">About</a></li>
            <li><a href="#contact">Contact</a></li>
          </ul>
        </div><!--/.nav-collapse -->
      </div>
    </nav>

    <div class="container">

        <div class="starter-template" style="margin-top:100px">
            <h1>Story development</h1>
            <br/>
            <br/>
            <div class="row">
                %for h in happenings:
                <div class="col-sm-6 col-md-4">
                        <div class="thumbnail" style="width:30%">
                          <img src="${h['character_img']}" alt="...">
                        </div>
                    </div>
                <div class="panel panel-default">
                    <div class="panel-heading"><b>${h['name']} - ${h['location']}</b>
                    %if h['character'].married:
                        <b class="pull-right">Spouse: ${h['character'].spouse.name}</b>
                    %endif
                    </div>
                    <div class="panel-body">
                    
                    <div class="col-md-8">
                        <h4>Year ${h['year']} - ${h['season']}</h4>
                        <p>${h['action_narrated']}</p>
                    </div>
                    </div>
                </div>
                %endfor

            
        </div>
    </div><!-- /.container -->
<!-- Bootstrap core JavaScript
    ================================================== -->
<footer class="footer">
      <div class="container">
        <p class="text-muted">The Game Master</p>
      </div>
    </footer>
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="//oss.maxcdn.com/libs/jquery/1.10.2/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/js/bootstrap.min.js"></script>
  </body>
</html>