$("#ing-form").submit(function(e) {

    var url = "http://frenetic.pythonanywhere.com/parse"; // the script where you handle the form input.

    $.ajax({
        type: "GET",
        url: url,
        data: $("#ing-form").serialize(), // serializes the form's elements.
        contentType: 'text/plain',
        xhrFields: {
            withCredentials: false
        },
        success: function(data){
            var result = "<div class=\"inner-result\">";
            data.forEach(function(d){
                var token = d[0];
                var cat = d[2];
                console.log(token, cat);
                result += "<a class=\"" + cat + "\">" + token + "</a>";
            });
            result += "</div>";
            $('#result').html(result);
            $('#result').show();
        }
    });

    e.preventDefault(); // avoid to execute the actual submit of the form.
});