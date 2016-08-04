document.getElementById('upload').onclick = function () {
    var file = document.getElementById('filename').files;
    // console.log(file);

    if (file.lenght <=0) {
        return false;
    }
    var fl = new FileReader();
    var final = "";
    fl.onload = function (e) {
    // console.log(e);
        var result = JSON.parse(e.target.result);
        data = JSON.stringify(result, null, 2);
        document.getElementById('result').value = data;
        // console.log(data);
        write(result);
    };

    function write(data){
       final  = data;
        var objData = JSON.stringify(final.devDependencies);
        var arrData = objData.split(",");
        console.log(arrData);
    };




    fl.readAsText(file.item(0))
};

