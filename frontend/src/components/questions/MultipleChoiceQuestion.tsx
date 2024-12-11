import React, { useEffect } from "react";
import { Button } from "@/components/ui/button";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { HelpCircle } from "lucide-react";
import Image from "next/image";

export const MultipleChoiceQuestion = ({
  question,
  options,
  hint,
  onSubmit,
  showHint,
  toggleHint,
  answer,
  selectedOption,
  isAnswerCorrect,
  answerSubmitted,
  getOptionClass,
  image,
}) => {
  const [localSelectedOption, setLocalSelectedOption] = React.useState(
    selectedOption || ""
  );

  useEffect(() => {
    setLocalSelectedOption(selectedOption);
  }, [selectedOption]);

  useEffect(() => {
    console.log("MultipleChoiceQuestion props:", {
      selectedOption,
      isAnswerCorrect,
      answerSubmitted,
    });
  }, [selectedOption, isAnswerCorrect, answerSubmitted]);

  const handleSubmit = () => {
    onSubmit(localSelectedOption);
  };

  return (
    <Card className="w-full max-w-2xl mx-auto mb-6">
      <CardHeader>
        <CardTitle className="text-2xl font-bold text-gray-800">
          Multiple Choice Question
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {image && (
          <div className="flex justify-center mb-4">
            <Image
              src={image}
              alt="Question related image"
              width={200}
              height={200}
              className="rounded-lg"
            />
          </div>
        )}

        <p className="text-lg text-gray-700">{question}</p>

        <RadioGroup
          value={localSelectedOption}
          onValueChange={setLocalSelectedOption}
          disabled={answerSubmitted && isAnswerCorrect}
        >
          {options.map((option) => (
            <div
              key={option}
              className={`flex items-center space-x-2 p-3 rounded-lg border ${getOptionClass(
                option
              )} cursor-pointer`}
              onClick={() => setLocalSelectedOption(option)}
            >
              <RadioGroupItem value={option} id={option} />
              <Label htmlFor={option} className="flex-grow">
                {option}
              </Label>
            </div>
          ))}
        </RadioGroup>

        <div className="flex space-x-2 items-center mt-4">
          <Button
            variant="outline"
            onClick={toggleHint}
            disabled={answerSubmitted && isAnswerCorrect}
          >
            {showHint ? "Hide Hint" : "Hint"}
          </Button>
          <Button
            onClick={handleSubmit}
            disabled={
              !localSelectedOption || (answerSubmitted && isAnswerCorrect)
            }
          >
            Submit
          </Button>
        </div>

        {showHint && hint && (
          <p className="text-sm text-blue-600 bg-blue-50 p-3 rounded-lg mt-2 flex items-center">
            <HelpCircle className="inline mr-2" size={18} />
            {hint}
          </p>
        )}

        {answerSubmitted && (
          <p className="mt-4 text-lg font-semibold">
            {isAnswerCorrect ? "Correct!" : "Incorrect, try again."}
          </p>
        )}
      </CardContent>
    </Card>
  );
};

export default MultipleChoiceQuestion;
