function pushCsvToServer() {
  var server_url = '';
  var user = '';
  var write_password = '';
  var read_password = '';

  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getActiveSheet();
  var selection = sheet.getActiveRange();

  var filename = selection.getCell(1, 1).getValue() + ".csv";

  var startRow = selection.getRow() + 3;
  var startColumn = selection.getColumn();
  var numColumns = selection.getWidth();

  var lastRow = selection.getLastRow();
  var numRows = lastRow - startRow + 1;

  var dataRange = sheet.getRange(startRow, startColumn, numRows, numColumns);
  var data = dataRange.getValues();

  var csvContent = arrayToCsv(data);
  var csvBlob = Utilities.newBlob(csvContent, 'text/csv', filename);

  var url = server_url + '/push/' + user + '/' + write_password + '/' + filename;

  var payload = {
    'file': csvBlob
  };

  var options = {
    'method' : 'post',
    'payload' : payload,
    'muteHttpExceptions': true
  };

  try {
    var response = UrlFetchApp.fetch(url, options);
    var responseCode = response.getResponseCode();
    var responseContent = response.getContentText();

    if (responseCode == 200) {
      var download_url = server_url + '/pull/' + user + '/' + read_password + '/' + filename;
      SpreadsheetApp.getUi().alert('The file can be retrieved using the following URL:\n' + download_url);
    } else {
      SpreadsheetApp.getUi().alert("Failed to upload file '" + filename + "': " + responseContent);
    }
  } catch (e) {
    SpreadsheetApp.getUi().alert("Failed to upload file '" + filename + "': " + e);
  }
}

function arrayToCsv(dataArray) {
  return dataArray.map(function(row) {
    return row.map(function(field) {
      if (field === null || field === undefined) {
        field = '';
      } else if (typeof field === 'string') {
        // Escape double quotes in the field
        field = field.replace(/"/g, '""');
        // If field contains comma, newline, or double quotes, enclose it in double quotes
        if (field.search(/("|,|\n)/g) >= 0) {
          field = '"' + field + '"';
        }
      }
      return field;
    }).join(',');
  }).join('\n');
}

function onOpen() {
  SpreadsheetApp.getUi()
      .createMenu('PythonLatexSync')
      .addItem('Push CSV to Server', 'pushCsvToServer')
      .addToUi();
}
