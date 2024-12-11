import React, { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import Image from "next/image";
import { DndProvider, useDrag, useDrop } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";
import { HelpCircle } from "lucide-react";
import html2canvas from "html2canvas";

interface DragAndDropQuestionProps {
  images: { component: string; image: string }[];
  labels: string[];
  onSubmit: (matches: { [key: string]: string | null }) => void;
  onScreenshotCaptured?: (image: string | null) => void;
  hint?: string;
  showHint: boolean;
  toggleHint: () => void;
  selectedOption: string;
  isAnswerCorrect: boolean;
  answer: { [key: string]: string };
  answerSubmitted: boolean;
}

const DraggableLabel: React.FC<{ label: string; isDisabled: boolean }> = ({
  label,
  isDisabled,
}) => {
  const [{ isDragging }, drag] = useDrag(
    () => ({
      type: "label",
      item: { label },
      collect: (monitor) => ({
        isDragging: !!monitor.isDragging(),
      }),
      canDrag: !isDisabled,
    }),
    [isDisabled]
  );

  return (
    <div
      ref={drag}
      className={`p-2 m-1 bg-blue-500 text-white rounded cursor-move ${
        isDragging ? "opacity-50" : "opacity-100"
      } ${isDisabled ? "cursor-not-allowed opacity-50" : ""}`}
    >
      {label}
    </div>
  );
};

const DroppableImage = ({
  component,
  image,
  matchedLabel,
  isCorrect,
  onDrop,
  isDisabled,
}) => {
  const [{ isOver }, drop] = useDrop(
    () => ({
      accept: "label",
      drop: (item) => onDrop(item.label),
      canDrop: () => !isDisabled,
      collect: (monitor) => ({
        isOver: !!monitor.isOver(),
      }),
    }),
    [isDisabled]
  );

  return (
    <div
      ref={drop}
      className={`relative p-2 border-2 rounded ${
        isCorrect === null
          ? "border-gray-300"
          : isCorrect
          ? "border-green-500 bg-green-100"
          : "border-red-500 bg-red-100"
      } ${isOver && !isDisabled ? "border-blue-500" : ""}`}
    >
      <Image
        src={image}
        alt={component}
        width={100}
        height={100}
        style={{ objectFit: "cover", width: "200px", height: "100px" }}
      />
      <div className="mt-2 text-center">
        {matchedLabel || "Drop label here"}
      </div>
    </div>
  );
};

const DragAndDropQuestion: React.FC<DragAndDropQuestionProps> = ({
  images,
  labels,
  onSubmit,
  hint,
  showHint,
  toggleHint,
  answer,
  selectedOption,
  isAnswerCorrect,
  onScreenshotCaptured,
  answerSubmitted,
}) => {
  const [matches, setMatches] = useState<{ [key: string]: string | null }>(
    images.reduce((acc, { component }) => ({ ...acc, [component]: null }), {})
  );
  const [isCorrectMap, setIsCorrectMap] = useState<{
    [key: string]: boolean | null;
  }>(
    images.reduce((acc, { component }) => ({ ...acc, [component]: null }), {})
  );
  const [submitClicked, setSubmitClicked] = useState(false);
  const [allCorrect, setAllCorrect] = useState(false);

  const handleDrop = (component: string, label: string) => {
    if (!submitClicked && !answerSubmitted) {
      setMatches((prev) => ({ ...prev, [component]: label }));
    }
  };

  const handleSubmit = async () => {
    const newIsCorrectMap = Object.keys(matches).reduce((acc, key) => {
      return { ...acc, [key]: matches[key] === answer[key] };
    }, {} as { [key: string]: boolean });

    setIsCorrectMap(newIsCorrectMap);

    const allCorrect = Object.values(newIsCorrectMap).every(
      (isCorrect) => isCorrect
    );
    setAllCorrect(allCorrect);
    setSubmitClicked(true);

    if (allCorrect && !answerSubmitted) {
      onSubmit(matches);
    }

    await new Promise((resolve) => setTimeout(resolve, 200));
    const image = await captureScreenshot();

    if (onScreenshotCaptured) {
      onScreenshotCaptured(image);
    } else {
      console.warn("onScreenshotCaptured is not defined.");
    }
  };

  useEffect(() => {
    if (answerSubmitted) {
      const correctState = Object.keys(answer).reduce((acc, key) => {
        acc[key] = true;
        return acc;
      }, {} as { [key: string]: boolean });
      setIsCorrectMap(correctState);
      setAllCorrect(true);
      setSubmitClicked(true);
    }
  }, [answerSubmitted, answer]);

  const captureScreenshot = async () => {
    console.log("Entered");
    const element = document.querySelector("#capture-section");
    if (!element) {
      console.error("Screenshot element not found");
      return;
    }

    try {
      const canvas = await html2canvas(element, {
        useCORS: true,
        backgroundColor: null,
        scale: 2,
      });
      const image = canvas.toDataURL("image/png");

      console.log("Screenshot capturexd:", image);
      return image;
    } catch (error) {
      console.error("Failed to capture screenshot:", error);
    }
  };

  return (
    <DndProvider backend={HTML5Backend}>
      <Card id="capture-section" className="w-full max-w-2xl mx-auto mb-6">
        <CardHeader>
          <CardTitle className="text-2xl font-bold text-gray-800">
            Drag and Drop Exercise
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-lg text-gray-700">
            Match the labels with the correct images:
          </p>

          <div className="grid grid-cols-2 gap-4">
            {images.map(({ component, image }) => (
              <DroppableImage
                key={component}
                component={component}
                image={image}
                matchedLabel={matches[component]}
                isCorrect={answerSubmitted ? true : isCorrectMap[component]}
                onDrop={(label) => handleDrop(component, label)}
                isDisabled={answerSubmitted || (submitClicked && allCorrect)}
              />
            ))}
          </div>

          <div className="flex flex-wrap justify-center">
            {labels.map((label) => (
              <DraggableLabel
                key={label}
                label={label}
                isDisabled={answerSubmitted || (submitClicked && allCorrect)}
              />
            ))}
          </div>

          <div className="space-y-2">
            {showHint && hint && (
              <p className="text-sm text-blue-600 bg-blue-50 p-3 rounded-lg">
                <HelpCircle className="inline mr-2" size={18} />
                {hint}
              </p>
            )}
            <Button
              variant="outline"
              onClick={toggleHint}
              disabled={answerSubmitted}
            >
              {showHint ? "Hide Hint" : "Hint"}
            </Button>
          </div>

          <Button
            onClick={handleSubmit}
            disabled={answerSubmitted || (submitClicked && allCorrect)}
          >
            Submit
          </Button>
        </CardContent>
      </Card>
    </DndProvider>
  );
};

export default DragAndDropQuestion;
