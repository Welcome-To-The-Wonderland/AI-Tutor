import React, {useEffect, useState} from 'react';
import {Button} from '@/components/ui/button';
import {Card, CardContent, CardHeader, CardTitle} from '@/components/ui/card';
import {HelpCircle} from 'lucide-react';

export const ShortAnswerQuestion = ({
  question,
  onSubmit,
  showHint,
  toggleHint,
  answerSubmitted,
}) => {
  const [userAnswer, setUserAnswer] = useState ('');
  const [feedback, setFeedback] = useState ('');
  const [isCorrect, setIsCorrect] = useState (null);
  const [submittedAnswer, setSubmittedAnswer] = useState ('');

  useEffect (
    () => {
      if (answerSubmitted) {
        setSubmittedAnswer (userAnswer);
      }
    },
    [answerSubmitted]
  );

  const handleAnswerChange = event => {
    setUserAnswer (event.target.value);
    setFeedback ('');
    setIsCorrect (null);
  };

  const handleSubmit = async () => {
    if (!userAnswer.trim ()) return;

    try {
      const response = await fetch (
        'http://127.0.0.1:8000/api/evaluate_question/',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify ({answer: userAnswer}),
        }
      );

      const result = await response.json ();

      if (result.correct) {
        setFeedback ('Correct!');
        setIsCorrect (true);
        onSubmit ('restart the computer');
      } else {
        setFeedback (result.feedback || 'Incorrect, try again.');
        setIsCorrect (false);
      }
    } catch (error) {
      console.error ('Error submitting answer:', error);
      setFeedback ('Something went wrong. Please try again.');
    }
  };

  const inputClasses = `
    w-full p-3 border rounded-lg 
    ${isCorrect === null ? 'border-gray-200' : ''} 
    ${isCorrect === true ? 'border-green-500 bg-green-100' : ''} 
    ${isCorrect === false ? 'border-red-500 bg-red-100' : ''}
  `;

  return (
    <Card className="w-full max-w-2xl mx-auto mb-6">
      <CardHeader>
        <CardTitle className="text-2xl font-bold text-gray-800">
          Short Answer Question
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <p className="text-lg text-gray-700">{question}</p>
        <input
          type="text"
          value={userAnswer}
          onChange={handleAnswerChange}
          disabled={isCorrect === true}
          className={inputClasses}
          placeholder="Type your answer here"
        />

        <div className="flex space-x-2 items-center">
          <Button
            variant="outline"
            onClick={toggleHint}
            disabled={isCorrect === true}
          >
            {showHint ? 'Hide Hint' : 'Hint'}
          </Button>
          <Button
            onClick={handleSubmit}
            disabled={!userAnswer.trim () || isCorrect === true}
          >
            Submit
          </Button>
        </div>

        {showHint &&
          question.hint &&
          <p className="text-sm text-blue-600 bg-blue-50 p-3 rounded-lg mt-2 flex items-center">
            <HelpCircle className="inline mr-2" size={18} />
            {question.hint}
          </p>}

        {feedback &&
          <p className={`mt-4 text-lg font-semibold`}>
            {feedback}
          </p>}
      </CardContent>
    </Card>
  );
};

export default ShortAnswerQuestion;
