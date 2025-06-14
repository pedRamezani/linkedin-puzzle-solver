function main() {
  var grid = document.querySelector(".queens-grid-no-gap");
  var nRows = +getComputedStyle(grid).getPropertyValue('--rows');
  var nCols = +getComputedStyle(grid).getPropertyValue('--cols');

  var lockedCells = [...grid.querySelectorAll(".queens-cell-with-border")].map(cell => ({
    cellId: +cell.dataset.cellIdx,
    cellType: +[...cell.classList].filter(a => a.startsWith("cell-color-"))[0].slice(11)
  }));

  var puzzleData = {
    nRows: nRows,
    nCols: nCols,
    cellColors: lockedCells
  };

  var blob = new Blob([JSON.stringify(puzzleData, null, 2)], {type : 'application/json'});
  var a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'queens.json';
  a.click();
}

var targetURL = "https://www.linkedin.com/games/queens/";
var targetHost = "www.linkedin.com";
var targetPath = "/games/queens/";

if (location.host !== targetHost || location.pathname !== targetPath) {
window.open(targetURL, "_blank");
alert("This bookmarklet only works on the LinkedIn Queens game page. The correct page has been opened — please run it again there.");
} else {
if (document.readyState === "complete" || document.readyState === "interactive") {
    main();
} else {
    window.addEventListener("DOMContentLoaded", main);
}
}