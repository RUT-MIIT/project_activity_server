import type { FC } from 'react';
import type { IWizardStepsProps } from '../../types/types';

import styles from './wizard-steps.module.scss';

export const WizardSteps: FC<IWizardStepsProps> = ({
	steps,
	currentStep,
	activeStep,
	onChange,
}) => {
	const handleChange = (id: number) => {
		if (id !== activeStep && id <= currentStep) {
			onChange(id);
		}
	};
	return (
		<ul className={styles.steps}>
			{steps.map((step) => (
				<li
					className={`
						${styles.step}
						${step.id <= currentStep ? styles.step_type_prev : ''}
						${step.id === activeStep ? styles.step_type_active : ''}
					`}
					key={step.id}
					onClick={() => handleChange(step.id)}>
					{step.name}
				</li>
			))}
		</ul>
	);
};
