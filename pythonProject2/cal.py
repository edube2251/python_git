Documentation()
EDITED BY EDWIN CHINYAMA  BFT 15/05/2012
//BFT1 080208 - Added code to check assessment journal has same number of students as those registered.
//29/08/12 - CHECKS TO ENSURE THAT THERE IS NOT AGGR. ASSESSMENT ALREADY POSTED FOR THIS COURSE
AO-CCM-28/11/13 - ADDED CODE TO MANAGE POSTING OF ADDITIONS TO POSTED CONTINUOS ASSESSMENTS
AO-CCM-30/11/13 - ADDED CODE TO MANAGE REVERSAL OF ASSESSMENT MARKS AND PREVENT CREATION OF REDUNDANT TABLES

OnRun()

PostContinousAssessment(Code : Code[10])

//**********************************************************************************************************************************
 // SECTION 1.1

// CALLING THE FUNCTIONS #1---Checks the continous assesment journals---//CheckContinousAssessmentLines(Code);
//                       #2---Post the continous assessment lines-------//PostContinousAssessmentLines(Code);
//                       #3---Delete the continous assessment lines-----//DeleteContinousAssessmentLines(Code);

//This function accepts the Assessment No. from the Continous Assessment form. It then passes this to all the other functions which
//are called therein.

         CheckContinousAssessmentLines(Code);
         PostContinousAssessmentLines(Code);
         DeleteContinousAssessmentLines(Code);

//**********************************************************************************************************************************

CheckContinousAssessmentLines(CACode : Code[10])

//**********************************************************************************************************************************
  // SECTION 1.2

     // CHECKS IF THE REGISTERED NUMBER OF STUDENTS IS THE SAME AS THE NUMBER IN THE JOURNAL

          IF NOT IsLecturer THEN
            ERROR(Text005,USERID);

          IF DateNotAllowed(TODAY) THEN
            ERROR(Text006);

          Result.RESET;
          Result.SETRANGE(Result."Assessment No.",CACode);
         ContAssessHdr1.RESET;
         ContAssmtHdr.SETRANGE(ContAssmtHdr."Assessment No.",CACode);
         ContAssmtHdr.FINDFIRST;


         IF ContAssmtHdr."Applies to Posted Assessment" = '' THEN //AO-CCM-28/11/13
          IF Result.FINDFIRST THEN BEGIN
             SCourse.RESET;
             SCourse.SETRANGE(SCourse."Programme Course Code",Result."Course Code");
             SCourse.SETRANGE(SCourse."Academic Year",Result."Academic Year");
             SCourse.SETRANGE(SCourse."Teaching Class Code",Result."Teaching Class Code");
             SCourse.SETRANGE(SCourse.Part,ContAssmtHdr."Programme Part");
             SCourse.SETRANGE(SCourse.Semester,ContAssmtHdr.Semester);
             //MESSAGE('Student Course %1',SCourse.COUNT);
             //MESSAGE('Result Count %1',Result.COUNT);


            IF (SCourse.COUNT<>Result.COUNT) THEN
               ERROR(Text50000,FORMAT(SCourse.COUNT));

          END;

//**********************************************************************************************************************************
  // SECTION 1.3

         IF Result.FIND('-') THEN
            REPEAT
             Result.TESTFIELD(Result."Teaching Class Code");
             Result.TESTFIELD(Result."Academic Year");
             Result.TESTFIELD(Result."Course Code");
             Result.TESTFIELD(Result."Student Registration No.");
             //HT Added 14/02/2018
             //Result.TESTFIELD(Result."Registry Entry No.",SCourse."Registry Entry No.");
             //HT EMD

             ContAssmtHdr.GET(Result."Assessment No.");
          IF (ContAssmtHdr.Type<>ContAssmtHdr.Type::Aggregating) THEN BEGIN
            IF Result.Attended IN [Result.Attended::Yes,Result.Attended::No] THEN BEGIN
              IF (Result.Attended=Result.Attended::Yes) AND (Result."Mark Attained (%)"=0)THEN
               Result.TESTFIELD("Mark Confirmed",TRUE);

              IF(Result.Attended=Result.Attended::No) THEN BEGIN
               Result.TESTFIELD(Result."Mark Attained (%)",0);
               Result.TESTFIELD("Mark Confirmed",TRUE);
              END;
            END ELSE BEGIN
              Result.FIELDERROR(Result.Attended);
            END;
             //IF Result.Attended = Result.Attended::" " THEN
             // ERROR();
          END;

//**********************************************************************************************************************************
  // SECTION 1.4

// CHECKS TO SEE IF EACH STUDENT IN THE COURSE ASSESSMENT LINES HAS REGISTERED FOR THE SUBJECT IN QUESTION

           SCourse.RESET;
           SCourse.SETRANGE(SCourse."Student Registration No.",Result."Student Registration No.");
           SCourse.SETRANGE(SCourse."Programme Course Code",Result."Course Code");
           SCourse.SETRANGE(SCourse."Academic Year",Result."Academic Year");
             IF NOT SCourse.FINDFIRST THEN
                   ERROR(Text000,Result."Student Registration No.",Result."Course Code");
                   UNTIL Result.NEXT=0
             ELSE
             ERROR(Text002);


//29/08/12 CHECKS TO ENSURE THAT THERE IS NOT AGGR. ASSESSMENT ALREADY POSTED FOR THIS COURSE
ContAssessHdr1.RESET;
IF ContAssessHdr1.GET(CACode) THEN
  CASE ContAssessHdr1.Type OF
    ContAssessHdr1.Type::Contributing:
      BEGIN
        ContAssessContri.SETRANGE("Posted Assessment No.",ContAssessHdr1."Assessment No.");
        ContAssessContri.SETRANGE(Reversed,FALSE);

        IF ContAssessContri.FINDFIRST THEN
          ERROR(Text003,ContAssessContri."Assessment No.");

  //This should also check if there is an Aggregating Assesment already posted then is yes no posting to be allowed.
        PstdContAssessHdr1.SETRANGE("Teaching Class Code",ContAssessHdr1."Teaching Class Code");
        PstdContAssessHdr1.SETRANGE("Course Code",ContAssessHdr1."Course Code");
        PstdContAssessHdr1.SETRANGE("Academic Year",ContAssessHdr1."Academic Year");
        PstdContAssessHdr1.SETRANGE("Programme Part",ContAssmtHdr."Programme Part");
        PstdContAssessHdr1.SETRANGE(Semester,ContAssmtHdr.Semester);
        PstdContAssessHdr1.SETRANGE(Type,PstdContAssessHdr1.Type::Aggregating);
        PstdContAssessHdr1.SETRANGE(Reversed,FALSE);
        IF PstdContAssessHdr1.FINDFIRST THEN
          ERROR(Text004,PstdContAssessHdr1."Academic Year");
      END;

    ContAssessHdr1.Type::Aggregating:
      BEGIN
        PstdContAssessHdr1.SETRANGE("Teaching Class Code",ContAssessHdr1."Teaching Class Code");
        PstdContAssessHdr1.SETRANGE("Course Code",ContAssessHdr1."Course Code");
        PstdContAssessHdr1.SETRANGE("Academic Year",ContAssessHdr1."Academic Year");
        PstdContAssessHdr1.SETRANGE("Programme Part",ContAssmtHdr."Programme Part");
        PstdContAssessHdr1.SETRANGE(Semester,ContAssmtHdr.Semester);
        PstdContAssessHdr1.SETRANGE(Type,PstdContAssessHdr1.Type::Aggregating);
        PstdContAssessHdr1.SETRANGE(Reversed,FALSE);
        IF PstdContAssessHdr1.FINDFIRST THEN
          ERROR(Text004,PstdContAssessHdr1."Academic Year");
      END;
  END;

PostContinousAssessmentLines(CACode : Code[10])
IF CourseAssessment.FIND('+') THEN
  CourseAssesmentLastEntryNo:=CourseAssessment."Entry No."
ELSE
  CourseAssesmentLastEntryNo:=0;

Result.RESET;
Result.SETRANGE(Result."Assessment No.",CACode);
IF Result.FIND('-') THEN BEGIN
  ContAssmtHdr.GET(Result."Assessment No.");
  ContAssmtHdr.TESTFIELD(ContAssmtHdr.Description);

  ExaminationSetup.GET;
  ExaminationSetup.TESTFIELD("Mark Rounding Precision");
  IF (ContAssmtHdr.Type=ContAssmtHdr.Type::Aggregating) THEN BEGIN
   REPEAT
    IF Result.Attended<>0 THEN BEGIN
     SCourse.RESET;
     SCourse.SETRANGE(SCourse."Student Registration No.",Result."Student Registration No.");
     SCourse.SETRANGE(SCourse."Teaching Class Code",Result."Teaching Class Code");
     SCourse.SETRANGE(SCourse."Programme Course Code",Result."Course Code");
     SCourse.SETRANGE(SCourse."Academic Year",Result."Academic Year");
     IF SCourse.FINDFIRST THEN BEGIN
       CLEAR(CourseAssessment);
       CourseAssessment.INIT;
       CourseAssesmentLastEntryNo+=1;
       CourseAssessment."Document No" := Result."Assessment No.";
       CourseAssessment."Entry No.":=CourseAssesmentLastEntryNo;
       CourseAssessment."Student Registration No.":=Result."Student Registration No.";
       CourseAssessment."Teaching Class Code":=Result."Teaching Class Code";
       CourseAssessment.AcademicYear:=Result."Academic Year";
       CourseAssessment."Programme Course Code":=Result."Course Code";
       CourseAssessment."Posting Date":=TODAY;
       CourseAssessment."User ID":=USERID;
       CourseAssessment."Assessment Mark":=ROUND(Result."Mark Attained (%)",ExaminationSetup."Mark Rounding Precision",'=');
       CourseAssessment."Overall Mark":=ROUND(Result."Mark Attained (%)",ExaminationSetup."Mark Rounding Precision",'=');
       CourseAssessment.ResultOpen:=TRUE;
       CourseAssessment."Programme Part" := ContAssmtHdr."Programme Part";
       CourseAssessment.Semester := ContAssmtHdr.Semester;
       CourseAssessment."Entry Type":=CourseAssessment."Entry Type"::Continuous;

       ProgCourse.SETRANGE("Teaching Class Code",ContAssmtHdr."Teaching Class Code");
       ProgCourse.SETRANGE("Academic Year",ContAssmtHdr."Academic Year");
       ProgCourse.SETRANGE("Programme Part",ContAssmtHdr."Programme Part");
       ProgCourse.SETRANGE(Semester,ContAssmtHdr.Semester);
       ProgCourse.SETRANGE(Code,Result."Course Code");
       IF ProgCourse.FINDFIRST THEN;

       CASE ContAssmtHdr."Assessment Type" OF
       'ASSIGN':
       BEGIN
        CourseAssessment."Exam Type" := 'ASSIGN';
       END;
       'PRAC':
       BEGIN
        CourseAssessment."Exam Type" := 'PRAC';
       END;
       'ORAL':
       BEGIN
        CourseAssessment."Exam Type" := 'ORAL';
       END;
        END;

       //>>>> HT Edited 24/01/2018
       CourseAssessment."Programme Code" :=SCourse."Programme Code";//ProgCourse."Programme Code";// pick this from the class code.
       CourseAssessment."Result Class Code" := SCourse."Result Class Code";
       //HT Added 14/02/2018
       CourseAssessment."Registry Entry No." := Result."Registry Entry No.";
       //<<<< HT END Code

       CourseAssessment.INSERT(TRUE);
     END;
    END;
   UNTIL Result.NEXT=0;
END;

   IF ContAssmtHdr.Type<>ContAssmtHdr.Type::Aggregating THEN
      ContAssmtHdr.TESTFIELD(ContAssmtHdr."Assessment Type");

   IF ContAssmtHdr."Applies to Posted Assessment" = '' THEN BEGIN

     PostedContAssmt.TRANSFERFIELDS(ContAssmtHdr);
     PostedContAssmt."Posted By":=USERID;
     PostedContAssmt."Posting Date":=TODAY;
     PostedContAssmt.INSERT;

     Result.RESET;
     Result.SETRANGE(Result."Teaching Class Code",ContAssmtHdr."Teaching Class Code");
     Result.SETRANGE(Result."Course Code",ContAssmtHdr."Course Code");
     Result.SETRANGE(Result."Academic Year",ContAssmtHdr."Academic Year");
     Result.SETRANGE(Result."Assessment No.",ContAssmtHdr."Assessment No.");
     Result.SETFILTER(Result."Student Registration No.",'<>%1','''');
     IF Result.FIND('-')THEN
      REPEAT
       PostedContAssmtLine.TRANSFERFIELDS(Result);
       PostedContAssmtLine.INSERT;
     UNTIL Result.NEXT=0;
   END ELSE BEGIN
     Result.RESET;
     Result.SETRANGE(Result."Teaching Class Code",ContAssmtHdr."Teaching Class Code");
     Result.SETRANGE(Result."Course Code",ContAssmtHdr."Course Code");
     Result.SETRANGE(Result."Academic Year",ContAssmtHdr."Academic Year");
     Result.SETRANGE(Result."Assessment No.",ContAssmtHdr."Assessment No.");
     Result.SETFILTER(Result."Student Registration No.",'<>%1','''');
      IF Result.FIND('-')THEN
       REPEAT
        //>>>> HT Edited
        //Edited out
        //PostedContAssmtLine.INIT;
        //PostedContAssmtLine.RESET;
        PostedContAssmtLine.TRANSFERFIELDS(Result);
        //PostedContAssmtLine."Assessment No." := ContAssmtHdr."Applies to Posted Assessment";
        PostedContAssmtLine."Added by Assessment No." := ContAssmtHdr."Assessment No.";
        //<<<< HT Edited 24/01/2017
        PostedContAssmtLine."Added On" := TODAY;
        PostedContAssmtLine."Added By" := USERID;
        PostedContAssmtLine.INSERT;
       UNTIL Result.NEXT = 0;
   END;
END;

 IF (ContAssmtHdr.Type=ContAssmtHdr.Type::Aggregating) THEN BEGIN

  ContAssmtContribution.SETRANGE(ContAssmtContribution."Assessment No.",CACode);
  IF ContAssmtContribution.FIND('-') THEN
    REPEAT
      PostedContAssmtContribution.INIT;
      PostedContAssmtContribution."Posted Assessment No." := ContAssmtContribution."Posted Assessment No.";
      PostedContAssmtContribution."Assessment No." := ContAssmtContribution."Assessment No.";
      PostedContAssmtContribution."Teaching Class Code" := ContAssmtContribution."Teaching Class Code";
      PostedContAssmtContribution."Course Code" := ContAssmtContribution."Course Code";
      PostedContAssmtContribution."Academic Year" := ContAssmtContribution."Academic Year";
      PostedContAssmtContribution.Contribution := ContAssmtContribution.Contribution;
      PostedContAssmtContribution.INSERT;
    UNTIL ContAssmtContribution.NEXT=0;
END;

COMMIT;

DeleteContinousAssessmentLines(CACode : Code[10])


//**********************************************************************************************************************************
   // SECTION 1.8

// Delete Continous Assessment Header

    Result.RESET;
    Result.SETRANGE(Result."Assessment No.",CACode);
    Result.FIND('-');
         ContAssmtHeader.GET(Result."Assessment No.");
         ContAssmtHeader.DELETE(TRUE);

// WHEN THE HEADER IS DELETED THE EFFECT WILL CASCADE TO THE LINES

//**********************************************************************************************************************************

PostPartAssessment(ProgramCode : Code[10];ProgramPart : Integer;AcademicYear : Integer)
CheckPartAssessmentLines(ProgramCode,ProgramPart,AcademicYear);
PostPartAssessmentLines(ProgramCode,ProgramPart,AcademicYear);
DeletePartAssessmentLines(ProgramCode,ProgramPart,AcademicYear);

CheckPartAssessmentLines(ProgramCode : Code[10];ProgramPart : Integer;AcademicYear : Integer)
{
Result.RESET;
Result.SETRANGE(Result."Allow Posting From",ProgramCode);
Result.SETRANGE(Result."Allow Posting To",AcademicYear);
Result.SETRANGE(Result.Part,ProgramPart);
IF Result.FIND('-') THEN
REPEAT
  //Result.CALCFIELDS(Result."Oral Exam Weight", Result."Exam Weight", Result."Assessment Weight");
  //Result.TESTFIELD(Result."Examination Code");
  //Result.TESTFIELD(Result."Programme Code");
  //Result.TESTFIELD(Result."Academic Year");
  //Result.TESTFIELD(Result."Course Code");
  //Result.TESTFIELD(Result."Student Registration No.");
  //Result.TESTFIELD(Result.Semester);
  //IF (Result."Exam Mark"<>0) AND (Result."Exam Weight"<>0) THEN
  //  Result.TESTFIELD(Result."Examination Attended",Result."Examination Attended"::Yes);

  //IF (Result.Attended=Result.Attended::Yes) THEN
  //   Result.TESTFIELD(Result."Mark Attained (%)")
  //ELSE
  //  Result.TESTFIELD(Result."Mark Attained (%)",0);

  IF Result."Programme Course Code"<>'' THEN BEGIN
    SCourse.RESET;
    SCourse.SETRANGE(SCourse."Student Registration No.",Result."User ID");
    SCourse.SETRANGE(SCourse."Programme Course Code",Result."Programme Course Code");
    SCourse.SETRANGE(SCourse."Academic Year",Result."Allow Posting To");
    //SCourse.SETRANGE(SCourse.Semester,Result.Semester);
    IF NOT SCourse.FINDFIRST THEN
      ERROR(Text000,Result."User ID",Result."Programme Course Code");
  END;
UNTIL Result.NEXT=0
ELSE
  ERROR(Text002);
}

PostPartAssessmentLines(ProgramCode : Code[10];ProgramPart : Integer;AcademicYear : Integer)
{
Result.RESET;
Result.SETRANGE(Result."Allow Posting From",ProgramCode);
Result.SETRANGE(Result."Allow Posting To",AcademicYear);
Result.SETRANGE(Result.Part,ProgramPart);
IF Result.FIND('-') THEN REPEAT
      IF Result."Programme Course Code"<>'' THEN BEGIN
        SCourse.RESET;
        SCourse.SETRANGE(SCourse."Student Registration No.",Result."User ID");
        SCourse.SETRANGE(SCourse."Programme Code",Result."Allow Posting From");
        SCourse.SETRANGE(SCourse."Programme Course Code",Result."Programme Course Code");
        SCourse.SETRANGE(SCourse."Academic Year",Result."Allow Posting To");
        //SCourse.SETRANGE(SCourse.Semester,Result.Semester);
        IF SCourse.FINDFIRST THEN BEGIN
          CLEAR(CourseAssessment);
          CourseAssessment.INIT;
          CourseAssesmentLastEntryNo:=GetLastAssmtNumber+1;
          CourseAssessment.Line:=CourseAssesmentLastEntryNo;
          CourseAssessment."Student Registration No.":=Result."User ID";
          CourseAssessment."Programme Code":=Result."Allow Posting From";
          CourseAssessment."Academic Year":=Result."Allow Posting To";
          CourseAssessment."Programme Part":=Result.Part;
         // CourseAssessment."Programme Course Code":=Result."Programme Course Code";

          CourseAssessment."Posting Date":=TODAY;
          CourseAssessment."User ID":=USERID;

         // CourseAssessment."Exam Weight":=Result."Exam Weight";
         // CourseAssessment."Assessment Weight":=Result."Assessment Weight";
        // CourseAssessment."Other Exam Weight":=Result."Oral Exam Weight";


         // CourseAssessment."Assessment Mark":=Result."Assessment Mark";
         // CourseAssessment."Exam Mark":=Result."Exam Mark";
         // CourseAssessment."Otherl Exam Mark":=Result."Oral Exam Mark";
         // CourseAssessment."Overall Mark":=Result."Overall Mark";

          CourseAssessment.Classification:=Result.Classification;
         // CourseAssessment.Remark:=Result.Remark;

          CourseAssessment.Open:=TRUE;
          IF Result."Entry Type"=Result."Entry Type"::"2" THEN
            CourseAssessment."Entry Type":=CourseAssessment."Entry Type"::Course
          ELSE
            CourseAssessment."Entry Type":=CourseAssessment."Entry Type"::Part;

          CourseAssessment.INSERT(TRUE);
        END;
      END
      ELSE BEGIN
          CLEAR(CourseAssessment);
          CourseAssessment.INIT;
          CourseAssesmentLastEntryNo:=1;
          CourseAssessment.Line:=GetLastAssmtNumber+1;
          CourseAssessment."Student Registration No.":=Result."User ID";
          CourseAssessment."Programme Code":=Result."Allow Posting From";
          CourseAssessment."Academic Year":=Result."Allow Posting To";
          CourseAssessment."Programme Part":=Result.Part;
          //CourseAssessment."Programme Course Code":=Result."Programme Course Code";

          CourseAssessment."Posting Date":=TODAY;
          CourseAssessment."User ID":=USERID;

        //  CourseAssessment."Exam Weight":=Result."Exam Weight";
        //  CourseAssessment."Assessment Weight":=Result."Assessment Weight";
         // CourseAssessment."Other Exam Weight":=Result."Oral Exam Weight";


         // CourseAssessment."Assessment Mark":=Result."Assessment Mark";
         // CourseAssessment."Exam Mark":=Result."Exam Mark";
          //CourseAssessment."Otherl Exam Mark":=Result."Oral Exam Mark";
          //CourseAssessment."Overall Mark":=Result."Overall Mark";

          CourseAssessment.Classification:=Result.Classification;
          //CourseAssessment.Remark:=Result.Remark;

          CourseAssessment.Open:=TRUE;
          IF Result."Entry Type"=Result."Entry Type"::"2" THEN
            CourseAssessment."Entry Type":=CourseAssessment."Entry Type"::Course
          ELSE
            CourseAssessment."Entry Type":=CourseAssessment."Entry Type"::Part;
          CourseAssessment.INSERT(TRUE);
      END;
  UNTIL Result.NEXT=0;
COMMIT;
}

DeletePartAssessmentLines(ProgramCode : Code[10];ProgramPart : Integer;AcademicYear : Integer)
{
// Delete Continous Assessment Header
Result.RESET;
Result.SETRANGE(Result."Allow Posting From",ProgramCode);
Result.SETRANGE(Result."Allow Posting To",AcademicYear);
Result.SETRANGE(Result.Part,ProgramPart);
Result2:=Result;
IF Result.FIND('-') THEN BEGIN
  Result2.DELETEALL;
END;
}

GetLastAssmtNumber() : Integer
StudentCourseAssessment.RESET;
IF StudentCourseAssessment.FIND('+') THEN
  EXIT(StudentCourseAssessment."Entry No.")
ELSE
  EXIT(0);

CopyPostedContinousAssessment(VAR PostedCA : Record "Posted Continous Assmt. Header";Selection : Integer;VAR NewAssessment : Code[20])


// SECTION 1.8
//**********************************************************************************************************************************
    // REVERSING OF CONTINOUS ASSESMENT JOURNAL

    // This Function reverses the Continous journal lines and create
   { ORIGINAL CODE 30/11/13
    Selection := DIALOG.STRMENU('Reverse and Create a new journal,Reverse ,Cancel');


       IF Selection = 1 THEN BEGIN


        IF PostedCA.Type = PostedCA.Type::Aggregating THEN
           ERROR('You cannot reverse and create an Aggregating journal')

        ELSE
        CAHeader.INIT;
        CAHeader.LOCKTABLE;
        CAHeader.TRANSFERFIELDS(PostedCA,FALSE);
        CAHeader."Assessment No.":=PostedCA."Assessment No.";
        CAHeader."Creation Date":=TODAY;
        CAHeader."Created By":=USERID;
        CAHeader."Assigned User":= USERID;
        CAHeader.Reversal:=TRUE;
        CAHeader.INSERT;
        PostedCALine.RESET;

        PostedCALine.SETRANGE(PostedCALine."Assessment No.",PostedCA."Assessment No.");

        IF PostedCALine.FIND('-') THEN
         REPEAT
         CALine.INIT;
         CALine.LOCKTABLE;
         CALine.TRANSFERFIELDS(PostedCALine);
         CALine."Assessment No.":=(CAHeader."Assessment No.");
         CALine.INSERT;
         UNTIL PostedCALine.NEXT=0;
       END;

       //below we are finding the posted CA Header and moving them to  "Reversed Header".
        //Added by FIDE. Derera 06/06/2013
        ReversedCAHdr.INIT;
        ReversedCAHdr.LOCKTABLE;
        ReversedCAHdr.TRANSFERFIELDS(PostedCA,FALSE);
        ReversedCAHdr."Creation Date":=TODAY;
        ReversedCAHdr."Reversed By":=  USERID;
        ReversedCAHdr.Reversed:= TRUE;
        ReversedCAHdr."Assessment No.":=PostedCA."Assessment No.";
        ReversedCAHdr.INSERT;


      //below we are finding the posted CAlines and moving them to  "Reversed Exam Documents".
      PostedCALine.SETRANGE(PostedCALine."Assessment No.",PostedCA."Assessment No.");

        IF PostedCALine.FIND('-') THEN
          REPEAT
           IF "Reversed Exam Documents".FINDLAST THEN
               EntryNo := "Reversed Exam Documents"."Entry No" + 1;
              "Reversed Exam Documents".INIT;
              "Reversed Exam Documents"."Entry No" := EntryNo;
              "Reversed Exam Documents"."Programme Code" := PostedCALine."Programme Code";
              "Reversed Exam Documents"."Course Code" := PostedCALine."Course Code";
              "Reversed Exam Documents"."Assessment No." := PostedCALine."Assessment No.";
              "Reversed Exam Documents"."Student Registration No." := PostedCALine."Student Registration No.";
              "Reversed Exam Documents".Attended := PostedCALine.Attended;
              "Reversed Exam Documents"."Mark Attained (%)" := PostedCALine."Mark Attained (%)";
              "Reversed Exam Documents".Name := PostedCALine.Name;
              "Reversed Exam Documents".Surname := PostedCALine.Surname;
              "Reversed Exam Documents"."Mark Confirmed" := PostedCALine."Mark Confirmed";
              "Reversed Exam Documents"."Reversed By" := USERID;
              "Reversed Exam Documents"."Entry Type" := "Reversed Exam Documents"."Entry Type"::"Continous Assesment";
              "Reversed Exam Documents".INSERT;
          UNTIL PostedCALine.NEXT=0;

          StudentCourseAssesment.SETRANGE(StudentCourseAssesment."Document No",PostedCA."Assessment No.");
            IF StudentCourseAssesment.FIND('-') THEN

            REPEAT
            //MESSAGE('Test');
            StudentCourseAssesment.Reversed := TRUE;
            StudentCourseAssesment.MODIFY;
            UNTIL StudentCourseAssesment.NEXT = 0;

          DeleteReversed(PostedCA."Assessment No.");
    }
//**********************************************************************************************************************************
//AO-CCM-30/11/13 BEGIN CODE


//Selection := DIALOG.STRMENU(Text008);

PostedCA.TESTFIELD(Reversed,FALSE);
CASE PostedCA.Type OF
  PostedCA.Type::Contributing:
    BEGIN
      PostedCA2.RESET;
      PostedCA2.SETRANGE("Teaching Class Code",PostedCA."Teaching Class Code");
      PostedCA2.SETRANGE("Course Code",PostedCA."Course Code");
      PostedCA2.SETRANGE("Academic Year",PostedCA."Academic Year");
      PostedCA2.SETRANGE(Type,PostedCA.Type::Aggregating);
      PostedCA2.SETRANGE("Programme Part",PostedCA."Programme Part");
      PostedCA2.SETRANGE(Semester,PostedCA.Semester);
      PostedCA2.SETRANGE(Reversed,FALSE);
      IF PostedCA2.FINDFIRST THEN
        ERROR(Text007,PostedCA.TABLECAPTION,PostedCA.FIELDCAPTION(PostedCA."Assessment No."),PostedCA."Assessment No.",
        PostedCA2.TABLECAPTION,PostedCA2.FIELDCAPTION(PostedCA2."Assessment No."),PostedCA2."Assessment No.");

      PostedCALine.RESET;
      PostedCALine.SETRANGE("Assessment No.",PostedCA."Assessment No.");
      IF PostedCALine.FINDSET THEN
        REPEAT
          PostedCALine.Reversed := TRUE;
          PostedCALine."Reversed By" := USERID;
          PostedCALine."Reversed On" := TODAY;
          PostedCALine.MODIFY;
        UNTIL PostedCALine.NEXT = 0;

      PostedCA.Reversed := TRUE;
      PostedCA."Reversed By" := USERID;
      PostedCA."Reversed On" := TODAY;
      PostedCA.MODIFY;

      IF Selection = 1 THEN BEGIN
        ContAssessHdr1.RESET;
        ContAssessLine.RESET;
        ContAssessHdr1.INIT;
        ContAssessHdr1.TRANSFERFIELDS(PostedCA);
        ContAssessHdr1."Assessment No." := '';
        ContAssessHdr1.INSERT(TRUE);
        ContAssessHdr1.SuggestContAssmtLines(FALSE);
        ContAssessLine.SETRANGE("Assessment No.",ContAssessHdr1."Assessment No.");
        IF ContAssessLine.FINDSET THEN
          REPEAT
            PostedCALine.SETRANGE("Student Registration No.",ContAssessLine."Student Registration No.");
            IF PostedCALine.FINDFIRST THEN BEGIN
              ContAssessLine."Mark Attained (%)" := PostedCALine."Mark Attained (%)";
              ContAssessLine.Attended := PostedCALine.Attended;
              ContAssessLine."Mark Confirmed" := PostedCALine."Mark Confirmed";
              ContAssessLine.MODIFY;
            END;
          UNTIL ContAssessLine.NEXT = 0;
        NewAssessment := ContAssessHdr1."Assessment No.";
      END;
    END;

 PostedCA.Type::Aggregating:
  BEGIN
     StudentCourseAssesment.RESET;
     StudentCourseAssesment.SETCURRENTKEY("Document No");
     StudentCourseAssesment.SETRANGE(StudentCourseAssesment."Document No",PostedCA."Assessment No.");
     IF StudentCourseAssesment.FINDSET THEN
      REPEAT
        StudentCourseAssesment.ResultOpen := FALSE;
        StudentCourseAssesment.Reversed := TRUE;
        StudentCourseAssesment.MODIFY;
      UNTIL StudentCourseAssesment.NEXT = 0;

      PostedCALine.RESET;
      PostedCALine.SETRANGE("Assessment No.",PostedCA."Assessment No.");
      IF PostedCALine.FINDSET THEN
        REPEAT
          PostedCALine.Reversed := TRUE;
          PostedCALine."Reversed By" := USERID;
          PostedCALine."Reversed On" := TODAY;
          PostedCALine.MODIFY;
        UNTIL PostedCALine.NEXT = 0;

      PstdAssmntContribution.RESET;
      PstdAssmntContribution.SETRANGE("Assessment No.",PostedCA."Assessment No.");
      PstdAssmntContribution.MODIFYALL(Reversed,TRUE);


      PostedCA.Reversed := TRUE;
      PostedCA."Reversed By" := USERID;
      PostedCA."Reversed On" := TODAY;
      PostedCA.MODIFY;
  END;
END;

//AO-CCM-30/11/13 END CODE

DeleteReversed(CACode : Code[10])

//SECTION 1.9

//**********************************************************************************************************************************
     //        DELETE REVERSED CONTINOUS ASSESMENT LINES

   //----------Find the header and the set of lines and delete them

          ReversedCAHdr.RESET;
          ReversedCAHdr.SETRANGE(ReversedCAHdr."Assessment No.",CACode);
          ReversedCAHdr.FIND('-');
          ReversedCAHdr.DELETE(TRUE);

          ReversedCALines.RESET;
          ReversedCALines.SETRANGE(ReversedCALines."Assessment No.",CACode);
          IF ReversedCALines.FINDSET() THEN
             ReversedCALines.DELETEALL(TRUE);

          Contibutions.SETRANGE(Contibutions."Assessment No.",CACode);
            IF Contibutions.FIND('-') THEN
               REPEAT
               Contibutions.Reversed := TRUE;
               UNTIL Contibutions.NEXT = 0;

//**********************************************************************************************************************************

Reverse Course Assesment("Exam Code" : Code[10];"Course Code" : Code[10])

//SECTION 3
//**********************************************************************************************************************************
// PICKING THE OPTION
   Selector := DIALOG.STRMENU('Reverse and Create a new journal,Reverse ,Cancel');

//**********************************************************************************************************************************
   // GETTING THE LAST ENTRY NUMBER USED IN THE POSTED EXAM DOCUMENTS
   {IF "Reversed Exam Documents".FIND('+') THEN
       EntryNo := "Reversed Exam Documents"."Entry No"+1
       ELSE
       EntryNo := 1;

  //--------------REVERSING THE COURSE ASSESMENT JOURNAL

  "Posted Exam Header".SETRANGE("Posted Exam Header"."Exam Code","Exam Code");
  "Posted Exam Header".SETRANGE("Posted Exam Header"."Course Code","Course Code");
    IF "Posted Exam Header".FIND('-') THEN
       "Posted Course ass Lines".SETRANGE("Posted Course ass Lines"."Examination Code","Posted Exam Header"."Exam Code");
       "Posted Course ass Lines".SETRANGE("Posted Course ass Lines"."Course Code","Posted Exam Header"."Course Code");


       IF "Posted Course ass Lines".FIND('-') THEN BEGIN
           Exam.SETRANGE(Exam.Code,"Posted Exam Header"."Exam Code");
            IF Exam.FIND('-') THEN BEGIN
               Exam.Status := Exam.Status::"5";
               Exam."Marks Posted" := FALSE;
               Exam.MODIFY;
               END;

       REPEAT
         IF Selector = 1 THEN BEGIN
         "Course Assesment lines".TRANSFERFIELDS("Posted Course ass Lines");
         "Course Assesment lines".INSERT;
             END;
//----------Inserting in the posted exam documents
    "Reversed Exam Documents".INIT;
    "Reversed Exam Documents"."Entry No" := EntryNo;
    "Reversed Exam Documents"."Programme Code" := "Posted Course ass Lines"."Programme Code";
    "Reversed Exam Documents"."Course Code" := "Posted Course ass Lines"."Course Code";
    "Reversed Exam Documents"."Academic Year" := "Posted Course ass Lines"."Academic Year";
    "Reversed Exam Documents"."Student Registration No." := "Posted Course ass Lines"."Student Registration No.";
    "Reversed Exam Documents"."No.":= "Posted Course ass Lines".Surname;
    "Reversed Exam Documents".Name := "Posted Course ass Lines".Name;
    "Reversed Exam Documents"."Mark Attained (%)" :=
    ROUND("Posted Course ass Lines"."Overall Mark",ExaminationSetup."Mark Rounding Precision",'=');;
    "Reversed Exam Documents"."Document No" := "Posted Course ass Lines"."Examination Code";
    "Reversed Exam Documents".Version := "Reversed Exam Documents".Version::"2";

   "Reversed Exam Documents".INSERT;
        EntryNo := EntryNo+1;

         UNTIL "Posted Course ass Lines".NEXT=0;

// UPDATING THE STUDENT COURSE TABLE------------------------------------------------------------------------------------------------

     "Student Course Assesment".SETRANGE("Student Course Assesment"."Document No","Exam Code");
       IF "Student Course Assesment".FIND('-') THEN
       REPEAT
       "Student Course Assesment".Reversed := TRUE;
       "Student Course Assesment".MODIFY;
       UNTIL "Student Course Assesment".NEXT = 0;

//------------Deleting the records--------------------------------------------------------------------------------------------------

       "Posted Course ass Lines".SETRANGE("Posted Course ass Lines"."Examination Code","Posted Exam Header"."Exam Code");
       "Posted Course ass Lines".SETRANGE("Posted Course ass Lines"."Course Code","Posted Exam Header"."Course Code");
          IF "Posted Course ass Lines".FINDSET THEN
             "Posted Course ass Lines".DELETEALL;
              END;

        "Posted Exam Header".SETRANGE("Posted Exam Header"."Exam Code","Exam Code");
        "Posted Exam Header".SETRANGE("Posted Exam Header"."Course Code","Course Code");
           IF "Posted Exam Header".FINDSET THEN
            "Posted Exam Header".DELETEALL;

             MESSAGE(Text001);
             }
//**********************************************************************************************************************************

PostOverrallDegree(DegreeClassficationJournal : Record "Assessment Journal")

//**********************************************************************************************************************************

  // write code which posts the overall degree classficatiion
  IF "Student Course Assesment".FIND('+') THEN
      NewNumber := "Student Course Assesment"."Entry No." + 1;

      //MESSAGE('The new number is %1',NewNumber);

      DegreeClassficationJournal.SETRANGE(DegreeClassficationJournal.Processed,FALSE);
         IF DegreeClassficationJournal.FIND('-') THEN BEGIN

            REPEAT

            {
            "Student Course Assesment".SETRANGE("Student Course Assesment"."Student Registration No.",
            DegreeClassficationJournal."Student No.");
               IF "Student Course Assesment".FIND('-') THEN
                  REPEAT
                 }


            "Student Course Assesment".INIT;
            "Student Course Assesment"."Entry No." := NewNumber;
            "Student Course Assesment"."Student Registration No." := DegreeClassficationJournal."Student No.";
            "Student Course Assesment"."Teaching Class Code" := DegreeClassficationJournal."Programme Code";
            "Student Course Assesment".AcademicYear  := AcademikYear;
            "Student Course Assesment"."Overall Mark" := DegreeClassficationJournal."Overall Mark";
            "Student Course Assesment"."User ID" := USERID;
            "Student Course Assesment"."Posting Date" := TODAY;
            "Student Course Assesment"."Entry Type" := "Student Course Assesment"."Entry Type"::Overall;
            //"Student Course Assesment"."Document No" := DocumentNumber

            "Student Course Assesment".INSERT;
             NewNumber := NewNumber+1;

             "Student Course Assesment".SETRANGE("Student Course Assesment"."Student Registration No.",
             DegreeClassficationJournal."Student No.");
                IF "Student Course Assesment".FIND('-') THEN
                    REPEAT
                    "Student Course Assesment"."Programme Classfied" := TRUE;
                    "Student Course Assesment".MODIFY;

                    UNTIL "Student Course Assesment".NEXT = 0;

                      //MESSAGE
             //MESSAGE('The new number is %1',NewNumber);
           UNTIL DegreeClassficationJournal.NEXT = 0;

           MESSAGE(Text001);
           END;

DateNotAllowed(PostingDate : Date) : Boolean
IF (AllowPostingFrom = 0D) AND (AllowPostingTo = 0D) THEN BEGIN
  IF USERID <> '' THEN
    IF AcademicUserSetup.GET(USERID) THEN BEGIN
      AllowPostingFrom := AcademicUserSetup."Allow Posting From";
      AllowPostingTo := AcademicUserSetup."Allow Posting To";
    END;
  IF (AllowPostingFrom = 0D) AND (AllowPostingTo = 0D) THEN BEGIN
    ExaminationSetup.GET;
    AllowPostingFrom := ExaminationSetup."Allow Posting From";
    AllowPostingTo := ExaminationSetup."Allow Posting To";
  END;

  IF AllowPostingTo = 0D THEN
    AllowPostingTo := 12319999D;
END;
EXIT((PostingDate < AllowPostingFrom) OR (PostingDate > AllowPostingTo));

IsLecturer() : Boolean
IF NOT AcademicUserSetup.GET(USERID) THEN
  EXIT(FALSE);

IF AcademicUserSetup.Lecturer THEN
  EXIT(TRUE)
ELSE
  EXIT(FALSE);

StudCourAssCalcOveralMark(Result : Record "Student Course Assessment")

//Changes made in any one of CourAssJnlLineCalcOveralMark(Result : Record "Course Assessment Journal Line") and
//StudCourAssCalcOveralMark(Result : Record "Student Course Assessment") should be synchronised

Exam.GET(Result."Document No");
ExaminationSetup.GET;
ExaminationSetup.TESTFIELD("Mark Rounding Precision");
//since the weight fields in the Std Cors Ass table are not calc fields get them from programm course table.
//ProgCourse key: Programme Code,Academic Year,Programme Part,Semester,Code
ProgCourse.RESET;
IF ProgCourse.GET(Exam."Programme Class",Exam."Academic Year",Exam."Programme Part",Exam.Semester,Exam."Course Code")
                  THEN BEGIN

  Result."Exam Weight":=ProgCourse."Examination Weight";
  Result."Assessment Weight":=ProgCourse."Continous Assesment Weight";
  Result."Other Exam Weight":=ProgCourse."Other Examination Weight";
//  Result.MODIFY;  // do we need to modify at this stage?
  //Make Sure Weights are equal to the Programme Course tabe weights need more reading
  Result.TESTFIELD("Exam Weight",ProgCourse."Examination Weight");
  Result.TESTFIELD("Assessment Weight",ProgCourse."Continous Assesment Weight");
  Result.TESTFIELD("Other Exam Weight",ProgCourse."Other Examination Weight");
  WeightTotal:= Result."Exam Weight" + Result."Other Exam Weight" + Result."Assessment Weight";

  IF WeightTotal <> 100 THEN //percentage
      ERROR(Text002,Exam."Programme Class",Exam."Academic Year",Exam."Programme Part",Exam.Semester);
END ELSE
  ERROR(Text001,Exam."Programme Class",Exam."Academic Year",Exam."Programme Part",Exam.Semester);

IF Exam."Exam Type" = Exam."Exam Type"::Normal THEN BEGIN

    Result."Overall Mark":=((Result."Exam Mark"*Result."Exam Weight")+
    (Result."Assessment Mark"*Result."Assessment Weight")+
    (Result."Other Exam Mark"*Result."Other Exam Weight"))
    /(Result."Exam Weight"+Result."Assessment Weight"+
    Result."Other Exam Weight");

    Result."Overall Mark" := ROUND(
    Result."Overall Mark",ExaminationSetup."Mark Rounding Precision",'=');
//    Result.MODIFY;

// calculate the Classification here and make it a function as well

    Classification1.SETCURRENTKEY("Mark Greater or Equal To");
    Classification1.SETFILTER("Mark Greater or Equal To",'<=%1',Result."Overall Mark");
    Classification1.SETRANGE(Classification1."Programme Code",Result."Teaching Class Code");
    Classification1.SETRANGE("Assessment Type",Classification1."Assessment Type"::Normal);
    IF Classification1.FINDLAST THEN
      IF Result."Overall Mark" >= Classification1."Mark Greater or Equal To" THEN BEGIN
       Result.Classification := Classification1.Classification;
       Result.Remark := Classification1.Remark;
      END;

  Result.MODIFY;
  END
ELSE BEGIN
  ExaminationSetup.TESTFIELD("Supplementary Pass Mark");
  ExaminationSetup.TESTFIELD("Supplementary Classification");
  ExaminationSetup.TESTFIELD("Supplementary Pass Remark");
  ExaminationSetup.TESTFIELD("Supplementary Fail Remark");
  ExaminationSetup.TESTFIELD("Suppl. Fail Classification");
  Result."Overall Mark":=((Result."Exam Mark"*Result."Exam Weight")+
    (Result."Assessment Mark"*Result."Assessment Weight")+
    (Result."Other Exam Mark"*Result."Other Exam Weight"))
    /(Result."Exam Weight"+Result."Assessment Weight"+
  Result."Other Exam Weight");
  Result."Overall Mark" := ROUND(Result."Overall Mark",
  ExaminationSetup."Mark Rounding Precision",'=');
  IF Result."Overall Mark" >= ExaminationSetup."Supplementary Pass Mark" THEN BEGIN
    Result."Overall Mark" := ExaminationSetup."Supplementary Pass Mark";
    Result.Classification := ExaminationSetup."Supplementary Classification";
    Result.Remark := ExaminationSetup."Supplementary Pass Remark";
  END ELSE BEGIN
    Result.Classification := ExaminationSetup."Suppl. Fail Classification";
    Result.Remark := ExaminationSetup."Supplementary Fail Remark";
  END;
  Result.MODIFY;
END

StudCourAssCalcOveralMark2(Result : Record "Student Course Assessment")

//Changes made in any one of CourAssJnlLineCalcOveralMark(Result : Record "Course Assessment Journal Line") and
//StudCourAssCalcOveralMark(Result : Record "Student Course Assessment") should be synchronised

Exam.GET(Result."Document No");
ExaminationSetup.GET;
ExaminationSetup.TESTFIELD("Mark Rounding Precision");
//since the weight fields in the Std Cors Ass table are not calc fields get them from programm course table.
//ProgCourse key: Programme Code,Academic Year,Programme Part,Semester,Code
ProgCourse.RESET;
IF ProgCourse.GET(Exam."Programme Class",Exam."Academic Year",Exam."Programme Part",Exam.Semester,Exam."Course Code")
                  THEN BEGIN

  Result."Exam Weight":=ProgCourse."Examination Weight";
  Result."Assessment Weight":=ProgCourse."Continous Assesment Weight";
  Result."Other Exam Weight":=ProgCourse."Other Examination Weight";
//  Result.MODIFY;  // do we need to modify at this stage?
  //Make Sure Weights are equal to the Programme Course tabe weights need more reading
  Result.TESTFIELD("Exam Weight",ProgCourse."Examination Weight");
  Result.TESTFIELD("Assessment Weight",ProgCourse."Continous Assesment Weight");
  Result.TESTFIELD("Other Exam Weight",ProgCourse."Other Examination Weight");
  WeightTotal:= Result."Exam Weight" + Result."Other Exam Weight" + Result."Assessment Weight";

  IF WeightTotal <> 100 THEN //percentage
      ERROR(Text002,Exam."Programme Class",Exam."Academic Year",Exam."Programme Part",Exam.Semester);
END ELSE
  ERROR(Text001,Exam."Programme Class",Exam."Academic Year",Exam."Programme Part",Exam.Semester);

IF Exam."Exam Type" = Exam."Exam Type"::Normal THEN BEGIN

    Result."Overall Mark":=((Result."Exam Mark"*Result."Exam Weight")+
    (Result."Assessment Mark"*Result."Assessment Weight")+
    (Result."Other Exam Mark"*Result."Other Exam Weight"))
    /(Result."Exam Weight"+Result."Assessment Weight"+
    Result."Other Exam Weight");

    Result."Overall Mark" := ROUND(
    Result."Overall Mark",ExaminationSetup."Mark Rounding Precision",'=');
//    Result.MODIFY;

// calculate the Classification here and make it a function as well

    Classification2.SETCURRENTKEY("Mark Greater or Equal To");
    Classification2.SETFILTER("Mark Greater or Equal To",'<=%1',Result."Overall Mark");
    Classification2.SETRANGE(Classification2."Programme Code",Result."Teaching Class Code");
    Classification2.SETRANGE("Assessment Type",Classification2."Assessment Type"::Normal);
    IF Classification2.FINDLAST THEN
      IF Result."Overall Mark" >= Classification2."Mark Greater or Equal To" THEN BEGIN
       Result.Classification := Classification2.Classification;
       Result.Remark := Classification2.Remark;
      END;

  Result.MODIFY;
  END
ELSE BEGIN
  ExaminationSetup.TESTFIELD("Supplementary Pass Mark");
  ExaminationSetup.TESTFIELD("Supplementary Classification");
  ExaminationSetup.TESTFIELD("Supplementary Pass Remark");
  ExaminationSetup.TESTFIELD("Supplementary Fail Remark");
  ExaminationSetup.TESTFIELD("Suppl. Fail Classification");
  Result."Overall Mark":=((Result."Exam Mark"*Result."Exam Weight")+
    (Result."Assessment Mark"*Result."Assessment Weight")+
    (Result."Other Exam Mark"*Result."Other Exam Weight"))
    /(Result."Exam Weight"+Result."Assessment Weight"+
  Result."Other Exam Weight");
  Result."Overall Mark" := ROUND(Result."Overall Mark",
  ExaminationSetup."Mark Rounding Precision",'=');
  IF Result."Overall Mark" >= ExaminationSetup."Supplementary Pass Mark" THEN BEGIN
    Result."Overall Mark" := ExaminationSetup."Supplementary Pass Mark";
    Result.Classification := ExaminationSetup."Supplementary Classification";
    Result.Remark := ExaminationSetup."Supplementary Pass Remark";
  END ELSE BEGIN
    Result.Classification := ExaminationSetup."Suppl. Fail Classification";
    Result.Remark := ExaminationSetup."Supplementary Fail Remark";
  END;
  Result.MODIFY;
END

CourAssJnlLineCalcOveralMark(Result : Record "Posted Course Assessment Jnl")

//Changes made in any one of CourAssJnlLineCalcOveralMark(Result : Record "Course Assessment Journal Line") and
//StudCourAssCalcOveralMark(Result : Record "Student Course Assessment") should be synchronised

Exam.GET(Result."Examination Code");
ExaminationSetup.GET;
ExaminationSetup.TESTFIELD("Mark Rounding Precision");
//since the weight fields in the Std Cors Ass table are not calc fields get them from programm course table.
//ProgCourse key: Programme Code,Academic Year,Programme Part,Semester,Code
ProgCourse.RESET;
IF ProgCourse.GET(Exam."Programme Class",Exam."Academic Year",Exam."Programme Part",Exam.Semester,Exam."Course Code")
                  THEN BEGIN

  Result."Exam Weight":=ProgCourse."Examination Weight";
  Result."Assessment Weight":=ProgCourse."Continous Assesment Weight";
  Result."Other Exam Weight":=ProgCourse."Other Examination Weight";
//  Result.MODIFY;  // do we need to modify at this stage?
  //Make Sure Weights are equal to the Programme Course tabe weights need more reading
  Result.TESTFIELD("Exam Weight",ProgCourse."Examination Weight");
  Result.TESTFIELD("Assessment Weight",ProgCourse."Continous Assesment Weight");
  Result.TESTFIELD("Other Exam Weight",ProgCourse."Other Examination Weight");
  WeightTotal:= Result."Exam Weight" + Result."Other Exam Weight" +
                     Result."Assessment Weight";
  IF WeightTotal <> 100 THEN //percentage
      ERROR(Text002,Exam."Programme Class",Exam."Academic Year",Exam."Programme Part",Exam.Semester);
END ELSE
  ERROR(Text001,Exam."Programme Class",Exam."Academic Year",Exam."Programme Part",Exam.Semester);

IF Exam."Exam Type" = Exam."Exam Type"::Normal THEN BEGIN

    Result."Overall Mark":=((Result."Exam Mark"*Result."Exam Weight")+
    (Result."Assessment Mark"*Result."Assessment Weight")+
    (Result."Other Exam Mark"*Result."Other Exam Weight"))
    /(Result."Exam Weight"+Result."Assessment Weight"+
    Result."Other Exam Weight");

    Result."Overall Mark" := ROUND(
    Result."Overall Mark",ExaminationSetup."Mark Rounding Precision",'=');
//    Result.MODIFY;

// calculate the Classification here and make it a function as well

    Classification1.SETCURRENTKEY("Mark Greater or Equal To");
    Classification1.SETFILTER("Mark Greater or Equal To",'<=%1',Result."Overall Mark");
    Classification1.SETRANGE(Classification1."Programme Code",Result."Programme Code");
    Classification1.SETRANGE("Assessment Type",Classification1."Assessment Type"::Normal);
    IF Classification1.FINDLAST THEN
      IF Result."Overall Mark" >= Classification1."Mark Greater or Equal To" THEN BEGIN
       Result.Classification := Classification1.Classification;
       Result.Remarks := Classification1.Remark;
      END;

  Result.MODIFY;
  END
ELSE BEGIN
  ExaminationSetup.TESTFIELD("Supplementary Pass Mark");
  ExaminationSetup.TESTFIELD("Supplementary Classification");
  ExaminationSetup.TESTFIELD("Supplementary Pass Remark");
  ExaminationSetup.TESTFIELD("Supplementary Fail Remark");
  ExaminationSetup.TESTFIELD("Suppl. Fail Classification");
  Result."Overall Mark":=((Result."Exam Mark"*Result."Exam Weight")+
    (Result."Assessment Mark"*Result."Assessment Weight")+
    (Result."Other Exam Mark"*Result."Other Exam Weight"))
    /(Result."Exam Weight"+Result."Assessment Weight"+
  Result."Other Exam Weight");
  Result."Overall Mark" := ROUND(Result."Overall Mark",
  ExaminationSetup."Mark Rounding Precision",'=');
  IF Result."Overall Mark" >= ExaminationSetup."Supplementary Pass Mark" THEN BEGIN
    Result."Overall Mark" := ExaminationSetup."Supplementary Pass Mark";
    Result.Classification := ExaminationSetup."Supplementary Classification";
    Result.Remarks := ExaminationSetup."Supplementary Pass Remark";
  END ELSE BEGIN
    Result.Classification := ExaminationSetup."Suppl. Fail Classification";
    Result.Remarks := ExaminationSetup."Supplementary Fail Remark";
  END;
  Result.MODIFY;
END

CourAssJnlLineCalcOveralMark2(Result : Record "Posted Course Assessment Jnl")

//Changes made in any one of CourAssJnlLineCalcOveralMark(Result : Record "Course Assessment Journal Line") and
//StudCourAssCalcOveralMark(Result : Record "Student Course Assessment") should be synchronised

Exam.GET(Result."Examination Code");
ExaminationSetup.GET;
ExaminationSetup.TESTFIELD("Mark Rounding Precision");
//since the weight fields in the Std Cors Ass table are not calc fields get them from programm course table.
//ProgCourse key: Programme Code,Academic Year,Programme Part,Semester,Code
ProgCourse.RESET;
IF ProgCourse.GET(Exam."Programme Class",Exam."Academic Year",Exam."Programme Part",Exam.Semester,Exam."Course Code")
                  THEN BEGIN

  Result."Exam Weight":=ProgCourse."Examination Weight";
  Result."Assessment Weight":=ProgCourse."Continous Assesment Weight";
  Result."Other Exam Weight":=ProgCourse."Other Examination Weight";
//  Result.MODIFY;  // do we need to modify at this stage?
  //Make Sure Weights are equal to the Programme Course tabe weights need more reading
  Result.TESTFIELD("Exam Weight",ProgCourse."Examination Weight");
  Result.TESTFIELD("Assessment Weight",ProgCourse."Continous Assesment Weight");
  Result.TESTFIELD("Other Exam Weight",ProgCourse."Other Examination Weight");
  WeightTotal:= Result."Exam Weight" + Result."Other Exam Weight" +
                     Result."Assessment Weight";
  IF WeightTotal <> 100 THEN //percentage
      ERROR(Text002,Exam."Programme Class",Exam."Academic Year",Exam."Programme Part",Exam.Semester);
END ELSE
  ERROR(Text001,Exam."Programme Class",Exam."Academic Year",Exam."Programme Part",Exam.Semester);

IF Exam."Exam Type" = Exam."Exam Type"::Normal THEN BEGIN

    Result."Overall Mark":=((Result."Exam Mark"*Result."Exam Weight")+
    (Result."Assessment Mark"*Result."Assessment Weight")+
    (Result."Other Exam Mark"*Result."Other Exam Weight"))
    /(Result."Exam Weight"+Result."Assessment Weight"+
    Result."Other Exam Weight");

    Result."Overall Mark" := ROUND(
    Result."Overall Mark",ExaminationSetup."Mark Rounding Precision",'=');
//    Result.MODIFY;

// calculate the Classification here and make it a function as well

    Classification2.SETCURRENTKEY("Mark Greater or Equal To");
    Classification2.SETFILTER("Mark Greater or Equal To",'<=%1',Result."Overall Mark");
    Classification2.SETRANGE(Classification2."Programme Code",Result."Programme Code");
    Classification2.SETRANGE("Assessment Type",Classification2."Assessment Type"::Normal);
    IF Classification2.FINDLAST THEN
      IF Result."Overall Mark" >= Classification2."Mark Greater or Equal To" THEN BEGIN
       Result.Classification := Classification2.Classification;
       Result.Remarks := Classification2.Remark;
      END;

  Result.MODIFY;
  END
ELSE BEGIN
  ExaminationSetup.TESTFIELD("Supplementary Pass Mark");
  ExaminationSetup.TESTFIELD("Supplementary Classification");
  ExaminationSetup.TESTFIELD("Supplementary Pass Remark");
  ExaminationSetup.TESTFIELD("Supplementary Fail Remark");
  ExaminationSetup.TESTFIELD("Suppl. Fail Classification");
  Result."Overall Mark":=((Result."Exam Mark"*Result."Exam Weight")+
    (Result."Assessment Mark"*Result."Assessment Weight")+
    (Result."Other Exam Mark"*Result."Other Exam Weight"))
    /(Result."Exam Weight"+Result."Assessment Weight"+
  Result."Other Exam Weight");
  Result."Overall Mark" := ROUND(Result."Overall Mark",
  ExaminationSetup."Mark Rounding Precision",'=');
  IF Result."Overall Mark" >= ExaminationSetup."Supplementary Pass Mark" THEN BEGIN
    Result."Overall Mark" := ExaminationSetup."Supplementary Pass Mark";
    Result.Classification := ExaminationSetup."Supplementary Classification";
    Result.Remarks := ExaminationSetup."Supplementary Pass Remark";
  END ELSE BEGIN
    Result.Classification := ExaminationSetup."Suppl. Fail Classification";
    Result.Remarks := ExaminationSetup."Supplementary Fail Remark";
  END;
  Result.MODIFY;
END

StudCourAssCalcOveralMarkImpor(Result : Record "Student Course Assessment")

//Changes made in any one of CourAssJnlLineCalcOveralMark(Result : Record "Course Assessment Journal Line") and
//StudCourAssCalcOveralMark(Result : Record "Student Course Assessment") should be synchronised

//Exam.GET(Result."Document No");

ExaminationSetup.GET;
ExaminationSetup.TESTFIELD("Mark Rounding Precision");

//since the weight fields in the Std Cors Ass table are not calc fields get them from programm course table.
//ProgCourse key: Programme Code,Academic Year,Programme Part,Semester,Code

ProgCourse.RESET;
IF ProgCourse.GET(Result."Teaching Class Code",Result.AcademicYear,Result."Programme Part",Result.Semester,
Result."Programme Course Code")
                  THEN BEGIN

  Result."Exam Weight":=ProgCourse."Examination Weight";
  Result."Assessment Weight":=ProgCourse."Continous Assesment Weight";
  Result."Other Exam Weight":=ProgCourse."Other Examination Weight";
//  Result.MODIFY;  // do we need to modify at this stage?
  //Make Sure Weights are equal to the Programme Course tabe weights need more reading
  Result.TESTFIELD("Exam Weight",ProgCourse."Examination Weight");
  Result.TESTFIELD("Assessment Weight",ProgCourse."Continous Assesment Weight");
  Result.TESTFIELD("Other Exam Weight",ProgCourse."Other Examination Weight");
  WeightTotal:= Result."Exam Weight" + Result."Other Exam Weight" + Result."Assessment Weight";

  IF WeightTotal <> 100 THEN //percentage
      ERROR(Text002,Result."Teaching Class Code",Result.AcademicYear,Result."Programme Part",Result.Semester,
      Result."Programme Course Code");
END; //ELSE
//  ERROR(Text001,Result."Programme Code",Result."Academic Year",Result."Programme Part",Result.Semester);

//IF Exam."Exam Type" = Exam."Exam Type"::Normal THEN BEGIN
IF TRUE THEN BEGIN
    Result."Overall Mark":=((Result."Exam Mark"*Result."Exam Weight")+
    (Result."Assessment Mark"*Result."Assessment Weight")+
    (Result."Other Exam Mark"*Result."Other Exam Weight"))
    /(Result."Exam Weight"+Result."Assessment Weight"+
    Result."Other Exam Weight");

    Result."Overall Mark" := ROUND(
    Result."Overall Mark",ExaminationSetup."Mark Rounding Precision",'=');
//    Result.MODIFY;

// calculate the Classification here and make it a function as well

    Classification1.SETCURRENTKEY("Mark Greater or Equal To");
    Classification1.SETFILTER("Mark Greater or Equal To",'<=%1',Result."Overall Mark");
    Classification1.SETRANGE(Classification1."Programme Code",Result."Teaching Class Code");
    Classification1.SETRANGE("Assessment Type",Classification1."Assessment Type"::Normal);
    IF Classification1.FINDLAST THEN
      IF Result."Overall Mark" >= Classification1."Mark Greater or Equal To" THEN BEGIN
       Result.Classification := Classification1.Classification;
       Result.Remark := Classification1.Remark;
      END;

  Result.MODIFY;
  END
ELSE BEGIN
  ExaminationSetup.TESTFIELD("Supplementary Pass Mark");
  ExaminationSetup.TESTFIELD("Supplementary Classification");
  ExaminationSetup.TESTFIELD("Supplementary Pass Remark");
  ExaminationSetup.TESTFIELD("Supplementary Fail Remark");
  ExaminationSetup.TESTFIELD("Suppl. Fail Classification");
  Result."Overall Mark":=((Result."Exam Mark"*Result."Exam Weight")+
    (Result."Assessment Mark"*Result."Assessment Weight")+
    (Result."Other Exam Mark"*Result."Other Exam Weight"))
    /(Result."Exam Weight"+Result."Assessment Weight"+
  Result."Other Exam Weight");
  Result."Overall Mark" := ROUND(Result."Overall Mark",
  ExaminationSetup."Mark Rounding Precision",'=');
  IF Result."Overall Mark" >= ExaminationSetup."Supplementary Pass Mark" THEN BEGIN
    Result."Overall Mark" := ExaminationSetup."Supplementary Pass Mark";
    Result.Classification := ExaminationSetup."Supplementary Classification";
    Result.Remark := ExaminationSetup."Supplementary Pass Remark";
  END ELSE BEGIN
    Result.Classification := ExaminationSetup."Suppl. Fail Classification";
    Result.Remark := ExaminationSetup."Supplementary Fail Remark";
  END;
  Result.MODIFY;
END

StudentBalanceAnalysis(StudentNo : Code[20])
Customer.GET(StudentNo);
IF Customer."On Cadetship" THEN BEGIN
  Customer."Result Programme Code" := Customer."Class Code";
  Customer."Result Academic Year" := Customer."Current Academic Year";
  Customer."Result Programme Part" := Customer."Programme Part";
  Customer."Result Semester"  :=Customer."Semester Part" ;
  Customer.MODIFY;
END ELSE BEGIN
  CustLedgerEntry.SETCURRENTKEY("Customer No.",Positive,Open,"Academic Year","Programme Part",Semester);
  CustLedgerEntry.SETRANGE("Customer No.",Customer."No.");
  CustLedgerEntry.SETRANGE(Positive,TRUE);

  IF CustLedgerEntry.ISEMPTY THEN BEGIN
    CLEAR(Customer."Result Programme Code");
    CLEAR(Customer."Result Academic Year");
    CLEAR(Customer."Result Programme Part");
    CLEAR(Customer."Result Semester");
    Customer.MODIFY;
  END ELSE BEGIN
    CustLedgerEntry.SETRANGE(Open,TRUE);
    IF CustLedgerEntry.FINDFIRST THEN BEGIN
      FirstUnpaidAcademicYear  := CustLedgerEntry."Academic Year";
      FirstUnpaidStudentSemester := CustLedgerEntry.Semester;
      FirstUnpaidStudentPart := CustLedgerEntry."Programme Part";
    END;
    CustLedgerEntry.SETRANGE(Open,FALSE);
    IF CustLedgerEntry.FINDLAST THEN BEGIN
      LastPaidAcademicYear  := CustLedgerEntry."Academic Year";
      LastPaidStudentSemester := CustLedgerEntry.Semester;
      LastPaidStudentPart := CustLedgerEntry."Programme Part";
    END;

    IF ((FirstUnpaidAcademicYear=LastPaidAcademicYear) AND (FirstUnpaidStudentSemester=LastPaidStudentSemester)) THEN BEGIN
      CASE FirstUnpaidStudentSemester OF
        FirstUnpaidStudentSemester::"0":
          BEGIN
            CLEAR(Customer."Result Programme Code");
            CLEAR(Customer."Result Academic Year");
            CLEAR(Customer."Result Programme Part");
            CLEAR(Customer."Result Semester");
            Customer.MODIFY;
          END;
        FirstUnpaidStudentSemester::"3":
          BEGIN
            Customer."Result Programme Code" := CustLedgerEntry."Programme Code";
            Customer."Result Academic Year" := FirstUnpaidAcademicYear;
            Customer."Result Programme Part" := LastPaidStudentPart;
            Customer."Result Semester"  := FirstUnpaidStudentSemester::"2";
            Customer.MODIFY;
          END;
        FirstUnpaidStudentSemester::"2":
          BEGIN
            Customer."Result Programme Code" := CustLedgerEntry."Programme Code";
            Customer."Result Academic Year" := FirstUnpaidAcademicYear;
            Customer."Result Programme Part" := LastPaidStudentPart;
            Customer."Result Semester"  := FirstUnpaidStudentSemester::"1";
            Customer.MODIFY;
          END;
        FirstUnpaidStudentSemester::"1":
          BEGIN
            CASE LastPaidStudentPart OF
              LastPaidStudentPart::"1":
                BEGIN
                  Customer."Result Programme Code" := CustLedgerEntry."Programme Code";
                  Customer."Result Academic Year" := FirstUnpaidAcademicYear - 1;
                  Customer."Result Programme Part" := LastPaidStudentPart::"1";
                  Customer."Result Semester"  := FirstUnpaidStudentSemester::"2";
                  Customer.MODIFY;
                END;
              LastPaidStudentPart::"2":
                BEGIN
                  Customer."Result Programme Code" := CustLedgerEntry."Programme Code";
                  Customer."Result Academic Year" := FirstUnpaidAcademicYear - 1;
                  Customer."Result Programme Part" := LastPaidStudentPart::"1";
                  Customer."Result Semester"  := FirstUnpaidStudentSemester::"2";
                  Customer.MODIFY;
                END;
              LastPaidStudentPart::"3":
                BEGIN
                  Customer."Result Programme Code" := CustLedgerEntry."Programme Code";
                  Customer."Result Academic Year" := FirstUnpaidAcademicYear - 1;
                  Customer."Result Programme Part" := LastPaidStudentPart::"2";
                  Customer."Result Semester"  := FirstUnpaidStudentSemester::"2";
                  Customer.MODIFY;
                END;
              LastPaidStudentPart::"4":
                BEGIN
                  Customer."Result Programme Code" := CustLedgerEntry."Programme Code";
                  Customer."Result Academic Year" := FirstUnpaidAcademicYear - 1;
                  Customer."Result Programme Part" := LastPaidStudentPart::"3";
                  Customer."Result Semester"  := FirstUnpaidStudentSemester::"2";
                  Customer.MODIFY;
                END;
              LastPaidStudentPart::"5":
                BEGIN
                  Customer."Result Programme Code" := CustLedgerEntry."Programme Code";
                  Customer."Result Academic Year" := FirstUnpaidAcademicYear - 1;
                  Customer."Result Programme Part" := LastPaidStudentPart::"4";
                  Customer."Result Semester"  := FirstUnpaidStudentSemester::"2";
                  Customer.MODIFY;
                END;
              LastPaidStudentPart::"6":
                BEGIN
                  Customer."Result Programme Code" := CustLedgerEntry."Programme Code";
                  Customer."Result Academic Year" := FirstUnpaidAcademicYear - 1;
                  Customer."Result Programme Part" := LastPaidStudentPart::"5";
                  Customer."Result Semester"  := FirstUnpaidStudentSemester::"2";
                  Customer.MODIFY;
                END;
              LastPaidStudentPart::"7":
                BEGIN
                  Customer."Result Programme Code" := CustLedgerEntry."Programme Code";
                  Customer."Result Academic Year" := FirstUnpaidAcademicYear - 1;
                  Customer."Result Programme Part" := LastPaidStudentPart::"6";
                  Customer."Result Semester"  := FirstUnpaidStudentSemester::"2";
                  Customer.MODIFY;
                END;
            END;
          END;
      END;
    END ELSE BEGIN
      Customer."Result Programme Code" := CustLedgerEntry."Programme Code";
      Customer."Result Academic Year" := LastPaidAcademicYear;
      Customer."Result Programme Part" := LastPaidStudentPart;
      Customer."Result Semester"  := LastPaidStudentSemester;
      Customer.MODIFY;
    END;
  END;
END;

{
Customer.GET(StudentNo);
Customer.CALCFIELDS("Balance (LCY)");
IF Customer."Balance (LCY)" <= 0 THEN BEGIN
  Customer."Result Programme Code" := Customer.Programme;
  Customer."Result Academic Year" := Customer."Current Academic Year";
  Customer."Result Programme Part" := Customer."Programme Part";
  Customer."Result Semester"  :=Customer."Semester Part" ;
  Customer.MODIFY;
END ELSE BEGIN
  CustLedgerEntry.SETCURRENTKEY("Customer No.",Open,"Academic Year","Programme Part",Semester);
  CustLedgerEntry.SETRANGE("Customer No.",Customer."No.");
  CustLedgerEntry.SETRANGE(Open,TRUE);
  IF CustLedgerEntry.FINDFIRST THEN BEGIN
    CASE CustLedgerEntry.Semester OF
      CustLedgerEntry.Semester::"3":
        BEGIN
          Customer."Result Programme Code" := CustLedgerEntry."Programme Code";
          Customer."Result Academic Year" := CustLedgerEntry."Academic Year";
          Customer."Result Programme Part" := CustLedgerEntry."Programme Part";
          Customer."Result Semester"  := CustLedgerEntry.Semester::"2";
          Customer.MODIFY;
        END;
      CustLedgerEntry.Semester::"2":
        BEGIN
          Customer."Result Programme Code" := CustLedgerEntry."Programme Code";
          Customer."Result Academic Year" := CustLedgerEntry."Academic Year";
          Customer."Result Programme Part" := CustLedgerEntry."Programme Part";
          Customer."Result Semester"  := CustLedgerEntry.Semester::"1";
          Customer.MODIFY;
        END;
      CustLedgerEntry.Semester::"1":
        BEGIN
          CASE CustLedgerEntry."Programme Part" OF
            CustLedgerEntry."Programme Part"::"1":
              BEGIN
                Customer."Result Programme Code" := CustLedgerEntry."Programme Code";
                Customer."Result Academic Year" := CustLedgerEntry."Academic Year" - 1;
                Customer."Result Programme Part" := CustLedgerEntry."Programme Part"::"1";
                Customer."Result Semester"  := CustLedgerEntry.Semester::"2";
                Customer.MODIFY;
              END;
            CustLedgerEntry."Programme Part"::"2":
              BEGIN
                Customer."Result Programme Code" := CustLedgerEntry."Programme Code";
                Customer."Result Academic Year" := CustLedgerEntry."Academic Year" - 1;
                Customer."Result Programme Part" := CustLedgerEntry."Programme Part"::"1";
                Customer."Result Semester"  := CustLedgerEntry.Semester::"2";
                Customer.MODIFY;
              END;
            CustLedgerEntry."Programme Part"::"3":
              BEGIN
                Customer."Result Programme Code" := CustLedgerEntry."Programme Code";
                Customer."Result Academic Year" := CustLedgerEntry."Academic Year" - 1;
                Customer."Result Programme Part" := CustLedgerEntry."Programme Part"::"2";
                Customer."Result Semester"  := CustLedgerEntry.Semester::"2";
                Customer.MODIFY;
              END;
            CustLedgerEntry."Programme Part"::"4":
              BEGIN
                Customer."Result Programme Code" := CustLedgerEntry."Programme Code";
                Customer."Result Academic Year" := CustLedgerEntry."Academic Year" - 1;
                Customer."Result Programme Part" := CustLedgerEntry."Programme Part"::"3";
                Customer."Result Semester"  := CustLedgerEntry.Semester::"2";
                Customer.MODIFY;
              END;
            CustLedgerEntry."Programme Part"::"5":
              BEGIN
                Customer."Result Programme Code" := CustLedgerEntry."Programme Code";
                Customer."Result Academic Year" := CustLedgerEntry."Academic Year" - 1;
                Customer."Result Programme Part" := CustLedgerEntry."Programme Part"::"4";
                Customer."Result Semester"  := CustLedgerEntry.Semester::"2";
                Customer.MODIFY;
              END;
            CustLedgerEntry."Programme Part"::"6":
              BEGIN
                Customer."Result Programme Code" := CustLedgerEntry."Programme Code";
                Customer."Result Academic Year" := CustLedgerEntry."Academic Year" - 1;
                Customer."Result Programme Part" := CustLedgerEntry."Programme Part"::"5";
                Customer."Result Semester"  := CustLedgerEntry.Semester::"2";
                Customer.MODIFY;
              END;
            CustLedgerEntry."Programme Part"::"7":
              BEGIN
                Customer."Result Programme Code" := CustLedgerEntry."Programme Code";
                Customer."Result Academic Year" := CustLedgerEntry."Academic Year" - 1;
                Customer."Result Programme Part" := CustLedgerEntry."Programme Part"::"6";
                Customer."Result Semester"  := CustLedgerEntry.Semester::"2";
                Customer.MODIFY;
              END;
          END;
        END;
    END;
  END;
END;
}

CalcOveralMark(VAR Result : Record "Course Assessment Journal Line")
//13/2/2018
//i) Proposed change is to add a Programme Class variable that is used to provide the programme code used to look up classification and remarks in this function.
//ii) Change this and move both gradings evaluations to the same function and table
//HT Added Code 13/02/2018
StudentGrading.GET(Result."Student Registration No.");
ProgrammeClass.RESET;
ProgrammeClass.SETRANGE(ProgrammeClass.Code,Result."Programme Code");
ProgrammeClass.FINDFIRST;
//IF ProgrammeClass.FINDFIRST THEN;
//END HT Code

Exam.GET(Result."Examination Code");
ExaminationSetup.GET;
ExaminationSetup.TESTFIELD("Mark Rounding Precision");
Result.CALCFIELDS("Credit Hours");

IF ((Exam."Exam Type" = Exam."Exam Type"::Normal) OR Result."Writing as first sitting") THEN BEGIN
  Result.CALCFIELDS(Result."Exam Weight",Result."Assessment Weight");
  //Make Sure Weights are not Zero
  IF Result."Exam Mark"<>0 THEN
    Result.TESTFIELD("Exam Weight");
  IF Result."Other Exam Mark"<>0 THEN
    Result.TESTFIELD("Other Exam Weight");

  IF NOT ((Result."Exam Weight"=0) AND (Result."Assessment Weight"=0) AND (Result."Other Exam Weight"=0)) THEN BEGIN
    Result."Overall Mark":=((Result."Exam Mark"*Result."Exam Weight")+(Result."Assessment Mark"*Result."Assessment Weight")+
      (Result."Other Exam Mark"*Result."Other Exam Weight"))
    /(Result."Exam Weight"+Result."Assessment Weight"+Result."Other Exam Weight");
    Result."Overall Mark" := ROUND(Result."Overall Mark",ExaminationSetup."Mark Rounding Precision",'=');
  END ELSE
    Result."Overall Mark":=0;

    "Dept.Prog".RESET;
    "Dept.Prog".SETRANGE(Code,Result."Programme Code");
    IF NOT "Dept.Prog".FINDFIRST THEN
     ERROR('The programme %1 was not found during classification',Result."Programme Code");
//***************************************************//
   ClassFlag := FALSE;

   IF (("Dept.Prog"."Min CA Mark" = 0) AND ("Dept.Prog"."Min Exam Mark" = 0) AND ("Dept.Prog"."Min OT Mark" = 0)) = FALSE THEN BEGIN

    //****  Testing Assessment Mark  ****//

    IF (Result."Assessment Mark" < "Dept.Prog"."Min CA Mark") AND ("Dept.Prog"."Min CA Mark" <> 0) THEN  BEGIN
      ClassFlag := TRUE;

      // this were the studnt is meant to repeat or supp
      //determine if the OM is greater than the supplementable mark.
      //if above supplementable mark the classification is F and Remark is Supp
      //ELSE classification is F remark is repeat or carry
      Classification1.SETCURRENTKEY("Mark Greater or Equal To");
      Classification1.SETFILTER("Mark Greater or Equal To",'<=%1',Result."Overall Mark");
      //HT Added code 13/02/2018
      Classification1.SETFILTER(GradingType,FORMAT(StudentGrading.Grading));
      //New code
      Classification1.SETRANGE(Classification1."Programme Code",ProgrammeClass."Programme Code");
      //OLD Code
      //Classification1.SETRANGE(Classification1."Programme Code",Result."Programme Code");
      //HT END CODE

      Classification1.SETRANGE("Assessment Type",Classification1."Assessment Type"::Normal);
      IF Classification1.FINDLAST THEN
        IF Result."Overall Mark" >= Classification1."Mark Greater or Equal To" THEN BEGIN
         Result.Classification := Classification1.Classification::F;
         Result."Quality Points" := Result."Credit Hours" * Classification1."Grade Points";
         Result."Grade Points" := Classification1."Grade Points";
         IF Classification1.Remark IN [Classification1.Remark::Supplement, Classification1.Remark::Pass] THEN
          Result.Remarks := Classification1.Remark::Supplement
         ELSE
          Result.Remarks := Classification1.Remark::Carry
        END;
    END;

    //****  Testing Exam Mark  ****//

    IF ClassFlag <> TRUE THEN
    IF (Result."Exam Mark" < "Dept.Prog"."Min Exam Mark") AND ("Dept.Prog"."Min Exam Mark" <> 0) THEN BEGIN
      ClassFlag := TRUE;         // the failing bit

      Classification1.SETCURRENTKEY("Mark Greater or Equal To");
      Classification1.SETFILTER("Mark Greater or Equal To",'<=%1',Result."Overall Mark");
      //HT Edited code
      //New code
      Classification1.SETFILTER(GradingType,FORMAT(StudentGrading.Grading));
      Classification1.SETRANGE(Classification1."Programme Code",ProgrammeClass."Programme Code");
      //OLD Code
      //Classification1.SETRANGE(Classification1."Programme Code",Result."Programme Code");
      //END HT Code

      Classification1.SETRANGE("Assessment Type",Classification1."Assessment Type"::Normal);
      IF Classification1.FINDLAST THEN
       IF Result."Overall Mark" >= Classification1."Mark Greater or Equal To" THEN BEGIN
        Result.Classification := Classification1.Classification::F;
        Result."Quality Points" := Result."Credit Hours" * Classification1."Grade Points";
        Result."Grade Points" := Classification1."Grade Points";
        IF Classification1.Remark IN [Classification1.Remark::Supplement, Classification1.Remark::Pass] THEN
          Result.Remarks :=Classification1.Remark::Supplement
        ELSE
          Result.Remarks := Classification1.Remark::Carry
        END;
    END;

    //****  Testing Other Exam Mark  ****//

    IF ClassFlag <> TRUE THEN
    IF (Result."Other Exam Mark" < "Dept.Prog"."Min OT Mark") AND ("Dept.Prog"."Min OT Mark" <> 0) THEN BEGIN
      ClassFlag := TRUE;        // the failing bit
      //ERROR('%1',ClassFlag);
      Classification1.SETCURRENTKEY("Mark Greater or Equal To");
      Classification1.SETFILTER("Mark Greater or Equal To",'<=%1',Result."Overall Mark");
      //HT Edited code
      //New code
      Classification1.SETFILTER(GradingType,FORMAT(StudentGrading.Grading));
      Classification1.SETRANGE(Classification1."Programme Code",ProgrammeClass."Programme Code");
      //OLD Code
      //Classification1.SETRANGE(Classification1."Programme Code",Result."Programme Code");
      //END HT Code
      Classification1.SETRANGE("Assessment Type",Classification1."Assessment Type"::Normal);
      IF Classification1.FINDLAST THEN
       IF Result."Overall Mark" >= Classification1."Mark Greater or Equal To" THEN BEGIN
        Result.Classification := Classification1.Classification::F;
        Result."Quality Points" := Result."Credit Hours" * Classification1."Grade Points";
        Result."Grade Points" := Classification1."Grade Points";
        IF Classification1.Remark IN [Classification1.Remark::Supplement, Classification1.Remark::Pass] THEN
         Result.Remarks :=Classification1.Remark::Supplement
        ELSE
         Result.Remarks := Classification1.Remark::Carry
        END;
    END;
  END;

//****  Where student has satisfied Max and Min Exam, Assessment and Other Exam Mark  ****//

    IF ClassFlag = FALSE THEN BEGIN
      Classification1.SETCURRENTKEY("Mark Greater or Equal To");
      Classification1.SETFILTER("Mark Greater or Equal To",'<=%1',Result."Overall Mark");
      //HT Edited code
      //New code
      Classification1.SETFILTER(GradingType,FORMAT(StudentGrading.Grading));
      Classification1.SETRANGE(Classification1."Programme Code",ProgrammeClass."Programme Code");
      //OLD Code
      //Classification1.SETRANGE(Classification1."Programme Code",Result."Programme Code");
      //END HT Code
      Classification1.SETRANGE("Assessment Type",Classification1."Assessment Type"::Normal);
      IF Classification1.FINDLAST THEN
        IF Result."Overall Mark" >= Classification1."Mark Greater or Equal To" THEN BEGIN
          Result."Quality Points" := Result."Credit Hours" * Classification1."Grade Points";
          Result."Grade Points" := Classification1."Grade Points";
          Result.Classification := Classification1.Classification;
          Result.Remarks := Classification1.Remark;
          //Result.MODIFY;
        END;
    END;

//16/06/14 CODE TO MANAGE CARRY COURSES

    IF ((Result."Course Type" = Result."Course Type"::Carry) AND (Result."Assessment Mark" = 0) AND
        (Result."Other Exam Mark" = 0))                                            THEN BEGIN
      MarkClassification.RESET;
      //HT Edited code
      //New code
      MarkClassification.SETRANGE(GradingType,StudentGrading.Grading);
      MarkClassification.SETRANGE("Programme Code",ProgrammeClass."Programme Code");
      //OLD Code
      //MarkClassification.SETRANGE("Programme Code",Result."Programme Code");
      //END HT Code
      MarkClassification.SETRANGE(Level,"Dept.Prog".Level);
      MarkClassification.SETRANGE("Assessment Type",MarkClassification."Assessment Type"::Supplementary);
      IF NOT MarkClassification.FINDFIRST THEN
        ERROR(Text02);
      IF Result."Exam Mark" >= MarkClassification."Mark Greater or Equal To" THEN BEGIN
        Result."Overall Mark" := MarkClassification."Mark Greater or Equal To";
        Result.Classification := MarkClassification.Classification;
        Result."Quality Points" := Result."Credit Hours" * MarkClassification."Grade Points";
        Result."Grade Points" := MarkClassification."Grade Points";
        Result.Remarks := MarkClassification.Remark;
      END ELSE BEGIN
        MarkClassification.RESET;
        //HT Edited code
        //New code
        MarkClassification.SETRANGE(GradingType,StudentGrading.Grading);
        MarkClassification.SETRANGE("Programme Code",ProgrammeClass."Programme Code");
        //OLD Code
        //MarkClassification.SETRANGE("Programme Code",Result."Programme Code");
        //END HT Code
        MarkClassification.SETRANGE(Level,"Dept.Prog".Level);
        MarkClassification.SETRANGE("Assessment Type",MarkClassification."Assessment Type"::Normal);
        MarkClassification.SETFILTER("Mark Greater or Equal To",'<=%1',Result."Exam Mark");
        Result."Overall Mark" := Result."Exam Mark";
        IF MarkClassification.FINDLAST THEN BEGIN
          Result.Classification := MarkClassification.Classification;
          Result."Quality Points" := Result."Credit Hours" * MarkClassification."Grade Points";
          Result."Grade Points" := MarkClassification."Grade Points";
          Result.Remarks := MarkClassification.Remark;
        END;
      END;
    END;

//16/06/14 END CODE


 END ELSE BEGIN
  ExaminationSetup.TESTFIELD("Supplementary Pass Mark");
  ExaminationSetup.TESTFIELD("Supplementary Classification");
  ExaminationSetup.TESTFIELD("Supplementary Pass Remark");
  ExaminationSetup.TESTFIELD("Supplementary Fail Remark");
  ExaminationSetup.TESTFIELD("Suppl. Fail Classification");
  Result.CALCFIELDS("Exam Weight","Assessment Weight");
  //Make Sure Weights are not Zero
  IF Result."Exam Mark"<>0 THEN
    Result.TESTFIELD("Exam Weight");
  IF Result."Assessment Mark"<>0 THEN BEGIN
    Result.TESTFIELD("Assessment Weight");
    //the line below may cause problems in the future
    //*******************ALERT*******************************//
    ProgrammeCourse2.SETRANGE("Teaching Class Code",Result."Programme Code");
    ProgrammeCourse2.SETRANGE("Academic Year",Result."Academic Year");
    ProgrammeCourse2.SETRANGE("Programme Part",Result."Programme Part");
    ProgrammeCourse2.SETRANGE(Semester,Result.Semester);
    ProgrammeCourse2.SETRANGE(Code,Result."Course Code");
    IF ProgrammeCourse2.FINDFIRST THEN BEGIN
      ProgrammeCourse2.TESTFIELD("Examination Weight",0);
      ProgrammeCourse2.TESTFIELD("Other Examination Weight",0);
    END;
  END;
  IF Result."Other Exam Mark"<>0 THEN
    Result.TESTFIELD("Other Exam Weight");

  IF NOT ((Result."Exam Weight"=0) AND (Result."Assessment Weight"=0) AND (Result."Other Exam Weight"=0)) THEN BEGIN
    Result."Overall Mark":=((Result."Exam Mark"*Result."Exam Weight")+(Result."Assessment Mark"*Result."Assessment Weight")+
    (Result."Other Exam Mark"*Result."Other Exam Weight"))
    /(Result."Exam Weight"+Result."Assessment Weight"+Result."Other Exam Weight");
    Result."Overall Mark" := ROUND(Result."Overall Mark",ExaminationSetup."Mark Rounding Precision",'=');
  END ELSE
    Result."Overall Mark":=0;

  IF NOT DptProgramme.GET(Result."Programme Code") THEN
    ERROR(Text01);


   IF Result."Exam Mark" <> 0 THEN BEGIN
    MarkClassification.RESET;
    //HT Edited code
    //New code
    MarkClassification.SETRANGE(GradingType,StudentGrading.Grading);
    MarkClassification.SETRANGE("Programme Code",ProgrammeClass."Programme Code");
    //OLD Code
    //MarkClassification.SETRANGE("Programme Code",Result."Programme Code");
    //END HT Code
    MarkClassification.SETRANGE(Level,DptProgramme.Level);
    MarkClassification.SETRANGE("Assessment Type",MarkClassification."Assessment Type"::Supplementary);
    IF MarkClassification.FINDFIRST THEN BEGIN
      IF Result."Exam Mark" >= MarkClassification."Mark Greater or Equal To" THEN BEGIN
        Result."Overall Mark" := MarkClassification."Mark Greater or Equal To";
        Result.Classification := ExaminationSetup."Supplementary Classification";
        Result."Quality Points" := Result."Credit Hours" * MarkClassification."Grade Points";
        Result."Grade Points" := MarkClassification."Grade Points";
        Result.Remarks := ExaminationSetup."Supplementary Pass Remark";
      END ELSE BEGIN
        Result."Overall Mark" := Result."Exam Mark";
        Result.Classification := ExaminationSetup."Suppl. Fail Classification";
         Result."Quality Points" := 0;
         Result."Grade Points" := 0;
        Result.Remarks := ExaminationSetup."Supplementary Fail Remark";
      END;
    END ELSE BEGIN
      IF Result."Exam Mark" >= ExaminationSetup."Supplementary Pass Mark" THEN BEGIN
        Result."Overall Mark" := ExaminationSetup."Supplementary Pass Mark";
        Result.Classification := ExaminationSetup."Supplementary Classification";

        Result.Remarks := ExaminationSetup."Supplementary Pass Remark";
      END ELSE BEGIN
        Result."Overall Mark" := Result."Exam Mark";
        Result.Classification := ExaminationSetup."Suppl. Fail Classification";
        Result.Remarks := ExaminationSetup."Supplementary Fail Remark";
        Result."Quality Points" := 0;
        Result."Grade Points" := 0;
      END;
    END;
   END ELSE BEGIN
    //HT Edited code
    //New code
    MarkClassification.SETRANGE(GradingType,StudentGrading.Grading);
    MarkClassification.SETRANGE("Programme Code",ProgrammeClass."Programme Code");
    //OLD Code
    //MarkClassification.SETRANGE("Programme Code",Result."Programme Code");
    //END HT Code
    MarkClassification.SETRANGE(Level,DptProgramme.Level);
    MarkClassification.SETRANGE("Assessment Type",MarkClassification."Assessment Type"::Supplementary);
    IF MarkClassification.FINDFIRST THEN BEGIN
      IF Result."Assessment Mark" >= MarkClassification."Mark Greater or Equal To" THEN BEGIN
        Result."Overall Mark" := MarkClassification."Mark Greater or Equal To";
        Result."Quality Points" := Result."Credit Hours" * MarkClassification."Grade Points";
        Result."Grade Points" := MarkClassification."Grade Points";
        Result.Classification := ExaminationSetup."Supplementary Classification";
        Result.Remarks := ExaminationSetup."Supplementary Pass Remark";
      END ELSE BEGIN
        Result."Overall Mark" := Result."Assessment Mark";
        Result.Classification := ExaminationSetup."Suppl. Fail Classification";
        Result.Remarks := ExaminationSetup."Supplementary Fail Remark";
        Result."Quality Points" := 0;
        Result."Grade Points" := 0;
      END;
    END ELSE BEGIN
      IF Result."Assessment Mark" >= ExaminationSetup."Supplementary Pass Mark" THEN BEGIN
        Result."Overall Mark" := ExaminationSetup."Supplementary Pass Mark";
        Result.Classification := ExaminationSetup."Supplementary Classification";
        Result.Remarks := ExaminationSetup."Supplementary Pass Remark";
      END ELSE BEGIN
        Result."Overall Mark" := Result."Assessment Mark";
        Result.Classification := ExaminationSetup."Suppl. Fail Classification";
        Result.Remarks := ExaminationSetup."Supplementary Fail Remark";
        Result."Quality Points" := 0;
        Result."Grade Points" := 0;
      END;
    END;
   END;
END;

CalcOveralMark2(VAR Result : Record "Course Assessment Journal Line")
Exam.GET(Result."Examination Code");
ExaminationSetup.GET;
ExaminationSetup.TESTFIELD("Mark Rounding Precision");
Result.CALCFIELDS("Credit Hours");
IF ((Exam."Exam Type" = Exam."Exam Type"::Normal) OR Result."Writing as first sitting") THEN BEGIN
  Result.CALCFIELDS(Result."Exam Weight",Result."Assessment Weight");
  //Make Sure Weights are not Zero
  IF Result."Exam Mark"<>0 THEN
    Result.TESTFIELD("Exam Weight");
  IF Result."Other Exam Mark"<>0 THEN
    Result.TESTFIELD("Other Exam Weight");

  IF NOT ((Result."Exam Weight"=0) AND (Result."Assessment Weight"=0) AND (Result."Other Exam Weight"=0)) THEN BEGIN
    Result."Overall Mark":=((Result."Exam Mark"*Result."Exam Weight")+(Result."Assessment Mark"*Result."Assessment Weight")+
      (Result."Other Exam Mark"*Result."Other Exam Weight"))
    /(Result."Exam Weight"+Result."Assessment Weight"+Result."Other Exam Weight");
    Result."Overall Mark" := ROUND(Result."Overall Mark",ExaminationSetup."Mark Rounding Precision",'=');
  END ELSE
    Result."Overall Mark":=0;

    "Dept.Prog".RESET;
    "Dept.Prog".SETRANGE(Code,Result."Programme Code");
    IF NOT "Dept.Prog".FINDFIRST THEN
     ERROR('The programme %1 was not found during classification',Result."Programme Code");
//***************************************************//
   ClassFlag := FALSE;

   IF (("Dept.Prog"."Min CA Mark" = 0) AND ("Dept.Prog"."Min Exam Mark" = 0) AND ("Dept.Prog"."Min OT Mark" = 0)) = FALSE THEN BEGIN

    //****  Testing Assessment Mark  ****//

    IF (Result."Assessment Mark" < "Dept.Prog"."Min CA Mark") AND ("Dept.Prog"."Min CA Mark" <> 0) THEN  BEGIN
      ClassFlag := TRUE;

      // this were the studnt is meant to repeat or supp
      //determine if the OM is greater than the supplementable mark.
      //if above supplementable mark the classification is F and Remark is Supp
      //ELSE classification is F remark is repeat or carry
      Classification2.SETCURRENTKEY("Mark Greater or Equal To");
      Classification2.SETFILTER("Mark Greater or Equal To",'<=%1',Result."Overall Mark");
      Classification2.SETRANGE(Classification2."Programme Code",Result."Programme Code");
      Classification2.SETRANGE("Assessment Type",Classification2."Assessment Type"::Normal);
      IF Classification2.FINDLAST THEN
        IF Result."Overall Mark" >= Classification2."Mark Greater or Equal To" THEN BEGIN
         Result.Classification := Classification2.Classification::F;
         Result."Quality Points" := Result."Credit Hours" * Classification2."Grade Points";
         Result."Grade Points" := Classification2."Grade Points";
         IF Classification2.Remark IN [Classification2.Remark::Supplement, Classification2.Remark::Pass] THEN
          Result.Remarks := Classification2.Remark::Supplement
         ELSE
          Result.Remarks := Classification2.Remark::Carry
        END;
    END;

    //****  Testing Exam Mark  ****//

    IF ClassFlag <> TRUE THEN
    IF (Result."Exam Mark" < "Dept.Prog"."Min Exam Mark") AND ("Dept.Prog"."Min Exam Mark" <> 0) THEN BEGIN
      ClassFlag := TRUE;         // the failing bit

      Classification2.SETCURRENTKEY("Mark Greater or Equal To");
      Classification2.SETFILTER("Mark Greater or Equal To",'<=%1',Result."Overall Mark");
      Classification2.SETRANGE(Classification2."Programme Code",Result."Programme Code");
      Classification2.SETRANGE("Assessment Type",Classification2."Assessment Type"::Normal);
      IF Classification2.FINDLAST THEN
       IF Result."Overall Mark" >= Classification2."Mark Greater or Equal To" THEN BEGIN
        Result.Classification := Classification2.Classification::F;
        Result."Quality Points" := Result."Credit Hours" * Classification2."Grade Points";
        Result."Grade Points" := Classification2."Grade Points";
        IF Classification2.Remark IN [Classification2.Remark::Supplement, Classification2.Remark::Pass] THEN
          Result.Remarks :=Classification2.Remark::Supplement
        ELSE
          Result.Remarks := Classification2.Remark::Carry
        END;
    END;

    //****  Testing Other Exam Mark  ****//

    IF ClassFlag <> TRUE THEN
    IF (Result."Other Exam Mark" < "Dept.Prog"."Min OT Mark") AND ("Dept.Prog"."Min OT Mark" <> 0) THEN BEGIN
      ClassFlag := TRUE;        // the failing bit
      //ERROR('%1',ClassFlag);
      Classification2.SETCURRENTKEY("Mark Greater or Equal To");
      Classification2.SETFILTER("Mark Greater or Equal To",'<=%1',Result."Overall Mark");
      Classification2.SETRANGE(Classification2."Programme Code",Result."Programme Code");
      Classification2.SETRANGE("Assessment Type",Classification2."Assessment Type"::Normal);
      IF Classification2.FINDLAST THEN
       IF Result."Overall Mark" >= Classification2."Mark Greater or Equal To" THEN BEGIN
        Result.Classification := Classification2.Classification::F;
        Result."Quality Points" := Result."Credit Hours" * Classification2."Grade Points";
        Result."Grade Points" := Classification2."Grade Points";
        IF Classification2.Remark IN [Classification2.Remark::Supplement, Classification2.Remark::Pass] THEN
         Result.Remarks :=Classification2.Remark::Supplement
        ELSE
         Result.Remarks := Classification2.Remark::Carry
        END;
    END;
  END;

//****  Where student has satisfied Max and Min Exam, Assessment and Other Exam Mark  ****//

    IF ClassFlag = FALSE THEN BEGIN
      Classification2.SETCURRENTKEY("Mark Greater or Equal To");
      Classification2.SETFILTER("Mark Greater or Equal To",'<=%1',Result."Overall Mark");
      Classification2.SETRANGE(Classification2."Programme Code",Result."Programme Code");
      Classification2.SETRANGE("Assessment Type",Classification2."Assessment Type"::Normal);
      IF Classification2.FINDLAST THEN
        IF Result."Overall Mark" >= Classification2."Mark Greater or Equal To" THEN BEGIN
        //Result2.GET(Result."Examination Code", Result."Student Registration No.");
          Result."Quality Points" := Result."Credit Hours" * Classification2."Grade Points";
          Result."Grade Points" := Classification2."Grade Points";
          Result.Classification := Classification2.Classification;
          Result.Remarks := Classification2.Remark;
         //ERROR('Trying to modify');
         Result.MODIFY;
        END;
    END;

//16/06/14 CODE TO MANAGE CARRY COURSES

    IF ((Result."Course Type" = Result."Course Type"::Carry) AND (Result."Assessment Mark" = 0) AND
        (Result."Other Exam Mark" = 0))                                            THEN BEGIN
      MarkClassification2.RESET;
      MarkClassification2.SETRANGE("Programme Code",Result."Programme Code");
      MarkClassification2.SETRANGE(Level,"Dept.Prog".Level);
      MarkClassification2.SETRANGE("Assessment Type",MarkClassification2."Assessment Type"::Supplementary);
      IF NOT MarkClassification2.FINDFIRST THEN
        ERROR(Text02);
      IF Result."Exam Mark" >= MarkClassification2."Mark Greater or Equal To" THEN BEGIN
        Result."Overall Mark" := MarkClassification2."Mark Greater or Equal To";
        Result.Classification := MarkClassification2.Classification;
        Result."Quality Points" := Result."Credit Hours" * MarkClassification2."Grade Points";
        Result."Grade Points" := MarkClassification2."Grade Points";
        Result.Remarks := MarkClassification2.Remark;
      END ELSE BEGIN
        MarkClassification2.RESET;
        MarkClassification2.SETRANGE("Programme Code",Result."Programme Code");
        MarkClassification2.SETRANGE(Level,"Dept.Prog".Level);
        MarkClassification2.SETRANGE("Assessment Type",MarkClassification2."Assessment Type"::Normal);
        MarkClassification2.SETFILTER("Mark Greater or Equal To",'<=%1',Result."Exam Mark");
        Result."Overall Mark" := Result."Exam Mark";
        IF MarkClassification2.FINDLAST THEN BEGIN
          Result.Classification := MarkClassification2.Classification;
          Result."Quality Points" := Result."Credit Hours" * MarkClassification2."Grade Points";
          Result."Grade Points" := MarkClassification2."Grade Points";
          Result.Remarks := MarkClassification2.Remark;
        END;
      END;
    END;

//16/06/14 END CODE


END ELSE BEGIN
  ExaminationSetup.TESTFIELD("Supplementary Pass Mark");
  ExaminationSetup.TESTFIELD("Supplementary Classification");
  ExaminationSetup.TESTFIELD("Supplementary Pass Remark");
  ExaminationSetup.TESTFIELD("Supplementary Fail Remark");
  ExaminationSetup.TESTFIELD("Suppl. Fail Classification");
  Result.CALCFIELDS("Exam Weight","Assessment Weight");
  //Make Sure Weights are not Zero
  IF Result."Exam Mark"<>0 THEN
    Result.TESTFIELD("Exam Weight");
  IF Result."Assessment Mark"<>0 THEN BEGIN
    Result.TESTFIELD("Assessment Weight");
    ProgrammeCourse2.SETRANGE("Teaching Class Code",Result."Programme Code");
    ProgrammeCourse2.SETRANGE("Academic Year",Result."Academic Year");
    ProgrammeCourse2.SETRANGE("Programme Part",Result."Programme Part");
    ProgrammeCourse2.SETRANGE(Semester,Result.Semester);
    ProgrammeCourse2.SETRANGE(Code,Result."Course Code");
    IF ProgrammeCourse2.FINDFIRST THEN BEGIN
      ProgrammeCourse2.TESTFIELD("Examination Weight",0);
      ProgrammeCourse2.TESTFIELD("Other Examination Weight",0);
    END;
  END;
  IF Result."Other Exam Mark"<>0 THEN
    Result.TESTFIELD("Other Exam Weight");

  IF NOT ((Result."Exam Weight"=0) AND (Result."Assessment Weight"=0) AND (Result."Other Exam Weight"=0)) THEN BEGIN
    Result."Overall Mark":=((Result."Exam Mark"*Result."Exam Weight")+(Result."Assessment Mark"*Result."Assessment Weight")+
    (Result."Other Exam Mark"*Result."Other Exam Weight"))
    /(Result."Exam Weight"+Result."Assessment Weight"+Result."Other Exam Weight");
    Result."Overall Mark" := ROUND(Result."Overall Mark",ExaminationSetup."Mark Rounding Precision",'=');
  END ELSE
    Result."Overall Mark":=0;

  IF NOT DptProgramme.GET(Result."Programme Code") THEN
    ERROR(Text01);


   IF Result."Exam Mark" <> 0 THEN BEGIN
    MarkClassification2.RESET;
    MarkClassification2.SETRANGE("Programme Code",Result."Programme Code");
    MarkClassification2.SETRANGE(Level,DptProgramme.Level);
    MarkClassification2.SETRANGE("Assessment Type",MarkClassification2."Assessment Type"::Supplementary);
    IF MarkClassification2.FINDFIRST THEN BEGIN
      IF Result."Exam Mark" >= MarkClassification2."Mark Greater or Equal To" THEN BEGIN
        Result."Overall Mark" := MarkClassification2."Mark Greater or Equal To";
        Result.Classification := ExaminationSetup."Supplementary Classification";
        Result."Quality Points" := Result."Credit Hours" * MarkClassification2."Grade Points";
        Result."Grade Points" := MarkClassification2."Grade Points";
        Result.Remarks := ExaminationSetup."Supplementary Pass Remark";
      END ELSE BEGIN
        Result."Overall Mark" := Result."Exam Mark";
        Result.Classification := ExaminationSetup."Suppl. Fail Classification";
         Result."Quality Points" := 0;
         Result."Grade Points" := 0;
        Result.Remarks := ExaminationSetup."Supplementary Fail Remark";
      END;
    END ELSE BEGIN
      IF Result."Exam Mark" >= ExaminationSetup."Supplementary Pass Mark" THEN BEGIN
        Result."Overall Mark" := ExaminationSetup."Supplementary Pass Mark";
        Result.Classification := ExaminationSetup."Supplementary Classification";

        Result.Remarks := ExaminationSetup."Supplementary Pass Remark";
      END ELSE BEGIN
        Result."Overall Mark" := Result."Exam Mark";
        Result.Classification := ExaminationSetup."Suppl. Fail Classification";
        Result.Remarks := ExaminationSetup."Supplementary Fail Remark";
       Result."Quality Points" := 0;
        Result."Grade Points" := 0;
      END;
    END;
   END ELSE BEGIN
    MarkClassification2.SETRANGE("Programme Code",Result."Programme Code");
    MarkClassification2.SETRANGE(Level,DptProgramme.Level);
    MarkClassification2.SETRANGE("Assessment Type",MarkClassification2."Assessment Type"::Supplementary);
    IF MarkClassification2.FINDFIRST THEN BEGIN
      IF Result."Assessment Mark" >= MarkClassification2."Mark Greater or Equal To" THEN BEGIN
        Result."Overall Mark" := MarkClassification2."Mark Greater or Equal To";
        Result."Quality Points" := Result."Credit Hours" * MarkClassification2."Grade Points";
        Result."Grade Points" := MarkClassification2."Grade Points";
        Result.Classification := ExaminationSetup."Supplementary Classification";
        Result.Remarks := ExaminationSetup."Supplementary Pass Remark";
      END ELSE BEGIN
        Result."Overall Mark" := Result."Assessment Mark";
        Result.Classification := ExaminationSetup."Suppl. Fail Classification";
        Result.Remarks := ExaminationSetup."Supplementary Fail Remark";
        Result."Quality Points" := 0;
        Result."Grade Points" := 0;
      END;
    END ELSE BEGIN
      IF Result."Assessment Mark" >= ExaminationSetup."Supplementary Pass Mark" THEN BEGIN
        Result."Overall Mark" := ExaminationSetup."Supplementary Pass Mark";
        Result.Classification := ExaminationSetup."Supplementary Classification";
        Result.Remarks := ExaminationSetup."Supplementary Pass Remark";
      END ELSE BEGIN
        Result."Overall Mark" := Result."Assessment Mark";
        Result.Classification := ExaminationSetup."Suppl. Fail Classification";
        Result.Remarks := ExaminationSetup."Supplementary Fail Remark";
        Result."Quality Points" := 0;
        Result."Grade Points" := 0;
      END;
    END;
   END;
END;
//Result2.GET(Result."Examination Code", Result."Student Registration No.");
//Result2.MODIFY;

CalcOveralMarkBoard(VAR Result : Record "Student Exam Detail Line")
//changes needed to make sure the classification is done using programme not class
//19/10/2018
//i) Proposed change is to add a Programme Class variable that is used to provide the programme code used to look up classification and remarks in this function.
//ii) Change this and move both gradings evaluations to the same function and table
//HT Added Code 19/10/2018
_ProgrammeClass.RESET;
_ProgrammeClass.SETRANGE(_ProgrammeClass.Code,Result."Programme Code"); // note the field Programme code represents "Result class code"
_ProgrammeClass.FINDFIRST;
//IF ProgrammeClass.FINDFIRST THEN;
//END HT Code

_StudentGradingBoard.GET(Result."Student No.");
//Exam.GET("Examination Code");
ExaminationSetup.GET;
ExaminationSetup.TESTFIELD("Mark Rounding Precision");
Result.CALCFIELDS(Result."Other Weight",Result."Exam Weight",Result."Assessment Weight");

IF Result."Assessment Type" = Result."Assessment Type"::Normal THEN BEGIN
  Result.CALCFIELDS(Result."Exam Weight",Result."Assessment Weight");
  //Make Sure Weights are not Zero
  IF Result."Exam Mark"<>0 THEN
    Result.TESTFIELD(Result."Exam Weight");
  IF Result."Other Exam Mark"<>0 THEN
    Result.TESTFIELD(Result."Other Weight");

  IF NOT ((Result."Exam Weight"=0) AND (Result."Assessment Weight"=0) AND (Result."Other Weight"=0)) THEN BEGIN
    Result."Overall Mark":=((Result."Exam Mark"*Result."Exam Weight")+(Result."Assessment Mark"*Result."Assessment Weight")+
(Result."Other Exam Mark"*Result."Other Weight"))
    /(Result."Exam Weight"+Result."Assessment Weight"+Result."Other Weight");
    Result."Overall Mark" := ROUND(Result."Overall Mark",ExaminationSetup."Mark Rounding Precision",'=');
  END ELSE
    Result."Overall Mark":=0;

    "Dept.Prog".RESET;
    "Dept.Prog".SETRANGE(Code,Result."Result Class Code");
    IF NOT "Dept.Prog".FINDFIRST THEN
     ERROR('The programme %1 was not found during Classification',Result."Result Class Code");
//***************************************************//
   ClassFlag := FALSE;

   IF (("Dept.Prog"."Min CA Mark" = 0) AND ("Dept.Prog"."Min Exam Mark" = 0) AND ("Dept.Prog"."Min OT Mark" = 0)) = FALSE THEN BEGIN

    IF (Result."Assessment Mark" < "Dept.Prog"."Min CA Mark") AND ("Dept.Prog"."Min CA Mark" <> 0) THEN  BEGIN
      ClassFlag := TRUE;
      // this were the studnt is meant to repeat or supp
      //determine if the OM is greater than the supplementable mark.
      //if above supplementable mark the Classification1.is F and Remark is Supp
      //ELSE Classification1.is F remark is repeat or carry
      Classification1.SETCURRENTKEY("Mark Greater or Equal To");
      Classification1.SETFILTER("Mark Greater or Equal To",'<=%1',Result."Overall Mark");

      //HT Edited 19/10/2018 --- Harmonising the lookup of classification to use Programme and not Class
      //OLD Code
      //Classification1.SETRANGE(Classification1."Programme Code",Result."Result Class Code");
      //New Code
      Classification1.SETRANGE(Classification1."Programme Code",_ProgrammeClass."Programme Code");
      //END HT Editing

      //HT Added 21/06/2018
      Classification1.SETFILTER(GradingType,FORMAT(_StudentGradingBoard.Grading));
      //HT Added 21/06/2018
      Classification1.SETRANGE("Assessment Type",Classification1."Assessment Type"::Normal);
      IF Classification1.FINDLAST THEN
        IF Result."Overall Mark" >= Classification1."Mark Greater or Equal To" THEN BEGIN
         Result.Classification:= Classification1.Classification::F;
         Result."Quality Points" := Result."Credit Hours" * Classification1."Grade Points";
         Result."Grade Points" := Classification1."Grade Points";
         IF Classification1.Remark IN [Classification1.Remark::Supplement, Classification1.Remark::Pass] THEN
          Result.Remark := Classification1.Remark::Supplement
         ELSE
          Result.Remark := Classification1.Remark::Carry
        END;
    END;

   IF ClassFlag <> TRUE THEN
    IF (Result."Exam Mark" < "Dept.Prog"."Min Exam Mark") AND ("Dept.Prog"."Min Exam Mark" <> 0) THEN BEGIN
      ClassFlag := TRUE;         // the failing bit
      Classification1.SETCURRENTKEY("Mark Greater or Equal To");
      Classification1.SETFILTER("Mark Greater or Equal To",'<=%1',Result."Overall Mark");

      //HT Edited 19/10/2018 --- Harmonising the lookup of classification to use Programme and not Class
      //OLD Code
      //Classification1.SETRANGE(Classification1."Programme Code",Result."Result Class Code");
      //New Code
      Classification1.SETRANGE(Classification1."Programme Code",_ProgrammeClass."Programme Code");
      //END HT Editing

      //HT Added 21/06/2018
      Classification1.SETFILTER(GradingType,FORMAT(_StudentGradingBoard.Grading));
      //HT Added 21/06/2018
      Classification1.SETRANGE("Assessment Type",Classification1."Assessment Type"::Normal);
      IF Classification1.FINDLAST THEN
       IF Result."Overall Mark" >= Classification1."Mark Greater or Equal To" THEN BEGIN
        Result.Classification:= Classification1.Classification::F;
         Result."Quality Points" := Result."Credit Hours" * Classification1."Grade Points";
         Result."Grade Points" := Classification1."Grade Points";

        IF Classification1.Remark IN [Classification1.Remark::Supplement, Classification1.Remark::Pass] THEN
          Result.Remark :=Classification1.Remark::Supplement
        ELSE
          Result.Remark := Classification1.Remark::Carry
        END;
    END;

   IF ClassFlag <> TRUE THEN
    IF (Result."Other Exam Mark" < "Dept.Prog"."Min OT Mark") AND ("Dept.Prog"."Min OT Mark" <> 0) THEN BEGIN
      ClassFlag := TRUE;        // the failing bit
      Classification1.SETCURRENTKEY("Mark Greater or Equal To");
      Classification1.SETFILTER("Mark Greater or Equal To",'<=%1',Result."Overall Mark");
      //HT Edited 19/10/2018 --- Harmonising the lookup of classification to use Programme and not Class
      //OLD Code
      //Classification1.SETRANGE(Classification1."Programme Code",Result."Result Class Code");
      //New Code
      Classification1.SETRANGE(Classification1."Programme Code",_ProgrammeClass."Programme Code");
      //END HT Editing

      //HT Added 21/06/2018
      Classification1.SETFILTER(GradingType,FORMAT(_StudentGradingBoard.Grading));
      //HT Added 21/06/2018
      Classification1.SETRANGE("Assessment Type",Classification1."Assessment Type"::Normal);
      IF Classification1.FINDLAST THEN
       IF Result."Overall Mark" >= Classification1."Mark Greater or Equal To" THEN BEGIN
        Result.Classification:= Classification1.Classification::F;
         Result."Quality Points" := Result."Credit Hours" * Classification1."Grade Points";
         Result."Grade Points" := Classification1."Grade Points";

        IF Classification1.Remark IN [Classification1.Remark::Supplement, Classification1.Remark::Pass] THEN
         Result.Remark :=Classification1.Remark::Supplement
        ELSE
         Result.Remark := Classification1.Remark::Carry
        END;
    END;
  END;
    IF ClassFlag = FALSE THEN BEGIN
      Classification1.SETCURRENTKEY("Mark Greater or Equal To");
      Classification1.SETFILTER("Mark Greater or Equal To",'<=%1',Result."Overall Mark");

      //HT Edited 19/10/2018 --- Harmonising the lookup of classification to use Programme and not Class
      //OLD Code
      //Classification1.SETRANGE(Classification1."Programme Code",Result."Result Class Code");
      //New Code
      Classification1.SETRANGE(Classification1."Programme Code",_ProgrammeClass."Programme Code");
      //END HT Editing


      //HT Added 21/06/2018
      Classification1.SETFILTER(GradingType,FORMAT(_StudentGradingBoard.Grading));
      //HT Added 21/06/2018
      Classification1.SETRANGE("Assessment Type",Classification1."Assessment Type"::Normal);
      IF Classification1.FINDLAST THEN
        IF Result."Overall Mark" >= Classification1."Mark Greater or Equal To" THEN BEGIN
         Result.Classification:= Classification1.Classification;
         Result."Quality Points" := Result."Credit Hours" * Classification1."Grade Points";
         Result."Grade Points" := Classification1."Grade Points";
         Result.Remark := Classification1.Remark;
        END;
    END;
//16/06/14 CODE TO MANAGE CARRY COURSES//241114 MODIFIED TO ACCOMODATE SETTING THE EXAM MARK AS COURSE MARK

    IF ((Result."Reg. Type" = Result."Reg. Type"::Carry) AND (Result."Assessment Mark" = 0) AND
        (Result."Other Exam Mark" = 0))                                            THEN BEGIN
      MarkClassification.RESET;

      //HT Edited 19/10/2018 --- Harmonising the lookup of classification to use Programme and not Class
      //OLD Code
      //MarkClassification.SETRANGE("Programme Code",Result."Result Class Code");
      //New Code
      MarkClassification.SETRANGE("Programme Code",_ProgrammeClass."Programme Code");
      //END HT Editing


      MarkClassification.SETRANGE(Level,"Dept.Prog".Level);
      //HT Added 21/06/2018
      MarkClassification.SETFILTER(GradingType,FORMAT(_StudentGradingBoard.Grading));
      //HT Added 21/06/2018
      MarkClassification.SETRANGE("Assessment Type",MarkClassification."Assessment Type"::Supplementary);
      IF NOT MarkClassification.FINDFIRST THEN
        ERROR(Text02);
      IF Result."Exam Mark" >= MarkClassification."Mark Greater or Equal To" THEN BEGIN
        Result."Overall Mark" := MarkClassification."Mark Greater or Equal To";
        Result.Classification:= MarkClassification.Classification;
         Result."Quality Points" := Result."Credit Hours" * MarkClassification."Grade Points";
         Result."Grade Points" := MarkClassification."Grade Points";
        Result.Remark := MarkClassification.Remark;
      END ELSE BEGIN
        MarkClassification.RESET;

        //HT Edited 19/10/2018 --- Harmonising the lookup of classification to use Programme and not Class
        //OLD Code
        //MarkClassification.SETRANGE("Programme Code",Result."Result Class Code");
        //New Code
        MarkClassification.SETRANGE("Programme Code",_ProgrammeClass."Programme Code");
        //END HT Editing

        MarkClassification.SETRANGE(Level,"Dept.Prog".Level);
        //HT Added 21/06/2018
        MarkClassification.SETFILTER(GradingType,FORMAT(_StudentGradingBoard.Grading));
        //HT Added 21/06/2018
        MarkClassification.SETRANGE("Assessment Type",MarkClassification."Assessment Type"::Normal);
        MarkClassification.SETFILTER("Mark Greater or Equal To",'<=%1',Result."Exam Mark");
        Result."Overall Mark" := Result."Exam Mark";
        IF MarkClassification.FINDLAST THEN BEGIN
          Result.Classification:= MarkClassification.Classification;
          Result."Quality Points" := Result."Credit Hours" * MarkClassification."Grade Points";
          Result."Grade Points" := MarkClassification."Grade Points";
          Result.Remark := MarkClassification.Remark;
        END;
      END;
    END;

//16/06/14 END CODE

END ELSE BEGIN
  ExaminationSetup.TESTFIELD("Supplementary Pass Mark");
  ExaminationSetup.TESTFIELD("Supplementary Classification");
  ExaminationSetup.TESTFIELD("Supplementary Pass Remark");
  ExaminationSetup.TESTFIELD("Supplementary Fail Remark");
  ExaminationSetup.TESTFIELD("Suppl. Fail Classification");
  Result.CALCFIELDS("Exam Weight","Assessment Weight");
  //Make Sure Weights are not Zero
  IF Result."Exam Mark"<>0 THEN
    Result.TESTFIELD("Exam Weight");
  IF Result."Assessment Mark"<>0 THEN BEGIN
    Result.TESTFIELD("Assessment Weight");
    ProgrammeCourse2.SETRANGE("Teaching Class Code",Result."Result Class Code");
    ProgrammeCourse2.SETRANGE("Academic Year",Result."Academic Year");
    ProgrammeCourse2.SETRANGE("Programme Part",Result."Programme Part");
    ProgrammeCourse2.SETRANGE(Semester,Result.Semester);
    ProgrammeCourse2.SETRANGE(Code,Result.Course);
    IF ProgrammeCourse2.FINDFIRST THEN BEGIN
      ProgrammeCourse2.TESTFIELD("Examination Weight",0);
      ProgrammeCourse2.TESTFIELD("Other Examination Weight",0);
    END;
  END;
  IF Result."Other Exam Mark"<>0 THEN
    Result.TESTFIELD("Other Weight");

  IF NOT ((Result."Exam Weight"=0) AND (Result."Assessment Weight"=0) AND (Result."Other Weight"=0)) THEN BEGIN
    Result."Overall Mark":=((Result."Exam Mark"*Result."Exam Weight")+(Result."Assessment Mark"*Result."Assessment Weight")+
(Result."Other Exam Mark"*Result."Other Weight"))
    /(Result."Exam Weight"+Result."Assessment Weight"+Result."Other Weight");
    Result."Overall Mark" := ROUND(Result."Overall Mark",ExaminationSetup."Mark Rounding Precision",'=');
  END ELSE
    Result."Overall Mark":=0;

  IF NOT DptProgramme.GET(Result."Result Class Code") THEN
    ERROR(Text01);


   IF Result."Exam Mark" <> 0 THEN BEGIN

    //HT Edited 19/10/2018 --- Harmonising the lookup of classification to use Programme and not Class
    //OLD Code
    //MarkClassification.SETRANGE("Programme Code",Result."Result Class Code");
    //New Code
    MarkClassification.SETRANGE("Programme Code",_ProgrammeClass."Programme Code");
    //END HT Editing

    MarkClassification.SETRANGE(Level,DptProgramme.Level);
    //HT Added 21/06/2018
    MarkClassification.SETFILTER(GradingType,FORMAT(_StudentGradingBoard.Grading));
    //HT Added 21/06/2018

    MarkClassification.SETRANGE("Assessment Type",MarkClassification."Assessment Type"::Supplementary);
    IF MarkClassification.FINDFIRST THEN BEGIN
      IF Result."Exam Mark" >= MarkClassification."Mark Greater or Equal To" THEN BEGIN
        Result."Overall Mark" := MarkClassification."Mark Greater or Equal To";
         Result."Quality Points" := Result."Credit Hours" * MarkClassification."Grade Points";
         Result."Grade Points" := MarkClassification."Grade Points";
        Result.Classification:= ExaminationSetup."Supplementary Classification";
        Result.Remark := ExaminationSetup."Supplementary Pass Remark";
      END ELSE BEGIN
        Result."Overall Mark" := Result."Exam Mark";
        Result.Classification:= ExaminationSetup."Suppl. Fail Classification";
        Result.Remark := ExaminationSetup."Supplementary Fail Remark";
        Result."Quality Points" := 0;
        Result."Grade Points" := 0;
      END;
    END ELSE BEGIN
      IF Result."Exam Mark" >= ExaminationSetup."Supplementary Pass Mark" THEN BEGIN
        Result."Overall Mark" := ExaminationSetup."Supplementary Pass Mark";
        Result.Classification:= ExaminationSetup."Supplementary Classification";
        Result.Remark := ExaminationSetup."Supplementary Pass Remark";
        Result."Quality Points" := 0;
        Result."Grade Points" := 0;
      END ELSE BEGIN
        Result."Overall Mark" := Result."Exam Mark";
        Result.Classification:= ExaminationSetup."Suppl. Fail Classification";
        Result.Remark := ExaminationSetup."Supplementary Fail Remark";
        Result."Quality Points" := 0;
        Result."Grade Points" := 0;
      END;
    END;
   END ELSE BEGIN

    //HT Edited 19/10/2018 --- Harmonising the lookup of classification to use Programme and not Class
    //OLD Code
    //MarkClassification.SETRANGE("Programme Code",Result."Result Class Code");
    //New Code
    MarkClassification.SETRANGE("Programme Code",_ProgrammeClass."Programme Code");
    //END HT Editing

    MarkClassification.SETRANGE(Level,DptProgramme.Level);

    //HT Added 21/06/2018
    MarkClassification.SETFILTER(GradingType,FORMAT(_StudentGradingBoard.Grading));
    //HT Added 21/06/2018

    MarkClassification.SETRANGE("Assessment Type",MarkClassification."Assessment Type"::Supplementary);
    IF MarkClassification.FINDFIRST THEN BEGIN
      IF Result."Assessment Mark" >= MarkClassification."Mark Greater or Equal To" THEN BEGIN
        Result."Overall Mark" := MarkClassification."Mark Greater or Equal To";
        Result."Quality Points" := Result."Credit Hours" * MarkClassification."Grade Points";
        Result."Grade Points" := MarkClassification."Grade Points";
        Result.Classification:= ExaminationSetup."Supplementary Classification";
        Result.Remark := ExaminationSetup."Supplementary Pass Remark";
      END ELSE BEGIN
        Result."Overall Mark" := Result."Assessment Mark";
        Result.Classification:= ExaminationSetup."Suppl. Fail Classification";
        Result.Remark := ExaminationSetup."Supplementary Fail Remark";
        Result."Quality Points" := 0;
        Result."Grade Points" := 0;
      END;
    END ELSE BEGIN
      IF Result."Assessment Mark" >= ExaminationSetup."Supplementary Pass Mark" THEN BEGIN
        Result."Overall Mark" := ExaminationSetup."Supplementary Pass Mark";
        Result.Classification:= ExaminationSetup."Supplementary Classification";
        Result.Remark := ExaminationSetup."Supplementary Pass Remark";
        Result."Quality Points" := 0;
        Result."Grade Points" := 0;
      END ELSE BEGIN
        Result."Overall Mark" := Result."Assessment Mark";
        Result.Classification:= ExaminationSetup."Suppl. Fail Classification";
        Result.Remark := ExaminationSetup."Supplementary Fail Remark";
        Result."Quality Points" := 0;
        Result."Grade Points" := 0;
      END;
    END;
   END;
END;

CalcOveralMarkBoard2(VAR Result : Record "Student Exam Detail Line")

//changes needed to make sure the classification is done using programme not class
//19/10/2018
//i) Proposed change is to add a Programme Class variable that is used to provide the programme code used to look up classification and remarks in this function.
//ii) Change this and move both gradings evaluations to the same function and table
//HT Added Code 19/10/2018
_ProgrammeClass.RESET;
_ProgrammeClass.SETRANGE(_ProgrammeClass.Code,Result."Programme Code"); // note the field Programme code represents "Result class code"
_ProgrammeClass.FINDFIRST;
//IF ProgrammeClass.FINDFIRST THEN;
//END HT Code


//Exam.GET("Examination Code");
ExaminationSetup.GET;
ExaminationSetup.TESTFIELD("Mark Rounding Precision");
Result.CALCFIELDS(Result."Other Weight",Result."Exam Weight",Result."Assessment Weight");

IF Result."Assessment Type" = Result."Assessment Type"::Normal THEN BEGIN
  Result.CALCFIELDS(Result."Exam Weight",Result."Assessment Weight");
  //Make Sure Weights are not Zero
  IF Result."Exam Mark"<>0 THEN
    Result.TESTFIELD(Result."Exam Weight");
  IF Result."Other Exam Mark"<>0 THEN
    Result.TESTFIELD(Result."Other Weight");

  IF NOT ((Result."Exam Weight"=0) AND (Result."Assessment Weight"=0) AND (Result."Other Weight"=0)) THEN BEGIN
    Result."Overall Mark":=((Result."Exam Mark"*Result."Exam Weight")+(Result."Assessment Mark"*Result."Assessment Weight")+
(Result."Other Exam Mark"*Result."Other Weight"))
    /(Result."Exam Weight"+Result."Assessment Weight"+Result."Other Weight");
    Result."Overall Mark" := ROUND(Result."Overall Mark",ExaminationSetup."Mark Rounding Precision",'=');
  END ELSE
    Result."Overall Mark":=0;

    "Dept.Prog".RESET;
    "Dept.Prog".SETRANGE(Code,Result."Result Class Code");
    IF NOT "Dept.Prog".FINDFIRST THEN
     ERROR('The programme %1 was not found during classification',Result."Result Class Code");
//***************************************************//
   ClassFlag := FALSE;

   IF (("Dept.Prog"."Min CA Mark" = 0) AND ("Dept.Prog"."Min Exam Mark" = 0) AND ("Dept.Prog"."Min OT Mark" = 0)) = FALSE THEN BEGIN

    IF (Result."Assessment Mark" < "Dept.Prog"."Min CA Mark") AND ("Dept.Prog"."Min CA Mark" <> 0) THEN  BEGIN
      ClassFlag := TRUE;
      // this were the studnt is meant to repeat or supp
      //determine if the OM is greater than the supplementable mark.
      //if above supplementable mark the classification is F and Remark is Supp
      //ELSE classification is F remark is repeat or carry
      Classification2.SETCURRENTKEY("Mark Greater or Equal To");
      Classification2.SETFILTER("Mark Greater or Equal To",'<=%1',Result."Overall Mark");
      //HT Edited 19/10/2018 --- Harmonising the lookup of classification to use Programme and not Class
      //OLD Code
      //Classification2.SETRANGE(Classification2."Programme Code",Result."Result Class Code");
      //New code
      Classification2.SETRANGE(Classification2."Programme Code",_ProgrammeClass."Programme Code");
      //END HT Edit

      Classification2.SETRANGE("Assessment Type",Classification2."Assessment Type"::Normal);
      IF Classification2.FINDLAST THEN
        IF Result."Overall Mark" >= Classification2."Mark Greater or Equal To" THEN BEGIN
         Result.Classification := Classification2.Classification::F;
         Result."Quality Points" := Result."Credit Hours" * Classification2."Grade Points";
         Result."Grade Points" := Classification2."Grade Points";
         IF Classification2.Remark IN [Classification2.Remark::Supplement, Classification2.Remark::Pass] THEN
          Result.Remark := Classification2.Remark::Supplement
         ELSE
          Result.Remark := Classification2.Remark::Carry
        END;
    END;

   IF ClassFlag <> TRUE THEN
    IF (Result."Exam Mark" < "Dept.Prog"."Min Exam Mark") AND ("Dept.Prog"."Min Exam Mark" <> 0) THEN BEGIN
      ClassFlag := TRUE;         // the failing bit
      Classification2.SETCURRENTKEY("Mark Greater or Equal To");
      Classification2.SETFILTER("Mark Greater or Equal To",'<=%1',Result."Overall Mark");

      //HT Edited 19/10/2018 --- Harmonising the lookup of classification to use Programme and not Class
      //OLD Code
      //Classification2.SETRANGE(Classification2."Programme Code",Result."Result Class Code");
      //New code
      Classification2.SETRANGE(Classification2."Programme Code",_ProgrammeClass."Programme Code");
      //End HT Edit

      Classification2.SETRANGE("Assessment Type",Classification2."Assessment Type"::Normal);
      IF Classification2.FINDLAST THEN
       IF Result."Overall Mark" >= Classification2."Mark Greater or Equal To" THEN BEGIN
        Result.Classification := Classification2.Classification::F;
         Result."Quality Points" := Result."Credit Hours" * Classification2."Grade Points";
         Result."Grade Points" := Classification2."Grade Points";

        IF Classification2.Remark IN [Classification2.Remark::Supplement, Classification2.Remark::Pass] THEN
          Result.Remark :=Classification2.Remark::Supplement
        ELSE
          Result.Remark := Classification2.Remark::Carry
        END;
    END;

   IF ClassFlag <> TRUE THEN
    IF (Result."Other Exam Mark" < "Dept.Prog"."Min OT Mark") AND ("Dept.Prog"."Min OT Mark" <> 0) THEN BEGIN
      ClassFlag := TRUE;        // the failing bit
      Classification2.SETCURRENTKEY("Mark Greater or Equal To");
      Classification2.SETFILTER("Mark Greater or Equal To",'<=%1',Result."Overall Mark");

      //HT Edited 19/10/2018 --- Harmonising the lookup of classification to use Programme and not Class
      //OLD Code
      //Classification2.SETRANGE(Classification2."Programme Code",Result."Result Class Code");
      //New code
      Classification2.SETRANGE(Classification2."Programme Code",_ProgrammeClass."Programme Code");
      //End HT Edit

      Classification2.SETRANGE("Assessment Type",Classification2."Assessment Type"::Normal);
      IF Classification2.FINDLAST THEN
       IF Result."Overall Mark" >= Classification2."Mark Greater or Equal To" THEN BEGIN
        Result.Classification := Classification2.Classification::F;
         Result."Quality Points" := Result."Credit Hours" * Classification2."Grade Points";
         Result."Grade Points" := Classification2."Grade Points";

        IF Classification2.Remark IN [Classification2.Remark::Supplement, Classification2.Remark::Pass] THEN
         Result.Remark :=Classification2.Remark::Supplement
        ELSE
         Result.Remark := Classification2.Remark::Carry
        END;
    END;
  END;
    IF ClassFlag = FALSE THEN BEGIN
      Classification2.SETCURRENTKEY("Mark Greater or Equal To");
      Classification2.SETFILTER("Mark Greater or Equal To",'<=%1',Result."Overall Mark");

      //HT Edited 19/10/2018 --- Harmonising the lookup of classification to use Programme and not Class
      //OLD Code
      //Classification2.SETRANGE(Classification2."Programme Code",Result."Result Class Code");
      //New code
      Classification2.SETRANGE(Classification2."Programme Code",_ProgrammeClass."Programme Code");
      //End HT Edit


      Classification2.SETRANGE("Assessment Type",Classification2."Assessment Type"::Normal);
      IF Classification2.FINDLAST THEN
        IF Result."Overall Mark" >= Classification2."Mark Greater or Equal To" THEN BEGIN
         Result.Classification := Classification2.Classification;
         Result."Quality Points" := Result."Credit Hours" * Classification2."Grade Points";
         Result."Grade Points" := Classification2."Grade Points";
         Result.Remark := Classification2.Remark;
        END;
    END;
//16/06/14 CODE TO MANAGE CARRY COURSES//241114 MODIFIED TO ACCOMODATE SETTING THE EXAM MARK AS COURSE MARK

    IF ((Result."Reg. Type" = Result."Reg. Type"::Carry) AND (Result."Assessment Mark" = 0) AND
        (Result."Other Exam Mark" = 0))                                            THEN BEGIN
      MarkClassification2.RESET;

      //HT Edited 19/10/2018 --- Harmonising the lookup of classification to use Programme and not Class
      //OLD Code
      //MarkClassification2.SETRANGE("Programme Code",Result."Result Class Code");
      //New code
      MarkClassification2.SETRANGE("Programme Code",_ProgrammeClass."Programme Code");
      // End HT Edit

      MarkClassification2.SETRANGE(Level,"Dept.Prog".Level);
      MarkClassification2.SETRANGE("Assessment Type",MarkClassification2."Assessment Type"::Supplementary);
      IF NOT MarkClassification2.FINDFIRST THEN
        ERROR(Text02);
      IF Result."Exam Mark" >= MarkClassification2."Mark Greater or Equal To" THEN BEGIN
        Result."Overall Mark" := MarkClassification2."Mark Greater or Equal To";
        Result.Classification := MarkClassification2.Classification;
         Result."Quality Points" := Result."Credit Hours" * MarkClassification2."Grade Points";
         Result."Grade Points" := MarkClassification2."Grade Points";
        Result.Remark := MarkClassification2.Remark;
      END ELSE BEGIN
        MarkClassification2.RESET;

      //HT Edited 19/10/2018 --- Harmonising the lookup of classification to use Programme and not Class
      //OLD Code
      //MarkClassification2.SETRANGE("Programme Code",Result."Result Class Code");
      //New code
      MarkClassification2.SETRANGE("Programme Code",_ProgrammeClass."Programme Code");
      // End HT Edit

        MarkClassification2.SETRANGE(Level,"Dept.Prog".Level);
        MarkClassification2.SETRANGE("Assessment Type",MarkClassification2."Assessment Type"::Normal);
        MarkClassification2.SETFILTER("Mark Greater or Equal To",'<=%1',Result."Exam Mark");
        Result."Overall Mark" := Result."Exam Mark";
        IF MarkClassification2.FINDLAST THEN BEGIN
          Result.Classification := MarkClassification2.Classification;
          Result."Quality Points" := Result."Credit Hours" * MarkClassification2."Grade Points";
          Result."Grade Points" := MarkClassification2."Grade Points";
          Result.Remark := MarkClassification2.Remark;
        END;
      END;
    END;

//16/06/14 END CODE

END ELSE BEGIN
  ExaminationSetup.TESTFIELD("Supplementary Pass Mark");
  ExaminationSetup.TESTFIELD("Supplementary Classification");
  ExaminationSetup.TESTFIELD("Supplementary Pass Remark");
  ExaminationSetup.TESTFIELD("Supplementary Fail Remark");
  ExaminationSetup.TESTFIELD("Suppl. Fail Classification");
  Result.CALCFIELDS("Exam Weight","Assessment Weight");
  //Make Sure Weights are not Zero
  IF Result."Exam Mark"<>0 THEN
    Result.TESTFIELD("Exam Weight");
  IF Result."Assessment Mark"<>0 THEN BEGIN
    Result.TESTFIELD("Assessment Weight");
    ProgrammeCourse2.SETRANGE("Teaching Class Code",Result."Result Class Code");
    ProgrammeCourse2.SETRANGE("Academic Year",Result."Academic Year");
    ProgrammeCourse2.SETRANGE("Programme Part",Result."Programme Part");
    ProgrammeCourse2.SETRANGE(Semester,Result.Semester);
    ProgrammeCourse2.SETRANGE(Code,Result.Course);
    IF ProgrammeCourse2.FINDFIRST THEN BEGIN
      ProgrammeCourse2.TESTFIELD("Examination Weight",0);
      ProgrammeCourse2.TESTFIELD("Other Examination Weight",0);
    END;
  END;
  IF Result."Other Exam Mark"<>0 THEN
    Result.TESTFIELD("Other Weight");

  IF NOT ((Result."Exam Weight"=0) AND (Result."Assessment Weight"=0) AND (Result."Other Weight"=0)) THEN BEGIN
    Result."Overall Mark":=((Result."Exam Mark"*Result."Exam Weight")+(Result."Assessment Mark"*Result."Assessment Weight")+
(Result."Other Exam Mark"*Result."Other Weight"))
    /(Result."Exam Weight"+Result."Assessment Weight"+Result."Other Weight");
    Result."Overall Mark" := ROUND(Result."Overall Mark",ExaminationSetup."Mark Rounding Precision",'=');
  END ELSE
    Result."Overall Mark":=0;

  IF NOT DptProgramme.GET(Result."Result Class Code") THEN
    ERROR(Text01);


   IF Result."Exam Mark" <> 0 THEN BEGIN

      //HT Edited 19/10/2018 --- Harmonising the lookup of classification to use Programme and not Class
      //OLD Code
      //MarkClassification2.SETRANGE("Programme Code",Result."Result Class Code");
      //New code
      MarkClassification2.SETRANGE("Programme Code",_ProgrammeClass."Programme Code");
      // End HT Edit


    MarkClassification2.SETRANGE(Level,DptProgramme.Level);
    MarkClassification2.SETRANGE("Assessment Type",MarkClassification2."Assessment Type"::Supplementary);
    IF MarkClassification2.FINDFIRST THEN BEGIN
      IF Result."Exam Mark" >= MarkClassification2."Mark Greater or Equal To" THEN BEGIN
        Result."Overall Mark" := MarkClassification2."Mark Greater or Equal To";
         Result."Quality Points" := Result."Credit Hours" * MarkClassification2."Grade Points";
         Result."Grade Points" := MarkClassification2."Grade Points";
        Result.Classification := ExaminationSetup."Supplementary Classification";
        Result.Remark := ExaminationSetup."Supplementary Pass Remark";
      END ELSE BEGIN
        Result."Overall Mark" := Result."Exam Mark";
        Result.Classification := ExaminationSetup."Suppl. Fail Classification";
        Result.Remark := ExaminationSetup."Supplementary Fail Remark";
        Result."Quality Points" := 0;
        Result."Grade Points" := 0;
      END;
    END ELSE BEGIN
      IF Result."Exam Mark" >= ExaminationSetup."Supplementary Pass Mark" THEN BEGIN
        Result."Overall Mark" := ExaminationSetup."Supplementary Pass Mark";
        Result.Classification := ExaminationSetup."Supplementary Classification";
        Result.Remark := ExaminationSetup."Supplementary Pass Remark";
        Result."Quality Points" := 0;
        Result."Grade Points" := 0;
      END ELSE BEGIN
        Result."Overall Mark" := Result."Exam Mark";
        Result.Classification := ExaminationSetup."Suppl. Fail Classification";
        Result.Remark := ExaminationSetup."Supplementary Fail Remark";
        Result."Quality Points" := 0;
        Result."Grade Points" := 0;
      END;
    END;
   END ELSE BEGIN

      //HT Edited 19/10/2018 --- Harmonising the lookup of classification to use Programme and not Class
      //OLD Code
      //MarkClassification2.SETRANGE("Programme Code",Result."Result Class Code");
      //New code
      MarkClassification2.SETRANGE("Programme Code",_ProgrammeClass."Programme Code");
      // End HT Edit

    MarkClassification2.SETRANGE(Level,DptProgramme.Level);
    MarkClassification2.SETRANGE("Assessment Type",MarkClassification2."Assessment Type"::Supplementary);
    IF MarkClassification2.FINDFIRST THEN BEGIN
      IF Result."Assessment Mark" >= MarkClassification2."Mark Greater or Equal To" THEN BEGIN
        Result."Overall Mark" := MarkClassification2."Mark Greater or Equal To";
        Result."Quality Points" := Result."Credit Hours" * MarkClassification2."Grade Points";
        Result."Grade Points" := MarkClassification2."Grade Points";
        Result.Classification := ExaminationSetup."Supplementary Classification";
        Result.Remark := ExaminationSetup."Supplementary Pass Remark";
      END ELSE BEGIN
        Result."Overall Mark" := Result."Assessment Mark";
        Result.Classification := ExaminationSetup."Suppl. Fail Classification";
        Result.Remark := ExaminationSetup."Supplementary Fail Remark";
        Result."Quality Points" := 0;
        Result."Grade Points" := 0;
      END;
    END ELSE BEGIN
      IF Result."Assessment Mark" >= ExaminationSetup."Supplementary Pass Mark" THEN BEGIN
        Result."Overall Mark" := ExaminationSetup."Supplementary Pass Mark";
        Result.Classification := ExaminationSetup."Supplementary Classification";
        Result.Remark := ExaminationSetup."Supplementary Pass Remark";
        Result."Quality Points" := 0;
        Result."Grade Points" := 0;
      END ELSE BEGIN
        Result."Overall Mark" := Result."Assessment Mark";
        Result.Classification := ExaminationSetup."Suppl. Fail Classification";
        Result.Remark := ExaminationSetup."Supplementary Fail Remark";
        Result."Quality Points" := 0;
        Result."Grade Points" := 0;
      END;
    END;
   END;
END;
