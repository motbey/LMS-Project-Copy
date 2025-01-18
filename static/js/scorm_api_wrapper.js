function SCORMAPIWrapper(config) {
  console.log("SCORMAPIWrapper initialized with config:", config);

  var self = this;
  var initialized = false;
  var finished = false;

  var data = {
    "cmi.core.lesson_status": "incomplete",
    "cmi.core.score.raw": "0",
    "cmi.core.entry": "ab-initio",
    "cmi.suspend_data": "",
    "cmi.core.lesson_location": "",
    "cmi.interactions._count": "0",
  };

  function logScormData(action, parameter, value) {
    console.log(`SCORM ${action}:`, {
      parameter: parameter,
      value: value,
      allData: { ...data },
      initialized: initialized,
      finished: finished,
    });
  }

  // Add these new methods that your SCORM content is looking for
  this.CommitData = function () {
    console.log("CommitData called");
    return this.LMSCommit();
  };

  this.ConcedeControl = function () {
    console.log("ConcedeControl called");
    return "true";
  };

  this.GetDataChunk = function () {
    console.log("GetDataChunk called");
    return data["cmi.suspend_data"] || "";
  };

  this.GetStatus = function () {
    console.log("GetStatus called");
    return data["cmi.core.lesson_status"];
  };

  this.SetBookmark = function (location) {
    console.log("SetBookmark called with:", location);
    return this.LMSSetValue("cmi.core.lesson_location", location);
  };

  this.SetDataChunk = function (chunk) {
    console.log("SetDataChunk called with:", chunk);
    return this.LMSSetValue("cmi.suspend_data", chunk);
  };

  this.SetPassed = function () {
    console.log("SetPassed called");
    return this.LMSSetValue("cmi.core.lesson_status", "passed");
  };

  this.SetFailed = function () {
    console.log("SetFailed called");
    return this.LMSSetValue("cmi.core.lesson_status", "failed");
  };

  this.SetReachedEnd = function () {
    console.log("SetReachedEnd called");
    return this.LMSSetValue("cmi.core.lesson_status", "completed");
  };

  // Initialize
  this.LMSInitialize = function () {
    console.log("LMSInitialize called");
    initialized = true;
    return "true";
  };

  // Finish
  this.LMSFinish = function () {
    console.log("LMSFinish called");
    if (initialized) {
      finished = true;
      // Always send final data on finish
      this.LMSCommit();
      initialized = false;
      return "true";
    }
    return "false";
  };

  // Get Value
  this.LMSGetValue = function (parameter) {
    logScormData("GetValue", parameter, data[parameter]);
    if (initialized && data.hasOwnProperty(parameter)) {
      return data[parameter];
    }
    return "";
  };

  // Set Value
  this.LMSSetValue = function (parameter, value) {
    logScormData("SetValue", parameter, value);
    if (!initialized) return "false";

    data[parameter] = value;

    // Track completion status changes
    if (parameter === "cmi.core.lesson_status") {
      console.log("Lesson status changed to:", value);
      if (value === "completed" || value === "passed") {
        this.LMSCommit(); // Commit immediately on completion
      }
    }

    // Track score changes
    if (parameter === "cmi.core.score.raw") {
      console.log("Score changed to:", value);
    }

    return "true";
  };

  // Commit
  this.LMSCommit = function () {
    console.log("LMSCommit called with data:", data);
    if (!initialized) return "false";

    let status = data["cmi.core.lesson_status"];
    let score = parseInt(data["cmi.core.score.raw"] || "0");
    let interactionCount = parseInt(data["cmi.interactions._count"] || "0");

    // Send data to server
    fetch(config.url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        module_id: config.moduleId,
        status: status,
        score: score,
        interactions: interactionCount,
        location: data["cmi.core.lesson_location"],
        suspend_data: data["cmi.suspend_data"],
      }),
      credentials: "include",
    })
      .then((response) => response.json())
      .then((result) => {
        console.log("SCORM data saved:", result);
      })
      .catch((error) => {
        console.error("Error saving SCORM data:", error);
      });

    return "true";
  };

  // Error Handling
  this.LMSGetLastError = function () {
    return "0";
  };
  this.LMSGetErrorString = function (errorCode) {
    return "No error";
  };
  this.LMSGetDiagnostic = function (errorCode) {
    return "No diagnostic info";
  };

  // Additional SCORM 2004 support
  this.Initialize = this.LMSInitialize;
  this.Terminate = this.LMSFinish;
  this.GetValue = this.LMSGetValue;
  this.SetValue = this.LMSSetValue;
  this.Commit = this.LMSCommit;
  this.GetLastError = this.LMSGetLastError;
  this.GetErrorString = this.LMSGetErrorString;
  this.GetDiagnostic = this.LMSGetDiagnostic;

  // Add this proxy handler to track all method calls
  return new Proxy(this, {
    get: function (target, prop) {
      const value = target[prop];
      if (typeof value === "function") {
        return function (...args) {
          console.log(`SCORM API Call: ${prop}`, args);
          return value.apply(target, args);
        };
      }
      return value;
    },
  });
}
