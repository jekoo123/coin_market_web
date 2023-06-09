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