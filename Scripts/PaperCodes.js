function getData() {
  let subjectCode = $("#subjectCodeIndividual").val();
  let yearCode = $("#yearIndividual").val();
  let sessionCode = $("#SessionCodeIndividual").val();

  return $.ajax({
    url: `data/${subjectCode}-Converted/I-${subjectCode}_${sessionCode}${yearCode}_gt.csv`,
    dataType: "text",
  });
}

function addPaperCodes() {
  getData()
    .done(function (text) {
      let parsedText = $.csv.toArrays(text);
      let paperCodes = {};

      parsedText.forEach((row, index) => {
        if (index !== 0) {
          paperCodes[row[0].slice(-2)] = row[0];
        }
      });

      let paperCodesSelect = $("#paperCodeIndividual");
      paperCodesSelect.empty();

      $("#FinalGradeIndividual").text("");

      $.each(paperCodes, function (val, code) {
        paperCodesSelect.append($("<option></option>").val(val).html(code));
      });
    })
    .fail(function (jqXHR, textStatus, error) {
      Toastify({
        text: "Something went wrong :(",
        duration: 3000,
        newWindow: true,
        gravity: "top", // `top` or `bottom`
        position: "right", // `left`, `center` or `right`
        // stopOnFocus: true, // Prevents dismissing of toast on hover
        style: {
          background: "linear-gradient(to right, #9A999A, #5E5D5E)",
        },
      }).showToast();
    });
}
