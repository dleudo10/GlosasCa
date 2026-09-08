import { createContext, useContext, useState } from "react";
import type { GlosaResult } from "../feature/glosaEntry/entry.types";

type StepContextType = {
    step: number;
    glosas: GlosaResult[];
    nextStep: () => void;
    start: () => void;
    setGlosas: (glosas: GlosaResult[]) => void;
    setStep: (step: number) => void;
};

const StepContext = createContext<StepContextType | undefined>(undefined);

export const useStep = () => {
    const context = useContext(StepContext);

    if (!context) {
        throw new Error("useStep must be used within a StepProvider");
    }

    return context;
};

export const StepProvider: React.FC<{ children: React.ReactNode }> = ({
    children,
}) => {
    const [step, setStep] = useState<number>(0);
    const [glosas, setGlosas] = useState<GlosaResult[]>([]);

    const nextStep = () => {
        setStep((prevStep) => prevStep + 1);
    };

    const start = () => {
        setStep(0);
        setGlosas([]);
    };

    return (
        <StepContext.Provider
            value={{
                step,
                glosas,
                nextStep,
                start,
                setGlosas,
                setStep,
            }}
        >
            {children}
        </StepContext.Provider>
    );
};