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
    <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css">



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

     <nav class="navbar navbar-default navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="/">The Game Master</a>
        </div>
        <div id="navbar" class="collapse navbar-collapse">
          <ul class="nav navbar-nav">
            <li class="active"><a href="/">Home</a></li>
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
                %for year in happenings:
                <%
                    bgcolor = {
                        'Spring': 'mistyrose',
                        'Winter': 'aliceblue',
                        'Summer': 'ivory',
                        'Fall': 'tan'
                    }

                    action_icons = {
                        'work': 'briefcase',
                        'travel': 'plane',
                        'travel_friend': 'plane',
                        'travel_enemy': 'plane',
                        'travel_free': 'plane',
                        'travel_friend_free': 'plane',
                        'travel_enemy_free': 'plane',
                        'play': 'gamepad',
                        'play_alone': 'user',
                        'love': 'heart',
                        'steal': 'money',
                        'fight': 'bomb',
                        'argue': 'exclamation',
                        'die': 'plus',
                        'cure': 'medkit',
                        'suicide': 'plus'
                    }

                    location_images = {
                        'Sydney Archology' : '/static/images/city.jpg',
                        'Luthien Prime Colony' : '/static/images/colony.jpg',
                        'Horizon RK7' : '/static/images/spaceship.jpg'
                    } 
                %>
                    %for season in year['seasons']:
                    <h3>${season['name']} of year ${year['number']}</h3>
                        %for h in season['happenings']:
                        <div class="col-sm-6 col-md-4">
                                <div class="thumbnail" style="width:30%">
                                  <img src="${h['character_img']}" alt="...">
                                </div>
                            </div>
                        <div class="panel panel-default">
                            <div class="panel-heading"><b>${h['name']} - ${h['location']}</b>
                            %if h['character'].married:
                                <b class=""> - Spouse: ${h['character'].spouse.name} </b>
                            %endif

                            <div class="pull-right">
                                    %if int(h['happiness']) >50:
                                         <i class="fa fa-smile-o fa-2x"></i>
                                    %else:
                                         <i class="fa fa-frown-o fa-2x"></i>
                                    %endif
                                </div>
                            </div>
                            <div class="panel-body">
                            
                            
                            <div class="col-md-6">
                                <p>${h['action_narrated']}</p>
                                <i class="fa fa-${action_icons[h['action']]} fa-2x"></i>
                            </div>
                            
                            <div class="col-md-2">
                            
                            <a href="#" class="thumbnail pull-right">
                              <img src="${location_images[h['location']]}" width="100px" alt="${h['location']}">
                            </a>

                            </div>
                            </div>
                        </div>
                        %endfor
                    %endfor
                %endfor

            
        </div>
        </div><!-- /.container -->
    </div>
<!-- Bootstrap core JavaScript
    ================================================== -->
<footer>
      <div class="container">
        <p class="text-muted">The Game Master</p>
      </div>
    </footer>
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="//oss.maxcdn.com/libs/jquery/1.10.2/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/js/bootstrap.min.js"></script>
  </body>
</html>