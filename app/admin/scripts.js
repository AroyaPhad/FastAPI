// '.tbl-content' consumed little space for vertical scrollbar, scrollbar width depend on browser/os/platfrom. Here calculate the scollbar width .
$(window).on("load resize ", function () {
    var scrollWidth = $('.tbl-content').width() - $('.tbl-content table').width();
    $('.tbl-header').css({ 'padding-right': scrollWidth });
}).resize();

var BE_URL = "http://localhost:8080/api/v1"

function getStudents() {
    fetch(`${BE_URL}/student`)
    .then(res => res.json())
    .then(data => {
        if (data.data.length > 0) {
            var temp = "";
            data.data.forEach((itemData) => {
                temp += "<tr>";
                temp += "<td>" + itemData.created_at + "</td>";
                temp += "<td>" + itemData.student_id + "</td>";
                temp += "<td>" + itemData.name + "</td>";
                temp += "<td>" + itemData.modified_at + "</td></tr>";
            });
            document.getElementById('students').innerHTML = temp;
        }
    })
}

getStudents()