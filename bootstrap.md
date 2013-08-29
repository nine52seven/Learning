about Bootstrap...
==============

Typeahead 输入提示
-----------------

    <html>
    <head>
        <title>test</title>
        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
        <link href="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.3.2/css/bootstrap-combined.min.css" rel="stylesheet">
        <script src="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.3.2/js/bootstrap.min.js"></script>
        <script type="text/javascript">
        $(document).ready(function() {
            $('#search').typeahead({
                source: function (query, process) {
                    return $.getJSON(
                        'https://api.github.com/users/chaing/followers',
                        {query: query},
                        function (data) {
                            states = [];
                            map = {};
                            $.each(data, function (i, state) {
                                map[state.login] = state;
                                states.push(state.login);
                            });

                            process(states);
                        })
                },
                updater: function (item) {
                    var $sel = $("#sel");
                    $sel.val(map[item].id);
                    return item;
                },
                highlighter: function (item) {
                    var regex = new RegExp( '(' + this.query + ')', 'gi' );
                    return item.replace( regex, "<strong>$1</strong>" );
                }

            });
        });
        </script>
    </head>
    <body>
    <input id="search" type="input" autocomplete="off"/>
    <input id="sel" value="" type="input" autocomplete="off"/>
    </body>
    </html>