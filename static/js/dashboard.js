function handleScormLaunch(url) {
  const scormWindow = window.open(
    url,
    "SCORM Module",
    "width=1024,height=768,status=yes,scrollbars=yes,resizable=yes"
  );
  if (scormWindow) {
    scormWindow.focus();
  } else {
    alert("Please allow popups to view the module.");
  }
}
