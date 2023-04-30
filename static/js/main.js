function changeImage(){
    var images = 
    ["{{ url_for('static', filename='images/1.jpg')}}", "{{ url_for('static', filename='images/2.jpg')}}", 
    "{{ url_for('static', filename='images/3.jpg')}}", "{{ url_for('static', filename='images/4.jpg')}}", 
    "{{ url_for('static', filename='images/5.jpg')}}", "{{ url_for('static', filename='images/6.jpg')}}", 
    "{{ url_for('static', filename='images/7.jpg')}}", "{{ url_for('static', filename='images/8.jpeg')}}", 
    ]
    
    var size = images.length;
    for(let i=1;i<9;i++){
      var n = Math.floor(size*Math.random())
      document.getElementById("img"+[i]).src = images[n];
    }
}

function getImage(element){
  var name = element.src;
  document.getElementById("name").src = name;
  document.getElementById("name").scrollIntoView(true);
}

function getData(){
    // document.getElementById("question").value
    var a= 'hii';
    $.ajax({
            type: 'post',
            url: "test.py",
            data: {'param1':'abc'},
            async: false,
            success: function (response) {
                console.log(response);
            }
        }).done(function (data) {
            console.log(data);
        });
    }