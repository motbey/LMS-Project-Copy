// SCORM API initialization function
var initScormAPI = function (url, moduleId, userId) {
  "use strict";

  // Create new instance with explicit parameters
  var api = new SCORMAPIWrapper({
    url: url,
    moduleId: moduleId,
    userId: userId,
  });

  // Function to recursively search up through parent windows
  function findAPITries() {
    var maxTries = 500;
    var searchAPI = function () {
      var win = window;
      var tries = 0;
      while (
        !win.API &&
        !win.API_1484_11 &&
        win.parent &&
        win.parent != win &&
        tries <= maxTries
      ) {
        tries++;
        win = win.parent;
      }
      return win;
    };
    return searchAPI();
  }

  // Function to expose API to a window
  function exposeAPI(win) {
    try {
      // First try direct assignment
      win.API = api;
      win.API_1484_11 = api;

      // Then try to assign to parent chain
      var currentWindow = win;
      while (currentWindow.parent && currentWindow.parent !== currentWindow) {
        currentWindow = currentWindow.parent;
        currentWindow.API = api;
        currentWindow.API_1484_11 = api;
      }

      console.log("API exposed to window:", win.location.href);
    } catch (e) {
      console.error("Error exposing API:", e);
    }
  }

  // Initialize the API
  api.LMSInitialize("");

  // Function to expose API to iframe once it loads
  window.exposeAPIToContent = function (iframe) {
    try {
      if (iframe.contentWindow) {
        // Expose to the immediate iframe window
        exposeAPI(iframe.contentWindow);

        // Try to find any nested frames
        try {
          if (iframe.contentWindow.frames) {
            for (var i = 0; i < iframe.contentWindow.frames.length; i++) {
              exposeAPI(iframe.contentWindow.frames[i]);
            }
          }
        } catch (e) {
          console.warn("Could not expose API to nested frames:", e);
        }

        // Set up a MutationObserver to watch for frame additions
        var observer = new MutationObserver(function (mutations) {
          mutations.forEach(function (mutation) {
            mutation.addedNodes.forEach(function (node) {
              if (node.tagName === "FRAME" || node.tagName === "IFRAME") {
                exposeAPI(node.contentWindow);
              }
            });
          });
        });

        observer.observe(iframe.contentDocument.body, {
          childList: true,
          subtree: true,
        });
      }
    } catch (e) {
      console.error("Error exposing API to iframe:", e);
    }
  };

  // Expose API to current window
  exposeAPI(window);

  // Log API initialization
  console.log("SCORM API initialized:", {
    url: url,
    moduleId: moduleId,
    userId: userId,
    api: api,
  });

  return api;
};
