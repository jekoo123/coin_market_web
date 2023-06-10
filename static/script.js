function handle_money() {
  const form = document.getElementById('money_form');
  const button = document.querySelector('.handle_money_button');
  if (form.style.display === 'none') {
    form.style.display = 'block';
    button.textContent = 'Close';
    button.style.width = '50px';
    button.style.height = '30px';
    button.style.position = 'relative';
    button.style.bottom = '45px';
    button.style.left='175px';
    button.style.backgroundColor = 'rgb(255, 190, 105)';
    button.style.borderRadius = '15px';
    button.style.boxShadow = '2px 2px 5px 0px rgba(0, 0, 0, 0.15)';
    button.style.fontSize='15px';
    button.style.textShadow='none';


  } else {
    form.style.display = 'none';
    button.textContent = 'Manage Your Money';
    button.style.width = '450px';
    button.style.height = '230px';
    button.style.position = '';
    button.style.bottom = '';
    button.style.left='';
    button.style.backgroundColor = '';
    button.style.borderRadius = '';
    button.style.marginBottom = '30px';
    button.style.boxShadow ='';
    button.style.fontSize='50px';
    button.style.textShadow='4px 4px 10px rgba(0, 0, 0, 0.3)';
  }
}




function showMarketContents() {
  const contentsContainer = document.getElementById('market_contents_container');
  const sellPostsContainer = document.getElementById('sell_contents_container');
  contentsContainer.style.display = 'block';
  sellPostsContainer.style.display = 'none';
}

function showSellPosts() {
  const contentsContainer = document.getElementById('market_contents_container');
  const sellPostsContainer = document.getElementById('sell_contents_container');
  contentsContainer.style.display = 'none';
  sellPostsContainer.style.display = 'block';
}

window.onload = function() {
  if (window.location.pathname === "/sell_post_screen") {
      $.getJSON('/api/history', function(history_data) {
          if (history_data.length <= 1) {
              console.log('No history data');
              return;
          }
          console.log('history data');
          
          // get the minimum and maximum values in the history_data
          let minValue = Math.min(...history_data);
          let maxValue = Math.max(...history_data);
          
          let ctx = document.getElementById('myChart').getContext('2d');
          let chart = new Chart(ctx, {
              type: 'line',  // line chart
              data: {
                  labels: Array.from({ length: history_data.length }, (_, i) => i+1),  // X-axis labels. Here, it's just 1, 2, 3, ...
                  datasets: [{
                      label: 'History',
                      data: history_data,
                      backgroundColor: 'green',
                      borderColor: 'green',
                      borderWidth: 1
                  }]
              },
              options: {
                  scales: {
                      y: {
                          min: minValue,
                          max: maxValue
                      }
                  }
              }
          });
      });
  }
};
