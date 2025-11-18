import type { ReactNode } from 'react';

export interface IWizardProps {
	id: string;
	children?: ReactNode;
}

export interface IWizardTitleProps {
	text: string;
}

export interface IWizardSubtitleProps {
	text: string;
}

export interface IWizardMainProps {
	children?: ReactNode;
}

export interface IWizardButtonsProps {
	children?: ReactNode;
}

export interface IStep {
	id: number;
	name: string;
	active: boolean;
}

export interface IWizardStepsProps {
	steps: IStep[];
	currentStep: number;
	activeStep: number;
	onChange: (step: number) => void;
}
