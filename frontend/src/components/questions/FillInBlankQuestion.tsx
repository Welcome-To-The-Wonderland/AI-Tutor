import React, { useEffect, useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { HelpCircle } from "lucide-react";

export const FillInBlankQuestion = ({
  question,
  onSubmit,
  hint,
  showHint,
  toggleHint,
  answer,
  selectedOption,
  isAnswerCorrect,
  answerSubmitted,
}) => {
  const [localAnswer, setLocalAnswer] = useState(selectedOption || "");

  useEffect(() => {
    setLocalAnswer("");
  }, [question]);

  const handleSubmit = () => onSubmit(localAnswer.trim().toLowerCase());

  return (
    <Card className="w-full max-w-2xl mx-auto mb-6">
      <CardHeader>
        <CardTitle className="text-2xl font-bold text-gray-800">
          Fill in the Blank Exercise
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <p className="text-lg text-gray-700">{question}</p>
        <Input
          type="text"
          placeholder="Enter your answer"
          value={localAnswer}
          onChange={(e) => setLocalAnswer(e.target.value)}
          disabled={isAnswerCorrect}
          className={
            answerSubmitted
              ? isAnswerCorrect
                ? "bg-green-100"
                : "bg-red-100"
              : ""
          }
        />

        <div className="flex space-x-2 items-center">
          <Button
            variant="outline"
            onClick={toggleHint}
            disabled={isAnswerCorrect}
          >
            {showHint ? "Hide Hint" : "Hint"}
          </Button>
          <Button
            onClick={handleSubmit}
            disabled={!localAnswer.trim() || isAnswerCorrect}
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
      </CardContent>
    </Card>
  );
};
