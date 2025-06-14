function main() {
  var grid = document.querySelector(".trail-grid");
  var nRows = +getComputedStyle(grid).getPropertyValue('--rows');
  var nCols = +getComputedStyle(grid).getPropertyValue('--cols');
  
  // STEPS FOR EACH DIRECTION
  var RIGHT = 1;
  var DOWN = nCols;
  var NONE = 0;

  var lockedCells = [...grid.querySelectorAll(".trail-cell:has(.trail-cell-content)")].map(cell => ({
    cellId: +cell.dataset.cellIdx,
    cellNumber: +cell.querySelector(".trail-cell-content").textContent.trim()
  }));
  
  var wallCondition = [...grid.querySelectorAll(".trail-cell:has(.trail-cell-wall)")].flatMap(cell => (
    [...cell.querySelectorAll(".trail-cell-wall")].map(wall => ({
      startCellId: +cell.dataset.cellIdx,
      direction: 	wall.classList.contains("trail-cell-wall--right") ? RIGHT :
                  wall.classList.contains("trail-cell-wall--down") ? DOWN : NONE
    }))
  )).filter((cell) => cell.direction != NONE).map((cell) => [cell.startCellId, cell.startCellId + cell.direction]);
  
  var puzzleData = {
    nRows: nRows,
    nCols: nCols,
    lockedCells: lockedCells,
    wallCondition: wallCondition
  };

  var blob = new Blob([JSON.stringify(puzzleData, null, 2)], {type : 'application/json'});
  var a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'zip.json';
  a.click();
}

var targetURL = "https://www.linkedin.com/games/zip";
var targetHost = "www.linkedin.com";
var targetPath = "/games/zip/";

if (location.host !== targetHost || location.pathname !== targetPath) {
  window.open(targetURL, "_blank");
  alert("This bookmarklet only works on the LinkedIn Zip game page. The correct page has been opened — please run it again there.");
} else {
  if (document.readyState === "complete" || document.readyState === "interactive") {
    main();
  } else {
    window.addEventListener("DOMContentLoaded", main);
  }
}