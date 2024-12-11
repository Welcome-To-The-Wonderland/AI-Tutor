import React, { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import Image from "next/image";
import { HelpCircle } from "lucide-react";
import html2canvas from "html2canvas";

const ComponentMatchQuestion = ({
  question,
  centerImage,
  options,
  hint,
  onSubmit,
  showHint,
  toggleHint,
  answer,
  selectedOption,
  isAnswerCorrect,
  onScreenshotCaptured,
  answerSubmitted,
}) => {
  const [localAnswer, setLocalAnswer] = useState(selectedOption || "");

  useEffect(() => {
    setLocalAnswer(selectedOption);
  }, [selectedOption]);

  const handleSelectionChange = (newAnswer) => setLocalAnswer(newAnswer);

  const handleSubmit = async () => {
    await new Promise((resolve) => setTimeout(resolve, 200));
    const image = await captureScreenshot();

    if (onScreenshotCaptured) {
      onScreenshotCaptured(image);
    } else {
      console.warn("onScreenshotCaptured is not defined.");
    }

    await captureScreenshot();

    onSubmit(localAnswer);
  };

  const captureScreenshot = async () => {
    console.log("Entered captureScreenshot");
    const element = document.querySelector("#capture-section");

    if (!element) {
      console.error("Screenshot element not found");
      return;
    }

    const clonedElement = element.cloneNode(true) as HTMLElement;

    clonedElement.style.position = "absolute";
    clonedElement.style.top = "-9999px";
    clonedElement.style.left = "-9999px";
    document.body.appendChild(clonedElement);

    const clonedImages = clonedElement.querySelectorAll("img");
    clonedImages.forEach((img) => {
      const parent = img.parentElement;

      if (parent) {
        const { width, height } = parent.getBoundingClientRect();
        img.style.width = `$500px`;
        img.style.height = `$300px`;
        img.style.objectFit = "cover";
      }
    });

    try {
      const canvas = await html2canvas(clonedElement, {
        useCORS: true,
        backgroundColor: null,
        scale: 0.8,
      });

      const image = canvas.toDataURL("image/png");
      console.log("Screenshot captured:", image);
      return image;
    } catch (error) {
      console.error("Failed to capture screenshot:", error);
    } finally {
      clonedElement.remove();
    }
  };
  return (
    <Card id="capture-section" className="w-full max-w-2xl mx-auto mb-6">
      <CardHeader>
        <CardTitle className="text-2xl font-bold text-gray-800">
          Component Match Exercise
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <p className="text-lg text-gray-700">{question}</p>

        {centerImage && (
        <div className="flex justify-center mb-6">
          <Image
            src={centerImage}
            alt="Center Component"
            width={300}
            height={300}
            className="border-2 border-gray-300 rounded-lg"
          />
        </div>
        )}

        <RadioGroup
          value={localAnswer}
          onValueChange={handleSelectionChange}
          className="grid grid-cols-2 gap-4"
          disabled={answerSubmitted && isAnswerCorrect}
        >
          {options.map(({ label, image }) => (
            <div
              key={label}
              className={`flex flex-col items-center p-4 border rounded-lg ${
                answerSubmitted && label === localAnswer
                  ? isAnswerCorrect
                    ? "bg-green-100 border-green-500"
                    : "bg-red-100 border-red-500"
                  : "border-gray-300 hover:border-blue-500"
              }`}
              style={{
                width: "320px",
                margin: "0 auto", 
              }}
            >
              <div
                className="relative w-full h-32 mb-4" 
                style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  border: "1px solid #ccc",
                  borderRadius: "8px",
                  overflow: "hidden",
                }}
              >
                <Image
                  src={image}
                  alt={label}
                  layout="intrinsic"
                  width={170} 
                  height={170} 
                  style={{
                    objectFit: "contain", 
                  }}
                  className="rounded"
                />
              </div>
              <RadioGroupItem value={label} id={label} />
              <Label htmlFor={label} className="text-center mt-2 font-medium">
                {label}
              </Label>
            </div>
          ))}
        </RadioGroup>

        {showHint && (
          <p className="text-sm text-blue-600 bg-blue-50 p-3 rounded-lg">
            <HelpCircle className="inline mr-2" size={18} />
            {hint}
          </p>
        )}
        <div className="flex space-x-2">
          <Button
            onClick={toggleHint}
            variant="outline"
            disabled={answerSubmitted && isAnswerCorrect}
          >
            {showHint ? "Hide Hint" : "Hint"}
          </Button>
          <Button
            onClick={handleSubmit}
            disabled={!localAnswer || (answerSubmitted && isAnswerCorrect)}
          >
            Submit
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

export default ComponentMatchQuestion;
