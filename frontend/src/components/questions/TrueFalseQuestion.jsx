import React, {useEffect, useState} from 'react';
import {Button} from '@/components/ui/button';
import {Label} from '@/components/ui/label';
import {Card, CardContent, CardHeader, CardTitle} from '@/components/ui/card';
import {HelpCircle} from 'lucide-react';

const TrueFalseQuestion = ({
  question,
  onSubmit,
  showHint,
  toggleHint,
  hint,
  answerSubmitted,
  isAnswerCorrect,
  selectedOption,
  getOptionClass,
}) => {
  const [selectedAnswer, setSelectedAnswer] = useState (selectedOption || '');
  const [submittedChoice, setSubmittedChoice] = useState ('');

  useEffect (
    () => {
      setSelectedAnswer (selectedOption);
    },
    [selectedOption]
  );

  useEffect (
    () => {
      console.log ('TrueFalseQuestion props:', {
        selectedOption,
        isAnswerCorrect,
        answerSubmitted,
      });
    },
    [selectedOption, isAnswerCorrect, answerSubmitted]
  );

  useEffect (
    () => {
      console.log ('Selected Answer:', selectedAnswer);
    },
    [selectedAnswer]
  );

  const handleAnswer = () => {
    if (selectedAnswer) {
      onSubmit (selectedAnswer);
      setSubmittedChoice (selectedAnswer);
    }
  };

  return (
    <Card className="w-full max-w-2xl mx-auto mb-6">
      <CardHeader>
        <CardTitle className="text-2xl font-bold text-gray-800">
          True/False Question
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <p className="text-lg text-gray-700">{question}</p>

        <div className="flex space-x-4">
          <div
            onClick={() => setSelectedAnswer ('true')}
            className={`cursor-pointer p-3 rounded-lg border text-center w-full ${selectedAnswer === 'true' ? 'border-black' : ''} ${answerSubmitted && selectedAnswer === 'true' && submittedChoice === 'true' ? (isAnswerCorrect ? 'bg-green-100 border-green-500' : 'bg-red-100 border-red-500') : getOptionClass ('true')}`}
            style={{borderColor: selectedAnswer === 'true' ? 'black' : ''}}
          >
            <Label htmlFor="true">True</Label>
          </div>
          <div
            onClick={() => setSelectedAnswer ('false')}
            className={`cursor-pointer p-3 rounded-lg border text-center w-full ${selectedAnswer === 'false' ? 'border-black' : ''} ${answerSubmitted && selectedAnswer === 'false' && submittedChoice === 'false' ? (isAnswerCorrect ? 'bg-green-100 border-green-500' : 'bg-red-100 border-red-500') : getOptionClass ('false')}`}
            style={{borderColor: selectedAnswer === 'false' ? 'black' : ''}}
          >
            <Label htmlFor="false">False</Label>
          </div>
        </div>

        <div className="flex space-x-2 items-center mt-4">
          <Button
            variant="outline"
            onClick={toggleHint}
            disabled={answerSubmitted && isAnswerCorrect}
          >
            {showHint ? 'Hide Hint' : 'Hint'}
          </Button>
          <Button
            onClick={handleAnswer}
            disabled={!selectedAnswer || (answerSubmitted && isAnswerCorrect)}
          >
            Submit
          </Button>
        </div>

        {showHint &&
          <p className="text-sm text-blue-600 bg-blue-50 p-3 rounded-lg mt-2 flex items-center">
            <HelpCircle className="inline mr-2" size={18} />
            {hint}
          </p>}

        {answerSubmitted &&
          <p className="mt-4 text-lg font-semibold">
            {isAnswerCorrect ? 'Correct!' : 'Incorrect, try again.'}
          </p>}
      </CardContent>
    </Card>
  );
};

export default TrueFalseQuestion;
