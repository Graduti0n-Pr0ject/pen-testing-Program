// Helper function to compare two version strings in semver format
function compareVersions(a, b) {
  const partsA = a.split('.');
  const partsB = b.split('.');
  for (let i = 0; i < 3; i++) {
    const diff = parseInt(partsA[i]) - parseInt(partsB[i]);
    if (diff !== 0) {
      return diff > 0 ? 1 : -1;
    }
  }
  return 0;
}

// Listen for the DOMContentLoaded event
// window.addEventListener('DOMContentLoaded', () => {

//   // Send a message to the background script to initiate scanning
//   chrome.runtime.sendMessage({ action: 'scan' }, (response) => {
//     if (response && response.result) {
//       const vulnerabilities = response.result;
//       const resultHtml = formatResult(vulnerabilities);
      
//       document.body.innerHTML = resultHtml;
//     } else {
//       console.error(response);
//       document.body.innerHTML = 'Error: Unable to retrieve vulnerability data';
//     }
//   });
// });

// Listen for messages from the background script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'scan') {
    const libraries = getLibraries();
    scanLibraries(libraries).then((results) => {
      const vulnerabilities = filterVulnerabilities(results);
      const result = { result: vulnerabilities };
      sendResponse(result);
    }).catch(() => {
      sendResponse('Error: Unable to retrieve vulnerability data');
    });
    return true; // Keep the message port open until the response is ready
  }
});

// Helper function to extract the names and versions of all script libraries on the page
function getLibraries() {
  const libraries = [];
  const scripts = document.querySelectorAll('script[src]');
  for (let i = 0; i < scripts.length; i++) {
    const src = scripts[i].getAttribute('src');

    // to match different URLs formates assets links
    const regex1 = /\/(\w+)[.-](\d+(?:\.\d+)*)(?:\.min)?\.js$/;
    // cdnLinks
    const regex2 = /(?:[^/]*\/)*([^/@]+)[/@]([\d\.]+)/;
    match1 = src.match(regex1);
    match2 = src.match(regex2);
    if (match1){
      const name = match1[1];
      const version = match1[2]
      if (!libraries.some(lib => lib.name === name && lib.version === version)){
        libraries.push({ name, version });
      }
    }

    if (match2){
      const name = match2[1];
      const version = match2[2];
      console.log(name)
      console.log(version)
      if (!libraries.some(lib => lib.name === name && lib.version === version)){
        libraries.push({ name, version });
      }
    }

    else {
      console.log(`Ignoring non-library script: ${src}`);
    }
  }

  console.log(`Found ${libraries.length} library scripts`);
  return libraries;
}

// Helper function to scan libraries for vulnerabilities using Retire.js repository
async function scanLibraries(libraries) {
  const response = await fetch('https://raw.githubusercontent.com/RetireJS/retire.js/master/repository/jsrepository.json');
  if (!response.ok) {
    throw new Error(`Error retrieving vulnerability data: ${response.status} - ${response.statusText}`);
  }
  const data = await response.json();
  const vulnerabilities = [];
  for (let i = 0; i < libraries.length; i++) {
    const library = libraries[i];
    const libraryName = library.name.toLowerCase();
    if (libraryName in data) {
      const matches = data[libraryName].vulnerabilities.filter((vuln) => {
        if (vuln.below && compareVersions(library.version, vuln.below) === -1) {
          return false;
        }
        if (vuln.atOrAbove && compareVersions(library.version, vuln.atOrAbove) === -1) {
          return false;
        }
        return true;
      });
      vulnerabilities.push({ library, cves: matches });
    }
  }
  return vulnerabilities;
}

// Helper function to filter out non-vulnerable libraries and format the results as an array of objects
function filterVulnerabilities(results) {
  const vulnerabilities = [];
  for (let i = 0; i < results.length; i++) {
    const { library: { name, version }, cves } = results[i];
    if (cves && cves.length > 0) {
      vulnerabilities.push({ library: { name, version }, cves });
      console.log(vulnerabilities)
    }
  }
  return vulnerabilities;
}



      
      