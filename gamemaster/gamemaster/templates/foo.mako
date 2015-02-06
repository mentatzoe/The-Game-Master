<!DOCTYPE html>
<html lang="${request.locale_name}">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="pyramid web application">
    <meta name="author" content="Pylons Project">
    <link rel="shortcut icon" href="${request.static_url('gamemaster:static/pyramid-16x16.png')}">

    <title>Alchemy Scaffold for The Pyramid Web Framework</title>

    <!-- Bootstrap core CSS -->
    <link href="//oss.maxcdn.com/libs/twitter-bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet">

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
    ${error}
    <table style="width: 100%">
            <tr>
                    <th>Name</th>
                    <th>Age</th>
                    <th>Gender</th>
                    <th>Location</th>
                    <th>Profession</th>
                    <th>Happiness</th>
                    <th>Resources</th>
                    <th>Health</th>
                    <th>Social need</th>
                    <th>Greedy</th>
                    <th>Favorite person</th>
            </tr>
    % for f in foo:
            <tr>
                <td>${f.name}</td>
                <td>${f.age}</td>
                <td>${f.gender}</td>
                <td>${f.location.name}</td>
                <td>${f.profession}</td>
                <td>${f.happiness}</td>
                <td>${f.resources}</td>
                <td>${f.health}</td>
                <td>${f.social_need}</td>
                <td>${f.is_greedy()}</td>
                <td>${foo[f.social_vector.index(min(f.social_vector))].name}
            </tr>
    % endfor 
    </table>

    <h4>Locations</h4>
    %for b in bar:
        ${b.name} - ${b.ocupation}<br/>
    %endfor

    
<!-- Bootstrap core JavaScript
    ================================================== -->

    <!-- Placed at the end of the document so the pages load faster -->
    <script src="//oss.maxcdn.com/libs/jquery/1.10.2/jquery.min.js"></script>
    <script src="//oss.maxcdn.com/libs/twitter-bootstrap/3.0.3/js/bootstrap.min.js"></script>
  </body>
</html>