let atualizando = false;

function number_format(number, decimals, dec_point, thousands_sep) {
    // *     example: number_format(1234.56, 2, ',', ' ');
    // *     return: '1 234,56'
    number = (number + '').replace(',', '').replace(' ', '');
    var n = !isFinite(+number) ? 0 : +number,
        prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
        sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
        dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
        s = '',
        toFixedFix = function(n, prec) {
            var k = Math.pow(10, prec);
            return '' + Math.round(n * k) / k;
        };
    // Fix for IE parseFloat(0.55).toFixed(0) = 0;
    s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
    if (s[0].length > 3) {
        s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
    }
    if ((s[1] || '').length < prec) {
        s[1] = s[1] || '';
        s[1] += new Array(prec - s[1].length + 1).join('0');
    }
    return s.join(dec);
}

async function atualizarGrafico() {
    if (atualizando)
        return;

    $("#chartContainer").html('<canvas id="myAreaChart"></canvas>');

    Swal.wait();

    try {
        const response = await fetch("/api/voo/listar?d=" + encodeURIComponent($("#selectDestino").val()))
        if (!response.ok) {
            atualizando = false;
            Swal.error("Ocorreu um erro ao atualizar o gráfico");
            return;
        }
        
        const dados = await response.json();

        atualizando = false;
        Swal.close();

        
        var ctx = document.getElementById("myAreaChart");
        var myLineChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: dados.labelsGol,
                datasets: [{
                    label: 'GOL',
                    yAxisID: 'GOL',
                    borderColor: 'rgb(252, 82, 3)',
                      backgroundColor: 'rgba(255, 159, 64, 0.2)' ,
                    data: dados.valoresGol
                    //7, 3, 13
                    // 'rgb(255, 159, 64)'
                  }, {
                    label: 'LATAM',
                    yAxisID:'GOL',
                    borderColor: 'rgb(36, 33, 148)',
                      backgroundColor: 'rgba(53, 162, 235, 0.5)',
                    data: dados.valoresLatam
                  }]
            },
        
            options: {
                maintainAspectRatio: false,
                layout: {
                    padding: {
                        left: 10,
                        right: 25,
                        top: 25,
                        bottom: 0
                    }
                },
                scales: {
                    
                    x: {
                        time: {
                            unit: 'date'
                        },
                        gridLines: {
                            display: false,
                            drawBorder: false
                        },
                        ticks: {
                            maxTicksLimit: 10
                        }
                    },
                    GOL:{							
                        position: 'left',
                        title:{
                            display:true,
                            text: 'VALOR EM REAIS'
                        }
                    },
                    //y: {
                    //	display: false, // MUDEI
                    //	ticks: {
                    //	
                    //		maxTicksLimit: 5,
                    //		padding: 10,
                    //		//callback: function(value, index, values) {
                    //		//	return 'R$' + number_format(value);
                    //		//}
                    //	},
                    //	gridLines: {
                    //		color: "rgb(234, 236, 244)",
                    //		zeroLineColor: "rgb(234, 236, 244)",
                    //		drawBorder: false,
                    //		borderDash: [2],
                    //		zeroLineBorderDash: [2]
                    //	}
                    //},
                },
                legend: {
                    display: false
                },
                tooltips: {
                    backgroundColor: "rgb(255,255,255)",
                    bodyFontColor: "#858796",
                    titleMarginBottom: 10,
                    titleFontColor: '#6e707e',
                    titleFontSize: 14,
                    borderColor: '#dddfeb',
                    borderWidth: 1,
                    xPadding: 15,
                    yPadding: 15,
                    displayColors: false,
                    intersect: false,
                    mode: 'index',
                    caretPadding: 10,
                    callbacks: {
                        label: function(tooltipItem, chart) {
                            var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
                            return datasetLabel + ': $' + number_format(tooltipItem.yLabel);
                        }
                    }
                }
            }
        });

    } catch (ex) {
        atualizando = false;
        Swal.error("Erro de rede ao atualizar o gráfico: " + ex.message);
    }
    //Swal.wait();	
}
atualizarGrafico();