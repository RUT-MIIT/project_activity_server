import { useState, useMemo } from 'react';

export const useSteps = (totalSteps: number, initialStep = 1) => {
	const [activeStep, setActiveStep] = useState<number>(initialStep);

	const steps = useMemo(() => {
		return Array.from({ length: totalSteps }, (_, index) => ({
			id: index + 1,
			name: `Шаг ${index + 1}`,
			active: index + 1 === activeStep,
		}));
	}, [totalSteps, activeStep]);

	const goToNextStep = () => {
		setActiveStep((prev) => Math.min(prev + 1, totalSteps));
	};

	const goToPreviousStep = () => {
		setActiveStep((prev) => Math.max(prev - 1, 1));
	};

	const goToStep = (step: number) => {
		if (step >= 1 && step <= totalSteps) {
			setActiveStep(step);
		}
	};

	return {
		steps,
		activeStep,
		goToNextStep,
		goToPreviousStep,
		goToStep,
	};
};
