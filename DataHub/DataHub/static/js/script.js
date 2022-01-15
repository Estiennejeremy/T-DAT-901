function changeRecommendation(selectObject){
    var value = selectObject.value;
    if (value == 1) {
        var newRecommendation = first_recommendation;
    } else if (value == 2) {
        var newRecommendation = second_recommendation;
    } else if (value == 3){
        var newRecommendation = third_recommendation;
    } else {
        var newRecommendation = fourth_recommendation;
    }

    $('#articleDiv').remove();
    $( "#recommendationDiv" ).append('<div id="articleDiv"><h4 style="color: #957DAD;">'+newRecommendation.LIBELLE+'</h6><h5>Prix moyen : '+newRecommendation.PRIX_NET+' €</h5><h6>'+newRecommendation.total+' achats par nos clients</h6><h6 style="color: #A1C9F1;">'+newRecommendation.FAMILLE+'</h6><h6 style="color: #FFABAB;">'+newRecommendation.UNIVERS+'</h6><h6 style="color: #C0DFB1;">'+newRecommendation.UNIVERS+'</h6></div>');
}

function changeDatas (selectObject) {

    let colorsFamilles = ['#a1c9f1', '#AACEF2', '#B3D3F3', '#BDD9F5', '#C6DEF6', '#D0E4F8', '#D9E9F9', '#E2EEFA', '#ECF4FC', '#F5F9FD', '#506478'];
    let colorsUnivers = ['#ffabab', '#FFB3B3', '#FFBBBB', '#FFC4C4', '#FFCCCC', '#FFD5D5', '#FFDDDD', '#FFE5E5', '#FFEEEE', '#FFF6F6', '#7F5555'];
    let colorsMailles = ['#C0DFB1', '#C6E2B8', '#CCE5C0', '#D2E8C8', '#D9EBD0', '#DFEED8', '#ECF5E7', '#ECF5E7', '#F2F8EF', '#F8FBF7', '#606F58'];

    let FamilleDatas = {
        labels: nameFamilles,
        datasets: [{
            data: countFamilles,
            backgroundColor: colorsFamilles,
            borderWidth: 1,
            borderRadius: 5,
        }]
    }
    let UniversDatas = {
        labels: nameUnivers,
        datasets: [{
            data: countUnivers,
            backgroundColor: colorsUnivers,
            borderWidth: 1,
            borderRadius: 5,
        }]
    }
    let MailleDatas = {
        labels: nameMailles,
        datasets: [{
            data: countMailles,
            backgroundColor: colorsMailles,
            borderWidth: 1,
            borderRadius: 5,
        }]
    }

    var value = selectObject.value;
    if (value == 1) {
        var newData = FamilleDatas;
    } else if (value == 2) {
        var newData = UniversDatas;
    } else {
        var newData = MailleDatas;
    }
    

    $('#myChart').remove();
    $( "#pieChartCard" ).append('<canvas id="myChart" class="mb-2" style="height: 100% !important;"></canvas>');
    const ctx = document.getElementById('myChart');

    const myChart = new Chart(ctx, {
        type: 'pie',
        data: newData,
        options: {
            responsive: false,

            plugins: {
                legend: {
                    display: true,
                    position: "right"
                }
            }
        }
    }); 


}


function main () {

    $(document).ready(function() {
        $('#myTable').DataTable({
            "order": [[ 0, "desc" ]],
            "bDestroy": true

        });
    } );


    const ctx = document.getElementById('myChart');
    const ctxLineChart = document.getElementById('myChartLineChart');
    const ctxMailleChart = document.getElementById('myChartMailles');
    var labels = ['Jan', 'Fev', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Aou', 'Sep', 'Oct', 'Nov', 'Dec']

    let object = {};
    let mailData = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

    let colorsFamilles = ['#a1c9f1', '#AACEF2', '#B3D3F3', '#BDD9F5', '#C6DEF6', '#D0E4F8', '#D9E9F9', '#E2EEFA', '#ECF4FC', '#F5F9FD', '#506478'];

    let FamilleDatas = {
        labels: nameFamilles,
        datasets: [{
            data: countFamilles,
            backgroundColor: colorsFamilles,
            borderWidth: 1,
            borderRadius: 5,
        }]
    }

    const myChart = new Chart(ctx, {
        type: 'pie',
        data: FamilleDatas,
        options: {
            responsive: false,

            plugins: {
                legend: {
                    display: true,
                    position: "right"
                }
            }
        }
    }); 

    const myChartLineChart = new Chart(ctxLineChart, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                data: priceByMonth,
                backgroundColor: [
                    'rgba(21, 119, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(21, 119, 64, 0.2)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            scales: {
                x: {
                    grid: {
                        display: false,
                    },
                },
                y: {
                    grid: {
                        display: false,
                    },
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });



    arrayObjMaillesByCli.forEach((key) => {
        object[key] = {
            "Jan": 0, "Fev": 0, "Mar": 0, "Avr": 0, "Mai": 0, "Juin": 0, "Juil": 0, "Auo": 0, "Sep": 0,
            "Oct": 0, "Nov": 0, "Dec": 0
        };
        arrayObjMaillesByMonths.index.forEach((keyb, idxb) => {
            arrayObjMaillesByMonths.data.forEach((keya, idxa) => {
                if (idxa === idxb) {
                    switch (keyb[0]) {
                        case 1:
                            if (keyb[1] == key) {
                                object[keyb[1]]["Jan"] = object[keyb[1]]["Jan"] + keya;
                            }
                            break;
                        case 2:
                            if (keyb[1] == key) {
                                object[keyb[1]]["Fev"] = object[keyb[1]]["Fev"] + keya;
                            }
                            break;
                        case 3:
                            if (keyb[1] == key)
                                object[keyb[1]]["Mar"] = object[keyb[1]]["Mar"] + keya;
                            break;
                        case 4:
                            if (keyb[1] == key) {
                                object[keyb[1]]["Avr"] = object[keyb[1]]["Avr"] + keya;
                            }
                            break;
                        case 5:
                            if (keyb[1] == key) {
                                object[keyb[1]]["Mai"] = object[keyb[1]]["Mai"] + keya;
                            }
                            break;
                        case 6:
                            if (keyb[1] == key) {
                                object[keyb[1]]["Juin"] = object[keyb[1]]["Juin"] + keya;
                            }
                            break;
                        case 7:
                            if (keyb[1] == key) {
                                object[keyb[1]]["Juil"] = object[keyb[1]]["Juil"] + keya;
                            }
                            break;
                        case 8:
                            if (keyb[1] == key) {
                                object[keyb[1]]["Aou"] = object[keyb[1]]["Aou"] + keya;
                            }
                            break;
                        case 9:
                            if (keyb[1] == key) {
                                object[keyb[1]]["Sep"] = object[keyb[1]]["Sep"] + keya;
                            }
                            break;
                        case 10:
                            if (keyb[1] == key) {
                                object[keyb[1]]["Oct"] = object[keyb[1]]["Oct"] + keya;
                            }
                            break;
                        case 11:
                            if (keyb[1] == key) {
                                object[keyb[1]]["Nov"] = object[keyb[1]]["Nov"] + keya;
                            }
                            break;
                        case 12:
                            if (keyb[1] == key) {
                                object[keyb[1]]["Dec"] = object[keyb[1]]["Dec"] + keya;
                            }
                            break;
                        default:
                            object[keyb[1]]["Dec"] = object[keyb[1]]["Dec"] + keya;
                            break;
                    }
                }
            });
        });
    });

    let datasetchartmaille = [];
    datasetchartmaille = [];

    Object.entries(object).map(([key, value]) => {
        mailData[0] = value.Jan;
        mailData[1] = value.Fev;
        mailData[2] = value.Mar;
        mailData[3] = value.Avr;
        mailData[4] = value.Mai;
        mailData[5] = value.Juin;
        mailData[6] = value.Juil;
        mailData[7] = value.Aou;
        mailData[8] = value.Sep;
        mailData[9] = value.Oct;
        mailData[10] = value.Nov;
        mailData[11] = value.Dec;

        datasetchartmaille.push({
            label: key,
            data: [mailData[0], mailData[1], mailData[2], mailData[3], mailData[4], mailData[5], mailData[6], mailData[7], mailData[8], mailData[9], 
            mailData[10], mailData[11]  ],
            backgroundColor: [
                'rgba(' + Math.floor(Math.random() * 255) +','+ Math.floor(Math.random() * 255) +',' +Math.floor(Math.random() * 255) + ', 0.2)'
            ],
            borderColor: [
                'rgba(0,0,0,0)'
            ],
            borderWidth: 1
        });
    });

    const myChartMaillesChart = new Chart(ctxMailleChart, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: datasetchartmaille
        },
        options: {
            scales: {
                x: {
                    grid: {
                        display: false,
                    },
                    stacked: true
                },
                y: {
                    grid: {
                        display: false,
                    },
                    beginAtZero: true,
                    stacked: true
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: "right",
                    labels: {
                        fontFamily: "Comic Sans MS",
                        font: 1,
                        boxWidth: 20,
                        boxHeight: 10,
                        fontSize: 5
                    }
                }
            }
        }
    });
    // myChart.canvas.parentNode.style.height = '100%';
    // myChart.parentNode.backgroundColor = 'white';
    myChart.canvas.style.height = '100%';
    // myChart.canvas.style.width = '70%';
    myChart.canvas.style.backgroundColor = '#FFF';
    myChartLineChart.canvas.style.backgroundColor = '#FFF';
    myChartMaillesChart.canvas.style.backgroundColor = '#FFF';

}