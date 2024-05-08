function calcGrades() {
  getData()
    .done(function (text) {
      let parsedText = $.csv.toArrays(text);
      let paperCode = $("#paperCodeIndividual").val().toString();
      let mark = Number($("#RawMarksIndividual").val());
      const GRADES = [0, 0, "A", "B", "C", "D", "E"];

      for (let i = 0; i < parsedText.length; i++) {
        const row = parsedText[i];
        if (row[0].includes(paperCode)) {
          let maxMark = row[1];
          for (let j = 0; j < row.length; j++) {
            if (j == 0 || j == 1) {
            } else {
              const boundary = row[j];

              console.log(boundary);
              if (mark >= boundary) {
                userGrade = GRADES[j];
                $("#FinalGradeIndividual").text(
                  "Your Individual Component Grade - " + userGrade
                );
                break;
              }
            }
          }
        }
      }
    })
    .fail(function (jqXHR, textStatus, error) {
      Toastify({
        text: "Something went wrong :(",
        duration: 3000,
        newWindow: true,
        gravity: "top", // `top` or `bottom`
        position: "right", // `left`, `center` or `right`
        style: {
          background: "linear-gradient(to right, #9A999A, #5E5D5E)",
        },
      }).showToast();
      // $("#FinalGradeIndividual").text("Sorry, something went wrong :(");
    });
}
