import type { FC } from 'react';
import type { IWizardButtonsProps } from '../../types/types';

import styles from './wizard-buttons.module.scss';

export const WizardButtons: FC<IWizardButtonsProps> = ({ children }) => {
	return <div className={styles.container}>{children}</div>;
};
