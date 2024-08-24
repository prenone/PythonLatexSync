// ==UserScript==
// @name         PythonLatexSync ALL
// @namespace    http://tampermonkey.net/
// @version      2024-08-23
// @description  Automatically expand items and refresh the page on Overleaf project pages with a custom button click.
// @author       You
// @match        https://www.overleaf.com/project/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=overleaf.com
// @grant        none
// ==/UserScript==

(function() {
  'use strict';

  const refresh_button_timeout = 5000;
  const refresh_timeout = 3000;

  function executeScript() {
    while (true) {
      let items = document.querySelectorAll('li[role="treeitem"][aria-expanded="false"]');
      let expansions = 0;

      for (let i = 0; i < items.length; i++) {
        let expandItem = items[i].querySelector('button[aria-label="Expand"]');
        if (expandItem) {
          expandItem.click();
          expansions += 1;
        }
      }

      if (expansions === 0) {
        break;
      }
    }

    let items = document.querySelectorAll('li[role="treeitem"]');
    let j = 0;

    for (let i = 0; i < items.length; i++) {
      let entity = items[i].querySelector("i.linked-file-highlight");

      if (!entity) {
        continue;
      }

      j++;

      setTimeout(() => {
        items[i].querySelector(".item-name-button").click();

        let refresh = document.querySelector("i.fa-refresh:not(.pls-refresh)").parentElement;
        if (refresh) {
          refresh.click();
          console.log(refresh);
        }
      }, refresh_timeout * j);
    }
  }


  setTimeout(() => {
    let toolbar = document.querySelector('.toolbar-filetree > .toolbar-left');

    console.log("Done")
    if (toolbar) {

      let button = document.createElement('button');
      button.type = 'button';
      button.className = 'btn btn-default';
      button.innerHTML = '<i class="fa fa-refresh fa-fw pls-refresh" aria-hidden="true"></i><span class="sr-only">Refresh all with PLS</span>';

      button.addEventListener('click', executeScript);

      toolbar.appendChild(button);
    }
  }, refresh_button_timeout)

})();

