// @ts-nocheck
// Enrichment.tsx

"use client";

import React, { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Send } from "lucide-react";
import Image from "next/image";
import { QuestionWrapper } from "@/components/questions/QuestionWrapper";
import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";

export default function Enrichment() {
  const [screenshot, setScreenshot] = useState<string | null>(null);
  const router = useRouter();
  const { user } = useAuth();
  console.log("User in Enrichment:", user);

  const [progress, setProgress] = useState(0);
  const [aiFeedback, setAiFeedback] = useState("");
  const [userReply, setUserReply] = useState("");
  const [waitingForAI, setWaitingForAI] = useState(false);
  const [conversation, setConversation] = useState([
    {
      role: "ai",
      content:
        "Hello! These are your enrichment exercises based on your performance.",
    },
  ]);
  const [unlockedModules, setUnlockedModules] = useState([]);
  const [modules, setModules] = useState([]);
  const [currentModuleIndex, setCurrentModuleIndex] = useState(0);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [questionStates, setQuestionStates] = useState({});
  const [moduleCompleted, setModuleCompleted] = useState(false);

  const [answeredQuestionsPerModule, setAnsweredQuestionsPerModule] = useState(
    {}
  );

  useEffect(() => {
    const fetchEnrichmentQuestions = async () => {
      try {
        const response = await fetch(
          `http://127.0.0.1:8000/api/enrichment_questions/?email=${user.email}`,
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
            },
          }
        );

        if (response.ok) {
          const data = await response.json();
          console.log("Fetched enrichment questions:", data);

          setModules(data.modules);
          const moduleNumbers = data.modules.map((module) => module.module);
          setUnlockedModules(moduleNumbers);

          const initialAnswered = {};
          data.modules.forEach((module) => {
            initialAnswered[module.module] = new Set();
          });
          setAnsweredQuestionsPerModule(initialAnswered);
        } else {
          console.error(
            "Failed to fetch enrichment questions:",
            response.statusText
          );
        }
      } catch (error) {
        console.error("Error fetching enrichment questions:", error);
      }
    };
    fetchEnrichmentQuestions();
  }, [user]);

  useEffect(() => {
    if (modules.length > 0) {
      const currentModule = modules[currentModuleIndex];
      const answeredCount =
        currentModule?.questions.filter((q) => q.answer_status === "Answered")
          .length || 0;
      const total = currentModule?.questions.length || 0;
      setProgress((answeredCount / total) * 100);
    }
  }, [answeredQuestionsPerModule, currentModuleIndex, modules]);

  const handleScreenshotCaptured = (image: string | null) => {
    if (image) {
      console.log("Screenshot captured in Enrichment:", image);
      const currentModule = modules[currentModuleIndex];
      const currentQuestion = currentModule.questions[currentQuestionIndex];
      setScreenshot(image);
      currentQuestion.image = image;

      if (currentQuestion.activity === "Identification") {
        currentQuestion.attempts += 1;
        currentModule.questions[currentQuestionIndex] = currentQuestion;
      }
      console.log("Current Question with Screenshot:", currentQuestion);
    } else {
      console.error("Failed to capture screenshot.");
    }
  };

  const handleQuestionSubmit = (option) => {
    const questionKey = `${currentModuleIndex}-${currentQuestionIndex}`;
    const currentModule = modules[currentModuleIndex];
    const currentQuestion = currentModule?.questions[currentQuestionIndex];

    if (!currentQuestion) return;

    if (!Array.isArray(currentQuestion.Previous_tries)) {
      currentQuestion.Previous_tries = [];
    }

    currentQuestion.Previous_tries.unshift(option);
    currentQuestion.attempts = currentQuestion.Previous_tries.length;

    console.log("Current Question:", currentQuestion);

    let isCorrect;
    if (currentQuestion.type === "dragAndDrop" && typeof option === "object") {
      const correctAnswer = currentQuestion.answer;
      isCorrect = Object.keys(correctAnswer).every(
        (key) => option[key] === correctAnswer[key]
      );
    } else if (currentQuestion.type === "trueFalse") {
      isCorrect = (option === "true") === currentQuestion.answer;
    } else {
      isCorrect = option === currentQuestion.answer;
    }

    setQuestionStates((prev) => ({
      ...prev,
      [questionKey]: {
        ...prev[questionKey],
        selectedOption: option,
        isCorrect,
        submitted: true,
      },
    }));

    if (isCorrect) {
      currentQuestion.answer_status = "Answered";
      setAnsweredQuestionsPerModule((prev) => {
        const updated = { ...prev };
        if (!updated[currentModule.module]) {
          updated[currentModule.module] = new Set();
        }
        updated[currentModule.module].add(currentQuestionIndex);
        return updated;
      });
    }

    setAiFeedback(isCorrect ? "Correct!" : "Try again.");
    setConversation((prev) => [
      ...prev,
      { role: "ai", content: isCorrect ? "Correct!" : "Try again." },
    ]);

    if (isCorrect) {
      setTimeout(() => {
        if (currentQuestionIndex === currentModule.questions.length - 1) {
          setModuleCompleted(true);
          if (currentModuleIndex < modules.length - 1) {
            setUnlockedModules((prev) => [...prev, currentModuleIndex + 2]);
          }
        } else {
          setCurrentQuestionIndex((prev) => prev + 1);
        }
      }, 1000);
    }
  };

  const getOptionClass = (option) => {
    const currentState =
      questionStates[`${currentModuleIndex}-${currentQuestionIndex}`] || {};
    if (currentState.selectedOption === option && currentState.submitted) {
      return currentState.isCorrect
        ? "bg-green-100 border-green-500"
        : "bg-red-100 border-red-500";
    }
    return "border-gray-200";
  };

  const toggleHint = () => {
    const questionKey = `${currentModuleIndex}-${currentQuestionIndex}`;
    setQuestionStates((prev) => ({
      ...prev,
      [questionKey]: {
        ...prev[questionKey],
        showHint: !prev[questionKey]?.showHint,
      },
    }));
  };

  const handleUserReply = async () => {
    if (waitingForAI || !userReply.trim()) return;
    setConversation([...conversation, { role: "user", content: userReply }]);
    console.log("User reply:", userReply);

    const currentModule = modules[currentModuleIndex];
    const currentQuestion = currentModule?.questions[currentQuestionIndex];

    if (!currentQuestion) {
      console.error("No question available to provide feedback for.");
      setAiFeedback("No question available for feedback.");
      setWaitingForAI(false);
      return;
    }

    setUserReply("");
    setWaitingForAI(true);

    const question_data = {
      activity: currentQuestion.activity,
      type: currentQuestion.type,
      question: currentQuestion.question,
      hint: currentQuestion.hint,
      answer: currentQuestion.answer,
      options: currentQuestion.options,
    };

    var student_progress = {};

    if (currentQuestion.activity === "Identification") {
      console.log(currentQuestion.image);
      student_progress = {
        answer_status: currentQuestion.answer_status || "Unanswered",
        Attempts: currentQuestion.attempts || 0,
        Image: currentQuestion.image,
      };
    } else {
      student_progress = {
        answer_status: currentQuestion.answer_status || "Unanswered",
        Attempts: currentQuestion.attempts || 0,
        Previous_tries: currentQuestion.Previous_tries || [],
      };
    }
    const assistant_info = {
      assistant_id: currentQuestion.assistant_id,
      thread_id: currentQuestion.thread_id,
    };

    const query = userReply.trim();

    console.log("Question State sent to AI:", currentQuestion);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/get_feedback/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question_data,
          student_progress,
          query,
          assistant_info,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        const feedback = data.feedback || "No feedback provided.";

        setConversation((prev) => [...prev, { role: "ai", content: feedback }]);
        setAiFeedback(feedback);

        console.log("AI Feedback:", feedback);
      } else {
        console.error("Failed to get feedback from AI:", response.statusText);
        setConversation((prev) => [
          ...prev,
          {
            role: "ai",
            content:
              "An error occurred while fetching feedback. Please try again.",
          },
        ]);
      }
    } catch (error) {
      console.error("Error calling get_feedback API:", error);
      setConversation((prev) => [
        ...prev,
        {
          role: "ai",
          content:
            "An error occurred while fetching feedback. Please try again.",
        },
      ]);
    } finally {
      setWaitingForAI(false);
    }
  };

  const currentModule = modules[currentModuleIndex];
  const currentQuestion = currentModule?.questions[currentQuestionIndex];
  const currentQuestionState =
    questionStates[`${currentModuleIndex}-${currentQuestionIndex}`] || {};

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <div className="w-64 bg-gray-800 text-white p-4 flex flex-col items-center">
        <h1 className="text-2xl font-bold mb-4 text-center">OverClockAI</h1>
        <div className="w-48 h-48 relative mb-6">
          <Image
            src="/Pic.png"
            alt="AI PC Building Tutor Icon"
            fill
            style={{ objectFit: "contain" }}
          />
        </div>
        <nav className="w-full">
          {modules.map((module, index) => (
            <div key={index}>
              {unlockedModules.includes(module.module) && (
                <Button
                  className="w-full mb-2"
                  onClick={() => {
                    setCurrentModuleIndex(index);
                    setCurrentQuestionIndex(0); // Reset to first question
                    setModuleCompleted(false);
                  }}
                >
                  {module.title} (Module {module.module})
                </Button>
              )}
            </div>
          ))}
        </nav>
      </div>

      {/* Main Content */}
      <div className="flex-1 p-8 overflow-auto">
        {/* Module Progress */}
        <div className="w-full max-w-2xl mx-auto mb-6">
          <div className="flex justify-between items-center mb-2">
            <h2 className="text-lg font-semibold">Progress</h2>
            <span className="text-sm font-medium text-gray-600">
              {answeredQuestionsPerModule[currentModule?.module]?.size || 0} of{" "}
              {currentModule?.questions.length || 0} questions answered
            </span>
          </div>
          <Progress value={progress} className="w-full" />
        </div>

        {moduleCompleted ? (
          <div className="max-w-2xl mx-auto text-center">
            <h2 className="text-2xl font-semibold mb-4">Module Completed!</h2>
            {currentModuleIndex < modules.length - 1 ? (
              <Button
                onClick={() => {
                  setCurrentModuleIndex((prev) => prev + 1);
                  setCurrentQuestionIndex(0);
                  setModuleCompleted(false);
                  setProgress(0);
                }}
              >
                Continue to Next Module
              </Button>
            ) : (
              <>
                <p>You have completed all enrichment modules!</p>
                <Button
                  className="mt-4"
                  onClick={() => {
                    router.push("/mockup");
                  }}
                >
                  Return Home
                </Button>
              </>
            )}
          </div>
        ) : (
          <>
            {/* Current Question */}
            {currentQuestion && (
              <QuestionWrapper
                questionData={currentQuestion}
                onSubmit={handleQuestionSubmit}
                onScreenshotCaptured={handleScreenshotCaptured}
                selectedOption={currentQuestionState.selectedOption || ""}
                getOptionClass={getOptionClass}
                showHint={currentQuestionState.showHint || false}
                toggleHint={toggleHint}
                isAnswerCorrect={currentQuestionState.isCorrect || false}
                answerSubmitted={currentQuestionState.submitted || false}
              />
            )}
            {/* Prev/Next Buttons */}
            {currentQuestion && (
              <div className="flex justify-between mt-4 max-w-2xl mx-auto">
                <Button
                  onClick={() => {
                    setCurrentQuestionIndex((prev) => prev - 1);
                  }}
                  disabled={currentQuestionIndex === 0}
                >
                  Prev
                </Button>
                <Button
                  onClick={() => {
                    setCurrentQuestionIndex((prev) => prev + 1);
                  }}
                  disabled={
                    currentQuestionIndex === currentModule.questions.length - 1
                  }
                >
                  Next
                </Button>
              </div>
            )}

            {/* AI Feedback Chat */}
            <Card className="w-full max-w-2xl mx-auto mt-6">
              <CardHeader>
                <CardTitle className="text-xl font-bold text-gray-800">
                  AI Feedback
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="max-h-48 overflow-y-auto space-y-2">
                  {conversation.map((message, index) => (
                    <div
                      key={index}
                      className={`p-3 rounded-lg ${
                        message.role === "ai"
                          ? "bg-blue-100 text-blue-800"
                          : "bg-gray-100 text-gray-800"
                      }`}
                    >
                      <p className="font-semibold">
                        {message.role === "ai" ? "AI" : "You"}:
                      </p>
                      {}
                      <ReactMarkdown
                        components={{
                          strong: ({ children }) => <>{children}</>,
                          em: ({ children }) => <>{children}</>,
                        }}
                      >
                        {message.content}
                      </ReactMarkdown>
                    </div>
                  ))}
                </div>
                <div className="flex space-x-2">
                  <Input
                    type="text"
                    placeholder="Type your reply..."
                    value={userReply}
                    onChange={(e) => setUserReply(e.target.value)}
                    className="flex-grow"
                    disabled={waitingForAI}
                  />
                  <Button onClick={handleUserReply} disabled={waitingForAI}>
                    Send <Send className="ml-2" size={18} />
                  </Button>
                </div>
              </CardContent>
            </Card>
          </>
        )}
      </div>
    </div>
  );
}
