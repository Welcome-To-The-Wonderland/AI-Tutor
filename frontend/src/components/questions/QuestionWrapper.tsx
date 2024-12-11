import React from "react";
import { MultipleChoiceQuestion } from "./MultipleChoiceQuestion";
import { FillInBlankQuestion } from "./FillInBlankQuestion";
import DragAndDropQuestion from "./DragAndDropQuestion";
import ComponentMatchQuestion from "./ComponentMatch";
import TrueFalseQuestion from "./TrueFalseQuestion";
import ShortAnswerQuestion from "./ShortAnswerQuestion";

export const QuestionWrapper = ({
  questionData,
  onSubmit,
  showHint,
  toggleHint,
  selectedOption,
  isAnswerCorrect,
  answerSubmitted,
  getOptionClass,
  onScreenshotCaptured,
}) => {
  switch (questionData.type) {
    case "multipleChoice":
      return (
        <MultipleChoiceQuestion
          question={questionData.question}
          options={questionData.options || []}
          hint={questionData.hint || ""}
          onSubmit={onSubmit}
          showHint={showHint}
          toggleHint={toggleHint}
          answer={questionData.answer || ""}
          selectedOption={selectedOption}
          isAnswerCorrect={isAnswerCorrect}
          answerSubmitted={answerSubmitted}
          getOptionClass={getOptionClass}
          image={questionData.image}
        />
      );
    case "fillInBlank":
      return (
        <FillInBlankQuestion
          question={questionData.question}
          hint={questionData.hint || ""}
          onSubmit={onSubmit}
          showHint={showHint}
          toggleHint={toggleHint}
          answer={questionData.answer || ""}
          selectedOption={selectedOption}
          isAnswerCorrect={isAnswerCorrect}
          answerSubmitted={answerSubmitted}
          getOptionClass={getOptionClass}
        />
      );
    case "dragAndDrop":
      return (
        <DragAndDropQuestion
          images={questionData.images || []}
          labels={questionData.labels || []}
          onSubmit={onSubmit}
          hint={questionData.hint || ""}
          onScreenshotCaptured={onScreenshotCaptured}
          showHint={showHint}
          toggleHint={toggleHint}
          answer={
            typeof questionData.answer === "object" ? questionData.answer : {}
          }
          selectedOption={selectedOption}
          isAnswerCorrect={isAnswerCorrect}
          answerSubmitted={answerSubmitted}
          getOptionClass={getOptionClass}
        />
      );
    case "componentMatch":
      return (
        <ComponentMatchQuestion
          question={questionData.question}
          centerImage={questionData.centerImage || ""}
          options={questionData.options || []}
          hint={questionData.hint || ""}
          onSubmit={onSubmit}
          showHint={showHint}
          toggleHint={toggleHint}
          onScreenshotCaptured={onScreenshotCaptured}
          answer={questionData.answer || ""}
          selectedOption={selectedOption}
          isAnswerCorrect={isAnswerCorrect}
          answerSubmitted={answerSubmitted}
          getOptionClass={getOptionClass}
        />
      );
    case "trueFalse":
      return (
        <TrueFalseQuestion
          question={questionData.question}
          hint={questionData.hint || ""}
          onSubmit={onSubmit}
          showHint={showHint}
          toggleHint={toggleHint}
          answer={questionData.answer || ""}
          selectedOption={selectedOption}
          isAnswerCorrect={isAnswerCorrect}
          answerSubmitted={answerSubmitted}
          getOptionClass={getOptionClass}
        />
      );
    case "shortAnswer":
      return (
        <ShortAnswerQuestion
          question={questionData.question}
          hint={questionData.hint || ""}
          onSubmit={onSubmit}
          showHint={showHint}
          toggleHint={toggleHint}
          answer={questionData.answer || ""}
          selectedOption={selectedOption}
          isAnswerCorrect={isAnswerCorrect}
          answerSubmitted={answerSubmitted}
          getOptionClass={getOptionClass}
        />
      );
    default:
      return null;
  }
};
