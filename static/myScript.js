

// Validations of Reports Page

function validateForm_std() {
    let x = document.forms["student"]["studentId"].value;
    if (x == "") {
      alert("Student_Id must be filled out");
      return false;
    }    
}

function validateForm_teacher() {
    let x = document.forms["teacher"]["teacherId"].value;
    if (x == "") {
      alert("Teacher Id field must be filled out");
      return false;
    }    
}

function validateForm_book() {
    let x = document.forms["book"]["bookId"].value;
    if (x == "") {
      alert("Book Id field must be filled out");
      return false;
    }    
}

// Validations of Librarian Page

function validateForm_book_issue() {
    let x = document.forms["lib_issue_book"]["memberId"].value;
    if (x == "") {
      alert("Student/Teacher Id field must be filled out");
      return false;
    }    

    let y = document.forms["lib_issue_book"]["bookId"].value;
    if (y == "") {
      alert("Book Id field must be filled out");
      return false;
    }    

    let z = document.forms["lib_issue_book"]["issueDate"].value;
    if (z == "") {
      alert("Issue Date field must be filled out");
      return false;
    }    
}

function validateForm_book_return() {
    let x = document.forms["lib_return_book"]["memberId"].value;
    if (x == "") {
      alert("Student/Teacher Id field must be filled out");
      return false;
    }    

    let y = document.forms["lib_return_book"]["bookId"].value;
    if (y == "") {
      alert("Book Id field must be filled out");
      return false;
    }    

    let z = document.forms["lib_return_book"]["returnDate"].value;
    if (z == "") {
      alert("Return Date field must be filled out");
      return false;
    }    
}


// Validations of Admin Page

function validateForm_admin_std() {
    let x = document.forms["admin_std"]["studentId"].value;
    if (x == "") {
      alert("Student Id field must be filled out");
      return false;
    }    

    let y = document.forms["admin_std"]["studentName"].value;
    if (y == "") {
      alert("Student Name field must be filled out");
      return false;
    }    

    let z = document.forms["admin_std"]["studentGrade"].value;
    if (z == "") {
      alert("Student Grade field must be filled out");
      return false;
    }   

    let l = document.forms["admin_std"]["studentSection"].value;
    if (l == "") {
      alert("Student Section field must be filled out");
      return false;
    }  
}

// not working
function validateForm_admin_std_del_only() {
    let x = document.forms["admin_std"]["studentId"].value;
    if (x == "") {
      alert("Student Id field must be filled out");
      return false;
    }    
}


function validateForm_admin_teacher() {
    let x = document.forms["admin_teacher"]["teacherId"].value;
    if (x == "") {
      alert("Teacher Id field must be filled out");
      return false;
    }    

    let y = document.forms["admin_teacher"]["teacherName"].value;
    if (y == "") {
      alert("Teacher Name field must be filled out");
      return false;
    }    

    let z = document.forms["admin_teacher"]["teacherEmail"].value;
    if (z == "") {
      alert("Teacher Email field must be filled out");
      return false;
    }   
}

function validateForm_admin_book() {
    let x = document.forms["admin_book"]["bookId"].value;
    if (x == "") {
      alert("Book Id field must be filled out");
      return false;
    }    

    let x1 = document.forms["admin_book"]["bookTitle"].value;
    if (x1 == "") {
      alert("Book Title field must be filled out");
      return false;
    }    

    let x2 = document.forms["admin_book"]["bookAuthor"].value;
    if (x2 == "") {
      alert("Book Author field must be filled out");
      return false;
    }   

    let x3 = document.forms["admin_book"]["bookSubject"].value;
    if (x3 == "") {
      alert("Book Subject field must be filled out");
      return false;
    }  

    let x4 = document.forms["admin_book"]["bookAvailability"].value;
    if (x4 == "") {
      alert("Book Availability field must be filled out");
      return false;
    }  

    let x5 = document.forms["admin_book"]["bookAllocatedId"].value;
    if (x5 == "") {
      alert("Book Allocated Id field must be filled out");
      return false;
    }  

    let x6 = document.forms["admin_book"]["bookIssueDate"].value;
    if (x6 == "") {
      alert("Book Issue Date field must be filled out");
      return false;
    }  

    let x7 = document.forms["admin_book"]["bookReturnDate"].value;
    if (x7 == "") {
      alert("Book Return Date field must be filled out");
      return false;
    }  
}