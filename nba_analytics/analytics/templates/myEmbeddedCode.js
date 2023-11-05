import {
    TableauAskData
  } from 'https://online.tableau.com/javascripts/api/tableau.embedding.3.latest.min.js';
  
  let elementId = 'askDataJsContainer';
  
  function initAskData() {
    console.log('InitAskData');
    let url = 'https://online.tableau.com/askData/lens/Superstore+Datasource';
    let askData = new TableauAskData();
  
    askData.height = 700;
    askData.width = 800;
    askData.showSave = true;
  
    askData.src = url;
  
    document.getElementById(elementId).appendChild(askData);
    console.log('Initialized askData with v3', askData);
  }
  
  initAskData();
  