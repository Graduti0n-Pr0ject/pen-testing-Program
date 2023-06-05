const scanButton = document.getElementById('scanButton');
const outputDiv = document.getElementById('center');

// Click listener for the scan button
scanButton.addEventListener('click', () => {
  // Send a message to the content script to start scanning the page
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    chrome.tabs.sendMessage(tabs[0].id, { action: 'scan' }, (response) => {
      // Display the results in the popup window
      formatResult(response);
    });
  });
});




// Helper function to format the vulnerabilities as HTML
function formatResult(res) {
  
  res = [...Object.values(res)][0]

  res = res.map(e => {
    e.cves = e.cves.map(cve => {
      if (cve.identifiers.CVE && cve.info) {

        return `<a href="${cve.info[0]}">${cve.identifiers.CVE[0]}</a>`
      }
      return  `<a href="#">#</a>`
    })
    return e;
  })


  res.map(e => {
    document.getElementById("scanResults").insertAdjacentHTML("afterend",
    `  <tr>
        <td>${e.library.name}</td>
        <td>${e.library.version}</td>
        <td>${e.cves.join(', ')}</td>
      </tr>
    ` );
  })
}


