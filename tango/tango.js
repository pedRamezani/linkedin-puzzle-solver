function main() {
  var grid = document.querySelector(".lotka-grid");
  var nRows = +getComputedStyle(grid).getPropertyValue('--rows');
  var nCols = +getComputedStyle(grid).getPropertyValue('--cols');
  
  // DON'T CHANGE
  var SUN = 1;
  var MOON = 0;
  
  var EQUAL = 1;
  var CROSS = -1;
  var NONE = 0; // ALSO STEPS FOR DIRECTION NONE
  
  // STEPS FOR EACH DIRECTION
  var RIGHT = 1;
  var DOWN = nCols;
  
  var lockedCells = [...grid.querySelectorAll(".lotka-cell--locked")].map(cell => ({
    cellId: +cell.dataset.cellIdx,
    cellType: (cell.querySelector("svg g#Sun") !== null) ? SUN : MOON
  }));
  
  var edgeCells = [...grid.querySelectorAll(".lotka-cell:has(.lotka-cell-edge)")].flatMap(cell => (
    [...cell.querySelectorAll(".lotka-cell-edge")].map(edge => ({
      startCellId: +cell.dataset.cellIdx,
      type: edge.querySelector("svg[aria-label='Equal']") ? EQUAL : 
            edge.querySelector("svg[aria-label='Cross']") ? CROSS : NONE,
      direction: 	edge.classList.contains("lotka-cell-edge--right") ? RIGHT :
                  edge.classList.contains("lotka-cell-edge--down") ? DOWN : NONE
    }))
  )).map((cell) => ({
    ...cell,
    endCellId: cell.startCellId + cell.direction
  }));
  
  var equalCondition = edgeCells.filter(cell => cell.type === EQUAL).map(cell => [cell.startCellId, cell.endCellId]);
  
  var crossCondition = edgeCells.filter(cell => cell.type === CROSS).map(cell => [cell.startCellId, cell.endCellId]);
  
  var puzzleData = {
    nRows: nRows,
    nCols: nCols,
    lockedCells: lockedCells,
    equalCondition: equalCondition,
    crossCondition: crossCondition
  };

  var blob = new Blob([JSON.stringify(puzzleData, null, 2)], {type : 'application/json'});
  var a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'tango.json';
  a.click();
}

var targetURL = "https://www.linkedin.com/games/tango/";
var targetHost = "www.linkedin.com";
var targetPath = "/games/tango/";

if (location.host !== targetHost || location.pathname !== targetPath) {
  window.open(targetURL, "_blank");
  alert("This bookmarklet only works on the LinkedIn Tango game page. The correct page has been opened — please run it again there.");
} else {
  if (document.readyState === "complete" || document.readyState === "interactive") {
    main();
  } else {
    window.addEventListener("DOMContentLoaded", main);
  }
}